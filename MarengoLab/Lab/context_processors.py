from .models import Patient, Sample
from datetime import datetime
def patient_count(request):
    pending_count = Sample.objects.filter(status='P').count()
    patient_count = Patient.objects.count()
    current_date = datetime.now().date()
    context= {'pending_count': pending_count, 'patient_count':patient_count,'current_date':current_date}
    return context
