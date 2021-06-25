from django.contrib.auth.views import LoginView
from django.contrib.auth import REDIRECT_FIELD_NAME, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic import (
    CreateView,
    UpdateView,
    RedirectView,
    ListView,
)
from django.views.decorators.debug import sensitive_post_parameters
from django.urls import reverse_lazy

from utils.mixins import HasRoleMixin
from utils.helpers import get_manager_lackeys

from .forms import RegisterForm, UpdateUserForm
from .models import ManagerUser, User


@method_decorator(sensitive_post_parameters('password'), name='dispatch')
@method_decorator(csrf_protect, name='dispatch')
@method_decorator(never_cache, name='dispatch')
class LoginView(LoginView):
    redirect_authenticated_user = True
    redirect_field_name = REDIRECT_FIELD_NAME
    success_url = reverse_lazy('hits:list')
    template_name = 'users/login.html'

    def form_invalid(self, form):
        messages.error(self.request, 'Datos incorrectos o usuario desactivado')
        return super(LoginView, self).form_invalid(form)

    def form_valid(self, form):
        if form.get_user().is_active:
            login(self.request, form.get_user())
            return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        redirect_to = self.request.POST.get(self.redirect_field_name)
        if not is_safe_url(url=redirect_to, allowed_hosts=self.request.get_host()):
            redirect_to = self.success_url
        return redirect_to


class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = reverse_lazy('users:login')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def get_title(self):
        return 'Registrar usuario'

    def set_username(self, user):
        """
            Assign a username based on first_name, last_name and email
        """
        username = "{}{}.{}".format(
            user.first_name,
            user.last_name,
            user.email.split('@')[0]
        )
        return username.lower()

    def form_valid(self, form):
        user = form.save(commit=False)
        user.username = self.set_username(user)
        messages.success(self.request, 'Usuario registrado correctamente')
        return super(RegisterView, self).form_valid(form)


class ManagerUserList(LoginRequiredMixin, HasRoleMixin, ListView):
    model = ManagerUser
    template_name = 'users/manageruser_list.html'

    def get_queryset(self):
        if self.request.user.role == 'manager':
            qs = self.model.objects.filter(
                lackey__in=get_manager_lackeys(
                    self.request.user
                )
            )
        else:
            qs = self.model.objects.all()
        return qs


class ManagerUserUpdate(LoginRequiredMixin, HasRoleMixin, UpdateView):
    model = User
    template_name = 'users/manageruser_update.html'
    form_class = UpdateUserForm
    success_url = reverse_lazy('users:list')

    def form_valid(self, form):
        if form.has_changed():
            messages.success(self.request, 'Status de sicario actualizado')
        return super(ManagerUserUpdate, self).form_valid(form)
