from django.urls import path
from . import views

from .views import (
    test_view,
    ClientSignupView,
    SecureVerifyEmailView,
    OpsSignupView,
    OpsLoginView,
    FileUploadView,
    FileListView,
    EncryptedDownloadLinkView,
    EncryptedFileDownloadView,
    UUIDDownloadLinkView,
    UUIDFileDownloadView,
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

urlpatterns = [
    # Test route
    path('test/', test_view, name='test_view'),

    # Client signup and email verification
    path('signup/', ClientSignupView.as_view(), name='client-signup'),
    path('verify-email/<uidb64>/<token>/', SecureVerifyEmailView.as_view(), name='verify-email'),

    # JWT login for clients
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # OPS user signup/login
    path('signup-ops/', OpsSignupView.as_view(), name='signup-ops'),
    path('login-ops/', OpsLoginView.as_view(), name='login-ops'),

    # File upload and listing
    path('upload/', FileUploadView.as_view(), name='upload-file'),
    path('files/', FileListView.as_view(), name='file-list'),

    # Encrypted download
    path('get-download-link/<int:file_id>/', EncryptedDownloadLinkView.as_view(), name='get-download-link'),
    path('download/<str:encrypted_id>/', EncryptedFileDownloadView.as_view(), name='download-file'),

    # UUID download
    path('get-uuid-download-link/<int:file_id>/', UUIDDownloadLinkView.as_view(), name='get-uuid-download-link'),
    path('download-by-token/<uuid:token>/', UUIDFileDownloadView.as_view(), name='uuid-file-download'),
]
