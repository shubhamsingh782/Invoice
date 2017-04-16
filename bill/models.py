from django.db import models
from django.conf import settings

# Create your models here.

class Order(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	contact = models.IntegerField()
	address = models.CharField(max_length=500)
	total_product_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True)
	tax = models.DecimalField(max_digits=10, decimal_places=2, default=5)
	order_made_on = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.id)

class Product(models.Model):
	product_name = models.CharField(max_length=200)
	cost = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return self.product_name


class Purchase(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)

	def total_cost(self):
		return self.quantity*self.product.cost

	def __str__(self):
		return self.product.product_name