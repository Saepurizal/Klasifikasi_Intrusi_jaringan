from django.contrib import admin
from django.urls import path
from app.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", signin, name="signin"),
    path("data/", data, name="data"),
    path("addnew/", addnew, name="addnew"),
    path("edit/<int:id>", edit, name="edit"),
    path("update/<int:id>", update, name="update"),
    path("delete/<int:id>", destroy, name="destroy"), 
    path('process_csv/', process_csv, name='process_csv'),
    path('index/', index, name="index"),
    path('signup/', signup, name="signup"),
    path('signout/', signout, name="signout"),
    path("perform-detection/", perform_detection, name="perform_detection"),
]
