from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import UserSerializer
from predictor.serializers import HouseListingSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from predictor.models import HouseListing
from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.
# class UserDetailsView(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         serializer = self.get_serializer(request.user)
#         return Response(serializer.data)

class CreateUserView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = [AllowAny]

class DeleteUserView(generics.DestroyAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = [IsAuthenticated]

  def delete(self, request, *args, **kwargs):
    user = self.request.user
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

class UserRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        print("Request data:", request.data)
        print("Request FILES:", request.FILES)
        
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

class HouseListingCreate(generics.ListCreateAPIView):
  serializer_class = HouseListingSerializer
  permission_classes = [IsAuthenticated]

  def get_queryset(self):
    user = self.request.user
    return HouseListing.objects.filter(author=user) # returns all listings created by the user
  
  def perform_create(self, serializer):
        try:
            serializer.save(author=self.request.user)
        except Exception as e:
            print(f"Error creating listing: {e}")
            raise e

class HouseListingRetrieveUpdate(generics.RetrieveUpdateAPIView):
    serializer_class = HouseListingSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
      user = self.request.user
      return HouseListing.objects.filter(author=user)
    
    def retrieve(self, request, *args, **kwargs):
      instance = self.get_object()
      serializer = self.get_serializer(instance)
      return Response(serializer.data)

    def update(self, request, *args, **kwargs):
      partial = kwargs.pop('partial', False)
      instance = self.get_object()
      serializer = self.get_serializer(instance, data=request.data, partial=partial)
      serializer.is_valid(raise_exception=True)
      self.perform_update(serializer)

      if getattr(instance, '_prefetched_objects_cache', None):
          instance._prefetched_objects_cache = {}

      return Response(serializer.data)

    def perform_update(self, serializer):
      serializer.save()
  
class HouseListingDelete(generics.DestroyAPIView):
  serializer_class = HouseListingSerializer
  permission_classes = [IsAuthenticated]

  def get_queryset(self):
    user = self.request.user
    return HouseListing.objects.filter(author=user) # returns all listings created by the user
  
class OtherUsersListingsView(generics.ListAPIView):
    serializer_class = HouseListingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return HouseListing.objects.exclude(author=user)

class OtherUsersDetailsView(generics.RetrieveAPIView):
    serializer_class = HouseListingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return HouseListing.objects.exclude(author=user)
    
    def get(self, request, *args, **kwargs):
        listing_id = kwargs.get('pk')
        queryset = self.get_queryset()
        try:
            listing = queryset.get(id=listing_id)
            serializer = self.get_serializer(listing)
            return Response(serializer.data)
        except HouseListing.DoesNotExist:
            return Response({"error": "Listing not found"}, status=status.HTTP_404_NOT_FOUND)
    