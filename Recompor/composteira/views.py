from django.shortcuts import render
from django.http import HttpResponse
from .models import Composteira
from .models import Compostagem
from usuarios import *
from django.db.models import Sum
from django.db.models.functions import ExtractMonth
from django.db.models import Subquery, OuterRef
from django.utils.safestring import mark_safe
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .forms import ComposteiraForm
from datetime import datetime, timedelta





def viewAdicionarComposteira(request):
    #Verifica se o user está logado
    if request.user.is_authenticated == True:
        #Verifica se o metodo é o get e não o post
        if request.method == 'GET': 
            return render(request, "addComposteira.html")
        #Captura os dados e salva e renderiza para outra tela
        else:
            name_comp = request.POST.get("name_comp")
            data_const = request.POST.get("data_const")
            #escala = request.POST.get("escala_comp")
            regiao = request.POST.get("regiao")
            tipo = request.POST.get("tipo")
            imagem = request.FILES.get("imagem") 
            composteira = Composteira(
                fkUsuario = request.user, 
                regiao = regiao, 
                #tamanho = escala, 
                tipo = tipo, 
                data_construcao = data_const, 
                nome = name_comp,
                imagem=imagem
                )
            composteira.save()
            context = {
                'nomeUser': request.user.username
            }
            composteiras = Composteira.objects.filter(fkUsuario_id = request.user)
            return render(request, "grafico-geral.html", {"composteiras": composteiras})
    return render(request, "usuarios/Login.html") 


def viewAdicionarCompostagem(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Você precisa estar logado para acessar essa página.")
        return redirect("login")  # Redireciona para a página de login, por exemplo

    # Busca composteiras do usuário autenticado
    composteiras = Composteira.objects.filter(fkUsuario_id=request.user)

    # Se for uma requisição GET → apenas exibe a página
    if request.method == "GET":
        compostagens = Compostagem.objects.filter(
            fkUsuario_comp=request.user,
            fkComposteira__in=composteiras
        )
        return render(request, "addCompostagem.html", {
            "composteiras": composteiras,
            "compostagens": compostagens
        })

    # Se for POST → tentativa de cadastrar uma nova compostagem
    try:
        data_inicio = datetime.strptime(request.POST.get("data_inicio"), "%Y-%m-%d").date()
        fkComposteira = request.POST.get("composteira")
        peso = float(request.POST.get("peso") or 0)

        # Validação simples
        if not fkComposteira or peso <= 0:
            messages.error(request, "Preencha todos os campos corretamente.")
            return redirect("composteira:addCompostagem")

        composteira = Composteira.objects.get(id_composteira=fkComposteira)

        # Evita compostagens duplicadas (mesma composteira + mesma data)
        existe = Compostagem.objects.filter(
            fkComposteira=composteira,
            data_inicio=data_inicio,
            fkUsuario_comp=request.user
        ).exists()

        if existe:
            messages.warning(request, "Já existe uma compostagem nessa composteira para essa data.")
            return redirect("composteira:addCompostagem")

        # Cria e salva
        compostagem = Compostagem.objects.create(
            fkComposteira=composteira,
            data_inicio=data_inicio,
            peso=peso,
            fkUsuario_comp=request.user
        )

        # Calcula previsão de adubo
        dias, data_pronto = compostagem.calcular()

        messages.success(
            request,
            f"✅ Compostagem salva! Adubo previsto para {data_pronto.strftime('%d/%m/%Y')} ({dias} dias)."
        )

    except Composteira.DoesNotExist:
        messages.error(request, "A composteira selecionada não existe.")
    except Exception as e:
        messages.error(request, f"Ocorreu um erro: {e}")

    return redirect("composteira:graficoIndividual")

#corrigir a parte de o gráfico se adaptar ao numero de compostagens do usuario

    if request.user.is_authenticated:
        if request.method == 'GET':
            composteiras = Composteira.objects.filter(fkUsuario_id=request.user)
            return render(request, "addCompostagem.html", {"composteiras": composteiras})
        else:
            data_inicio = datetime.strptime(request.POST.get("data_inicio"), '%Y-%m-%d').date()
            fkComposteira = request.POST.get("composteira")
            peso = request.POST.get("peso")

            composteira = Composteira.objects.get(id_composteira=fkComposteira)

            compostagem = Compostagem(
                fkComposteira=composteira,
                data_inicio=data_inicio,
                peso=peso,
                fkUsuario_comp=request.user
            )
            compostagem.save()

            dias, data_pronto = compostagem.calcular()

            composteiras = Composteira.objects.filter(fkUsuario=request.user)
            compostagens = Compostagem.objects.filter(
                fkUsuario_comp=request.user,
                fkComposteira__in=composteiras
            ).order_by('data_inicio')

            # Gera o mesmo dicionário 'dados' usado no gráfico individual
            dados = {}
            for c in composteiras:
                composts = compostagens.filter(fkComposteira=c)
                dados[c.id_composteira] = {
                    "labels": [comp.data_inicio.strftime("%d/%m") for comp in composts],
                    "pesos": [float(comp.peso or 0) for comp in composts],
                }

            messages.success(request, f"Compostagem salva! Adubo previsto para {data_pronto.strftime('%d/%m/%Y')} ({dias} dias).")

            return render(request, "graficoIndiv.html", {
                "compostagens": compostagens,
                "composteiras": composteiras,
                "dados": dados,   # adiciona este
                "data_pronto": data_pronto,
                "dias": dias
            })

    

def viewGraficoGeral(request):
    
    if not request.user.is_authenticated:
        return render(request, "usuarios/Login.html")

    # Filtra composteiras do usuário
    composteiras = Composteira.objects.filter(fkUsuario=request.user)

    # Pega todas as compostagens dessas composteiras
    compostagens = Compostagem.objects.filter(fkComposteira__in=composteiras)

    # Monta os dados do gráfico geral
    dados = {
        'labels': [c.data_inicio.strftime("%d/%m") for c in compostagens],
        'pesos': [float(c.peso) for c in compostagens],
        'datas': [c.data_inicio.strftime("%Y-%m-%d") for c in compostagens],
    }

    return render(request, "grafico-geral.html", {
        "composteiras": composteiras,
        "dados": dados
    })



def Emissao(request):
    if request.user.is_authenticated:
        #Filtra as composteiras associadas ao usuário
        composteiras_usuario = Composteira.objects.filter(fkUsuario=request.user)
        #Lista para armazenar os resultados
        resultados = []
        for composteira in composteiras_usuario:
            #Filtra as compostagens associadas à composteira e ao usuário
            peso_compostagem = (
                Compostagem.objects
                .filter(fkComposteira=composteira)
                .annotate(mes=ExtractMonth('data_inicio'))
                .values('mes')
                .annotate(soma_peso=Sum('peso'))
                .order_by('mes')
            )

            #Loop para iterar sobre os resultados da compostagem
            for resultado in peso_compostagem:
                mes = resultado['mes']
                soma_peso = resultado['soma_peso']
                emissao_real = f'Composteira: {composteira.nome}, Mês: {mes}, Soma do Peso: {0.084 * soma_peso}'
                #Adiciona o resultado à lista
                resultados.append(emissao_real)

        #Une os resultados em uma única string com quebras de linha HTML
        resposta = '\n'.join(resultados)
        #Retorna a resposta HTTP com todos os resultados
        return HttpResponse(resposta)


def GraficoIndividualView(request):
    composteiras = Composteira.objects.filter(fkUsuario=request.user)
    compostagens = Compostagem.objects.filter(
        fkUsuario_comp=request.user,
        fkComposteira__in=composteiras
    ).order_by('data_inicio')

    dados = {}
    for c in composteiras:
        composts = compostagens.filter(fkComposteira=c)
        dados[c.id_composteira] = {
            "labels": [comp.data_inicio.strftime("%d/%m") for comp in composts],
            "pesos": [float(comp.peso or 0) for comp in composts],
            "datas": [comp.data_inicio.strftime("%Y-%m-%d") for comp in composts],
        }

    return render(request, "graficoIndiv.html", {
        "composteiras": composteiras,
        "compostagens": compostagens,
        "dados": dados
    })





def vieweditarComposteira(request, id_composteira):
    # Verifica se o user está logado
    if request.user.is_authenticated:
        try:
            # Tenta obter a composteira pelo id_composteira e do usuário logado
            composteira = Composteira.objects.get(id_composteira=id_composteira, fkUsuario=request.user)
        except Composteira.DoesNotExist:
            return render(request, "erro.html", {"mensagem": "Composteira não encontrada"})


        if composteira.fkUsuario == request.user:    
            if request.method == 'GET':
                # Passa a composteira para o template
                return render(request, "editarComposteira.html", {"composteira": composteira})
            elif request.method == "POST":
                # Captura os dados do POST e atualiza a composteira
                composteira.nome = request.POST.get("name_comp")
                composteira.data_construcao = request.POST.get("data_const")
                composteira.regiao = request.POST.get("regiao")
                composteira.tipo = request.POST.get("tipo")
                composteira.save()
                composteiras = Composteira.objects.filter(fkUsuario_id=request.user)
                return render(request, "grafico-geral.html", {"composteiras": composteiras})
        return render(request, "usuarios/Login.html")
    
    
def viewexcluirComposteira(request, id_composteira):
    # Obtém a composteira com o id especificado
    composteira = get_object_or_404(Composteira, id_composteira=id_composteira)
    if request.method == 'POST':
        # Se a requisição for um POST, exclui a composteira
        composteira.delete()
        # Adiciona uma mensagem de sucesso informando que a composteira foi excluída com sucesso
        messages.success(request, 'Composteira excluída com sucesso!')
        # Redireciona o usuário para a página geral de gráficos das composteiras
        return redirect('composteira:graficoGeral')

    # Se a requisição for um GET, renderiza o template 'excluirComposteira.html'
    # passando a composteira para ser exibida na confirmação de exclusão
    return render(request, 'excluirComposteira.html', {'composteira': composteira})




#def seu_view(request):
    # Suponha que você já tenha as composteiras e compostagens
    composteiras = Composteira.objects.all()
    compostagens = Compostagem.objects.all()

    # Classifique as compostagens por data de início
    compostagens_ordenadas = compostagens.order_by('data_inicio')

    context = {
        'composteiras': composteiras,
        'compostagens': compostagens_ordenadas,
        # ... outras variáveis de contexto
    }
    return render(request, 'seu_template.html', context)
