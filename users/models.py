from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def ensure_profile(sender, instance: User, created, **kwargs):
    """
    Always have a Profile. If created and nickname missing, assign a safe unique default.
    This covers superusers created via createsuperuser and any programmatic user creation.
    """
    profile, made = Profile.objects.get_or_create(user=instance)
    if (made or not profile.nickname):
        default_base = instance.username or (instance.email.split("@")[0] if instance.email else "user")
        profile.nickname = _unique_nickname(default_base)
        profile.save(update_fields=["nickname"])

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    nickname = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    # optional profile areas via the blank =True, null=True code
    # Definitely would be preferred in a realistic, but for the sake of testing and making new profiles, I am making these choices optional for convenience
    dob = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True) # 15 should be the max digits you can have in a phone number

    def __str__(self):
        return self.user.username

def _unique_nickname(base: str) -> str:
    """
    Generate a unique nickname from a base string (e.g., username).
    Ensures we never leave nickname null/blank, even for superusers created via CLI.
    """
    base = (base or "user").strip() or "user"
    candidate = base
    i = 1
    from django.db.models import Q
    while Profile.objects.filter(Q(nickname__iexact=candidate)).exists():
        i += 1
        candidate = f"{base}-{i}"
    return candidate