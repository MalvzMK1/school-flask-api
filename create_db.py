from app import app  # Importe a instância do seu app Flask
from src.models import db

# Certificando-se de que estamos dentro do contexto da aplicação
with app.app_context():
    db.create_all()  # Cria todas as tabelas no banco de dados
    print("Banco de dados e tabelas criados com sucesso!")
