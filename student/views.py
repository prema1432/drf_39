from django.http import Http404
from django.shortcuts import render
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from student.models import Student, School, Cart
from student.serializer import StudentSerializer, SchoolSerializer

from rest_framework import status, serializers


# Create your views here.

class StudentAPI(APIView):
    # authentication_classes = [BasicAuthentication]  # this basic authentication
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        # if request.user.roles == "admin:"
        students = Student.objects.all().order_by('-id')
        # elif request.user.roles == "customer":
        #     students = Student.objects.filter(user=request.user)
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentDetail(APIView):

    def get_object(self, pk):
        try:
            return Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        # student = Student.objects.get(pk=pk)
        student = self.get_object(pk)
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    def put(self, request, pk):
        student = self.get_object(pk)
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        student = self.get_object(pk)
        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        student = self.get_object(pk)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SchoolAPI(APIView):
    def get(self, request):
        schools = School.objects.all()
        serializer = SchoolSerializer(schools, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SchoolSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, pk):
        try:
            return School.objects.get(pk=pk)
        except School.DoesNotExist:
            return None

    def put(self, request):
        if not "id" in request.data:
            return Response({"status": "id field not present in the payload"}, status=status.HTTP_400_BAD_REQUEST)
        get_id = request.data.get("id")

        if type(get_id) != int:
            return Response({"status": "id field not a number"}, status=status.HTTP_400_BAD_REQUEST)

        school = self.get_object(get_id)
        if school == None:
            return Response({"status": "Id not present in the database"}, status=status.HTTP_404_NOT_FOUND)
        serializer = SchoolSerializer(school, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# crud == Create Read Update Delete
#
# student== get,post,put,patch,delete
# get- all
# post -
#
# get - id
# put -
# patch - id
# delete -di

# one product ==
# Rice -Quantity : 5kg ,10kg, 30kg, 50kg
# Shirt -size : S, M, L, XL
#     colour : R, G,B
#
#
# Cart - Rice -20 kg, Shirt S (2), Rice 5kg(4)
#
#
# order --


class GetTokenAPI(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


"""SEND OTP API."""


#
# from PremaDjango.response_handlers.custom_response_handlre import CustomResponseHandler
# from rest_framework.permissions import AllowAny
# from rest_framework.views import APIView
# from rest_framework_simplejwt.tokens import RefreshToken
# from user_agents import parse
#
# from commonapp.models.sending_otp_data_model import SendingOTPDataModel
# from commonapp.models.user_login_history import LoginHistory
# from commonapp.models.wallet_model import Wallet
# from user.models import User
# from utils.helpers.unique_number_genaration import generate_customer_username
#
#
# class CustomerVerifyOTP(APIView):
#     """Customer Verify OTP API."""
#
#     permission_classes = [AllowAny]
#
#     def post(self, request):
#         """Handle POST requests and return a successful response with a message."""
#         data = request.data
#         session_key = data.get("session_key", None)
#
#         if not session_key:
#             return CustomResponseHandler().bad_request_400("session_key is required.")
#         if not data.get("otp_number", None):
#             return CustomResponseHandler().bad_request_400("otp_number is required")
#
#         if not SendingOTPDataModel.objects.filter(otp_session_key=session_key).exists():
#             return CustomResponseHandler().bad_request_400("Invalid session key.")
#         get_otp_data = SendingOTPDataModel.objects.get(otp_session_key=session_key)
#         if get_otp_data.otp_verified:
#             return CustomResponseHandler().bad_request_400("OTP has already been verified.")
#         if not get_otp_data.get_otp == data.get("otp_number", ""):
#             return CustomResponseHandler().bad_request_400("Invalid OTP number.")
#
#         # get_otp_data.otp_verified = True
#         # get_otp_data.save()
#         new_user = False
#         if User.objects.filter(phone_number=get_otp_data.phone_number, is_customer=True).exists():
#             user = User.objects.filter(is_customer=True).get(phone_number=get_otp_data.phone_number)
#         else:
#             new_user = True
#             user = User()
#             user.username = generate_customer_username()
#             user.phone_number = get_otp_data.phone_number
#             user.is_customer = True
#             user.is_active = True
#             user.set_password("BALA@2024#123")
#             user.save()
#
#         refresh = RefreshToken.for_user(user)
#         Wallet.objects.get_or_create(customer_id=user.id)
#         create_login_history_task(user.id, "LOGIN", request)
#
#         response_data = {}
#         response_data["new_user"] = new_user
#         response_data["id"] = user.id
#         response_data["username"] = user.username
#         response_data["phone_number"] = user.phone_number
#         response_data["name"] = user.name
#         response_data["email"] = user.email
#         response_data["is_customert"] = user.is_customer
#         response_data["refresh"] = str(refresh)
#         response_data["access"] = str(refresh.access_token)
#         return CustomResponseHandler().success_200("OTP Verified successfully.", data=response_data)
#
#
# def create_login_history_task(user_id, auth_type, request):
#     """
#     Create a login history task for the given user with the provided authentication type and request information.
#
#     Parameters:
#     - user_id (int): The ID of the user.
#     - auth_type (str): The type of authentication used.
#     - request (HttpRequest): The HTTP request object containing user information.
#
#     Returns:
#     - None
#     """
#     ua_string = request.headers.get("user-agent", "")
#     user_agent = parse(ua_string)
#
#     LoginHistory.objects.create(
#         user_id=user_id,
#         auth_type=auth_type,
#         user_data={
#             "ip": request.META.get("REMOTE_ADDR", None),
#             "user_agent": ua_string,
#             "country": request.headers.get("cf-ipcountry", None),
#             "city": request.headers.get("cf-ipcity", None),
#             "region": request.headers.get("cf-ipregion", None),
#             "isp": request.headers.get("x-original-computername", None),
#             "user_agent_browser": user_agent.browser,
#             "user_agent_browser_family": user_agent.browser.family,
#             "user_agent_browser_version": user_agent.browser.version,
#             "user_agent_browser_version_string": user_agent.browser.version_string,
#             "user_agent_os": user_agent.os,
#             "user_agent_os_family": user_agent.os.family,
#             "user_agent_os_version": user_agent.os.version,
#             "user_agent_os_version_string": user_agent.os.version_string,
#             "user_agent_device": user_agent.device,
#             "user_agent_device_family": user_agent.device.family,
#             "user_agent_device_brand": user_agent.device.brand,
#             "user_agent_device_model": user_agent.device.model,
#             "user_agent_mobile": user_agent.is_mobile,
#             "user_agent_tablet": user_agent.is_tablet,
#             "user_agent_touch_capable": user_agent.is_touch_capable,
#             "user_agent_pc": user_agent.is_pc,
#             "user_agent_bot": user_agent.is_bot,
#         },
#     )
#
# """SEND OTP API."""
#
# import random
# import uuid
#
# from PremaDjango.response_handlers.custom_response_handlre import CustomResponseHandler
# from rest_framework.permissions import AllowAny
# from rest_framework.views import APIView
#
# from commonapp.models.sending_otp_data_model import SendingOTPDataModel
#
#
# class UserSendOTP(APIView):
#     """User Send OTP API."""
#
#     permission_classes = [AllowAny]
#
#     def post(self, request):
#         """Handle POST requests and return a successful response with a message."""
#         data = request.data
#         phone_number = data.get("phone_number", None)
#
#         if not phone_number:
#             return CustomResponseHandler().bad_request_400("phone_number is required.")
#         phone_number = str(phone_number)
#         if not (isinstance(phone_number, str) and phone_number.isdigit() and len(phone_number) == 10 and phone_number[0] in ["6", "7", "8", "9"]):
#             return CustomResponseHandler().bad_request_400("Invalid phone number format.")
#
#         generate_otp = random.randrange(111111, 999999, 6)
#         data["phone_number"] = phone_number
#         data["otp_number"] = generate_otp
#         data["session_key"] = uuid.uuid4()
#         SendingOTPDataModel.objects.create_otp_data(data["phone_number"], generate_otp, data["session_key"], "success")
#
#         return CustomResponseHandler().success_200("OTP sent successfully.", data=data)

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"
        depth = 2


class CartAPI(APIView):
    def get(self, request):
        cart = Cart.objects.all()
        serializer = CartSerializer(cart, many=True)
        cart_total_price = 0
        cart_total_price_with_discount = 0
        savings = 0
        data = serializer.data
        # print("data",data)
        for item in data:
            print("iteemmmmm", item["product"])

            cart_total_price_with_discount = item["product"]["price"] * item["quantity"] + cart_total_price_with_discount

        # cart_total_price_with_discount = cart_total_price_with_di
        # return Response(serializer.data)
        return Response(
            {
                "data": data,
                "cart_total_price": cart_total_price,
                "cart_total_price_with_discount": cart_total_price_with_discount,
                "savings": savings
            }
        )
