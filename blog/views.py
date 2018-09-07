import json

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from blog.models import Article, Comment
from blog.serializers import CommentSerializer


@login_required
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
        comments = Comment.objects.all()
        context = {'article': article, 'user': request.user, 'comments': comments}
        return render(request, 'blog/blog-post.html', context)


@login_required
def comment_submit(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        content = request.POST.get('comment')
        article_id = request.POST.get('article_id')
        
        try:
            user_id = int(user_id)
            article_id = int(article_id)
        except Exception as e:
            resp = {'statecode': 400, 'detail': 'Bad Request Parameters'}
        else:
            comment = Comment.objects.submit_comment(user_id, article_id, content)
            serializers = CommentSerializer(comment)
            print(serializers.data)
            resp = {'statecode': 200, 'comment': serializers.data}
    else:
        resp = {'statecode': 400, 'detail': 'Bad Request Method'}
    return HttpResponse(json.dumps(resp), content_type="application/json")
