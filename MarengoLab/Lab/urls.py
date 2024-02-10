from django.urls import path 
from . import views 
urlpatterns =[
    path('',views.home_page,name='home_page'),
    path('register',views.register_patient),
    path('test',views.test),
    path('delete/<int:id>/',views.delete_patient),
    path('update-patient/',views.update_patient,name='update'),
    path('viewParam',views.Param_list),
    path('addSample',views.Add_Sample),
    path('ViewSample',views.ViewSample),
    path('Delete/<int:id>/',views.delete_sample),
    path('update-sample/',views.update_sample)
]