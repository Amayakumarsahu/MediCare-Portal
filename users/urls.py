from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),

    path('patient/<int:user_id>/', views.patient_dashboard, name='patient_dashboard'),
    path('doctor/<int:user_id>/', views.doctor_dashboard, name='doctor_dashboard'),

]
