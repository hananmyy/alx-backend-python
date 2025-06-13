from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, logout
from django.shortcuts import redirect, render
from django.http import HttpResponseForbidden
from .models import Message
from django.views.decorators.cache import cache_page


User = get_user_model()

@login_required
def delete_user(request):
    if request.method == "POST":
        user = request.user
        logout(request)
        user.delete()
    return HttpResponseForbidden("Invalid request method.")


@cache_page(60) # Cache this view for 60 seconds

@login_required
def inbox(request):
    messages = (
        Message.objects
        .filter(receiver=request.user, parent_message__isnull=True)
        .select_related('sender')
        .prefetch_related('replies')
        .order_by('-timestamp')
    )
    return render(request, "messaging/inbox.html", {"messages": messages})


@login_required
def unread_inbox(request):
    unread_messages = Message.unread.unread_for_user(request.user)
    return render(request, "messaging/unread.html", {"unread_messages": unread_messages})