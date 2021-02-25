from django.urls import include, path
from cybercamp_backoffice.camp.views import StartView


app_name = 'camp'


urlpatterns = [
    path('', StartView.as_view(), name='start'),
]