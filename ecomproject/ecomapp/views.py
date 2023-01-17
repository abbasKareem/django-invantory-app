from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, View, CreateView, FormView, DeleteView, ListView
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from io import BytesIO


from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

class EcomMixin(object):
    def dispatch(self, request, *args, **kwargs):
        # if the user is login we relate him to the cart
        cart_id = request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            if request.user.is_authenticated and request.user:
                cart_obj.customer = request.user
                cart_obj.save()

        return super().dispatch(request, *args, **kwargs)


class HomeView(EcomMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['myname'] = "abbas Kareem"
        all_products = Product.objects.filter(exist_in_stock=True).order_by('-id')
        paginator = Paginator(all_products, 10)
        page_number = self.request.GET.get('page')
        product_list = paginator.get_page(page_number)
        context['product_list'] = product_list
        return context


class AllProductsView(EcomMixin, TemplateView):
    template_name = 'allproducts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allcategories'] = Category.objects.all()
        return context


class ProductDetailsView(EcomMixin, TemplateView):
    template_name = 'productdetail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']
        product = Product.objects.get(slug=url_slug)
        # product.view_count += 1
        # product.save()
        context['product'] = product

        return context


class AddToCartView(EcomMixin, TemplateView):
    template_name = 'addtocart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get prdouct id from requested url
        product_id = self.kwargs['pro_id']

        #  then get product
        product_obj = Product.objects.get(id=product_id)

        # check if cart exists
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(
                product=product_obj)

            # item already exists in cart
            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity += 1
                # cartproduct.subtotal += product_obj.selling_price
                cartproduct.save()
                # cart_obj.total += product_obj.selling_price
                cart_obj.save()

            # new item is added in cart
            else:
                cartproduct = CartProduct.objects.create(cart=cart_obj, product=product_obj,quantity=1)
                cart_obj.save()

        else:
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id

            cartproduct = CartProduct.objects.create(cart=cart_obj,product=product_obj,quantity=1)
            cart_obj.save()

        return context


class ManageCartView(EcomMixin, View):
    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs['cp_id']
        action = request.GET.get('action')
        cp_obj = CartProduct.objects.get(id=cp_id)
        cart_obj = cp_obj.cart
        if action == 'inc':
            cp_obj.quantity += 1
            cp_obj.save()
            cart_obj.save()
        elif action == 'dcr':
            cp_obj.quantity -= 1
          
            cp_obj.save()
           
            cart_obj.save()
            if cp_obj.quantity == 0:
                cp_obj.delete()

        elif action == "rmv":
            
            cart_obj.save()
            cp_obj.delete()
        # else:
        #     pass
        return redirect('ecomapp:mycart')


class EmptyCartView(EcomMixin, View):
    def get(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            cart.cartproduct_set.all().delete()
            cart.total = 0
            cart.save()

        return redirect("ecomapp:mycart")


class CheckoutView(EcomMixin, CreateView):
    # the form is sent to html page when using CreateForm
    template_name = 'checkout.html'
    form_class = CheckoutForm

    # after submit the form redirect to url
    success_url = reverse_lazy("ecomapp:home")

    # this method will run before all other method in this class
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user:
            pass
        else:
            return redirect("/login/?next=/checkout/")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id', None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
        else:
            cart_obj = None

        context['cart'] = cart_obj
        return context
    # because Order model have a requeired feilds we need to use form_vaild

    def form_valid(self, form):
        cart_id = self.request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            form.instance.ordered_by = self.request.user
            form.instance.cart = cart_obj
            form.instance.order_status = "In Box"
            del self.request.session['cart_id']

        else:
            return redirect("ecomapp:home")
        return super().form_valid(form)


class MyCartView(EcomMixin, TemplateView):
    template_name = 'mycart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id', None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        context['cart'] = cart
        return context


class CustomerRegistrationView(CreateView):
    template_name = "customerregistration.html"
    form_class = CustomerRegistrationForm
    success_url = reverse_lazy("ecomapp:home")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        user = User.objects.create_user(username, email, password)
        form.instance.user = user
        login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url


class CustomerLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("ecomapp:home")


class CustomerLoginView(FormView):
    template_name = "customerlogin.html"
    form_class = CustomerLoginForm
    success_url = reverse_lazy("ecomapp:home")
    # form_valid method is a type of post method and is available in createview, formview, updateview

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data.get("password")
        new_password = make_password(pword)
      

       
        usr = authenticate(self.request, username=uname, password=pword)
        user = User.objects.filter(username=uname, password=new_password)
        

       
        if usr is not None and User.objects.filter(username=uname).exists():
        # if User.objects.filter(username=uname, password=new_password).exists():
           
            login(self.request, usr)
        else:
           
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid credentials"})
        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url


class AboutView(EcomMixin, TemplateView):
    template_name = 'about.html'


class ContectView(EcomMixin, TemplateView):
    template_name = 'contect.html'


class CustomerProfileView(TemplateView):
    template_name = 'customerprofile.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user:
            pass

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        customer = self.request.user
        context = super().get_context_data(**kwargs)
        context['customer'] = customer
        orders = Order.objects.filter(cart__customer=customer).order_by("-id")
        context['orders'] = orders

        return context


class CustomerOrderDetailView(DeleteView):
    template_name = 'customerorderdetail.html'
    model = Order
    context_object_name = "ord_obj"


    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user:
            # if user try to go to other user's order he will redirect to profile page
            order_id = self.kwargs['pk']
       

            order = Order.objects.get(id=order_id)
            if request.user != order.cart.customer:
                return redirect("ecomapp:customerprofile")
        else:
            return redirect("/login/?next=/profile/")

        return super().dispatch(request, *args, **kwargs)


class SearchView(TemplateView):
    template_name = 'search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        results = Product.objects.filter(name__icontains=kw, exist_in_stock=True)
        context['results'] = results
        return context


# Admin
class AdminLoginView(FormView):
    template_name = 'adminpages/adminlogin.html'
    form_class = AdminLoginForm
    success_url = reverse_lazy("ecomapp:adminhome")

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data.get("password")
        usr = authenticate(username=uname, password=pword)
        if usr is not None and Admin.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid credentials"})
        return super().form_valid(form)


# admin username: sara
# admin password: saraadmin@123


class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Admin.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/admin-login/")
        return super().dispatch(request, *args, **kwargs)


class AdminHomeView(AdminRequiredMixin, TemplateView):
    template_name = 'adminpages/adminhome.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pendingorders'] = Order.objects.filter(
            order_status="In Box").order_by("-id")
        return context


class AdminOrderDetailView(AdminRequiredMixin, DeleteView):
    template_name = 'adminpages/adminorderdetail.html'
    model = Order
    context_object_name = "ord_obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allstatus'] = ORDER_STATUS
        return context


class AdminOrdersListView(AdminRequiredMixin, ListView):
    template_name = 'adminpages/adminorderslist.html'
    queryset = Order.objects.all().order_by("-id")
    context_object_name = "allorders"


class AdminOrderStatusChangeView(AdminRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        order_id = self.kwargs["pk"]
        order_obj = Order.objects.get(id=order_id)
        new_status = request.POST.get("status")
        order_obj.order_status = new_status
        order_obj.save()
        return redirect(reverse_lazy("ecomapp:adminorderdetail", kwargs={"pk": order_id}))


class AdminProductListView(AdminRequiredMixin, ListView):
    template_name = 'adminpages/adminproductlist.html'
    queryset = Product.objects.all().order_by("-id")
    context_object_name = "allproducts"


class AdminProductCreateView(AdminRequiredMixin, CreateView):
    template_name = 'adminpages/adminprdouctcreate.html'
    form_class = ProductForm
    success_url = reverse_lazy("ecomapp:adminproductlist")

    # we need this function to handle saving "more_images" to Product table
    def form_valid(self, form):
        p = form.save()
        images = self.request.FILES.getlist("more_images")
        for i in images:
            ProductImage.objects.create(product=p, image=i)


        return super().form_valid(form)




def log_in(request, template_name="customerlogin.html"):
    page_title = "Login"
    if request.method == "POST":
        form = CustomerLoginForm(request.POST)
        postdata = request.POST.copy()
        username = postdata.get('username', '')
        password = postdata.get('password', '')

        try:
            user = authenticate(username=username, password=password)
            login(request, user)

            return HttpResponseRedirect('/')
        except :
            error = True

    return render(request, template_name, locals())


def not_login_user(request):
    return redirect('ecomapp:login')


def category_list(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'category.html', {'category': category, 'products': products})




def generate_pdf(request):
    print("+++++++++++++++++++++++++++++++")
    template = get_template('customerorderdetail.html')
    data = {
        "name": "abbas kareem",
        "order_id": "3433"
    }
    html = template.render(data)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=template.pdf'
        return response
    return HttpResponse("Error Rendering PDF", status=400)


def download_order(request, order_id):
    order = Order.objects.get(id=order_id)

    template = get_template('test.html')
    
    context = {
        "ord_obj": order
    }
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=template.pdf'
        return response
    return HttpResponse("Error Rendering PDF", status=400)


    return render(request, 'test.html', context)
