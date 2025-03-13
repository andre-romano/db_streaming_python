from flask import Flask, request, render_template

from db.db import executar_insert_delete_update, executar_select

# Create a Flask application
app = Flask(__name__)

##################
#     TELAS      #
##################


@app.route('/')
def home():
    return render_template('index.jinja2')


@app.route("/atualizar/video")
def tela_atualizar_video():
    # classificacoes dos videos ( formato [ (id, nome) ] )
    classificacoes = executar_select(
        db="streaming",
        consulta_sql="""
                SELECT id, nome
                FROM classificacao
            """
    )

    # conecta com o banco e executa o comando SQL
    registros = executar_select(
        db="streaming",
        consulta_sql="""
            SELECT ano, titulo, sinopse, duracao, id_classificacao
            FROM video 
            WHERE id = %s
        """,
        parametros=(
            # pegue os dados enviados pelo usuario
            request.form.get('id'),
        )
    )

    if len(registros) <= 0:
        return "ERRO: Consulta de video falhou. Veja logs do Python para detalhes."
    ano, titulo, sinopse, duracao, id_classificacao = registros[0]

    return render_template(
        "atualizar/video.jinja2",
        api=f"/api/atualizar/video",
        classificacoes=classificacoes,
        ano=ano,
        titulo=titulo,
        sinopse=sinopse,
        duracao=duracao,
        id_classificacao=id_classificacao,
    )


@app.route("/cadastrar/video")
def tela_cadastrar_video():

    # classificacoes dos videos ( formato [ (id, nome) ] )
    classificacoes = executar_select(
        db="streaming",
        consulta_sql="""
                SELECT id, nome
                FROM classificacao
            """
    )

    return render_template(
        f"cadastrar/video.jinja2",
        api=f"/api/cadastrar/video",
        classificacoes=classificacoes,
    )


@app.route("/consultar/video")
def tela_consultar_video():
    # conecta com o banco e executa o comando SQL
    registros = executar_select(
        db="streaming",
        consulta_sql="""
            SELECT v.id, ano, titulo, sinopse, duracao, c.nome
            FROM video v, classificacao c
            WHERE v.id_classificacao = c.id
        """
    )

    # cabecalho da tabela Video (ordem das colunas)
    cabecalho = ["ID", "Ano", "Titulo", "Sinopse", "Duracao", "Classificacao"]

    return render_template(
        f"consultar/video.jinja2",
        api_atualizar="/api/atualizar/video",
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
            INSERT INTO  video (ano, titulo, sinopse, duracao, id_classificacao)
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
    # conecta com o banco e executa o comando SQL
    qtd_linhas = executar_insert_delete_update(
        db="streaming",
        consulta_sql="""
            UPDATE  video 
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
            DELETE FROM video
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
    app.run(debug=True)
