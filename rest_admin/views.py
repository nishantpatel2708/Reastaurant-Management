from django.template.loader import get_template
from .utils import render_to_pdf  # created in step 4
from django.views.generic import View
from django.http import HttpResponse
import datetime

from django.contrib import messages

from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404, redirect
from django.urls import reverse
from .models import *
from .forms import *
from accounts.forms import RestaurantForm
from accounts.models import User
from restaurant.models import *


# Create your views here.

def qr(request):
    restro = User.objects.get(id=request.user.id)
    res = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = QrForm(request.POST, request.FILES)

        if form.is_valid():

            form_r = form.save(commit=False)
            form_r.rest = res
            form_r.status = 'available'
            form_r.save()
            return redirect('rest_admin:table_list')
        else:
            print(form.errors)
    else:
        form = QrForm()
    return render(request, 'rest_admin/index.html', {
        'form': form,
        'restro': restro
    })


def add_menu(request):
    restro = User.objects.get(id=request.user.id)
    res = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = AddMenuForm(res.id, request.POST, request.FILES)

        if form.is_valid():

            form_r = form.save(commit=False)
            form_r.res = res
            form_r.status = 'available'
            form_r.save()
            return redirect('rest_admin:menu_list')
        else:
            print(form.errors)
    else:
        form = AddMenuForm(res.id)
    return render(request, 'rest_admin/add_menu.html', {
        'form': form,
        'restro': restro
    })


def add_employee(request):
    restro = User.objects.get(id=request.user.id)
    res = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)

        if form.is_valid():

            form_r = form.save(commit=False)
            form_r.set_password(form_r.password)
            form_r.rest = res
            form_r.is_employee = True
            form_r.save()
            return redirect('rest_admin:emp_list')
        else:
            print(form.errors)
    else:
        form = EmployeeForm()

    return render(request, 'rest_admin/add_employee.html', {
        'form': form,
        'restro': restro
    })


def add_categories(request):
    restro = User.objects.get(id=request.user.id)
    res = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = AddCategoryForm(request.POST, request.FILES)

        if form.is_valid():

            form_r = form.save(commit=False)
            form_r.rest = res
            form_r.save()
            return redirect('rest_admin:cat_list')
        else:
            print(form.errors)
    else:
        form = AddCategoryForm()
    return render(request, 'rest_admin/add_category.html', {
        'form': form,
        'restro': restro
    })


def category_list(request):
    restro = User.objects.get(id=request.user.id)
    res = User.objects.get(id=request.user.id)
    cat_list = Categories.objects.filter(rest_id=res)
    return render(request, 'rest_admin/cat_list.html', {
        'cat_list': cat_list,
        'restro': restro
    })


def menu_list(request):
    restro = User.objects.get(id=request.user.id)
    res = User.objects.get(id=request.user.id)
    menu_lists = MenuTable.objects.filter(res_id=res)
    return render(request, 'rest_admin/menu_list.html', {
        'menu_lists': menu_lists,
        'restro': restro
    })


def employee_list(request):
    restro = User.objects.get(id=request.user.id)
    res = User.objects.get(id=request.user.id)
    emp_lists = User.objects.filter(is_employee=True, rest_id=res.id)
    print(emp_lists)
    return render(request, 'rest_admin/emp_list.html', {
        'emp_lists': emp_lists,
        'restro': restro
    })


def cat_form_edit(request, id):
    restro = User.objects.get(id=request.user.id)
    instance = get_object_or_404(Categories, id=id)

    form = AddCategoryForm(request.POST or None, instance=instance)

    if form.is_valid():
        form.save()
        return redirect('rest_admin:cat_list')
    return render(request, 'rest_admin/cat_edit.html', {
        'form': form,
        'restro': restro
    })


def delete(request, id):
    user2 = Categories.objects.get(id=id).delete()
    return HttpResponseRedirect(reverse('rest_admin:cat_list'))


def emp_form_edit(request, id):
    restro = User.objects.get(id=request.user.id)
    instance = get_object_or_404(User, id=id)
    form = EmployeeForm(request.POST or None, instance=instance)

    if form.is_valid():
        form.save()

        return redirect('rest_admin:emp_list')
    else:
        print(form.errors)
    return render(request, 'rest_admin/emp_edite.html', {
        'form': form,
        'restro': restro
    })


def emp_delete(request, id):
    user2 = User.objects.get(id=id).delete()
    return HttpResponseRedirect(reverse('rest_admin:emp_list'))


def menu_form_edit(request, id):
    restro = User.objects.get(id=request.user.id)
    res = User.objects.get(id=request.user.id)
    instance = get_object_or_404(MenuTable, id=id)

    form = AddMenuForm(res, request.POST or None, instance=instance)

    if form.is_valid():
        form.save()
        return redirect('rest_admin:menu_list')
    return render(request, 'rest_admin/edit_menu.html', {
        'form': form,
        'restro': restro
    })


def menu_delete(request, id):
    user2 = MenuTable.objects.get(id=id).delete()
    return HttpResponseRedirect(reverse('rest_admin:menu_list'))


def menu_avc(request, id):
    item = MenuTable.objects.get(id=id)
    if item.status == 'available':
        item.status = 'Not Available'
        item.save()
    else:
        item.status = 'available'
        item.save()

    return HttpResponseRedirect(reverse('rest_admin:menu_list'))


def table_view(request):
    restro = User.objects.get(id=request.user.id)

    tables = Table.objects.filter(rest_id=request.user)
    return render(request, 'rest_admin/tables.html', {
        'tables': tables,
        'restro': restro
    })


def table_list(request):
    restro = User.objects.get(id=request.user.id)

    tables = Table.objects.filter(rest_id=request.user)
    return render(request, 'rest_admin/table_list.html', {
        'tables': tables,
        'restro': restro
    })


def table_edit(request, id):
    instance = Table.objects.get(id=id)

    form = QrForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()

        return redirect('rest_admin:table_list')
    else:
        print(form.errors)
    return render(request, 'rest_admin/table_u.html', {'form': form})


def table_delete(request, id):
    user2 = Table.objects.get(id=id).delete()
    return HttpResponseRedirect(reverse('rest_admin:table_list'))


def t_price(request):
    restro = User.objects.get(id=request.user.id)
    res = User.objects.get(id=request.user.id)
    order_list = OrderItem.objects.filter(table_no__rest_id=res.id, ordered=True,
                                          date__year=datetime.datetime.today().year,
                                          date__month=datetime.datetime.today().month,
                                          date__day=datetime.datetime.today().day)
    order_list2 = OrderItem.objects.filter(table_no__rest_id=res.id, ordered=True,
                                           date__year=datetime.datetime.today().year,
                                           date__month=datetime.datetime.today().month)
    total_emp = User.objects.filter(id=request.user.id)
    total_earn = OrderItem.objects.filter(
        table_no__rest_id=res.id, ordered=True)
    total = 0
    m_total = 0
    a_total = 0
    for i in order_list:

        total += i.product.Price

    for j in order_list2:
        m_total += j.product.Price

    for k in total_earn:
        a_total += k.product.Price

    return render(request, 'rest_admin/t_earn.html', {'total': total, 'm_total': m_total, 'total_emp': total_emp,
                                                      'a_total': a_total, 'restro': restro})


def report(request):
    restro = User.objects.get(id=request.user.id)
    res = User.objects.get(id=request.user.id)
    month = request.GET.get('month')
    year = request.GET.get('year')
    result = OrderItem.objects.filter(table_no__rest_id=res.id, ordered=True, date__year=year,
                                      date__month=month)

    m_total = 0
    for i in result:
        m_total += i.product.Price
    messages.success(request, f'Months Income:{m_total} ')
    return render(request, 'rest_admin/report.html', {'m_total': m_total, 'restro': restro})


def orders(request):
    restro = User.objects.get(id=request.user.id)
    res = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        from_date = request.POST.get('fromDate')
        to_date = request.POST.get('toDate')
        order_list = Order.objects.filter(
            ordered_date__range=[from_date, to_date])
    else:
        order_list = Order.objects.filter(
            table_no__rest_id=res.id, ordered=True)

    return render(request, 'rest_admin/orders.html', {'order_list': order_list, 'restro': restro})


def order_details(request, id):
    restro = User.objects.get(id=request.user.id)
    res = User.objects.get(id=request.user.id)
    order_det = Order.objects.get(id=id)
    return render(request, 'rest_admin/order_details.html', {'order_det': order_det, 'user': res, 'restro': restro})


def today_order(request):
    restro = User.objects.get(id=request.user.id)
    res = User.objects.get(id=request.user.id)
    order_list = Order.objects.filter(table_no__rest_id=res.id, ordered=True,
                                      ordered_date__day=datetime.datetime.today().day, status='Pending')
    print(order_list)
    return render(request, 'rest_admin/today_order.html', {'order_list': order_list, 'restro': restro})


def order_complete(request, id):

    o_state = Order.objects.get(id=id)
    o_state.status = 'Complete'
    o_state.save()
    table = Table.objects.get(table_no=o_state.table_no.table_no)
    table.status = 'available'
    table.save()
    return render(request, 'rest_admin/payment.html', {'o_state': o_state})


class GeneratePdf(View):
    def get(self, request, id):
        o_state = Order.objects.get(id=id)
        o_state.status = 'Complete'
        o_state.save()
        table = Table.objects.get(table_no=o_state.table_no.table_no)
        table.status = 'available'
        table.save()
        list = Order.objects.get(id=id)

        data = {
            'bill_no': list.id,
            'sgst_amount': list.sgst_price(),
            'cgst_amount': list.cgst_price(),
            'total_gst': list.sc_total(),
            'rest_name': list.table_no.rest.restaurant_name,
            'Discount': list.table_no.rest.discount,
            'gst_number': list.table_no.rest.GST_Number,
            'rest_image': list.table_no.rest.profile_photo.url,
            'Table_No': list.table_no.table_no,
            'address': list.table_no.rest.address,
            'state': list.table_no.rest.state,
            'pin_code': list.table_no.rest.pin_code,
            'phone_no': list.table_no.rest.mobile_no,
            'Item': list.item.all(),
            'sgst': list.table_no.rest.SGST,
            'cgst': list.table_no.rest.CGST,
            'date': datetime.datetime.today().date(),
            'time': datetime.datetime.today().time(),


            'Total': list.get_total(),
            'grand_total': list.gst_total(),
        }
        pdf = render_to_pdf('rest_admin/invoice.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


def user_details(request):
    restro = User.objects.get(id=request.user.id)
    user = User.objects.get(id=request.user.id)
    return render(request, 'rest_admin/user_profile.html', {'user': user, 'restro': restro})


def update_details(request, id):
    restro = User.objects.get(id=request.user.id)
    res = User.objects.get(id=request.user.id)
    instance = get_object_or_404(User, id=res.id)

    form = RestaurantForm(request.POST or None, instance=instance)

    if form.is_valid():
        form.save()
        return redirect('rest_admin:user_profile')
    else:
        print(form.errors)
    return render(request, 'rest_admin/update_u.html', {'form': form, 'restro': restro})


def com_edit(request, id):
    instance = get_object_or_404(OrderItem, id=id)

    form = ComForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()

        return redirect('rest_admin:t_order')
    else:
        print(form.errors)
    return render(request, 'rest_admin/com_u.html', {'form': form})


def add_manager(request):
    restro = User.objects.get(id=request.user.id)
    res = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        print(request.FILES)

        if form.is_valid():

            form_r = form.save(commit=False)
            form_r.set_password(form_r.password)
            form_r.rest = res
            form_r.is_employee = True
            form_r.is_manager = True
            form_r.save()
            return redirect('rest_admin:manager_list')
        else:
            print(form.errors)
    else:
        form = EmployeeForm()

    return render(request, 'rest_admin/add_manager.html', {
        'form': form,
        'restro': restro
    })


def manager_list(request):
    restro = User.objects.get(id=request.user.id)
    res = User.objects.get(id=request.user.id)
    emp_lists = User.objects.filter(
        is_employee=True, is_manager=True, rest_id=res.id)

    return render(request, 'rest_admin/manager_list.html', {
        'emp_lists': emp_lists,
        'restro': restro
    })


def manager_form_edit(request, id):
    restro = User.objects.get(id=request.user.id)
    instance = get_object_or_404(User, id=id)
    form = EditEmployeeForm(
        request.POST or None, request.FILES or None, instance=instance)

    if form.is_valid():
        form.save()

        return redirect('rest_admin:manager_list')
    else:
        print(form.errors)
    return render(request, 'rest_admin/manager_edite.html', {
        'form': form,
        'restro': restro
    })


def manager_delete(request, id):
    user2 = User.objects.get(id=id).delete()
    return HttpResponseRedirect(reverse('rest_admin:manager_list'))
