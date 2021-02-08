from typing import Dict, Tuple
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import DateTimeField, DecimalField


class Entrant(models.Model):
    first_name: str = models.CharField(max_length=100, null=False, blank=False)
    last_name: str = models.CharField(max_length=100, null=False, blank=False)
    company: str = models.CharField(max_length=255, blank=False, null=False)
    tel_number: str = models.CharField(max_length=15, blank=False, null=False)
    id_number: str = models.CharField(max_length=20)

    @staticmethod
    def get_temperature_history(entrant_id: int):
        entrant = Entrant.objects.get(id=entrant_id)
        return entrant.user_temperatures.objects.all()

    def validate(self):
        return True, {}

    def create_entry(self, reading, timestamp):
        self.save()
        temp = Temperature(reading=reading, timestamp=timestamp, user=self)
        temp.save()

    def last_entry(self):
        return self.user_temperatures.all().order_by('-timestamp')[0]


class Temperature(models.Model):
    reading: DecimalField = models.DecimalField(
        max_digits=4, decimal_places=2, null=False)
    timestamp: DateTimeField = models.DateTimeField(null=False, blank=False)
    user: User = models.ForeignKey(
        to=Entrant, on_delete=models.CASCADE, related_name='user_temperatures', null=False)

    def validate(self) -> Tuple[bool, Dict]:
        errors = {}
        if not self.reading:
            errors['error_reading'] = 'Temperature reading can not be empty'

        if not self.timestamp:
            errors['error_timestamp'] = 'Date and Time are required'

        if not self.user:
            raise Exception(
                'User is required to successfully create this record')

        return bool(len(errors.keys())), errors
