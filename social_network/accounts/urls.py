from .views import *
from django.urls import path

urlpatterns = [
    path('signup/', view=signup, name='signup'),
    path('login/', view=login_view, name='login_view'),
    path('logout/', view=logout_view, name='logout'),
    path('search/', view=search_users, name='search_users'),
    path('send_requests/', view=send_requests, name='send_requests'),
    path('accept_requests/', view=accept_requests, name='accept_requests'),
    path('reject_requests/', view=reject_requests, name='reject_requests'),
    path('list_friends/', view=list_friends, name='list_friends'),
    path('pending_list/', view=request_pending_lists, name='pending_list'),
]
