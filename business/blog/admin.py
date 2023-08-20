from django.contrib import admin

# from blog.models import Comment
from blog.models import BlogPage

# Register your models here.
    
@admin.register(BlogPage)
class BlogPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'display_authors')
    
    def display_authors(self, obj):
        return ", ".join([author.name for author in obj.authors.all()])
    display_authors.short_description = 'Authors'
    
    # def display_tags(self, obj):
    #     return ", ".join([tag.content_object for tag in obj.tags.all()])
    # display_tags.short_description = 'Tags'
    
    
# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('name', 'post', 'email', 'active')
#     date_hierarchy = 'created'