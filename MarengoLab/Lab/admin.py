from django.contrib import admin
from .models import Patient,Parameters,Group,Sample
# Register your models here.
class PatientAdmin(admin.ModelAdmin):
  list_display = ("patient_id", "l_name", "f_name",)
admin.site.register(Patient,PatientAdmin)

###############################################
class ParametersAdmin(admin.ModelAdmin):
  list_display = ("p_name", "p_unit", "p_normalRange",)
admin.site.register(Parameters,ParametersAdmin)

#################################################

class GroupAdmin(admin.ModelAdmin):
  list_display = ("group_ID", "group_name",)
admin.site.register(Group,GroupAdmin)


####################################################
class SampleAdmin(admin.ModelAdmin):
  list_display = ("sample_ID", "get_patient","status","group","date")
  def get_patient(self,object):
    return object.patient.l_name
admin.site.register(Sample,SampleAdmin)