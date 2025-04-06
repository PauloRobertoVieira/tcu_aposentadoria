from .pessoa import db


class HistoricoConsulta(db.Model):
    __tablename__ = 'historico_consultas'
    
    id = db.Column(db.Integer, primary_key=True)
    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoas.id'), nullable=False)
    data_consulta = db.Column(db.DateTime, default=db.func.now())
    status = db.Column(db.String(100))
    detalhes = db.Column(db.Text)
    url_consulta = db.Column(db.String(500))
    
    def to_dict(self):
        return {
            'id': self.id,
            'data_consulta': self.data_consulta.isoformat(),
            'status': self.status,
            'detalhes': self.detalhes
        }