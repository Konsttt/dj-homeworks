from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, ListCreateAPIView, RetrieveDestroyAPIView, \
    RetrieveAPIView
from rest_framework.response import Response

from .models import Measurement, Sensor
from .serializers import SensorSerializer, MeasurementSerializer, SensorDetailSerializer


# ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView, RetrieveDestroyAPIView для таблицы Sensor
class SensorAPIList(ListCreateAPIView):  # GET - все записи, POST - добавить одну запись из json (id автоматически)
    queryset = Sensor.objects.all()      # Как делать POST из списка словарей, пока не нашёл...
    serializer_class = SensorSerializer


class SensorAPIUpdate(RetrieveUpdateAPIView):  # GET, PUT, PATCH - для одной записи, id которой указан в url-запроса
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class SensorAPICreate(CreateAPIView):  # POST - только создать запись. (GET в данном запросе not allowed, 405.)
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class SensorAPIDelete(RetrieveDestroyAPIView):  # DELETE or read single model instance
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


# ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView, RetrieveDestroyAPIView для таблицы Measurement
class MeasurementAPIList(ListCreateAPIView):  # GET - все записи, POST - добавить одну запись
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer


class MeasurementAPIUpdate(RetrieveUpdateAPIView):  # GET, PUT, PATCH - для одной записи, id указан в url-запроса
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer


class MeasurementAPICreate(CreateAPIView):  # POST - только создать запись. (GET в данном запросе not allowed, 405.)
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer


class MeasurementAPIDelete(RetrieveDestroyAPIView):  # DELETE or read single model instance
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer


# Детальная информация по одному датчику
class SensorDetailAPIView(RetrieveAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer