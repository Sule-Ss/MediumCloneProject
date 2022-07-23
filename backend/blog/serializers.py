
from numpy import require
from rest_framework import serializers
from .models import Story, Tag, StoryClap
from users.models import UserProfile
from django.contrib.auth.models import User


class StoryClapSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryClap
        fields = (
            "user",
            "story",
        )



class StorySerializer(serializers.ModelSerializer):
    clap_story = StoryClapSerializer(many = True)
    creatorInfo = serializers.SerializerMethodField('get_creatorInfo')
    tags=serializers.SerializerMethodField('get_tags')
    tag_name = serializers.CharField(write_only=True)
    user_id = serializers.IntegerField(write_only=True)
    # image_upload = serializers.ImageField(
    #     write_only=True, use_url=True, allow_null =False, allow_empty_file= False, required=False)
    class Meta:
        model = Story
        fields = (
            "id",
            "creatorInfo",
            "title",
            "content",
            "image",
            "tags",
            "publish_date",
            "tag_name",
            "user_id",
            "status",
            "clap_story"
            # "image_upload"
        )
    
    def get_tags(self,obj):
        return obj.tags.all().values('tag_name')

    def get_creatorInfo(self, obj):
        user_img =  UserProfile.objects.filter(user= obj.user).first()
        short_bio = user_img.short_bio
        request = self.context.get('request')
        user_img = user_img.profile_photo.url
        user_img = request.build_absolute_uri(user_img)
        print(user_img)
        
        context = {
            "first_name" : obj.user.first_name,
            "last_name": obj.user.last_name,
            "email": obj.user.email,
            "user_img": user_img,
            "short_bio":short_bio,
        }
        return  context


    def create(self, validated_data):
        tag_name = validated_data.pop("tag_name")
        user_id = validated_data.pop("user_id")
        
        createrUser = User.objects.get(id=user_id)
        print(createrUser)


        if Tag.objects.filter(tag_name__iexact=tag_name).exists():
            categoryOfStory=Tag.objects.get(tag_name__iexact = tag_name)
        else:
            categoryOfStory=Tag.objects.create(tag_name = tag_name)
        

        validated_data["user_id"] = createrUser.id
        story = Story.objects.create(**validated_data)
        
        story.tags.add(categoryOfStory)

        story.save()
        return story
    
    