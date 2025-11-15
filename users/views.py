from django.shortcuts import render, redirect
from .models import CustomUser
from django.contrib import messages

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

        # Check if user exists
        try:
            user = CustomUser.objects.get(username=username, password=password)
        except CustomUser.DoesNotExist:
            messages.error(request, "Invalid username or password!")
            return render(request, "users/login.html")

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

