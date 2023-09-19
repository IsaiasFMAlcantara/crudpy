/*
CREATE TABLE tipo_genero(
id_tipo INTEGER PRIMARY KEY AUTOINCREMENT,
descricao varchar(50)
);

CREATE TABLE tipo_documento(
id_tipo INTEGER PRIMARY KEY AUTOINCREMENT,
descricao varchar(50)
);

CREATE TABLE pessoas (
    idpessoa INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(60),
    sobrenome VARCHAR(60),
    genero INTEGER,
    idade INT,
    documento VARCHAR(20) UNIQUE,
    tipo INTEGER,
    UNIQUE(documento),
    FOREIGN KEY(tipo) REFERENCES tipo_documento(id_tipo),
    FOREIGN KEY(genero) REFERENCES tipo_genero(id_tipo)
);

CREATE TABLE endereco(
idendereco INTEGER PRIMARY KEY AUTOINCREMENT,
documento VARCHAR(20),
pais VARCHAR(40),
estado VARCHAR(40),
cidade VARCHAR(40),
bairro VARCHAR(40),
rua VARCHAR(40),
numero_casa INTEGER,
observacao VARCHAR(40),
FOREIGN KEY (documento) REFERENCES pessoas(documento)
);

*/
-- SELECT * FROM tipo_documento td;
-- SELECT * FROM tipo_genero tg;
-- SELECT * FROM endereco e
-- SELECT * FROM pessoas p;

SELECT
p.idpessoa,
p.nome,
p.sobrenome ,
p.idade,
CASE
	WHEN p.genero = 1 THEN "Masculino"
	ELSE "Feminino"
END as genero,
p.documento,
CASE
	WHEN p.tipo = 1 THEN "cpf"
	ELSE "cnpj"
END as tipo_documento,
e.pais||', '||e.estado||', '||e.cidade||', '||e.bairro||', '||e.rua||', '||e.numero_casa||', '||e.observacao as endereco
FROM pessoas p
LEFT JOIN endereco e
ON p.documento = e.documento;