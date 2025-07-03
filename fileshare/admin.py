from django.contrib import admin
from .models import CustomUser, SharedFile, FileDownloadToken  # adjust import if needed

admin.site.register(CustomUser)
admin.site.register(SharedFile)
admin.site.register(FileDownloadToken)
