from django.db import models
from django.db.models import Q

from users.models import User
from utils.models import TimeStamp

HITSTATUS_CHOICES = (
    ('assigned', 'ASIGNADO'),
    ('failed', 'FALLADO'),
    ('completed', 'COMPLETADO'),
)


class Hit(TimeStamp, models.Model):
    hitman = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="hitman",
        limit_choices_to=Q(is_active=True) & Q(role__in=['hitman', 'manager'])
    )
    target = models.CharField('Objetivo', max_length=100)
    description = models.TextField('Descripción')
    status = models.CharField(
        'Status',
        max_length=10,
        choices=HITSTATUS_CHOICES,
        default='assigned'
    )
    requester = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="requester",
    )

    def __str__(self):
        return self.hitman.get_full_name()

    def get_status_text(self):
        return dict(HITSTATUS_CHOICES)[self.status]

    def hitman_is_manager(self, manager):
        return self.hitman == manager
