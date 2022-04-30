from django.urls import path

from crycoin.views import views

urlpatterns = [
    path('login', views.login_view, name='login'),
    path('blockchain_view', views.blockchain_view, name='blockchain_view'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('mine', views.mine, name='mine'),
    path('', views.view_transaction, name='view_transaction'),
    path('nodes', views.register_nodes, name='register_nodes'),
    # path('resolve', views.consensus, name='resolve'),
    path('chain', views.chain, name='chain'),
]