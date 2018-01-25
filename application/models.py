import uuid

from django.db import models
from user.models import Base, User

APPLICATION_STATUS = (('Applied', 'Applied'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected'))


class Applications(Base):

    name = models.CharField(max_length=255)
    app_ref_no = models.CharField(max_length=255, null=True, blank=True)
    dob = models.DateField()
    email = models.EmailField()
    phone_no = models.CharField(max_length=20, null=True, blank=True)
    phone_code = models.CharField(max_length=20, default='+91')
    resume = models.FileField()
    skills = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, choices=APPLICATION_STATUS, default='Applied')
    status_changed_by = models.CharField(max_length=255, null=True, blank=True)
    status_changed_at = models.DateTimeField(null=True, blank=True)

    class Meta:

        db_table = 'applications'
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'

    def __str__(self):
        return "{} - {}".format(self.name, self.status)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.app_ref_no = uuid.uuid4().hex[:6].upper()
        return super().save(*args, **kwargs)
