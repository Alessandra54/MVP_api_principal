import os

class Config:
    # Definindo a chave da API Spoonacular (pode ser armazenada como variável de ambiente)
    SPOONACULAR_API_KEY = os.getenv('SPOONACULAR_API_KEY', '04773d54c6eb43f99a167f034d52bca3')
    BASE_URL = 'https://api.spoonacular.com'
