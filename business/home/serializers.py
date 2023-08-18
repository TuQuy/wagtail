


from rest_framework import serializers

from home.models import HomePage


class HomePageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HomePage
        fields = '__all__'