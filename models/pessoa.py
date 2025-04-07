# models/pessoa.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Pessoa(db.Model):
    __tablename__ = 'pessoas'
    
    id = db.Column(db.Integer, primary_key=True)
    matricula = db.Column(db.String(20), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), nullable=False, unique=True)
    status = db.Column(db.String(100))
    url_consulta = db.Column(db.String(500))
    ativo = db.Column(db.Boolean, default=True)
    data_cadastro = db.Column(db.DateTime, default=db.func.now())
    data_atualizacao = db.Column(db.DateTime, onupdate=db.func.now())
    
    historico = db.relationship('HistoricoConsulta', 
                              backref='pessoa', 
                              cascade="all, delete-orphan",
                              lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'matricula': self.matricula,
            'nome': self.nome,
            'cpf': self.cpf,
            'status': self.status,
            'ativo': self.ativo
        }