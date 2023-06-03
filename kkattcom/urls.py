"""
URL configuration for kkattcom project.

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
from django.conf import settings
from django.urls import path, re_path, include
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    #path('dashboard/', views.dashboard),
    #path('about/', views.about),
    #path('kkattdrop/', views.kkattdrop, name='kkattdrop'),
    #path('app/', views.app),
    #path('app/<int:appno>', views.app),
    path('studywkkattmos/', views.swkm),
    path('studygram/', views.stdgindex, name='stdgindex'),
    path('studygram/theme', views.themelist, name='theme'),
    path('studygram/sheet/error', views.sheeterror, name='sheeterror'),
    path('studygram/giveaway/', views.stdggiveaway, name="stdggiveaway1"),
    path('studygram/resetgiveaway', views.resetgiveaway),
    path('account/', views.accountedit, name='editaccount'),
    path('account/login/', views.login, name='login'),
    path('account/logout/', views.logout, name='logout'),
    path('account/create/', views.accountcreate, name='createaccount'),
    path('account/changepassword', views.changepassword, name='changepassword')
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)