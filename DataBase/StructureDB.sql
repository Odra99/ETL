--
-- PostgreSQL database dump
--

-- Dumped from database version 14.1
-- Dumped by pg_dump version 14.1

-- Started on 2022-04-17 01:15:51

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

DROP DATABASE "ProjectIA";
--
-- TOC entry 3328 (class 1262 OID 73945)
-- Name: ProjectIA; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE "ProjectIA" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'Spanish_Spain.1252';


ALTER DATABASE "ProjectIA" OWNER TO postgres;

\connect "ProjectIA"

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 209 (class 1259 OID 73949)
-- Name: Empresa; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Empresa" (
    "Codigo" bigint NOT NULL,
    "Nombre" character varying(250) NOT NULL,
    "Nit" character varying(20) NOT NULL,
    "Direccion" character varying(250),
    "Telefono" character varying(20)
);


ALTER TABLE public."Empresa" OWNER TO postgres;

--
-- TOC entry 212 (class 1259 OID 74029)
-- Name: Persona; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Persona" (
    "Dpi" bigint NOT NULL,
    "Primer_Nombre" character varying(50) NOT NULL,
    "Segundo_Nombre" character varying(50) NOT NULL,
    "Primer_Apellido" character varying(50) NOT NULL,
    "Segundo_Apellido" character varying(50) NOT NULL,
    "Apellido_Casada" character varying(50),
    "Cedula_Orden" character varying(5),
    "Cedula_Registro" character varying(10),
    "Direccion" character varying(250),
    "Nit" character varying(25) NOT NULL,
    "Genero" character(1),
    "Telefono" character varying(15),
    "Correo_Electronico" character varying(100),
    "Fecha_Nacimiento" date
);


ALTER TABLE public."Persona" OWNER TO postgres;

--
-- TOC entry 211 (class 1259 OID 74004)
-- Name: Trabajo; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Trabajo" (
    "ID_Trabajo" integer NOT NULL,
    "ID_Persona" bigint NOT NULL,
    "Fecha_Inicial" date NOT NULL,
    "Fecha_Final" date NOT NULL,
    "ID_Empresa" bigint,
    "Nombre_Puesto" character varying(100),
    "Mes_Planilla" character varying(15),
    "Salario" double precision
);


ALTER TABLE public."Trabajo" OWNER TO postgres;

--
-- TOC entry 210 (class 1259 OID 74003)
-- Name: Trabajo_ID_Trabajo_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Trabajo_ID_Trabajo_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Trabajo_ID_Trabajo_seq" OWNER TO postgres;

--
-- TOC entry 3329 (class 0 OID 0)
-- Dependencies: 210
-- Name: Trabajo_ID_Trabajo_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Trabajo_ID_Trabajo_seq" OWNED BY public."Trabajo"."ID_Trabajo";


--
-- TOC entry 3172 (class 2604 OID 74007)
-- Name: Trabajo ID_Trabajo; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Trabajo" ALTER COLUMN "ID_Trabajo" SET DEFAULT nextval('public."Trabajo_ID_Trabajo_seq"'::regclass);


--
-- TOC entry 3174 (class 2606 OID 73976)
-- Name: Empresa Codigo_Empresa_Unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Empresa"
    ADD CONSTRAINT "Codigo_Empresa_Unique" UNIQUE ("Codigo");


--
-- TOC entry 3176 (class 2606 OID 73992)
-- Name: Empresa Empresa_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Empresa"
    ADD CONSTRAINT "Empresa_pkey" PRIMARY KEY ("Codigo");


--
-- TOC entry 3178 (class 2606 OID 73974)
-- Name: Empresa Nit_Empresa_Unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Empresa"
    ADD CONSTRAINT "Nit_Empresa_Unique" UNIQUE ("Nit");


--
-- TOC entry 3182 (class 2606 OID 74035)
-- Name: Persona Persona_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Persona"
    ADD CONSTRAINT "Persona_pkey" PRIMARY KEY ("Dpi");


--
-- TOC entry 3180 (class 2606 OID 74009)
-- Name: Trabajo Trabajo_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Trabajo"
    ADD CONSTRAINT "Trabajo_pkey" PRIMARY KEY ("ID_Trabajo", "ID_Persona");


--
-- TOC entry 3183 (class 2606 OID 74010)
-- Name: Trabajo ID_Empresa_Trabajo; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Trabajo"
    ADD CONSTRAINT "ID_Empresa_Trabajo" FOREIGN KEY ("ID_Empresa") REFERENCES public."Empresa"("Codigo");


-- Completed on 2022-04-17 01:15:51

--
-- PostgreSQL database dump complete
--

