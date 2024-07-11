from django.urls import path
from .views import ItemViewSet

item_list=ItemViewSet.as_view({
    'get': 'list',
    'post': 'create'
})


urlpatterns = [
    path('items/', item_list, name='item-list'),
]