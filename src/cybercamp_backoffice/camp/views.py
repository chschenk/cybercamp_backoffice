from django.views.generic import TemplateView, RedirectView, CreateView, ListView, DetailView, UpdateView, DeleteView
from django.views import View
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseForbidden
from django.core.signing import Signer, BadSignature
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils import timezone
from cybercamp_backoffice.camp.models import Map, User, Workshop


class StartView(TemplateView):
	template_name = "camp/start.html"


class GoToCybercampView(RedirectView):
	permanent = False
	query_string = False
	pattern_name = 'cybercamp'

	def get_redirect_url(self, *args, **kwargs):
		if not self.request.user.is_authenticated:
			return '/'

		return settings.WORK_ADVENTURE_URL.rstrip('/') + '/register/' + Signer().sign(self.request.user.wa_uuid)


class LoginUrlView(View):
	"""
	Login User and return start Map etc
	"""
	def get(self, request, login_token):
		if self.request.headers.get('Authorization') != settings.ADMIN_API_TOKEN:
			return HttpResponseForbidden('Not authenticated')

		try:
			uuid = Signer().unsign(login_token)

			user = get_object_or_404(User, wa_uuid=uuid)
			admin_api_data = {
				'userUuid': user.wa_uuid,
				'organizationSlug': user.wa_organization,
				'worldSlug': user.wa_world,
				'roomSlug': user.wa_room,
				'mapUrlStart': "",  # never read !
				'textures': [  # TODO: add to database
					{
						'id': 2,
						'level': 6,
						'url': 'resources/characters/pipoya/Headmaster male.png'
					}
				],
				'playerName': user.username,
				'characterLayers': ["customCharacterTexture2"],  # TODO: add to database
			}
			return JsonResponse(admin_api_data)
		except BadSignature:
			return HttpResponseNotFound('User unknown')


class MapView(View):
	"""
	Get Map for request
	"""

	ANONYMOUS_POLICY = 1
	MEMBERS_ONLY_POLICY = 2
	USE_TAGS_POLICY = 3

	def get(self, request):
		if self.request.headers.get('Authorization') != settings.ADMIN_API_TOKEN:
			return HttpResponseForbidden('Not authenticated')

		organization_slug = request.GET.get('organizationSlug')
		world_slug = request.GET.get('worldSlug')
		room_slug = request.GET.get('roomSlug')

		map_object = Map.objects.filter(organization=organization_slug, world=world_slug, room=room_slug)[:1]
		level = 1
		if not map_object:
			map_object = Map.objects.filter(organization=organization_slug, world=world_slug)[:1]
			level = 2
			if not map_object:
				map_object = Map.objects.filter(organization=organization_slug)[:1]
				level = 3

		if map_object:
			map_object = map_object.get()
			url = map_object.map_url.rstrip('/')
			if level == 3:
				url += '/' + world_slug
			if level >= 2:
				url += '/' + room_slug

			map_data = {
				'organizationSlug': organization_slug,
				'worldSlug': world_slug,
				'roomSlug': room_slug,
				'mapUrl': url,
				'tags': [organization_slug],  # TODO: add tags from db
				'policy_type': map_object.policy,
			}

			return JsonResponse(map_data)
		else:
			return HttpResponseNotFound('Unknown Map')


class MembershipView(View):
	"""
	Check if user is available
	"""
	def get(self, request, user_id):
		if self.request.headers.get('Authorization') != settings.ADMIN_API_TOKEN:
			return HttpResponseForbidden('Not authenticated')

		user = User.objects.filter(wa_uuid=user_id)[:1]

		if user:
			user = user.get()

			tags = [
				user.wa_organization,
			]
			if user.is_superuser:
				tags += [
					'admin',
				]
			if user.is_staff:
				tags += [
					'staff',
				]

			membership_data = {
				'uuid': user_id,  # never Read
				'tags': tags,
				'textures': [  # TODO: move to database
					{
						'id': 2,
						'level': 6,
						'url': 'resources/characters/pipoya/Headmaster male.png'
					}
				],
				'messages': [],
				# 'messages': [{'type': 'TypeMessageExt', 'message': 'hello membershipAction'}],
				# 'messages': [{'type': 'Banned', 'message': 'You are banned'}],
			}
			return JsonResponse(membership_data)
		else:
			if settings.ALLOW_ANONYMOUS_LOGIN_INTO_WORKADVENTURE:
				return HttpResponseNotFound('User unknown')
			else:
				membership_data = {
					'uuid': user_id,  # never Read
					'tags': [],
					'textures': [],
					'messages': [{'type': 'Banned', 'message': 'Only registered Users are allowed on this Server'}],
				}
				return JsonResponse(membership_data)


class CheckUserView(View):
	"""
	Check if user is available
	"""
	def get(self, request, user_id):
		if self.request.headers.get('Authorization') != settings.ADMIN_API_TOKEN:
			return HttpResponseForbidden('Not authenticated')

		user = get_object_or_404(User, wa_uuid=user_id)

		user_data = {
			'userUuid': user_id,  # never Read, but to identify
		}
		return JsonResponse(user_data)


class CheckModerateUserView(View):
	"""
	Check if user is available
	"""
	def get(self, request, organization_slug, world_slug):
		if self.request.headers.get('Authorization') != settings.ADMIN_API_TOKEN:
			return HttpResponseForbidden('Not authenticated')

		admin_banned_data = {
			'is_banned': False,
			'message': '',  # Never Read :/
		}
		return JsonResponse(admin_banned_data)


class WorkshopCreateView(LoginRequiredMixin, CreateView):
	login_url = reverse_lazy('login')
	success_url = reverse_lazy('camp:list_workshop')
	model = Workshop
	fields = ('name', 'description', 'start_time', 'end_time', 'location')

	def form_valid(self, form):
		form.instance.organizer = self.request.user
		return super(WorkshopCreateView, self).form_valid(form)


class WorkshopListView(LoginRequiredMixin, ListView):
	login_url = reverse_lazy('login')
	model = Workshop
	ordering = ['start_time']
	paginate_by = 10
	def get_queryset(self):
		qs = super().get_queryset()
		return qs.filter(end_time__gt=timezone.now()).order_by('start_time', 'name')


class PastWorkshopListView(LoginRequiredMixin, ListView):
	login_url = reverse_lazy('login')
	model = Workshop
	ordering = ['start_time']
	paginate_by = 10


class MyWorkshopListView(LoginRequiredMixin, ListView):
	login_url = reverse_lazy('login')
	model = Workshop
	ordering = ['start_time']
	paginate_by = 10
	def get_queryset(self):
		qs = super().get_queryset()
		return qs.filter(organizer=self.request.user)


class WorkshopDetailView(LoginRequiredMixin, DetailView):
	login_url = reverse_lazy('login')
	model = Workshop


class WorkshopUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	login_url = reverse_lazy('login')
	success_url = reverse_lazy('camp:list_workshop')
	model = Workshop
	fields = ('name', 'description', 'start_time', 'end_time', 'location')

	def test_func(self):
		return self.request.user.pk == self.get_object().organizer.pk or self.request.user.is_staff

class WorkshopDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	login_url = reverse_lazy('login')
	success_url = reverse_lazy('camp:list_workshop')
	model = Workshop

	def test_func(self):
		return self.request.user.pk == self.get_object().organizer.pk or self.request.user.is_staff