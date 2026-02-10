from rest_framework import serializers
from categories.models import Category, Product

from vendors.models import Vendor


class ProductCategorySerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(
        source='vendor.username',
        read_only=True
    )

    class Meta:
        model = Product
        fields = [
            'product_id', 'vendor_name', 'name', 'price', 'quantity',
            'available'
        ]


class CategorySerializer(serializers.ModelSerializer):
    products = ProductCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = [
            'category_id', 'name', 'description',
            'products', 'created_at', 'updated_at'
            ]


class VendorProductSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username')

    class Meta:
        model = Vendor
        fields = [
            'vendor_id', 'owner', 'name'
        ]


class ProductSerializer(serializers.ModelSerializer):
    vendor = VendorProductSerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            'product_id', 'vendor',
            'category', 'name', 'price', 'quantity',
            'available', 'created_at', 'updated_at'
        ]

