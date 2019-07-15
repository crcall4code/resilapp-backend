--Pasos_Resiliencia
CREATE TABLE "RESILIENCIA-PASOS" (
	"ID"	INTEGER NOT NULL PRIMARY KEY UNIQUE,
	"Etapa"	INTEGER NOT NULL,
	"Paso"	INTEGER NOT NULL,
	"Detalle"	VARCHAR(255) NOT NULL,
	"Referencia"	VARCHAR(255),
	"Logros"	VARCHAR(255)
);
INSERT INTO "RESILIENCIA-PASOS" ("ID","Etapa","Paso","Detalle","Referencia","Logros") VALUES (1,1,0,'Participación y conexión',NULL,NULL);
INSERT INTO "RESILIENCIA-PASOS" ("ID","Etapa","Paso","Detalle","Referencia","Logros") VALUES (2,1,1,'Formar equipo de trabajo',NULL,NULL);
INSERT INTO "RESILIENCIA-PASOS" ("ID","Etapa","Paso","Detalle","Referencia","Logros") VALUES (3,1,2,'Definir comunidades',NULL,NULL);
INSERT INTO "RESILIENCIA-PASOS" ("ID","Etapa","Paso","Detalle","Referencia","Logros") VALUES (4,1,3,'Presentación y participación',NULL,NULL);
INSERT INTO "RESILIENCIA-PASOS" ("ID","Etapa","Paso","Detalle","Referencia","Logros") VALUES (5,1,4,'Línea Base',NULL,NULL);
INSERT INTO "RESILIENCIA-PASOS" ("ID","Etapa","Paso","Detalle","Referencia","Logros") VALUES (6,1,5,'Mapa de socios interesados','Comprometerse como Sociedad Nacional',NULL);
INSERT INTO "RESILIENCIA-PASOS" ("ID","Etapa","Paso","Detalle","Referencia","Logros") VALUES (7,1,6,'Facilitar Conexiones','Establecer contacto entre la comunidad y las partes interesadas',NULL);
INSERT INTO "RESILIENCIA-PASOS" ("ID","Etapa","Paso","Detalle","Referencia","Logros") VALUES (8,2,0,'Comprensión del riesgo y la Resiliencia',NULL,NULL);
INSERT INTO "RESILIENCIA-PASOS" ("ID","Etapa","Paso","Detalle","Referencia","Logros") VALUES (9,2,1,'Acordar el propósito y alcance',NULL,NULL);
INSERT INTO "RESILIENCIA-PASOS" ("ID","Etapa","Paso","Detalle","Referencia","Logros") VALUES (10,2,2,'Elegir el enfoque','Preparar la evaluación',NULL);
INSERT INTO "RESILIENCIA-PASOS" ("ID","Etapa","Paso","Detalle","Referencia","Logros") VALUES (11,2,3,'Identificar las amenazas principales',NULL,NULL);
INSERT INTO "RESILIENCIA-PASOS" ("ID","Etapa","Paso","Detalle","Referencia","Logros") VALUES (12,2,4,'Contextualizar las características',NULL,NULL);
INSERT INTO "RESILIENCIA-PASOS" ("ID","Etapa","Paso","Detalle","Referencia","Logros") VALUES (13,2,5,'Convertir las descripciones en indicadores',NULL,NULL);
INSERT INTO "RESILIENCIA-PASOS" ("ID","Etapa","Paso","Detalle","Referencia","Logros") VALUES (14,2,6,'Recopilar datos primarios',NULL,NULL);
INSERT INTO "RESILIENCIA-PASOS" ("ID","Etapa","Paso","Detalle","Referencia","Logros") VALUES (15,2,7,'Analizar los datos',NULL,NULL);
INSERT INTO "RESILIENCIA-PASOS" ("ID","Etapa","Paso","Detalle","Referencia","Logros") VALUES (16,2,8,'Asignar una puntuación a las características',NULL,NULL);
INSERT INTO "RESILIENCIA-PASOS" ("ID","Etapa","Paso","Detalle","Referencia","Logros") VALUES (17,2,9,'Sumar y concluir','Medir la Resiliencia Comunitaria',NULL);
INSERT INTO "RESILIENCIA-PASOS" ("ID","Etapa","Paso","Detalle","Referencia","Logros") VALUES (18,3,0,'Adopción de medidas para fortalecer la resiliencia',NULL,NULL);
INSERT INTO "RESILIENCIA-PASOS" ("ID","Etapa","Paso","Detalle","Referencia","Logros") VALUES (19,3,1,'Capacidad interna',NULL,NULL);
INSERT INTO "RESILIENCIA-PASOS" ("ID","Etapa","Paso","Detalle","Referencia","Logros") VALUES (20,3,2,'Apoyo externo',NULL,NULL);
INSERT INTO "RESILIENCIA-PASOS" ("ID","Etapa","Paso","Detalle","Referencia","Logros") VALUES (21,3,3,'Actividad y recursos',NULL,NULL);
INSERT INTO "RESILIENCIA-PASOS" ("ID","Etapa","Paso","Detalle","Referencia","Logros") VALUES (22,3,4,'Conexión con otros socios','Plan de acción para la Resiliencia Comunitaria',NULL);
INSERT INTO "RESILIENCIA-PASOS" ("ID","Etapa","Paso","Detalle","Referencia","Logros") VALUES (23,4,0,'Aprendizaje para la resiliencia',NULL,NULL);
INSERT INTO "RESILIENCIA-PASOS" ("ID","Etapa","Paso","Detalle","Referencia","Logros") VALUES (24,4,1,'Motivar para el monitoreo',NULL,NULL);
INSERT INTO "RESILIENCIA-PASOS" ("ID","Etapa","Paso","Detalle","Referencia","Logros") VALUES (25,4,2,'Registrar acciones',NULL,NULL);
INSERT INTO "RESILIENCIA-PASOS" ("ID","Etapa","Paso","Detalle","Referencia","Logros") VALUES (26,4,3,'Actualizar la medición de la resiliencia',NULL,NULL);
INSERT INTO "RESILIENCIA-PASOS" ("ID","Etapa","Paso","Detalle","Referencia","Logros") VALUES (27,4,4,'Extraer lecciones',NULL,NULL);
INSERT INTO "RESILIENCIA-PASOS" ("ID","Etapa","Paso","Detalle","Referencia","Logros") VALUES (28,4,5,'Implementar lecciones aprendidas','Aprender de las acciones de resiliencia ',NULL);
COMMIT;
--End of Pasos_Resiliencia