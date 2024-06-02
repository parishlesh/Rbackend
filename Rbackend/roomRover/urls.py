from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path("signup", views.userRegister, name="signup"),
    path("login", views.userLogin, name="login"),
    path('rooms', views.get_all_rooms, name='get_all_rooms'),
    path('room/<int:room_id>', views.get_room_by_id, name='get_room_by_id'),
    path('createroom', views.create_room, name='create_room'),
] 