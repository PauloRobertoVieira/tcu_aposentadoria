from app import app, db
from models.pessoa import Pessoa

with app.app_context():
    pessoas = Pessoa.query.all()
    for pessoa in pessoas:
        if not pessoa.url_consulta:
            pessoa.url_consulta = f"https://pesquisa.apps.tcu.gov.br/#/atos/consultar?termo=*&filtro=CPF:{pessoa.cpf}"
    db.session.commit()
    print("URLs atualizadas para todas as pessoas")


"""
from app import app, db
from models.pessoa import Pessoa
from services.tcu_service import consultar_status_aposentadoria

with app.app_context():
    pessoas = Pessoa.query.all()
    for pessoa in pessoas:
        consultar_status_aposentadoria(pessoa.id)
"""