from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from .forms import CsRegisterForm
from django.views.generic import CreateView
from . models import User
from django.contrib import messages


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            request.session['username'] = username
            login(request, user)
            return redirect("gshsapp:home")

    return render(request, "login/login.html")

def logout_view(request):
    logout(request)
    return redirect("login:login")


class CsRegisterView(CreateView):
    model = User
    template_name = 'login/register_cs.html'
    form_class = CsRegisterForm

    # def get(self, request, *args, **kwargs):
    #     if not request.session.get('agreement', False):
    #         raise PermissionDenied
    #     request.session['agreement'] = False
    #     return super().get(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, "회원가입 성공.")
        return redirect('login:login')

    def form_valid(self, form):
        self.object = form.save()
        return redirect(self.get_success_url())
