from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.decorators import api_view
from mozio_api.models import ProviderModel, ServiceAreaModel
from mozio_api.serializers import ProviderSerializer, ServiceAreaSerializer
from datetime import datetime
from shapely.geometry import Point, MultiPoint
import math

class Provider(generics.GenericAPIView):
    serializer_class = ProviderSerializer
    queryset = ProviderModel.objects.all()

    def get(self, request):
        page_num = int(request.GET.get("page", 1))
        limit_num = int(request.GET.get("limit", 10))
        start_num = (page_num - 1) * limit_num
        end_num = limit_num * page_num
        search_param = request.GET.get("search")
        providers = ProviderModel.objects.all()
        total_providers = providers.count()
        if search_param:
            providers = providers.filter(name__icontains=search_param)
        serializer = self.serializer_class(providers[start_num:end_num], many=True)
        return Response({
            "status": "success",
            "total": total_providers,
            "page": page_num,
            "last_page": math.ceil(total_providers / limit_num),
            "providers": serializer.data
        })

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "provider": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ProviderDetail(generics.GenericAPIView):
    queryset = ProviderModel.objects.all()
    serializer_class = ProviderSerializer

    def get_provider(self, pk):
        try:
            return ProviderModel.objects.get(pk=pk)
        except:
            return None

    def get(self, request, pk):
        provider = self.get_provider(pk=pk)
        if provider == None:
            return Response({"status": "fail", "message": f"Provider with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(provider)
        return Response({"status": "success", "provider": serializer.data})

    def patch(self, request, pk):
        provider = self.get_provider(pk)
        if provider == None:
            return Response({"status": "fail", "message": f"Provider with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            provider, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.validated_data['updatedAt'] = datetime.now()
            serializer.save()
            return Response({"status": "success", "Provider": serializer.data})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        provider = self.get_provider(pk)
        if provider == None:
            return Response({"status": "fail", "message": f"Provider with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        provider.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ServiceArea(generics.GenericAPIView):
    serializer_class = ServiceAreaSerializer
    queryset = ServiceAreaModel.objects.all()

    def get(self, request):
        page_num = int(request.GET.get("page", 1))
        limit_num = int(request.GET.get("limit", 10))
        start_num = (page_num - 1) * limit_num
        end_num = limit_num * page_num
        search_param = request.GET.get("search")
        serviceArea = ServiceAreaModel.objects.all()
        total_serviceArea = serviceArea.count()
        if search_param:
            serviceArea = serviceArea.filter(name__icontains=search_param)
        serializer = self.serializer_class(serviceArea[start_num:end_num], many=True)
        return Response({
            "status": "success",
            "total": total_serviceArea,
            "page": page_num,
            "last_page": math.ceil(total_serviceArea / limit_num),
            "serviceArea": serializer.data
        })

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "serviceArea": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ServiceAreaDetail(generics.GenericAPIView):
    queryset = ServiceAreaModel.objects.all()
    serializer_class = ServiceAreaSerializer

    def get_serviceArea(self, pk):
        try:
            return ServiceAreaModel.objects.get(pk=pk)
        except:
            return None

    def get(self, request, pk):
        serviceArea = self.get_serviceArea(pk=pk)
        if serviceArea == None:
            return Response({"status": "fail", "message": f"serviceArea with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(serviceArea)
        return Response({"status": "success", "serviceArea": serializer.data})

    def patch(self, request, pk):
        serviceArea = self.get_serviceArea(pk)
        if serviceArea == None:
            return Response({"status": "fail", "message": f"ServiceArea with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            serviceArea, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.validated_data['updatedAt'] = datetime.now()
            serializer.save()
            return Response({"status": "success", "serviceArea": serializer.data})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        serviceArea = self.get_serviceArea(pk)
        if serviceArea == None:
            return Response({"status": "fail", "message": f"ServiceArea with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        serviceArea.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def getPolygon(request):
    polygonList = []
    
    serviceAreaModels = ServiceAreaModel.objects.all()
    serializerClass = ServiceAreaSerializer
    poviderSrClass = ProviderSerializer

    if 'lat' in request.GET and 'lng' in request.GET:
        try:
            lat = float(request.GET['lat'])
            lng = float(request.GET['lng'])
        except Exception as ex:
            return Response({"status": "fail", "message": "You should put correct float values."}, status=status.HTTP_400_BAD_REQUEST )
        serviceAreas = serializerClass(serviceAreaModels, many=True)
        serviceAreas = serviceAreas.data
        for serviceArea in serviceAreas:
            if serviceArea.get("geoJson").get('type') == 'Polygon' :
                # only handling when geoJson type is polygon
                coordinates = serviceArea.get("geoJson").get('coordinates')
                coords = []
                
                try:
                    for coord in coordinates:
                        coords.append(tuple(coord))
                    
                    poly = MultiPoint(coords).convex_hull
                    if Point(lat, lng).intersects(poly):       
                        # check if following point is in the polygon
                        polygonName = serviceArea.get('name')

                        providerName = serviceArea.get("geoJson").get("provider")

                        price = serviceArea.get("price")
                        
                        if providerName:
                            provider = ProviderModel.objects.get(name=providerName)
                            if provider:
                                providerObj = poviderSrClass(provider)
                                providerObj = providerObj.data
                                currency = providerObj.get('currency')
                        
                                polygonList.append({
                                    'polygonName': polygonName,
                                    'providerName': providerName,
                                    'price': currency + str(price)
                                })
                    

                except Exception as ex:
                    print(ex)

        return Response({"status": "success", "polygons": polygonList})
    else:
        message = f"Need lat and lng parameter"
        return Response({"status": "fail", "message": message}, status=status.HTTP_400_BAD_REQUEST )