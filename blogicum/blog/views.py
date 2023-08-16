from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from blog.models import Category, Post

COUNT_OF_POST = 5


def get_short_code():
    '''Вспомогательная функция для нуждающихся функций.'''
    return Post.objects.select_related(
        'category',
        'location',
        'author'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    )


def index(request):
    '''Главная страница со всеми постами.'''
    posts = get_short_code()[:COUNT_OF_POST]
    context = {'posts': posts}
    return render(request, 'blog/index.html', context)


def post_detail(request, post_id):
    '''Страница определенного поста.'''
    post_list = get_object_or_404(
        get_short_code(),
        pk=post_id
    )
    context = {'post': post_list}
    return render(request, 'blog/detail.html', context)


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
        pub_date__lte=timezone.now()
    )
    context = {'posts': posts, 'category': category}
    return render(request, 'blog/category.html', context)
