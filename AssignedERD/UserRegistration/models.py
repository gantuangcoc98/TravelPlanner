from django.db import models

# Create your models here.
class Destination(models.Model):
    destination_id = models.BigAutoField(primary_key=True)
    destination_name = models.CharField(max_length=50)
    description = models.TextField()
    location = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/', default='load_img.png')

    def __str__(self):
        return self.destination_name
    
class User(models.Model):
    USER_TYPE_CHOICES = (
        (0, 'User'),
        (1, 'Admin'),
    )

    user_id = models.BigAutoField(primary_key=True)
    usertype = models.IntegerField(choices=USER_TYPE_CHOICES, default=0)
    username = models.CharField(max_length=20, unique=True)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    contact_number = models.CharField(max_length=15)
    wishlist = models.ManyToManyField(Destination, blank=True)

    def __str__(self):
        return self.username

    def check_password(self, password):
        if self.password == password:
            return True
        else:
            return False
        
    def check_admin(self, usertype):
        if self.usertype == 1 and self.usertype == usertype:
            return True
        else:
            return False
        