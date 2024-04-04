import csv

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Company
from .serializers import CompanySerializer
from django_filters.rest_framework import DjangoFilterBackend

from django.utils.deprecation import MiddlewareMixin


class DisableCSRFMiddleware(MiddlewareMixin):
    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'

    @csrf_exempt
    @action(detail=False, methods=['post'])
    def import_csv(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        fieldnames = ['company_code', 'name', 'domain', 'year_founded', 'industry', 'size_range', 'locality', 'country',
                      'linkedin_url', 'current_employee_estimate', 'total_employee_estimate']

        try:
            decoded_file = file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file, fieldnames=fieldnames)
            next(reader)
            companies_created = 0
            for row in reader:
                Company.objects.create(**row)
                companies_created += 1

            return Response({'message': f'{companies_created} companies imported successfully'},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
