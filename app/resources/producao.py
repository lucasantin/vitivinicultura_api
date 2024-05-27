from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flasgger import swag_from
from app.utils.scraper import fetch_data
from flask import Blueprint, jsonify, request

bp = Blueprint('producao', __name__)

@bp.route('/producao',methods=['POST'])

class ProducaoResource(Resource):
    @swag_from({
        'tags': ['Producao'],
        'parameters': [
            {
                'name': 'ano',
                'in': 'path',
                'type': 'integer',
                'required': True,
                'description': 'Ano para filtrar os dados'
            }
        ],
        'responses': {
            '200': {
                'description': 'Dados processados com sucesso',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'data': {
                            'type': 'array',
                            'items': {
                                'type': 'object'
                            }
                        }
                    }
                }
            },
            '404': {
                'description': 'Dados não encontrados'
            }
        }
    })
    #@jwt_required()
    def get(self, ano):  # O método get deve receber o parâmetro ano
        # Adicionando logs para depuração
        url = f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_02'
        data = fetch_data(url)
        if data:
            return data, 200
        return {'message': 'Data not found'}, 404
