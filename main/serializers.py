from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import (Problem, Picture, Reply, Comment)


class PictureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Picture
        fields = ('image',)


class ProblemSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Problem
        fields = ('id', 'title', 'description', 'author')
    
    def create(self, validated_data):
        request = self.context.get('request')
        pictures_files = request.FILES 
        problem = Problem.objects.create(
            author=request.user, **validated_data
        )
        for picture in pictures_files.getlist('pictures'):
            Picture.objects.create(
                image=picture, problem=problem
            )
        return problem

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['images'] = PictureSerializer(
            instance.pictures.all(), many=True
        ).data
        return representation


class ReplySerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email'),

    class Meta:
        model = Reply
        fields = "__all__"
    
    def create(self, validated_data):
        request = self.context.get('request')
        reply = Reply.objects.create(
            author=request.user,
            **validated_data
        )
        return reply


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Comment
        fields = "__all__"

    def create(self, validated_data):
        request = self.context.get('request')
        comment = Comment.objects.create(
            author=request.user,
            **validated_data
        )
        return comment




