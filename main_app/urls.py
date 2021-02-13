from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('user_list/', CustomUserListView.as_view()),
    path('record_list/', RecordListView.as_view()),
    path('own_record_list/', OwnRecordListView.as_view()),
    path('add_record/', AddRecordView.as_view()),
    path('update_record/<int:pk>/', RecordDetailView.as_view()),
    path('hire/', HireStaffView.as_view()),
    path('fire/', FireStaffView.as_view()),
]
