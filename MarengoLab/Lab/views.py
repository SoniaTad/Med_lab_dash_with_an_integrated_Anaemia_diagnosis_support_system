from django.shortcuts import render
from django.http import HttpResponseNotAllowed, HttpResponse
from .models import Patient , Group,Parameters, Sample
from .forms import RegisterPatientForm
from django.contrib import messages
from django.http import JsonResponse
#from django.core.exceptions import ValidationError
from django.middleware.csrf import get_token
# Create your views here.
def home_page(request):
    return render(request,'index.html')

def register_patient(request):
    if request.method == 'POST':
        form = RegisterPatientForm(request.POST)
        if form.is_valid():
            l_name = form.cleaned_data['l_name']
            f_name = form.cleaned_data['f_name']
            
            # Check if a patient with the same first name and last name already exists
            if Patient.objects.filter(l_name=l_name).exists() and Patient.objects.filter(f_name=f_name).exists():
                messages.error(request, 'Patient exists already')
               
            else:
                # Create and save the new patient
                form.save()
                messages.success(request, 'Patient registered successfully!')
                
    else:
        form = RegisterPatientForm()
    
    return render(request, 'register_patient.html', {'form': form})

def test(request): 
    csrf_token = get_token(request)
    rows = Patient.objects.all()
    return render(request,'test.html',{'rows':rows,'csrf_token':csrf_token})

def delete_patient(request,id):
     
     if request.method == 'DELETE':
        try:
            # Filter the rows per patient_id
            p_details = Patient.objects.get(patient_id=id)
            # Delete the patient
            p_details.delete()
            # Return a success response
            return HttpResponse(status=204) 
        except Patient.DoesNotExist:
            # If the row doesn't exist, return a not found response
            return HttpResponse(status=404)  # 404 Not Found
     else:
       return HttpResponseNotAllowed(['DELETE'])

def update_patient(request):
    if request.method == 'POST':
        # Get the rowId from the POST data
        id = request.POST.get('id')
        first_name = request.POST.get('First Name')
        last_name = request.POST.get('Last Name')
        age = request.POST.get('Age')
        email = request.POST.get('Email')
        telephone_number = request.POST.get('Telephone number')
        comment = request.POST.get('Comment')
        try:
            # Retrieve the model instance based on the rowId
            model_instance = Patient.objects.get(patient_id=id)
            
            # Update the model fields with the form data
            model_instance.f_name = first_name
            model_instance.l_name = last_name
            model_instance.age = age
            model_instance.email = email
            model_instance.tel_num = telephone_number
            model_instance.comment = comment
            # ... and so on for other fields
            
            # Save the changes to the model instance
            model_instance.save()
            
            # Return a JSON response indicating success
            return JsonResponse({'success': True})
        
        except Patient.DoesNotExist:
            # Return a JSON response indicating failure if the model instance does not exist
            return JsonResponse({'success': False, 'message': 'Model instance does not exist'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    

def Param_list(request):
    groups = Group.objects.all()
    parameters_by_group = {}

    for group in groups:
        parameters = Parameters.objects.filter(group=group).values('p_name').distinct()
        parameters_by_group[group] = parameters

    context = {
        'parameters_by_group': parameters_by_group}
    
    return render(request,'Param_list.html',context)


def Add_Sample(request):
    #this view will get the data from the template , check it then use it to create a row in the sample model 
    #flat is set to true to get a list instead of a list of tuples 
    Patient_data=Patient.objects.values_list('patient_id','l_name','f_name')
    Group_data=Group.objects.values_list('group_name',flat=True)
    if request.method == 'POST':
        p = request.POST['Patient']
        g = request.POST.get('group')
        print(p)
        # for each of my foreign keys I would need to get the data from the main tables depending on p and g values 
        # create an empty instance of sample then allocate the foreign keys values one by one 
        pid = Patient.objects.get(patient_id=p)
        #pid=patient_rows.patient_id
        print(pid)
        Sample_row=Sample()
        Sample_row.patient=pid
        Sample_row.patient_id=pid.patient_id
        group_rows = Group.objects.get(group_name=g)
        Sample_row.group=group_rows
        Sample_row.save()
        ##########################" thinking of changing thid message to have it within another if statement if row was saved "
        messages.success(request, 'Sample has been added')
    else:
        messages.error(request, 'error')


    return render(request,'Add_sample.html',{'Patient_data':Patient_data,'Group_data':Group_data})
    
   

    