from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Company
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CompanySerializer

class CompanyListView(ListView):
    model = Company
    template_name = 'company/company_list.html'

class CompanyCreateView(APIView):

    def get(self, request, format=None):
        serializer = CompanySerializer()
        return render(request, 'company/company_register.html', {'company': serializer})

    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
