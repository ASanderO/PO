from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'Olá, bem vindo ao meu perfil do LinkedIn!'
@app.route('/contratando')
def contratando():
    contratando = True # Aqui você pode implementar sua lógica para verificar se a pessoa está contratando ou não
    if contratando:
        return 'Entre em contato comigo no privado!'
    else:
        return 'Obrigado por passar pelo meu perfil, sinta-se à vontade para me seguir!'
if __name__ == '__main__':
    app.run()