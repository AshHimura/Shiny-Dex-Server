"""View module for handling requests about game"""
import base64
import uuid
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from shinydexapi.models import DexUser


class DexUserView(ViewSet):
    """Level up game view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game 
        
        Returns:
            Response -- JSON serialized game 
        """
        try:
            dex_user = DexUser.objects.get(pk=pk)
            serializer = DexUserSerializer(dex_user)
            return Response(serializer.data)
        except DexUser.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 

    def list(self, request):
        """Handle GET requests to get all dex_user 

        Returns:
            Response -- JSON serialized list of dex_user
        """
        dex_users = DexUser.objects.all()
        dex_users = DexUser.objects.order_by('-user__username')
        serializer = DexUserSerializer(dex_users, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized dex_user instance
        """
        dex_user = DexUser.objects.get(user=request.auth.user)
        try:
            serializer = CreateDexUserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            return Response(dex_user.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, pk):
        """Handle PUT requests for a dex_user

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            dex_user = DexUser.objects.get(pk=pk)
            format, imgstr = request.data["profile_image_url"].split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f'{pk}-{uuid.uuid4()}.{ext}')
            dex_user.profile_image_url = data
            dex_user.save()
            
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk):
        dex_user = DexUser.objects.get(pk=pk)
        dex_user.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        
    
class DexUserSerializer(serializers.ModelSerializer):
    """JSON serializer for dex_user
    """
    class Meta:
        model = DexUser
        fields = ('id', 'user', 'bio', 'created_on')
        depth = 1
        
class CreateDexUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DexUser
        fields = ['id', 'bio', 'created_on']