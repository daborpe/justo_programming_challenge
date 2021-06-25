from django.core.exceptions import PermissionDenied

from .helpers import get_manager_lackeys

allowed_roles = ['boss', 'manager']


class HasRoleMixin(object):
    """
        Check if request.user has his role in allowed_roles
    """

    def dispatch(self, request, *args, **kwargs):
        if request.user.role not in allowed_roles:
            raise PermissionDenied
        return super(HasRoleMixin, self).dispatch(request, *args, **kwargs)


class ManagerAccessMixin(object):
    """
        Restrict access other manager's hitman
    """

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user.role in allowed_roles:
            if request.user.is_superuser or request.user.role == 'boss':
                return super(ManagerAccessMixin, self).get(request, *args, **kwargs)
            if request.user == self.object.hitman:
                return super(ManagerAccessMixin, self).get(request, *args, **kwargs)
            if self.object.hitman not in get_manager_lackeys(request.user):
                raise PermissionDenied
        return super(ManagerAccessMixin, self).get(request, *args, **kwargs)


class HitAssignedMixin(object):
    """
        Only allow hitmen to see their jobs
    """

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user.role == 'hitman':
            if not request.user == self.object.hitman:
                raise PermissionDenied
        return super(HitAssignedMixin, self).get(request, *args, **kwargs)
