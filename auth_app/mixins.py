from django.http import HttpResponseRedirect
from django.shortcuts import redirect

class UserIsProfileOwner(object):
    def dispatch(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.id != self.request.user.id:
            prev_page = request.META.get('HTTP_REFERER')
            if prev_page:
                return HttpResponseRedirect(prev_page)
            else:
                return redirect('/')
        return super().dispatch(request, *args, **kwargs)