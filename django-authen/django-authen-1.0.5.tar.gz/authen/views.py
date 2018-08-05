from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings


def login_view(request):
    if request.method == "GET":
        ctx = {
            "company_name": settings.AUTHEN["COMPANY_NAME"],
            "login_title": settings.AUTHEN["LOGIN_TITLE"],
        }
        return render(request, "authen/login.html", ctx)
    else:
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)

        user = authenticate(request, username=username, password=password)

        if not user:
            return JsonResponse({"isValid": False, "payload": "<strong>Invalid credentials</strong>"})

        login(request, user)

        return JsonResponse({"isValid": True, "payload": user.username})


@login_required
def logout_view(request):
    logout(request)

    ctx = {
        "company_name": settings.AUTHEN["COMPANY_NAME"],
        "logout_title": settings.AUTHEN["LOGOUT_TITLE"],
        "logout_message": settings.AUTHEN["LOGOUT_MESSAGE"],
    }

    return render(request, "authen/logout.html", ctx)

