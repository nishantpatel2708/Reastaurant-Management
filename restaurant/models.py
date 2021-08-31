from django.contrib.auth.models import User
from rest_admin.models import *
from django.core.validators import RegexValidator
from django.db import models
from rest_admin.models import *


class OrderItem(models.Model):
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(
        MenuTable, on_delete=models.CASCADE, related_name='product')
    quantity = models.PositiveIntegerField(default=1)
    comment = models.CharField(max_length=120, blank=True, null=True)
    table_no = models.ForeignKey(
        Table, on_delete=models.CASCADE, related_name='table_id')
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    status = models.CharField(max_length=30, default='pending')

    def __str__(self):
        return f"{self.quantity} of {self.product.Dish_Name}"

    def get_total_item_price(self):
        return self.quantity * self.product.Price


class Order(models.Model):
    table_no = models.ForeignKey(
        Table, on_delete=models.CASCADE, related_name='order_table_id')
    item = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    comment = models.CharField(max_length=120, blank=True, null=True)
    ordered = models.BooleanField(default=False)
    status = models.CharField(max_length=100)
    total_bill = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.table_no.rest.restaurant_name

    def get_total(self):
        total = 0
        for i in self.item.all():
            total += i.get_total_item_price()

        return total

    def sgst_price(self):
        total = 0
        for i in self.item.all():
            total += i.get_total_item_price()

        sgst = (total * int(self.table_no.rest.SGST)) / 100
        return sgst

    def cgst_price(self):
        total = 0
        for i in self.item.all():
            total += i.get_total_item_price()

        cgst = (total * int(self.table_no.rest.SGST)) / 100
        return cgst

    def sc_total(self):
        total = 0
        for i in self.item.all():
            total += i.get_total_item_price()

        gst = (total*int(self.table_no.rest.SGST))/100
        cgst = (total*int(self.table_no.rest.CGST))/100
        net_price = total+gst+cgst

        return round(net_price)

    def gst_total(self):
        total = 0
        for i in self.item.all():
            total += i.get_total_item_price()

        if self.table_no.rest.discount != 0:
            total -= self.table_no.rest.discount

        gst = (total*int(self.table_no.rest.SGST))/100
        cgst = (total*int(self.table_no.rest.CGST))/100
        net_price = total+gst+cgst
        if net_price < 0:
            net_price = 0
        else:
            net_price = net_price
        return round(net_price)
