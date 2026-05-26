from rest_framework import serializers
from .models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'description')  # подставь реальные поля модели


class ProductPositionSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = StockProduct
        fields = ('product', 'price')


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True, write_only=True)

    class Meta:
        model = Stock
        fields = ('id', 'address', 'positions')

    def create(self, validated_data):
        positions = validated_data.pop('positions')

        stock = Stock.objects.create(**validated_data)

        for position in positions:
            StockProduct.objects.create(
                stock=stock,
                product=position['product'],
                price=position['price']
            )

        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')

        stock = super().update(instance, validated_data)

        StockProduct.objects.filter(stock=instance).delete()

        for position in positions:
            StockProduct.objects.create(
                stock=stock,
                product=position['product'],
                price=position['price']
            )

        return stock