from django.contrib import admin
from django.urls import path
from hospital import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # ADMIN
    path('admin/', admin.site.urls),

    # LOGIN (default page)
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

    # LOGOUT
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    # MAIN PAGE (INDEX - NOT HOME)
    path('index/', views.home, name='index'),

    # DASHBOARD
    path('dashboard/', views.dashboard, name='dashboard'),

    # REGISTER PATIENT
    path('register/', views.register_patient, name='register'),

    # APPOINTMENT
    path('appointment/', views.book_appointment, name='appointment'),
    path('cancel/<int:id>/', views.cancel_appointment, name='cancel'),

    # DOCTOR DETAIL
    path('doctor/<int:id>/', views.doctor_detail, name='doctor_detail'),
]