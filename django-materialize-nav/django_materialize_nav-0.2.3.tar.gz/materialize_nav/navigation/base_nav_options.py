from dynamicmethod import dynamicmethod


__all__ = ['BaseNavOptions']


class BaseNavOptions(object):
    @dynamicmethod
    def get_context(self, request, context=None, *,
                    notification=None, notification_classes=None, notification_time=None,
                    **kwargs):
        if context is None:
            context = {}

        if notification is None:
            try:
                notification = request.session['notification']
                del request.session['notification']
            except KeyError:
                pass

        if notification_classes is None:
            try:
                notification_classes = request.session['notification_classes']
                del request.session['notification_classes']
            except KeyError:
                pass

        if notification_time is None:
            try:
                notification_time = request.session['notification_time']
                del request.session['notification_time']
            except KeyError:
                pass

        context['previous_page'] = request.META.get("HTTP_REFERER", '/')
        context['notification'] = notification
        context['notification_classes'] = notification_classes
        context['notification_time'] = notification_time

        # Force the request to be in the context
        if "request" not in context:
            context['request'] = request

        # Notify that the nav context was loaded
        request.nav_context_loaded = True

        return context
