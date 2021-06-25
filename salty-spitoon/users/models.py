import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

from utils.models import TimeStamp

ROLE_CHOICES = (
    ('boss', 'Boss'),
    ('hitman', 'Hitman'),
    ('manager', 'Manager')
)


class User(AbstractUser, TimeStamp):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField('Correo electrónico', unique=True)
    role = models.CharField(
        'rol',
        choices=ROLE_CHOICES,
        default='hitman',
        max_length=10,
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def is_manager(self):
        return self.role in ['manager', 'boss']

    def is_active_user(self):
        return {True: 'ACTIVO', False: 'INACTIVO'}[self.is_active]

    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    class Meta:
        ordering = ('id', 'first_name', 'email')
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'


class ManagerUser(TimeStamp, models.Model):
    manager = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="manager"
    )
    lackey = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="lackey"
    )

    def __str__(self):
        return "{}->{}".format(
            self.manager.get_full_name(),
            self.lackey.get_full_name()
        )
