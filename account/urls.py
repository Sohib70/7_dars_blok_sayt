from django.urls import path
from .views import *
# from .forms import SignUpForm, LoginForm

urlpatterns = [
    path('signup/',signup_view,name='signup'),
    path('login/',login_view,name='login'),
    path('logout/',logout_view,name='logout')
]

# from django.urls import path
# from .views import SignUpView, LoginView, LogoutView
#
# urlpatterns = [
#     path('signup/', SignUpView.as_view(), name='signup'),
#     path('login/', LoginView.as_view(), name='login'),
#
# ]