from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from wallets.models import Withdrawal
from .serializers import WithdrawalSerializer

# Request Withdrawal (POST)
class RequestWithdrawal(APIView):
    def post(self, request, merchant_id):
        data = request.data
        data['merchant_id'] = merchant_id
        serializer = WithdrawalSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# Get All Merchant Withdrawals (GET)
class MerchantWithdrawalsList(generics.ListAPIView):
    serializer_class = WithdrawalSerializer

    def get_queryset(self):
        merchant_id = self.kwargs['merchant_id']
        return Withdrawal.objects.filter(merchant_id=merchant_id)

# Get Specific Withdrawal (GET)
class GetWithdrawalDetail(generics.RetrieveAPIView):
    queryset = Withdrawal.objects.all()
    serializer_class = WithdrawalSerializer
    lookup_url_kwarg = 'withdrawal_id'
