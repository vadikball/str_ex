from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('', views.MainPage.as_view(), name='readme'),
    path('buy/<int:pk>', views.BuyItem.as_view(), name='buy'),
    path('item/<int:pk>', views.GetItem.as_view(), name='item_detail'),
    path('success/', views.SuccessPage.as_view(), name='success'),
    path('success/<int:pk>', views.SuccessPageOrder.as_view(), name='success_detailed'),
    path('order/<int:pk>', views.GetOrder.as_view(), name='order_detailed'),
    path('order/buy/<int:pk>', views.BuyOrder.as_view(), name='order_buy'),
    path('intent/<int:pk>', views.CreatePaymentIntent.as_view(), name='intent'),
    path('pub_key/', views.PubKey.as_view(), name='pub_key'),
    path('intent/<int:pk>/status', views.IntentStatus.as_view(), name='intent_status'),
    path('intent/<int:pk>/status/success', views.IntentStatusSuccess.as_view(), name='intent_status_success'),
    path('catalog/', views.ItemCatalog.as_view(), name='catalog'),
    path('scrap-it/', views.GetTestData.as_view(), name='scrap_it'),
    path('clear-items/', views.DeleteTestData.as_view(), name='clear_items'),
]
