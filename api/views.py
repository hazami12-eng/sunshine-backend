from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

from .models import ContactMessage
from .serializers import RegisterSerializer, UserSerializer, ContactMessageSerializer


class RegisterView(generics.CreateAPIView):
    """POST /api/auth/register/"""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class MeView(APIView):
    """GET /api/auth/me/  — returns logged-in user profile"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class ContactCreateView(generics.CreateAPIView):
    serializer_class = ContactMessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)

        # Send email notification
        try:
            send_mail(
                subject=f'New Contact Form Submission from {instance.name}',
                message=f'''
New message from the Sunshine Multi Plus mobile app:

Name:    {instance.name}
Email:   {instance.email}
Message:
{instance.message}

Submitted at: {instance.created_at}
                ''',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_RECEIVER_EMAIL],
                fail_silently=False,
            )
        except Exception as e:
            # Don't fail the API if email fails
            print(f'Email send error: {e}')


class ContactListView(generics.ListAPIView):
    """GET /api/contact/  — list own messages"""
    serializer_class = ContactMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ContactMessage.objects.filter(user=self.request.user)