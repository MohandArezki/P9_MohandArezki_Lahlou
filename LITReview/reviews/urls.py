from django.urls import path
from .views import (
    FeedsView,
    PostsView,
    TicketDeleteView,
    TicketUpdateView,
    TicketCreateView,
    ReviewDeleteView,
    ReviewAddView,
    ReviewAddFullView,
    ReviewUpdateView,
    SubscribeView,
)

urlpatterns = [
    # Feeds view for displaying user feeds
    path("feeds", FeedsView.as_view(), name="feeds"),

    # Posts view for displaying user posts
    path("posts", PostsView.as_view(), name="posts"),

    # Delete ticket view with dynamic primary key
    path("delete-ticket/<int:pk>/", TicketDeleteView.as_view(), name="delete-ticket"),

    # Update ticket view with dynamic primary key
    path("update-ticket/<int:pk>/", TicketUpdateView.as_view(), name="update-ticket"),

    # Create new ticket view
    path("add-ticket/", TicketCreateView.as_view(), name="add-ticket"),

    # Add a response to a review with dynamic primary key
    path("add-review-response/<int:pk>/", ReviewAddView.as_view(), name="add-review-response"),

    # Add a complete review with all fields
    path("add-review-full/", ReviewAddFullView.as_view(), name="add-review-full"),

    # Update review view with dynamic primary key
    path("update-review/<int:pk>/", ReviewUpdateView.as_view(), name="update-review"),

    # Delete review view with dynamic primary key
    path("delete-review/<int:pk>/", ReviewDeleteView.as_view(), name="delete-review"),

    # Subscribe view for user subscriptions
    path("subscribe/", SubscribeView.as_view(), name="subscribe"),
]
