from rest_framework import serializers
from .models import SharedFile
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.urls import reverse

from rest_framework import serializers
from .models import SharedFile

class FileListSerializer(serializers.ModelSerializer):
    filename = serializers.SerializerMethodField()
    uploaded_by = serializers.SerializerMethodField()

    class Meta:
        model = SharedFile
        fields = ['id', 'filename', 'uploaded_by']

    def get_filename(self, obj):
        return obj.file.name.split('/')[-1]

    def get_uploaded_by(self, obj):
        return obj.uploaded_by.username


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedFile
        fields = ['file']

    def validate_file(self, value):
        # Ensure the uploaded file ends with a valid extension
        if not value.name.endswith(('.pptx', '.docx', '.xlsx')):
            raise serializers.ValidationError("Only .pptx, .docx, .xlsx files allowed")
        return value
    
class FileUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.role != 'OPS':
            return Response({'error': 'Only OPS users can upload files.'}, status=403)

        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(uploaded_by=user)
            return Response({'message': 'File uploaded successfully.'}, status=201)
        return Response(serializer.errors, status=400)
    

User = get_user_model()

class ClientSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role='CLIENT',
            email_verified=False
        )

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        verify_link = f"http://localhost:8000/api/verify-email/{uid}/{token}/"
        
        send_mail(
            subject="Verify Your Email",
            message=f"Click the link to verify your email: {verify_link}",
            from_email="noreply@example.com",
            recipient_list=[user.email],
            fail_silently=False,
        )

        return user

class OpsSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role='OPS',
            email_verified=False  # Optional: OPS doesn't need verification
        )
