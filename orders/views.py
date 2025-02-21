from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser
from rest_framework.pagination import PageNumberPagination
from .models import Order
from .serializers import OrderSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

class OrderPagination(PageNumberPagination):
    page_size = 10  # Number of orders per page
    page_size_query_param = 'page_size'
    max_page_size = 100

class OrderViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]
    pagination_class = OrderPagination  # Adding pagination
    
    
    def retrieve(self, request, pk=None):
        order = self.get_object()
        serializer = self.get_serializer(order)
        return Response({
            'status': 'True',
            'message': 'order retrieved successfully.', 
            'data': serializer.data
            }, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        try:
            order = self.get_object()
            serializer = self.get_serializer(order, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                'status': 'True',
                'message': 'Order status updated successfully.'
                }, status=status.HTTP_200_OK)
        
        except ValidationError as e:
            return Response({
                'status': 'False',
                'message': "Invalid data provided",
                }, status=status.HTTP_400_BAD_REQUEST)
        
        except Order.DoesNotExist:
            return Response({
                'status': 'False',
                'message': 'Order not found. Please check the order ID.'
                }, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({
                'status': 'False',
                'message': 'An unexpected error occurred.', 
                'data': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)