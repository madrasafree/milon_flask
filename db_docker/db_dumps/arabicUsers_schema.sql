--
-- PostgreSQL database dump
--

-- Dumped from database version 16.3 (Debian 16.3-1.pgdg120+1)
-- Dumped by pg_dump version 16.3 (Debian 16.3-1.pgdg120+1)

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
-- Name: allowEdit; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."allowEdit" (
    "siteName" text NOT NULL,
    allowed text
);


ALTER TABLE public."allowEdit" OWNER TO postgres;

--
-- Name: log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.log (
    "ID" text NOT NULL,
    "opType" text,
    "afDB" text,
    "afPage" text,
    "opNum" text,
    "userIP" text,
    "opTimestamp" text,
    "durationMs" text,
    "sStr" text
);


ALTER TABLE public.log OWNER TO postgres;

--
-- Name: loginLog; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."loginLog" (
    "ID" text NOT NULL,
    "userID" text,
    "loginTimeUTC" text
);


ALTER TABLE public."loginLog" OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id text NOT NULL,
    "userStatus" text,
    username text,
    password text,
    role text,
    name text,
    "eMail" text,
    "eMailVerify" text,
    "eMailLast" text,
    "eMailInterval" text,
    about text,
    gender text,
    picture text,
    "joinDateUTC" text,
    "maxLists" text,
    "addWords" text,
    "editorWords" text,
    "editorPics" text,
    "editorMedia" text,
    speaker text,
    coder text,
    "arabicLevel" text,
    "hebrewLevel" text,
    "arabicDialect" text,
    "arabicCity" text,
    credit text,
    "creditLink" text
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: usersWordsFollow; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."usersWordsFollow" (
    "userID" text NOT NULL,
    "wordID" text
);


ALTER TABLE public."usersWordsFollow" OWNER TO postgres;

--
-- Name: allowEdit allowEdit_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."allowEdit"
    ADD CONSTRAINT "allowEdit_pkey" PRIMARY KEY ("siteName");


--
-- Name: log log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.log
    ADD CONSTRAINT log_pkey PRIMARY KEY ("ID");


--
-- Name: loginLog loginLog_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."loginLog"
    ADD CONSTRAINT "loginLog_pkey" PRIMARY KEY ("ID");


--
-- Name: usersWordsFollow usersWordsFollow_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."usersWordsFollow"
    ADD CONSTRAINT "usersWordsFollow_pkey" PRIMARY KEY ("userID");


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

