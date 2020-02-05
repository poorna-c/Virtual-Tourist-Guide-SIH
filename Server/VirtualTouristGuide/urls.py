"""VirtualTouristGuide URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from main import views as main_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('main.urls')),
    path('register/',main_views.register,name = 'register_page'),
    path('accounts/login/',main_views.login_, name='login_page'),
    path('logout/',auth_views.LogoutView.as_view(template_name='main/logout.html'),name = 'logout'),
    path('delete/<int:id>',main_views.delete_comment,name="delete_comment_page"),
    path('comment',main_views.add_comment,name="add_comment_page"),
    path('checkins',main_views.checkins,name="checkins_page"),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
