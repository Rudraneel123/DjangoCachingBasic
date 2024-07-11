from django.shortcuts import render
from .serializers import ItemSerializer
from .models import Item
from django.core.cache import cache
from rest_framework import viewsets,status
from rest_framework.response import Response

# Create your views here.
class ItemViewSet(viewsets.ViewSet):
  def list(self, request):
      try:
        cached_items = cache.get('items')
        if cached_items:
            return Response(cached_items)

        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        cache.set('items', serializer.data, timeout=60*5)  # Cache for 5 minutes
        return Response(serializer.data)
      except Exception as e:
          return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
  def create(self, request):
   try:
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete('items')  # Invalidate the cached list
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
   except Exception as e:
        return Response(serializer.errors,{'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
