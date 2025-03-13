
## Instalar dependencias

No terminal execute o seguinte comando:

```batch
pip install -r requirements.txt
```

## Executar app Flask

No terminal execute o seguinte comando:

```batch
python.exe app.py
```

## O que fazer

1) Importar o arquivo **db/streaming_modelo_fisico.sql** no PhpMyAdmin ( http://localhost/phpmyadmin )
2) Instalar dependências do Flask (veja comando acima)
3) Executar o App Flask (veja o comando acima)
4) Acessar o App no endereço http://localhost:5000
5) Construir as telas no Flask para criar, atualizar, apagar e consultar (CRUD) cada tabela do DB

## Estrutura do projeto

- **app.py**: Aplicativo Python que usa a biblioteca Flask para criar o site
- **db/**: contem o arquivo .SQL do banco de dados, e a biblioteca db.py para acesso ao sistema do MySQL no Python
- **static/**: contem os arquivos .JPG, .CSS e .JS do site
- **templates/**: contem os templates HTML que o Python irá preencher (arquivos .JINJA2)
  - **_base.jinja2**: Template da pagina inicial do site
  - **_macros.jinja2**: Funções (macros) que o Python pode usar para criar as paginas HTML (usando o sistema Jinja2)
  - **index.jinja2**: Pagina inicial do site
  - **atualizar/**: contem as paginas para atualizar registros (*UPDATE*) em cada tabela no DB
  - **cadastrar/**: contem as paginas para cadastrar registros (*INSERT*) em cada tabela no DB
  - **consultar/**: contem as paginas para consultar registros (*SELECT*) em cada tabela no DB

> **PS**: Para deletar registros (*DELETE*) nao precisamos de uma tela. Basta ter uma API e passar para ela as informações necessárias para encontrar o registro a ser deletado (ex: id, cpf, outra_chave_primaria, etc).