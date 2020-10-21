
from model_bakery import baker, recipe

from pizzas.models import Topping


def load_data():
    vegan_topping = recipe.Recipe(
        'pizzas.Topping', rating=Topping.VEGAN)
    veggy_topping = recipe.Recipe(
        'pizzas.Topping', rating=Topping.VEGETARIAN)
    non_vg_non_v_topping = recipe.Recipe(
        'pizzas.Topping', rating=Topping.NON_VG_NON_V)

    # toppings

    tomato_sauce = vegan_topping.make(name='tomato sauce')
    mushrooms = vegan_topping.make(name='mushrooms')
    artichokes = vegan_topping.make(name='artichokes')
    olives = vegan_topping.make(name='olives')
    aubergines = vegan_topping.make(name='aubergines')
    jalapenos = vegan_topping.make(name='jalapenos')

    mozzarella = veggy_topping.make(name='mozzarella')
    egg = veggy_topping.make(name='egg')

    ham = non_vg_non_v_topping.make(name='ham')
    pepperoni = non_vg_non_v_topping.make(name='pepperoni')

    # pizzas

    rossa = baker.make('pizzas.Pizza', name='rossa', price=6.0)
    rossa.toppings.add(tomato_sauce)

    bianca = baker.make('pizzas.Pizza', name='bianca', price=6.0)
    bianca.toppings.add(mozzarella)

    margherita = baker.make('pizzas.Pizza', name='margherita', price=6.5)
    margherita.toppings.add(tomato_sauce)
    margherita.toppings.add(mozzarella)

    capricciosa = baker.make('pizzas.Pizza', name='capricciosa', price=9.80)
    capricciosa.toppings.add(tomato_sauce)
    capricciosa.toppings.add(mozzarella)
    capricciosa.toppings.add(ham)
    capricciosa.toppings.add(mushrooms)
    capricciosa.toppings.add(egg)
    capricciosa.toppings.add(artichokes)
    capricciosa.toppings.add(olives)

    diablo = baker.make('pizzas.Pizza', name='diablo', price=8.50)
    diablo.toppings.add(tomato_sauce)
    diablo.toppings.add(mozzarella)
    diablo.toppings.add(pepperoni)
    diablo.toppings.add(jalapenos)

    campagnola = baker.make('pizzas.Pizza', name='campagnola', price=10.0)
    campagnola.toppings.add(tomato_sauce)
    campagnola.toppings.add(mushrooms)
    campagnola.toppings.add(olives)
    campagnola.toppings.add(aubergines)

    # customers
    vegan, veggy, meaty = baker.make('pizzas.Customer', _quantity=3)

    # orders - vegan customer
    ord1, ord2 = baker.make('pizzas.Order', customer=vegan, _quantity=2)
    ord1.pizzas.add(rossa)
    ord1.pizzas.add(campagnola)
    ord2.pizzas.add(campagnola)

    # orders - vegetarian customer
    ord3, ord4 = baker.make('pizzas.Order', customer=vegan, _quantity=2)
    ord3.pizzas.add(rossa)
    ord3.pizzas.add(margherita)
    ord4.pizzas.add(campagnola)

    # orders - non vegan, non vegetarian customer
    ord5, ord6, ord7 = baker.make('pizzas.Order', customer=vegan, _quantity=3)
    ord5.pizzas.add(rossa)
    ord6.pizzas.add(margherita)
    ord7.pizzas.add(diablo)
    ord7.pizzas.add(capricciosa)
