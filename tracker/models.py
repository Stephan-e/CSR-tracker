from django.db import models
import uuid
import datetime
from django.urls import reverse
from enumfields import EnumField
from tracker.enums import *


# Create your models here.

class DateModel(models.Model):
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.created)

class Company(DateModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    description = models.CharField(max_length=200, default = None, null=True, blank=True)
    name = models.CharField(max_length=50)
    water_saved = models.DecimalField(default = 0.00, max_digits=15, decimal_places=2)
    carbondioxide_saved = models.DecimalField(default = 0.00, max_digits=15, decimal_places=2)
    land_saved = models.DecimalField(default = 0.00, max_digits=15, decimal_places=2)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self): # new
        return reverse('company_detail', args=[str(self.id)])


class Ingredient(DateModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    description = models.CharField(max_length=200, default = None, null=True, blank=True)
    name = models.CharField(max_length=50)
    water = models.DecimalField(default = 0.00, max_digits=15, decimal_places=5)
    carbondioxide = models.DecimalField(default = 0.00, max_digits=15, decimal_places=5)
    land = models.DecimalField(default = 0.00, max_digits=15, decimal_places=5)
    category = EnumField(
                IngredientCategory, 
                max_length=50,
                default=IngredientCategory.NONE)

    def __str__(self):
        return self.name

    def get_absolute_url(self): 
        return reverse('ingredient_detail', args=[str(self.id)])


class IngredientAmount(DateModel):
    ingredient = models.ForeignKey('Ingredient', related_name='ingredient_amount', on_delete=models.SET_NULL, null=True, blank=True)
    recipe = models.ForeignKey('Recipe', related_name='ingredient_amount', on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.IntegerField(default = 0)

    def delete(self, *args, **kwargs):
        self.recipe.water_use -= self.ingredient.water*self.amount
        self.recipe.carbondioxide_use -= self.ingredient.carbondioxide*self.amount
        self.recipe.land_use -= self.ingredient.land*self.amount
        self.recipe.save()
        super(IngredientAmount, self).delete(*args, **kwargs)
    
    def get_absolute_url(self): 
        return reverse('ingredient_item_detail', args=[str(self)])

    def __str__(self):
        return self.ingredient.name +' x '+ str(self.amount)


class VegIngredientAmount(DateModel):
    ingredient = models.ForeignKey('Ingredient', related_name='veg_ingredient_amount', on_delete=models.SET_NULL, null=True, blank=True)
    recipe = models.ForeignKey('Recipe', related_name='veg_ingredient_amount', on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.IntegerField(default = 0)

    def delete(self, *args, **kwargs):
        self.recipe.water_use_veg -= self.ingredient.water*self.amount
        self.recipe.carbondioxide_use_veg -= self.ingredient.carbondioxide*self.amount
        self.recipe.land_use_veg -= self.ingredient.land*self.amount
        self.recipe.save()
        super(VegIngredientAmount, self).delete(*args, **kwargs)
    
    def get_absolute_url(self): 
        return reverse('veg_ingredient_item_detail', args=[str(self)])

    def __str__(self):
        return self.ingredient.name +' x '+ str(self.amount)


class Recipe(DateModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    description = models.CharField(max_length=200, default = None, null=True, blank=True)
    name = models.CharField(max_length=50)
    ingredients = models.ManyToManyField(Ingredient, related_name="meat_ingredient", through=IngredientAmount)
    veg_ingredients = models.ManyToManyField(Ingredient, related_name="veg_ingredient", through=VegIngredientAmount)
    water_use = models.DecimalField(default = 0.00, max_digits=15, decimal_places=2)
    carbondioxide_use = models.DecimalField(default = 0.00, max_digits=15, decimal_places=2)
    land_use = models.DecimalField(default = 0.00, max_digits=15, decimal_places=2)
    water_use_veg = models.DecimalField(default = 0.00, max_digits=15, decimal_places=2)
    carbondioxide_use_veg = models.DecimalField(default = 0.00, max_digits=15, decimal_places=2)
    land_use_veg = models.DecimalField(default = 0.00, max_digits=15, decimal_places=2)

    def __str__(self):
        return self.name

    def get_absolute_url(self): 
        return reverse('recipe_detail', args=[str(self.id)])


class Order(DateModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    quantity = models.IntegerField(default = 0)

    def delete(self, *args, **kwargs):
        co = CompanyOrder.objects.get(order=self)
        co.company.water_saved -= self.quantity*(self.recipe.water_use-self.recipe.water_use_veg)
        co.company.carbondioxide_saved -= self.quantity*(self.recipe.carbondioxide_use-self.recipe.carbondioxide_use_veg)
        co.company.land_saved -= self.quantity*(self.recipe.land_use-self.recipe.land_use_veg)
        co.company.save()
        super(Order, self).delete(*args, **kwargs)

    def get_absolute_url(self): 
        return reverse('item_detail', args=[str(self.id)])
    
    def __str__(self):
        return self.recipe.name + ' x ' + str(self.quantity)


    # @property
    # def metrics(self):
    #     metrics ={}
    #     # metrics['water_saved'] = self.quantity*(self.recipe.metrics['water_use']-self.recipe.metrics['water_use_veg'])
    #     # metrics['carbondioxide_saved'] = self.quantity*(self.recipe.metrics['carbondioxide_use']-self.recipe.metrics['carbondioxide_use_veg'])
    #     # metrics['land_saved'] = self.quantity*(self.recipe.metrics['land_use']-self.recipe.metrics['land_use_veg'])
    #     return metrics


class CompanyOrder(DateModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=200)
    date = models.DateField()
    order = models.ManyToManyField('Order',related_name="company_order")
    company = models.ForeignKey('Company', on_delete=models.CASCADE, null=True,)

    @property
    def metrics(self):
        metrics ={}
        metrics['water_saved'] = 0
        metrics['carbondioxide_saved'] = 0
        metrics['land_saved'] = 0
        for order in self.order.all():
            metrics['water_saved'] += order.quantity*(order.recipe.water_use - order.recipe.water_use_veg)
            metrics['carbondioxide_saved'] += order.quantity*(order.recipe.carbondioxide_use - order.recipe.carbondioxide_use_veg)
            metrics['land_saved'] += order.quantity*(order.recipe.land_use - order.recipe.land_use_veg)
        return metrics

    def get_absolute_url(self): 
        return reverse('order_detail', args=[str(self.id)])

    def __str__(self):
        return self.name

