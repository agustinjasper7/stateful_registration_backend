from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from backend.users.constants import MAX_REGISTRATION_STEP, MIN_REGISTRATION_STEP


class User(AbstractUser):
    """
    Default custom user model for backend.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    #: First and last name do not cover name patterns around the globe
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    # Registration Steps
    step1 = models.CharField(_("Registration step 1"), blank=True, max_length=255)
    step2 = models.CharField(_("Registration step 2"), blank=True, max_length=255)
    step3 = models.CharField(_("Registration step 3"), blank=True, max_length=255)

    @property
    def current_registration_step(self):
        if not self.step1:
            return 1
        if not self.step2:
            return 2
        if not self.step3:
            return 3
        return 4

    def update_registration_step(self, step, value):
        if step < MIN_REGISTRATION_STEP or step > MAX_REGISTRATION_STEP:
            return

        step_mapping = ["", "step1", "step2", "step3"]
        setattr(self, step_mapping[step], value)
        self.save()
