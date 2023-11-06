from Book import views
from django.urls import path

urlpatterns=[
    path('',views.bookApi),
    path('/<int:id>',views.bookApi),   
]