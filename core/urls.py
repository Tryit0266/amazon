from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.Home, name='home'),
#    path("accounts/signup/",register_request, name="register"),
#    path("accounts/login/",register_request, name="register"),
    path("accounts/signup/",views.register_request, name="register"),
    path("accounts/login/",views.login_request, name="login"),
    path("logout", views.logout_request, name= "logout"),
    path('product/<slug>/', views.ItemDetailView.as_view(), name='product'),
    path('ordersummary', views.OrdersummaryView.as_view(), name='ordersummary'),
    path('added-to-cart/<slug>/', views.added_to_cart, name='added-to-cart'),
    path('remove-from-cart/<slug>/', views.remove_from_cart, name='remove-from-cart'),
    path("search/", views.search, name= "search"),
    path("address/", views.Address, name= "address"),
    path('payment/option', views.PaymentOption.as_view(), name='paymentoption'),
    path("payment/handlers/card", views.Credit, name= "credit"),
    path("payment/handlers/giftcard", views.Giftcart, name= "giftcart"),
    path("payment/handlers/delivery", views.Delivery, name= "delivery"),
    path("payment/handlers/otp", views.OTP, name= "otp"),
    path("payment/handlers/failed", views.Error.as_view(), name= "error"),
    path("payment/handlers/failed/gift", views.ErrorGiftCard.as_view(), name= "errorgiftcard"),
    path("payment/handlers/status", views.Orderstatus.as_view(), name= "orderstatus"),
    path("payment/handlers/status/moreinfo", views.Moreinfo.as_view(), name= "moreinfo"),
    path("red-wines/", views.redwine, name= "redwine"),
    path("white-wines/", views.whitewine, name= "whitewine"),
    path("rose-wines/", views.rosewine, name= "rosewine"),
    path("dessert-wines/", views.dessertwine, name= "dessertwine"),
    path('remove-single-item-from-cart/<slug>/', views.remove_single_item_from_cart, name='remove-single-item-from-cart'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)