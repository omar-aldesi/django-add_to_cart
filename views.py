from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object':order
            }
            return render(self.request,'pages/order_summary.html',context)
        except ObjectDoesNotExist:
            messages.info(self.request,"You do not have an active order")
            return redirect("/")
            


@login_required
def remove_from_cart(request,slug):

    item = get_object_or_404(Item,slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False,
        )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False,
            )[0]
            order.items.remove(order_item)
            messages.info(request, "This item was removed from your cart.")
            return redirect('core:product',slug=slug)
        else:
            # message (the user does not have an order)
            messages.info(request, "this item not in your cart")
            return redirect('core:product',slug=slug)

    else:
        # message (the user does not have an order)
        messages.info(request, "you dont have an active order")
        return redirect('core:product',slug=slug)


@login_required
def remove_one_item_from_cart(request,slug):

    item = get_object_or_404(Item,slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False,
        )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False,
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect('core:order-summary')
        else:
            # message (the user does not have an order)
            messages.info(request, "this item not in your cart")
            return redirect('core:order-summary')

    else:
        # message (the user does not have an order)
        messages.info(request, "you dont have an active order")
        return redirect('core:home')


@login_required
def add_one_to_item_cart(request,slug):

    item = get_object_or_404(Item,slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False,
        )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False,
            )[0]
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect('core:order-summary')
        else:
            # message (the user does not have an order)
            messages.info(request, "this item not in your cart")
            return redirect('core:order-summary')

    else:
        # message (the user does not have an order)
        messages.info(request, "you dont have an active order")
        return redirect('core:home')


def remove_from_cart_in_summary(request,slug):

    item = get_object_or_404(Item,slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False,
        )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False,
            )[0]
            order.items.remove(order_item)
            messages.info(request, "This item was removed from your cart.")
            return redirect('core:order-summary')
        else:
            # message (the user does not have an order)
            messages.info(request, "this item not in your cart")
            return redirect('core:order-summary')

    else:
        # message (the user does not have an order)
        messages.info(request, "you dont have an active order")
        return redirect('core:home')

