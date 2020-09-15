from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import *
import json

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name', 'description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save company'))


class CompanyOrderForm(forms.ModelForm):
    date = forms.DateField(
                    widget=forms.TextInput(     
                    attrs={'type': 'date'} ))   
    class Meta:
        model = CompanyOrder
        fields = ('name', 'date', 'company')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save company'))


class AddItemOrderForm(forms.ModelForm):
    recipe = forms.ModelChoiceField(queryset=Recipe.objects.filter())
    quantity = forms.IntegerField()

    class Meta:
        model = CompanyOrder
        fields = (
            'recipe',
            'quantity',
            )
        read_only_fields = ('id')
        # widgets = {
        #     'ingredients': forms.widgets.ChoiceField(),
        #     'veg_ingredients': forms.widgets.ChoiceField()}
    
    def save(self, commit=True):
        recipe = Recipe.objects.get(id=self.data.get('recipe'))
        quantity = self.cleaned_data.get('quantity')
        order = Order.objects.create(
             recipe=recipe, 
             quantity=quantity
             )
        self.data.get('company_order').order.add(order)
        self.data.get('company_order').company.water_saved += quantity*(recipe.water_use-recipe.water_use_veg)
        self.data.get('company_order').company.carbondioxide_saved += quantity*(recipe.carbondioxide_use-recipe.carbondioxide_use_veg)
        self.data.get('company_order').company.land_saved += quantity*(recipe.land_use-recipe.land_use_veg)
        self.data.get('company_order').company.save()
        return self


class RecipeForm(forms.ModelForm):
    name = forms.CharField()
    description = forms.CharField()
    
    class Meta:
        model = Recipe
        fields = (
            'name', 
            'description',
            )
        
    def save(self, commit=True):
        instance = super(RecipeForm, self).save(commit=False)
        if commit:
            instance.save()
        return instance


class AddIngredientForm(forms.ModelForm):
    ingredient = forms.ModelChoiceField(queryset=Ingredient.objects.filter(category='animal_based'))
    amount = forms.IntegerField()

    class Meta:
        model = Recipe
        fields = (
            'ingredient',
            'amount',
            )
        read_only_fields = ('id')
    
    def save(self, commit=True):
        ingredient = self.cleaned_data.get('ingredient')
        amount = self.cleaned_data.get('amount')
        recipe = self.data.get('recipe')
        recipe.water_use += ingredient.water*amount
        recipe.carbondioxide_use += ingredient.carbondioxide*amount
        recipe.land_use += ingredient.land*amount
        recipe.save()
        ingredientamount = IngredientAmount.objects.create(
            recipe=recipe, 
            ingredient=self.cleaned_data.get('ingredient'), 
            amount=self.cleaned_data.get('amount'))
        return ingredientamount


class AddVegIngredientForm(forms.ModelForm):
    ingredient = forms.ModelChoiceField(queryset=Ingredient.objects.filter(category='plant_based'))
    amount = forms.IntegerField()

    class Meta:
        model = Recipe
        fields = (
            'ingredient',
            'amount',
            )
        read_only_fields = ('id')

    def save(self, commit=True):
        ingredient = self.cleaned_data.get('ingredient')
        amount = self.cleaned_data.get('amount')
        recipe = self.data.get('recipe')
        recipe.water_use_veg += ingredient.water*amount
        recipe.carbondioxide_use_veg += ingredient.carbondioxide*amount
        recipe.land_use_veg += ingredient.land*amount
        recipe.save()
        recipe = VegIngredientAmount.objects.create(
            recipe=recipe,
            ingredient=ingredient, 
            amount=amount)
        return recipe
    
class IngredientForm(forms.ModelForm):
    name = forms.CharField()
    description = forms.CharField()

    class Meta:
        model = Ingredient
        fields = (
            'name', 
            'description',
            'water',
            'carbondioxide',
            'land',
            'category'
            )
            