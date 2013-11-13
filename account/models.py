from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    validation_code = models.TextField(editable=False)

    def create_user_profile(self, user, validation_code=''):
        prof = self.model(user=user, validation_code=validation_code)
        prof.save()
        return prof