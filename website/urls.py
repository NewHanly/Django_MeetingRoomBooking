"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from meeting import views as meeting_view

urlpatterns = [
    path('', meeting_view.index),
    #path('admin/', admin.site.urls),
    path('<int:mtno>/', meeting_view.meetingList),
    path('add/', meeting_view.addmeeting),
    path('addroom/', meeting_view.addroom),
    path('callback/', meeting_view.addcallback),
    path('delcallback/',meeting_view.delcallback)
]
