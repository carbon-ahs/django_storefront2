from decimal import Decimal
from rest_framework import serializers

from store.models import Cart, CartItem, Product, Collection, Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            "id",
            "date",
            "name",
            "description",
        ]

    def create(self, validated_data):
        product_id = self.context["product_id"]
        return Review.objects.create(
            product_id=product_id,
            **validated_data,
        )


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = [
            "id",
            "title",
            "products_count",
        ]

    products_count = serializers.IntegerField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "description",
            "slug",
            "inventory",
            "unit_price",
            "collection",
            "price_with_tax",
        ]

    price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "unit_price"]


class CartItemSerializers(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unit_price

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "total_price"]


class CartSerializers(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializers(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart: Cart):
        total_price = 0
        for item in cart.items.all():
            total_price_item = item.quantity * item.product.unit_price
            total_price = total_price + total_price_item
        return total_price

    class Meta:
        model = Cart
        fields = ["id", "items", "total_price"]


class AddCartItemSerializers(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError("No product with this ID")
        return value

    def save(self, **kwargs):
        cart_id = self.context["cart_pk"]
        product_id = self.validated_data["product_id"]
        qty = self.validated_data["quantity"]

        try:
            # Update exiting item
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += qty
            cart_item.save()
            self.instance = cart_item

        except CartItem.DoesNotExist:
            # create Item
            cart_item = CartItem.objects.create(cart_id=cart_id, **self.validated_data)
            self.instance = cart_item

        return self.instance

    class Meta:
        model = CartItem
        fields = ["id", "product_id", "quantity"]
