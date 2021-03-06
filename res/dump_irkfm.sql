-- SQL Manager 2007 Lite for PostgreSQL 4.5.0.2
-- ---------------------------------------
-- Хост         : localhost
-- База данных  : irkfm
-- Версия       : PostgreSQL 8.3.6, compiled by Visual C++ build 1400



--
-- Definition for language plpgsql (OID = 16386) : 
--
CREATE TRUSTED PROCEDURAL LANGUAGE plpgsql
   HANDLER "plpgsql_call_handler"
   VALIDATOR "pg_catalog"."plpgsql_validator";
SET check_function_bodies = false;
--
-- Definition for sequence leika_load_id_seq (OID = 16402) : 
--
SET search_path = public, pg_catalog;
CREATE SEQUENCE public.leika_load_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
--
-- Structure for table leika (OID = 16404) : 
--
CREATE TABLE public.leika (
    id integer DEFAULT nextval('leika_load_id_seq'::regclass) NOT NULL,
    url varchar,
    url_login varchar,
    url_password varchar,
    title varchar,
    category smallint,
    create_time timestamp without time zone,
    user_id integer,
    state smallint,
-- все до этого момента пишет при создании закачки controller.py
    start_time timestamp without time zone, -- запустив wget, надо вызвать контроллер и передать ему время старта закачки
    process_id smallint, -- и pid wget-а
-- все, что дальше, заполняется после того, как отработал wget и вызвал controller.py
    result_time timestamp without time zone,
    result_code smallint,
    result_msg varchar,
    storage_id smallint
) WITHOUT OIDS;
--
-- Comments
--
COMMENT ON SCHEMA public IS 'standard public schema';
