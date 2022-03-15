"""View module for handling requests about pokemon"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from shinydexapi.models import Pokemon, DexUser


class PokemonView(ViewSet):
    """ShinyDex pokemon view"""
    
    permission_classes = [ DjangoModelPermissions ]
    queryset = Pokemon.objects.none()

    def retrieve(self, request, pk):
        """Handle GET requests for single pokemon

        Returns:
            Response -- JSON serialized pokemon
        """
        try:
            pokemon = Pokemon.objects.get(pk=pk)
            serializer = PokemonSerializer(pokemon)
            return Response(serializer.data)
        except Pokemon.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        pokemon = Pokemon.objects.all()
        serializer = PokemonSerializer(pokemon, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """
        user = DexUser.objects.get(user=request.auth.user)
        try:
            serializer = CreatePokemonSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        """Handle PUT requests for a pokemon

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            pokemon = Pokemon.objects.get(pk=pk)
            serializer = CreatePokemonSerializer(pokemon, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        pokemon = Pokemon.objects.get(pk=pk)
        pokemon.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class PokemonSerializer(serializers.ModelSerializer):
    """JSON serializer for pokemon
    """
    class Meta:
        model = Pokemon
        fields = ('id', 'name', 'pokemon_kind', 'description',
                  'standard_height', 'standard_alpha_height', 'standard_weight',
                   'standard_alpha_weight', 'is_shiny', 'is_alpha', 'home_regions', 'poke_types', 'poke_items')
        depth = 1
        

class CreatePokemonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pokemon
        fields = ['id', 'name', 'pokemon_kind', 'description',
                  'standard_height', 'standard_alpha_height', 'standard_weight',
                   'standard_alpha_weight', 'is_shiny', 'is_alpha']
        