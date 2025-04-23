from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from models.pessoa import db, Pessoa
from models.historico import HistoricoConsulta
from services.tcu_service import consultar_status_aposentadoria
from services.scheduler import agendar_tarefas
import os
from datetime import datetime

app = Flask(__name__)
app.config.from_object('config.Config')

db.init_app(app)

with app.app_context():
    db.create_all()

agendar_tarefas(app)

ultima_atualizacao = datetime.now()


@app.route('/')
def index():
    total_pessoas = Pessoa.query.count()
    aguardando = Pessoa.query.filter_by(status='Aguardando autuação').count()
    concedidas = Pessoa.query.filter_by(status='Concedida').count()
    ilegais = Pessoa.query.filter_by(status='Apreciado ilegal').count()

   
    return render_template('index.html', 
                           total_pessoas=total_pessoas,
                           aguardando=aguardando,
                           concedidas=concedidas,
                           ilegais=ilegais,
                           ultima_atualizacao=ultima_atualizacao)


@app.route('/verificar_atualizacoes', methods=['GET'])
def verificar_atualizacoes():
    global ultima_atualizacao
    
    
    pessoas = Pessoa.query.all()
    alteracoes = []
    
    for pessoa in pessoas:
        if pessoa.status_atualizado_em > ultima_atualizacao:
            alteracoes.append(pessoa)
    
    ultima_atualizacao = datetime.now()  
    
    
    if alteracoes:
        return jsonify({"atualizacoes": len(alteracoes), "alteracoes_detectadas": True})
    
    return jsonify({"atualizacoes": 0, "alteracoes_detectadas": False})


@app.route('/pessoas')
def listar_pessoas():
    pessoas = Pessoa.query.order_by(Pessoa.nome).all()
    return render_template('pessoas.html', pessoas=pessoas)


@app.route('/pessoa/<int:id>')
def detalhes_pessoa(id):
    pessoa = Pessoa.query.get_or_404(id)
    historico = HistoricoConsulta.query.filter_by(pessoa_id=id).order_by(HistoricoConsulta.data_consulta.desc()).all()
    return render_template('detalhes.html', pessoa=pessoa, historico=historico)


@app.route('/pessoa/cadastrar', methods=['GET', 'POST'])
def cadastrar_pessoa():
    if request.method == 'POST':
        matricula = request.form['matricula']
        nome = request.form['nome']
        cpf = request.form['cpf'].replace('.', '').replace('-', '')
        
        nova_pessoa = Pessoa(matricula=matricula, nome=nome, cpf=cpf)
        db.session.add(nova_pessoa)
        db.session.commit()
        
        consultar_status_aposentadoria(nova_pessoa.id)
        
        return redirect(url_for('listar_pessoas'))
    
    return render_template('cadastro.html')


@app.route('/pessoa/editar/<int:id>', methods=['GET', 'POST'])
def editar_pessoa(id):
    pessoa = Pessoa.query.get_or_404(id)
    
    if request.method == 'POST':
        pessoa.matricula = request.form['matricula']
        pessoa.nome = request.form['nome']
        pessoa.cpf = request.form['cpf'].replace('.', '').replace('-', '')
        pessoa.ativo = 'ativo' in request.form
        
        db.session.commit()
        return redirect(url_for('detalhes_pessoa', id=id))
    
    return render_template('editar.html', pessoa=pessoa)


@app.route('/pessoa/excluir/<int:id>')
def excluir_pessoa(id):
    pessoa = Pessoa.query.get_or_404(id)
    db.session.delete(pessoa)
    db.session.commit()
    return redirect(url_for('listar_pessoas'))


@app.route('/api/pessoas')
def api_pessoas():
    pessoas = Pessoa.query.all()
    return jsonify([p.to_dict() for p in pessoas])


@app.route('/api/pessoas/<cpf>/historico')
def api_historico(cpf):
    pessoa = Pessoa.query.filter_by(cpf=cpf).first_or_404()
    historico = HistoricoConsulta.query.filter_by(pessoa_id=pessoa.id).all()
    return jsonify([h.to_dict() for h in historico])


@app.route('/relatorio')
def relatorio():
    pessoas = Pessoa.query.order_by(Pessoa.nome).all()
    now = datetime.now()  
    return render_template('relatorio.html', pessoas=pessoas, now=now)


if __name__ == '__main__':
    app.run(debug=True)
