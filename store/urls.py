from django.urls import include, path
from rest_framework_nested import routers
from . import views

# URLConf
router = routers.DefaultRouter()
router.register(
    "products",
    views.ProductViewSet,
    basename="products",
)
router.register(
    "collections",
    views.CollectionViewSet,
    basename="collections",
)

products_router = routers.NestedDefaultRouter(
    router,
    "products",
    lookup="product",
)
products_router.register(
    "reviews",
    views.ReviewViewSet,
    basename="product-reviews",
)

# collection_router =

urlpatterns = [
    path(r"", include(router.urls)),
    path(r"", include(products_router.urls)),
]


# urlpatterns = [
#     path("products/", views.ProductList.as_view()),
#     path("products/<int:pk>/", views.product_detail),
#     path("collections/", views.collection_list),
#     path("collections/<int:pk>/", views.CollectionDetail.as_view()),
# ]
