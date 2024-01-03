from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter

from .filters import ProductFilter
from .models import Cart, CartItem, Collection, OrderItem, Product, Review
from .serializers import (
    AddCartItemSerializers,
    CartSerializers,
    CollectionSerializer,
    ProductSerializer,
    ReviewSerializer,
    CartItemSerializers,
)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ["title", "description"]
    ordering_fields = ["unit_price", "last_update"]

    def get_serializer_context(self):
        context = {
            "request": self.request,
        }
        return context

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs["pk"]).count() > 0:
            error_message = {
                "error": "Product can't be deleted.",
            }
            return Response(error_message)
        return super().destroy(request, *args, **kwargs)


class ProductViewSetOld(ModelViewSet):
    #     serializer_class = ProductSerializer

    #     def get_queryset(self):
    #         queryset = Product.objects.all()
    #         collection_id = self.request.query_params.get("collection_id")
    #         if collection_id is not None:
    #             queryset = queryset.filter(collection_id=collection_id)
    #         return queryset

    #     def get_serializer_context(self):
    #         context = {
    #             "request": self.request,
    #         }
    #         return context

    #     def destroy(self, request, *args, **kwargs):
    #         if OrderItem.objects.filter(product_id=kwargs["pk"]).count() > 0:
    #             error_message = {
    #                 "error": "Product can't be deleted.",
    #             }
    #             return Response(error_message)
    #         return super().destroy(request, *args, **kwargs)
    pass


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count("products")).all()
    serializer_class = CollectionSerializer

    def get_serializer_context(self):
        context = {
            "request": self.request,
        }
        return context

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs["pk"]).count() > 0:
            error_message = {
                "error": "Collection can't be deleted. ",
            }
            return Response(error_message)
        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        queryset = Review.objects.filter(product_id=self.kwargs["product_pk"])
        return queryset

    def get_serializer_context(self):
        context = {
            "product_id": self.kwargs["product_pk"],
        }
        return context


class CartViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    serializer_class = CartSerializers

    def get_queryset(self):
        return Cart.objects.prefetch_related("items__product").all()

    def get_serializer_context(self):
        context = {
            "lorem": "lorem",
        }
        return context


class CartItemViewSet(ModelViewSet):
    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartItemSerializers
        return CartItemSerializers

    def get_queryset(self):
        queryset = CartItem.objects.filter(
            cart_id=self.kwargs["cart_pk"]
        ).select_related("product")
        return queryset

    def get_serializer_context(self):
        context = {
            "lorem": "lorem",
            "cart_pk": self.kwargs["cart_pk"],
        }
        return context
