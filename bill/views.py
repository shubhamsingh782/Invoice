from django.shortcuts import render, redirect
from .forms import ( LoginForm,
					 RegistrationForm,
					 OrderForm,
					 ProductForm,
					 PurchaseForm)
from django.contrib import auth
from .models import Order, Product, Purchase
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.forms import formset_factory
from .pdfgenerator import generate_pdf
# Create your views here.

def user_login(request):
	form = LoginForm()
	try:
		orders = Order.objects.all()
		orders =orders.filter(user=request.user)
	except:
		orders=None
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = auth.authenticate(username=cd['username'], password=cd['password'])
			if user:
				auth.login(request, user)
				try:
					orders = Order.objects.all()
					orders =orders.filter(user=user)
				except:
					orders=None
				return render(request, 'base.html', {'user':user,'orders': orders})
			else:
				return render(request, 'base.html', {'error':'Invalid Credentials','form':form})
		else:
			return render(request, 'base.html', {'error':'All fields are mandatory','form':form})
	else:
		return render(request, 'base.html', {'form':form,'orders':orders})


def register(request):
	user_form = RegistrationForm()
	if request.method=='POST':
		user_form = RegistrationForm(request.POST)
		if user_form.is_valid():
			new_user = user_form.save(commit=False)
			new_user.set_password(user_form.cleaned_data['password'])
			new_user.save()
			return redirect('/')
		else:
			return render(request,'register.html', {'form':user_form})
	else:
		return render(request, 'register.html', {'form':user_form})


@login_required(login_url='/')
def place_order(request):
	order_form = OrderForm()
	try:
		products = Product.objects.all()
	except:
		products=None
	if request.method == "POST":
		list_quantity=[]
		list_name=[]
		net_cost=0
		order = OrderForm(request.POST)

		if order.is_valid():
			new_order = order.save(commit=False)
		new_order.user = request.user
		new_order.save()

		for i in range(5):
			list_name.append(request.POST.get('name'+str(i)))
			list_quantity.append(request.POST.get('quantity'+str(i)))

		for i in range(5):
			if list_quantity[i] and list_name[i]:
				try:
					product = Product.objects.get(pk=int(list_name[i]))
				except:
					product = None
				if product:
					purchase=Purchase(order=new_order, product=product, quantity=int(list_quantity[i]))
					purchase.save()
					net_cost+=purchase.total_cost()

		new_order.total_product_cost=net_cost
		new_order.save()

		return redirect('/')
	else:
		return render(request, 'order.html', {'products':products,'range':range(5), 'order_form':order_form})

@login_required(login_url='/')
def print_pdf(request, pk):
	try:
		order = Order.objects.get(pk=pk)
	except:
		order = None
	try:
		purchases = Purchase.objects.filter(order=order)
	except:
		purchases=None

	net_cost = 0
	for purchase in purchases:
		net_cost+=purchase.total_cost()

	net_cost+=net_cost*(order.tax/100)
	return render(request, 'bill.html' ,{'order':order, 'purchases':purchases,'net_cost':net_cost})

@login_required(login_url='/')
def pdf_view(response, pk):
	try:
		order = Order.objects.get(pk=pk)
	except:
		order = None
	try:
		purchases = Purchase.objects.filter(order=order)
	except:
		purchases=None

	net_cost = 0
	for purchase in purchases:
		net_cost+=purchase.total_cost()

	net_cost+=net_cost*(order.tax/100)
	resp = HttpResponse(content_type='application/pdf')
	result = generate_pdf('bill.html',file_object=resp, context={'order':order, 'purchases':purchases,'net_cost':net_cost})
	return result

	
@login_required(login_url='/')
def logout(request):
	auth.logout(request)
	return redirect('/')
