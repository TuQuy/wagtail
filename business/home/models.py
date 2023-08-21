from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
class HomePage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        
        blogpages = self.get_children().live().order_by('-first_published_at')
        
        paginator = Paginator(blogpages, 10)
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
