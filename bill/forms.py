from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Order, Product, Purchase

def validate_email_unique(value):
	exists = User.objects.filter(email=value)
	if exists:
		raise ValidationError("This email address is alredy in use")


class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

class RegistrationForm(forms.ModelForm):
	password = forms.CharField(label='Password',widget=forms.PasswordInput)
	password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput)
	email = forms.EmailField(required=True, validators=[validate_email_unique])

	class Meta:
		model = User
		fields = ('username','first_name','last_name',)

	def clean_password2(self):
		cd = self.cleaned_data
		if cd['password']!=cd['password2']:
			raise forms.ValidationError('Password Do Not Match')
		return cd['password']

class OrderForm(forms.ModelForm):
	class Meta:
		model = Order
		fields = ('contact', 'address')

class ProductForm(forms.ModelForm):
	class Meta:
		model = Product
		fields = ('product_name',)

class PurchaseForm(forms.ModelForm):
	class Meta:
		model=Purchase
		fields = ('quantity',)