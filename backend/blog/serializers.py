
# from numpy import require
from rest_framework import serializers
from .models import CommentClap, SavedStories, StorieView, Story, StoryTag, Tag, StoryClap, Comment, TagFollower
from django.utils.timezone import now
from users.models import UserProfile, Following
from django.contrib.auth.models import User


class StoryClapSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryClap
        fields = (
            "user",
        )


class CommentClapSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentClap
        fields = '__all__'


class CommentsSerializer(serializers.ModelSerializer):
    #! yorum sahibi ekleme işini view da yapacağımız için read_only dedik.
    user = serializers.StringRelatedField(read_only=True)
    clap_comment = CommentClapSerializer(many=True, read_only=True)
    clap_comment_count = serializers.IntegerField(
        source='clap_comment.count', read_only=True)
    days_since_joined = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        # exclude = ('story', 'user',)
        fields = ('content', 'user', 'id', 'clap_comment_count',
                  'clap_comment', 'days_since_joined')

    def get_days_since_joined(self, obj):
        return (now() - obj.created_date).days
        # return (now() - obj.created_date).seconds #dakika olarak gostermek istersen


class StoryViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorieView
        fields = ('user',)


class StorySaveSerializer(serializers.ModelSerializer):
    userId = serializers.CharField(source='user.id', read_only=True)
    title = serializers.CharField(source='story.title', read_only=True)
    storyImage = serializers.ImageField(source='story.image', read_only=True)
    content = serializers.CharField(source='story.content', read_only=True)
    creatorInfo = serializers.SerializerMethodField('get_creatorInfo')
    class Meta:
        model = SavedStories
        fields = ('userId', 'story', 'id', 'title', 'content', 'creatorInfo', 'storyImage' )

    def get_creatorInfo(self, obj):

        user_img = UserProfile.objects.filter(user=obj.story.user).first()
        userProfilId = user_img.id
        
        short_bio = user_img.short_bio

        request = self.context.get('request')
        user_img = user_img.profile_photo.url
        user_img = request.build_absolute_uri(user_img)

        followedCount = Following.objects.filter(followed=obj.user).count()

        context = {
            "first_name": obj.story.user.first_name,
            "last_name": obj.story.user.last_name,
            "email": obj.story.user.email,
            "user_img": user_img,
            "short_bio": short_bio,
            "followedCount": followedCount,
            "userProfilId": userProfilId,
            # "userProfilId": obj.user.id,
        }
        return context

    def create(self, validated_data):
        user = self.context.get("request").user
        validated_data['user'] = user
        print(validated_data)
        saved = SavedStories.objects.create(**validated_data)
        return saved


class StorySerializer(serializers.ModelSerializer):

    clap_story = StoryClapSerializer(many=True, read_only=True)
    comments = CommentsSerializer(many=True, read_only=True)
    creatorInfo = serializers.SerializerMethodField('get_creatorInfo')
    tags = serializers.SerializerMethodField('get_tags')
    tag_name = serializers.CharField(write_only=True)
    user_id = serializers.IntegerField(write_only=True)
    clap_count = serializers.IntegerField(
        source='clap_story.count', read_only=True)
    comment_count = serializers.IntegerField(
        source='comments.count', read_only=True)
    views = StoryViewSerializer(many=True, read_only=True)
    views_count = serializers.ReadOnlyField(source='views.count')
    saved_users = StorySaveSerializer(many=True, read_only=True)
    saved_users_count = serializers.ReadOnlyField(source='saved_users.count')

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
            'clap_count',
            "clap_story",
            'comment_count',
            "comments",
            'views',
            'views_count',
            'saved_users',
            'saved_users_count',
        )

    def get_tags(self, obj):
        return obj.tags.all().values('tag_name', 'id')

    def get_creatorInfo(self, obj):

        user_img = UserProfile.objects.filter(user=obj.user).first()
        userId = user_img.id

        short_bio = user_img.short_bio

        request = self.context.get('request')
        user_img = user_img.profile_photo.url
        user_img = request.build_absolute_uri(user_img)
        print(user_img)

        followedCount = Following.objects.filter(followed=obj.user).count()

        context = {
            "first_name": obj.user.first_name,
            "last_name": obj.user.last_name,
            "email": obj.user.email,
            "user_img": user_img,
            "short_bio": short_bio,
            "followedCount": followedCount,
            "userId": userId,
            "userProfilId": obj.user.id,
        }
        return context

    def create(self, validated_data):
        tag_name = validated_data.pop("tag_name")
        user_id = validated_data.pop("user_id")

        createrUser = User.objects.get(id=user_id)
        print(createrUser)

        if Tag.objects.filter(tag_name__iexact=tag_name).exists():
            categoryOfStory = Tag.objects.get(tag_name__iexact=tag_name)
        else:
            categoryOfStory = Tag.objects.create(tag_name=tag_name)

        validated_data["user_id"] = createrUser.id
        story = Story.objects.create(**validated_data)

        story.tags.add(categoryOfStory)

        story.save()
        return story


class SearchBarStorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Story
        fields = ('title', 'id', 'image')


class SearchBarTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'tag_name')


class SearchBarUserSerializer(serializers.ModelSerializer):

    # userfor = SearchBarUserProfilSerializer(many=True)
    userImage = serializers.SerializerMethodField('get_userImage')
    userProfilId = serializers.SerializerMethodField('get_userProfilId')

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'userImage', 'userProfilId')

    def get_userImage(self, obj):

        user_img = UserProfile.objects.filter(user=obj.id).first()

        request = self.context.get('request')
        user_img = user_img.profile_photo.url
        user_img = request.build_absolute_uri(user_img)
        print(user_img)
        # context = {
        #     "user_img": user_img,
        # }
        return user_img

    def get_userProfilId(self, obj):

        userProfilId = UserProfile.objects.filter(user=obj.id).first()
        userProfilId = userProfilId.id
        return userProfilId


class AddStoryClapSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryClap
        fields = ('story', )

    def create(self, validated_data):
        user = self.context.get("request").user
        validated_data['user'] = user
        clapp = StoryClap.objects.create(**validated_data)
        return clapp


class TagFollowerSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    userImage = serializers.SerializerMethodField('get_userImage')

    class Meta:
        model = TagFollower
        fields = ('id', 'user', 'userImage', 'tag')

    def get_userImage(self, obj):

        user_img = UserProfile.objects.filter(user=obj.user).first()

        request = self.context.get('request')
        user_img = user_img.profile_photo.url
        user_img = request.build_absolute_uri(user_img)
        print(user_img)
        # context = {
        #     "user_img": user_img,
        # }
        return user_img


class StoryTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryTag
        fields = ('story',)


class TagsSerializer(serializers.ModelSerializer):
    tag_follower = TagFollowerSerializer(many=True, read_only=True)
    stories = StorySerializer(many=True)
    stories_count = serializers.IntegerField(
        source='stories.count', read_only=True)
    tag_follower_count = serializers.IntegerField(
        source='tag_follower.count', read_only=True)

    class Meta:
        model = Tag
        fields = ('tag_name', 'id', "tag_follower_count",
                  'tag_follower', 'stories_count', 'stories')
