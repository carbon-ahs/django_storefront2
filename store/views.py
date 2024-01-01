from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter

from .filters import ProductFilter
from .models import Collection, OrderItem, Product, Review
from .serializers import CollectionSerializer, ProductSerializer, ReviewSerializer


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
        return Review.objects.filter(product_id=self.kwargs["product_pk"])

    def get_serializer_context(self):
        context = {
            "product_id": self.kwargs["product_pk"],
        }
        return context
