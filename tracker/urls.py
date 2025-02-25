from django.urls import path
from .views import *
urlpatterns = [
path('company', CompanyListView.as_view(), name='company_list'),
path('company/create', CompanyCreateView.as_view(), name='company_create'),
path('company/<uuid:pk>', CompanyDetailView.as_view(), name='company_detail'),
path('company/<uuid:pk>/update', CompanyUpdateView.as_view(), name='company_update'),
path('company/<uuid:pk>/delete', CompanyDeleteView.as_view(), name='company_delete'),
path('order', OrderListView.as_view(), name='order_list'),
path('order/create', OrderCreateView.as_view(), name='order_create'),
path('order/<uuid:pk>', OrderDetailView.as_view(), name='order_detail'),
path('order/<uuid:pk>/item', RecipeOrderItemAddView.as_view(), name='item_add'),
path('order/<uuid:pk>/report', OrderDownloadView.as_view(), name='order_report'),
path('item/<uuid:pk>/delete', RecipeOrderItemRemoveView.as_view(), name='item_remove'),
path('order/<uuid:pk>/update', OrderUpdateView.as_view(), name='order_update'),
path('order/<uuid:pk>/delete', OrderDeleteView.as_view(), name='order_delete'),
path('recipe', RecipeListView.as_view(), name='recipe_list'),
path('recipe/create', RecipeCreateView.as_view(), name='recipe_create'),
path('recipe/<uuid:pk>', RecipeDetailView.as_view(), name='recipe_detail'),
path('recipe/<uuid:pk>/update', RecipeUpdateView.as_view(), name='recipe_update'),
path('recipe/<uuid:pk>/delete', RecipeDeleteView.as_view(), name='recipe_delete'),
path('recipe/<uuid:pk>/ingredient', RecipeIngredientAddView.as_view(), name='ingredient_add'),
path('ingredient_item/<int:pk>', RecipeIngredientRemoveView.as_view(), name='ingredient_remove'),
path('recipe/<uuid:pk>/veg_ingredient', RecipeVegIngredientAddView.as_view(), name='veg_ingredient_add'),
path('ingredient_item_veg/<int:pk>', RecipeVegIngredientRemoveView.as_view(), name='veg_ingredient_remove'),
path('ingredient', IngredientListView.as_view(), name='ingredient_list'),
path('ingredient/create', IngredientCreateView.as_view(), name='ingredient_create'),
path('ingredient/<uuid:pk>', IngredientDetailView.as_view(), name='ingredient_detail'),
path('ingredient/<uuid:pk>/update', IngredientUpdateView.as_view(), name='ingredient_update'),
path('ingredient/<uuid:pk>/delete', IngredientDeleteView.as_view(), name='ingredient_delete'),

]