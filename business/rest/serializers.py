from rest_framework import serializers

from news.models import news, Images, Category
from users.models import UserData


class ImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Images
        fields = ('image_url',)
    
    def get_image_url(self, obj):
        image = Images.objects.get(News = obj)
        # print(image.image.url)
        return image.image.url

class NewsSerializer(serializers.ModelSerializer):
    image_url = ImageSerializer(read_only = True)
    class Meta:
        model = news
        fields = (
            'id','Heading', 'News', 'timestamp', 
            'tags', 'category', 'author', 
            'excerpt', 'slug','image_url',
        )

class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ('userID', 'newsID')

class UniqueIDSerializer(serializers.Serializer):

    userID = serializers.UUIDField()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('title','slug',)

class CategoryNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = news
        fields = (
            'id','Heading', 'News', 'timestamp', 
            'tags', 'category', 'author', 
            'excerpt', 'slug',
        )
