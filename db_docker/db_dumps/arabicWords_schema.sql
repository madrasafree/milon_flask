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
-- Name: history; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.history (
    "ID" text NOT NULL,
    word text,
    "actionUTC" text,
    action text,
    "user" text,
    "statusOld" text,
    "statusNew" text,
    "errorTypes" text,
    explain text,
    "showOld" text,
    "showNew" text,
    "hebrewOld" text,
    "hebrewNew" text,
    "hebrewDefOld" text,
    "hebrewDefNew" text,
    "arabicOld" text,
    "arabicNew" text,
    "arabicWordOld" text,
    "arabicWordNew" text,
    "pronunciationOld" text,
    "pronunciationNew" text,
    "searchStringOld" text,
    "searchStringNew" text,
    "rootOld" text,
    "rootNew" text,
    "partOfSpeachOld" text,
    "partOfSpeachNew" text,
    "binyanOld" text,
    "binyanNew" text,
    "genderOld" text,
    "genderNew" text,
    "numberOld" text,
    "numberNew" text,
    "infoOld" text,
    "infoNew" text,
    "exampleOld" text,
    "exampleNew" text,
    "imgLinkOld" text,
    "imgLinkNew" text,
    "imgCreditOld" text,
    "imgCreditNew" text,
    "linkDescOld" text,
    "linkDescNew" text,
    "linkOld" text,
    "linkNew" text,
    "labelsOld" text,
    "labelsNew" text
);


ALTER TABLE public.history OWNER TO postgres;

--
-- Name: labels; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.labels (
    "ID" text NOT NULL,
    "labelName" text,
    "fbIMG" text
);


ALTER TABLE public.labels OWNER TO postgres;

--
-- Name: lists; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.lists (
    "ID" text NOT NULL,
    creator text,
    "listName" text,
    "listDesc" text,
    "viewCNT" text,
    "creationTimeUTC" text,
    "lastUpdateUTC" text,
    privacy text,
    type text
);


ALTER TABLE public.lists OWNER TO postgres;

--
-- Name: listsUsers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."listsUsers" (
    list text NOT NULL,
    "user" text,
    pos text
);


ALTER TABLE public."listsUsers" OWNER TO postgres;

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
-- Name: media; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.media (
    id text NOT NULL,
    "mType" text,
    "mLink" text,
    description text,
    credit text,
    "creditLink" text,
    speaker text,
    uploader text,
    school text,
    "creationTime" text,
    "creationTimeUTC" text,
    "lastUpdateUTC" text
);


ALTER TABLE public.media OWNER TO postgres;

--
-- Name: sentences; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sentences (
    id text NOT NULL,
    show text,
    status text,
    hebrew text,
    "hebrewClean" text,
    arabic text,
    "arabicClean" text,
    "arabicHeb" text,
    "arabicHebClean" text,
    info text,
    creator text,
    "creationTimeUTC" text
);


ALTER TABLE public.sentences OWNER TO postgres;

--
-- Name: words; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.words (
    id text NOT NULL,
    show text,
    status text,
    "lockedUTC" text,
    "isLocked" text,
    "hebrewTranslation" text,
    "hebrewClean" text,
    "hebrewCleanMore" text,
    "hebrewDef" text,
    "sndxHebrewV1" text,
    arabic text,
    "arabicClean" text,
    "arabicCleanMore" text,
    "sndxArabicV1" text,
    "arabicWord" text,
    "arabicHebClean" text,
    "arabicHebCleanMore" text,
    pronunciation text,
    "searchString" text,
    "originWordID" text,
    "partOfSpeach" text,
    gender text,
    number text,
    binyan text,
    info text,
    example text,
    "creatorID" text,
    "creationTimeUTC" text,
    "imgLink" text,
    "imgCredit" text
);


ALTER TABLE public.words OWNER TO postgres;

--
-- Name: wordsLabels; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."wordsLabels" (
    "wordID" text NOT NULL,
    "labelID" text NOT NULL
);


ALTER TABLE public."wordsLabels" OWNER TO postgres;

--
-- Name: wordsLists; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."wordsLists" (
    "wordID" text NOT NULL,
    "listID" text NOT NULL,
    pos text
);


ALTER TABLE public."wordsLists" OWNER TO postgres;

--
-- Name: wordsMedia; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."wordsMedia" (
    "wordID" text NOT NULL,
    "mediaID" text
);


ALTER TABLE public."wordsMedia" OWNER TO postgres;

--
-- Name: wordsRelations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."wordsRelations" (
    word1 text NOT NULL,
    word2 text,
    "relationType" text
);


ALTER TABLE public."wordsRelations" OWNER TO postgres;

--
-- Name: wordsSentences; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."wordsSentences" (
    word text NOT NULL,
    sentence text,
    location text,
    relevance text,
    merge text
);


ALTER TABLE public."wordsSentences" OWNER TO postgres;

--
-- Name: wordsShort; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."wordsShort" (
    "ID" text NOT NULL,
    "sStr" text,
    "wordID" text
);


ALTER TABLE public."wordsShort" OWNER TO postgres;

--
-- Name: history history_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.history
    ADD CONSTRAINT history_pkey PRIMARY KEY ("ID");


--
-- Name: labels labels_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.labels
    ADD CONSTRAINT labels_pkey PRIMARY KEY ("ID");


--
-- Name: listsUsers listsUsers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."listsUsers"
    ADD CONSTRAINT "listsUsers_pkey" PRIMARY KEY (list);


--
-- Name: lists lists_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lists
    ADD CONSTRAINT lists_pkey PRIMARY KEY ("ID");


--
-- Name: log log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.log
    ADD CONSTRAINT log_pkey PRIMARY KEY ("ID");


--
-- Name: media media_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.media
    ADD CONSTRAINT media_pkey PRIMARY KEY (id);


--
-- Name: sentences sentences_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sentences
    ADD CONSTRAINT sentences_pkey PRIMARY KEY (id);


--
-- Name: wordsLabels wordsLabels_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."wordsLabels"
    ADD CONSTRAINT "wordsLabels_pkey" PRIMARY KEY ("wordID", "labelID");


--
-- Name: wordsLists wordsLists_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."wordsLists"
    ADD CONSTRAINT "wordsLists_pkey" PRIMARY KEY ("wordID", "listID");


--
-- Name: wordsMedia wordsMedia_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."wordsMedia"
    ADD CONSTRAINT "wordsMedia_pkey" PRIMARY KEY ("wordID");


--
-- Name: wordsRelations wordsRelations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."wordsRelations"
    ADD CONSTRAINT "wordsRelations_pkey" PRIMARY KEY (word1);


--
-- Name: wordsSentences wordsSentences_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."wordsSentences"
    ADD CONSTRAINT "wordsSentences_pkey" PRIMARY KEY (word);


--
-- Name: wordsShort wordsShort_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."wordsShort"
    ADD CONSTRAINT "wordsShort_pkey" PRIMARY KEY ("ID");


--
-- Name: words words_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.words
    ADD CONSTRAINT words_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

