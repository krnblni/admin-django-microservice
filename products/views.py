from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from products.models import Product, User
from products.producer import publish
from products.serializers import ProductSerializer
import random


class ProductViewSet(viewsets.ViewSet):
    def list(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish(method='product_created', body=serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def update(self, request, pk=None):
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(instance=product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish(method='product_updated', body=serializer.data)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        product = Product.objects.get(id=pk)
        product.delete()
        publish(method='product_deleted', body=pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserAPIView(APIView):
    def get(self, _):
        users = User.objects.all()
        user = random.choice(users)
        return Response({
            'id': user.id
        })
