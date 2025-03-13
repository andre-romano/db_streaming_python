
/* streaming_log_tipos: */

-- Criar um banco de dados novo, e selecionar ele
DROP DATABASE IF EXISTS streaming;
CREATE DATABASE streaming;
USE streaming;

/*
  --------------------------------
    DDL (criar esquemas do DB)
  --------------------------------
*/

-- CRIAR TABELAS

CREATE TABLE Video (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    ano YEAR NOT NULL,
    titulo VARCHAR(50) NOT NULL,
    sinopse TEXT,
    duracao TIME NOT NULL CHECK (duracao > '00:00:00'),
    id_classificacao INTEGER NOT NULL
);

CREATE TABLE Usuario (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    senha VARCHAR(40) NOT NULL,
    primeiro_nome VARCHAR(60) NOT NULL,
    sobrenome VARCHAR(60) NOT NULL,
    dt_nascimento DATE NOT NULL,
    dt_registro DATE NOT NULL
);

CREATE TABLE Avaliacao (
    id_video INTEGER NOT NULL,
    id_usuario INTEGER NOT NULL,
    nota DOUBLE NOT NULL CHECK (nota >= 0 AND nota <= 10),
    dt_avaliacao DATE NOT NULL,
    PRIMARY KEY (id_video, id_usuario)
);

CREATE TABLE Visualizacao (
    data_hora DATETIME NOT NULL,
    id_usuario INTEGER NOT NULL,
    id_video INTEGER NOT NULL,
    duracao_assistida TIME NOT NULL CHECK (duracao_assistida > '00:00:00'),
    PRIMARY KEY (id_usuario, data_hora)
);

CREATE TABLE Video_Genero (
    id_video  INTEGER NOT NULL,
    id_genero INTEGER NOT NULL
);

CREATE TABLE Genero (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(30) NOT NULL
);

CREATE TABLE Classificacao (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    idade_min INTEGER NOT NULL CHECK (idade_min >= 0)
);
 
-- ADICIONAR AS CHAVES ESTRANGEIRAS

ALTER TABLE Video 
ADD CONSTRAINT Video_FK_Classificacao FOREIGN KEY (id_classificacao) REFERENCES Classificacao (id)
;
 
ALTER TABLE Video_Genero 
ADD CONSTRAINT Video_Genero_FK_Video  FOREIGN KEY (id_video)  REFERENCES Video (id),
ADD CONSTRAINT Video_Genero_FK_Genero FOREIGN KEY (id_genero) REFERENCES Genero (id)
;

ALTER TABLE Avaliacao 
ADD CONSTRAINT Avaliacao_FK_Usuario FOREIGN KEY (id_usuario) REFERENCES Usuario (id),
ADD CONSTRAINT Avaliacao_FK_Video   FOREIGN KEY (id_video)   REFERENCES Video   (id)
;
 
ALTER TABLE Visualizacao 
ADD CONSTRAINT Visualizacao_FK_Usuario FOREIGN KEY (id_usuario) REFERENCES Usuario (id),
ADD CONSTRAINT Visualizacao_FK_Video   FOREIGN KEY (id_video)   REFERENCES Video   (id)
;

/*
  --------------------------------
    DML (adicionar dados no DB)
  --------------------------------
*/

INSERT INTO Genero (nome) VALUES ('Ação');
INSERT INTO Genero (nome) VALUES ('Comédia');
INSERT INTO Genero (nome) VALUES ('Drama');
INSERT INTO Genero (nome) VALUES ('Ficção Científica');
INSERT INTO Genero (nome) VALUES ('Terror');

INSERT INTO Classificacao (nome, idade_min) VALUES ('Livre',    0);
INSERT INTO Classificacao (nome, idade_min) VALUES ('10 anos', 10);
INSERT INTO Classificacao (nome, idade_min) VALUES ('12 anos', 12);
INSERT INTO Classificacao (nome, idade_min) VALUES ('14 anos', 14);
INSERT INTO Classificacao (nome, idade_min) VALUES ('16 anos', 16);
INSERT INTO Classificacao (nome, idade_min) VALUES ('18 anos', 18);

INSERT INTO Video (sinopse, duracao, ano, titulo, id_classificacao) VALUES 
('Um herói luta contra forças do mal para salvar o mundo.',    '02:15:00', 2023, 'O Último Herói',    4),
('Um grupo de amigos se mete em várias situações engraçadas.', '01:30:00', 2022, 'A Grande Comédia',  3),
('Um drama intenso sobre amor e perdas.',                      '02:00:00', 2021, 'Histórias de Vida', 5),
('Exploração do espaço e os desafios da humanidade.',          '02:30:00', 2024, 'Além das Estrelas', 2),
('Uma entidade sobrenatural aterroriza uma pequena cidade.',   '01:45:00', 2020, 'O Terror da Noite', 6)
;

INSERT INTO Video_Genero (id_video, id_genero) VALUES 
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5)
;

INSERT INTO Usuario (email, senha, primeiro_nome, sobrenome, dt_nascimento, dt_registro) VALUES
('joao.silva@example.com',     'senha123', 'João',  'Silva',    '1990-05-15', '2024-09-01'),
('maria.oliveira@example.com', 'senha456', 'Maria', 'Oliveira', '1985-11-23', '2024-09-02'),
('ana.souza@example.com',      'senha789', 'Ana',   'Souza',    '1995-07-30', '2024-09-08'),
('pedro.santos@example.com',   'senha321', 'Pedro', 'Santos',   '2000-03-10', '2024-09-13'),
('lucas.martins@example.com',  'senha654', 'Lucas', 'Martins',  '1992-09-18', '2024-09-17')
;

INSERT INTO Avaliacao (id_video, id_usuario, nota, dt_avaliacao) VALUES 
(1, 1, 8.5, '2024-09-02'),
(2, 5, 3.8, '2024-09-02'),
(3, 3, 7.9, '2024-09-10'),
(4, 4, 9.2, '2024-09-17'),
(5, 2, 4.0, '2024-09-18')
;

INSERT INTO Visualizacao (data_hora, id_usuario, id_video, duracao_assistida) VALUES 
('2024-09-02 20:15:00', 1, 1, '01:30:00'),
('2024-09-02 21:00:00', 5, 2, '01:00:00'),
('2024-09-02 22:00:00', 4, 3, '02:00:00'),
('2024-09-02 23:00:00', 2, 4, '02:15:00'),
('2024-09-02 23:30:00', 3, 5, '00:50:00')
;

-- grave as alteracoes no banco de dados
COMMIT;

