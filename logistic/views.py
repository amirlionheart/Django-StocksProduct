from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from django.db.models import Q

from .models import Product, Stock
from .serializers import ProductSerializer, StockSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # поиск по названию и описанию
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description']


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()  # важно для router
    serializer_class = StockSerializer

    def get_queryset(self):
        queryset = Stock.objects.all()

        search = self.request.query_params.get('search')

        if search:
            queryset = queryset.filter(
                Q(stockproduct__product__title__icontains=search) |
                Q(stockproduct__product__description__icontains=search)
            ).distinct()

        return queryset