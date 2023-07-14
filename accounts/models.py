from django.db import models

from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.



# class accounts(BaseUserManager):



#     # Other fields specific to Moderator model

#     def __str__(self):
#         return self.username

# class User(AbstractBaseUser):
#     first_name = models.CharField(max_length=150)
#     last_name = models.CharField(max_length=150)
#     email = models.EmailField()
#     username =models.CharField(max_length=100,unique=True)
#     password = models.CharField(max_length=128)
#     phone_no =models.CharField(max_length=100,unique=True)
#     pin_code =models.CharField(max_length=150,)
#     user_image =models.ImageField(upload_to="userProfile") 
#     address=models.CharField(max_length=300)

#     #required 

#     date_joined = models.DateTimeField(auto_now_add=True)
#     last_login = models.DateTimeField(auto_now_add=True)
#     Is_admin= models.BooleanField(default=False)
#     Is_active= models.BooleanField(default=False)
#     Is_staff = models.BooleanField(default=False)
#     Is_superadmin= models.BooleanField(default=False)

#     USERNAME_FIELD ='email'
#     REQUIRED_FIELDS=['username','first_name','last_name','pin_code','address','phone_no']


#     def __str__(self):
#         return self.email
    
#     def __str__(self):
#         return self.Is_admin
    
#     def has_module_perms(self,obj=None):
#         return True

# class Seller(AbstractBaseUser):
#     first_name = models.CharField(max_length=150)
#     last_name = models.CharField(max_length=150)
#     email = models.EmailField()
#     username =models.CharField(max_length=100,unique=True)
#     password = models.CharField(max_length=128)
#     phone_no =models.CharField(max_length=100,unique=True)
#     location =models.CharField(max_length=150)
#     user_image =models.ImageField(upload_to="workerProfile") 
#     dob =models.DateField(null=True)
#     user_bio=models.CharField(max_length=150)
#     type=models.CharField(max_length=100,default='worker') 
#     address=models.CharField(max_length=300)
    
#     is_approved=models.BooleanField(null= True)
#     status=models.BooleanField(null= True)
#     report=models.BooleanField(null= True)

#     def __str__(self):
#         return self.username

# class login(models.Model):
#     username =models.CharField(max_length=100)
#     password = models.CharField(max_length=128)
#     type=models.CharField(max_length=100)

#     def __str__(self):
#         return self.username