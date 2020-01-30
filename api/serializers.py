from rest_auth.app_settings import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from api.models import Pouzivatel, PouzivatelProfil, Miestnost, Post, Sprava
from rest_framework import serializers
from django.db import models


class MiestnostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Miestnost
        fields = ['url', 'id', 'nazov']


class PostSerializer(serializers.HyperlinkedModelSerializer):
    odosielatel = serializers.SlugRelatedField(many=False, slug_field='username', queryset=Pouzivatel.objects.all())
    miestnostNazov = serializers.CharField(source='miestnost.nazov', required=False)

    class Meta:
        model = Post
        fields = ['odosielatel', 'miestnost', 'miestnostNazov', 'sprava', 'timestamp']


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = PouzivatelProfil
        fields = ()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Bifrost user writable nested serializer
    """
    profile = UserProfileSerializer(required=False)
    title = serializers.CharField(source='profile.title', max_length=5, allow_blank=True)
    dob = serializers.DateField(source='profile.dob')
    address = serializers.CharField(source='profile.address')
    country = serializers.CharField(source='profile.country')
    city = serializers.CharField(source='profile.city')
    zip = serializers.CharField(source='profile.zip')
    photo = serializers.ImageField(source='profile.photo', allow_null=True)


    class Meta:
        model = Pouzivatel
        fields = ('url', 'id', 'username', 'email', 'first_name', 'last_name', 'password', 'profile', 'title', 'dob', 'address', 'country', 'city', 'zip', 'photo')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = Pouzivatel(**validated_data)
        user.set_password(password)
        user.save()
        PouzivatelProfil.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile

        instance.email = validated_data.get('email', instance.email)
        instance.save()

        profile.title = profile_data.get('title', profile.title)
        profile.dob = profile_data.get('dob', profile.dob)
        profile.address = profile_data.get('address', profile.address)
        profile.country = profile_data.get('country', profile.country)
        profile.city = profile_data.get('city', profile.city)
        profile.zip = profile_data.get('zip', profile.zip)
        profile.photo = profile_data.get('photo', profile.photo)
        profile.save()

        return instance


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        data['username'] = self.user.username
        data['first_name'] = self.user.first_name
        data['last_name'] = self.user.last_name
        data['id'] = self.user.id
        data['title'] = self.user.profile.title
        data['dob'] = self.user.profile.dob
        data['address'] = self.user.profile.address
        data['country'] = self.user.profile.country
        data['city'] = self.user.profile.city
        data['zip'] = self.user.profile.zip
        data['photo'] = self.user.profile.photo.url
        data['groups'] = self.user.groups.values_list('name', flat=True)
        return data


class MessageSerializer(serializers.ModelSerializer):
    odosielatel = serializers.SlugRelatedField(many=False, slug_field='username', queryset=Pouzivatel.objects.all())
    prijmatel = serializers.SlugRelatedField(many=False, slug_field='username', queryset=Pouzivatel.objects.all())

    class Meta:
        model = Sprava
        fields = ['url', 'odosielatel', 'prijmatel', 'sprava', 'timestamp']
