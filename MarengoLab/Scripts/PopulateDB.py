from django.core.management.base import BaseCommand
import django
import sys
import os
projectDirectory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(projectDirectory)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MarengoLab.settings')
django.setup()
from Lab.models import Group, Parameter, NormalRange
class Command(BaseCommand):
    help = 'Populate models'

    def handle(self, *args, **options):
        # Create groups
        group1, _ = Group.objects.get_or_create(group_name='hematology')
        group2, _ = Group.objects.get_or_create(group_name='hormonology')

        # Create parameters
        param1, _ = Parameter.objects.get_or_create(p_name='hb', p_unit='g/dl', group=group1)
        param2, _ = Parameter.objects.get_or_create(p_name='MCV', p_unit='fl', group=group1)
        param3, _ = Parameter.objects.get_or_create(p_name='vit D', p_unit='UI', group=group2)

        # Create normal ranges
        NormalRange.objects.get_or_create(parameter=param1, gender='0', range_value='13-17')
        NormalRange.objects.get_or_create(parameter=param1, gender='1', range_value='12-15')
        NormalRange.objects.get_or_create(parameter=param2, gender='0', range_value='80-100')
        NormalRange.objects.get_or_create(parameter=param2, gender='1', range_value='80-100')
        NormalRange.objects.get_or_create(parameter=param3, gender='0', range_value='35-50')
        NormalRange.objects.get_or_create(parameter=param3, gender='1', range_value='25-45')

        self.stdout.write(self.style.SUCCESS('Models populated successfully.'))