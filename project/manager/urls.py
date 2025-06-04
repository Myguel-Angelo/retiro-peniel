from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import InscricoesView, InscricaoCreateView, InscricaoDetailView, PagamentoCreateView, InscricaoDeleteView

urlpatterns = [
    path('', InscricoesView.as_view(), name='home'),
    path('auth/login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('auth/logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('nova-inscricao/', InscricaoCreateView.as_view(), name='nova_inscricao'),
    path('inscricao/<int:pk>/', InscricaoDetailView.as_view(), name='detalhes_inscricao'),
    path('inscricao/<int:inscricao_id>/registrar-pagamento/', PagamentoCreateView.as_view(), name='registrar_pagamento'),
    path('inscricao/<int:pk>/deletar/', InscricaoDeleteView.as_view(), name='inscricao_deletar'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)