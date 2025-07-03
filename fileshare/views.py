from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import FileUploadSerializer
from .models import SharedFile
from rest_framework.generics import ListAPIView
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.authentication import SessionAuthentication



from rest_framework.generics import CreateAPIView
from .serializers import ClientSignupSerializer
from django.contrib.auth import get_user_model

from django.http import FileResponse, Http404
from .utils import encrypt_file_id, decrypt_file_id
from django.shortcuts import get_object_or_404
import os

from .models import FileDownloadToken
from django.utils import timezone

import os
from django.http import FileResponse, Http404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import FileDownloadToken  # You must have this model defined
# from django.utils import timezone  # Uncomment if using expiration


from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator



User = get_user_model()

def test_view(request):
    return JsonResponse({"message": "Fileshare app is working!"})

class SecureVerifyEmailView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.email_verified = True
            user.save()
            return Response({'message': 'Email verified successfully!'}, status=200)
        else:
            return Response({'error': 'Invalid or expired token.'}, status=400)


class UUIDFileDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, token):
        user = request.user
        try:
            token_obj = FileDownloadToken.objects.get(token=token)
        except FileDownloadToken.DoesNotExist:
            raise Http404("Invalid or expired token.")

        if user != token_obj.created_by or user.role != 'CLIENT':
            return Response({'error': 'Unauthorized'}, status=403)

        # Increment download count
        shared_file = token_obj.file
        shared_file.download_count += 1
        shared_file.save()

        file_path = shared_file.file.path
        if not os.path.exists(file_path):
            raise Http404("File not found.")

        return FileResponse(open(file_path, 'rb'), as_attachment=True)



class UUIDDownloadLinkView(APIView):
    authentication_classes = [SessionAuthentication]  # ✅ Accepts session cookie
    permission_classes = [IsAuthenticated]

    def get(self, request, file_id):
        from .models import SharedFile, FileDownloadToken
        try:
            shared_file = SharedFile.objects.get(id=file_id)
        except SharedFile.DoesNotExist:
            return Response({'error': 'File not found'}, status=404)

        if request.user.role != 'CLIENT':
            return Response({'error': 'Unauthorized'}, status=403)

        token_obj = FileDownloadToken.objects.create(
            file=shared_file,
            created_by=request.user
        )

        download_url = f"/api/download-by-token/{token_obj.token}/"
        return Response({'url': download_url}, status=200)



class EncryptedDownloadLinkView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, file_id):
        user = request.user
        if user.role != 'CLIENT':
            return Response({'error': 'Only CLIENT users can generate download links.'}, status=403)

        encrypted = encrypt_file_id(file_id)
        download_url = request.build_absolute_uri(f'/api/download/{encrypted}/')
        return Response({'download_url': download_url})


class EncryptedFileDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, encrypted_id):
        user = request.user
        if user.role != 'CLIENT':
            return Response({'error': 'Access denied.'}, status=403)

        try:
            file_id = decrypt_file_id(encrypted_id)
        except Exception:
            raise Http404("Invalid download link.")

        file_obj = get_object_or_404(SharedFile, pk=file_id)
        file_path = file_obj.file.path

        if not os.path.exists(file_path):
            raise Http404("File not found.")

        return FileResponse(open(file_path, 'rb'), as_attachment=True)

class FileListView(ListAPIView):
    serializer_class = FileUploadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'CLIENT':
            return SharedFile.objects.all().order_by('-uploaded_at')
        return SharedFile.objects.none()  # OPS or unauthorized


class FileUploadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user

        # Check if user is OPS
        if user.role != 'OPS':
            return Response({"error": "Only OPS users can upload files."}, status=status.HTTP_403_FORBIDDEN)

        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            shared_file = serializer.save(uploaded_by=user)
            return Response({"message": "File uploaded successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientSignupView(APIView):
    def post(self, request):
        serializer = ClientSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Signup successful. Verification email sent."}, status=201)
        return Response(serializer.errors, status=400)


class VerifyEmailView(APIView):
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            user.email_verified = True
            user.save()
            return Response({"message": "Email verified successfully."}, status=200)
        except User.DoesNotExist:
            return Response({"error": "Invalid verification link."}, status=400)


class OpsLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is None or user.role != 'OPS':
            return Response({'error': 'Invalid credentials or not an OPS user.'}, status=401)

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

class OpsSignupView(APIView):
    def post(self, request):
        serializer = OpsSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'OPS user created successfully.'}, status=201)
        return Response(serializer.errors, status=400)

class OpsSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # Ensure this is set correctly
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role='OPS',
            email_verified=True  # Optional
        )
