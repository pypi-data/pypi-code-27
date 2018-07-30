from django.core.management.base import BaseCommand
from dj_pysher.application import PysherApplication

class Command(BaseCommand):

    help = "Whatever you want to print here"

    def handle(self, *args, **options):
        app = PysherApplication()
        app.main()