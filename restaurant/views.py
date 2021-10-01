from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages


from .forms import *
from .models import *
from accounts.models import *
# Create your views here.


def menu_list(request, id, pk):
    menu = MenuTable.objects.filter(res_id=id,  status='available')
    cat = Categories.objects.filter(rest_id=id)
    table = Table.objects.get(table_no=pk, rest_id=id)
    user = User.objects.get(id=id)
    table.status = 'Occupied'
    table.save()
    cart = OrderItem.objects.filter(
        table_no__table_no=pk, table_no__rest=id, ordered=True, status='pending')
    print(cart)
    return render(request, 'customer/menu.html', {'menu': menu, 'table': table, 'cart': cart, 'cat': cat, 'user': user})


def add_to_cart(request, id, pk):
    item = get_object_or_404(MenuTable, id=id)
    order_item, created = OrderItem.objects.get_or_create(
        product=item, table_no__rest=item.res_id, table_no_id=pk, ordered=True, status='pending')
    order_qs = Order.objects.filter(
        table_no_id=pk, ordered=True, status='Pending', table_no__rest=item.res_id)
    table = Table.objects.get(id=pk)
    if order_qs.exists():
        order = order_qs[0]

        if order.item.filter(product_id=item.pk, status='pending').exists() or order.item.filter(product_id=item.pk, status='Preparing'):
            order_item.quantity += 1
            order_item.save()
            order.item.add(order_item)
            messages.info(request, "Item Quantity was Updated")
            return redirect("restaurant:menu", id=table.rest.id, pk=table.table_no)
        else:
            messages.info(request, "item was added to cart")
            order.item.add(order_item)
            return redirect("restaurant:menu", id=table.rest.id, pk=table.table_no)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            table_no_id=pk, ordered_date=ordered_date,  ordered=True, status='Pending')
        order.item.add(order_item)
        messages.info(request, "item was added to cart")
    return redirect("restaurant:menu", id=table.rest.id, pk=table.table_no)


def remove_from_cart(request, id, pk):
    item = get_object_or_404(MenuTable, id=id)
    order_qs = Order.objects.filter(
        table_no_id=pk, ordered=True, status='pending', table_no__rest=item.res_id)
    table = Table.objects.get(id=pk)
    if order_qs.exists():
        order = order_qs[0]

        if order.item.filter(product_id=item.pk).exists():
            order_item = OrderItem.objects.filter(
                product=item, table_no_id=pk, ordered=True, status='pending', table_no__rest=item.res_id)[0]
            order.item.model.delete(order_item)
            messages.info(request, "Item was removed from cart")
            return redirect("restaurant:menu", id=table.rest.id, pk=table.table_no)
        else:
            messages.info(request, "Item was not in your cart")
            return redirect("restaurant:menu", id=table.rest.id, pk=table.table_no)
    else:
        messages.info(request, "You do not have active order")
        return redirect("restaurant:menu", id=table.rest.id, pk=table.table_no)


def remove_single_item_from_cart(request, id, pk):
    item = get_object_or_404(MenuTable, id=id)
    order_qs = Order.objects.filter(
        table_no_id=pk, ordered=True, status='Pending', table_no__rest=item.res_id)
    table = Table.objects.get(id=pk)
    if order_qs.exists():
        order = order_qs[0]

        if order.item.filter(product_id=item.pk).exists():
            order_item = OrderItem.objects.filter(
                product=item, table_no_id=pk, ordered=True, status='pending', table_no__rest=item.res_id)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.item.model.delete(order_item)
            messages.info(request, "Item was removed from cart")
            return redirect("restaurant:menu", id=table.rest.id, pk=table.table_no)
        else:
            messages.info(request, "Item was not in your cart")
            return redirect("restaurant:menu", id=table.rest.id, pk=table.table_no)
    else:
        messages.info(request, "You do not have active order")
        return redirect("restaurant:menu", id=table.rest.id, pk=table.table_no)


def order_summary(request, id, id2):
    try:
        cart = OrderItem.objects.filter(
            table_no__table_no=id2, table_no__rest=id, ordered=True, status='pending')
        table = Table.objects.get(table_no=id2, rest_id=id)
        orders = Order.objects.get(
            table_no__table_no=id2, table_no__rest=id, ordered=True, status='Pending')
        print(orders)
        return render(request, 'customer/order_sumery.html', {'cart': cart, 'orders': orders, 'table': table})
    except:
        cart = OrderItem.objects.filter(
            table_no__table_no=id2, table_no__rest=id, ordered=True, status='pending')
        table = Table.objects.get(table_no=id2, rest_id=id)
        return render(request, 'customer/order_sumery.html', {'cart': cart, 'table': table})


def comment(request, id):
    cart = OrderItem.objects.get(id=id)
    a = request.GET.get(f'com{id}')

    cart.comment = a
    cart.save()
    return redirect('restaurant:order_summary', id=cart.table_no.rest.id, id2=cart.table_no.table_no)


def proceed_to_pay(request, id, id2):
    cart = OrderItem.objects.filter(
        table_no__table_no=id2, table_no__rest=id, ordered=False)
    orders = Order.objects.get(
        table_no__table_no=id2, table_no__rest=id, ordered=True, status='Pending')
    print(cart)
    orders.ordered = True
    orders.status = 'Pending'
    orders.save()

    for i in cart:

        i.ordered = True
        i.save()
    messages.warning(request, "New order ")
    messages.error(request, "order placed succesfully")
    return redirect('restaurant:menu', id=orders.table_no.rest.id, pk=orders.table_no.table_no)


def index(request):
    return render(request, 'index.html', {})


def call_a_waiter(request, id):
    tab_no = Table.objects.get(id=id)
    messages.warning(request, f'Table No: {tab_no.table_no} Need A Waiter')
    waiter_call = CallWaiter(table=tab_no, Status=True) 
    waiter_call.save()
    return HttpResponse("waiter is comming sir")


def add_to_cart_order(request, id, pk):
    item = get_object_or_404(MenuTable, id=id)
    order_item, created = OrderItem.objects.get_or_create(
        product=item, table_no__rest=item.res_id, table_no_id=pk, ordered=True, status='pending')
    order_qs = Order.objects.filter(
        table_no_id=pk, ordered=True, status='Pending', table_no__rest=item.res_id)
    table = Table.objects.get(id=pk)
    if order_qs.exists():
        order = order_qs[0]

        if order.item.filter(product_id=item.pk, status='pending').exists() or order.item.filter(product_id=item.pk, status='Preparing'):
            order_item.quantity += 1
            order_item.save()
            order.item.add(order_item)
            messages.info(request, "Item Quantity was Updated")
            return redirect("restaurant:order_summary", id=table.rest.id, id2=table.table_no)
        else:
            messages.info(request, "item was added to cart")
            order.item.add(order_item)
            return redirect("restaurant:order_summary", id=table.rest.id, id2=table.table_no)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            table_no_id=pk, ordered_date=ordered_date,  ordered=True, status='Pending')
        order.item.add(order_item)
        messages.info(request, "item was added to cart")
    return redirect("restaurant:order_summary", id=table.rest.id, id2=table.table_no)


def remove_single_item_from_cart_order(request, id, pk):
    item = get_object_or_404(MenuTable, id=id)
    order_qs = Order.objects.filter(
        table_no_id=pk, ordered=True, status='Pending', table_no__rest=item.res_id)
    table = Table.objects.get(id=pk)
    if order_qs.exists():
        order = order_qs[0]

        if order.item.filter(product_id=item.pk).exists():
            order_item = OrderItem.objects.filter(
                product=item, table_no_id=pk, ordered=True, status='pending', table_no__rest=item.res_id)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.item.model.delete(order_item)
            messages.info(request, "Item was removed from cart")
            return redirect("restaurant:order_summary", id=table.rest.id, id2=table.table_no)
        else:
            messages.info(request, "Item was not in your cart")
            return redirect("restaurant:order_summary", id=table.rest.id, id2=table.table_no)
    else:
        messages.info(request, "You do not have active order")
        return redirect("restaurant:order_summary", id=table.rest.id, id2=table.table_no)

