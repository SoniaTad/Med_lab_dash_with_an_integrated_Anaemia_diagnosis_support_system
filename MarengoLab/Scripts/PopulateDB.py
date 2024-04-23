from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import django
import sys
import os
projectDirectory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(projectDirectory)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MarengoLab.settings')
django.setup()
from Lab.models import Group, Parameter, NormalRange



def handle():
        
        username1="SONIA"
        ps1="STAFF1234"
        supuname="ADMIN"
        ps2="ADMIN1234"
        #create a superuser(admin):
        User = get_user_model()
    
        if not User.objects.filter(username=supuname).exists():
            user = User.objects.create_superuser(
                username=supuname,
                password=ps2,
            )
            print("created successfully.")
        else:
            print('user exists')
        #creating a regular user 
        User = get_user_model()
        if not User.objects.filter(username=username1).exists():
            user2 = User.objects.create_user(
                username=username1,
                password=ps1,
              
            )
            print("created successfully.")
        else:
            print('user exists')
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

        print('done')



# Add script
if __name__ == '__main__':
    handle()