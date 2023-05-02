import plotly
from flask import Flask, render_template, jsonify
import pandas as pd
import plotly.graph_objs as go
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/images')
def images():
    image_dir = 'static/graficos/'
    image_files = [f for f in os.listdir(image_dir) if f.endswith('.png')]
    return jsonify(image_files)


@app.route('/data')
def data():
    # Execute o código para gerar o gráfico
    df = pd.read_csv('resultados_agricultura.csv', encoding='ISO-8859-1')
    fig = go.Figure()
    for coluna in df.columns:
        if coluna != 'Mes':
            fig.add_trace(go.Scatter(x=df['Mes'], y=df[coluna], mode='lines', name=coluna))
    fig.update_layout(xaxis_title='Mês', yaxis_title='Quantidade de água (litros)',
                      title='Quantidade de água utilizada por área')
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

if __name__ == '__main__':
    app.run(debug=True, port=5001)