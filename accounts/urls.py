from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    path('', views.SignUpView.as_view(), name='signup'),
    #path('signup/', views.SignUpView.as_view(), name='signup'),
]
