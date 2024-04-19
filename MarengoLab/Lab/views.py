from django.shortcuts import render, redirect
from django.http import HttpResponseNotAllowed, HttpResponse
from .models import Patient , Group,Parameter, Sample , NormalRange, results
from .forms import RegisterPatientForm
from django.contrib import messages
from django.http import JsonResponse
import json
import requests
import re 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
#from django.core.exceptions import ValidationError
from django.middleware.csrf import get_token
from datetime import datetime
@login_required(login_url='/login')
def home_page(request):
    pending_count = Sample.objects.filter(status='P').count()
    patient_count = Patient.objects.count()
    current_date = datetime.now().date()
    context = {'patient_count': pending_count, 'patient_count':patient_count,'current_date':current_date}
    return render(request,'index.html',context)

def register_patient(request):
    if request.method == 'POST':
        clean_data=False
        form = RegisterPatientForm(request.POST)
        if form.is_valid():
            l_name = form.cleaned_data['l_name']
            f_name = form.cleaned_data['f_name']
            email = form.cleaned_data['email']
            tel_num = form.cleaned_data['tel_num']
            age = form.cleaned_data['age']

            
            # Check if a patient with the same first name and last name already exists
            if Patient.objects.filter(l_name=l_name).exists() and Patient.objects.filter(f_name=f_name).exists():
                clean_data=True
                messages.error(request, 'Patient exists already')
            
            elif not re.match(r"^[A-Za-z]+$", l_name) or  not re.match(r"^[A-Za-z]+$", f_name):
                clean_data=True
                messages.error(request,'invalid name entered, please only use letters')

            elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                clean_data=True
                messages.error(request,'invalid email form')

            elif not re.match(r"^(?:[0-9] ?){6,14}[0-9]$", tel_num):
                clean_data=True
                messages.error(request,'invalid phone number')
            elif not( 0 <= age <= 110):
                clean_data = True 
                messages.error(request,'age should range between 15 and 110 years ')
               
            else:
                # Create and save the new patient
                form.save()
                clean_data=True
                messages.success(request, 'Patient registered successfully!')
                
    else:
        clean_data= False
        form = RegisterPatientForm()
    
    return render(request, 'register_patient.html', {'form': form,'clean_data':clean_data})

def test(request): 
    csrf_token = get_token(request)
    rows = Patient.objects.all()
    return render(request,'test.html',{'rows':rows,'csrf_token':csrf_token})

def delete_patient(request,id):
     
     if request.method == 'DELETE':
        try:
            # Filter the rows per patient_id
            p_details = Patient.objects.get(patient_id=id)
            # check that a patient doesn't have a sample or else dont delete 
            p_sample = Sample.objects.filter(patient_id=id)
            if(p_sample):
                 return HttpResponse("Patient has associated samples and cannot be deleted", status=400)
            else:
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

        if not re.match(r"^[A-Za-z]+$", last_name) or not re.match(r"^[A-Za-z]+$", first_name):
            return JsonResponse({'success': False, 'message': 'Invalid name format'})

        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return JsonResponse({'success': False, 'message': 'Invalid email'})
       
        elif not re.match(r"^(?:[0-9] ?){6,14}[0-9]$", telephone_number):
            return JsonResponse({'success': False, 'message': 'Invalid telephone number'})

        # Age Validation
        elif  not (0 <= int(age) <= 110):
            return JsonResponse({'success': False, 'message': 'Invalid age range'})
        try:
            # Retrieve the model instance based on the rowId
            model_instance = Patient.objects.get(patient_id=id)
            ############# can add some code to check if name of a patient wasnt change to another 
            ################# that way duplicates patients with # id would be avoided 
            
            # Update the model fields with the form data
            model_instance.f_name = first_name
            model_instance.l_name = last_name
            model_instance.age = age
            model_instance.email = email
            model_instance.tel_num = telephone_number
            model_instance.comment = comment
        
            
            # Save the changes to the model instance
            model_instance.save()
            
            # Return a JSON response indicating success
            return JsonResponse({'success': True, 'data':{
                'first_name': model_instance.f_name,
                 'last_name': model_instance.l_name,
                 'age': model_instance.age,
                 'email': model_instance.email,
                 'telephone_number': model_instance.tel_num,
                 'comment': model_instance.comment
            }})
        
        except Patient.DoesNotExist:
            # Return a JSON response indicating failure if the model instance does not exist
            return JsonResponse({'success': False, 'message': 'Model instance does not exist'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    

def Param_list(request):
    parameters_by_group = {}

    # Fetch all parameter groups
    parameter_groups = Group.objects.all()

    for group in parameter_groups:
        # Fetch parameters for each group
        parameters = Parameter.objects.filter(group=group).values('p_name', 'p_unit','param_id')
        parameters_with_ranges = []

        for parameter in parameters:
            # Fetch normal ranges for each parameter
            normal_ranges = NormalRange.objects.filter(parameter=parameter['param_id']).values('gender', 'range_value')

            # Create a dictionary to store the parameter and its normal ranges
            parameter_with_ranges = {
                'parameter': parameter,
                'normal_ranges': normal_ranges
            }

            parameters_with_ranges.append(parameter_with_ranges)

        parameters_by_group[group] = parameters_with_ranges

    context = {
        'parameters_by_group': parameters_by_group
    }

    return render(request, 'Param_list.html', context)


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
        row_added= True
        messages.success(request, 'Sample has been added')
    else:
        row_added = False


    return render(request,'Add_sample.html',{'Patient_data':Patient_data,'Group_data':Group_data, 'row_added':row_added})




def ViewSample(request): 
    csrf_token = get_token(request)
    
    rows = Sample.objects.select_related('patient').all()
    return render(request,'View_Sample.html',{'rows':rows,'csrf_token':csrf_token})



def delete_sample(request,id):
     
     if request.method == 'DELETE':
        try:
            # Filter the rows per sample ID 
           
            ROW=Sample.objects.filter(sample_ID=id).first()
            if ROW:
                if ROW.status == 'D':
                    return HttpResponse("Sample has existing results, cannot be deleted", status=400)
                else:
                    ROW.delete()

          
            # Return a success response
            return HttpResponse(status=204) 
        except Patient.DoesNotExist:
            # If the row doesn't exist, return a not found response
            return HttpResponse(status=404)  # 404 Not Found
     else:
       return HttpResponseNotAllowed(['DELETE'])
    


def update_sample(request):
    if request.method == 'POST':
        # Get the rowId from the POST data
        id = request.POST.get('sample_ID')
        status = request.POST.get('status')
       
        try:
            # Retrieve the model instance based on the rowId
            model_instance = Sample.objects.get(sample_ID=id)
            
            # Update the model fields with the form data
            model_instance.status = status
            
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
    


def ViewResult(request): 
    csrf_token = get_token(request)
    
    rows = results.objects.all()
    

    # Convert the JSON fields to Python objects
    for result in rows:
        result.parameters = json.loads(result.parameters)
        result.values = json.loads(result.values)

    # Pass the results objects to the template context
    context = {
        'rows': rows
    }
    return render(request,'View_Result.html',{'rows':rows,'csrf_token':csrf_token})


def update_result(request):
    if request.method == 'POST':
        # Get the rowId from the POST data
        id = request.POST.get('result_ID')
        print(id)
        KeyVal = request.POST.get('VALUES')
       
        try:
            # Retrieve the model instance based on the rowId
        
            result = results.objects.get(result_ID=id)
        
            
            result.values = KeyVal
            result.save()
            result.values = json.loads(result.values)
            # change the status of the sample linked to the result just updated
            sample = results.objects.filter(result_ID=id).values('sample').first()
            model_instance = Sample.objects.get(sample_ID=sample['sample'])
            if model_instance:
                model_instance.status = 'D'
                model_instance.save()

            
            
            
            
            # Return a JSON response indicating success
            return JsonResponse({'success': True, 'values': result.values})
        
        except Patient.DoesNotExist:
            # Return a JSON response indicating failure if the model instance does not exist
            return JsonResponse({'success': False, 'message': 'Model instance does not exist'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

   

    

def get_prediction(request):
    if request.method == 'POST':
    
        id = request.POST.get('result_ID')
        result = results.objects.get(result_ID=id)
        sample = result.sample
        patient = sample.patient
        patient_age = patient.age
        patient_gender = patient.gender
        keys_to_check = ['hb', 'MCV']
        dicti = json.loads(result.values)
        for key in keys_to_check:
            if dicti.get(key) is None :
                return JsonResponse({'success': False, 'message': f'The value of the parameter {key} is None please enter results first'})
        if int(patient_age) < 15 :
            return JsonResponse({'success': False, 'message': ' Model cannot predict Anemia for a kid '})
        else:

            result.values = json.loads(result.values)
            data = {
            "data": [[float(patient_gender), float(result.values.get('MCV')), float(result.values.get('hb'))]]}
            response = requests.post('http://model:8443/predict', json=data)

        if response.status_code == 200:
            prediction = response.json()["predictions"]
            return JsonResponse({"prediction": prediction})
            #return render(request, 'index.html', {"prediction": prediction})
            
        else:
            return JsonResponse({"error": "Failed to get prediction"}, status=500)
    return render(request,'View_Result.html')



def Login(request):
     csrf_token = get_token(request)
     check = False
     if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('psw')
   


        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('home_page')
            
           
        else:
            check =True
            messages.error(request,'Wrong credentials! Please, try again')


     else:
         pass
     return render(request,'Login.html',{'check':check,'csrf_token':csrf_token})






def Logout(request):
    logout(request)
    return redirect('/login')



