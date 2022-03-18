"""View module for handling requests about pokemon"""
from django.http import HttpResponseServerError
from rest_framework.decorators import action
import json
from django.core.exceptions import ValidationError
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from shinydexapi.models import Pokemon, RegionPokemon, PokeType, Region, Item


class PokemonView(ViewSet):
    """ShinyDex pokemon view"""

    permission_classes = [DjangoModelPermissions]
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

    @action(methods=["get"], detail=True)
    def getregions(self, request, pk):
        """Handle GET requests to get all pokemon by region

        Returns:
            Response: JSON serialized list of pokemon according to region id
        """
        #Create var to filter regions by id
        regionpoke = RegionPokemon.objects.filter(region_id=pk)
        #set pokemon object to empty list
        pokemon = []
        
        #for loop creates a variable to contain pokemon instance found by id, then append to empty list
        for poke in regionpoke:
            pika = Pokemon.objects.get(pk=poke.pokemon.id)
            pokemon.append(pika)
        serializer = PokemonSerializer(pokemon, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """
        #Many-to-Many fields require an empty list in create
        home_regions = []
        for region in request.data['home_regions']:
            home_regions.append(Region.objects.get(pk=region))
        poke_types = []
        for poketype in request.data['poke_types']:
            poke_types.append(PokeType.objects.get(pk=poketype))
        poke_items = []
        for item in request.data['poke_items']:
            poke_items.append(Item.objects.get(pk=item))
        try:
            serializer = CreatePokemonSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(home_regions=home_regions, poke_types=poke_types, poke_items=poke_items)
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
