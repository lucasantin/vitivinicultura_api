from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from .resources.producao import ProducaoResource
from .resources.processamento import ProcessamentoResource
from .resources.comercializacao import ComercializacaoResource
from .resources.importacao import ImportacaoResource
from .resources.exportacao import ExportacaoResource
from .resources.auth import UserLogin, UserRegister

def create_app():
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Substitua com sua própria chave secreta
    app.config['SWAGGER'] = {
        'title': 'Vitivinicultura API',
        'uiversion': 3,
        'specs': [
            {
                'endpoint': 'apispec_1',
                'route': '/apispec_1.json',
                'rule_filter': lambda rule: True,  # all in
                'model_filter': lambda tag: True,  # all in
            }
        ],
        'static_url_path': "/flasgger_static",
        'swagger_ui': True,
        'specs_route': "/apidocs/"
    }

    jwt = JWTManager(app)
    api = Api(app)
    swagger = Swagger(app)
    
    api.add_resource(ProducaoResource, '/producao/<int:ano>')
    api.add_resource(ProcessamentoResource, '/processamento/<int:ano>')
    api.add_resource(ComercializacaoResource, '/comercializacao/<int:ano>')
    api.add_resource(ImportacaoResource, '/importacao/<int:ano>')
    api.add_resource(ExportacaoResource, '/exportacao/<int:ano>')
    api.add_resource(UserLogin, '/login')
    api.add_resource(UserRegister, '/register')
    
    return app
