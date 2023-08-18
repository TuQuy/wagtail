from .models import Author, BlogPage, BlogPageTag
from rest_framework import serializers
from .models import BlogPage, Author, BlogPageGalleryImage


# class BlogPageSerializer(serializers.ModelSerializer):
#     tags = serializers.StringRelatedField(many=True)
#     class Meta:
#         model = BlogPage
#         fields = ['id', 'title', 'date', 'intro', 'body', 'authors', 'tags', 'main_image']

class BlogPageGalleryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPageGalleryImage
        fields = ('image', 'caption')

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class BlogPageSerializer(serializers.ModelSerializer):

    # authors = AuthorSerializer(many=True)
    date = serializers.DateField()
    intro = serializers.CharField(max_length=250)
    body = serializers.CharField()
    main_image = serializers.URLField(allow_null=True)
    # tags = serializers.StringRelatedField(many=True)
    authors = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    def get_authors(self, obj):
        return [{'id': author.id, 'name': author.name} for author in obj.authors.all()]

    def get_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]

    def get_gallery_images(self, obj):
        gallery_images = obj.gallery_images.all()
        return BlogPageGalleryImageSerializer(gallery_images, many=True).data
    
   
    class Meta:
        model = BlogPage
        fields = ['title', 'date', 'intro', 'body', 'authors', 'tags', 'main_image']

