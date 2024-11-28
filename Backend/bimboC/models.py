from django.db import models

class Product(models.Model):
    product = models.CharField(primary_key=True, max_length=50)
    description = models.CharField(max_length=50)
    
class Truck(models.Model):
    truck_number = models.CharField(max_length=50, primary_key=True)
    location = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    size = models.CharField(max_length=50)

class OutGoingOrder(models.Model):
    id = models.AutoField(primary_key=True)
    order_number = models.IntegerField(unique=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    order_date = models.DateField()
    price = models.FloatField()
    creation_date = models.DateField()
    detail = models.CharField(max_length=50)
    og_quantity = models.IntegerField()
    requested_quantity = models.IntegerField()
    assigned_quantity = models.IntegerField()
    packed_quantity = models.IntegerField()


class ActiveStock(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, unique=True)
    available = models.IntegerField()
    assigned = models.IntegerField()
    total_active = models.IntegerField()

class ReserveStock(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, unique=True)
    received = models.IntegerField()
    located = models.IntegerField()
    partially_assigned = models.IntegerField()
    assigned = models.IntegerField()
    lost = models.IntegerField()
    total_reserve = models.IntegerField()

class StockOBLPN(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, unique=True)
    picking = models.IntegerField()
    packed = models.IntegerField()
    loaded = models.IntegerField()
    total_oblpn = models.IntegerField()

class Remission(models.Model):
    id = models.AutoField(primary_key=True)
    embark = models.CharField(max_length=50, unique=True)
    box_number = models.ForeignKey(Truck, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(null=True, blank=True)

class Pending(models.Model):
    id = models.AutoField(primary_key=True)
    close_dt = models.DateField()  
    embark = models.CharField(max_length=50)
    order = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    send_dt = models.DateField()
    quantity = models.IntegerField()
    lpn = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default="En ruta")

