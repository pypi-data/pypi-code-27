# Django
from django.db import models


class DBLogEntry(models.Model):
    """
    Model to store logs
    """

    log_levels = (
        ('NOTSET', 'NotSet'),
        ('INFO', 'Info'),
        ('WARNING', 'Warning'),
        ('DEBUG', 'Debug'),
        ('ERROR', 'Error'),
        ('FATAL', 'Fatal'),
    )

    level = models.CharField(choices=log_levels, max_length=10, db_index=True)
    message = models.TextField()
    trace = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('-created_on', )
        app_label = 'db_logger'
