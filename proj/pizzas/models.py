
from django.db import models
from django.db.models import (
    Case,
    Max,
    Value,
    When,
)


class Topping(models.Model):
    VEGAN = 0
    VEGETARIAN = 1
    NON_VG_NON_V = 2
    TOPPING_TYPE_CHOICES = (
        (VEGAN, 'Vegan-friendly'),
        (VEGETARIAN, 'Vegetarian-friendly'),
        (NON_VG_NON_V, 'Non-vegan non-veg'))
    name = models.CharField(max_length=64)
    rating = models.PositiveSmallIntegerField(choices=TOPPING_TYPE_CHOICES)

    def __str__(self):
        return self.name


class PizzaManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().annotate(
            max_rating=Max('toppings__rating'),
            is_vegan=Case(
                When(max_rating=Topping.VEGAN, then=Value(True)),
                default=Value(False),
                output_field=models.BooleanField(),
            ),
            is_vegetarian=Case(
                When(max_rating__lte=Topping.VEGETARIAN, then=Value(True)),
                default=Value(False),
                output_field=models.BooleanField(),
            )
        )


class Pizza(models.Model):
    name = models.CharField(max_length=64)
    toppings = models.ManyToManyField(Topping)
    price = models.DecimalField(max_digits=4, decimal_places=2)

    objects = PizzaManager()

    def __str__(self):
        return self.name


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

    def pizzas_ordered(self):
        return Pizza.objects.filter(
            id__in=self.order_set.values_list('pizzas__id', flat=True)
        ).distinct()

    @property
    def is_vegan(self):
        return all([pizza.is_vegan for pizza in self.pizzas_ordered()])

    @property
    def is_vegetarian(self):
        return all([pizza.is_vegetarian for pizza in self.pizzas_ordered()])
