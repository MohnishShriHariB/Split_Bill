"""
URL configuration for split_bill project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from sbill import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup',views.signupuser,name='signupuser'),
    path('logout',views.logoutuser,name='logoutuser'),
    path('current',views.currentpage,name='currentpage'),
    path('',views.home,name='home'),
    path('login',views.loginuser,name='loginuser'),
    path('trip/',views.addtrip,name='addtrip'),
    path('trips/<int:task_pk>',views.trippage,name='trippage'),
    path('task/<int:task_pk>',views.addtask,name='addtask'),
    path('friend/<int:task_pk>',views.addfriend,name='addfriend'),
    path('uptask/<int:trip_pk>/<int:task_pk>',views.updatetask,name='updatetask'),
    path('completed/<int:trip_pk>',views.completed,name='completed'),
]
