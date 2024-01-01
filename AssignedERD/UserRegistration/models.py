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

class BookOrder(models.Model):
    VERIFICATION = (
        (0, 'Pending'),
        (1, 'Approved'),
        (2, 'Declined'),
    )

    book_id = models.BigAutoField(primary_key=True)
    destination_id = models.ForeignKey(Destination, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(choices=VERIFICATION, default=0)

    def __str__(self):
        return str(self.book_id)

class Wishlist(models.Model):
    wishlist_id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    destination_id = models.ForeignKey(Destination, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.wishlist_id)
