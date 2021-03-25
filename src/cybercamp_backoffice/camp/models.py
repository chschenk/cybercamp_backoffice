from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4


class User(AbstractUser):
	wa_uuid = models.UUIDField(auto_created=True, unique=True, default=uuid4)
	wa_organization = models.CharField(max_length=30, help_text='OrganisationSlug, for start map', default='cybercamp')
	wa_world = models.CharField(max_length=30, help_text='WorldSlug, for start map', default='camp')
	wa_room = models.CharField(max_length=30, help_text='RoomSlug, for start map', default='map.json')


class Map(models.Model):
	policy_type_choices = (
		(1, 'Anonymous'),
		(2, 'Members only'),
		(3, 'use Tags'),
	)

	organization = models.CharField(max_length=30, help_text='Organisation used after @')
	world = models.CharField(max_length=30, null=True, blank=True,
							 help_text='if not set, will be added from request to map_url')
	room = models.CharField(max_length=30, null=True, blank=True,
							help_text='if not set, will be added from request to map_url')
	map_url = models.URLField()
	policy = models.IntegerField(choices=policy_type_choices)
