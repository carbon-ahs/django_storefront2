# from django.urls import URLPattern, include, path
from rest_framework_nested import routers
from . import views

# URLConf
router = routers.DefaultRouter()
router.register("products", views.ProductViewSet, basename="products")
router.register("collections", views.CollectionViewSet, basename="collections")
router.register("carts", views.CartViewSet, basename="carts")

products_router = routers.NestedDefaultRouter(
    router,
    "products",
    lookup="product",
)
products_router.register("reviews", views.ReviewViewSet, basename="product-reviews")

cart_router = routers.NestedDefaultRouter(
    router,
    "carts",
    lookup="cart",
)
cart_router.register("items", views.CartItemViewSet, basename="cart-items-details")
urlpatterns = router.urls + products_router.urls + cart_router.urls

# collection_router =

# urlpatterns = [
#     path(r"", include(router.urls)),
#     path(r"", include(products_router.urls)),
#     path(r"", include(cart_router.urls)),
# ]


# urlpatterns = [
#     path("products/", views.ProductList.as_view()),
#     path("products/<int:pk>/", views.product_detail),
#     path("collections/", views.collection_list),
#     path("collections/<int:pk>/", views.CollectionDetail.as_view()),
# ]
