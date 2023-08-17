from .models import BlogPage
from rest_framework import serializers



class BlogPageSerializer(serializers.ModelSerializer):
    date = serializers.DateField()
    intro = serializers.CharField(max_length=250)
    body = serializers.CharField()
    tags = serializers.ListField(child=serializers.CharField())
    main_image = serializers.URLField(allow_null=True)
    class Meta:
        model = BlogPage
        fields = ('date', 'intro', 'body', 'tags', 'main_image')