"""betting URL Configuration

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

from django.urls import include, path
from . import views
from .views import ATPPlayerCreateView, ATPPlayerUpdateView, ATPPlayerDeleteView

app_name = 'players'

urlpatterns = [
    path('atp/', views.atp_player_list, name='player_list'),
    path('atp/create/', ATPPlayerCreateView.as_view(), name="player_create"),
    path('atp/edit/<int:pk>', ATPPlayerUpdateView.as_view(), name="player_edit"),
    path('atp/delete/<int:pk>', ATPPlayerDeleteView.as_view(), name="player_delete"),

    path('wta/', views.wta_player_list, name='wta_player_list')
]
