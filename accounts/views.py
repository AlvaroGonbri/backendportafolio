from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status



from .serializers import GroupSerializer, UserSerializer, ChangePasswordSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.DjangoModelPermissions]

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.DjangoModelPermissions]

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            # Verifica la contraseña actual
            if not user.check_password(serializer.validated_data.get('old_password')):
                return Response(
                    {"old_password": ["Contraseña actual incorrecta."]},
                    status=status.HTTP_400_BAD_REQUEST
                )
            # Asigna la nueva contraseña
            user.set_password(serializer.validated_data.get('new_password'))
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ChangeOtherPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, user_id):
        # Verifica si el usuario actual pertenece al grupo "passwordsmanagers"
        if not request.user.groups.filter(name='passwordsmanagers').exists():
            return Response(
                {"detail": "No tienes permiso para cambiar la contraseña de otros usuarios."},
                status=status.HTTP_403_FORBIDDEN
            )
        # Obtiene el usuario objetivo
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"detail": "Usuario no encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data.get('new_password'))
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
