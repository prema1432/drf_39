from django.contrib import admin

from student.models import Student, School, Product, Cart

# Register your models here.
admin.site.register(Student)
admin.site.register(School)
admin.site.register(Product)
admin.site.register(Cart)
