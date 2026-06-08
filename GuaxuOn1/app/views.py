from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.db.models import Q
from .models import AgendaColeta, Bairro, TipoResiduo, Manifestacao, Imovel, IPTU2026

# --- FUNÇÃO AUXILIAR DE PERMISSÃO ---
def eh_admin(user):
    """Verifica se o usuário está logado e pertence à equipe de administração"""
    return user.is_authenticated and user.is_staff


# --- VIEW DO DASHBOARD (RESTRITA) ---
@login_required
def dashboard_view(request):
    """Esta página só abre se o usuário estiver autenticado"""
    return render(request, 'app/base.html')


# --- VIEW DA TELA PRINCIPAL (INDEX) ---
def index(request):
    dias = [
        'Segunda-feira', 'Terça-feira', 'Quarta-feira', 
        'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo'
    ]
    hoje_num = datetime.now().weekday()
    dia_atual = dias[hoje_num]

    coletas_hoje = AgendaColeta.objects.filter(
        dia_semana=dia_atual, 
        ativo=True
    ).select_related('bairro', 'tipo').order_by('horario')

    context = {
        'dia_atual': dia_atual,
        'coletas_hoje': coletas_hoje,
    }
    return render(request, 'app/index.html', context)


# --- VIEW DA LISTA DE COLETAS COM FILTRO (SUPORTE A DADOS FICTÍCIOS REFORÇADOS) ---
def coleta_list(request):
    # 1. Tenta buscar os bairros reais do banco de dados
    bairros_queryset = Bairro.objects.filter(ativo=True).order_by('nome')
    
    # Se o banco de bairros estiver zerado, cria a lista base na memória para renderizar o select
    if not bairros_queryset.exists():
        bairros = [
            Bairro(id=1, nome="Centro"),
            Bairro(id=2, nome="Avenida"),
            Bairro(id=3, nome="Colina dos Prados"),
            Bairro(id=4, nome="Jardim Planalto"),
        ]
    else:
        bairros = list(bairros_queryset)

    # 2. Captura o parâmetro enviado pelo formulário HTML
    bairro_param = request.GET.get('bairro', '').strip()
    bairro_selecionado = None

    # 3. Tenta buscar as agendas reais salvas no banco de dados
    agendas_queryset = AgendaColeta.objects.filter(ativo=True).select_related('bairro', 'tipo')
    
    if agendas_queryset.exists():
        # SE JÁ EXISTIREM DADOS REAIS NO BANCO, REALIZA O FILTRO REAL
        if bairro_param:
            if bairro_param.isdigit():
                bairro_selecionado = int(bairro_param)
                agendas = agendas_queryset.filter(bairro_id=bairro_selecionado)
            else:
                agendas = agendas_queryset.filter(bairro__nome__icontains=bairro_param)
                bairro_obj = Bairro.objects.filter(nome__icontains=bairro_param).first()
                if bairro_obj:
                    bairro_selecionado = bairro_obj.id
        else:
            agendas = agendas_queryset
            
        agendas = agendas.order_by('bairro__nome', 'dia_semana', 'horario')
    else:
        # SE O BANCO ESTIVER TOTALMENTE VAZIO, CRIA AUTOMATICAMENTE DADOS FICTÍCIOS EM MEMÓRIA
        tipo_organico = TipoResiduo(nome="Orgânico", cor_identificacao="#004a8d")
        tipo_reciclavel = TipoResiduo(nome="Reciclável", cor_identificacao="#28a745")
        tipo_eletronico = TipoResiduo(nome="Eletrônico", cor_identificacao="#ffc107")

        b1 = Bairro(id=1, nome="Centro")
        b2 = Bairro(id=2, nome="Avenida")
        b3 = Bairro(id=3, nome="Colina dos Prados")
        b4 = Bairro(id=4, nome="Jardim Planalto")

        dados_ficticios = [
            # === 5 HORÁRIOS: CENTRO ===
            AgendaColeta(bairro=b1, tipo=tipo_organico, dia_semana="Segunda-feira", horario="07:00"),
            AgendaColeta(bairro=b1, tipo=tipo_reciclavel, dia_semana="Terça-feira", horario="09:00"),
            AgendaColeta(bairro=b1, tipo=tipo_organico, dia_semana="Quarta-feira", horario="07:00"),
            AgendaColeta(bairro=b1, tipo=tipo_reciclavel, dia_semana="Quinta-feira", horario="14:30"),
            AgendaColeta(bairro=b1, tipo=tipo_eletronico, dia_semana="Sábado", horario="08:00"),

            # === 5 HORÁRIOS: AVENIDA ===
            AgendaColeta(bairro=b2, tipo=tipo_organico, dia_semana="Terça-feira", horario="08:30"),
            AgendaColeta(bairro=b2, tipo=tipo_organico, dia_semana="Quinta-feira", horario="08:30"),
            AgendaColeta(bairro=b2, tipo=tipo_reciclavel, dia_semana="Sexta-feira", horario="10:00"),
            AgendaColeta(bairro=b2, tipo=tipo_organico, dia_semana="Sábado", horario="07:15"),
            AgendaColeta(bairro=b2, tipo=tipo_eletronico, dia_semana="Domingo", horario="19:00"),

            # === 5 HORÁRIOS: COLINA DOS PRADOS ===
            AgendaColeta(bairro=b3, tipo=tipo_organico, dia_semana="Segunda-feira", horario="13:00"),
            AgendaColeta(bairro=b3, tipo=tipo_reciclavel, dia_semana="Quarta-feira", horario="10:30"),
            AgendaColeta(bairro=b3, tipo=tipo_organico, dia_semana="Quinta-feira", horario="13:00"),
            AgendaColeta(bairro=b3, tipo=tipo_reciclavel, dia_semana="Sexta-feira", horario="16:00"),
            AgendaColeta(bairro=b3, tipo=tipo_eletronico, dia_semana="Sábado", horario="11:15"),

            # === 5 HORÁRIOS: JARDIM PLANALTO ===
            AgendaColeta(bairro=b4, tipo=tipo_organico, dia_semana="Segunda-feira", horario="06:30"),
            AgendaColeta(bairro=b4, tipo=tipo_reciclavel, dia_semana="Terça-feira", horario="14:00"),
            AgendaColeta(bairro=b4, tipo=tipo_organico, dia_semana="Quarta-feira", horario="06:30"),
            AgendaColeta(bairro=b4, tipo=tipo_organico, dia_semana="Sexta-feira", horario="06:30"),
            AgendaColeta(bairro=b4, tipo=tipo_eletronico, dia_semana="Sábado", horario="15:30"),
        ]

        if bairro_param:
            if bairro_param.isdigit():
                bairro_selecionado = int(bairro_param)
                agendas = [a for a in dados_ficticios if a.bairro.id == bairro_selecionado]
            else:
                bairro_selecionado = bairro_param
                agendas = [a for a in dados_ficticios if bairro_param.lower() in a.bairro.nome.lower()]
        else:
            agendas = dados_ficticios

    context = {
        'agendas': agendas,
        'bairros': bairros,
        'bairro_selecionado': bairro_selecionado,
    }
    
    return render(request, 'app/coleta_lixo.html', context)


# --- VIEW DE CADASTRO DE NOVOS USUÁRIOS ---
def register_view(request):
    """Gera o formulário para criação de novas contas de cidadãos"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user) 
            return redirect('dashboard') 
    else:
        form = UserCreationForm()
    
    return render(request, 'app/registration/register.html', {'form': form})


# --- VIEW DE PERFIL DO USUÁRIO ---
@login_required
def perfil_view(request):
    """Exibe os dados do usuário autenticado no sistema"""
    return render(request, 'app/perfil.html', {'usuario': request.user})


# --- VIEW DE BUSCA INTELIGENTE (REDIRECIONAMENTO) ---
def search_view(request):
    """Captura a pesquisa global e redireciona dinamicamente baseada em palavras-chave"""
    termo = request.GET.get('q', '').strip().lower()
    
    if not termo:
        return redirect('index')

    palavras_coleta = ['coleta', 'lixo', 'horario', 'bairro', 'agenda', 'reciclavel', 'organico', 'residuo']
    if any(p in termo for p in palavras_coleta) or Bairro.objects.filter(nome__icontains=termo, ativo=True).exists():
        return redirect(f"/coletas/?bairro={termo}")

    palavras_perfil = ['perfil', 'minha conta', 'dados', 'usuario', 'meu perfil', 'alterar senha']
    if any(p in termo for p in palavras_perfil):
        return redirect('perfil')

    if 'entrar' in termo or 'login' in termo:
        return redirect('login')
    if 'cadastrar' in termo or 'registro' in termo or 'conta' in termo:
        return redirect('register')

    return redirect(f"/coletas/?bairro={termo}")


# --- VIEW PARA ADICIONAR NOVA AGENDA (APENAS ADMIN) ---
@user_passes_test(eh_admin, login_url='login')
def coleta_create(request):
    if request.method == 'POST':
        bairro_id = request.POST.get('bairro')
        tipo_id = request.POST.get('tipo')
        dia_semana = request.POST.get('dia_semana')
        horario = request.POST.get('horario')
        
        bairro = get_object_or_404(Bairro, id=bairro_id)
        tipo = get_object_or_404(TipoResiduo, id=tipo_id)
        
        AgendaColeta.objects.create(
            bairro=bairro,
            tipo=tipo,
            dia_semana=dia_semana,
            horario=horario,
            ativo=True
        )
        messages.success(request, "Novo horário de coleta adicionado com sucesso!")
        return redirect('coleta_list')
        
    bairros = Bairro.objects.filter(ativo=True).order_by('nome')
    tipos = TipoResiduo.objects.all()
    dias = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo']
    
    return render(request, 'app/coleta_form.html', {
        'bairros': bairros,
        'tipos': tipos,
        'dias': dias,
        'titulo': 'Adicionar Horário de Coleta'
    })


# --- VIEW PARA EDITAR AGENDA EXISTENTE (APENAS ADMIN) ---
@user_passes_test(eh_admin, login_url='login')
def coleta_update(request, pk):
    agenda = get_object_or_404(AgendaColeta, pk=pk)
    
    if request.method == 'POST':
        agenda.bairro_id = request.POST.get('bairro')
        agenda.tipo_id = request.POST.get('tipo')
        agenda.dia_semana = request.POST.get('dia_semana')
        agenda.horario = request.POST.get('horario')
        agenda.save()
        
        messages.success(request, f"Horário de coleta atualizado com sucesso!")
        return redirect('coleta_list')
        
    bairros = Bairro.objects.filter(ativo=True).order_by('nome')
    tipos = TipoResiduo.objects.all()
    dias = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo']
    
    return render(request, 'app/coleta_form.html', {
        'agenda': agenda,
        'bairros': bairros,
        'tipos': tipos,
        'dias': dias,
        'titulo': 'Editar Horário de Coleta'
    })


# --- MÓDULO INTEGRADO DE OUVIDORIA MUNICIPAL ---

def ouvidoria_home(request):
    """Exibe o menu de opções da ouvidoria"""
    return render(request, 'app/ouvidoria_home.html')


def ouvidoria_nova(request):
    """Salva a manifestação atrelando OBRIGATORIAMENTE ao usuário logado"""
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "Você precisa entrar na sua conta para registrar uma manifestação.")
            return redirect('login')

        tipo = request.POST.get('tipo')
        assunto = request.POST.get('assunto')
        descricao = request.POST.get('descricao')
        bairro_texto = request.POST.get('bairro', '').strip()
        
        bairro_obj = None
        if bairro_texto:
            bairro_obj = Bairro.objects.filter(nome__icontains=bairro_texto, ativo=True).first()
        
        nova_manifestacao = Manifestacao.objects.create(
            tipo=tipo, 
            assunto=assunto, 
            descricao=descricao, 
            bairro=bairro_obj,
            usuario=request.user  # Garante o vínculo rígido do dono
        )
        
        messages.success(request, f"Manifestação registrada com sucesso! Protocolo: {nova_manifestacao.protocolo}")
        return redirect(f"/ouvidoria/consulta/?protocolo={nova_manifestacao.protocolo}")
        
    bairros = Bairro.objects.filter(ativo=True).order_by('nome')
    return render(request, 'app/ouvidoria_form.html', {'bairros': bairros})


def ouvidoria_consulta(request):
    """Permite pesquisar o andamento protegendo rigidamente os dados de terceiros"""
    protocolo_busca = request.GET.get('protocolo', '').strip().upper()
    manifestacao = None
    erro = None
    
    # 1. Regra do Histórico: Se for Admin vê tudo, se for usuário comum vê apenas os dele.
    if request.user.is_authenticated:
        if request.user.is_staff:
            todas_manifestacoes = Manifestacao.objects.all().select_related('bairro').order_by('-data_criacao')
        else:
            todas_manifestacoes = Manifestacao.objects.filter(usuario=request.user).select_related('bairro').order_by('-data_criacao')
    else:
        todas_manifestacoes = Manifestacao.objects.none()
    
    # 2. Regra da Busca Direta por Protocolo com Validação Blindada e Redirecionamento de Erro
    if protocolo_busca:
        if not request.user.is_authenticated:
            erro = "Você precisa entrar na sua conta para consultar os detalhes deste protocolo."
            return render(request, 'app/ouvidoria_erro.html', {'erro': erro})
        else:
            manifestacao_alvo = Manifestacao.objects.filter(protocolo=protocolo_busca).select_related('bairro', 'usuario').first()
            
            if not manifestacao_alvo:
                erro = f"O protocolo '{protocolo_busca}' não foi localizado no sistema. Verifique se digitou corretamente."
                return render(request, 'app/ouvidoria_erro.html', {'erro': erro})
            else:
                # 🔒 TRAVA DE PRIVACIDADE: Só acessa se for da equipe ou o dono real da requisição
                if request.user.is_staff or manifestacao_alvo.usuario == request.user:
                    manifestacao = manifestacao_alvo
                    
                    if hasattr(manifestacao, 'resposta_admin'):
                        manifestacao.resposta_limpa = manifestacao.resposta_admin
                    elif hasattr(manifestacao, 'resposta_ouvidoria'):
                        manifestacao.resposta_limpa = manifestacao.resposta_ouvidoria
                    else:
                        manifestacao.resposta_limpa = ""
                else:
                    erro = f"Acesso negado. O protocolo '{protocolo_busca}' pertence a outro cidadão. Você não possui permissões de visibilidade."
                    return render(request, 'app/ouvidoria_erro.html', {'erro': erro})
            
    # Injeta a resposta limpa no laço do histórico
    for m in todas_manifestacoes:
        if hasattr(m, 'resposta_admin'):
            m.resposta_limpa = m.resposta_admin
        elif hasattr(m, 'resposta_ouvidoria'):
            m.resposta_limpa = m.resposta_ouvidoria
        else:
            m.resposta_limpa = ""

    return render(request, 'app/ouvidoria_consulta.html', {
        'manifestacao': manifestacao,
        'erro': erro,
        'protocolo_busca': protocolo_busca,
        'todas_manifestacoes': todas_manifestacoes
    })


@user_passes_test(eh_admin, login_url='login')
def ouvidoria_painel(request):
    """Painel operacional restrito para triagem de ouvidoria"""
    if request.method == 'POST':
        manifestacao_id = request.POST.get('id')
        novo_status = request.POST.get('status')
        resposta = request.POST.get('resposta')
        
        instancia = get_object_or_404(Manifestacao, id=manifestacao_id)
        instancia.status = novo_status
        
        if hasattr(instancia, 'resposta_admin'):
            instancia.resposta_admin = response
        else:
            instancia.resposta_ouvidoria = resposta
            
        instancia.save()
        
        messages.success(request, f"Parecer registrado com sucesso para o protocolo {instancia.protocolo}!")
        return redirect('ouvidoria_painel')

    chamados = Manifestacao.objects.all().select_related('bairro').order_by('-data_criacao')
    for chamado in chamados:
        if hasattr(chamado, 'resposta_admin'):
            chamado.resposta_limpa = chamado.resposta_admin
        elif hasattr(chamado, 'resposta_ouvidoria'):
            chamado.resposta_limpa = chamado.resposta_ouvidoria
        else:
            chamado.resposta_limpa = ""

    return render(request, 'app/ouvidoria_painel.html', {'chamados': chamados})


# --- MÓDULO INTEGRADO DE ARRECADACAO E IPTU 2026 ---

def iptu_home(request):
    """Menu Inicial de opções do IPTU"""
    return render(request, 'app/iptu_home.html')


def iptu_consulta(request):
    """Consulta os débitos do imóvel usando Inscrição Imobiliária ou CPF/CNPJ"""
    busca = request.GET.get('busca', '').strip()
    imoveis = None
    erro = None
    
    if busca:
        busca_limpa = busca.replace('.', '').replace('-', '').replace('/', '')
        imoveis = Imovel.objects.filter(
            Q(inscricao_imobiliaria__exact=busca) | 
            Q(cpf_cnpj__icontains=busca_limpa) |
            Q(cpf_cnpj__icontains=busca)
        ).prefetch_related('debitos')
        
        if not imoveis.exists():
            erro = "Nenhum imóvel foi localizado. Verifique os dados inseridos."
            
    return render(request, 'app/iptu_consulta.html', {
        'imoveis': imoveis,
        'erro': erro,
        'busca': busca
    })


def iptu_certidao(request):
    """Gera a Certidão Negativa de Débitos Municipal"""
    if request.method == 'POST':
        documento = request.POST.get('documento', '').strip()
        busca_limpa = documento.replace('.', '').replace('-', '').replace('/', '')
        
        possui_imovel = Imovel.objects.filter(cpf_cnpj=busca_limpa).exists()
        
        if not possui_imovel:
            messages.error(request, "Contribuinte não localizado no cadastro imobiliário de Guaxupé.")
            return redirect('iptu_certidao')
            
        case_debitos = IPTU2026.objects.filter(
            imovel__cpf_cnpj=busca_limpa, 
            status__in=['ABERTO', 'VENCIDO']
        ).exists()
            
        return render(request, 'app/iptu_certidao_resultado.html', {
            'documento': documento,
            'regular': not case_debitos,
            'data_emissao': datetime.now()
        })
        
    return render(request, 'app/iptu_certidao.html')