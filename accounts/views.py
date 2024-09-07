from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSignupSerializer, UserLoginSerializer, UserSerializer
from .models import CustomUser
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination


class UserSearchPagination(PageNumberPagination):
    page_size = 10  # Number of records per page
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserSearchView(APIView):

    def get(self, request):
        search_query = request.query_params.get('search', '').strip().lower()
        users = CustomUser.objects.none()  # Initialize empty queryset

        # Search by exact email match
        if '@' in search_query:
            users = CustomUser.objects.filter(email__iexact=search_query)

        # If no email match, search by name
        if not users.exists():
            users = CustomUser.objects.filter(
                first_name__icontains=search_query
            ) | CustomUser.objects.filter(last_name__icontains=search_query)

        # Paginate the results
        paginator = UserSearchPagination()
        result_page = paginator.paginate_queryset(users, request)

        # Serialize the paginated data
        serializer = UserSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class UserSignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully", "user": {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
