"""
URL configuration for sistema_tienda project.

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
# sistema_tienda/urls.py
from django.contrib import admin # Importa el módulo de administración de Django.
from django.urls import path, include # Importa path y include.

urlpatterns = [
    path('admin/', admin.site.urls), # Mapea la URL '/admin/' al panel de administración de Django.
    path('', include('tienda.urls')), # <-- Incluye todas las URLs definidas en 'tienda/urls.py' bajo la ruta raíz ('/').
]