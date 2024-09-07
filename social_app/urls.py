from django.urls import path
from .views import SendFriendRequestView, AcceptFriendRequestView, RejectFriendRequestView, ListFriendsView, ListPendingFriendRequestsView

urlpatterns = [
    path('friend-request/send/<int:user_id>/',
         SendFriendRequestView.as_view(), name='send-friend-request'),
    path('friend-request/accept/<int:user_id>/',
         AcceptFriendRequestView.as_view(), name='accept-friend-request'),
    path('friend-request/reject/<int:user_id>/',
         RejectFriendRequestView.as_view(), name='reject-friend-request'),
    path('friends/', ListFriendsView.as_view(), name='list-friends'),
    path('friend-requests/pending/',
         ListPendingFriendRequestsView.as_view(), name='list-pending-requests'),
]
