from django.urls import include, path
from cybercamp_backoffice.camp.views import StartView, LoginUrlView, MapView, MembershipView, CheckUserView,\
    CheckModerateUserView, GoToCybercampView


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
]
