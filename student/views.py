from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from student.models import Student
from student.serializer import StudentSerializer


# Create your views here.

class StudentAPI(APIView):
    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
