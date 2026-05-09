from typing import Final

from django.conf import settings
from django.core.cache import cache

from .models import Product

PRODUCT_LIST_CACHE_KEY: Final[str] = 'catalog:products:all'
PRODUCTS_BY_CATEGORY_CACHE_KEY: Final[str] = 'catalog:products:category:{category_id}'


def get_cache_timeout() -> int:
    return int(getattr(settings, 'CACHE_TTL', 900))


def get_product_list() -> list[Product]:
    """Возвращает кешированный список всех продуктов."""
    products = cache.get(PRODUCT_LIST_CACHE_KEY)

    if products is None:
        products = list(
            Product.objects.select_related('category', 'owner').order_by('-created_at')
        )
        cache.set(PRODUCT_LIST_CACHE_KEY, products, get_cache_timeout())

    return products


def get_products_by_category(category_id: int) -> list[Product]:
    """Возвращает кешированный список продуктов указанной категории."""
    cache_key = PRODUCTS_BY_CATEGORY_CACHE_KEY.format(category_id=category_id)
    products = cache.get(cache_key)

    if products is None:
        products = list(
            Product.objects.select_related('category', 'owner')
            .filter(category_id=category_id)
            .order_by('-created_at')
        )
        cache.set(cache_key, products, get_cache_timeout())

    return products


def clear_product_cache(category_id: int | None = None) -> None:
    """Очищает кеш списка продуктов и, при необходимости, кеш категории."""
    cache.delete(PRODUCT_LIST_CACHE_KEY)

    if category_id is not None:
        cache.delete(PRODUCTS_BY_CATEGORY_CACHE_KEY.format(category_id=category_id))