from django.shortcuts import render
from django.views.generic import View
from .models import Product


class ProductView(View):
    def get(self, request, pk):
        product = Product.objects.get(id=pk)
        return render(request, 'product/detail.html', context={'product': product})
