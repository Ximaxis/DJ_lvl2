from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.core.cache import cache
from django.views.decorators.cache import cache_page
import datetime
from .models import ProductCategory, Products
import random
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.

def get_links_menu():
    if settings.LOW_CACHE:
        key = "links_menu"
        links_menu = cache.get(key)
        if links_menu is None:
            # print(f'caching {key}')
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_category(slug):
    if settings.LOW_CACHE:
        key = f"category_{slug}"
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, slug=slug)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, slug=slug)



def get_products():
    if settings.LOW_CACHE:
        key = "products"
        products = cache.get(key)
        if products is None:
            products = Products.objects.filter(is_active=True, category__is_active=True).select_related("category")
            cache.set(key, products)
        return products
    else:
        return Products.objects.filter(is_active=True, category__is_active=True).select_related("category")


def get_productq(slug):
    if settings.LOW_CACHE:
        key = {slug}
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Products, slug=slug)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Products, slug=slug)


def get_products_orederd_by_price():
    if settings.LOW_CACHE:
        key = "products_orederd_by_price"
        products = cache.get(key)
        if products is None:
            products = Products.objects.filter(is_active=True, category__is_active=True).order_by("price")
            cache.set(key, products)
        return products
    else:
        return Products.objects.filter(is_active=True, category__is_active=True).order_by("price")


def get_products_in_category_orederd_by_price(slug):
    if settings.LOW_CACHE:
        key = f"products_in_category_orederd_by_price_{slug}"
        products = cache.get(key)
        if products is None:
            products = Products.objects.filter(category__slug=slug, is_active=True, category__is_active=True).order_by(
                "price"
            )
            cache.set(key, products)
        return products
    else:
        return Products.objects.filter(category__slug=slug, is_active=True, category__is_active=True).order_by("price")




def get_hot_product_list():
    products = get_products()
    hot_product = random.sample(list(products), 1)[0]
    hot_list = products.exclude(slug=hot_product.slug)[:3]
    return (hot_product, hot_list)


# def get_hot_product():
#     products = Products.objects.all()
#     return random.sample(list(products), 1)[0]
#
#
# def get_same_products(hot_product):
#     same_products = Products.objects.filter(is_active=True, category=hot_product.category). \
#                         exclude(pk=hot_product.pk)[:3]
#     return same_products


#@cache_page(600)
def main(request):
    title = "Главная"
    visit_date = datetime.datetime.now()
    products = get_products()[:6]
    hot_product, same_products = get_hot_product_list()
    content = {"title": title,
               "visit_date": visit_date,
               'products': products,
               "same_products": same_products,
               'hot_product': hot_product}

    return render(request, 'mainapp/index.html', content)


def products(request, slug):
    title = "Страница товара"
    get_product = get_productq(slug)
    hot_product, same_products = get_hot_product_list()
    content = {
        "title": title,
        "same_products": same_products,
        "media_url": settings.MEDIA_URL,
        "get_product": get_product,
        'hot_product': hot_product,
    }
    return render(request, 'mainapp/product-single.html', content)


def contacts(request):
    title = "Контактные данные"
    content = {"title": title}
    return render(request, 'mainapp/contact.html', content)


def blogsingle(request):
    title = "Запись в блоге"
    content = {"title": title}
    return render(request, 'mainapp/blog-single.html', content)


def blog(request):
    title = "Блог"
    content = {"title": title}
    return render(request, 'mainapp/blog.html', content)


def shop(request, slug="all", page=1):
    title = "Каталог товаров"
    links_menu = get_links_menu()
    if slug is not None:
        if slug == "all":
            category = {"slug": "all", "name": "все"}
            products = get_products_orederd_by_price()
        else:
            category = get_category(slug)
            products = get_products_in_category_orederd_by_price(slug)
        paginator = Paginator(products, 4)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)
        content = {
            "title": title,
            "links_menu": links_menu,
            "category": category,
            "products": products_paginator,
            "media_url": settings.MEDIA_URL,
        }
        return render(request, "mainapp/shop-list.html", content)
    content = {"title": title, "links_menu": links_menu}
    return render(request, 'mainapp/shop.html', content)


def checkout(request):
    title = "Хз как назвать"
    content = {"title": title}
    return render(request, 'mainapp/checkout.html', content)


@cache_page(600)
def about(request):
    title = "О нас"
    content = {"title": title}
    return render(request, 'mainapp/about.html', content)


