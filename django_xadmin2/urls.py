"""django_xadmin2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
import xadmin
from django.urls import path,include
#引用通用模板
from django.views import generic
from apps.users.views import LoginView,RegisterView #基于类的url

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('',generic.TemplateView.as_view(template_name='index.html'),name='index'),
    path('login/',LoginView.as_view(),name='login'),#用户登录路由
    path('register/',RegisterView.as_view(),name='register'),
    path('captcha/',include('captcha.urls')),
]
