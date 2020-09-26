from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import *
from .forms import *



import functools
import ssl
from django.conf import settings

from django_weasyprint import WeasyTemplateResponseMixin, WeasyTemplateResponse
from django_weasyprint.views import CONTENT_TYPE_PNG
from django.db.models import Sum, F, DecimalField



# Create your views here.

# class CompanyPageView(TemplateView):
#     template_name = 'tracker/company.html'

class CompanyListView(ListView):
    model = Company
    context_object_name = 'company_list'
    template_name = 'tracker/company/company.html'

class CompanyCreateView(CreateView):
    model = Company
    form_class = CompanyForm
    context_object_name = 'company_create'
    template_name = 'tracker/company/company_form.html'

class CompanyDetailView(DetailView): 
    model = Company
    context_object_name = 'company'
    template_name = 'tracker/company/company_detail.html'

    def get_context_data(self, **kwargs):
        try: 
            company = Company.objects.get(id=self.kwargs['pk'])
        except CompanyOrder.DoesNotExist():
            raise ValueError
        context = super(CompanyDetailView, self).get_context_data(**kwargs)
        context['orders'] = CompanyOrder.objects.filter(company=company)
        return context


class CompanyUpdateView(UpdateView): 
    model = Company
    context_object_name = 'company'
    template_name = 'tracker/company/company_update.html'
    form_class = CompanyForm

class CompanyDeleteView(DeleteView):
    model = Company
    success_url = reverse_lazy('company_list')

class OrderListView(ListView):
    model = CompanyOrder
    context_object_name = 'order_list'
    template_name = 'tracker/order/order.html'

class OrderCreateView(CreateView):
    model = CompanyOrder
    form_class = CompanyOrderForm
    context_object_name = 'order_create'
    template_name = 'tracker/order/order_form.html'

class OrderUpdateView(UpdateView):
    model = CompanyOrder
    form_class = CompanyOrderForm
    context_object_name = 'order_update'
    template_name = 'tracker/order/order_update.html'

class OrderDetailView(DetailView): 
    model = CompanyOrder
    context_object_name = 'order'
    template_name = 'tracker/order/order_detail.html'

    def get_context_data(self, **kwargs):
        try: 
            company_order = CompanyOrder.objects.get(id=self.kwargs['pk'])
        except CompanyOrder.DoesNotExist():
            raise ValueError
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(company_order=company_order)
        return context

class OrderDeleteView(DeleteView):
    model = CompanyOrder
    success_url = reverse_lazy('order_list')

class RecipeOrderItemAddView(UpdateView): 
    model = Order
    context_object_name = 'item_add'
    template_name = 'tracker/order/item_order_form.html'
    form_class = AddItemOrderForm

    def get_object(self, queryset=None): 
        try: 
            company_order = CompanyOrder.objects.get(id=self.kwargs['pk'])
        except CompanyOrder.DoesNotExist():
            raise ValueError
        self.request.company_order = company_order
        return company_order

    def form_valid(self, form):
        mutable = form.data._mutable
        form.data._mutable = True
        form.data['company_order'] = self.request.company_order
        form.data._mutable = False
        # self.object = form.save() 
        return super(RecipeOrderItemAddView, self).form_valid(form)   

    def get_success_url(self):
        return reverse('order_detail', args=[self.kwargs['pk']])

class RecipeOrderItemRemoveView(DeleteView): 
    model = Order

    def get_success_url(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['order'] = self.request.GET.get('order', None)
        return reverse('order_detail', args=[ctx['order']])

class IngredientListView(ListView):
    model = Ingredient
    context_object_name = 'ingredient_list'
    template_name = 'tracker/ingredient/ingredient.html'

class IngredientCreateView(CreateView):
    model = Ingredient
    form_class = IngredientForm
    context_object_name = 'ingredient_create'
    template_name = 'tracker/ingredient/ingredient_form.html'

class IngredientUpdateView(UpdateView):
    model = Ingredient
    form_class = IngredientForm
    context_object_name = 'ingredient_update'
    template_name = 'tracker/ingredient/ingredient_update.html'

class IngredientDetailView(DetailView): 
    model = Ingredient
    context_object_name = 'ingredient'
    template_name = 'tracker/ingredient/ingredient_detail.html'

class IngredientDeleteView(DeleteView):
    model = Ingredient
    success_url = reverse_lazy('ingredient_list')
    
class RecipeListView(ListView):
    model = Recipe
    context_object_name = 'recipe_list'
    template_name = 'tracker/recipe/recipe.html'

class RecipeCreateView(CreateView):
    model = Recipe
    context_object_name = 'recipe_create'
    template_name = 'tracker/recipe/recipe_form.html'
    form_class = RecipeForm

    def form_valid(self, form):   
        response = super(RecipeCreateView, self).form_valid(form)
        return response
    
class RecipeUpdateView(UpdateView):
    model = Recipe
    context_object_name = 'recipe_update'
    template_name = 'tracker/recipe/recipe_update.html'
    form_class = RecipeForm

class RecipeDetailView(DetailView): 
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'tracker/recipe/recipe_detail.html'

    def get_context_data(self, **kwargs):
        try: 
            recipe = Recipe.objects.get(id=self.kwargs['pk'])
        except Recipe.DoesNotExist():
            raise ValueError
        context = super(RecipeDetailView, self).get_context_data(**kwargs)
        ingredients = IngredientAmount.objects.filter(recipe=recipe)
        context['ingredients'] = ingredients
        context['ingredients_water'] = ingredients.aggregate(
            total=Sum(F('amount') * F('ingredient__water'),
            output_field=DecimalField()))['total']

        context['ingredients_carbondioxide'] = ingredients.aggregate(
            total=Sum(F('amount') * F('ingredient__carbondioxide'),
            output_field=DecimalField()))['total']

        context['ingredients_land'] = ingredients.aggregate(
            total=Sum(F('amount') * F('ingredient__land'),
            output_field=DecimalField()))['total']

        veg_ingredients = VegIngredientAmount.objects.filter(recipe=recipe)
        context['veg_ingredients'] = veg_ingredients

        context['ingredients_water_veg'] = veg_ingredients.aggregate(
            total=Sum(F('amount') * F('ingredient__water'),
            output_field=DecimalField()))['total']

        context['ingredients_carbondioxide_veg'] = veg_ingredients.aggregate(
            total=Sum(F('amount') * F('ingredient__carbondioxide'),
            output_field=DecimalField()))['total']

        context['ingredients_land_veg'] = veg_ingredients.aggregate(
            total=Sum(F('amount') * F('ingredient__land'),
            output_field=DecimalField()))['total']


        return context

class RecipeDeleteView(DeleteView):
    model = Recipe
    success_url = reverse_lazy('recipe_list')

class RecipeIngredientAddView(UpdateView): 
    model = Recipe
    context_object_name = 'ingredient_add'
    template_name = 'tracker/recipe/ingredient_recipe_form.html'
    form_class = AddIngredientForm

    def get_object(self, queryset=None): 
        try: 
            recipe = Recipe.objects.get(id=self.kwargs['pk'])
        except Recipe.DoesNotExist():
            raise ValueError
        self.request.recipe = recipe
        return recipe

    def form_valid(self, form):
        mutable = form.data._mutable
        form.data._mutable = True
        form.data['recipe'] = self.request.recipe
        form.data._mutable = False
        # self.object = form.save() 
        return super(RecipeIngredientAddView, self).form_valid(form)   

    def get_success_url(self):
        return reverse('recipe_detail', args=[self.kwargs['pk']])

class RecipeIngredientRemoveView(DeleteView): 
    model = IngredientAmount

    def get_success_url(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['recipe'] = self.request.GET.get('recipe', None)
        return reverse('recipe_detail', args=[ctx['recipe']])

class RecipeVegIngredientAddView(UpdateView): 
    model = Recipe
    context_object_name = 'ingredient_add'
    template_name = 'tracker/recipe/ingredient_recipe_form.html'
    form_class = AddVegIngredientForm

    def get_object(self, queryset=None): 
        try: 
            recipe = Recipe.objects.get(id=self.kwargs['pk'])
        except Recipe.DoesNotExist():
            raise ValueError
        self.request.recipe = recipe
        return recipe

    def form_valid(self, form):
        mutable = form.data._mutable
        form.data._mutable = True
        form.data['recipe'] = self.request.recipe
        form.data._mutable = False
        # self.object = form.save() 
        return super(RecipeVegIngredientAddView, self).form_valid(form)   

    def get_success_url(self):
        return reverse('recipe_detail', args=[self.kwargs['pk']])


class RecipeVegIngredientRemoveView(DeleteView): 
    model = VegIngredientAmount

    def get_success_url(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['recipe'] = self.request.GET.get('recipe', None)
        return reverse('recipe_detail', args=[ctx['recipe']])

class OrderPdfView(DetailView): 
    model = CompanyOrder
    context_object_name = 'order'
    template_name = 'tracker/order/order_pdf.html'

    def get_context_data(self, **kwargs):
        try: 
            company_order = CompanyOrder.objects.get(id=self.kwargs['pk'])
        except CompanyOrder.DoesNotExist():
            raise ValueError
        context = super(OrderPdfView, self).get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(company_order=company_order)
        return context

class OrderDownloadView(WeasyTemplateResponseMixin, OrderPdfView):
    # suggested filename (is required for attachment/download!)
    pdf_filename = 'pitythefoo.pdf'
