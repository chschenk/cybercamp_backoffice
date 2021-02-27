from django.urls import include, path
from cybercamp_backoffice.camp.views import StartView, CheckUserView


app_name = 'camp'


urlpatterns = [
    path('', StartView.as_view(), name='start'),
    path('api/check-user/<uuid:user_id>', CheckUserView.as_view(), name='check_user'),
]
