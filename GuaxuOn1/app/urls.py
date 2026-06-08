from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='app/registration/logged_out.html'), name='logout'),
    
    # 🌟 Nova URL da busca inteligente
    path('search/', views.search_view, name='global_search'),

    # 🚚 Rotas de Coleta de Lixo (Listagem + Administrativas)
    path('coletas/', views.coleta_list, name='coleta_list'),
    path('coletas/novo/', views.coleta_create, name='coleta_create'),
    path('coletas/editar/<int:pk>/', views.coleta_update, name='coleta_update'),

    # 📢 Rotas do Módulo de Ouvidoria (Cidadão e Administrador)
    path('ouvidoria/', views.ouvidoria_home, name='ouvidoria_home'),
    path('ouvidoria/nova/', views.ouvidoria_nova, name='ouvidoria_nova'),
    path('ouvidoria/consulta/', views.ouvidoria_consulta, name='ouvidoria_consulta'),
    path('ouvidoria/painel/', views.ouvidoria_painel, name='ouvidoria_painel'),

    # 🧾 MÓDULO DE ARRECADAÇÃO E IPTU 2026
    path('iptu/', views.iptu_home, name='iptu_home'),
    path('iptu/consulta/', views.iptu_consulta, name='iptu_consulta'),
    path('iptu/certidao/', views.iptu_certidao, name='iptu_certidao'),
]