from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),

    path('patient/<int:user_id>/', views.patient_dashboard, name='patient_dashboard'),
    path('doctor/<int:user_id>/', views.doctor_dashboard, name='doctor_dashboard'),

    path("create_blog/", views.create_blog, name="create_blog"),
    path("my_posts/", views.my_posts, name="my_posts"),

    path("blogs/", views.view_blogs, name="view_blogs"),
    path("blog/<int:post_id>/", views.full_blog, name="full_blog"),




]
