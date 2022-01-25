from memo import views
from django.urls import path

urlpatterns=[
    path('',views.home),
    path('insert_memo', views.insert_memo),
    path('detail',views.detail),
    path('update_memo',views.update_memo),
    path('delete_memo',views.delete_memo),
]