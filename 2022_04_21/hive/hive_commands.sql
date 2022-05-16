--mkdir http_data_hive
--wget https://storage.googleapis.com/public-bucket-up-2022/email.csv
--wget https://storage.googleapis.com/public-bucket-up-2022/http_sentiment_raw.csv



CREATE EXTERNAL TABLE carpetas_investigacion 
(
  id INT ,   ao_hechos INT,   mes_hechos STRING,  fecha_hechos TIMESTAMP,  delito STRING,  categoria_delito STRING,  fiscalia STRING ,
  agencia STRING ,  unidad_investigacion STRING,  colonia_hechos STRING ,  alcaldia_hechos STRING,  fecha_inicio TIMESTAMP ,
  mes_inicio STRING,  ao_inicio INT,  calle_hechos STRING ,  calle_hechos2 STRING,  longitud float,  latitud float,  geopoint STRING  
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
STORED AS TEXTFILE
location '/user/carpetas_hdfs' 
TBLPROPERTIES ("skip.header.line.count"="1"); 


CREATE TABLE HTTP_DATA
(
seq INT, id STRING, 
visited TIMESTAMP, logged_user STRING, 
pc STRING, url STRING,
 content STRING, sentiment FLOAT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
STORED AS TEXTFILE
TBLPROPERTIES ("skip.header.line.count"="1"); 


CREATE TABLE EMAIL_DATA
(
id STRING, sent_date TIMESTAMP,
logged_user STRING, pc STRING,
to_mail STRING, cc_mail STRING,
bcc_mail STRING, from_mail STRING, 
size int, attachment_count INT,
content STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
STORED AS TEXTFILE
TBLPROPERTIES ("skip.header.line.count"="1");

LOAD DATA LOCAL INPATH '/home/[USUARIO]/http_data_hive/email' OVERWRITE INTO TABLE EMAIL_DATA;


CREATE EXTERNAL TABLE EMAIL_DATA_STAGING
(
id STRING, sent_date STRING,
logged_user STRING, pc STRING,
to_mail STRING, cc_mail STRING,
bcc_mail STRING, from_mail STRING, 
size int, attachment_count INT,
content STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
STORED AS TEXTFILE;

hive>LOAD DATA LOCAL INPATH '/home/rutiliobuenaventura123/http_data_hive/email' OVERWRITE INTO TABLE EMAIL_DATA_STAGING;

CREATE EXTERNAL TABLE EMAIL_DATA_PARTITIONED
(
id STRING, sent_date TIMESTAMP,
logged_user STRING, pc STRING,
to_mail STRING, cc_mail STRING,
bcc_mail STRING, from_mail STRING, 
size int, attachment_count INT,
content STRING
)
PARTITIONED BY (year int, month int)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
STORED AS TEXTFILE;


INSERT INTO EMAIL_DATA_PARTITIONED SELECT id, from_unixtime(unix_timestamp(sent_date, "MM/dd/yyyy hh:mm:ss")) as sent_date, logged_user, pc, to_mail, cc_mail, bcc_mail, from_mail, size, attachment_count, content, year(from_unixtime(unix_timestamp(sent_date, "MM/dd/yyyy hh:mm:ss"))) as year, month(from_unixtime(unix_timestamp(sent_date, "MM/dd/yyyy hh:mm:ss"))) as month from EMAIL_DATA_STAGING;

Si hay problema con la particion
hive>set hive.exec.dynamic.partition=true;
hive>set hive.exec.dynamic.partition.mode=nonstrict;


SHOW PARTITIONS


CREATE EXTERNAL TABLE EMAIL_DATA_BUCKETED
(
id STRING, sent_date TIMESTAMP,
logged_user STRING, pc STRING,
to_mail STRING, cc_mail STRING,
bcc_mail STRING, from_mail STRING, 
size int, attachment_count INT,
content STRING
)
CLUSTERED BY (logged_user) SORTED BY (sent_date) INTO 30 BUCKETS
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
STORED AS TEXTFILE;


INSERT INTO EMAIL_DATA_BUCKETED SELECT id, from_unixtime(unix_timestamp(sent_date, "MM/dd/yyyy hh:mm:ss")) as sent_date, logged_user, pc, to_mail, cc_mail, bcc_mail, from_mail, size, attachment_count, content from EMAIL_DATA_STAGING;

Si hay problema con el 'bucketing'
hive>set hive.enforce.bucketing = true;
