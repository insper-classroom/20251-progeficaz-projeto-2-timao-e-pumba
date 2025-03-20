from flask import Blueprint, request, jsonify, render_template
from app.database import db
from app.models import Imovel

bp = Blueprint('main', __name__)

# 🔹 Nova rota para renderizar o HTML
@bp.route('/')
def index():
    return render_template('index.html')  # Certifique-se de que 'index.html' está na pasta 'templates'

# Rota para listar todos os imóveis
@bp.route('/imoveis', methods=['GET'])
def listar_imoveis():
    tipo = request.args.get('tipo')
    cidade = request.args.get('cidade')
    imoveis = []
    if cidade:
        imoveis = Imovel.query.filter_by(cidade=cidade).all()
    elif tipo:
        imoveis = Imovel.query.filter_by(tipo=tipo).all()
    else:
        imoveis = Imovel.query.all()
    return jsonify([imovel.to_dict() for imovel in imoveis])

# Rota para buscar um imóvel pelo ID
@bp.route('/imoveis/<int:id>', methods=['GET'])
def buscar_imovel(id):
    imovel = db.session.get(Imovel, id)
    if imovel:
        return jsonify(imovel.to_dict())
    return jsonify({"erro": "Imóvel não encontrado"}), 404

# Rota para adicionar um novo imóvel
@bp.route('/imoveis', methods=['POST'])
def adicionar_imovel():
    dados = request.json
    novo_imovel = Imovel(
        logradouro=dados['logradouro'],
        cidade=dados['cidade'],
        tipo=dados['tipo'],
        valor=dados['valor']
    )
    db.session.add(novo_imovel)
    db.session.commit()
    return jsonify(novo_imovel.to_dict()), 201

# Rota para atualizar um imóvel existente
@bp.route('/imoveis/<int:id>', methods=['PUT'])
def atualizar_imovel(id):
    imovel = db.session.get(Imovel, id)
    if not imovel:
        return jsonify({"erro": "Imóvel não encontrado"}), 404
    
    dados = request.json
    imovel.logradouro = dados.get('logradouro', imovel.logradouro)
    imovel.cidade = dados.get('cidade', imovel.cidade)
    imovel.tipo = dados.get('tipo', imovel.tipo)
    imovel.valor = dados.get('valor', imovel.valor)
    
    db.session.commit()
    return jsonify(imovel.to_dict())

# Rota para remover um imóvel
@bp.route('/imoveis/<int:id>', methods=['DELETE'])
def remover_imovel(id):
    imovel = db.session.get(Imovel, id)
    if not imovel:
        return jsonify({"erro": "Imóvel não encontrado"}), 404
    
    db.session.delete(imovel)
    db.session.commit()
    return jsonify({"mensagem": "Imóvel removido com sucesso"})

# Rota para listar imóveis por tipo
@bp.route('/imoveis/tipo', methods=['GET'])
def listar_por_tipo():
    tipo = request.args.get('tipo')
    imoveis = []
    if tipo:
        imoveis = Imovel.query.filter_by(tipo=tipo).all()
    return jsonify([imovel.to_dict() for imovel in imoveis])

# Rota para listar imóveis por cidade
@bp.route('/imoveis/cidade', methods=['GET'])
def listar_por_cidade():
    cidade = request.args.get('cidade')
    imoveis = []
    if cidade:
        imoveis = Imovel.query.filter_by(cidade=cidade).all()
    return jsonify([imovel.to_dict() for imovel in imoveis])