"""View module for handling requests about item"""
from django.http import HttpResponseServerError
from rest_framework.decorators import action
from django.core.exceptions import ValidationError
from rest_framework.permissions import DjangoModelPermissions
from django.core.files.base import ContentFile
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from shinydexapi.models import Post, DexUser


class PostView(ViewSet):
    """ShinyDex post view"""

    permission_classes = [DjangoModelPermissions]
    queryset = Post.objects.none()

    def retrieve(self, request, pk):
        """Handle GET requests for single post

        Returns:
            Response -- JSON serialized post
        """
        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        post = Post.objects.all()
        post = Post.objects.order_by('-publication_date')
        serializer = PostSerializer(post, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """
        user = DexUser.objects.get(user=request.auth.user)
        try:
            serializer = CreatePostSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        """Handle PUT requests for a post

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            post = Post.objects.get(pk=pk)
            serializer = CreatePostSerializer(post, data=request.data)
            serializer.is_valid(raise_exception=True)
            post = serializer.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for post
    """
    class Meta:
        model = Post
        fields = ('__all__')
        depth = 2


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'publication_date', 'content', 'user']
