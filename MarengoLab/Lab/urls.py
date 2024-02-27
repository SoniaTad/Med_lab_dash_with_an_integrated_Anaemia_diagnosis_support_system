from django.urls import path 
from . import views 
from django.views.generic import RedirectView
urlpatterns =[
    path('',views.home_page,name='home_page'),
    path('register',views.register_patient),
    path('test',views.test),
    #path('ViewResult',views.ViewResult, name='ViewResult'),
    path('delete/<int:id>/',views.delete_patient),
    path('update-patient/',views.update_patient,name='update'),
    path('viewParam',views.Param_list),
    path('addSample',views.Add_Sample),
    path('ViewSample',views.ViewSample),
    path('Delete/<int:id>/',views.delete_sample),
    
    path('update-sample/',views.update_sample),
    path('update-result/',views.update_result),
  
     path('ViewResult/', RedirectView.as_view(url='/ViewResult')),
    path('ViewResult', views.ViewResult, name='ViewResult'),
    path('get_prediction', views.get_prediction, name='getPrediction'),
    # Other URL patterns


    
]