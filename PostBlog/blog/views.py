import logging

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView, DeleteView, ListView, CreateView, TemplateView

from PostBlog.settings import logger
from blog.forms import ImageForm, BlogForm, CommentForm, BlogFormSet, UpdateFormSet, BlogImageForm
from blog.models import Blog, Comment, Image
from user.models import STAFF


class BlogView(LoginRequiredMixin, ListView):
    """show short information of all blogs"""
    paginate_by = 2
    template_name = 'manager.html'
    context_object_name = 'blog_listing'

    def get_queryset(self):
        """one queryset display all the blogs
            also filter by search query.
        """
        query = self.request.GET.get("title")
        logging.getLogger().setLevel(logging.INFO)
        logger.info('something')
        if query:
            object_list = Blog.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query) | Q(user__username__icontains=query)
            )
            return object_list
        else:
            return Blog.objects.order_by('pub_date')


class AddBlogView(LoginRequiredMixin, CreateView):
    """
        This view is for users who are staff members,
        and only they can add blogs.
    """
    template_name = "blog/addingblog.html"
    success_message = " blog successfully added"
    form_class = BlogForm
    success_url = reverse_lazy('blog:home')

    def form_valid(self, form):
        """after adding blog,
        if user is staff then their manager's id will get or else user id get"""
        blog = form.save(commit=False)
        if self.request.user.user_type == STAFF:
            if self.request.user.parent:
                blog.user = self.request.user.parent

        blog.user = self.request.user
        blog.save()
        return redirect('blog:home')


class UserBlog(LoginRequiredMixin, ListView):
    """user see all the blogs that they upload"""
    template_name = "blog/userblog.html"
    context_object_name = "your_blog"
    success_url = reverse_lazy('blog:home')

    def get_queryset(self, **kwargs):
        """manager see his/her blogs that staff members add behalf
            of their manager and staff members can see their manager's blog"""
        if self.request.user.user_type == "staff":
            return Blog.objects.filter(user=self.request.user.parent.id)

        return Blog.objects.filter(user=self.request.user.id)


class UpdateBlog(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    staff members can update existing blog
    """

    model = Blog
    form_class = BlogForm
    template_name = "blog/update_blog.html"
    success_url = reverse_lazy('blog:home')

    def test_func(self):
        """
        if user is staff members then only they can edit the blogs
        """
        obj = Blog.objects.get(pk=self.kwargs.get('pk'))

        if self.request.user.user_type == "staff":
            return self.request.user.parent_id == obj.user_id

        return self.request.user.id == obj.user_id


class ImageView(ListView):
    """
    This view should filter queryset and display images according to blog.
    """
    template_name = "blog/blog_images.html"
    context_object_name = "blog_images"
    success_url = reverse_lazy('blog:home')

    def get_queryset(self, **kwargs):
        """Image model queryset filtered by blog_id."""
        return Image.objects.filter(blog_image=self.kwargs.get('image'))


class UpdateImage(LoginRequiredMixin, UpdateView):
    """staff members can change the blog image """
    model = Image
    form_class = ImageForm
    template_name = "blog/update_image.html"
    success_url = reverse_lazy("blog:home")


class AddComments(LoginRequiredMixin, CreateView):
    """add comments on blogs."""
    template_name = "blog/comment.html"
    form_class = CommentForm
    success_url = reverse_lazy('blog:home')

    def form_valid(self, form):
        """comment model save the current logged-in username and blog id"""

        user_comment = form.save(commit=False)
        if self.request.user:
            user_comment.comment = self.request.user
            user_comment.blog = Blog.objects.get(pk=self.kwargs.get('pk'))
        user_comment.save()
        return redirect('blog:home')


class ShowComment(LoginRequiredMixin, ListView):
    template_name = 'blog/showcomment.html'
    context_object_name = 'comment_listing'
    success_url = reverse_lazy("blog:home")

    def get_queryset(self):
        """It should filter comment queryset and display comments according to blogs."""
        return Comment.objects.filter(blog=self.kwargs.get('comments'))


class BlogImage(LoginRequiredMixin, CreateView):
    """uploading images related to blogs."""
    template_name = "blog/uploadimage.html"
    form_class = ImageForm
    success_url = reverse_lazy('blog:home')

    def get_form_kwargs(self):
        """user only show their published blog and can upload image for their blog only."""
        kwargs = super(BlogImage, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class SearchView(LoginRequiredMixin, ListView):
    """search by title only"""
    template_name = 'blog/search.html'

    def get_queryset(self):
        """filter queryset by blog title"""
        query = self.request.GET.get("title")
        object_list = Blog.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query) | Q(user__username__icontains=query)
        )
        return object_list


class DetailBlogView(LoginRequiredMixin, ListView):
    """detail information of any blog is given here"""
    template_name = "blog/detail.html"
    context_object_name = "detail_listing"

    def get_queryset(self, **kwargs):
        """detail page will filter by blog """
        return Blog.objects.filter(pk=self.kwargs.get('pk'))


class BlogDelete(LoginRequiredMixin, DeleteView):
    """publisher delete their blogs"""
    model = Blog
    success_url = reverse_lazy('blog:home')

    def get(self, request, *args, **kwargs):
        """after delete the  blog this redirect to main page"""
        self.get_object().delete()
        return redirect(self.success_url)


class ImageDelete(LoginRequiredMixin, DeleteView):
    model = Image
    success_url = reverse_lazy('blog:home')

    def get(self, request, *args, **kwargs):
        """after delete the images this  redirect to main page"""
        self.get_object().delete()
        return redirect(self.success_url)


class UpdateBlogAjax(View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        title1 = request.GET.get('title', None)
        description1 = request.GET.get('description', None)
        highlights1 = request.GET.get('highlights', None)
        obj = Blog.objects.get(id=id1)
        obj.title = title1
        obj.description = description1
        obj.highlights = highlights1
        obj.save()

        blog = {'id': obj.id, 'title': obj.title, 'description': obj.description, 'highlights': obj.highlights}
        data = {
            'blog': blog
        }
        return JsonResponse(data)


class DeleteBlogAjax(View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        Blog.objects.get(id=id1).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)


class BlogFormSetView(TemplateView):
    """This view is for creating and display multiple form using formset."""
    template_name = "blog/blogformset.html"

    def get(self, *args, **kwargs):
        """Render template that display blog formset."""
        formset = BlogFormSet(queryset=Blog.objects.all())
        return self.render_to_response({'blog_formset': formset})

    def post(self, *args, **kwargs):
        """This method should create multiple blog in formset."""
        formset = BlogFormSet(self.request.POST, self.request.FILES)
        if formset.is_valid():
            new_instances = formset.save(commit=False)
            for object in formset.deleted_objects:
                object.delete()
            for new_instance in new_instances:
                new_instance.user = self.request.user
                new_instance.slug = new_instance.title
                new_instance.save()
            return redirect(reverse_lazy("blog:home"))
        return self.render_to_response({'blog_formset': formset})


def update_blog_formset(request):
    """This view should use for update blogs in formset."""
    template_name = 'store/create_normal.html'
    heading_message = 'Formset Demo'

    if request.method == 'GET':
        formset = UpdateFormSet(request.GET or None)

    if request.method == 'POST':
        formset = UpdateFormSet(data=request.POST)
        if formset.is_valid():

            new_instances = formset.save(commit=False)
            for new_instance in new_instances:
                new_instance.user = request.user
                new_instance.save()
            return redirect('blog:home')
    return render(request, template_name, {
        'formset': formset,
        'heading': heading_message,
    })


class Image_request_form(CreateView):
    model = Blog
    template_name = 'blog/image_form.html'
    form_class = BlogImageForm
    success_url = reverse_lazy("blog:home")

    def post(self, *args, **kwargs):
        """This method should create multiple blog in formset.

        """
        form = BlogImageForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = self.request.user
            obj.save()
            return redirect(reverse_lazy("blog:home"))
        return self.render_to_response({'form': form})

    # def get_form_class(self):
    #     form = self.form_class(self.request.POST, self.request.FILES)
    #     return form

# def image_request_for_form(request):
#     """
#     This view should create blog with image files.There are some validations for image size.
#
#     """
#     if request.method == 'POST':
#         form = BlogImageForm(request.POST, request.FILES)
#         if form.is_valid():
#             obj = form.save(commit=False)
#             obj.user = request.user
#             obj.save()
#             # form.save()
#             return JsonResponse({'error': False, 'message': 'Uploaded Successfully'})
#         else:
#             return JsonResponse({'error': True, 'errors': form.errors})
#     else:
#         form = BlogImageForm()
#         return render(request, 'blog/image_form.html', {'form': form})

# def random(request):
#     return render(request, 'chat/basic_count.html', context={'text': "hello world"})
# class ImageInlineView(CreateView):
#     form_class = RecipeForm
#     template_name = "inline/recipe.html"
#
#     def get_context_data(self, **kwargs):
#         context = super(RecipeView, self).get_context_data(**kwargs)
#         context['recipe_meta_formset'] = IngredientInlineFormset()
#         return context
#
#     def post(self, request, *args, **kwargs):
#         """This method should create recipes and ingredients using inline formset."""
#         self.object = None
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         recipe_meta_formset = IngredientInlineFormset(self.request.POST, request.FILES)
#         if form.is_valid() and recipe_meta_formset.is_valid():
#             return self.form_valid(form, recipe_meta_formset)
#         else:
#             return self.form_invalid(form, recipe_meta_formset)
#
#     def form_valid(self, form, recipe_meta_formset):
#         self.object = form.save(commit=False)
#         self.object.save()
#         product_metas = recipe_meta_formset.save(commit=False)
#         for meta in product_metas:
#             meta.recipe = self.object
#             meta.save()
#         return redirect(reverse("blog:home"))
#
#     def form_invalid(self, form, recipe_meta_formset):
#         return self.render_to_response(
#             self.get_context_data(form=form,
#                                   recipe_meta_formset=recipe_meta_formset
#                                   )
#         )
#
