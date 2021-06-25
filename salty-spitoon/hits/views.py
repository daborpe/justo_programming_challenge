from django.views.generic import ListView, CreateView, UpdateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q

from extra_views import ModelFormSetView

from utils.helpers import get_manager_lackeys, get_hitman_choices
from utils.mixins import HasRoleMixin, HitAssignedMixin, ManagerAccessMixin

from .models import Hit
from .forms import HitCreateForm, HitUpdateForm, HitListBulkForm


class HitCreate(LoginRequiredMixin, HasRoleMixin, CreateView):
    model = Hit
    template_name = 'hits/hit_create.html'
    form_class = HitCreateForm
    success_url = reverse_lazy('hits:list')

    def get_form_kwargs(self):
        kwargs = super(HitCreate, self).get_form_kwargs()
        kwargs.update({'current_user': self.request.user})
        return kwargs

    def form_invalid(self, form):
        messages.error(self.request, 'Revisa los errores del formulario')
        return super(HitCreate, self).form_invalid(form)

    def form_valid(self, form):
        # Check if hitman is same logged in user
        if form.instance.hitman == self.request.user:
            form.add_error('hitman', 'No puedes asignarte un golpe a ti mismo')
            return self.form_invalid(form)
        form.instance.requester = self.request.user
        messages.success(self.request, 'Golpe creado correctamente')
        return super(HitCreate, self).form_valid(form)


class HitUpdate(
    LoginRequiredMixin,
    ManagerAccessMixin,
    HitAssignedMixin,
    UpdateView
):
    model = Hit
    template_name = 'hits/hit_update.html'
    form_class = HitUpdateForm
    success_url = reverse_lazy('hits:list')

    def get_form_kwargs(self):
        kwargs = super(HitUpdate, self).get_form_kwargs()
        kwargs.update({'current_user': self.request.user})
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super(HitUpdate, self).get_context_data(*args, **kwargs)
        # Ugly way to check if a job is assigned to a manager user
        context.update({
            'hitman_is_manager': context['object'].hitman_is_manager(
                self.request.user
            )
        })
        return context

    def form_invalid(self, form):
        messages.error(self.request, 'Revisa los errores del formulario')
        return super(HitUpdate, self).form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, 'Golpe actualizado correctamente')
        return super(HitUpdate, self).form_valid(form)


class HitList(LoginRequiredMixin, ListView):
    model = Hit
    template_name = 'hits/hit_list.html'

    def get_queryset(self):
        if self.request.user.role == 'manager':
            qs = self.model.objects.filter(
                Q(hitman=self.request.user) | Q(hitman__in=get_manager_lackeys(
                    self.request.user)
                )
            ).order_by('-hitman')
        elif self.request.user.role == 'hitman':
            qs = self.model.objects.filter(
                hitman=self.request.user
            )
        else:
            qs = self.model.objects.all()
        return qs


class HitListBulk(LoginRequiredMixin, HasRoleMixin, ModelFormSetView):
    model = Hit
    template_name = 'hits/hit_bulk.html'
    factory_kwargs = {'extra': 0}
    form_class = HitListBulkForm

    def construct_formset(self):
        formsets = super(HitListBulk, self).construct_formset()
        # Handle hitman options according to request.user role
        if not self.request.user.role == 'boss':
            for formset in formsets:
                formset.fields['hitman'].widget.choices = get_hitman_choices(
                    self.request.user
                )
        return formsets

    def get_success_url(self):
        return reverse_lazy('hits:list')

    def get_queryset(self):
        if self.request.user.role == 'manager':
            qs = self.model.objects.filter(
                hitman__in=get_manager_lackeys(self.request.user),
                status='assigned'
            )
        else:
            qs = self.model.objects.filter(status='assigned')
        return qs

    def formset_invalid(self, formset):
        messages.error(self.request, 'Revisa tus campos')
        return super(HitListBulk, self).formset_invalid(formset)

    def formset_valid(self, formset):
        messages.success(self.request, 'Cambios realizados correctamente')
        return super(HitListBulk, self).formset_valid(formset)
