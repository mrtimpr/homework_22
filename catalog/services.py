from typing import Final

from django.conf import settings
from django.core.cache import cache

from .models import Product

PRODUCTS_CACHE_KEY: Final[str] = 'products'
CATEGORY_PRODUCTS_CACHE_KEY: Final[str] = 'category_{id}'


def get_cache_ttl() -> int:
    return int(getattr(settings, 'CACHE_TTL', 900))


def get_product_list() -> list[Product]:
    products = cache.get(PRODUCTS_CACHE_KEY)

    if products is None:
        products = list(
            Product.objects.select_related('category', 'owner').order_by('-created_at')
        )
        cache.set(PRODUCTS_CACHE_KEY, products, get_cache_ttl())

    return products


def get_products_by_category(category_id: int) -> list[Product]:
    cache_key = CATEGORY_PRODUCTS_CACHE_KEY.format(id=category_id)
    products = cache.get(cache_key)

    if products is None:
        products = list(
            Product.objects.select_related('category', 'owner')
            .filter(category_id=category_id)
            .order_by('-created_at')
        )
        cache.set(cache_key, products, get_cache_ttl())

    return products


def clear_product_cache(category_id: int | None = None) -> None:
    cache.delete(PRODUCTS_CACHE_KEY)

    if category_id is not None:
        cache.delete(CATEGORY_PRODUCTS_CACHE_KEY.format(id=category_id))