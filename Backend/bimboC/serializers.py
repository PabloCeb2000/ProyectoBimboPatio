from rest_framework import serializers
from .models import (
    Product, Truck, OutGoingOrder, ActiveStock, ReserveStock, StockOBLPN, Remission, Pending
)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product', 'description']


class TruckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Truck
        fields = ['truck_number', 'location', 'status', 'size']

class OutGoingOrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )

    class Meta:
        model = OutGoingOrder
        fields = [
            'id', 'order_number', 'product', 'product_id', 'status', 'order_date', 
            'price', 'creation_date', 'detail', 'og_quantity', 'requested_quantity', 
            'assigned_quantity', 'packed_quantity'
        ]

class ActiveStockSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )

    class Meta:
        model = ActiveStock
        fields = ['id', 'product', 'product_id', 'available', 'assigned', 'total_active']

class ReserveStockSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )

    class Meta:
        model = ReserveStock
        fields = [
            'id', 'product', 'product_id', 'received', 'located', 'partially_assigned', 
            'assigned', 'lost', 'total_reserve'
        ]

class StockOBLPNSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )

    class Meta:
        model = StockOBLPN
        fields = ['id', 'product', 'product_id', 'picking', 'packed', 'loaded', 'total_oblpn']

class RemissionSerializer(serializers.ModelSerializer):
    box_number = TruckSerializer(read_only=True)
    box_number_id = serializers.PrimaryKeyRelatedField(
        queryset=Truck.objects.all(), source='box_number', write_only=True
    )

    class Meta:
        model = Remission
        fields = ['id', 'embark', 'box_number', 'box_number_id', 'date']


class PendingSerializer(serializers.ModelSerializer):
    embark = serializers.CharField(write_only=True)
    remission = RemissionSerializer(read_only=True)

    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )

    class Meta:
        model = Pending
        fields = [
            'id', 'close_dt', 'embark', 'remission', 'order', 'product', 'product_id',
            'send_dt', 'quantity', 'lpn', 'status'
        ]

    def create(self, validated_data):
        embark_value = validated_data.pop('embark')
        remission = Remission.objects.create(embark=embark_value)
        validated_data['embark'] = remission
        return super().create(validated_data)
    

class RemissionSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Remission
        fields = '__all__'

class TruckSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Truck
        fields = '__all__'

class PendingSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Pending
        fields = '__all__'
