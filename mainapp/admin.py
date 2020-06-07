from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import *


class ProductsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Products
        fields = '__all__'


class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    form = ProductsAdminForm


class ProductCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Products, ProductsAdmin)
