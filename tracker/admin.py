from django.contrib import admin

from .models import *

class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "description")

class CompanyOrderAdmin(admin.ModelAdmin):
    list_display = ("name", "id")

class OrderAdmin(admin.ModelAdmin):
    list_display = ("recipe", "id")

class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "description")

class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "description")

class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = ("recipe", "amount", 'ingredient')

admin.site.register(Company, CompanyAdmin)
admin.site.register(CompanyOrder, CompanyOrderAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Recipe, RecipeAdmin) 
admin.site.register(Ingredient, IngredientAdmin) 
admin.site.register(IngredientAmount, IngredientAmountAdmin) 