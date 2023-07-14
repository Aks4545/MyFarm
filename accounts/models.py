from django.db import models

from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.



class UserManager(BaseUserManager):

     # Other fields specific to Moderator model

    def create_user(self,first_name,last_name,username,email,password=None):
        if not email:
            raise ValueError('user must have  email address')

        if not username:
            raise ValueError('user must have  an username')
        

        user = self.model(
            email= self.normalize_email(email),
            username= username,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,first_name,last_name,username,email,password=None):
        user = self.create_user (
            email= self.normalize_email(email),
            username= username,
            first_name=first_name,
            last_name=last_name,
        )

        user.is_admin= True
        user.is_active=True
        user.is_staff=True
        user.is_superadmin=True
        user.save(using =self._db)
        return user





class User(AbstractBaseUser):
    FARMER = 1
    CUSTOMER = 2

    ROLE_CHOICE = (
        (FARMER,'farmer'),
        (CUSTOMER,'customer')
    )

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_no =models.CharField(max_length=100,unique=True)
    username=  models.CharField(max_length=150)
    pin_code =models.CharField(max_length=150,)
    email = models.EmailField(max_length=150,unique=True)
    password = models.CharField(max_length=128)
    user_image =models.ImageField(upload_to="userProfile") 
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE,blank=True,null=True)
    #required 

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    Is_admin= models.BooleanField(default=False)
    Is_active= models.BooleanField(default=False)
    Is_staff = models.BooleanField(default=False)
    Is_superadmin= models.BooleanField(default=False)

    USERNAME_FIELD ='email'
    REQUIRED_FIELDS=['username','first_name','last_name','pin_code','phone_no']

    objects = UserManager()

    def __str__(self): 
        return self.email
    
    def has_perm(self,perm,obj=None):
        return self.Is_admin
    

    def has_module_perms(self,obj=None):
        return True

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