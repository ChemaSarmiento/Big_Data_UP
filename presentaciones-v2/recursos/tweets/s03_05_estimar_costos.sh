for SQL in \
 "SELECT COUNT(*) FROM tweets_bronze.entrada" \
 "SELECT value FROM tweets_bronze.entrada LIMIT 1" \
 "SELECT JSON_VALUE(value, '\$.id') FROM tweets_bronze.entrada" \
 "SELECT value FROM tweets_bronze.entrada TABLESAMPLE SYSTEM (0.1 PERCENT)"; do
  echo "$SQL"; bq query --nouse_legacy_sql --dry_run "$SQL"
done

bq query --nouse_legacy_sql --maximum_bytes_billed=200000000 \
 "SELECT value FROM tweets_bronze.entrada TABLESAMPLE SYSTEM (0.1 PERCENT)"
