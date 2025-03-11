def notifications(request):
    current_user = request.user
    if current_user.is_authenticated:
        return {'notifications': current_user.notifications_user.all()}
    else:
        return {'notifications': []}
