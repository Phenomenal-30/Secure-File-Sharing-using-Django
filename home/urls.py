from django.urls import path
from .views import (
    home_page, 
    client_register, 
    ops_register,
    client_login,
    ops_login,
    dashboard,
    logout_view,
    ops_upload_form,
    resend_verification_email
)

urlpatterns = [
    path('', home_page, name='home'),  # Homepage
    path('client-register/', client_register, name='client-register'),  # Client registration form
    path('ops-register/', ops_register, name='ops-register'),  # OPS registration form
    path('client-login/', client_login, name='client-login'),  # Client login
    path('ops-login/', ops_login, name='ops-login'),  # OPS login
    path('dashboard/', dashboard, name='dashboard'),  # Common dashboard
    path('logout/', logout_view, name='logout'),
    path('upload-form/', ops_upload_form, name='upload-form'),
    path('resend-verification/', resend_verification_email, name='resend-verification'),
]
