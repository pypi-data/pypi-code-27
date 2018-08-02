from django.shortcuts import render, redirect, render_to_response
from django.views import generic
from qb.models import *
from qb.features import *

# Create your views here.
class PageView(generic.TemplateView):
    """ Single page view functions """
    template_name = 'qb/index.html'
    def get(self, request, node=False):
        context = self.get_context_data()

        # check enabled features
        ft = Features()
        context["features"] = ft.getft_queryset('sample')

        return render(request, self.template_name, context)


