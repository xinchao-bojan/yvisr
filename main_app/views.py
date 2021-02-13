from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from .models import *
from .permissions import *


# class CustomPagination(PageNumberPagination):
#     page_size = 50
#     max_page_size = 30


class CustomUserListView(generics.ListAPIView):
    permission_classes = [IsStaff]
    queryset = CustomUser.objects.filter(is_admin=False, is_staff=False).order_by('-rating_points', 'last_name',
                                                                                  'first_name')
    serializer_class = CustomUserSerializer


class RecordListView(generics.ListAPIView):
    permission_classes = [IsStaff]
    queryset = Record.objects.order_by('confirmed', '-value')
    serializer_class = RecordSerializer


class OwnRecordListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Record.objects.order_by('confirmed')
    serializer_class = RecordSerializer

    def get(self, request):
        queryset = Record.objects.filter(owner=request.user).order_by('confirmed')
        serializer = RecordSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)


class RecordDetailView(APIView):
    permission_classes = [IsStaff]

    def get(self, request, pk):
        serializer = RecordSerializer(Record.objects.get(pk=pk), context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        r = Record.objects.get(pk=pk)
        r.confirmed = request.data['confirmed']
        r.value = request.data['value']
        r.judge = request.user
        r.save()
        serializer = RecordSerializer(r, context={'request': request})
        return Response(serializer.data)

    def delete(self, request, pk):
        r = Record.objects.get(pk=pk).delete()
        serializer = RecordSerializer(r, context={'request': request})
        return Response(serializer.data)


class AddRecordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = CustomUserSerializer(CustomUser.objects.filter(is_staff=True), context={'request': request},
                                          many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            j = CustomUser.objects.filter(is_staff=True).get(email=request.data['judge'])
        except CustomUser.DoesNotExist:
            j = CustomUser.objects.get(pk=1)
        r, created = Record.objects.get_or_create(owner=request.user,
                                                  title=request.data['title'],
                                                  judge=j)
                                                # proof=request.data['proof'], )
        serializer = RecordSerializer(r, context={'request': request})
        return Response(serializer.data)


class HireStaffView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        try:
            cu = CustomUser.objects.get(email=request.data['email'])
        except CustomUser.DoesNotExist:
            return Response('CustomUser.DoesNotExist')
        cu.is_staff = request.data['position'] == 'staff'
        cu.is_admin = request.data['position'] == 'admin'
        cu.save()
        serializer = CustomUserSerializer(cu, context={'request': request})
        return Response(serializer.data)


class FireStaffView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        cu = CustomUser.objects.get(email=request.data['email'])
        cu.is_staff = False
        cu.is_admin = False
        cu.save()
        serializer = CustomUserSerializer(cu, context={'request': request})
        return Response(serializer.data)
