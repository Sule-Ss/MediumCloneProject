from django.urls import path, include
from .views import RegisterView,UserView,AboutYouUpdateView


urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path("register/", RegisterView.as_view()),
    path("users/", UserView.as_view()),
    path("users/<uuid:pk>", AboutYouUpdateView.as_view()),
    
]