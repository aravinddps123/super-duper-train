"""
django command to wait fo db to be available

"""

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """Django command for wait fo database"""
    def handle(self, *args, **kwargs):
        pass