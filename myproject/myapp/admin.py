from django.contrib import admin
from .models import Product,Customer,Cart,Payment,OrderPlaced

class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'selling_price', 'discounted_price', 'category','product_image']
admin.site.register(Product, ProductModelAdmin)

class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'locality', 'city', 'state','zipcode']
admin.site.register(Customer, CustomerModelAdmin)


class CartModelAdmin(admin.ModelAdmin):
    list_display=['id','user','product','quantity']
admin.site.register(Cart,CartModelAdmin)

class PaymentModelAdmin(admin.ModelAdmin):
    list_display=['id','user','amount','razorpay_order_id','razorpay_paymenr_status','razorpay_payment_id','paid']
admin.site.register(Payment,PaymentModelAdmin)

class OrderPlaceAdmin(admin.ModelAdmin):
    list_display=['id','user','customer','product','quantity','ordered_date','status','payment']
admin.site.register(OrderPlaced,OrderPlaceAdmin)