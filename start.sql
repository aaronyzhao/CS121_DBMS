drop database final;
create database final;
use final;

SET GLOBAL log_bin_trust_function_creators = 1;
source setup.sql;
source load-data.sql;