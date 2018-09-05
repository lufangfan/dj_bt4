from django.shortcuts import render

# Create your views here.
from blog.models import Article


def blog_page(request):
    articles = Article.objects.all().order_by('-date_publish')
    context = {'articles': articles, 'user': request.user}
    return render(request, 'blog/blog-page.html', context)


def blog_post(request, pk):
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        pass
    else:
        context = {'article': article, 'user': request.user}
        return render(request, 'blog/blog-post.html', context)
