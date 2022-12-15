from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from measurement.views import SensorAPIList, SensorAPIUpdate, SensorAPICreate, SensorAPIDelete, MeasurementAPIList,\
    MeasurementAPICreate, MeasurementAPIUpdate, MeasurementAPIDelete, SensorDetailAPIView

urlpatterns = [
    path('sensor/', SensorAPIList.as_view()),
    path('sensor/<pk>/', SensorAPIUpdate.as_view()),
    path('sensor_create/', SensorAPICreate.as_view()),
    path('sensor_del/<pk>/', SensorAPIDelete.as_view()),
    path('measurement/', MeasurementAPIList.as_view()),
    path('measurement/<pk>/', MeasurementAPIUpdate.as_view()),
    path('measurement_create/', MeasurementAPICreate.as_view()),
    path('measurement_del/<pk>/', MeasurementAPIDelete.as_view()),
    path('sensor_detail/<pk>/', SensorDetailAPIView.as_view())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
