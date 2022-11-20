from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('', views.MainPage.as_view(), name='all'),
    path('buy/<int:pk>', views.BuyItem.as_view()),
    path('item/<int:pk>', views.GetItem.as_view()),
    path('success/', views.SuccessPage.as_view()),
    path('success/<int:pk>', views.SuccessPageOrder.as_view()),
    path('order/<int:pk>', views.GetOrder.as_view()),
    path('order/buy/<int:pk>', views.BuyOrder.as_view()),
    path('intent/<int:pk>', views.CreatePaymentIntent.as_view()),
    path('pub_key/', views.PubKey.as_view()),
    path('intent/<int:pk>/status', views.IntentStatus.as_view()),
    path('intent/<int:pk>/status/success', views.IntentStatusSuccess.as_view()),
    path('catalog/', views.ItemCatalog.as_view(), name='catalog'),
    path('scrap-it/', views.GetTestData.as_view()),
]
