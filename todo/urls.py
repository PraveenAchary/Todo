"""
URL configuration for todo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from .views import signup_view2,signup_view,login_view,home,addtask_view,edittask_view,logout_view,delete_view

urlpatterns = [
    path('',signup_view2,name='indexpage'),
    path('signup/',signup_view,name='register'),
    path('login/',login_view,name='login'),
    path('home/',home,name='home'),
    path('addtask/',addtask_view,name='addtask'),
    path('edittask/<int:taskid>/',edittask_view,name='edittask'),
    path('deletetask/<int:taskid>/',delete_view,name='deletetask'),
    path('logout/',logout_view,name='logout'),
    path('admin/', admin.site.urls),

    path('addtask/',addtask_view,name='addtask'),
    path('editask/',edittask_view,name='edittask'),
]
