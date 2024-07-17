from django.urls import path
from .views import HouseListingCreate, HouseListingRetrieveUpdate, HouseListingDelete, OtherUsersListingsView, OtherUsersDetailsView
from predictor.views import PredictPrice

urlpatterns = [
    path("listings/", HouseListingCreate.as_view(), name="listing-list"),
    path("listings/<int:pk>/", HouseListingRetrieveUpdate.as_view(), name="listing-detail"),
    path("listings/<int:pk>/delete/", HouseListingDelete.as_view(), name="delete-listing"),
    path('listings/<int:pk>/predict/', PredictPrice.as_view(), name='predict_price'),
    path('other-users-listings/', OtherUsersListingsView.as_view(), name='other_users_listings'),
    path('other-users-listings/<int:pk>/', OtherUsersDetailsView.as_view(), name='other_users_details'),
]