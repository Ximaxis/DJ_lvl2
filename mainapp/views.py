from django.shortcuts import render, get_object_or_404
from django.conf import settings
import datetime
from .models import ProductCategory, Products
from basketapp.models import Basket
import random
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.

def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []


def get_hot_product():
    products = Products.objects.all()

    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    same_products = Products.objects.filter(category=hot_product.category). \
                        exclude(pk=hot_product.pk)[:3]

    return same_products

def main(request):
    title = "Главная"
    visit_date = datetime.datetime.now()
    products = Products.objects.all()[:5]
    basket = get_basket(request.user)
    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)
    content = {"title": title, "visit_date": visit_date, 'products': products, "basket": basket,
               "same_products": same_products,
                'hot_product': hot_product}

    return render(request, 'mainapp/index.html', content)


def products(request, slug):
    title = "Страница товара"
    get_product = get_object_or_404(Products, slug=slug)
    basket = get_basket(request.user)
    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)
    content = {
        "title": title,
        "same_products": same_products,
        "media_url": settings.MEDIA_URL,
        "get_product": get_product,
        'hot_product': hot_product,
        "basket": basket,
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
    links_menu = ProductCategory.objects.filter(is_active=True)
    basket = get_basket(request.user)
    if slug is not None:
        if slug == "all":
            category = {"slug": "all", "name": "все"}
            products = Products.objects.filter(is_active=True).order_by("price")
        else:
            category = get_object_or_404(ProductCategory, slug=slug)
            products = Products.objects.filter(category__slug=slug, is_active=True, category__is_active=True).order_by(
                "price"
            )
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
            "basket": basket,
        }
        return render(request, "mainapp/shop-list.html", content)
    content = {"title": title, "links_menu": links_menu,  'basket': basket}
    return render(request, 'mainapp/shop.html', content)


def checkout(request):
    title = "Хз как назвать"
    content = {"title": title}
    return render(request, 'mainapp/checkout.html', content)


def about(request):
    title = "О нас"
    content = {"title": title}
    return render(request, 'mainapp/about.html', content)


