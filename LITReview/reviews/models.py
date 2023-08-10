from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class UserFollow(models.Model):
    """
    Model representing a user following another user.

    Attributes:
        user (ForeignKey): The user who is following.
        followed_user (ForeignKey): The user being followed.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    followed_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followed_by"
    )

    class Meta:
        verbose_name = "User Follow"
        verbose_name_plural = "User Follows"
        unique_together = ("user", "followed_user")

    def __str__(self):
        return f"{self.user.username} |---> {self.followed_user.username}"


class Ticket(models.Model):
    """
    Model representing a ticket.

    Attributes:
        title (str): The title of the ticket.
        description (str): The description of the ticket.
        user (ForeignKey): The user who created the ticket.
        time_created (DateTimeField): The timestamp when the ticket was created.
        image (ImageField): An image associated with the ticket.
    """
    title = models.CharField(max_length=128, verbose_name="Title")
    description = models.TextField(
        max_length=2048, blank=True, verbose_name="Description"
    )
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    time_created = models.DateTimeField(default=timezone.now)
    image = models.ImageField(
        blank=True, null=True, upload_to="img/reviews")

    @property
    def is_closed(self):
        return hasattr(self, "review")

    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"

    def __str__(self):
        return f"Ticket ( {self.title} )"


class Review(models.Model):
    """
    Model representing a review for a ticket.

    Attributes:
        ticket (OneToOneField): The ticket associated with the review.
        rating (PositiveSmallIntegerField): The rating given in the review.
        headline (str): A headline for the review.
        body (str): The body of the review.
        user (ForeignKey): The user who created the review.
        time_created (DateTimeField): The timestamp when the review was created.
    """
    ticket = models.OneToOneField(to=Ticket, on_delete=models.CASCADE, unique=True)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="Note"
    )
    headline = models.CharField(max_length=128, verbose_name="Comment")
    body = models.TextField(max_length=8192, blank=True, verbose_name="Review")
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    time_created = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    def __str__(self):
        return f"Review ( {self.headline} )"
