from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout as django_logout 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from slice .models import (UserInformation,ContactSubmission,SecondContactSubmission,
                        Course,UserCourse,User_Academy_Product,
                        Academy_Product,User_Coffee_Delivery,Coffee_Delivery,MyCart,
                        CartItem,FavoriteItem,Notification,
                        PaymentConfirmation)
from slice import models
from .forms import ContactForm,SecondContactForm,ProductForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import update_session_auth_hash
from .forms import ChangePasswordForm
from django.contrib.auth.forms import PasswordChangeForm
from .forms import PaymentForm
from decimal import Decimal
from django.utils import timezone
from django.db.models import F
import random
import string







from django.views.decorators.http import require_http_methods
import hashlib
import base64
import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import urllib.parse





def get_cart_item_count(user):
    if user.is_authenticated:
        cart = MyCart.objects.filter(user=user).first()
        if cart:
            cart_items = cart.cartitem_set.all()
            return cart_items.count()
        else:
            return 0 
        
    return 0



def home(request):
    if request.user.is_authenticated:
        user = request.user
        cart_items = CartItem.objects.filter(cart__user=user)
        total_items = sum(cart_item.quantity for cart_item in cart_items)
        notification_count = get_notification_count(user)
    else:
        total_items = 0
        notification_count = 0

    context = {
        'total_items': total_items,
        'notification_count': notification_count,
    }
    return render(request, 'main/home.html', context)



def cofe_home(request):
    if request.user.is_authenticated:
        user = request.user
        cart_items = CartItem.objects.filter(cart__user=user)
        total_items = sum(cart_item.quantity for cart_item in cart_items)
        notification_count = get_notification_count(user)
    else:
        total_items = 0
        notification_count = 0
    context = {
        'total_items': total_items,
        'notification_count' : notification_count
    }
    return render(request,'main/cofe_home.html',context)




def cake_education(request):
    user = request.user
    courses = Course.objects.all()
    notification_count = get_notification_count(user)
    cart_items = None  

    if request.user.is_authenticated:
        user = request.user
        try:
            cart_items = CartItem.objects.filter(cart__user=user)
        except CartItem.DoesNotExist:
            cart_items = None

        total_items = sum(cart_item.quantity for cart_item in cart_items)
    else:
        total_items = 0
    
    context = {
        'courses' : courses,
        'total_items': total_items,
        'cart_items': cart_items,  
        'notification_count':notification_count
    }
    return render(request, 'main/cake_education.html', context)






def cofee_delivery(request):
    coffee_delivery = Coffee_Delivery.objects.all()
    

    discounted_coffee_delivery = Coffee_Delivery.objects.filter(
        discount_price__isnull=False
    )
    if request.user.is_authenticated:
        user = request.user
        cart_items = CartItem.objects.filter(cart__user=user)
        total_items = sum(cart_item.quantity for cart_item in cart_items)
        notification_count = get_notification_count(user)
    else:
        total_items = 0
        notification_count = 0


    context = {
        'coffee_delivery' : coffee_delivery,
        'total_items': total_items,
        'notification_count' : notification_count
    }

    return render(request,'main/cofee_delivery.html',context)



def academy(request):
    user = request.user
    academy_product = Academy_Product.objects.all()
    notification_count = get_notification_count(user)
    notification_count = get_notification_count(user)
    discounted_academy_products = Academy_Product.objects.filter(
        discount_price__isnull=False
    )
    if request.user.is_authenticated:
        user = request.user
        cart_items = CartItem.objects.filter(cart__user=user)
        total_items = sum(cart_item.quantity for cart_item in cart_items)
        
    else:
        total_items = 0
        


    context = {
        'academy_product' : academy_product,
        'total_items': total_items,
        'notification_count' : notification_count
    }
    return render(request,'main/academy.html',context)





def courses(request,course_id):
    courses = get_object_or_404(Course, pk=course_id)
    
    if request.user.is_authenticated:
        user_course, created = UserCourse.objects.get_or_create(user=request.user, courses=courses)
    else:
        user_course = None

    context ={
        'courses' : courses,
        'user_course' : user_course
    }
    return render(request,'index.html',context)




def coffee_delivery_sale(request,coffee_delivery_sale_id):
    coffee_delivery_sale = get_object_or_404(Coffee_Delivery, pk=coffee_delivery_sale_id)
    
    if request.user.is_authenticated:
        user_coffee_delivery, created = User_Coffee_Delivery.objects.get_or_create(user=request.user,
                                                                coffee_delivery_sale= coffee_delivery_sale)
    else:
        user_coffee_delivery = None

    context ={
        'coffee_delivery_sale' : coffee_delivery_sale,
        'user_coffee_delivery' : user_coffee_delivery
    }
    return render(request,'index.html',context)





def academy_sale(request,academy_sale_id):
    academy_sale = get_object_or_404(Academy_Product, pk=academy_sale_id)
    
    if request.user.is_authenticated:
        user_academy_product, created = User_Academy_Product.objects.get_or_create(user=request.user,
                                                                         academy_sale=academy_sale)
    else:
        user_academy_product = None

    context ={
        'academy_sale' : academy_sale,
        'user_academy_product' : user_academy_product
    }
    return render(request,'index.html',context)






@login_required
def dashboard(request):
    user = request.user
    favorite_items = FavoriteItem.objects.filter(user=request.user)
    change_password_form = PasswordChangeForm(user=request.user)
    favorite_count = get_favorite_count(user)

    user_information = None
    previous_orders = None

    try:
        user_information = UserInformation.objects.get(user=request.user)
        previous_orders = CartItem.objects.filter(userinformation=user_information)
    except UserInformation.DoesNotExist:
        user_information = None
        previous_orders = None

    if previous_orders is not None:
        for order in previous_orders:
            order.created_at = timezone.localtime(order.created_at)

            try:
                order.my_cart = MyCart.objects.get(items=order)
            except MyCart.DoesNotExist:
                order.my_cart = None

            if order.my_cart:
                for cart_item in order.my_cart.items.all():
                    if cart_item.academy_product:
                        cart_item.product = cart_item.academy_product
                    elif cart_item.coffee_delivery:
                        cart_item.product = cart_item.coffee_delivery
                    elif cart_item.course:
                        cart_item.product = cart_item.course


    try:
        user_information = UserInformation.objects.get(user=request.user)
    except UserInformation.DoesNotExist:
        user_information = None

    academy_product = Academy_Product.objects.first() 
    coffee_delivery = Coffee_Delivery.objects.first()

    favorite_academy_products = Academy_Product.objects.filter(
        user_academy_product__user=request.user
    )
    
    favorite_coffee_deliveries = Coffee_Delivery.objects.filter(
        user_coffee_delivery__user=request.user
    )

    check_discounts_and_notify_user(request.user)
    user_notifications = Notification.objects.filter(user=request.user)

    context = {
        'change_password_form': change_password_form,
        'user_information': user_information,
        'favorite_items': favorite_items,
        'academy_product': academy_product,  
        'coffee_delivery': coffee_delivery,
        'favorite_academy_products': favorite_academy_products,
        'favorite_coffee_deliveries': favorite_coffee_deliveries,
        'user_notifications': user_notifications,
        'previous_orders': previous_orders,
        'favorite_count': favorite_count, 

    }
    return render(request,'main/dashboard.html',context)



def login_register(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('home')
    else:
        messages.error(request, "Invalid email or password.")

    return render(request, 'main/login_register.html')



def custom_logout(request):
    django_logout(request)
    return redirect('home')



def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            existing_user = User.objects.get(username=username)
            messages.error(request, "Username already taken.")
            return redirect("register")
        except User.DoesNotExist:
            user = User.objects.create_user(username=username, email=email, password=password)
            userinfo = UserInformation.objects.create(user=user, email=email)

            user = authenticate(request, username=username, password=password)
            login(request, user)

            messages.success(request, "Registration successful. You are now logged in.")
            return redirect("home")
    
    return render(request, "main/login_register.html")



def contact(request):
    success_message = None  
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            submission = ContactSubmission(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            submission.save()

            success_message = 'Your message has been sent successfully!'
    
    else:
        form = ContactForm()

    return render(request, 'main/home.html', {'form': form, 'success_message': success_message})





def second_contact(request):
    success_message = None  
    if request.method == 'POST':
        form = SecondContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            Second_submission = SecondContactSubmission(
                name=name,
                email=email,
                message=message
            )
            Second_submission.save()

            success_message = 'Your message has been sent successfully!'
    
    else:
        form = ContactForm()

    return render(request, 'main/home.html', {'form': form, 'success_message': success_message})





@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            messages.success(request, 'Your password was successfully updated!')
            return redirect('academy')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')
    else:
        form = ChangePasswordForm(user=request.user)
    return render(request, 'main/dashboard.html', {'form': form})





def change_password_done(request):
    messages.success(request, 'Your password was successfully updated!')
    return render(request,'main/dashboard.html')





@login_required(login_url="/login_register/")
def cart_add(request, academy_product_id=None, coffee_delivery_id=None):

    user = request.user
    cart, created = MyCart.objects.get_or_create(user=user)

    academy_product = None
    coffee_delivery = None

    if academy_product_id:
        academy_product = get_object_or_404(Academy_Product, id=academy_product_id)
    elif coffee_delivery_id:
        coffee_delivery = get_object_or_404(Coffee_Delivery, id=coffee_delivery_id)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        academy_product=academy_product,
        coffee_delivery=coffee_delivery,

    )

    if not created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1
    


    if academy_product:
        if academy_product.discount_price is not None:
            cart_item.total_price = academy_product.discount_price * cart_item.quantity
        else:
            cart_item.total_price = academy_product.price * cart_item.quantity
    elif coffee_delivery:
        if coffee_delivery.discount_price is not None:
            cart_item.total_price = coffee_delivery.discount_price * cart_item.quantity
        else:
            cart_item.total_price = coffee_delivery.price * cart_item.quantity

    cart_item.save()
    return redirect("cart_detail")
    



@login_required(login_url="/login_register/")
def item_clear(request, academy_product_id=None, coffee_delivery_id=None):
    user = request.user
    cart, created = MyCart.objects.get_or_create(user=user)

    if academy_product_id:
        item = get_object_or_404(Academy_Product, id=academy_product_id)
        cart_items = CartItem.objects.filter(cart=cart, academy_product=item)
    elif coffee_delivery_id:
        item = get_object_or_404(Coffee_Delivery, id=coffee_delivery_id)
        cart_items = CartItem.objects.filter(cart=cart, coffee_delivery=item)
    else:
        return HttpResponse("Invalid request", status=400)

    cart_items.delete()

    return redirect("cart_detail")



@login_required(login_url="/users/login")
def item_increment(request, id):
    cart = MyCart.objects.get(user=request.user)
    cartitem = CartItem.objects.get(id=id)  
    cart.add(cartitem=cartitem)  
    return redirect("cart_detail")




@login_required(login_url="/login_register/")
def item_decrement(request, id):
    cart_item = get_object_or_404(CartItem, id=id)
    
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect("cart_detail")



@login_required(login_url="/login_register/")
def cart_clear(request):
    user = request.user
    try:
        cart = MyCart.objects.get(user=user)
        cart.delete()
    except MyCart.DoesNotExist:
        messages.error(request, "Cart not found.")
    return redirect("cart_detail")


@login_required(login_url="/login_register/")
def cart_detail(request):
    
    user = request.user
    cart_items = CartItem.objects.filter(cart__user=user)  
    total_items = sum(cart_item.quantity for cart_item in cart_items)
    total_item_price = Decimal(0)
    overall_total_price = Decimal(0)

    for cart_item in cart_items:
        total_item_price += cart_item.get_total_item_price()
        overall_total_price += cart_item.total_price

    total_item_price_float = float(total_item_price)
    overall_total_price_float = float(overall_total_price)


    context = {
        'cart_items': cart_items,
        'total_items': total_items,
        'total_item_price': total_item_price,
        'overall_total_price': overall_total_price,
    }

    return render(request, 'main/cart_detail.html', context)


    




SANAL_POS = {
    'customer_id': '400235',
    'merchant_id': '496',
    'username': 'apitest',
    'password': 'api123',
    'ok_url': 'http://127.0.0.1:8000/ok-url/',
    'fail_url': 'http://127.0.0.1:8000/fail-url/',
    'kart_onay_url': 'https://boatest.kuveytturk.com.tr/boa.virtualpos.services/Home/ThreeDModelPayGate',
    'odeme_onay_url': 'https://boatest.kuveytturk.com.tr/boa.virtualpos.services/Home/ThreeDModelProvisionGate',
} # DEBUG == True şeklinde kontrol yaparak prod'a göre conf yapabilirsiniz


   

@login_required
def index(request):
    user_info = None
    cart_item_count = get_cart_item_count(request.user)
    payment_form = PaymentForm(request.POST or None)

    
    if request.method == 'POST':
        try:
            user = request.user
            user_info, created = UserInformation.objects.get_or_create(user=user)
            user_info.full_name = request.POST.get('full_name')
            user_info.city = request.POST.get('city')
            user_info.email = request.POST.get('email')
            user_info.phone_number = request.POST.get('phone_number')
            user_info.street = request.POST.get('street')
            user_info.district = request.POST.get('district')
            user_info.address = request.POST.get('address')
            

            user_info.save()

            cart = MyCart.objects.filter(user=user).first()
            if cart:
                for cart_item in cart.items.all():
                    cart_item.userinformation = user_info
                    cart_item.ordered = True
                    cart_item.save()
                
                total_price = sum(item.get_total_item_price() for item in cart.items.all())
                request.session['payment_success'] = True
                return redirect('odeme', total_price=total_price)

            else:
                return render(request, 'payment_failed.html')
        
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    cart = MyCart.objects.filter(user=request.user).first()
    context = {
        'cart_items': cart.items.all() if cart else [],
        'total_price': sum(item.get_total_item_price() for item in cart.items.all()),
        'user_info': user_info,
        'cart_item_count': cart_item_count,
        'payment_form': payment_form,
       
    }

    return render(request, 'index.html', context)






def generate_reference_code(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))




@login_required
def payment_confirmation(request,course_id):
    user = request.user
    user_course = None
    course = None

   
    if course_id:
        course = get_object_or_404(Course, pk=course_id)
        user_course = UserCourse(user=request.user, course=course)
        user_course.save()
        
    else:
        cart_items = CartItem.objects.filter(cart__user=user)
        total_price = sum(cart_item.total_price for cart_item in cart_items)
        print("Total Price:", total_price)
    user = request.user
    user_info, created = UserInformation.objects.get_or_create(user=user)


    reference_code = generate_reference_code()
    print("Generated Reference Code:", reference_code)
    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)
        
        if payment_form.is_valid():
            print("Payment Form is Valid")
            card_number = payment_form.cleaned_data['number']
            cvc = payment_form.cleaned_data['cvc']
            expiry = payment_form.cleaned_data['expiry']
            cardholder_name = payment_form.cleaned_data['name']
            
            user_info.full_name = request.POST.get('full_name')
            user_info.city = request.POST.get('city')
            user_info.email = request.POST.get('email')
            user_info.phone_number = request.POST.get('phone_number')
            user_info.street = request.POST.get('street')
            user_info.district = request.POST.get('district')
            user_info.address = request.POST.get('address')
            user_info.save()

            total_price = sum(cart_item.total_price for cart_item in CartItem.objects.filter(cart__user=user))


            for cart_item in cart_items:
                cart_item.userinformation = user_info
                cart_item.ordered = True
                cart_item.save()

            
            PaymentConfirmation.objects.create(user=user_info,
                                                amount=total_price,
                                                 reference_code=reference_code)

            request.session['payment_success'] = True
            print("Payment success")
            return redirect('payment_confirmation', course_id=course_id)
        else:
            print("Payment form is not valid:", payment_form.errors)
            return redirect('payment_failed') 

    else:
        payment_form = PaymentForm()

    context = {
        'payment_form': payment_form,
        'user_info': user_info,
        'payment_success': True,
        'reference_code': reference_code,
    }

    return render(request, 'main/payment_confirmation.html', context)


def payment_failed(request):
    return render(request,'main/payment_failed.html')

# @require_http_methods(['POST'])
# def odeme(request,course_id=None):
#     user = request.user
#     user_course = None
#     course = None

   
#     if course_id:
#         course = get_object_or_404(Course, pk=course_id)
#         user_course = UserCourse(user=request.user, course=course)
#         user_course.save()
        
#     else:
#         cart_items = CartItem.objects.filter(cart__user=user)
#         total_price = sum(cart_item.total_price for cart_item in cart_items)
#         print("Total Price:", total_price)


#     name = request.POST.get('name')
#     expiry = request.POST.get('expiry').split('/')
#     year = expiry[1].strip()
#     month = expiry[0].strip()
#     number = request.POST.get('number').replace(' ', '')
#     cvc = request.POST.get('cvc')
#     merchant_order_id = 'web-odeme'


#     tutar = int(total_price * 100) if not course else int(course.price * 100)

#     hashed_password = base64.b64encode(hashlib.sha1(f"{SANAL_POS['password']}".encode('ISO-8859-9')).digest()).decode()
#     hashed_data = base64.b64encode(hashlib.sha1(
#         f"{SANAL_POS['merchant_id']}{merchant_order_id}{tutar}{SANAL_POS['ok_url']}{SANAL_POS['fail_url']}{SANAL_POS['username']}{hashed_password}".encode(
#             'ISO-8859-9')).digest()).decode()
#     data = f"""
#         <KuveytTurkVPosMessage xmlns:xsi="http://www.w3.org/2001/XMLSchemainstance"
#     xmlns:xsd="http://www.w3.org/2001/XMLSchema">
#     <APIVersion>1.0.0</APIVersion>
#     <OkUrl>{str(SANAL_POS["ok_url"])}</OkUrl>
#     <FailUrl>{str(SANAL_POS["fail_url"])}</FailUrl>
#     <HashData>{hashed_data}</HashData>
#     <MerchantId>{int(SANAL_POS['merchant_id'])}</MerchantId>
#     <CustomerId>{int(SANAL_POS['customer_id'])}</CustomerId>
#     <UserName>{str(SANAL_POS['username'])}</UserName>
#     <CardNumber>{str(number)}</CardNumber>
#     <CardExpireDateYear>{str(year)}</CardExpireDateYear>
#     <CardExpireDateMonth>{str(month)}</CardExpireDateMonth>
#     <CardCVV2>{str(cvc)}</CardCVV2>
#     <CardHolderName>{str(name)}</CardHolderName>
#     <CardType>Troy</CardType>
#     <TransactionType>Sale</TransactionType>
#     <InstallmentCount>{int('0')}</InstallmentCount>
#     <Amount>{int(tutar)}</Amount>
#     <DisplayAmount>{int(tutar)}</DisplayAmount>
#     <CurrencyCode>{str('0949')}</CurrencyCode>
#     <MerchantOrderId>{str(merchant_order_id)}</MerchantOrderId>
#     <TransactionSecurity>{int('3')}</TransactionSecurity>
#     </KuveytTurkVPosMessage>
#     """
#     headers = {'Content-Type': 'application/xml'}
#     r = requests.post(SANAL_POS['kart_onay_url'], data=data.encode('ISO-8859-9'), headers=headers)
#     return HttpResponse(r)


# @require_http_methods(['POST'])
# @csrf_exempt
# def ok_url(request):
#     gelen = request.POST.get('AuthenticationResponse')
#     data = urllib.parse.unquote(gelen)
#     merchant_order_id_start = data.find('<MerchantOrderId>')
#     merchant_order_id_stop = data.find('</MerchantOrderId>')
#     merchant_order_id = data[merchant_order_id_start + 17:merchant_order_id_stop]
#     amount_start = data.find('<Amount>')
#     amount_end = data.find('</Amount>')
#     amount = data[amount_start + 8:amount_end]
#     md_start = data.find('<MD>')
#     md_end = data.find('</MD>')
#     md = data[md_start + 4:md_end]
#     hashed_password = base64.b64encode(
#         hashlib.sha1(SANAL_POS["password"].encode('ISO-8859-9')).digest()).decode()
#     hashed_data = base64.b64encode(hashlib.sha1(
#         f'{SANAL_POS["merchant_id"]}{merchant_order_id}{amount}{SANAL_POS["username"]}{hashed_password}'.encode(
#             "ISO-8859-9")).digest()).decode()
#     xml = f"""
#     <KuveytTurkVPosMessage xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
#     xmlns:xsd="http://www.w3.org/2001/XMLSchema">
#     <APIVersion>1.0.0</APIVersion>
#     <HashData>{hashed_data}</HashData>
#     <MerchantId>{int(SANAL_POS['merchant_id'])}</MerchantId>
#     <CustomerId>{int(SANAL_POS['customer_id'])}</CustomerId>
#     <UserName>{str(SANAL_POS['username'])}</UserName>
#     <TransactionType>Sale</TransactionType>
#     <InstallmentCount>0</InstallmentCount>
#     <Amount>{amount}</Amount>
#     <MerchantOrderId>{str(merchant_order_id)}</MerchantOrderId>
#     <TransactionSecurity>3</TransactionSecurity>
#     <KuveytTurkVPosAdditionalData>
#     <AdditionalData>
#     <Key>MD</Key>
#     <Data>{md}</Data>
#     </AdditionalData>
#      </KuveytTurkVPosAdditionalData>
#     </KuveytTurkVPosMessage>
#     """
#     headers = {'Content-Type': 'application/xml'}
#     r = requests.post(SANAL_POS['odeme_onay_url'], data=xml.encode('ISO-8859-9'), headers=headers)
#     return HttpResponse(r)


# @require_http_methods(['POST'])
# @csrf_exempt
# def fail_url(request):
#     return HttpResponse("Payment_Failed")






def add_to_favorite(request, item_type, item_id):
    user = request.user
    favorite_item = None

    if item_type == 'academy_product':
        item = Academy_Product.objects.get(pk=item_id)
        favorite_item, created = FavoriteItem.objects.get_or_create(user=user, academy_product=item)
    elif item_type == 'coffee_delivery':
        item = Coffee_Delivery.objects.get(pk=item_id)
        favorite_item, created = FavoriteItem.objects.get_or_create(user=user, coffee_delivery=item)

    if favorite_item:
        if created:
            success_message = "Item added to favorites successfully!"
        else:
            success_message = "Item is already in your favorites!"

        if item.discount_price is not None:
            favorite_item.discounted_price = item.discount_price
            favorite_item.save()
            
    else:
        failure_message = "Failed to add item to favorites." 
        return render(request, 'main/home.html', {'message': failure_message})

    return redirect('dashboard')




def remove_from_favorite(request, item_type, item_id):
    user = request.user

    try:
        if item_type not in ['academy_product', 'coffee_delivery']:
            raise ValueError("Invalid item type")

        if item_type == 'academy_product':
            item = Academy_Product.objects.get(pk=item_id)
        else:
            item = Coffee_Delivery.objects.get(pk=item_id)

        favorite_item = FavoriteItem.objects.get(user=user, academy_product=item) if item_type == 'academy_product' else FavoriteItem.objects.get(user=user, coffee_delivery=item)
        
        favorite_item.delete()
        success_message = "Item removed from favorites successfully!"
    except (Academy_Product.DoesNotExist, Coffee_Delivery.DoesNotExist, FavoriteItem.DoesNotExist, ValueError):
        failure_message = "Failed to remove item from favorites." 
        return render(request, 'main/home.html', {'message': failure_message})

    return redirect('dashboard')





def get_favorite_count(user):
    favorite_count = FavoriteItem.objects.filter(user=user).count()
    print(favorite_count)

    return favorite_count



def check_discounts_and_notify_user(user):
    notifications = []
    processed_products = set()  
    
    academy_products_with_discount = Academy_Product.objects.filter(
        discount_price__isnull=False,
        discount_price__lt=F('price')
    )
    for product in academy_products_with_discount:
        if product not in processed_products:  
            notification_message = f"Academy Product '{product.name}' has a discount available."
            notifications.append(Notification(user=user, message=notification_message, academy_product=product))
            processed_products.add(product)  

    coffee_deliveries_with_discount = Coffee_Delivery.objects.filter(
        discount_price__isnull=False,
        discount_price__lt=F('price')
    )
    for delivery in coffee_deliveries_with_discount:
        if delivery not in processed_products:  
            notification_message = f"Coffee Delivery '{delivery.name}' has a discount available."
            notifications.append(Notification(user=user, message=notification_message, coffee_delivery=delivery))
            processed_products.add(delivery)  

    if notifications:
        Notification.objects.bulk_create(notifications)





def get_notification_count(user):
    notification_count = Notification.objects.filter(user=user).count()

    return notification_count





@login_required
def purchase_course(request, course_id):
    user_info = None
    course = get_object_or_404(Course, pk=course_id)

    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)
        
        if payment_form.is_valid():
            card_number = payment_form.cleaned_data['number']
            cvc = payment_form.cleaned_data['cvc']
            expiry = payment_form.cleaned_data['expiry']
            cardholder_name = payment_form.cleaned_data['name']
            
            
            user_info, created = UserInformation.objects.get_or_create(user=request.user)
            user_info.full_name = request.POST.get('full_name')
            user_info.city = request.POST.get('city')
            user_info.email = request.POST.get('email')
            user_info.phone_number = request.POST.get('phone_number')
            user_info.street = request.POST.get('street')
            user_info.district = request.POST.get('district')
            user_info.address = request.POST.get('address')
            user_info.save()

            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

            total_price = course.price
            return redirect('odeme', total_price=total_price)
    else:
        payment_form = PaymentForm()

    context = {
        'payment_form': payment_form,
        'course': course,
    }

    return render(request, 'purchase_course.html', context)








def choose_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            selected_product_type = form.cleaned_data['product_type']
    else:
        form = ProductForm()

    return render(request, 'main/choose_product.html', {'form': form})