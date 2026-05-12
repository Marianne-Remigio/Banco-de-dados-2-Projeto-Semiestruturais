SELECT uf.nome_uf, SUM(vitima.numero_vitimas) AS total_vitimas
FROM vitima
JOIN unidade_federativa uf ON vitima.id_uf = uf.id_uf
GROUP BY uf.nome_uf
ORDER BY total_vitimas DESC;

-----------------------------------------

SELECT c.nome_crime, SUM(vitima.numero_vitimas) AS total_vitimas
FROM vitima
JOIN crime c ON vitima.id_crime = c.id_crime
GROUP BY c.nome_crime
ORDER BY total_vitimas DESC;

-----------------------------------------

SELECT t.ano, t.mes, SUM(vitima.numero_vitimas) AS total_vitimas
FROM vitima
JOIN tempo t ON vitima.id_tempo = t.id_tempo
GROUP BY t.ano, t.mes
ORDER BY t.ano, t.mes;

-----------------------------------------

SELECT s.sexo, SUM(vitima.numero_vitimas) AS total_vitimas
FROM vitima
JOIN sexo s ON vitima.id_sexo = s.id_sexo
GROUP BY s.sexo
ORDER BY total_vitimas DESC;

-----------------------------------------

SELECT uf.nome_uf, SUM(vitima.numero_vitimas) AS total_vitimas
FROM vitima
JOIN unidade_federativa uf ON vitima.id_uf = uf.id_uf
GROUP BY uf.nome_uf
ORDER BY total_vitimas DESC
LIMIT 27;
