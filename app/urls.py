from django.urls import path

import app.views.users as user_views
import app.views.transactions as transaction_views

urlpatterns = [
    # User paths
    path('', user_views.index, name='user_list'),
    path('users/', user_views.index, name='user_list'),
    path('users/view/<int:pk>', user_views.show, name='user_view'),
    path('users/new', user_views.create, name='user_new'),
    path('users/edit/<int:pk>', user_views.update, name='user_edit'),
    path('users/delete/<int:pk>', user_views.destroy, name='user_delete'),

    # Transaction paths
    path('transactions/view/<int:pk>', transaction_views.show, name='transaction_view'),
    path('transactions/new', transaction_views.create, name='transaction_new'),
    # path('transactions/edit/<int:pk>', transaction_views.update, name='transaction_edit'),
    # path('transactions/delete/<int:pk>', transaction_views.destroy, name='transaction_delete'),
    path('transactions/today', transaction_views.today, name='transaction_today'),
]
