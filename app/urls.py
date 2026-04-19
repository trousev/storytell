from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("inference/", views.InferenceView.as_view(), name="inference"),
    path("inference/status/", views.JobStatusView.as_view(), name="job_status"),
]
