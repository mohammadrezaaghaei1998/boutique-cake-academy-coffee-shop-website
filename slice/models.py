from django.db import models
from django.contrib.auth.models import User



class UserInformation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=17, blank=False)
    order_datetime = models.DateTimeField(null=True, blank=False)
    email = models.EmailField(default='default@example.com', null=True, blank=False)
    full_name = models.CharField(max_length=30,default=' ', blank=False)
    city = models.CharField(max_length=255,  blank=False)
    street = models.CharField(max_length=255, blank=False)
    district = models.CharField(max_length=255,  blank=False) 
    address = models.CharField(max_length=255, blank=False)
    
    


    def __str__(self):
        return self.user.username 
    

class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    submission_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
    


class SecondContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submission_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Second Contact Submission - {self.name}'
    
    


class Course(models.Model):
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    price = models.FloatField(max_length=50)
    hour = models.PositiveIntegerField()
    image = models.ImageField(upload_to='course_images/',default=None)
    timestamp = models.DateTimeField(auto_now_add=True)
    duration_minutes = models.PositiveIntegerField()
    start_date = models.DateField()
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)



class UserCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    userinformation = models.ForeignKey(UserInformation,on_delete=models.CASCADE,null=True,blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,default=None)





class Coffee_Delivery(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    gram = models.IntegerField()
    image = models.ImageField(upload_to='coffee_delivery_images/',default=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


    def has_discount(self):
        return self.discount_price is not None and self.discount_price < self.price


class User_Coffee_Delivery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coffee_delivery = models.ForeignKey(Coffee_Delivery,on_delete=models.CASCADE,default=None)





class Academy_Product(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    gram = models.IntegerField()
    adult = models.BooleanField(default=True)
    image = models.ImageField(upload_to='academy_product_images/',default=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


    def has_discount(self):
        return self.discount_price is not None and self.discount_price < self.price


class User_Academy_Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    academy_products = models.ForeignKey(Academy_Product,on_delete=models.CASCADE,default=None)





class MyCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    items = models.ManyToManyField('CartItem')


    @property
    def total_price(self):
        return sum(cart_item.total_price for cart_item in self.items.all())

    def add(self, cartitem, quantity=1):
        cart_item, created = CartItem.objects.get_or_create(
            cart=self,
            academy_product=cartitem.academy_product,  
            coffee_delivery=cartitem.coffee_delivery,  
        )

        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity

        cart_item.save()

        return cart_item, created


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    cart = models.ForeignKey(MyCart, on_delete=models.CASCADE,blank=True, null=True)
    academy_product = models.ForeignKey(Academy_Product, on_delete=models.CASCADE, null=True, blank=True)
    coffee_delivery = models.ForeignKey(Coffee_Delivery, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    userinformation = models.ForeignKey(UserInformation,on_delete=models.CASCADE,null=True,blank=True)

    
    # def get_total_item_price(self):
    #     if self.academy_product:
    #         return self.quantity * self.academy_product.price
    #     elif self.coffee_delivery:
    #         return self.quantity * self.coffee_delivery.price
    #     else:
    #         return 0
        


    def get_total_item_price(self):
        if self.academy_product:
            if self.academy_product.discount_price is not None:
                return self.quantity * self.academy_product.discount_price
            else:
                return self.quantity * self.academy_product.price
        elif self.coffee_delivery:
            if self.coffee_delivery.discount_price is not None:
                return self.quantity * self.coffee_delivery.discount_price
            else:
                return self.quantity * self.coffee_delivery.price
        else:
            return 0


    def get_total_item_quantity(self):
        return self.quantity


    def save(self, *args, **kwargs):
        self.total_price = self.get_total_item_price()
        super(CartItem, self).save(*args, **kwargs)






class FavoriteItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    academy_product = models.ForeignKey(Academy_Product, on_delete=models.CASCADE, null=True, blank=True)
    coffee_delivery = models.ForeignKey(Coffee_Delivery, on_delete=models.CASCADE, null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Favorite Item ({self.user.username})'
    




class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    academy_product = models.ForeignKey(Academy_Product, on_delete=models.CASCADE, null=True, blank=True)
    coffee_delivery = models.ForeignKey(Coffee_Delivery, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.message
    






class PaymentConfirmation(models.Model):
    user = models.ForeignKey(UserInformation, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    reference_code = models.CharField(max_length=8, unique=True)





class Product(models.Model):
    PRODUCT_TYPES = (
        ('chocolate', 'Chocolate'),
        ('cream', 'Cream'),
        ('pancake', 'Pancake'),
    )
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=PRODUCT_TYPES)

    def __str__(self):
        return self.name