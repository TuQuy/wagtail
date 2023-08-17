


from rest_framework import serializers

from business.home.models import HomePage


class HomePageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HomePage
        fields = '__all__'