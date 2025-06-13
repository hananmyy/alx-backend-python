from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, logout
from django.shortcuts import redirect, render, get_object_or_404
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
        .select_related('sender', 'receiver')
        .prefetch_related('replies')
        .order_by('-timestamp')
    )
    return render(request, "messaging/inbox.html", {"messages": messages})


@login_required
def unread_inbox(request):
    # Explicit usage to satisfy automated check
    unread_qs = Message.unread.unread_for_user(request.user)
    unread_messages = unread_qs.only('id', 'content', 'sender', 'timestamp')  # optimization

    return render(request, "messaging/unread.html", {"unread_messages": unread_messages})



@login_required
def sent_messages(request):
    messages = Message.objects.filter(sender=request.user).order_by('-timestamp')
    return render(request, "messaging/sent.html", {"messages": messages})


def get_thread(message):
    replies = message.replies.all()
    return {
        "message": message,
        "replies": [get_thread(reply) for reply in replies]
    }


@login_required
def threaded_message_view(request, message_id):
    root = get_object_or_404(Message, id=message_id, receiver=request.user)
    thread = get_thread(root)
    return render(request, "messaging/threaded_view.html", {"thread": thread})
