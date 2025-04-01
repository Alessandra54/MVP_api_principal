from flask import Flask, jsonify, request
from flask_restx import Api, Resource, fields
import requests
from config import Config
from database import Database

app = Flask(__name__)
app.config.from_object(Config)

# Inicializando o banco de dados
db = Database()
db.init_db()

# Criação do Swagger
api = Api(app, doc="/swagger")

# Definindo os Namespaces
favoritas_ns = api.namespace('favoritas', description='Operações relacionadas às receitas favoritas')

# Definindo o Modelo para o Swagger
receita_model = api.model('Receita', {
    'titulo': fields.String(required=True, description='Título da receita'),
    'ingredientes': fields.String(required=True, description='Ingredientes da receita')
})

# Modelo de receitas favoritas no banco de dados
class ReceitaFavorita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    ingredientes = db.Column(db.String(500), nullable=False)

# Função para chamar a API do Spoonacular
def chamar_api_spoonacular(endpoint, params=None):
    url = f"{app.config['BASE_URL']}/{endpoint}"
    params = params or {}
    params['apiKey'] = app.config['SPOONACULAR_API_KEY']
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Isso irá levantar uma exceção se o status for 4xx ou 5xx
        return response.json()  # Aqui estamos retornando o JSON diretamente
    except requests.exceptions.RequestException as e:
        # Retornando um erro com o código 500 se houver falha ao chamar a API
        return {"error": str(e)}, 500

# Endpoint para adicionar e listar receitas favoritas
@favoritas_ns.route('/')
class ReceitaFavoritaLista(Resource):
    @api.doc('Listar todas as receitas favoritas')
    def get(self):
        try:
            receitas = ReceitaFavorita.query.all()
            resultado = [{"id": r.id, "titulo": r.titulo, "ingredientes": r.ingredientes} for r in receitas]
            return jsonify(resultado)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @api.doc('Adicionar uma nova receita favorita')
    @api.expect(receita_model)
    def post(self):
        try:
            dados = request.json
            if not dados or 'titulo' not in dados or 'ingredientes' not in dados:
                return jsonify({"error": "Campos 'titulo' e 'ingredientes' são obrigatórios"}), 400

            nova_receita = ReceitaFavorita(titulo=dados['titulo'], ingredientes=dados['ingredientes'])
            db.session.add(nova_receita)
            db.session.commit()

            return jsonify({"message": "Receita adicionada com sucesso!"}), 201
        except Exception as e:
            # Exibindo mensagem de erro para ajudar a depurar
            return jsonify({"error": "Erro ao adicionar a receita", "details": str(e)}), 500

# Endpoint para buscar e deletar uma receita favorita por ID
@favoritas_ns.route('/<int:id>')
class ReceitaFavoritaDetalhe(Resource):
    @api.doc('Buscar uma receita favorita pelo ID')
    def get(self, id):
        try:
            receita = ReceitaFavorita.query.get(id)
            if not receita:
                return jsonify({"error": "Receita não encontrada"}), 404
            return jsonify({"id": receita.id, "titulo": receita.titulo, "ingredientes": receita.ingredientes})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @api.doc('Remover uma receita favorita pelo ID')
    def delete(self, id):
        try:
            receita = ReceitaFavorita.query.get(id)
            if not receita:
                return jsonify({"error": "Receita não encontrada"}), 404
            
            db.session.delete(receita)
            db.session.commit()
            return jsonify({"message": "Receita removida com sucesso!"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
