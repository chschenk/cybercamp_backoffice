from django.urls import include, path
from cybercamp_backoffice.camp.views import StartView, LoginUrlView, MapView, MembershipView, CheckUserView,\
    CheckModerateUserView, GoToCybercampView, WorkshopCreateView, WorkshopListView, WorkshopDetailView,\
    WorkshopUpdateView, WorkshopDeleteView, MyWorkshopListView, PastWorkshopListView, AccountActivationView


app_name = 'camp'


urlpatterns = [
    path('', StartView.as_view(), name='start'),
    path('goToCybercamp', GoToCybercampView.as_view(), name='go_to_cybercamp'),

    path('api/login-url/<login_token>', LoginUrlView.as_view(), name='login_url'),
    path('api/map', MapView.as_view(), name='map'),
    path('api/membership/<uuid:user_id>', MembershipView.as_view(), name='membership'),
    path('api/check-user/<uuid:user_id>', CheckUserView.as_view(), name='check_user'),
    path('api/check-moderate-user/<organization_slug>/<world_slug>', CheckModerateUserView.as_view(),
         name='moderate_user'),

    path('workshop/list', WorkshopListView.as_view(), name='list_workshop'),
    path('workshop/my', MyWorkshopListView.as_view(), name='my_workshop'),
    path('workshop/past', PastWorkshopListView.as_view(), name='past_workshop'),
    path('workshop/create', WorkshopCreateView.as_view(), name='create_workshop'),
    path('workshop/detail/<int:pk>', WorkshopDetailView.as_view(), name='detail_workshop'),
    path('workshop/update/<int:pk>', WorkshopUpdateView.as_view(), name='update_workshop'),
    path('workshop/delete/<int:pk>', WorkshopDeleteView.as_view(), name='delete_workshop'),
    path('accountActivation/<str:activation_key>/', AccountActivationView.as_view(), name='activate_account'),
]
