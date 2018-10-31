import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from accounts.models import UserProfile
from blog.models import Article, Comment, Tag
from blog.serializers import CommentSerializer



def blog_page(request):
    articles = Article.objects.all().order_by('-date_publish')
    context = {'articles': articles, 'user': request.user}
    return render(request, 'blog/blog-page.html', context)


@login_required
def blog_post(request, pk):
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        pass
    else:
        cms = []
        comments = Comment.objects.filter(article=article, supercomment_id=None, reply_to_user_id=None)
        for comment in comments:
            cm = []
            cm.append(comment)
            sub_cms = Comment.objects.filter(supercomment_id=comment.id)
            cm.append(sub_cms)
            cms.append(cm)
        context = {'article': article, 'user': request.user, 'comments': cms, 'article_author': UserProfile.objects.get(user=article.user), 'tags': Tag.objects.filter(article=article)}
        print(cms)
        return render(request, 'blog/blog-post.html', context)



def comment_submit(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        content = request.POST.get('comment')
        article_id = request.POST.get('article_id')
        reply_user_id = request.POST.get('reply_user_id', None)
        supercomment_id = request.POST.get('supercomment_id', None)
        try:
            user_id = int(user_id)
            article_id = int(article_id)
            if supercomment_id is not None and supercomment_id != '':
                supercomment_id = int(supercomment_id)
            if reply_user_id is not None and reply_user_id != '':
                reply_user_id = int(reply_user_id)
        except Exception as e:
            resp = {'statecode': 400, 'detail': 'Bad Request Parameters'}
        else:
            comment = Comment.objects.submit_comment(user_id, article_id, content, supercomment_id, reply_user_id)
            serializers = CommentSerializer(comment)
            print(serializers.data)
            resp = {'statecode': 200, 'comment': serializers.data}
    else:
        resp = {'statecode': 400, 'detail': 'Bad Request Method'}
    return HttpResponse(json.dumps(resp), content_type="application/json")
