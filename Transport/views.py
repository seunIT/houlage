from datetime import datetime
from django.shortcuts import render, HttpResponse,redirect
from .models import AutoMobile,Vehicle,Brand,Booking,Rent,Locations
from Cart.models import cart
from Orders.models import order,Status
from .forms import DateForm, CarForm
# Create your views here.
def AutomobileView(request):
	template='Transport/automobile.html'
	automobile = AutoMobile.objects.all()
	vehic= Vehicle.objects.all()
	context={
	'automobile':automobile,
	'vehic':vehic,
	}
	return render(request,template,context)

def Auto_details(request,pk):
	template= 'Transport/auto_detail.html'
	details = AutoMobile.objects.get(pk=pk)
	carts, new_obj=cart.objects.new_or_get(request)
	cart_id=request.session.get('cart_id', None)
	if request.user.is_authenticated:
		RentInfo= Rent.objects.filter(Automobile__pk=details.pk, user=request.user)
	else:
		RentInfo= Rent.objects.filter(Automobile__pk=details.pk, Cart__id=cart_id)

	dateForm=DateForm(None)
	context={
	'details':details,
	'carts':carts,
	'dateForm':dateForm,
	'RentInfo':RentInfo,
	}
	return render(request,template,context)	

def BookingView(request):
	template='Transport/bookInfo.html'
	if request.method=='POST':
		vehicle=request.POST.get('vehicle')
		Brand=request.POST.get('Brand')
		modl=request.POST.get('Model')
		source=request.POST.get('Source')
		Destination=request.POST.get('Destination')
		context={
		'vehicle':vehicle,
		'Brand':Brand,
		'modl':modl,
		'source':source,
		'Destination':Destination,
		}
		return render(request, template, context)

def RentCreate(request):
	if request.method=='POST':
		detail=request.POST.get('automobile')
		Autos = AutoMobile.objects.get(pk=detail) 
		pickup=request.POST.get('pickup_date')
		returns=request.POST.get('return_date')
		date_format = "%Y-%m-%d"
		day1=datetime.strptime(str(pickup), date_format)
		day2=datetime.strptime(str(returns), date_format)
		delta=day2-day1

		carts,new_obj= cart.objects.new_or_get(request)	
		price=Autos.Cost * int(delta.days)
		User=request.user
		print(User)
		if not User.is_authenticated:
			Rent_create= Rent.objects.create(
				user=None,
				Automobile=Autos,
				Cart=carts,
				pickup_date=pickup,
				return_date=returns,
				Cost=price,
				days=delta.days,
				)	

		else:
			user_obj=request.user
			Rent_create= Rent.objects.create(
			user=user_obj,
			Automobile=Autos,
			Cart=carts,
			pickup_date=pickup,
			return_date=returns,
			Cost=price,
			days=delta.days,
			)		
		Rent_create.save()

	return redirect('cart_home')

def RemoveRent(request,rpk):
	rent_obj_delete= Rent.objects.get(pk=rpk).delete()
	return redirect('cart_home')

def PickUp (request):
	template= "Transport/pickup.html"
	pickup = request.GET.get('pickup')
	cost=0
	if pickup =="pick":
		cost=0
	elif pickup =="deliver":
		cost=200
	print (cost)
	locations = Locations.objects.all()
	context = {
		'pickup':pickup,
		'locations':locations,
		'cost':cost,
	}
	print (pickup)
	return render(request,template,context)

def Approve_Order(request):
	template= "Admin/order-approve.html"
	order_id=request.GET.get('val')
	Order= order.objects.get(id=order_id)
	cart_id=cart.objects.get(id=Order.Carts.id)
	Auto=Rent.objects.filter(Cart=cart_id)
	status=Status.objects.get(id=4)
	for auto in Auto:
		autos_id=auto.Automobile.id
		avai=AutoMobile.objects.get(id=autos_id)
		avai.Availability=False
		avai.save()
	Order.status=status
	Order.save()
	return render(request,template)

def Cancel_Order(request):
	template= "Admin/order-cancel.html"
	order_id=request.GET.get('val')
	Order= order.objects.get(id=order_id)
	cart_id=cart.objects.get(id=Order.Carts.id)
	Auto=Rent.objects.filter(Cart=cart_id)
	status=Status.objects.get(id=5)
	for auto in Auto:
		autos_id=auto.Automobile.id
		avai=AutoMobile.objects.get(id=autos_id)
		avai.Availability=True
		avai.save()
	Order.status=status
	Order.save()
	return render(request,template)

def Edit_cars(request):
	template="Admin/editcars.html"
	if request.method=='GET':
		cars=AutoMobile.objects.all()
		form = CarForm()
		context={
			'cars':cars,
			'form':form
		}

		return render(request,template,context)
	elif request.method=='POST':
		vehicle_id= request.POST.get("Vehicle_id")
		brand_id= request.POST.get("Brands")
		model= request.POST.get("Model")
		color= request.POST.get("Color")
		seat=request.POST.get("No_of_Seat")
		Image=request.FILES.get("image")
		Air_Condition=request.POST.get("Air_Condition")
		Availability=request.POST.get("Availability")
		Cost=request.POST.get("Cost")

		vehicle= Vehicle.objects.get(id=vehicle_id)
		brands=Brand.objects.get(id=brand_id)
		if Air_Condition or Availability =="on":
			Air_Condition=True
			Availability=True
		elif Air_Condition or Availability !="on":
			Air_Condition=False
			Availability=False
		car_create = AutoMobile.objects.create(
			Vehicle_id=vehicle,
			Brands=brands,
			Model=model,
			Color=color,
			No_of_Seat=seat,
			image=Image,
			Air_Condition=Air_Condition,
			Availability=Availability,
			Cost=Cost
		)
		car_create.save()
		return redirect('edit_cars')

def Load_cars(request):
	template="Admin/Load-cars.html"
	car_id = request.GET.get('val')

	car= AutoMobile.objects.get(id=car_id)
	form=CarForm()
	context = {
		'car':car,
		'form':form
	}
	return render(request,template,context)
	if request.method=='POST':
		vehicle_id= request.POST.get("Vehicle_id")
		brand_id= request.POST.get("Brands")
		model= request.POST.get("Model")
		color= request.POST.get("Color")
		seat=request.POST.get("No_of_Seat")
		Image=request.FILES.get("image")
		Air_Condition=request.POST.get("Air_Condition")
		Availability=request.POST.get("Availability")
		Cost=request.POST.get("Cost")

		vehicle= Vehicle.objects.get(id=vehicle_id)
		brands=Brand.objects.get(id=brand_id)
		if Air_Condition or Availability =="on":
			Air_Condition=True
			Availability=True
		elif Air_Condition or Availability !="on":
			Air_Condition=False
			Availability=False
		
		car.Vehicle_id=vehicle,
		car.Brands=brands,
		car.Model=model,
		car.Color=color,
		car.No_of_Seat=seat,
		car.image=Image,
		car.Air_Condition=Air_Condition,
		car.Availability=Availability,
		car.Cost=Cost
		car.save()
		return redirect('edit_cars')	

	
