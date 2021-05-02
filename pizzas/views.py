from django.shortcuts import render, redirect
from .models import Pizza, Topping
from .forms import CommentForm

# Create your views here.

def index(request):
    return render(request, 'pizzas/index.html')

def pizzas(request):
    pizzas = Pizza.objects.order_by('name')
    context = {'pizzas': pizzas}
    return render(request, 'pizzas/pizzas.html', context)

def pizza(request, pizza_id):
    pizza = Pizza.objects.get(id=pizza_id)
    toppings = pizza.topping_set.order_by('pizza')

    context = {'pizza': pizza, 'toppings': toppings}
    return render(request, 'pizzas/pizza.html', context)

def comments(request, pizza_id):
    pizza = Pizza.objects.get(id=pizza_id)
        
    if request.method != 'POST':
        form = CommentForm()
    else:
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comments = form.save(commit=False)
            comments.pizza = pizza
            comments.save()
            return redirect('pizzas:pizza', pizza_id=pizza_id)

    context = {'form': form, 'pizza': pizza}
    return render(request, 'pizzas/comments.html', context)