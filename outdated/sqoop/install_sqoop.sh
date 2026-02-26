
#Install sqoop


wget https://archive.apache.org/dist/sqoop/1.4.6/sqoop-1.4.6.bin__hadoop-2.0.4-alpha.tar.gz
tar -xvf sqoop-1.4.6.bin__hadoop-2.0.4-alpha.tar.gz
echo export SQOOP_HOME=~/sqoop-1.4.6.bin__hadoop-2.0.4-alpha export PATH=$PATH:$SQOOP_HOME/bin>~/.bashrc
source ~/.bashrc
sudo cp /usr/lib/hive/conf/hive-site.xml $SQOOP_HOME/conf
sudo ln -s /usr/share/java/mysql-connector-java-8.0.27.jar $SQOOP_HOME/lib
cd $SQOOP_HOME/conf
mv sqoop-env-template.sh sqoop-env.sh
echo export HADOOP_COMMON_HOME=/usr/lib/hadoop > sqoop-env.sh
echo export HADOOP_MAPRED_HOME=/usr/lib/hadoop-mapreduce > sqoop-env.sh
echo export SQOOP_HOME=~/sqoop-1.4.6.bin__hadoop-2.0.4-alpha export PATH=$PATH:$SQOOP_HOME/bin>~/.bashrc
source ~/.bashrc


#example commands for HDFS

hdfs dfs -ls /
echo "esto es un ejemplo" > mi_archivo.txt
hdfs dfs -ls /user/
hdfs dfs -mkdir /user/example1
hdfs dfs -copyFromLocal mi_archivo.txt /user/example1
hdfs dfs -ls /user/example1
hdfs dfs -get /user/example1/mi_archivo.txt

wget https://storage.googleapis.com/public-bucket-up-2022/carpetas_investigacion.csv