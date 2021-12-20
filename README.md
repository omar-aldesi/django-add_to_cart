# django-add_to_cart

lets start:

# create models
note: there are optional fields
```python

# category
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# the item
class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price =  models.FloatField(blank=True, null=True)
    description = models.TextField()
    image = models.ImageField(upload_to='images')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1,default='P')
    # slug important
    slug = models.SlugField(unique=True,null=True)
  
    
    # add to carts functionality
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('core:product', kwargs={'slug': self.slug})

    def get_add_to_cart_url(self):
        return reverse('core:add-to-cart', kwargs={'slug': self.slug})
        
    def get_remove_from_cart_url(self):
        return reverse('core:remove-from-cart', kwargs={'slug': self.slug})

# the order item
class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.quantity} of {self.item.name}"

    def get_total_item_price(self):
        return self.quantity * self.item.price
    
    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()
    
    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()

# the order
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True,null=True)
    orderd_date = models.DateTimeField(null=True)
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)


    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total

```

# create functionality
<code>in views.py</code>

okay its a cart integrated system
Please pay attention on urls 
and dont forget import models 
```python

@login_required
def add_to_cart(request,slug):
    item = get_object_or_404(Item,slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False,
        )
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "The item quantity was updated in your cart.")
            return redirect('core:product',slug=slug)

        else:
            # message (the item added to cart successfully)
            messages.info(request, "This item was added to your cart.")
            order.items.add(order_item)
            return redirect('core:product',slug=slug)

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user,orderd_date=ordered_date)
        order.items.add(order_item)
        return redirect('core:product',slug=slug)


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

```

# create urls:
<code>now in urls.py</code>

```python

    path('add-to-cart/<str:slug>/',views.add_to_cart,name='add-to-cart'),
    path('remove-from-cart/<str:slug>/',views.remove_from_cart,name='remove-from-cart'),
    path('remove_from_cart_in_summary/<str:slug>/',views.remove_from_cart_in_summary,name='remove-from-cart-in-summary'),
    path('order-summary/',views.OrderSummaryView.as_view(),name='order-summary'),
    path('remove-item-from-cart/<str:slug>',views.remove_one_item_from_cart,name='remove-one-item-from-cart'),
    path('add_one_to_item_cart/<str:slug>',views.add_one_to_item_cart,name='add-one-item-to-cart'),
    
```

**** note make sure you put the models in class/def context example: ***
```python
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
```

# html templates:


for update quantity and remove from cart:
i use here (ion icon) you can use what you want
```html
<td><a href="{% url 'core:remove-one-item-from-cart' order.item.slug %}"><i class="fas fa-minus mr-2"></a></i> {{order.quantity}}<a href="{% url 'core:add-one-item-to-cart' order.item.slug %}"><i class="fas fa-plus ml-2"></i></a></td>
```

in product.html:
for add and remove from cart:

```html
<a href="{{object.get_add_to_cart_url}}" class="btn btn-primary btn-md my-0 p">Add to cart<i class="fas fa-shopping-cart ml-1"></i></a> <!-- add to cart -->
<a href="{{object.get_remove_from_cart_url}}" class="btn btn-danger btn-md my-0 p">remove from cart</a> <!-- remove from cart -->
```
# optional
to make count icon for items in cart:

make folder ' templatetags ' 
then ' cart_template_tag '

inside the file put this codel:

```python
from django import template
from core.models import *

register = template.Library()

@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user,ordered=False)
        if qs.exists():
            return qs[0].items.count()
    return 0
```

in navbar.html:
```html
{% load cart_template_tags %}
```

this span will count all item in cart and show it as int()
```html
<span class="badge red z-depth-1 mr-1">{{request.user|cart_item_count}} </span>
```

and thats it!!
