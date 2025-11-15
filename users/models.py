from django.db import models

class CustomUser(models.Model):
    USER_TYPE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)

    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)

    password = models.CharField(max_length=255)

    # Address fields
    address_line1 = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.username} ({self.user_type})"
