from django.shortcuts import render, redirect
from .models import CustomUser
from django.contrib import messages
from django.http import HttpResponse
from .models import BlogPost, Category, CustomUser

def signup(request):
    if request.method == "POST":

        user_type = request.POST.get("user_type")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")

        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        address_line1 = request.POST.get("address_line1")
        city = request.POST.get("city")
        state = request.POST.get("state")
        pincode = request.POST.get("pincode")

        profile_picture = request.FILES.get("profile_picture")

        # 1️⃣ Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, "users/signup.html")

        # 2️⃣ Check if username already exists
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return render(request, "users/signup.html")

        # 3️⃣ Check if email already exists
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return render(request, "users/signup.html")

        # 4️⃣ Save data to database
        user = CustomUser(
            user_type=user_type,
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password,
            address_line1=address_line1,
            city=city,
            state=state,
            pincode=pincode
        )

        # Save image separately
        if profile_picture:
            user.profile_picture = profile_picture

        user.save()

        messages.success(request, "Signup successful! Please login.")
        return redirect("login")  # We will create login later

    return render(request, "users/signup.html")

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = CustomUser.objects.get(username=username, password=password)
        except CustomUser.DoesNotExist:
            messages.error(request, "Invalid username or password!")
            return render(request, "users/login.html")

        #  Save session data
        request.session["user_id"] = user.id
        request.session["username"] = user.username
        request.session["user_type"] = user.user_type   # <-- IMPORTANT

        # Redirect to respective dashboard
        if user.user_type == "patient":
            return redirect("patient_dashboard", user_id=user.id)
        else:
            return redirect("doctor_dashboard", user_id=user.id)

    return render(request, "users/login.html")


def patient_dashboard(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    return render(request, "users/patient_dashboard.html", {"user": user})


def doctor_dashboard(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    return render(request, "users/doctor_dashboard.html", {"user": user})



def create_blog(request):
    # Ensure only doctors can access
    if request.session.get("user_type").lower() != "doctor":

        return HttpResponse("Access Denied: Only doctors can upload blogs.")

    categories = Category.objects.all()

    if request.method == "POST":
        title = request.POST.get("title")
        category_id = request.POST.get("category")
        summary = request.POST.get("summary")
        content = request.POST.get("content")
        is_draft = True if request.POST.get("is_draft") == "on" else False
        image = request.FILES.get("image")

        user_id = request.session.get("user_id")
        user = CustomUser.objects.get(id=user_id)

        category_id = request.POST.get("category")
        category = Category.objects.get(id=category_id)


        # Save blog
        blog = BlogPost(
            title=title,
            category=category,
            summary=summary,
            content=content,
            author=user,
            is_draft=is_draft
        )

        if image:
            blog.image = image
        
        blog.save()

        return HttpResponse("Blog uploaded successfully!")
    
    categories = Category.objects.all()
    return render(request, "users/create_blog.html", {"categories": categories})


def my_posts(request):
    # Ensure only doctors can access
    if request.session.get("user_type") != "doctor":
        return HttpResponse("Access Denied: Only doctors can view their posts.")

    user_id = request.session.get("user_id")
    posts = BlogPost.objects.filter(author_id=user_id)

    return render(request, "users/my_posts.html", {"posts": posts})

def view_blogs(request):
    # Only visible to patients
    if request.session.get("user_type", "").lower() != "patient":
        return HttpResponse("Access Denied: Only patients can view blogs.")

    categories = Category.objects.all()

    # Fetch only published posts (not drafts)
    posts = BlogPost.objects.filter(is_draft=False)

    return render(request, "users/view_blogs.html", {
        "categories": categories,
        "posts": posts
    })


def full_blog(request, post_id):

    # Allow both doctor and patient, just require login
    if request.session.get("user_type") is None:
        return HttpResponse("Please login to read blogs.")

    try:
        post = BlogPost.objects.get(id=post_id)
    except BlogPost.DoesNotExist:
        return HttpResponse("Blog not found.")

    # Prevent patients from reading drafts
    if post.is_draft and request.session.get("user_type") != "doctor":
        return HttpResponse("This post is not published yet.")

    return render(request, "users/full_blog.html", {"post": post})

