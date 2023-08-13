from datetime import datetime

from blog.models import Category, Post
from django.shortcuts import get_object_or_404, render


def index(request):
    '''Главная страница со всеми постами.'''
    posts = Post.objects.select_related(
        'category',
        'location',
        'author'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=datetime.now()
    )[0:5]
    context = {'posts': posts}
    return render(request, 'blog/index.html', context)


def post_detail(request, post_id):
    '''Страница определенного поста.'''
    template = 'blog/detail.html'
    post_list = get_object_or_404(Post.objects.select_related(
        'location', 'author', 'category').filter(
            is_published=True,
            pub_date__lte=datetime.now(),
            category__is_published=True,
    ), pk=post_id
    )
    context = {'post': post_list}
    return render(request, template, context)


def category_posts(request, category_slug):
    '''Страница с постами определнной категории.'''
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )
    posts = Post.objects.filter(
        category=category,
        is_published=True,
        pub_date__lte=datetime.now()
    )
    context = {'posts': posts, 'category': category}
    return render(request, 'blog/category.html', context)
