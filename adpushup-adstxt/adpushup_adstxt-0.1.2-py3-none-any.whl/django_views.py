# -*- coding: utf-8 -*-
from .utils import get_ads_txt, authenticate, set_ads_txt
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json

from .django_settings import API_KEY, API_USER_ID, WWW_DIR


@csrf_exempt
def handle(request):

    if request.method == "GET":
        if request.GET.get("test", False):
            return HttpResponse(
                json.dumps(dict(status=1, status_message="connected to api")),
                content_type="application/json",
            )
        else:
            code, content = get_ads_txt(WWW_DIR)
            return HttpResponse(content, content_type="application/json", status=code)

    elif request.method == "POST":
        data = request.POST.get("data", None)
        hash = request.POST.get("hash", None)
        ts = request.POST.get("ts", None)
        if data and hash and ts:
            if authenticate(hash, ts, API_USER_ID, API_KEY):
                code, content = set_ads_txt(WWW_DIR, data)
                return HttpResponse(
                    content, content_type="application/json", status=code
                )
            return HttpResponse(
                json.dumps(
                    dict(
                        status=0,
                        status_message="Authentication failed. Can not update ads.txt",
                    )
                ),
                content_type="application/json",
                status=400,
            )

        HttpResponse(
            json.dumps(dict(status=0, status_message="Request not proper")),
            content_type="application/json",
            status=400,
        )

    return HttpResponse("Bad request", status=500)
