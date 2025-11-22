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


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    summary = models.TextField()
    content = models.TextField()
    is_draft = models.BooleanField(default=False)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    # Helper method to return truncated summary
    def short_summary(self):
        words = self.summary.split()
        if len(words) > 15:
            return " ".join(words[:15]) + "..."
        return self.summary
