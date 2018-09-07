from rest_framework import serializers

from accounts.models import UserProfile
from blog.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    nickname = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ('content', 'date_publish', 'avatar', 'nickname')


    def get_avatar(self, obj):
        try:
            userprofile = UserProfile.objects.get(user=obj.user)
        except UserProfile.DoesNotExist:
            return None
        avatar = ''
        if userprofile.avatar:
            avatar = userprofile.avatar.url
        return avatar

    def get_nickname(self, obj):
        try:
            userprofile = UserProfile.objects.get(user=obj.user)
        except UserProfile.DoesNotExist:
            return ''
        else:
            return userprofile.nickname