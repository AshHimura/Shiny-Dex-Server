"""View module for handling requests about poketype"""
from django.http import HttpResponseServerError
from rest_framework.decorators import action
import json
from django.core.exceptions import ValidationError
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from shinydexapi.models import PokeType


class PokeTypeView(ViewSet):
    """ShinyDex poketype view"""

    permission_classes = [DjangoModelPermissions]
    queryset = PokeType.objects.none()

    def retrieve(self, request, pk):
        """Handle GET requests for single poketype

        Returns:
            Response -- JSON serialized poketype
        """
        try:
            poketype = PokeType.objects.get(pk=pk)
            serializer = PokeTypeSerializer(poketype)
            return Response(serializer.data)
        except PokeType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all game poketypes

        Returns:
            Response -- JSON serialized list of game poketypes
        """
        poketype = PokeType.objects.all()
        serializer = PokeTypeSerializer(poketype, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """
        try:
            serializer = CreatePokeTypeSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        """Handle PUT requests for a poketype

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            poketype = PokeType.objects.get(pk=pk)
            serializer = CreatePokeTypeSerializer(poketype, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        poketype = PokeType.objects.get(pk=pk)
        poketype.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class PokeTypeSerializer(serializers.ModelSerializer):
    """JSON serializer for poketype
    """
    class Meta:
        model = PokeType
        fields = ('__all__')


class CreatePokeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PokeType
        fields = ['id', 'name']
