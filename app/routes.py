from flask import Blueprint, request, jsonify, render_template
from app.database import db
from app.models import Imovel

bp = Blueprint('main', __name__)

# Rota para listar todos os imóveis
@bp.route('/imoveis', methods=['GET'])
def listar_imoveis():
    return jsonify([])

# Rota para buscar um imóvel pelo ID
@bp.route('/imoveis/<int:id>', methods=['GET'])
def buscar_imovel(id):
    return jsonify({}), 404

# Rota para adicionar um novo imóvel
@bp.route('/imoveis', methods=['POST'])
def adicionar_imovel():
    return jsonify({}), 201

# Rota para atualizar um imóvel existente
@bp.route('/imoveis/<int:id>', methods=['PUT'])
def atualizar_imovel(id):
    return jsonify()

# Rota para remover um imóvel
@bp.route('/imoveis/<int:id>', methods=['DELETE'])
def remover_imovel(id):
    return jsonify({})

# Rota para listar imóveis por tipo
@bp.route('/imoveis/tipo', methods=['GET'])
def listar_por_tipo():
    return jsonify({})

# Rota para listar imóveis por cidade
@bp.route('/imoveis/cidade', methods=['GET'])
def listar_por_cidade():
    return jsonify({})