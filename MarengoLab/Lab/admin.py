from django.contrib import admin
from .models import Patient,Parameter,Group,Sample,NormalRange
# Register your models here.
class PatientAdmin(admin.ModelAdmin):
  list_display = ("patient_id", "l_name", "f_name",)
admin.site.register(Patient,PatientAdmin)

###############################################
class ParametersAdmin(admin.ModelAdmin):
  list_display = ( "p_unit", "p_name",)
admin.site.register(Parameter,ParametersAdmin)

#################################################

class NormalRangeAdmin(admin.ModelAdmin):
  list_display=("parameter","gender","range_value",)
admin.site.register(NormalRange,NormalRangeAdmin)

##################################################

class GroupAdmin(admin.ModelAdmin):
  list_display = ("group_ID", "group_name",)
admin.site.register(Group,GroupAdmin)


####################################################
class SampleAdmin(admin.ModelAdmin):
  list_display = ("sample_ID", "get_patient","status","group","date")
  # added this line to change the field of patient used on the admin side . 
  def get_patient(self,object):
    return object.patient.l_name
admin.site.register(Sample,SampleAdmin)