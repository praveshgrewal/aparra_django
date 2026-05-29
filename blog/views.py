from django.shortcuts import render, get_object_or_404
from .models import BlogPost
from store.views import get_footer_content


def blog_list(request):
    posts = BlogPost.objects.filter(status='published').order_by('-published_at', '-created_at')
    return render(request, 'blog/list.html', {'posts': posts, 'footer_content': get_footer_content()})


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, status='published')
    related = BlogPost.objects.filter(status='published').exclude(id=post.id)[:3]
    return render(request, 'blog/detail.html', {
        'post': post,
        'related_posts': related,
        'footer_content': get_footer_content(),
    })
