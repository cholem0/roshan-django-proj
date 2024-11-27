from django.urls import path
from .views import ProductsList, ProductUpdate, TokenWithCookieView, TokenRefreshWithCookieView, LogoutView, \
    CategoryList, CategoryUpdate, CategoryProductList, CartAddProduct, \
    CartRemoveProduct, CartList, CartClear

urlpatterns = [
    path('auth/token/', TokenWithCookieView.as_view(), name='token_obtain_pair'),
    path('auth/token/logout/', LogoutView.as_view(), name='logout'),
    # path('auth/token/refresh/', TokenRefreshWithCookieView.as_view(), name='token_refresh'),
    path('products/' , ProductsList.as_view() , name ="list_products"),
    path('products/<int:pk>' , ProductUpdate.as_view() , name = "update_products"),
    path('categories/', CategoryList.as_view(), name="list_categories"),
    path('categories/<int:pk>', CategoryUpdate.as_view(), name="update_categories"),
    path('categories/<int:id>/products' , CategoryProductList.as_view() , name="products_of_category"),
    path('cart/add/<int:product_id>/', CartAddProduct.as_view(), name='add-to-cart'),
    path('cart/remove/<int:product_id>/', CartRemoveProduct.as_view(), name='remove-from-cart'),
    path('cart/', CartList.as_view(), name='view-cart'),
    path('cart/clear/', CartClear.as_view(), name='clear-cart'),
]
