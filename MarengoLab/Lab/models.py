from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date
# creating the patient model
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
        return self.sample_ID
    
#####################################

class Result(models.Model):
    result_ID = models.AutoField(primary_key=True)
    value = models.IntegerField()
    sample_details = models.ForeignKey(Sample, on_delete=models.CASCADE)
    p_details = models.ForeignKey(Parameter, on_delete=models.CASCADE)


    def __str__(self):
        return self.result_ID,self.value