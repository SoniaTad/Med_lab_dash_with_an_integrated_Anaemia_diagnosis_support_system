from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date
from django.db.models.signals import post_save
from django.dispatch import receiver
import json

# creating the patient models
class Patient(models.Model):
    Gender_type=[('0','Male'),('1','Female')]
    patient_id =models.AutoField(primary_key=True)
    f_name = models.CharField(max_length=100)
    l_name = models.CharField(max_length=100)
    age = models.IntegerField()
    validators=[
            MinValueValidator(0),
            MaxValueValidator(100)]
    gender = models.CharField(max_length=1, choices=Gender_type)
    email = models.EmailField()
    tel_num = models.CharField(max_length=15)
    comment = models.TextField(null=True)
    

    def __str__(self):
        return self.f_name

class Group(models.Model):
    group_ID = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=100)
    

    def __str__(self):
        return self.group_name


class Parameter(models.Model):
    param_id = models.AutoField(primary_key=True)
    p_name = models.CharField(max_length=100)
    p_unit = models.CharField(max_length=50)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)


    def __str__(self):
        return self.p_name
    
class NormalRange(models.Model):
    GENDER_CHOICES = [
        ('0', 'Male'),
        ('1', 'Female'),
    ]
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE,db_column='param_id')
    gender=models.CharField(max_length=1, choices=GENDER_CHOICES,default='0')
    range_value = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['parameter', 'gender'], name='composite_pk'),
        ]
    def __str__(self) :
        return self.range_value





class Sample(models.Model):
    PENDING = 'P'
    DONE = 'D'
    status_choice = [
        (PENDING, 'Pending'),
        (DONE, 'Done'),
    ]
    sample_ID = models.AutoField(primary_key=True)
    date = models.DateField(default=date.today)
    status = models.CharField(max_length=1,choices=status_choice,default=PENDING,null=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE,to_field='patient_id')
    group = models.ForeignKey(Group, on_delete=models.CASCADE,to_field='group_ID')

   

    def __str__(self):
        return str(self.sample_ID)
    
#####################################

class results(models.Model):
    result_ID = models.AutoField(primary_key=True)
    values = models.JSONField(null=True) 
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    parameters = models.JSONField(null=True)


    def __str__(self):
        
        result_str = str(self.result_ID)
         # Check the type of the result_str variable
        return result_str
    
    
@receiver(post_save, sender=Sample)
def create_result(sender, instance, created, **kwargs):
    if created:
        # Retrieve the parameters from the Parameter table based on the sample type
        parameters = Parameter.objects.filter(group=instance.group)
        result = results.objects.create(sample=instance)
        
        # Create the parameters dictionary
        parameters_dict = {}
        values_dict = {}
        for parameter in parameters:
            # Retrieve the unit from the Parameter model
            unit = parameter.p_unit
            
            # Retrieve the normal range based on the parameter and gender
            normal_range = NormalRange.objects.get(parameter=parameter, gender=instance.patient.gender)
            
            # Create the parameter dictionary with name, unit, and normal range
            parameter_dict = {
                'name': parameter.p_name,
                'unit': unit,
                'normal_range': normal_range.range_value,
            }
            
            # Add the parameter dictionary to the parameters dictionary
            parameters_dict[parameter.p_name] = parameter_dict
            
            # Add the parameter name to the values dictionary with a None value
            values_dict[parameter.p_name] = None
        
        # Convert the parameters and values dictionaries to JSON
        parameters_json = json.dumps(parameters_dict)
        values_json = json.dumps(values_dict)
        
        # Set the parameters and values fields of the Result instance
        result.parameters = parameters_json
        result.values = values_json
        result.save()
        