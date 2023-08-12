from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import UpdateView, CreateView, TemplateView, DeleteView
from itertools import chain
from django.db.models import Value, CharField
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth.models import User
from .models import Ticket, Review, UserFollow
from .forms import TicketForm, ReviewForm, SubscribeForm


class BaseFeedsView(View):
    """
    Base view for handling feeds and posts.
    """
    def get_data(self, users=None):
        """
        Get feeds/posts data for the provided users.
        """
        if users is None:
            users = []

        tickets = Ticket.objects.filter(user__in=users).annotate(
            content_type=Value("TICKET", CharField())
        )
        reviews = Review.objects.filter(user__in=users).annotate(
            content_type=Value("REVIEW", CharField())
        )
        return sorted(
            chain(reviews, tickets), key=lambda feeds: feeds.time_created, reverse=True
        )

    def get_paginator(self, data, per_page=5):
        """
        Get a paginator for the provided data.
        """
        paginator = Paginator(data, per_page)
        page = self.request.GET.get("page")
        try:
            paginated_data = paginator.page(page)
        except PageNotAnInteger:
            paginated_data = paginator.page(1)
        except EmptyPage:
            paginated_data = paginator.page(paginator.num_pages)
        return paginated_data


class FeedsView(LoginRequiredMixin, BaseFeedsView):
    """
    View for displaying user feeds.
    """
    def get(self, request):
        followed_users = UserFollow.objects.filter(user=request.user)
        users = [followed_user.followed_user for followed_user in followed_users]
        users.append(request.user)
        feeds = self.get_data(users)
        paginated_feeds = self.get_paginator(feeds, per_page=5)
        return render(
            request,
            "reviews/feeds.html",
            context={"feeds": paginated_feeds, "title": "Feeds"},
        )


class PostsView(LoginRequiredMixin, BaseFeedsView):
    """
    View for displaying user posts.
    """
    def get(self, request):
        users = [request.user]
        posts = self.get_data(users)
        paginated_posts = self.get_paginator(posts, per_page=5)
        return render(
            request,
            "reviews/feeds.html",
            context={"feeds": paginated_posts, "title": "Posts"},
        )


class TicketDeleteView(View):
    """
    View for confirming and deleting a ticket.
    """
    template_name = "reviews/confirm_delete.html"

    def get(self, request, pk):
        ticket_instance = get_object_or_404(Ticket, pk=pk, user=request.user)
        context = {
            "type": "TICKET",
            "title": "Delete a Ticket",
            "confirm_message": "Are you sure you want to delete this ticket?",
            "posts": ticket_instance,
        }
        return render(request, self.template_name, context=context)

    def post(self, request, pk):
        # make sure it's the right ticket before deleting (Ticket + Current User)
        ticket_instance = get_object_or_404(Ticket, pk=pk, user=request.user)
        ticket_instance.delete()
        return redirect("posts")


class TicketUpdateView(UpdateView):
    """
    View for updating a ticket.
    """
    model = Ticket
    form_class = TicketForm
    template_name = "reviews/ticket_form.html"

    def get_object(self, queryset=None):
        """
        Get the ticket object based on the provided primary key.
        """
        pk = self.kwargs.get("pk")        
        # make sure it's the right ticket before updating (Ticket + Current User)
        ticket_instance = get_object_or_404(Ticket, pk=pk, user=self.request.user)
        return ticket_instance

    def get_context_data(self, **kwargs):
        """
        Get additional context data for the template.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = "Update - Ticket"
        return context

    def get_success_url(self):
        """
        Get the URL to redirect after a successful update.
        """
        return reverse("posts")


class TicketCreateView(CreateView):
    """
    View for creating a new ticket.
    """
    model = Ticket
    form_class = TicketForm
    template_name = "reviews/ticket_form.html"

    def get_context_data(self, **kwargs):
        """
        Get additional context data for the template.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = "Create - Ticket"
        return context

    def form_valid(self, form):
        """
        Process the form data and assign the current user to the ticket.
        """
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """
        Get the URL to redirect after a successful creation.
        """
        next_page = self.request.GET.get('next')
        if next_page:
            return reverse(next_page)
        else:
            return reverse('feeds')


class ReviewAddView(CreateView):
    """
    View for adding a new review.
    """
    def get(self, request, pk):
        """
        Display the review form for adding a new review.
        """
        ticket_instance = get_object_or_404(Ticket, pk=pk)
        context = {
            "type": "response",
            "ticket": ticket_instance,
            "r_form": ReviewForm(),
            "title": "New Review"
        }
        return render(request, "reviews/review_form.html", context)

    def post(self, request, pk):
        """
        Process the review form data and create a new review.
        """
        ticket_instance = get_object_or_404(Ticket, pk=pk)
        r_form = ReviewForm(request.POST)
        if r_form.is_valid():
            Review.objects.create(
                ticket=ticket_instance,
                user=request.user,
                headline=request.POST["headline"],
                rating=request.POST["rating"],
                body=request.POST["body"],
            )
            messages.success(request, "Your review has been posted!")
            return redirect(self.get_success_url())

        context = {
            "type": "response",
            "ticket": ticket_instance,
            "r_form": ReviewForm(),
            "title": "New Review"
        }
        return render(request, "reviews/review_form.html", context)

    def get_success_url(self):
        """
        Get the URL to redirect after a successful review submission.
        """
        next_page = self.request.GET.get('next')
        if next_page:
            return reverse(next_page)
        else:
            return reverse('feeds')


class ReviewAddFullView(View):
    """
    View for adding a full review including a ticket.
    """
    def get(self, request):
        context = {"type": "full", "t_form": TicketForm(), "r_form": ReviewForm(), "title": "New Review"}
        return render(request, "reviews/review_form.html", context)

    def post(self, request):
        t_form = TicketForm(request.POST, request.FILES)
        r_form = ReviewForm(request.POST)

        if t_form.is_valid() and r_form.is_valid():
            # Create a new ticket and associated review
            image = None
            t = Ticket.objects.create(
                user=request.user,
                title=request.POST["title"],
                description=request.POST["description"],
                image=image,
            )
            t.save()
            Review.objects.create(
                ticket=t,
                user=request.user,
                headline=request.POST["headline"],
                rating=request.POST["rating"],
                body=request.POST["body"],
            )
            messages.success(request, "Your review has been posted!")
            return redirect("feeds")

        context = {"type": "full", "t_form": t_form, "r_form": r_form, "title": "New Review"}
        return render(request, "reviews/review_form.html", context)


class ReviewUpdateView(UpdateView):
    """
    View for updating a review.
    """
    model = Review
    template_name = "reviews/review_form.html"
    form_class = ReviewForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = "response"
        context["ticket"] = self.object.ticket
        context["title"] = "Update Review"
        context["r_form"] = self.get_form()
        return context

    def get_object(self, queryset=None):
        """
        Get the review object based on the provided primary key.
        """
        pk = self.kwargs.get("pk")
        # make sure it's the right review before updating (Review + Current User)
        review_instance = get_object_or_404(Ticket, pk=pk, user=self.request.user)
        return review_instance

    def get_success_url(self):
        return reverse("posts")


class ReviewDeleteView(DeleteView):
    """
    View for deleting a review.
    """
    model = Review
    template_name = "reviews/confirm_delete.html"

    def get_object(self, queryset=None):
        pk = self.kwargs.get("pk")
        # make sure it's the right review before updating (Review + Current User)
        review_instance = get_object_or_404(Ticket, pk=pk, user=self.request.user)        
        return review_instance

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        review_instance = self.get_object()
        context.update({
            "type": "REVIEW",
            "title": "Delete a Review",
            "confirm_message": "Are you sure you want to delete this review?",
            "review": review_instance,
        })
        return context

    def get_success_url(self):
        return reverse("posts")


class SubscribeView(LoginRequiredMixin, TemplateView):
    """
    View for subscribing and unsubscribing to/from users.
    """
    template_name = "reviews/subscribe.html"
    title = "Subscriptions"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_follows = UserFollow.objects.filter(user=self.request.user).order_by(
            "followed_user"
        )
        followed_by = UserFollow.objects.filter(
            followed_user=self.request.user
        ).order_by("user")
        context["form"] = SubscribeForm()
        context["user_follows"] = user_follows
        context["followed_by"] = followed_by
        context["title"] = self.title
        return context

    def post(self, request, *args, **kwargs):
        form = SubscribeForm(request.POST)
        action = request.POST.get("action")

        if form.is_valid():
            followed_user = form.cleaned_data["followed_user"]
            try:
                followed_user = User.objects.get(pk=followed_user.id)
                if request.user == followed_user:
                    messages.error(request, "You can't subscribe/unsubscribe to/from yourself!")
                else:
                    if action == "subscribe":
                        try:
                            UserFollow.objects.create(
                                user=request.user, followed_user=followed_user
                            )
                            messages.success(
                                request, f"You have subscribed to {followed_user.username}!"
                            )
                        except IntegrityError:
                            messages.error(
                                request, f"Already following {followed_user.username}!"
                            )
                    elif action == "unsubscribe":
                        try:
                            follow = UserFollow.objects.get(
                                user=request.user, followed_user=followed_user
                            )
                            follow.delete()
                            messages.success(
                                request, f"You have unsubscribed from {followed_user.username}!"
                            )
                        except UserFollow.DoesNotExist:
                            messages.error(
                                request, f"You were not following {followed_user.username}!"
                            )
            except User.DoesNotExist:
                messages.error(request, f"User {followed_user.username} does not exist")

        return redirect("subscribe")
