import mysql.connector

from mysql.connector import Error
from mysql.connector.pooling import PooledMySQLConnection
from mysql.connector.abstracts import MySQLConnectionAbstract

from typing import Any, Callable, List


def connect_to_database(db, callback: Callable[[PooledMySQLConnection | MySQLConnectionAbstract], Any], host="localhost", user="root", password="") -> Any:
    """
    Conecta com o banco de dados DB, e executa a funcao callback(connection). 
    Essa funcao retorna callback() ou None
    """
    res = None
    try:
        # Estabelece a conexão com o banco de dados
        connection = mysql.connector.connect(
            host=host,  # Ex: 'localhost' ou o IP do servidor
            user=user,  # Ex: 'root'
            password=password,  # Senha do seu usuário
            database=db,  # Nome do Banco de dados para se conectar
        )

        if connection.is_connected():
            print('Conexão com o banco de dados bem-sucedida!')

        # executar comando
        print("Executando comando SQL no DB ...")
        res = callback(connection)

    except Error as e:
        print(f'Erro ao conectar ao banco de dados: {e}')

    finally:
        if connection.is_connected():
            connection.close()
            print('Conexão encerrada.')
        return res


def executar_select(db: str, consulta_sql: str, parametros: tuple = ()) -> List[tuple]:
    """
    Conecta com o DB e executa uma consulta SQL do tipo SELECT FROM,
    passando uma lista de parametros para a consulta.

    Retorna uma lista de registros encontrados pela consulta SELECT.

    registros = [ 

    (valor_da_coluna_1_do_registro_1, valor_da_coluna_2_do_registro_1, ...),

    (valor_da_coluna_1_do_registro_2, valor_da_coluna_2_do_registro_2, ...), 

    ]
    """

    def executar_sql(connection: PooledMySQLConnection | MySQLConnectionAbstract):
        cursor = connection.cursor()  # pega um cursor para o banco de dados
        cursor.execute(consulta_sql, params=parametros)
        registros = cursor.fetchall()
        if not registros:
            return []
        return registros

    # conecta com o banco e executa a funcao consulta_db()
    registros = connect_to_database(db=db, callback=executar_sql)
    return registros


def executar_insert_delete_update(db: str, consulta_sql: str, parametros: tuple = ()) -> int:
    """
    Conecta com o DB e executa uma consulta SQL do tipo INSERT INTO,  DELETE ou UPDATE,
    passando uma lista de parametros para a consulta.

    Retorna qtd_linhas_alteradas se operacao bem sucedida, do contrario retorna -1.
    """

    def executar_sql(connection: PooledMySQLConnection | MySQLConnectionAbstract):
        cursor = connection.cursor()  # pega um cursor para o banco de dados
        cursor.execute(consulta_sql, params=parametros)
        connection.commit()   # salva as alteracoes no banco de dados (operacao COMMIT)
        # quantidade de linhas alteradas no DB
        qtd_linhas = cursor.rowcount
        cursor.fetchall()
        return qtd_linhas

    # conecta com o banco e executa a funcao consulta_db()
    qtd_linhas = connect_to_database(db=db, callback=executar_sql)

    # testa se a operacao foi bem sucedida
    if not qtd_linhas:
        return -1
    return qtd_linhas
