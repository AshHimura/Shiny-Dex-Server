"""View module for handling requests about caught"""

from django.http import HttpResponseServerError
from rest_framework.decorators import action
from django.core.exceptions import ValidationError
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from shinydexapi.models import Caught, Pokemon, DexUser


class CaughtView(ViewSet):
    """ShinyDex caught view"""

    permission_classes = [DjangoModelPermissions]
    queryset = Caught.objects.none()

    def retrieve(self, request, pk):
        """Handle GET requests for single caught

        Returns:
            Response -- JSON serialized caught
        """
        try:
            caught = Caught.objects.get(pk=pk)
            serializer = CaughtSerializer(caught)
            return Response(serializer.data)
        except Caught.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all caught pokemon

        Returns:
            Response -- JSON serialized list of caught pokemon
        """
        caught = Caught.objects.all()
        serializer = CaughtSerializer(caught, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """
        # Many-to-Many fields require an empty list in create
        user = DexUser.objects.get(user=request.auth.user)
        pokemon = Pokemon.objects.get(pk=request.data['pokemon'])
        try:
            serializer = CreateCaughtSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user, pokemon=pokemon)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        """Handle PUT requests for a caught

        Returns:
            Response -- Empty body with 204 status code
        """
        # user = DexUser.objects.get(user=request.auth.user)
        # pokemon = Pokemon.objects.get(pk=pk)
        try:
            caught = Caught.objects.get(pk=pk)
            serializer = CreateCaughtSerializer(caught, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)


class CaughtSerializer(serializers.ModelSerializer):
    """JSON serializer for caught
    """
    class Meta:
        model = Caught
        fields = ('__all__')
        depth = 1


class CreateCaughtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caught
        fields = ['id', 'is_shiny', 'is_alpha']
