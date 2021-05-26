from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb import settings
from users.models import User

from .permissions import AdminPermission
from .serializers import (ConfirmationCodeSerializer, EmailSerializer,
                          UserSerializer)


@api_view(['POST'])
@permission_classes([AllowAny])
def confirmation_code_sender(request):
    serializer = EmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.data['email']
    username = serializer.data['username']
    user = User.objects.get_or_create(email=email, username=username)[0]
    confirmation_code = default_token_generator.make_token(user)

    send_mail(
        subject='Ваш персональный код от сервиса YamDb',
        from_email=settings.DEFAULT_FROM_EMAIL,
        message=f'Ваш код: {confirmation_code}.',
        recipient_list=[email],
        fail_silently=False,
    )
    return Response(
        {'message': f'Код отправлен на почту: {email}'},
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    serializer = ConfirmationCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.data['email']
    username = serializer.data['username']
    confirmation_code = serializer.data['confirmation_code']
    user = get_object_or_404(User, email=email, username=username)
    if not default_token_generator.check_token(user, confirmation_code):
        return Response(
            {'confirmation_code': 'Неверный код'},
            status=status.HTTP_400_BAD_REQUEST
        )
    token = AccessToken.for_user(user)
    return Response({'token': f'{token}'}, status=status.HTTP_200_OK)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AdminPermission]
    lookup_field = 'username'

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
