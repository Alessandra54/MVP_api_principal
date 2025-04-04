from flask import Flask, jsonify, request
from flask_restx import Api, Resource, fields
import requests
from config import Config
from database import Database, db

app = Flask(__name__)
app.config.from_object(Config)

# Inicializa banco
database = Database()
database.init_app(app)
with app.app_context():
    database.init_db(app)

# Swagger
api = Api(app, doc="/swagger")

# Namespaces
receitas_ns = api.namespace('receitas', description='Operações relacionadas a receitas')
alimentos_ns = api.namespace('alimentos', description='Operações relacionadas a alimentos')
categorias_ns = api.namespace('categorias', description='Operações relacionadas a categorias de refeições')

# Modelo para criação e atualização
receita_model = api.model('Receita', {
    'nome': fields.String(required=True, description='Nome da receita'),
    'ingredientes': fields.String(required=True, description='Ingredientes da receita')
})

# Função auxiliar: chamada à Spoonacular
def chamar_api_spoonacular(endpoint, params=None):
    url = f"{app.config['BASE_URL']}/{endpoint}"
    params = params or {}
    params['apiKey'] = app.config['SPOONACULAR_API_KEY']

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}, 500

# 🔹 GET receitas por ingredientes (Spoonacular)
@receitas_ns.route('/')
class BuscarReceitas(Resource):
    @api.doc('Buscar receitas por ingredientes')
    @api.param('ingredientes', 'Lista de ingredientes separados por vírgula')
    def get(self):
        ingredientes = request.args.get('ingredientes')
        if not ingredientes:
            return jsonify({"error": "Parâmetro 'ingredientes' é necessário"}), 400

        params = {'ingredients': ingredientes, 'number': 5}
        dados = chamar_api_spoonacular('recipes/findByIngredients', params)
        return jsonify(dados)



# 🔹 GET categorias (mock local)
@categorias_ns.route('/')
class ListarCategorias(Resource):
    @api.doc('Listar categorias de refeições')
    def get(self):
        categorias = [
            "Café da manhã", "Almoço", "Jantar", "Sobremesa", "Lanche"
        ]
        return jsonify(categorias)

# 🔹 GET dados nutricionais por alimento (Spoonacular)
@alimentos_ns.route('/<string:nome>')
class BuscarAlimento(Resource):
    @api.doc('Buscar informações nutricionais de um alimento')
    def get(self, nome):
        params = {'query': nome}
        dados = chamar_api_spoonacular('food/search', params)
        return jsonify(dados)

# 🔹 GET e POST banco local
@receitas_ns.route('/banco')
class ReceitaBanco(Resource):
    @api.doc('Listar todas as receitas do banco de dados')
    def get(self):
        receitas = database.get_receitas()
        return jsonify(receitas)

    @api.doc('Adicionar uma nova receita ao banco de dados')
    @api.expect(receita_model)
    def post(self):
        data = request.json
        database.add_receita(data['nome'], data['ingredientes'])
        return jsonify({"message": "Receita adicionada com sucesso!"})

# 🔹 PUT e DELETE banco local
@receitas_ns.route('/banco/<int:id>')
class ReceitaBancoDetalhes(Resource):
    @api.doc('Atualizar uma receita no banco de dados')
    @api.expect(receita_model)
    def put(self, id):
        data = request.json
        database.update_receita(id, data['nome'], data['ingredientes'])
        return jsonify({"message": "Receita atualizada com sucesso!"})

    @api.doc('Deletar uma receita do banco de dados')
    def delete(self, id):
        database.delete_receita(id)
        return jsonify({"message": "Receita deletada com sucesso!"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
