from django.urls import path
from . import views
app_name = 'user'

urlpatterns = [
    path('users/', views.user_list, name='user_list'),
    path('users/<int:pk>/', views.user_detail, name='user_detail'),
    path('users/create/', views.user_add, name='user_add'),
    path('users/edit/<int:pk>/', views.user_edit, name='user_edit'),
    path('import/', views.import_users, name='import_users'),
    path('export/', views.export_users, name='export_users'),
    path('user/<int:user_id>/assign-programs/', views.assign_training_programs, name='assign_training_programs'),
]
