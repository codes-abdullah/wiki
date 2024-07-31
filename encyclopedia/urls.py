from django.urls import path

from . import views
app_name='wiki'
urlpatterns = [
    path("", views.index, name="index"),    
    path("wiki/<str:title>", views.goto_entry, name='entry'),
    path('create', views.create_entry, name='create')
    ,path('search', views.search, name='search')
    ,path('random_entry', views.random_entry, name='random_entry')
]


