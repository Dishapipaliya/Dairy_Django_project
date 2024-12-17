from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.views import View  # Importing the View class
from .models import Product, Customer,Cart
from.forms import CustomRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404



# Define the home view
def home(request):
    return render(request, 'home.html')  # Ensure this template exists

def about(request):
    return render(request, 'about.html') 

def contact(request):
    return render(request, 'contact.html') 

class CategoryView(View):
    def get(self, request,val):
        product = Product.objects.filter(category=val)
        title=Product.objects.filter(category=val).values("title").annotate(total=Count("title"))
        return render(request, 'category.html',locals())  # Ensure this template exists
    
class CategoryTitle(View):
    def get(self, request,val):
        product = Product.objects.filter(title=val)
        title=Product.objects.filter(category=product[0].category).values('title')
        return render(request,'category.html',locals())  # Ensure this template exists


class ProductDetail(View):
    def get(self,request,pk):
        product=Product.objects.get(pk=pk)
        return render(request,"productdetail.html", {'product': product})
    
class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomRegistrationForm()
        return render(request,'customerregistration.html',locals())
    def post(self,request):
        form=CustomRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulations! User Registration Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request,'customerregistration.html',locals())
    


class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        # Your logic here, e.g., render a template
        return render(request, 'profile.html',locals())
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            
            reg = Customer(user=user, name=name, locality=locality, mobile=mobile, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, "Profile updated successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, 'profile.html', locals())
    

    

def address(request):
    add = Customer.objects.filter(user=request.user)  # Fetch addresses for the logged-in user
    return render(request, 'address.html', {'add': add})  # Pass 'add' to the template context


# def update_address(request, pk):
#     address = get_object_or_404(Customer, pk=pk)
#     # Add logic for updating the address (form handling, saving, etc.)
#     return render(request, 'update_address.html', {'address': address})


class  updateAddress(View):
    def get(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request,'updateAddress.html',locals())
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request, "Profile updated successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return redirect("address")

from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView

class MyPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('passwordchangedone')

def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('cart/')
from django.shortcuts import render
from .models import Cart

def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for item in cart:
        value = item.quantity * item.product.discounted_price
        amount += value
    totalamount = amount + 40  # Adding shipping fee or other charges
    
    return render(request, 'addtocart.html', {'cart': cart, 'amount': amount, 'totalamount': totalamount})


# def show_cart(request):
#     user=request.user
#     cart = Cart.object.filter(user=user)
#     amount = 0
#     for p in cart:
#        value = p.quantity * p.product.discounted_price
#        amount = amount + value  # Increment amount
#        totalamount = amount + 40 
#     return render(request,'addtocart.html',locals())

class checkout(View):
    def get(self,request):
        user=request.user
        add=Customer.objects.filter(user=user)  
        cart_items=Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
            totalamount = famount + 40
        return render(request,'checkout.html',locals())

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(Product=prod_id)& Q( user=request.user))
        c.quantity += 1
        c.save()
        user=request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount+value
            totalamount = amount + 40 
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(Product=prod_id)& Q( user=request.user))
        c.quantity -= 1
        c.save()
        user=request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount+value
            totalamount = amount + 40 
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)     

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(Product=prod_id)& Q( user=request.user))
        c.delete()
        user=request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount+value
            totalamount = amount + 40 
        data = {
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)
# def add_to_cart(request):
#     if request.method == 'GET':
#         prod_id = request.GET.get('prod_id')
#         if prod_id:
#             product = Product.objects.get(id=prod_id)
#             user = request.user
#             if user.is_authenticated:
#                 # Check if cart item already exists
#                 cart_item = Cart.objects.filter(user=user, product=product).first()
#                 if cart_item:
#                     # If it exists, increment the quantity
#                     cart_item.quantity += 1
#                     cart_item.save()
#                 else:
#                     # If not, create a new cart item
#                     Cart.objects.create(user=user, product=product, quantity=1)

#                 return redirect('cart/')  # Redirect to cart page
#     return redirect('product_list')  # Or another page if no product ID is passed







# from django.shortcuts import render
# from .models import Cart

# def show_cart(request):
#     # Assuming you're using the logged-in user to filter the cart
#     user = request.user
#     if user.is_authenticated:
#         cart = Cart.objects.filter(user=user)
#     else:
#         cart = []  # Empty cart if the user is not logged in
#     return render(request, 'addtocart.html', {'cart': cart})





# from django.http import JsonResponse
# from django.db.models import Q
# from .models import Cart, Product  # Ensure Product is imported

# def plus_cart(request):
#     if request.method == 'GET':
#         prod_id = request.GET.get('prod_id')
#         user = request.user

#         try:
#             cart_item = Cart.objects.get(Q(product_id=prod_id) & Q(user=user))
#             cart_item.quantity += 1
#             cart_item.save()
#         except Cart.DoesNotExist:
#             product = get_object_or_404(Product, id=prod_id)
#             cart_item = Cart.objects.create(product=product, user=user, quantity=1)
        
#         # Calculate total amounts
#         cart = Cart.objects.filter(user=user)
#         amount = sum([item.quantity * item.product.discounted_price for item in cart])
#         totalamount = amount + 40

#         data = {
#             'quantity': cart_item.quantity,
#             'amount': amount,
#             'totalamount': totalamount
#         }

#         return JsonResponse(data)
#     return JsonResponse({'error': 'Invalid request method'}, status=400)



# def minus_cart(request):
#     if request.method == 'GET':
#         prod_id = request.GET.get('prod_id')
#         user = request.user

#         try:
#             cart_item = Cart.objects.get(product_id=prod_id, user=user)
#             if cart_item.quantity > 1:
#                 cart_item.quantity -= 1
#                 cart_item.save()
#             else:
#                 cart_item.delete()
            
#             # Calculate total amounts
#             cart = Cart.objects.filter(user=user)
#             amount = sum([item.quantity * item.product.discounted_price for item in cart])
#             totalamount = amount + 40

#             data = {
#                 'amount': amount,
#                 'totalamount': totalamount
#             }
#             return JsonResponse(data)
#         except Cart.DoesNotExist:
#             return JsonResponse({'error': 'Item not found'}, status=404)


# def remove_cart(request):
#     if request.method == 'GET':
#         prod_id = request.GET.get('prod_id')
#         user = request.user

#         try:
#             cart_item = Cart.objects.get(product_id=prod_id, user=user)
#             cart_item.delete()
            
#             # Calculate total amounts
#             cart = Cart.objects.filter(user=user)
#             amount = sum([item.quantity * item.product.discounted_price for item in cart])
#             totalamount = amount + 40

#             data = {
#                 'amount': amount,
#                 'totalamount': totalamount
#             }
#             return JsonResponse(data)
#         except Cart.DoesNotExist:
#             return JsonResponse({'error': 'Item not found'}, status=404)


# class checkout(View):
#     def get(self,request):
#         user=request.user
#         add=Customer.objects.filter(user=user)  
#         cart_items=Cart.objects.filter(user=user)
#         famount = 0
#         for p in cart_items:
#             value = p.quantity * p.product.discounted_price
#             famount = famount + value
#             totalamount = famount + 40
#         return render(request,'checkout.html',locals())