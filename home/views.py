from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

from fileshare.forms import FileUploadForm
from fileshare.models import SharedFile
from django.core.paginator import Paginator



User = get_user_model()

def logout_view(request):
    logout(request)
    return redirect('home')


def home_page(request):
    return render(request, 'home.html')

def client_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'client_register.html', {'error': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return render(request, 'client_register.html', {'error': 'Username already taken'})

        if User.objects.filter(email=email).exists():
            return render(request, 'client_register.html', {'error': 'Email already registered'})

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role='CLIENT',
            email_verified=False
        )

        # Create verification link
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        verify_url = f"http://localhost:8000/api/verify-email/{uid}/{token}/"

        # Render email template as HTML
        context = {
            'username': username,
            'verification_url': verify_url,
        }
        html_message = render_to_string('email_verification.html', context)

        # Send HTML email
        send_mail(
            subject='Verify Your Email',
            message='',
            from_email='noreply@example.com',
            recipient_list=[email],
            html_message=html_message,
            fail_silently=False
        )

        return render(request, 'client_register.html', {'message': 'Registration successful! Check your email to verify.'})

    return render(request, 'client_register.html')

def ops_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'ops_register.html', {'error': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return render(request, 'ops_register.html', {'error': 'Username already exists'})

        if User.objects.filter(email=email).exists():
            return render(request, 'ops_register.html', {'error': 'Email already registered'})

        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            role='OPS',
            email_verified=False  # Not verified yet
        )

        # ✅ Email Verification Logic for OPS
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        verify_url = f"http://localhost:8000/api/verify-email/{uid}/{token}/"

        context = {
            'username': user.username,
            'verification_url': verify_url,
        }

        html_message = render_to_string('email_verification.html', context)

        send_mail(
            subject='Verify Your Email (OPS)',
            message='',
            from_email='noreply@example.com',  # Replace with settings.DEFAULT_FROM_EMAIL or env
            recipient_list=[user.email],
            html_message=html_message,
        )

        return render(request, 'ops_register.html', {'message': 'Verification email sent! Please check your inbox.'})

    return render(request, 'ops_register.html')

# ✅ Client Login View
def client_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user and user.role == 'CLIENT':
            if user.email_verified:
                login(request, user)
                return redirect('dashboard')
            else:
                return render(request, 'client_login.html', {'error': 'Email not verified'})
        else:
            return render(request, 'client_login.html', {'error': 'Invalid credentials or role'})

    return render(request, 'client_login.html')


# ✅ OPS Login View
def ops_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user and user.role == 'OPS':
            if user.email_verified:
                login(request, user)
                return redirect('dashboard')
            else:
                return render(request, 'ops_login.html', {'error': 'Email not verified'})
        else:
            return render(request, 'ops_login.html', {'error': 'Invalid credentials or role'})

    return render(request, 'ops_login.html')


# ✅ Dashboard View
@login_required(login_url='home')
def dashboard(request):
    if request.user.role == 'CLIENT':
        files = SharedFile.objects.all().order_by('-uploaded_at')  # Or filter by conditions later
        paginator = Paginator(files, 5)  # Show 5 files per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'client_dashboard.html', {'files': page_obj})

    elif request.user.role == 'OPS':
        return render(request, 'ops_dashboard.html')

    else:
        return redirect('home')
    


@login_required(login_url='home')
def ops_upload_form(request):
    if request.user.role != 'OPS':
        return redirect('dashboard')

    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.uploaded_by = request.user
            uploaded_file.save()
            return redirect('dashboard')
    else:
        form = FileUploadForm()

    return render(request, 'ops_upload_form.html', {'form': form})

@login_required(login_url='home')
def resend_verification_email(request):
    user = request.user
    if user.email_verified:
        messages.info(request, 'Your email is already verified.')
        return redirect('dashboard')

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    verify_url = f"http://localhost:8000/api/verify-email/{uid}/{token}/"

    context = {
        'username': user.username,
        'verification_url': verify_url,
    }

    html_message = render_to_string('email_verification.html', context)

    send_mail(
        subject='Resend Email Verification',
        message='',
        from_email='noreply@example.com',
        recipient_list=[user.email],
        html_message=html_message,
    )

    messages.success(request, 'Verification email has been sent again.')
    return redirect('dashboard')
