from .models import Notification

def notifications_count(request):
    if request.user.is_authenticated:
        return {
            "notif_count": Notification.objects.filter(user=request.user, seen=False).count()
        }
    return {"notif_count": 0}
