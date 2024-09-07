from django.urls import path
from .views import UserSignupView, UserLoginView, UserSearchView

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('search/', UserSearchView.as_view(), name='user-search'),
]


# from django.urls import path
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )
# from .views import UserSignupView

# urlpatterns = [
#     path('signup/', UserSignupView.as_view(), name='signup'),
#     path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
# ]
