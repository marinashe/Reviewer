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


class ProductTypeAdmin(admin.ModelAdmin):
    list_display = (
                'id',
                'name',

                )


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


class ScoreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


class ReviewScoreInline(admin.TabularInline):
    model = models.ReviewScore


class ReviewAdmin(admin.ModelAdmin):
    inlines = [
        ReviewScoreInline,
    ]
    date_hierarchy = 'time'
    list_filter = (
        'product__type__name',
    )
    list_display = (
        'time',
        'get_type',
        'product',
        'user',
        'text',

    )

    def get_type(self, obj):
        return obj.product.type

    get_type.short_description = 'Type'
    get_type.admin_order_field = 'product__type'


admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductType, ProductTypeAdmin)
admin.site.register(models.Feature, FeatureAdmin)
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Score, ScoreAdmin)
admin.site.register(models.Review, ReviewAdmin)


