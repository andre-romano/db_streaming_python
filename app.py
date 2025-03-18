
from datetime import datetime

from flask import Flask, request, render_template

from db.db import executar_insert_delete_update, executar_select

from utils.functions import get_env

# Create a Flask application
app = Flask(__name__)

##################
#     TELAS      #
##################


@app.route('/', methods=['GET'])
def home():
    return render_template('index.jinja2')


@app.route("/atualizar/video", methods=['GET'])
def tela_atualizar_video():
    # classificacoes dos videos ( formato [ (id, nome) ] )
    classificacoes = executar_select(
        db="streaming",
        consulta_sql="""
                SELECT id, nome
                FROM Classificacao
            """
    )

    # conecta com o banco e executa o comando SQL
    registros = executar_select(
        db="streaming",
        consulta_sql="""
            SELECT id, ano, titulo, sinopse, duracao, id_classificacao
            FROM Video 
            WHERE id = %s
        """,
        parametros=(
            # pegue os dados enviados pelo usuario
            request.args.get('id'),
        )
    )

    if len(registros) <= 0:
        return "ERRO: Consulta de video falhou. Veja logs do Python para detalhes."
    id, ano, titulo, sinopse, duracao, id_classificacao = registros[0]

    # converter duracao do formato HH:MM:SS para HH:MM
    duracao_formatada = datetime.strptime(
        str(duracao), "%H:%M:%S").strftime("%H:%M")

    return render_template(
        "atualizar/video.jinja2",
        api=f"/api/atualizar/video",
        classificacoes=classificacoes,
        id=id,
        ano=ano,
        titulo=titulo,
        sinopse=sinopse,
        duracao=duracao_formatada,
        id_classificacao=id_classificacao,
    )


@app.route("/cadastrar/video", methods=['GET'])
def tela_cadastrar_video():

    # classificacoes dos videos ( formato [ (id, nome) ] )
    classificacoes = executar_select(
        db="streaming",
        consulta_sql="""
                SELECT id, nome
                FROM Classificacao
            """
    )

    return render_template(
        f"cadastrar/video.jinja2",
        api=f"/api/cadastrar/video",
        classificacoes=classificacoes,
    )


@app.route("/consultar/video", methods=['GET'])
def tela_consultar_video():
    # conecta com o banco e executa o comando SQL
    registros = executar_select(
        db="streaming",
        consulta_sql="""
            SELECT v.id, ano, titulo, sinopse, duracao, c.nome
            FROM Video v, Classificacao c
            WHERE v.id_classificacao = c.id
        """
    )

    # cabecalho da tabela Video (ordem das colunas)
    cabecalho = ["ID", "Ano", "Titulo", "Sinopse", "Duracao", "Classificacao"]

    return render_template(
        f"consultar/video.jinja2",
        api_atualizar="/atualizar/video",
        api_apagar="/api/apagar/video",
        cabecalho=cabecalho,
        dados=registros,
    )

################
#     API      #
################


@app.route('/api/cadastrar/video', methods=['POST'])
def api_cadastrar_video():
    # conecta com o banco e executa o comando SQL
    qtd_linhas = executar_insert_delete_update(
        db="streaming",
        consulta_sql="""
            INSERT INTO  Video (ano, titulo, sinopse, duracao, id_classificacao)
            VALUES             (  %s,    %s,      %s   ,  %s     ,   %s  ) 
        """,
        parametros=(
            # pegue os dados enviados pelo usuario
            request.form.get('ano'),
            request.form.get('titulo'),
            request.form.get('sinopse'),
            request.form.get('duracao'),
            request.form.get('id_classificacao'),
        )
    )
    if qtd_linhas < 0:
        return "ERRO: Insercao mal feita. Veja os logs do Python para detalhes."
    return f"SUCESSO: {qtd_linhas} videos inseridos no DB. Retorne para a pagina /consultar/video para ver o resultado."


@app.route('/api/atualizar/video', methods=['POST'])
def api_atualizar_video():
    print([request.form.get('ano'),
           request.form.get('titulo'),
           request.form.get('sinopse'),
           request.form.get('duracao'),
           request.form.get('id_classificacao'),
           request.form.get('id'),])

    # conecta com o banco e executa o comando SQL
    qtd_linhas = executar_insert_delete_update(
        db="streaming",
        consulta_sql="""
            UPDATE  Video 
            SET ano = %s, titulo = %s, sinopse = %s, duracao = %s, id_classificacao = %s
            WHERE id = %s
        """,
        parametros=(
            # pegue os dados enviados pelo usuario
            request.form.get('ano'),
            request.form.get('titulo'),
            request.form.get('sinopse'),
            request.form.get('duracao'),
            request.form.get('id_classificacao'),
            request.form.get('id'),
        )
    )
    if qtd_linhas < 0:
        return "ERRO: Atualizacao mal feita. Veja os logs do Python para detalhes."
    return f"SUCESSO: {qtd_linhas} videos atualizados no DB. Retorne para a pagina /consultar/video para ver o resultado."


@app.route('/api/apagar/video', methods=['POST'])
def api_apagar_video():
    # conecta com o banco e executa o comando SQL
    qtd_linhas = executar_insert_delete_update(
        db="streaming",
        consulta_sql="""
            DELETE FROM Video
            WHERE id = %s
        """,
        parametros=(
            # pegue os dados enviados pelo usuario
            request.form.get('id'),
        )
    )
    if qtd_linhas < 0:
        return "ERRO: Delete mal feito. Veja os logs do Python para detalhes."
    return f"SUCESSO: {qtd_linhas} videos deletados no DB. Retorne para a pagina /consultar/video para ver o resultado."


# Run the Flask application
if __name__ == '__main__':
    app.run(debug=get_env('APP_DEBUG', False), port=get_env('APP_PORT', 5000),)
