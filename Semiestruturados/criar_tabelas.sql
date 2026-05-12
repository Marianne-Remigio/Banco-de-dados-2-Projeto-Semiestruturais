CREATE TABLE unidade_federativa(
	id_uf SERIAL PRIMARY KEY,
	nome_uf VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE crime(
	id_crime SERIAL PRIMARY KEY,
	nome_crime VARCHAR(100) NOT NULL
);

CREATE TABLE tempo(
	id_tempo SERIAL PRIMARY KEY,
	ano INTEGER NOT NULL,
	mes INTEGER NOT NULL CHECK (mes BETWEEN 1 AND 12),
	UNIQUE (ano, mes)
);

CREATE TABLE sexo(
	id_sexo SERIAL PRIMARY KEY,
	sexo VARCHAR(15) NOT NULL UNIQUE
);

CREATE TABLE Vitima(
	id_vitima SERIAL PRIMARY KEY,
	numero_vitimas INTEGER NOT NULL,
	id_uf INTEGER NOT NULL,
	id_crime INTEGER NOT NULL,
	id_tempo INTEGER NOT NULL,
	id_sexo INTEGER NOT NULL,
	FOREIGN KEY (id_uf) REFERENCES unidade_federativa(id_uf),
	FOREIGN KEY (id_crime) REFERENCES crime(id_crime),
	FOREIGN KEY (id_tempo) REFERENCES tempo(id_tempo),
	FOREIGN KEY (id_sexo) REFERENCES sexo(id_sexo)
);

CREATE TABLE ocorrencia(
	id_ocorrencia SERIAL PRIMARY KEY,
	numero_ocorrencias INTEGER NOT NULL,
	id_uf INTEGER NOT NULL,
	id_crime INTEGER NOT NULL,
	id_tempo INTEGER NOT NULL,
	FOREIGN KEY (id_uf) REFERENCES unidade_federativa(id_uf),
	FOREIGN KEY (id_crime) REFERENCES crime(id_crime),
	FOREIGN KEY (id_tempo) REFERENCES tempo(id_tempo)
);
