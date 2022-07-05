from django.shortcuts import redirect, render, get_object_or_404
from .models import Post, Group, User
from django.core.paginator import Paginator
from .forms import PostForm
from django.contrib.auth.decorators import login_required

ELEMENT_QUANTITY = 10
ELEMENT_LAST_POST = 1


def index(request):
    post_list = Post.objects.all().select_related('group')
    paginator = Paginator(post_list, ELEMENT_QUANTITY)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    paginator = Paginator(post_list, ELEMENT_QUANTITY)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)
    

def profile(request, username):
    post = get_object_or_404(User, username=username)
    post_list = post.posts.all()
    paginator = Paginator(post_list, ELEMENT_QUANTITY)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    post_count = post_list.count()
    context = {
        'post': post,
        'page_obj': page_obj,
        'post_count': post_count,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user_post = Post.objects.get(id=post_id)
    post_count = user_post.author.posts.count()
    context = {
        'post': post,
        'post_count': post_count
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    name = request.user.username
    ch_group = Group.objects.all()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.author_id = request.user.id
            form.save()
            return redirect('posts:profile', name)
        return render(request, 'posts/create_post.html', {'form': form, 'ch_group': ch_group})
    form = PostForm()
    context = {
        'form': form,
        'ch_group': ch_group
    }
    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect(
            'posts:post_detail',
            post_id=post_id
        )
    form = PostForm(request.POST or None, instance=post)
    if not form.is_valid():
        return render(request, 'posts/create_post.html', {
            'form': form,
            'post_id': post_id,
            'is_edit': True
        })
    form.save()
    return redirect('posts:post_detail', post_id=post_id)


