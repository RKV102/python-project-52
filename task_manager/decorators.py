from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages


def usage_check_decorator(model, message_text, redirect_url):

    def wrapper(func):

        def inner(*args, **kwargs):
            model_item_id = kwargs['pk']
            model_item = get_object_or_404(model, id=model_item_id)
            request = args[0]
            if model_item.task_set.all():
                messages.error(
                    request,
                    message_text,
                    extra_tags='danger'
                )
                return redirect(redirect_url)
            return func(*args, **kwargs)

        return inner

    return wrapper
