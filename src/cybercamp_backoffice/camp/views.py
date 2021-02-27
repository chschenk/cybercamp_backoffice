from django.views.generic import TemplateView
from django.views import View
from django.http import HttpResponse


class StartView(TemplateView):
	template_name = "camp/start.html"


class CheckUserView(View):

	def get(self, request, user_id):
		return HttpResponse("User ok")
