from django.shortcuts import get_object_or_404, get_list_or_404
from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Collection, Product
from .serializers import CollectionSerializer, ProductSerializer


class ProductList(ListCreateAPIView):
    queryset = get_list_or_404(Product)
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        context = {
            "request": self.request,
        }
        return context


class ProductListAPIView(APIView):
    def get(self, request):
        queryset = get_list_or_404(Product)
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductDetailAPIView(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
def product_list(request):
    if request.method == "GET":
        queryset = get_list_or_404(Product)
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

        # print(serializer.validated_data)
        # if serializer.is_valid():
        #     return Response("ok")
        # else:
        #     return Response(
        #         serializer.errors,
        #         status=status.HTTP_400_BAD_REQUEST,
        #     )


@api_view(["GET", "PUT", "DELETE"])
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.method == "GET":
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == "DELETE":
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(products_count=Count("products")).all()
    serializer_class = CollectionSerializer


@api_view(["GET", "POST"])
def collection_list(request):
    if request.method == "GET":
        queryset = Collection.objects.annotate(products_count=Count("products"))
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CollectionDetail(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.annotate(product_count=Count("products"))

    serializer_class = CollectionSerializer

    def delete(self, request, pk):
        """
        docstring
        """
        collection = get_object_or_404(
            Collection.objects.annotate(product_count=Count("products")), pk=pk
        )
        if collection.products.count() > 0:
            error_message = {
                "error": "Collection can't be deleted. ",
            }
            return Response(error_message)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "PUT", "DELETE"])
def collection_detail(request, id):
    collection = get_object_or_404(
        Collection.objects.annotate(product_count=Count("products")), pk=id
    )
    if request.method == "GET":
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == "DELETE":
        if collection.products.count() > 0:
            error_message = {
                "error": "Collection can't be deleted. ",
            }
            return Response(error_message)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
