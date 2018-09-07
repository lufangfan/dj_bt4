from allauth.account.signals import user_signed_up
from django.dispatch import receiver

from accounts.models import UserProfile


@receiver(user_signed_up, dispatch_uid="allauth.user_signed_up")
def profile_init(user, **kwargs):
    nickname = str(user.id)+'号破壁人'
    avatar = 'avatar/default_user_avatar.jpg'
    UserProfile.objects.get_or_create(user=user, defaults={'nickname': nickname, 'avatar': avatar})
    print('userproflie init success!')
