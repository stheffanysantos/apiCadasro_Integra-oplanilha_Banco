from flask import Flask, render_template
from sync import sync_with_sheetdb  # cSpell:ignore sheetdb 

app = Flask(__name__)

# Rota principal que irá renderizar o template com o botão
@app.route('/')
def index():
    return render_template('index.html')

# Rota para iniciar a sincronização via um clique
@app.route('/sync', methods=['GET'])
def sync():
    try:
        # Chama a função de sincronização que irá rodar o código Python de sincronização
        sync_with_sheetdb()  
        return "Sincronização concluída com sucesso!"  # Retorna uma mensagem de sucesso
    except Exception as e:
        return f"Ocorreu um erro na sincronização: {str(e)}"  # Retorna uma mensagem de erro caso algo dê errado

if __name__ == '__main__':
    app.run(debug=True)
