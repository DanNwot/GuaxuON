from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Rotas base do sistema
    path('', views.index, name='index'),
    path('coletas/', views.coleta_list, name='coleta_list'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # 🌟 Rota que resolve o erro NoReverseMatch da linha 88 do login.html
    path('register/', views.register_view, name='register'),
    
    # 🌟 Rota que resolve o erro 405 do Logout
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='app/registration/logged_out.html'), name='logout'),
]