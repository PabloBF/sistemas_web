from extensions import db
from flask_login import UserMixin

class Credor(UserMixin, db.Model):
    __tablename__ = 'credor'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    cidade = db.Column(db.String(50), nullable=False)
    estado = db.Column(db.String(50), nullable=False)
    titles = db.relationship('Title', backref='creditor', lazy=True)

    def serialize(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'cidade': self.cidade,
            'estado': self.estado
        }


class Title(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creditor_id = db.Column(db.Integer, db.ForeignKey('credor.id'), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)  # Numeric com 2 casas decimais
    month = db.Column(db.Integer, nullable=False)  # Mês como inteiro
    year = db.Column(db.Integer, nullable=False)  # Ano como inteiro
    status = db.Column(db.String(20), nullable=False)  # Status pode ser 'paga', 'atrazo', 'devendo'

    def serialize(self):
        return {
            'id': self.id,
            'description': self.description,
            'amount': str(self.amount),  # Converter para string se necessário para o formato
            'status': self.status,
            'creditor_id': self.creditor_id,
            'month': int(self.month),  # Garantir que o mês é um inteiro
            'year': int(self.year)  # Garantir que o ano é um inteiro
        }
