from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Company, Representante
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CompanySerializer, RepresentanteSerializer
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test


def is_admin_or_superuser(user):
    return user.is_superuser or user.is_staff


@method_decorator(login_required, name="dispatch")
@method_decorator(
    user_passes_test(is_admin_or_superuser, login_url="/accounts/home/"),
    name="dispatch",
)
class CompanyListView(APIView):
    def get(self, request, format=None):
        companies = Company.objects.all()
        return render(request, "company/company_list.html", {"object_list": companies})


@method_decorator(login_required, name="dispatch")
@method_decorator(
    user_passes_test(is_admin_or_superuser, login_url="/accounts/home/"),
    name="dispatch",
)
class CompanyCreateView(APIView):

    def get(self, request, format=None):
        serializer = CompanySerializer()
        representantes = Representante.objects.all()
        return render(
            request,
            "company/company_novo.html",
            {"form": serializer, "representantes": representantes},
        )

    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect("company-list")
        else:
            representantes = Representante.objects.all()
            return render(
                request,
                "company/company_novo.html",
                {"form": serializer, "representantes": representantes},
            )


class CompanyUpdateView(APIView):

    def get(self, request, pk, format=None):
        company = Company.objects.get(pk=pk)
        serializer = CompanySerializer(instance=company)
        representantes = Representante.objects.all()
        return render(
            request,
            "company/company_editar.html",
            {"form": serializer, "representantes": representantes, "company": company},
        )

    def post(self, request, pk):
        company = Company.objects.get(pk=pk)
        serializer = CompanySerializer(instance=company, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect("company-list")
        else:
            representantes = Representante.objects.all()
            return render(
                request,
                "company/company_editar.html",
                {
                    "form": serializer,
                    "representantes": representantes,
                    "company": company,
                },
            )


class RepresentanteListView(APIView):
    def get(self, request, format=None):
        representantes = Representante.objects.all()
        return render(
            request,
            "representante/representante_list.html",
            {"object_list": representantes},
        )


class RepresentanteCreateView(APIView):

    def get(self, request, format=None):
        serializer = RepresentanteSerializer()
        return render(
            request, "representante/representante_novo.html", {"form": serializer}
        )

    def post(self, request):
        serializer = RepresentanteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect("representante-list")
        else:
            return render(
                request, "representante/representante_novo.html", {"form": serializer}
            )


class RepresentanteUpdateView(APIView):

    def get(self, request, pk, format=None):
        representante = Representante.objects.get(pk=pk)
        serializer = RepresentanteSerializer(instance=representante)
        return render(
            request,
            "representante/representante_editar.html",
            {"form": serializer, "representante": representante},
        )

    def post(self, request, pk):
        representante = Representante.objects.get(pk=pk)
        serializer = RepresentanteSerializer(instance=representante, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect("representante-list")
        else:
            return render(
                request,
                "representante/representante_editar.html",
                {"form": serializer, "representante": representante},
            )


class CompanyDeleteView(APIView):

    def post(self, request, pk):
        try:
            company = Company.objects.get(pk=pk)
            company.delete()
            return redirect("company-list")
        except Company.DoesNotExist:
            return redirect("company-list")


class RepresentanteDeleteView(APIView):

    def post(self, request, pk):
        try:
            representante = Representante.objects.get(pk=pk)
            representante.delete()
            return redirect("representante-list")
        except Representante.DoesNotExist:
            return redirect("representante-list")
