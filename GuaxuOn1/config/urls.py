from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Aponta diretamente para o caminho real da sua árvore de ficheiros
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/registration/login.html'), name='login'),
    
    # Suas rotas do aplicativo
    path('', include('app.urls')),
]