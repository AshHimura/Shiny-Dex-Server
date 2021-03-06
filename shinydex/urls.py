"""shinydex URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf.urls import include
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from shinydexapi.views import register_user, login_user
from shinydexapi.views import PokemonView, RegionView, ItemView, PokeTypeView, PostView, DexUserView, CaughtView

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'pokemon', PokemonView, 'pokemon')
router.register(r'regions', RegionView, 'region')
router.register(r'items', ItemView, 'item')
router.register(r'socials', PostView, 'social')
router.register(r'caught', CaughtView, 'caught')
router.register(r'users', DexUserView, 'user')
router.register(r'poketypes', PokeTypeView, 'poketype')


urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
