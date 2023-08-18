from datetime import date, datetime, time
from django.db import models
from django.shortcuts import get_object_or_404
from accounts.models import User,UserProfile
from accounts.utils import send_notification

# Create your models here.

class seller(models.Model):
    user = models.OneToOneField(User,related_name= 'user',on_delete=models.CASCADE) 
    user_profile= models.OneToOneField(UserProfile,related_name='userprofile',on_delete=models.CASCADE)
    seller_name = models.CharField(max_length=100)
    seller_slug = models.SlugField(max_length=100, unique=True)
    is_approved = models.BooleanField(default=False)
    created_at= models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.seller_name
    
    def save(self,*args,**kwargs):
        if self.pk is not None:
            #update
            orig = get_object_or_404(seller,pk=self.pk)

            if orig.is_approved != self.is_approved:
                mail_template = "accounts/emails/admin_approval_email.html"
                context ={
                    'user':self.user,
                    'is_approved': self.is_approved,
                    'to_email': self.user.email,
                }
                if self.is_approved == True:
                    #send mail
                    mail_subject= "congartulations!! Your Farm has been approved."
                
                    send_notification(mail_subject,mail_template, context)
                else:
                    #send mail
                    mail_subject= "Sorry!!!!!!!! You are not eligible."
                   
                    send_notification(mail_subject,mail_template, context)
        return super(seller,self).save(*args,**kwargs)
    
    def is_open(self):
        # Check current day's opening hours.
        today_date = date.today()
        today = today_date.isoweekday()
        
        current_opening_hours = OpeningHour.objects.filter(vendor=self, day=today)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        is_open = None
        for i in current_opening_hours:
            if not i.is_closed:
                start = str(datetime.strptime(i.from_hour, "%I:%M %p").time())
                end = str(datetime.strptime(i.to_hour, "%I:%M %p").time())
                if current_time > start and current_time < end:
                    is_open = True
                    break
                else:
                    is_open = False
        return is_open
    





    
DAYS = [
    (1, ("Monday")),
    (2, ("Tuesday")),
    (3, ("Wednesday")),
    (4, ("Thursday")),
    (5, ("Friday")),
    (6, ("Saturday")),
    (7, ("Sunday")),
]

HOUR_OF_DAY_24 = [(time(h, m).strftime('%I:%M %p'), time(h, m).strftime('%I:%M %p')) for h in range(0, 24) for m in (0, 30)]
class OpeningHour(models.Model):
    vendor = models.ForeignKey(seller, on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAYS)
    from_hour = models.CharField(choices=HOUR_OF_DAY_24, max_length=10, blank=True)
    to_hour = models.CharField(choices=HOUR_OF_DAY_24, max_length=10, blank=True)
    is_closed = models.BooleanField(default=False)

    class Meta:
        ordering = ('day', '-from_hour')
        unique_together = ('vendor', 'day', 'from_hour', 'to_hour')
    def __str__(self):
        return self.get_day_display()
    


    