from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from cart.cart_module import Cart
from cart.models import Order, OrderItem, DiscountCode
from product.models import Product


class CartDetailView(View):
    def get(self, reqeust):
        cart = Cart(reqeust)
        return render(reqeust, 'cart/cart_detail.html', context={"cart": cart})


class CartAddView(View):
    def post(self, reqeust, pk):
        product = get_object_or_404(Product, id=pk)
        size, color, quantity = (reqeust.POST.get('size', 'Empty'), reqeust.POST.get('color', 'Empty'),
                                 reqeust.POST.get('quantity', 'Empty'))
        print(quantity)
        cart = Cart(reqeust)
        cart.add(product, quantity, color, size)
        return redirect('cart:cart_Detail')


class CartDeleteView(View):
    def get(self, request, pk):
        cart = Cart(request)
        cart.delete(pk)
        return redirect('cart:cart_Detail')


class OrderDetailView(View):
    def get(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        return render(request, 'cart/order_detail.html', context={'order': order})


class OrderCreationView(View):
    def get(self, request):
        cart = Cart(request)

        order = Order.objects.create(user=request.user, total_price=cart.total())
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], color=item['color'],
                                     size=item['size'], quantity=item['quantity'], price=item['price'])
        cart.remove()
        return redirect('cart:cart_order_detail', order.id)


class ApplyDiscountView(View):
    def post(self, request, pk):
        code = request.POST.get('discount_code')
        print(code)
        order = get_object_or_404(Order, id=pk)
        discount_code = get_object_or_404(DiscountCode, name=code)
        if discount_code.quantity == 0:
            return redirect('cart:cart_order_detail', order.id)
        order.total_price -= order.total_price * discount_code.discount / 100
        order.save()
        discount_code.quantity -= 1
        discount_code.save()
        return redirect('cart:cart_order_detail', order.id)
