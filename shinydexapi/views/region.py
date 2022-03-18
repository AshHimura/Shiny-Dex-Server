"""View module for handling requests about pokemon"""
from django.http import HttpResponseServerError
from rest_framework.decorators import action
import json
from django.core.exceptions import ValidationError
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from shinydexapi.models import Region, DexUser


class RegionView(ViewSet):
    """ShinyDex region view"""

    permission_classes = [DjangoModelPermissions]
    queryset = Region.objects.none()

    def retrieve(self, request, pk):
        """Handle GET requests for single region

        Returns:
            Response -- JSON serialized region
        """
        try:
            region = Region.objects.get(pk=pk)
            serializer = RegionSerializer(region)
            return Response(serializer.data)
        except Region.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        region = Region.objects.all()
        serializer = RegionSerializer(region, many=True)
        return Response(serializer.data)

    

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """
        try:
            serializer = CreateRegionSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        """Handle PUT requests for a region

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            region = Region.objects.get(pk=pk)
            serializer = CreateRegionSerializer(region, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        region = Region.objects.get(pk=pk)
        region.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class RegionSerializer(serializers.ModelSerializer):
    """JSON serializer for region
    """
    class Meta:
        model = Region
        fields = ('id', 'name')


class CreateRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name']
