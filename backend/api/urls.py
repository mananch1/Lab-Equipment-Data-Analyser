from django.urls import path
from .views import UploadFileView, HistoryView

urlpatterns = [
    path('upload/', UploadFileView.as_view(), name='upload'),
    path('history/', HistoryView.as_view(), name='history'),
]
