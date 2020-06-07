from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import HttpResponseRedirect, get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
import datetime
from adminapp.forms import ProductCategoryEditForm, ProductEditForm, ShopUserAdminEditForm
from authnapp.forms import ShopUserRegisterForm
from authnapp.models import ShopUser
from mainapp.models import Products, ProductCategory


@user_passes_test(lambda u: u.is_superuser)
def admin_main(request):
    response = redirect("my_admin:users")
    return response


class UsersListView(LoginRequiredMixin, ListView):
    model = ShopUser
    template_name = "adminapp/users.html"


@user_passes_test(lambda u: u.is_superuser)
def users(request):
    title = "Admin/Users"
    users_list = ShopUser.objects.all().order_by("-is_active", "-is_superuser", "-is_staff", "username")
    content = {"title": title, "objects": users_list, "media_url": settings.MEDIA_URL}
    return render(request, "adminapp/users.html", content)


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    title = "Users/Create"

    if request.method == "POST":
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse("my_admin:users"))
    else:
        user_form = ShopUserRegisterForm()

    content = {"title": title, "update_form": user_form, "media_url": settings.MEDIA_URL}

    return render(request, "adminapp/user_update.html", content)


@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    title = "Users/Edit"

    edit_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == "POST":
        edit_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse("my_admin:user_update", args=[edit_user.pk]))
    else:
        edit_form = ShopUserAdminEditForm(instance=edit_user)

    content = {"title": title, "update_form": edit_form, "media_url": settings.MEDIA_URL}

    return render(request, "adminapp/user_update.html", content)


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    title = "Users/DELETE"

    user = get_object_or_404(ShopUser, pk=pk)

    if request.method == "POST":
        # user.delete()
        # Instead delete we will set users inactive
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse("my_admin:users"))

    content = {"title": title, "user_to_delete": user, "media_url": settings.MEDIA_URL}

    return render(request, "adminapp/user_delete.html", content)


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    title = "Admin/Category"
    categories_list = ProductCategory.objects.all()
    content = {"title": title, "objects": categories_list, "media_url": settings.MEDIA_URL}
    return render(request, "adminapp/categories.html", content)


class ProductCategoryCreateView(LoginRequiredMixin, CreateView):
    model = ProductCategory
    template_name = "adminapp/category_update.html"
    success_url = reverse_lazy("my_admin:categories")
    fields = "__all__"


class ProductCategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = ProductCategory
    template_name = "adminapp/category_update.html"
    success_url = reverse_lazy("my_admin:categories")
    fields = "__all__"
    foo = "bar"

    def get_context_data(self, **kwargs):
        context = super(ProductCategoryUpdateView, self).get_context_data(**kwargs)
        context["title"] = "Category/Edit"
        return context


class ProductCategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = ProductCategory
    template_name = "adminapp/category_delete.html"
    success_url = reverse_lazy("my_admin:categories")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


@user_passes_test(lambda u: u.is_superuser)
def products(request, slug):
    title = "Admin/Product"
    category = get_object_or_404(ProductCategory, slug=slug)
    products_list = Products.objects.filter(category__slug=slug).order_by("slug")
    content = {"title": title, "category": category, "objects": products_list, "media_url": settings.MEDIA_URL}
    return render(request, "adminapp/products.html", content)



@user_passes_test(lambda u: u.is_superuser)
def product_create(request, slug):
    title = "Product/create"
    category = get_object_or_404(ProductCategory, slug=slug)

    if request.method == "POST":
        product_form = ProductEditForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse("my_admin:products", args=[slug]))
    else:
        # set initial value for form
        product_form = ProductEditForm(initial={"category": category})

    content = {"title": title, "update_form": product_form, "category": category, "media_url": settings.MEDIA_URL}
    return render(request, "adminapp/product_update.html", content)


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Products
    template_name = "adminapp/product_read.html"


@user_passes_test(lambda u: u.is_superuser)
def product_update(request, slug):
    title = "Product/update"
    edit_product = get_object_or_404(Products, slug=slug)

    if request.method == "POST":
        edit_form = ProductEditForm(request.POST, request.FILES, instance=edit_product)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse("my_admin:product_update", args=[edit_product.slug]))
    else:
        edit_form = ProductEditForm(instance=edit_product)

    content = {
        "title": title,
        "update_form": edit_form,
        "category": edit_product.category,
        "media_url": settings.MEDIA_URL,
    }
    return render(request, "adminapp/product_update.html", content)


@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, slug):
    title = "Product/delete"
    product = get_object_or_404(Products, slug=slug)

    if request.method == "POST":
        product.is_active = False
        product.save()
        return HttpResponseRedirect(reverse("my_admin:products", args=[product.category.slug]))

    content = {"title": title, "product_to_delete": product, "media_url": settings.MEDIA_URL}
    return render(request, "adminapp/product_delete.html", content)
