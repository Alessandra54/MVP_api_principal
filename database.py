from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Database:
    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Inicializa a conexão do banco com o app Flask."""
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(app)

    def init_db(self, app):
        """Cria as tabelas no banco de dados dentro do contexto do Flask."""
        with app.app_context():
            db.create_all()

    def add_receita(self, nome, ingredientes):
        """Adiciona uma nova receita ao banco."""
        nova_receita = Receita(nome=nome, ingredientes=ingredientes)
        db.session.add(nova_receita)
        db.session.commit()

    def get_receitas(self):
        """Retorna todas as receitas cadastradas."""
        receitas = Receita.query.all()
        return [{"id": r.id, "nome": r.nome, "ingredientes": r.ingredientes} for r in receitas]

    def update_receita(self, id, nome, ingredientes):
        """Atualiza uma receita pelo ID."""
        receita = Receita.query.get(id)
        if receita:
            receita.nome = nome
            receita.ingredientes = ingredientes
            db.session.commit()

    def delete_receita(self, id):
        """Deleta uma receita pelo ID."""
        receita = Receita.query.get(id)
        if receita:
            db.session.delete(receita)
            db.session.commit()

# Modelo da Receita
class Receita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    ingredientes = db.Column(db.Text, nullable=False)
