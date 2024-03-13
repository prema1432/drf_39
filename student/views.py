from django.http import Http404
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from student.models import Student
from student.serializer import StudentSerializer

from rest_framework import status
# Create your views here.

class StudentAPI(APIView):
    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class StudentDetail(APIView):

    def get_object(self,pk):
        try:
            return Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            raise Http404


    def get(self, request, pk):
        # student = Student.objects.get(pk=pk)
        student = self.get_object(pk)
        serializer = StudentSerializer(student)
        return Response(serializer.data)

#
# student== get,post,put,patch,delete
# get- all
# post -
#
# get - id
# put -
# patch - id
# delete -di
