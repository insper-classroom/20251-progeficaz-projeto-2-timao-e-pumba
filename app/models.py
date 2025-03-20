from app.database import db

# Modelo de Imóvel
class Imovel(db.Model):
    __tablename__ = 'imoveis'
    id = db.Column(db.Integer, primary_key=True)
    logradouro = db.Column(db.String(200), nullable=True)
    tipo_logradouro = db.Column(db.String(100), nullable=True)
    bairro = db.Column(db.String(100), nullable=True)
    cidade = db.Column(db.String(100), nullable=True)
    cep = db.Column(db.String(10), nullable=True)
    tipo = db.Column(db.String(50), nullable=True)
    valor = db.Column(db.Float, nullable=True)
    data_aquisicao = db.Column(db.String(10), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "logradouro": self.logradouro,
            "tipo_logradouro": self.tipo_logradouro,
            "bairro": self.bairro,
            "cidade": self.cidade,
            "cep": self.cep,
            "tipo": self.tipo,
            "valor": self.valor,
            "data_aquisicao": self.data_aquisicao
        }