from django import forms
from django.db import models
from django.shortcuts import render

# New imports added for ClusterTaggableManager, TaggedItemBase

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.conf import settings
from wagtail.images.models import Image
from modelcluster.fields import ParentalKey

# Create your models here.



class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        
        blogpages = self.get_children().live().order_by('-first_published_at')
        homepage = self.get_parent().live().order_by('-first_published_at')
        paginator = Paginator(blogpages, 1)
        page = request.GET.get("page")
        try:
            posts = paginator.page(page)
        
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        context["posts"] = posts
        context['blogpages'] = blogpages

        
        return context
    

@register_snippet
class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class TopicPage(Page):
    intro = models.CharField(max_length=255, blank=True, null=True)
    
    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None
    
    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        InlinePanel('gallery_images', label="Gallery images"),
    ]

    subpage_types = ['BlogIndexPage']

class TopicPageGalleryImage(Orderable):
    topic_page = ParentalKey(TopicPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        "wagtailimages.Image", on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]

class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    
    authors = ParentalManyToManyField('blog.Author', blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    
    #Add the main_image method:
    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None
    def get_tags_as_strings(self):
        return [tag.name for tag in self.tags.all()]
    
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        blogpages = self.get_children().live().order_by('-first_published_at')
        for blogpage in blogpages:
            blogpage.first_image = blogpage.main_image()  # Thay thế dòng này
            if blogpage.gallery_images.exists():
                blogpage.first_image = blogpage.gallery_images.first().image
        context['blogpages'] = blogpages
        
        return context
    
    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]
    content_panels = Page.content_panels + [

        InlinePanel('gallery_images', label="Gallery images"),
        FieldPanel('intro'),
        FieldPanel('body'),

        
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('authors', widget=forms.CheckboxSelectMultiple),
            FieldPanel('tags'),
        ], heading="Blog information"),
        
    ]

class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        "wagtailimages.Image", on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]

@register_snippet
class Author(models.Model):
    name = models.CharField(max_length=255)
    author_image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('author_image'),
    ]

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Authors'

@register_snippet
class BlogTagIndexPage(Page):
    def get_context(self, request):

        tag = request.GET.get('tag')
        blogpages = BlogPage.objects.filter(tags__name=tag)

        context = super().get_context(request)
        context['blogpages'] = blogpages
        return context


class Comment(models.Model):
    post = models.ForeignKey(BlogPage, on_delete=models.CASCADE, related_name='comments')
    email = models.EmailField()
    name = models.CharField(max_length=50)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    user_author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return f"Comment form {self.name} - {self.body}"
    
    
class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user_author = kwargs.pop('user_author', None)
        self.post = kwargs.pop('post', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        comment = super().save(commit=False)
        comment.user_author= self.user_author
        comment.post = self.post
        comment.save()
    class Meta:
        model = Comment
        fields = ["body"]