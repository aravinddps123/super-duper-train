"""
django command to wait fo db to be available

"""
import time

from django.db.utils import OperationalError
from psycopg2 import OperationalError as psycopg2_OP_error

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command for wait fo database"""

    def handle(self, *args, **kwargs):
        """Entry point fo the command """
        self.stdout.write("waiting for database to be available")
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (psycopg2_OP_error, OperationalError):
                self.stdout.write(
                    "Database is unavailable ...waiting for 1 second")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
