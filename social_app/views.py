from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from accounts.models import CustomUser, FriendRequest
from .serializers import UserSerializer


class SendFriendRequestView(APIView):

    def post(self, request, user_id):
        try:
            receiver = CustomUser.objects.get(id=user_id)

            # Check if the user has sent more than 3 requests in the last minute
            one_minute_ago = timezone.now() - timedelta(minutes=1)
            recent_requests = FriendRequest.objects.filter(
                sender=request.user, timestamp__gte=one_minute_ago).count()

            if recent_requests >= 3:
                return Response({"detail": "You can only send 3 friend requests per minute."}, status=status.HTTP_429_TOO_MANY_REQUESTS)

            if request.user == receiver:
                return Response({"detail": "You cannot send a friend request to yourself."}, status=status.HTTP_400_BAD_REQUEST)

            # Send friend request
            friend_request, created = FriendRequest.objects.get_or_create(
                sender=request.user, receiver=receiver)

            if created:
                return Response({"detail": "Friend request sent."}, status=status.HTTP_201_CREATED)
            else:
                return Response({"detail": "Friend request already sent."}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)


class AcceptFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try:
            sender = CustomUser.objects.get(id=user_id)
            request.user.accept_friend_request(sender)
            return Response({"detail": "Friend request accepted."}, status=status.HTTP_200_OK)
        except:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)


class RejectFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try:
            sender = CustomUser.objects.get(id=user_id)
            request.user.reject_friend_request(sender)
            return Response({"detail": "Friend request rejected."}, status=status.HTTP_200_OK)
        except:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)


class ListFriendsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        friends = request.user.friends.all()
        serializer = UserSerializer(friends, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListPendingFriendRequestsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pending_requests = FriendRequest.objects.filter(
            receiver=request.user, status='pending')
        senders = [request.sender for request in pending_requests]
        serializer = UserSerializer(senders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
