from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse
from .models import Basket
from mainapp.models import Products
from mainapp.views import get_basket, get_hot_product, get_same_products


@login_required
def basket(request):
    title = "корзина"
    basket_items = Basket.objects.filter(user=request.user)
    basket = get_basket(request.user)
    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)
    content = {"title": title, "basket_items": basket_items, "media_url": settings.MEDIA_URL,
               "project_settings": settings, "basket": basket,
               "same_products": same_products,
                'hot_product': hot_product}
    return render(request, "mainapp/cart.html", content)


@login_required
def basket_add(request, slug):
    if "login" in request.META.get("HTTP_REFERER"):
        return HttpResponseRedirect(reverse("products:product", args=[slug]))
    product = get_object_or_404(Products, slug=slug)
    basket = Basket.objects.filter(user=request.user, product=product).first()

    if not basket:
        basket = Basket(user=request.user, product=product)

    basket.quantity += 1
    basket.save()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def basket_remove(request, pk):
    basket_record = get_object_or_404(Basket, pk=pk)
    basket_record.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def basket_edit(request, pk, quantity):
    if request.is_ajax():
        print(f"{pk} - {quantity}")
        new_basket_item = Basket.objects.get(pk=int(pk))

        if quantity > 0:
            new_basket_item.quantity = quantity
            new_basket_item.save()
        else:
            new_basket_item.delete()

        basket_items = Basket.objects.filter(user=request.user)

        content = {"basket_items": basket_items, "media_url": settings.MEDIA_URL}

        result = render_to_string("mainapp/includes/inc_basket_list.html", content)

        return JsonResponse({"result": result})
