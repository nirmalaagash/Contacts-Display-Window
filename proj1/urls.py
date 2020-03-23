"""proj1 URL Configuration

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
from django.urls import path
from helloWorld.views import contactSearch, addContact, contactAdded, contactSearchData, indexNew, changeData, modifyData, modifiedData, deleteData

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', indexNew, name='index'),
    path('contactSearch/', contactSearch, name='contactSearch'),
    path('addContact/', addContact, name='addContact'),
    path('contactAdded/', contactAdded, name='contactAdded'),
    path('data/', contactSearchData, name='contactSearchData'),
    path('changeData/', changeData, name='changeData'),
    path('modifyData/', modifyData, name='modifyData'),
    path('modifiedData/', modifiedData, name="modifiedData"),
    path('deleteData/', deleteData, name="deleteData"),
]
