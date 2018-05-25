from django.db import models
from django.utils import timezone

class Room(models.Model):
	label = models.SlugField(unique=True)

	def __str__(self):
		return '{}'.format(self.label)

class Message(models.Model):
	room = models.ForeignKey(Room, related_name='messages')
	handle = models.TextField()
	message = models.TextField()
	timestamp = models.DateTimeField(default=timezone.now, db_index=True)

	def __str__(self):
		return '[{timestamp}] {handle}: {message}'.format(**self.as_dict())

	@property
	def formatted_timestamp(self):
		return self.timestamp.strftime('%x %X')
	
	def as_dict(self):
		return {'handle': self.handle, 'message': self.message, 'timestamp': self.formatted_timestamp}