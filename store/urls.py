from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path("products/", views.ProductList.as_view()),
    path("products/<int:pk>/", views.product_detail),
    path("collections/", views.collection_list),
    path("collections/<int:pk>/", views.CollectionDetail.as_view()),
]
