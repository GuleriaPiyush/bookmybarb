from django.urls import path
from .views import ServiceView,ServiceCreate,assign_templates_to_dates

urlpatterns = [
    # shop owener urls
    path("services/", ServiceView, name="serviceview"),
    path("services/create/",ServiceCreate, name="servicecreate" ),
    path("assign-template/",assign_templates_to_dates, name="assigntemplate" ),

]
