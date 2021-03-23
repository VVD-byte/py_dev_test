from rest_framework.views import APIView, Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.db import IntegrityError

from .models import PurseUser, Transactions
from .serializer import PurseSerializer, TransactionsSerializer


def help(func):
    def wrap(*args, **kwargs):
        try:
            return Response(func(*args, **kwargs))
        except Exception as e:
            return Response({'error': 'Ошибка данных'})
    return wrap


class RegUser(APIView):
    @help
    def post(self, request):
        dat = [request.query_params.get('username', None), request.query_params.get('email', None),
               request.query_params.get('password', None)]
        if None not in dat:
            if User.objects.filter(email=dat[1]).exists():
                return {'error': 'email занят'}
            if User.objects.filter(username=dat[0]).exists():
                return {'error': 'username занят'}
            try:
                User.objects.create_user(dat[0], dat[1], dat[2])
                return {'create_user': True}
            except IntegrityError as e:
                return {'error': f'username {dat[0]} занят'}
            except:
                return {'error': 'Ошибка данных'}
        else:
            return {'error': 'Ошибка данных'}


class Purse(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @help
    def get(self, request):
        # добавить фильтрацию по name
        return PurseSerializer(PurseUser.objects.filter(user__username=request.user), many=True).data

    @help
    def post(self, request):
        ser = PurseSerializer(data={'user': request.user,
                              'name': request.query_params.get('name', None), 'money': 0})
        if ser.is_valid():
            ser.save()
            return {'create': True}
        else:
            return {'error': ser.errors}

    @help
    def put(self, request):
        dat = PurseUser.objects.filter(user=User.objects.filter(username=request.user).first().id,
                                       id=request.query_params.get('id', None)).first()
        ser = PurseSerializer(dat, data={'name':request.query_params.get('new_name', None),
                                         'money': dat.money,
                                         'user': dat.user})
        if ser.is_valid():
            ser.save()
            return {'update': True}
        else:
            return {'error': ser.errors}

    @help
    def delete(self, request):
        dat = PurseUser.objects.filter(user=User.objects.filter(username=request.user).first().id,
                                       id=request.query_params.get('id', None)).first()
        if dat.money != 0:
            return {'error': 'Невозможно удалить. Не нулевой баланс'}
        if dat:
            dat.delete()
            return {'delete': True}
        else:
            return {'error': 'Кошелек не найден'}


class Transact(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @help
    def get(self, request):
        if not request.query_params.get('purse', None) is None:
            dat = Transactions.objects.filter(purse__user=request.user.id,
                                              purse__id=request.query_params.get('purse', None))
        else:
            dat = Transactions.objects.filter(purse__user=request.user.id)
        ser = TransactionsSerializer(dat, many=True)
        return ser.data

    @help
    def post(self, request):
        purse_id = int(request.query_params.get('purse', None))
        money = int(request.query_params.get('money', None))
        comment = request.query_params.get('comment', None)
        if None in [purse_id, money]:
            return {'error': 'error data'}
        pur = PurseUser.objects.filter(id=purse_id, user=request.user.id).first()
        if pur:
            if pur.money + money > 0:
                pur.money += money
                try:
                    Transactions(purse=pur, money=money, comment=comment).save()
                    pur.save()
                except ValueError:
                    return {'error': 'Счет не найден'}
                except:
                    return {'error': 'Невозможно создать транзакцию'}
            else:
                return {'error': 'Недостаточно денег'}
        else:
            return {'error': 'Не найден счет'}
        return {'add_trans': True}

    @help
    def delete(self, request):
        dat = Transactions.objects.filter(id=request.query_params.get('trans_id', None)).first()
        dat.delete()
        return {'delete': True}
