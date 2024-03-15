drop database az_rj_dbms;
create database az_rj_dbms;
use final;

SET GLOBAL log_bin_trust_function_creators = 1;
source setup.sql;
source load-data.sql;