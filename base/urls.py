from django.urls import path
from . import views

app_name='base'
urlpatterns = [
    path("",views.home,name='home'),
    path("onlyAdmin/",views.onlyAdmin,name='onlyAdmin'),
    path("tierOne/",views.tierOne,name='tierOne'),
    path("tierTwo/",views.tierTwo,name='tierTwo'),
    path("tierThree/",views.tierThree,name='tierThree'),
    path("loginPage/",views.loginPage,name='loginPage'),
    path("regPage/",views.regPage,name='regPage'),
    path("createGroups/",views.createGroups,name='createGroups'),
    path("logoutPage/",views.logoutPage,name='logoutPage'),
]

