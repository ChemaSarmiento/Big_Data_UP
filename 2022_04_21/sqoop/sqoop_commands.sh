sqoop import --connect jdbc:mysql://34.75.67.253:3306/SPAIN_TENDERS --table TENDER_DETAIL --username sqoop_user --password example123

sqoop import --connect jdbc:mysql://34.75.67.253:3306/SPAIN_TENDERS --table TENDER_DETAIL --username sqoop_user --password example123 --check-column id --incremental append --last-value 700
