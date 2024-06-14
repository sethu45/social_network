from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
from .models import FriendRequest, Friendship
from .serializers import SignUpSerializer, LoginSerializer, FriendRequestSerializer, FriendshipSerializer
from datetime import timedelta

# class for maximum pagination 
class StandardResultPagination(PageNumberPagination):
    
    page_size = 10
    query_size_page_param = 'page_size'
    max_page_size = 10

# function for register new user
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignUpSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# function for login the registered user
@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([TokenAuthentication])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(username = email, password= password) #custom authentication
        
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'success': 'Successfully logged in'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# function for logout user
@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([TokenAuthentication])
def logout_view(request):
    logout(request)
    return Response({'success': 'Logged out successfully'},status=status.HTTP_200_OK)
    
# search user based on name or email
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def search_users(request):
    query = request.GET.get('search', '').strip()
    if not query:
        return Response({'result':[]}, status=status.HTTP_200_OK)
    if '@' in query:
         users = User.objects.filter(email__iexact = query)
    else:
        users = User.objects.filter(username__icontains = query)
        
    paginator = StandardResultPagination()
    result_page = paginator.paginate_queryset(users, request)
    serializer = SignUpSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

# function for send friend request 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def send_requests(request):
    receiver_id = request.data.get('receiver_id')
    
    try:
        receiver = User.objects.get(id=receiver_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    one_min_ago = timezone.now() - timedelta(minutes=1)
    recent_request = FriendRequest.objects.filter(sender = request.user, timestamp__gte = one_min_ago).count()
    if recent_request >= 3:
        return Response({'status':'Only send three friend request per minute'}, status=status.HTTP_429_TOO_MANY_REQUESTS)
    
    friend_request, created = FriendRequest.objects.get_or_create(sender=request.user, receiver = receiver, status='pending')
    if created:
        return Response({'success': 'Friend request sent'}, status=status.HTTP_201_CREATED)
    return Response({'status': 'Friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)

# function for accept friend request send by other user
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def accept_requests(request):
    request_id = request.data.get('request_id')
    
    try:
        friend_request = FriendRequest.objects.get(id=request_id, receiver = request.user)
    except FriendRequest.DoesNotExist:
        return Response({'error':'Friend request not found'}, status=status.HTTP_400_BAD_REQUEST)
    
    if friend_request.status == 'pending':
        friend_request.status = 'accepted'
        friend_request.save()
        Friendship.objects.create(user1 = friend_request.sender, user2=friend_request.receiver)
        return Response({'success':'Friend request accepted'}, status=status.HTTP_200_OK)
    return Response({'error':'Friend request already accepted'}, status=status.HTTP_400_BAD_REQUEST)

# function for reject friend request
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def reject_requests(request):
    request_id = request.data.get('request_id')
    
    try:
        friend_request = FriendRequest.objects.get(id=request_id, receiver = request.user)
    except FriendRequest.DoesNotExist:
        return Response({'error':'Friend request not found'}, status=status.HTTP_400_BAD_REQUEST)
    
    if friend_request.status == 'pending':
        friend_request.status = 'rejected'
        friend_request.save()
        return Response({'success':'Friend request rejected'}, status=status.HTTP_200_OK)
    return Response({'error':'Friend request already processed'}, status=status.HTTP_400_BAD_REQUEST)

#function for list all friend request
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def list_friends(request):
    friendships = Friendship.objects.filter(Q(user1=request.user) | Q(user2 = request.user))
    friends = [friendship.user1 if friendship.user2==request.user else friendship.user2 for friendship in friendships]
    serializer = SignUpSerializer(friends, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# function for list all pending friend request 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def request_pending_lists(request):
    pending_list = FriendRequest.objects.filter(receiver = request.user, status= 'pending')
    serializer = FriendRequestSerializer(pending_list, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)