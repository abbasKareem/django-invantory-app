from django.urls import path
from .views import *
app_name = 'ecomapp'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('contect/', ContectView.as_view(), name='contact'),
    path('all-products/', AllProductsView.as_view(), name='allproducts'),
    path('product/<slug:slug>/', ProductDetailsView.as_view(), name='productdetails'),

    path('add-to-cart-<int:pro_id>/', AddToCartView.as_view(), name='addtocart'),
    path('my-cart/', MyCartView.as_view(), name='mycart'),
    path('manage-cart/<int:cp_id>', ManageCartView.as_view(), name='managecart'),
    path('empty-cart/', EmptyCartView.as_view(), name='emptycart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('register/', CustomerRegistrationView.as_view(),
         name='customerregistration'),
    path('logout/', CustomerLogoutView.as_view(), name='customerlogout'),
    path('login/', CustomerLoginView.as_view(), name='customerlogin'),
#     path('login/', log_in, name='customerlogin'),
    path('profile/', CustomerProfileView.as_view(), name='customerprofile'),
    path('profile/order-<int:pk>/', CustomerOrderDetailView.as_view(),
         name='customerorderdetail'),
    path('search/', SearchView.as_view(), name='search'),
    # Admin Side Pages
    path('admin-login/', AdminLoginView.as_view(), name='adminlogin'),
    path('admin-home/', AdminHomeView.as_view(), name='adminhome'),
    path('admin-order/<int:pk>/', AdminOrderDetailView.as_view(),
         name='adminorderdetail'),
    path('admin-all-orders/', AdminOrdersListView.as_view(), name='adminorderslist'),
    path('admin-order-<int:pk>-change/',
         AdminOrderStatusChangeView.as_view(), name='adminorderstatuschange'),
    path('admin-prdouct/list/', AdminProductListView.as_view(),
         name='adminproductlist'),
    path('admin-prdouct/add/', AdminProductCreateView.as_view(),
         name='adminproductcreate'),

     path('not-login/', not_login_user, name='not-login-user'),
     path('ecomapp/<slug:category_slug>/', category_list, name='category_list'),
     path('generate-pdf/', generate_pdf, name='generate-pdf'),
     path('download-order/<int:order_id>/', download_order, name='download-order'),


]
