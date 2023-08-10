from django import forms
from django_starfield import Stars
from .models import Ticket, Review, UserFollow


class TicketForm(forms.ModelForm):
    """
    Form for creating or updating a ticket.

    Attributes:
        title (str): The title of the ticket.
        description (str): The description of the ticket.
        image (ImageField): An image associated with the ticket.
    """
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]


class ReviewForm(forms.ModelForm):
    """
    Form for creating a review.

    Attributes:
        rating (IntegerField): The rating given in the review, represented as stars.
        headline (str): A headline for the review.
        body (str): The body of the review.
    """
    rating = forms.IntegerField(widget=Stars)

    class Meta:
        model = Review
        fields = ["headline", "rating", "body"]


class SubscribeForm(forms.ModelForm):
    """
    Form for subscribing to a user's updates.

    Attributes:
        followed_user (ForeignKey): The user to follow for updates.
    """
    class Meta:
        model = UserFollow
        fields = ["followed_user"]
