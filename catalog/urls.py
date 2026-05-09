from django.urls import path
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from .views import (
    CategoryProductsView,
    ContactsTemplateView,
    HomeListView,
    ProductCreateView,
    ProductDeleteView,
    ProductDetailView,
    ProductUnpublishView,
    ProductUpdateView,
)

app_name = 'catalog'

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('contacts/', ContactsTemplateView.as_view(), name='contacts'),

    path(
        'products/<int:pk>/',
        cache_page(60 * 15)(vary_on_cookie(ProductDetailView.as_view())),
        name='product_detail',
    ),

    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('products/<int:pk>/unpublish/', ProductUnpublishView.as_view(), name='product_unpublish'),

    path(
        'categories/<int:category_pk>/products/',
        CategoryProductsView.as_view(),
        name='category_products',
    ),
]