from django.shortcuts import render
from django.http import JsonResponse

def dashboard(request):
    total_pessoas = 100
    aguardando = 20
    concedidas = 60
    ilegais = 20

    dados_grafico = [aguardando or 0, concedidas or 0, ilegais or 0]

    return render(request, 'dashboard.html', {
        'total_pessoas': total_pessoas,
        'aguardando': aguardando,
        'concedidas': concedidas,
        'ilegais': ilegais,
        'dados_grafico': dados_grafico
    })

def dados_dashboard(request):
    aguardando = 18
    concedidas = 62
    ilegais = 20

    dados_grafico = [aguardando or 0, concedidas or 0, ilegais or 0]
    return JsonResponse({'dados_grafico': dados_grafico})
