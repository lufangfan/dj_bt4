from allauth.account.signals import user_signed_up
from django.dispatch import receiver

from accounts.models import UserProfile


@receiver(user_signed_up, dispatch_uid="allauth.user_signed_up")
def profile_init(user, **kwargs):
    nickname = str(user.id)+'号破壁人'
    UserProfile.objects.get_or_create(user=user, defaults={'nickname': nickname})
    print('userproflie init success!')
