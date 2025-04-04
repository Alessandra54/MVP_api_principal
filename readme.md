# 📌 API Principal - Sistema de Refeições e Nutrição

## 📖 Descrição
A **API Principal** é responsável por interagir com a API do Spoonacular para buscar informações sobre receitas, ingredientes e categorias de refeições. Essa API permite que os usuários pesquisem receitas com base nos ingredientes disponíveis, obtenham detalhes nutricionais de alimentos e acessem categorias de refeições.

---

## 🚀 Tecnologias Utilizadas
- **Python 3**
- **Flask**
- **Flask-RESTX** (para documentação Swagger)
- **Requests** (para chamadas à API externa)
- **Spoonacular API** (API externa para dados de receitas e nutrição)

---

## 🛠️ Instalação e Configuração

### 📌 Pré-requisitos
Certifique-se de ter os seguintes itens instalados em seu ambiente:
- Python 3.8+
- Virtualenv 

### 🖥️ Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/api-principal.git
   cd api-principal
   ```

2. **Crie um ambiente virtual (opcional, mas recomendado):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Para Linux/macOS
   venv\Scripts\activate  # Para Windows
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente:**
   - Crie um arquivo `.env` na raiz do projeto e adicione:
     ```ini
     SPOONACULAR_API_KEY=your_api_key_here
     BASE_URL=https://api.spoonacular.com
     ```

5. **Execute a aplicação:**
   ```bash
   python app.py
   ```

6. **Acesse a API:**
   - API: `http://localhost:5000`
   - Swagger: `http://localhost:5000/swagger`

---

## 📌 Endpoints Disponíveis

### 🥗 Receitas
- `GET /api/receitas?ingredientes=tomate,queijo` - Busca receitas com base nos ingredientes informados.
- `GET /api/receitas/banco` - Busca as receitas adicionadas no banco

- `POST /api/receitas/banco` - Adiciona as receitas no banco

- `PUT /api/receitas/banco/{id}` - Atualiza as receitas no banco

- `Delete /api/receitas/banco/{id}` - Atualiza as receitas no banco

### 🍎 Alimentos
- `GET /api/alimento/{nome}` - Busca informações nutricionais de um alimento específico.

### 📌 Categorias
- `GET /api/categorias` - Lista categorias de refeições disponíveis.

---

## 🏗 Arquitetura da Aplicação
A aplicação segue uma arquitetura baseada em Flask, estruturada para facilitar a escalabilidade e organização do código. A comunicação entre a API Principal e a Spoonacular API ocorre via chamadas HTTP.

### 🔍 Fluxograma
![Arquitetura da Aplicação](/fluxograma.png) 
---

## 📜 Licença
Este projeto está licenciado sob a licença MIT. Sinta-se à vontade para usar e modificar conforme necessário.

---

## 🤝 Contribuição
Caso queira contribuir com melhorias, siga os passos:
1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/minha-feature`)
3. Faça o commit das suas alterações (`git commit -m 'Adicionando minha feature'`)
4. Faça o push para a branch (`git push origin feature/minha-feature`)
5. Abra um Pull Request 🚀

---

