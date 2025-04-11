from rest_framework import serializers
from django.db.models import Avg
from .models import Category, Product, Review


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = '__all__'

    def get_products_count(self, obj):
        return Category.objects.all().count()

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductWithReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_average_rating(self, obj):
        avg_rating = obj.reviews.aggregate(Avg('stars'))['stars__avg']
        return round(avg_rating or 0, 2)









