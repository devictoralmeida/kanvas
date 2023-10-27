from rest_framework.generics import CreateAPIView
from accounts.models import Account
from accounts.serializers import AccountSerializer
from drf_spectacular.utils import extend_schema


class CreateAccountView(CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    @extend_schema(
        description="Rota para criação de usuários",
        tags=["Criação de usuários"],
        parameters=[
            AccountSerializer,
        ],
    )
    def post(self, request):
        return self.create(request)
