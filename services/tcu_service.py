import requests
from models.pessoa import Pessoa
from models.historico import HistoricoConsulta
from models.pessoa import db


def consultar_status_aposentadoria(pessoa_id):
    pessoa = Pessoa.query.get(pessoa_id)
    if not pessoa:
        return False

    # Remove pontuação do CPF
    cpf_limpo = pessoa.cpf.replace('.', '').replace('-', '')
    
    # URL formatada corretamente para a interface web do TCU
    web_url = (
        f"https://pesquisa.apps.tcu.gov.br/resultado/ato-pessoal/*/"
        f"CPF%253A%2522{cpf_limpo}%2522"
    )

    try:
        # Consulta à API para obter os dados
        api_url = "https://pesquisa.apps.tcu.gov.br/rest/publico/base/ato-pessoal/documentosResumidos"
        params = {
            "termo": "*",
            "filtro": f"CPF:{cpf_limpo}",
            "ordenacao": "DTVIGENCIAATO desc",
            "quantidade": "10",
            "inicio": "0"
        }

        response = requests.get(api_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        resultados = data.get('documentos', [])
        status_atual = "Status não disponível"
        detalhes = []
        
        for doc in resultados:
            tipo_ato = doc.get('tipoAto', '').lower()
            if 'aposentadoria' in tipo_ato:
                status = doc.get('situacao', '')
                data_vigencia = doc.get('dataVigenciaAto', '')
                detalhes.append(f"Data: {data_vigencia}; Tipo Ato: {tipo_ato}; Status: {status}")
                
                if status:
                    status_atual = status

        # Atualiza os dados da pessoa
        pessoa.status = status_atual
        pessoa.url_consulta = web_url  # Usa a URL formatada para a interface web
        
        registro = HistoricoConsulta(
            pessoa_id=pessoa.id,
            status=status_atual,
            detalhes="\n".join(detalhes) if detalhes else "Nenhum detalhe disponível",
            url_consulta=web_url
        )
        
        db.session.add(registro)
        db.session.commit()
        return True

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição para {pessoa.nome}: {str(e)}")
        pessoa.url_consulta = web_url  # Mantém a URL formatada mesmo em caso de erro
        db.session.commit()
        return False
    except Exception as e:
        print(f"Erro inesperado ao consultar TCU para {pessoa.nome}: {str(e)}")
        pessoa.url_consulta = web_url
        db.session.commit()
        return False


def consultar_todos():
    """Consulta o status de todas as pessoas ativas no sistema"""
    try:
        pessoas = Pessoa.query.filter_by(ativo=True).all()
        for pessoa in pessoas:
            consultar_status_aposentadoria(pessoa.id)
        return True
    except Exception as e:
        print(f"Erro ao consultar todos: {str(e)}")
        return False