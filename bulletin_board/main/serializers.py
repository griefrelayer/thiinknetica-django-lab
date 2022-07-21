from .models import Car, Thing, Service, Category, Seller, ContentType
from rest_framework import serializers


class ContentTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ContentType
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        seller = Seller(
            email=validated_data['email'],
            username=validated_data['username']
        )
        seller.set_password(validated_data['password'])
        seller.save()
        return seller


class CarSerializer(serializers.ModelSerializer):
    category = CategorySerializer
    seller = SellerSerializer
    depth = 1

    class Meta:
        model = Car
        exclude = ['ad_type']


class ThingSerializer(serializers.HyperlinkedModelSerializer):
    category = CategorySerializer
    seller = SellerSerializer
    depth = 1

    class Meta:
        model = Thing
        exclude = ['ad_type']
        # fields = '__all__'


class ServiceSerializer(serializers.HyperlinkedModelSerializer):
    category = CategorySerializer
    seller = SellerSerializer
    depth = 1

    class Meta:
        model = Service
        exclude = ['ad_type']

    def create(self, validated_data):
        return Seller.objects.create(**validated_data)