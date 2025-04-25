from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from .models import Category, Product, Review, User, ConfirmationCode
from django.contrib.auth.hashers import check_password
import random
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ReviewSerializer,
    ProductWithReviewsSerializer,
    LoginSerializer,
    RegisterSerializer,
    ConfirmCodeSerializer,
)


class RegistrationAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = User.objects.create(username=username, email=email, password=password, is_active=False)

        code = f"{random.randint(100000, 999999)}"
        ConfirmationCode.objects.create(user=user, code=code)

        return Response({'user_id': user.id, 'confirmation_code': code}, status=status.HTTP_201_CREATED)


class ConfirmUserAPIView(APIView):
    def post(self, request):
        serializer = ConfirmCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        code = serializer.validated_data['code']

        try:
            user = User.objects.get(username=username)
            if user.confirmation_code.code != code:
                return Response({'error': 'Неверный код'}, status=status.HTTP_400_BAD_REQUEST)

            user.is_active = True
            user.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'message': 'Пользователь подтверждён', 'token': token.key})

        except User.DoesNotExist:
            return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)


class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        try:
            user = User.objects.get(username=username)
            if not user.is_active:
                return Response({'error': 'Пользователь не подтверждён'}, status=status.HTTP_403_FORBIDDEN)
            if not check_password(password, user.password):
                return Response({'error': 'Неверный пароль'}, status=status.HTTP_400_BAD_REQUEST)

            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})

        except User.DoesNotExist:
            return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)


class CategoryListCreateAPIView(CreateAPIView, ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailAPIView(UpdateAPIView, DestroyAPIView, RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'


class ProductListCreateAPIView(CreateAPIView, ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailAPIView(UpdateAPIView, DestroyAPIView, RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'


class ReviewListCreateAPIView(CreateAPIView, ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewDetailAPIView(UpdateAPIView, DestroyAPIView, RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'id'


class ProductWithReviewsAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        data = ProductWithReviewsSerializer(products, many=True).data
        return Response(data)


class CategoryDetailOnlyAPIView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'


class ProductDetailOnlyAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'


class ReviewDetailOnlyAPIView(RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'id'