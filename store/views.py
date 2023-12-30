from itertools import product
from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Collection, OrderItem, Product, Review
from .serializers import CollectionSerializer, ProductSerializer, ReviewSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        context = {
            "request": self.request,
        }
        return context

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs["pk"]).count() > 0:
            error_message = {
                "error": "Product can't be deleted. ",
            }
            return Response(error_message)
        return super().destroy(request, *args, **kwargs)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count("products")).all()
    serializer_class = CollectionSerializer

    def get_serializer_context(self):
        context = {
            "request": self.request,
        }
        return context

    # def destroy(self, request, *args, **kwargs):
    #     if OrderItem.objects.filter(product_id=kwargs["pk"]).count() > 0:
    #         error_message = {
    #             "error": "Collection can't be deleted. ",
    #         }
    #         return Response(error_message)
    #     return super().destroy(request, *args, **kwargs)

    def delete(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk)
        if collection.products.count() > 0:
            error_message = {
                "error": "Collection can't be deleted. ",
            }
            return Response(error_message)


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
 