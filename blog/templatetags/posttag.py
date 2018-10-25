from django import template

from accounts.models import UserProfile

register = template.Library()


@register.filter(name='get_nickname')  # 过滤器在模板中使用时的name
def get_nickname(user_id):
    try:
        up = UserProfile.objects.get(user_id=user_id)
    except Exception as e:
        nickname = '无名氏'
    else:
        nickname = up.nickname
    return nickname

