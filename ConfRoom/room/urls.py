from django.urls import path

from . import views

urlpatterns = [
    # For Admin(Read, Update)
    # Employee(Read Only)
    path('', views.RoomView.as_view()),
    path('<int:room_id>/', views.RoomDetailView.as_view()),
    path('<int:room_id>/slots/', views.RoomSlotView.as_view()),
    path('<int:room_id>/slots/<int:slot_id>/', views.RoomSlotDetailView.as_view()),
    path('<int:room_id>/slots/<int:slot_id>/book/', views.RoomSlotBookView.as_view()),
    path('<int:room_id>/slots/<int:slot_id>/cancel/', views.RoomSlotCancelView.as_view())
]
