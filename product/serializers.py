from rest_framework import serializers
from django.db.models import Avg
from .models import Category, Product, Review, User, ConfirmationCode
from django.contrib.auth.hashers import make_password, check_password



class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = User.objects.create(**validated_data)
        ConfirmationCode.objects.create(user=user)
        return user

class ConfirmCodeSerializer(serializers.Serializer):
    username = serializers.CharField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            user = User.objects.get(username=data['username'])
            if user.confirmation_code.code != data['code']:
                raise serializers.ValidationError("Неверный код подтверждения.")
            return data
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден.")

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            user = User.objects.get(username=data['username'])
            if not user.is_active:
                raise serializers.ValidationError("Пользователь не подтверждён.")
            if not check_password(data['password'], user.password):
                raise serializers.ValidationError("Неверный пароль.")
            return user
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден.")


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = '__all__'

    def get_products_count(self, obj):
        return Category.objects.all().count()

    def validate_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Название категории должно быть длиннее 1 символа.")
        return value

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

        def validate_text(self, value):
            if not value.strip():
                raise serializers.ValidationError("Текст отзыва не может быть пустым")
            if len(value) > 2000:
                raise serializers.ValidationError("Текст отзыва слишком длинный (максимум 2000 символов)")
            return value

        def validate_rating(self, value):
            if value < 1 or value > 5:
                raise serializers.ValidationError("Рейтинг должен быть от 1 до 5")
            return value


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Название товара не может быть пустым.")
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Цена должна быть положительной.")
        return value

class ProductWithReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_average_rating(self, obj):
        avg_rating = obj.reviews.aggregate(Avg('stars'))['stars__avg']
        return round(avg_rating or 0, 2)


    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Рейтинг должен быть от 1 до 5.")
        return value

    def validate_text(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Текст отзыва должен содержать минимум 10 символов.")
        return value









