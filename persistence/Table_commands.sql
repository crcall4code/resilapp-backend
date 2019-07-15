--Reorg Table
	CALL sysproc.admin_cmd('REORG TABLE MHG98374.COMMUNITIES');
--End of Reorg Table


--MQT (Provincias)
CREATE TABLE PROVINCIA (PROVINCIA) AS
  (SELECT DISTINCT PROVINCIA
     FROM POBLADOS)
     DATA INITIALLY DEFERRED
     REFRESH DEFERRED
     MAINTAINED BY SYSTEM
     ENABLE QUERY OPTIMIZATION;
--End of MQT (Cantones)


--MQT (Cantones)
CREATE TABLE PROVINCIA_NAME (CANTON) AS
  (SELECT DISTINCT CANTON
     FROM POBLADOS
     WHERE PROVINCIA = 'PROVINCIA_NAME'
     )
     DATA INITIALLY DEFERRED
     REFRESH DEFERRED
     MAINTAINED BY SYSTEM
     ENABLE QUERY OPTIMIZATION;
--End of MQT (Cantones)

