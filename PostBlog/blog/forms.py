from django.core.exceptions import ValidationError
from django.forms import ModelForm, modelformset_factory, forms, BaseModelFormSet, inlineformset_factory
from blog.models import Blog, Comment, Image
from django.utils.translation import gettext_lazy as _


class BlogForm(ModelForm):
    """this form is for adding more blogs"""

    class Meta:
        model = Blog
        fields = [
            'title',
            'pub_date',
            'description',
            'highlights',
            'formset_image',
        ]

        def save(self, commit=True):
            """this method saves the current logged user"""
            blog = super(BlogForm, self).save(commit=False)
            blog.user = True

            if commit:
                blog.save()
            return blog


class CommentForm(ModelForm):
    """to add comments """

    class Meta:
        model = Comment

        fields = [

            'body',
            'active',

        ]

    def save(self, commit=True):
        """it saves current logged in user and blog id """
        user_comment = super(CommentForm, self).save(commit=False)
        user_comment.user = True
        user_comment.blogs = True
        if commit:
            user_comment.save()
        return user_comment


class ImageForm(ModelForm):
    """related images for blogs"""

    def __init__(self, *args, **kwargs):
        """user only show their published blog"""
        self.request = kwargs.pop('request')
        super(ImageForm, self).__init__(*args, **kwargs)
        self.fields['blog_image'].queryset = Blog.objects.filter(
            user=self.request.user.parent)

    class Meta:
        model = Image
        fields = [
            "blog_image",
            'post_image',
        ]


class UpdateForm(ModelForm):
    """this form is for adding more blogs"""

    class Meta:
        model = Blog
        fields = [
            'title',
        ]


class CustomFormSetBase(BaseModelFormSet):

    def add_fields(self, form, index):
        super().add_fields(form, index)
        if 'DELETE' in form.fields and form.instance.pk:
            form.fields['DELETE'] = forms.BooleanField(
                label=_('Delete'),
                widget=forms.CheckboxInput(
                    attrs={
                        'class': 'form-check-input'
                    }
                ),
                required=False
            )
        else:
            form.fields.pop('DELETE', None)


BlogFormSet = modelformset_factory(Blog, form=BlogForm, can_delete=True)
UpdateFormSet = modelformset_factory(Blog, form=UpdateForm)


class BlogImageForm(ModelForm):
    """this form is for adding more blogs"""

    class Meta:
        model = Blog
        fields = [
            'title',
            'pub_date',
            'description',
            'highlights',
            'formset_image',
        ]

    # def validate_formset_image(img):
    #     size = img.size
    #     format = img.name.split(".")[-1]
    #     avaible_formats = [
    #         'png',
    #         'jpeg',
    #         'jpg',
    #     ]
    #     import pdb;
    #     pdb.set_trace()
    #     if size > 4194304:
    #         raise ValidationError("Image size must be less than 4MB")
    #     if format not in avaible_formats:
    #         raise ValidationError("Image extension is not avaible")
    #
    #     return img

    def clean_formset_image(self):
        img = self.cleaned_data['formset_image']
        if img.size > 2621440:  # 2.5 Mb
            raise ValidationError("Your image size is too big,try to upload image that's size is less then.")
        return img
