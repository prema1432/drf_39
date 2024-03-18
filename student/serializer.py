from rest_framework import serializers

from student.models import Student, School


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = "__all__"


class SchoolSerializerGET(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ["id", "name"]


class StudentSerializer(serializers.ModelSerializer):
    # school = SchoolSerializerGET()
    school_name = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = "__all__"
        # depth = 1

    def get_school_name(self, obj):
        # return obj.school.name if obj.school else "No School Name"
        return obj.school.name if obj.school else None
