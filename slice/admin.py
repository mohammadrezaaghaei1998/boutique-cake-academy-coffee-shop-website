from django.contrib import admin
from .models import (UserInformation,ContactSubmission,SecondContactSubmission,Course,
                     UserCourse,Academy_Product,Coffee_Delivery,
                     User_Coffee_Delivery,User_Academy_Product,MyCart,
                     CartItem,FavoriteItem,
                     PaymentConfirmation,Product)
# Register your models here.


admin.site.register(UserInformation)
admin.site.register(ContactSubmission)
admin.site.register(SecondContactSubmission)
admin.site.register(Course)
admin.site.register(UserCourse)
admin.site.register(Academy_Product)
admin.site.register(User_Academy_Product)
admin.site.register(Coffee_Delivery)
admin.site.register(User_Coffee_Delivery)
admin.site.register(MyCart)
admin.site.register(CartItem)
admin.site.register(FavoriteItem)
admin.site.register(PaymentConfirmation)
admin.site.register(Product)










