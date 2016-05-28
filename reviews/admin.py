from django.contrib import admin

from reviews import models


class FeatureAdmin(admin.ModelAdmin):
    list_display = (
                    'id',
                    'name',

                    )


class ProductFeatureInline(admin.TabularInline):
    model = models.ProductFeature


class ProductAdmin(admin.ModelAdmin):
    inlines = [
                ProductFeatureInline,
                ]
    list_display = (
                    'id',
                    'type',
                    'name',
                    'description',
                    )


# class FeatureInline(admin.TabularInline):
#     model = models.ProductType.features.through


class ProductTypeAdmin(admin.ModelAdmin):
    # inlines = [
    #     FeatureInline,
    # ]
    list_display = (
                    'id',
                    'name',

                    )

admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductType, ProductTypeAdmin)
admin.site.register(models.Feature, FeatureAdmin)
