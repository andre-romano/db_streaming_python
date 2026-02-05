
import time

from datetime import datetime

from flask import Flask, request, render_template

from db.db import executar_insert_delete_update, executar_select

# Create a Flask application
app = Flask(__name__)

##################
#     TELAS      #
##################


# Rota da tela inicial (pagina inicial / home page)
@app.route('/', methods=['GET'])
def home():
    # retorna a tela inicial do sistema
    return render_template(
        'index.jinja2',  # template a ser renderizado
    )


# Rota da tela de atualizar video (/atualizar/video)
@app.route("/atualizar/video", methods=['GET'])
def tela_atualizar_video():
    # conecta com o banco e executa o comando SQL
    classificacoes = executar_select(
        db="streaming",
        consulta_sql="""
            SELECT id, nome
            FROM classificacao
        """
    )
    # classificacoes tem o formato [ (id, nome), ... ]

    # conecta com o banco e executa o comando SQL
    registros = executar_select(
        db="streaming",
        consulta_sql="""
            SELECT id, ano, titulo, sinopse, duracao, id_classificacao
            FROM video 
            WHERE id = %s
        """,
        # parametros a serem inseridos no lugar dos %s no SQL acima, em ordem
        parametros=(
            # request.args pega os dados enviados pelo usuario na tela de atualizacao
            request.args.get('id') or "",
        )
    )

    if len(registros) <= 0:
        return "ERRO: Consulta de video falhou. Veja logs do Python para detalhes."
    id, ano, titulo, sinopse, duracao, id_classificacao = registros[0]

    # converter duracao do formato HH:MM:SS para HH:MM
    duracao_formatada = datetime.strptime(
        str(duracao), "%H:%M:%S").strftime("%H:%M")

    # retorna a tela de atualizar video com os dados preenchidos
    return render_template(
        "atualizar/video.jinja2",  # template a ser renderizado
        api="/api/atualizar/video",  # rota da API que fara o update (usada no formulario)
        classificacoes=classificacoes,  # lista de classificacoes para o componente <select> do HTML5

        # DADOS do video a ser atualizado
        id=id,
        ano=ano,
        titulo=titulo,
        sinopse=sinopse,
        duracao=duracao_formatada,
        id_classificacao=id_classificacao,
    )


@app.route("/cadastrar/video", methods=['GET'])
def tela_cadastrar_video():

    # conecta com o banco e executa o comando SQL
    classificacoes = executar_select(
        db="streaming",
        consulta_sql="""
            SELECT id, nome
            FROM classificacao
        """
    )
    # classificacoes tem o formato [ (id, nome), ... ]

    # retorna a tela de cadastrar video
    return render_template(
        "cadastrar/video.jinja2",  # template a ser renderizado
        api="/api/cadastrar/video",  # rota da API que fara o insert (usada no formulario)
        classificacoes=classificacoes,  # lista de classificacoes para o componente <select> do HTML5
    )


@app.route("/consultar/video", methods=['GET'])
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
    # registros tem o formato [ (id, ano, titulo, sinopse, duracao, nome_classificacao), ... ]

    # cabecalho da tabela Video (ordem das colunas)
    cabecalho = ["ID", "Ano", "Titulo", "Sinopse", "Duracao", "Classificacao"]

    return render_template(
        "consultar.jinja2",  # template a ser renderizado
        api_atualizar="/atualizar/video",  # rota para a tela de atualizar (usada no botao de atualizar)
        api_apagar="/api/apagar/video",  # rota para a API de apagar (usada no botao de apagar)
        cabecalho=cabecalho,  # cabecalho da tabela (usado para renderizar o cabecalho dinamicamente)
        dados=registros,  # dados a serem exibidos na tabela (usado para renderizar as linhas dinamicamente)
    )

################
#     API      #
################


@app.route('/api/cadastrar/video', methods=['POST'])
def api_cadastrar_video():
    print("Recebendo dados para cadastrar video:", request.form)

    # conecta com o banco e executa o comando SQL
    qtd_linhas_inseridas = executar_insert_delete_update(
        db="streaming",
        consulta_sql="""
            INSERT INTO  video (ano, titulo, sinopse, duracao, id_classificacao)
            VALUES             (  %s,    %s,      %s   ,  %s     ,   %s  ) 
        """,
        # parametros a serem inseridos no lugar dos %s no SQL acima, em ordem
        parametros=(
            # request.form pega os dados enviados pelo usuario na tela de cadastro
            request.form.get('ano') or "",
            request.form.get('titulo') or "",
            request.form.get('sinopse') or "",
            request.form.get('duracao') or "",
            request.form.get('id_classificacao') or "",
        )
    )

    # verifica se o insert falhou (qtd_linhas_inseridas < 0)
    if qtd_linhas_inseridas < 0:
        # mostra mensagem de erro se o insert falhar
        return "ERRO: Insercao mal feita. Veja os logs do Python para detalhes."

    # mostra mensagem de sucesso se o insert for bem sucedido
    return f"SUCESSO: {qtd_linhas_inseridas} videos inseridos no DB. Retorne para a pagina /consultar/video para ver o resultado."


@app.route('/api/atualizar/video', methods=['POST'])
def api_atualizar_video():
    print("Recebendo dados para atualizar video:", request.form)

    # conecta com o banco e executa o comando SQL
    qtd_linhas_atualizadas = executar_insert_delete_update(
        db="streaming",
        consulta_sql="""
            UPDATE  video 
            SET ano = %s, titulo = %s, sinopse = %s, duracao = %s, id_classificacao = %s
            WHERE id = %s
        """,
        # parametros a serem inseridos no lugar dos %s no SQL acima, em ordem
        parametros=(
            # request.form pega os dados enviados pelo usuario na tela de atualizacao
            request.form.get('ano') or "",
            request.form.get('titulo') or "",
            request.form.get('sinopse') or "",
            request.form.get('duracao') or "",
            request.form.get('id_classificacao') or "",
            request.form.get('id') or "",
        )
    )

    # verifica se o update falhou (qtd_linhas_atualizadas < 0)
    if qtd_linhas_atualizadas < 0:
        # mostra mensagem de erro se o update falhar
        return "ERRO: Atualizacao mal feita. Veja os logs do Python para detalhes."

    # mostra mensagem de sucesso se o update for bem sucedido
    return f"SUCESSO: {qtd_linhas_atualizadas} videos atualizados no DB. Retorne para a pagina /consultar/video para ver o resultado."


@app.route('/api/apagar/video', methods=['POST'])
def api_apagar_video():
    print("Recebendo dados para apagar video:", request.form)

    # conecta com o banco e executa o comando SQL
    qtd_linhas_apagadas = executar_insert_delete_update(
        db="streaming",
        consulta_sql="""
            DELETE FROM video
            WHERE id = %s
        """,
        # parametros a serem inseridos no lugar dos %s no SQL acima, em ordem
        parametros=(
            # request.form pega os dados enviados pelo usuario na tela de atualizacao
            request.form.get('id') or "",
        )
    )

    # verifica se o delete falhou (qtd_linhas_apagadas < 0)
    if qtd_linhas_apagadas < 0:
        # mostra mensagem de erro se o delete falhar
        return "ERRO: Delete mal feito. Veja os logs do Python para detalhes."

    # mostra mensagem de sucesso se o delete for bem sucedido
    return f"SUCESSO: {qtd_linhas_apagadas} videos deletados no DB. Retorne para a pagina /consultar/video para ver o resultado."


# Inicia o servidor Flask (NAO ALTERE OU REMOVA O CODIGO ABAIXO)
if __name__ == '__main__':
    while True:
        try:
            print("Iniciando servidor Flask...")
            print("Pressione Ctrl+C para encerrar o servidor.")
            app.run(debug=True)
            raise KeyboardInterrupt()  # Encerra servidor
        except KeyboardInterrupt:
            print("Servidor Flask encerrado pelo usuário.")
            break  # Sai do loop se o servidor for encerrado normalmente
        except Exception as e:
            print(f"Erro no servidor Flask: {e}")
            time.sleep(0.500)  # Aguarde um pouco antes de tentar reiniciar o servidor
