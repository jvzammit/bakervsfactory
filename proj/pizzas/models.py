
from django.db import models


class Topping(models.Model):
    VEGAN = 0
    VEGETARIAN = 1
    TOPPING_TYPE_CHOICES = (
        (VEGAN, 'Vegan-friendly'),
        (VEGETARIAN, 'Vegetarian-friendly'))
    name = models.CharField(max_length=64)
    rating = models.PositiveSmallIntegerField(
        blank=True, null=True, choices=TOPPING_TYPE_CHOICES)

    def __str__(self):
        return self.name


class Pizza(models.Model):
    name = models.CharField(max_length=64)
    toppings = models.ManyToManyField(Topping)
    price = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return self.name

    @property
    def is_vegan(self):
        return all([
            topping.rating == Topping.VEGAN for topping in self.toppings.all()
        ])

    @property
    def is_vegetarian(self):
        return all([
            topping.rating in (
                Topping.VEGAN, Topping.VEGETARIAN
            ) for topping in self.toppings.all()
        ])


class OrderManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().annotate(
            total=models.Sum('pizzas__price'))


class Order(models.Model):
    date = models.DateField()
    customer = models.ForeignKey('pizzas.Customer', on_delete=models.CASCADE)
    pizzas = models.ManyToManyField('pizzas.Pizza')

    objects = OrderManager()

    def __str__(self):
        return (
            f'On {self.date.strftime("%Y-%m-%d")} by '
            f'{self.customer.first_name} {self.customer.last_name}')


class Customer(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
