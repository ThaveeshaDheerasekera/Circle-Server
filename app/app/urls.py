from django.urls import path
from . import views


# URL configuration of the store app
urlpatterns = [
    path('notes/<str:username>/', views.list_and_create_entry),
    # path('notes/<String:username>/<uuid:id>/', views.manipulate_entry_by_pk),
]
