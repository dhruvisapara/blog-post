from django.shortcuts import render
from django.http import JsonResponse
from .models import Post


def create_post(request):
    posts = Post.objects.all()
    response_data = {}

    if request.POST.get('action') == 'post':#check method
        title = request.POST.get('title')
        description = request.POST.get('description')
        response_data['title'] = title
        response_data['description'] = description

        Post.objects.create(
            title=title,
            description=description,
        )
        return JsonResponse(response_data)

    return render(request, 'ajaxpost/create_post.html', {'posts': posts})


def blog_view(request):
    posts = Post.objects.all().order_by('-id')
    return render(request, 'ajaxpost/blog.html', {'posts': posts})


def create_post_view(request):
    if request.POST.get('action') == 'create-post':
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')  # request.FILES used for to get files
        Post.objects.create(
            title=title,
            description=description,
            image=image
        )

    return render(request, 'ajaxpost/create.html')
