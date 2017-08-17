--
-- PostgreSQL database cluster dump
--

SET default_transaction_read_only = off;

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

--
-- Roles
--

CREATE ROLE dbas;
ALTER ROLE dbas WITH NOSUPERUSER INHERIT NOCREATEROLE NOCREATEDB LOGIN NOREPLICATION NOBYPASSRLS PASSWORD 'md5181cd7dfb38b99d445abaeff03b0aa05';
CREATE ROLE dolan;
ALTER ROLE dolan WITH NOSUPERUSER INHERIT NOCREATEROLE NOCREATEDB LOGIN NOREPLICATION NOBYPASSRLS PASSWORD 'md5ecfa1a1878544ac476cad6b4f2e619ca';
CREATE ROLE postgres;
ALTER ROLE postgres WITH SUPERUSER INHERIT CREATEROLE CREATEDB LOGIN REPLICATION BYPASSRLS PASSWORD 'md543583b54d80863d13a8f9ef30f0cfddb';
CREATE ROLE read_only_discussion;
ALTER ROLE read_only_discussion WITH NOSUPERUSER INHERIT NOCREATEROLE NOCREATEDB NOLOGIN NOREPLICATION NOBYPASSRLS;
CREATE ROLE writer;
ALTER ROLE writer WITH NOSUPERUSER INHERIT NOCREATEROLE NOCREATEDB NOLOGIN NOREPLICATION NOBYPASSRLS;


--
-- Role memberships
--

GRANT read_only_discussion TO dolan GRANTED BY postgres;
GRANT writer TO dbas GRANTED BY postgres;




--
-- Database creation
--

CREATE DATABASE beaker WITH TEMPLATE = template0 OWNER = postgres;
CREATE DATABASE discussion WITH TEMPLATE = template0 OWNER = postgres;
GRANT CONNECT ON DATABASE discussion TO read_only_discussion;
CREATE DATABASE news WITH TEMPLATE = template0 OWNER = postgres;
REVOKE CONNECT,TEMPORARY ON DATABASE template1 FROM PUBLIC;
GRANT CONNECT ON DATABASE template1 TO PUBLIC;


\connect beaker

SET default_transaction_read_only = off;

--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.3
-- Dumped by pg_dump version 9.6.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- PostgreSQL database dump complete
--

\connect discussion

SET default_transaction_read_only = off;

--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.3
-- Dumped by pg_dump version 9.6.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: arguments; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE arguments (
    uid integer NOT NULL,
    premisesgroup_uid integer,
    conclusion_uid integer,
    argument_uid integer,
    is_supportive boolean NOT NULL,
    author_uid integer,
    "timestamp" timestamp without time zone,
    issue_uid integer,
    is_disabled boolean NOT NULL
);


ALTER TABLE arguments OWNER TO dbas;

--
-- Name: arguments_uid_seq; Type: SEQUENCE; Schema: public; Owner: dbas
--

CREATE SEQUENCE arguments_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE arguments_uid_seq OWNER TO dbas;

--
-- Name: arguments_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbas
--

ALTER SEQUENCE arguments_uid_seq OWNED BY arguments.uid;


--
-- Name: clicked_arguments; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE clicked_arguments (
    uid integer NOT NULL,
    argument_uid integer,
    author_uid integer,
    "timestamp" timestamp without time zone,
    is_up_vote boolean NOT NULL,
    is_valid boolean NOT NULL
);


ALTER TABLE clicked_arguments OWNER TO dbas;

--
-- Name: clicked_arguments_uid_seq; Type: SEQUENCE; Schema: public; Owner: dbas
--

CREATE SEQUENCE clicked_arguments_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE clicked_arguments_uid_seq OWNER TO dbas;

--
-- Name: clicked_arguments_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbas
--

ALTER SEQUENCE clicked_arguments_uid_seq OWNED BY clicked_arguments.uid;


--
-- Name: clicked_statements; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE clicked_statements (
    uid integer NOT NULL,
    statement_uid integer,
    author_uid integer,
    "timestamp" timestamp without time zone,
    is_up_vote boolean NOT NULL,
    is_valid boolean NOT NULL
);


ALTER TABLE clicked_statements OWNER TO dbas;

--
-- Name: clicked_statements_uid_seq; Type: SEQUENCE; Schema: public; Owner: dbas
--

CREATE SEQUENCE clicked_statements_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE clicked_statements_uid_seq OWNER TO dbas;

--
-- Name: clicked_statements_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbas
--

ALTER SEQUENCE clicked_statements_uid_seq OWNED BY clicked_statements.uid;


--
-- Name: groups; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE groups (
    uid integer NOT NULL,
    name text NOT NULL
);


ALTER TABLE groups OWNER TO dbas;

--
-- Name: groups_uid_seq; Type: SEQUENCE; Schema: public; Owner: dbas
--

CREATE SEQUENCE groups_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE groups_uid_seq OWNER TO dbas;

--
-- Name: groups_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbas
--

ALTER SEQUENCE groups_uid_seq OWNED BY groups.uid;


--
-- Name: history; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE history (
    uid integer NOT NULL,
    author_uid integer,
    path text NOT NULL,
    "timestamp" timestamp without time zone
);


ALTER TABLE history OWNER TO dbas;

--
-- Name: history_uid_seq; Type: SEQUENCE; Schema: public; Owner: dbas
--

CREATE SEQUENCE history_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE history_uid_seq OWNER TO dbas;

--
-- Name: history_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbas
--

ALTER SEQUENCE history_uid_seq OWNED BY history.uid;


--
-- Name: issues; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE issues (
    uid integer NOT NULL,
    title text NOT NULL,
    slug text NOT NULL,
    info text NOT NULL,
    long_info text NOT NULL,
    date timestamp without time zone,
    author_uid integer,
    lang_uid integer,
    is_disabled boolean NOT NULL
);


ALTER TABLE issues OWNER TO dbas;

--
-- Name: issues_uid_seq; Type: SEQUENCE; Schema: public; Owner: dbas
--

CREATE SEQUENCE issues_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE issues_uid_seq OWNER TO dbas;

--
-- Name: issues_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbas
--

ALTER SEQUENCE issues_uid_seq OWNED BY issues.uid;


--
-- Name: languages; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE languages (
    uid integer NOT NULL,
    name text NOT NULL,
    ui_locales text NOT NULL
);


ALTER TABLE languages OWNER TO dbas;

--
-- Name: languages_uid_seq; Type: SEQUENCE; Schema: public; Owner: dbas
--

CREATE SEQUENCE languages_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE languages_uid_seq OWNER TO dbas;

--
-- Name: languages_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbas
--

ALTER SEQUENCE languages_uid_seq OWNED BY languages.uid;


--
-- Name: last_reviewers_delete; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE last_reviewers_delete (
    uid integer NOT NULL,
    reviewer_uid integer,
    review_uid integer,
    is_okay boolean NOT NULL,
    "timestamp" timestamp without time zone
);


ALTER TABLE last_reviewers_delete OWNER TO dbas;

--
-- Name: last_reviewers_delete_uid_seq; Type: SEQUENCE; Schema: public; Owner: dbas
--

CREATE SEQUENCE last_reviewers_delete_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE last_reviewers_delete_uid_seq OWNER TO dbas;

--
-- Name: last_reviewers_delete_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbas
--

ALTER SEQUENCE last_reviewers_delete_uid_seq OWNED BY last_reviewers_delete.uid;


--
-- Name: last_reviewers_duplicates; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE last_reviewers_duplicates (
    uid integer NOT NULL,
    reviewer_uid integer,
    review_uid integer,
    is_okay boolean NOT NULL,
    "timestamp" timestamp without time zone
);


ALTER TABLE last_reviewers_duplicates OWNER TO dbas;

--
-- Name: last_reviewers_duplicates_uid_seq; Type: SEQUENCE; Schema: public; Owner: dbas
--

CREATE SEQUENCE last_reviewers_duplicates_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE last_reviewers_duplicates_uid_seq OWNER TO dbas;

--
-- Name: last_reviewers_duplicates_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbas
--

ALTER SEQUENCE last_reviewers_duplicates_uid_seq OWNED BY last_reviewers_duplicates.uid;


--
-- Name: last_reviewers_edit; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE last_reviewers_edit (
    uid integer NOT NULL,
    reviewer_uid integer,
    review_uid integer,
    is_okay boolean NOT NULL,
    "timestamp" timestamp without time zone
);


ALTER TABLE last_reviewers_edit OWNER TO dbas;

--
-- Name: last_reviewers_edit_uid_seq; Type: SEQUENCE; Schema: public; Owner: dbas
--

CREATE SEQUENCE last_reviewers_edit_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE last_reviewers_edit_uid_seq OWNER TO dbas;

--
-- Name: last_reviewers_edit_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbas
--

ALTER SEQUENCE last_reviewers_edit_uid_seq OWNED BY last_reviewers_edit.uid;


--
-- Name: last_reviewers_merge; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE last_reviewers_merge (
    uid integer NOT NULL,
    reviewer_uid integer,
    review_uid integer,
    should_merge boolean NOT NULL,
    "timestamp" timestamp without time zone
);


ALTER TABLE last_reviewers_merge OWNER TO dbas;

--
-- Name: last_reviewers_merge_uid_seq; Type: SEQUENCE; Schema: public; Owner: dbas
--

CREATE SEQUENCE last_reviewers_merge_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE last_reviewers_merge_uid_seq OWNER TO dbas;

--
-- Name: last_reviewers_merge_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbas
--

ALTER SEQUENCE last_reviewers_merge_uid_seq OWNED BY last_reviewers_merge.uid;


--
-- Name: last_reviewers_optimization; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE last_reviewers_optimization (
    uid integer NOT NULL,
    reviewer_uid integer,
    review_uid integer,
    is_okay boolean NOT NULL,
    "timestamp" timestamp without time zone
);


ALTER TABLE last_reviewers_optimization OWNER TO dbas;

--
-- Name: last_reviewers_optimization_uid_seq; Type: SEQUENCE; Schema: public; Owner: dbas
--

CREATE SEQUENCE last_reviewers_optimization_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE last_reviewers_optimization_uid_seq OWNER TO dbas;

--
-- Name: last_reviewers_optimization_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbas
--

ALTER SEQUENCE last_reviewers_optimization_uid_seq OWNED BY last_reviewers_optimization.uid;


--
-- Name: last_reviewers_split; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE last_reviewers_split (
    uid integer NOT NULL,
    reviewer_uid integer,
    review_uid integer,
    should_split boolean NOT NULL,
    "timestamp" timestamp without time zone
);


ALTER TABLE last_reviewers_split OWNER TO dbas;

--
-- Name: last_reviewers_split_uid_seq; Type: SEQUENCE; Schema: public; Owner: dbas
--

CREATE SEQUENCE last_reviewers_split_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE last_reviewers_split_uid_seq OWNER TO dbas;

--
-- Name: last_reviewers_split_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbas
--

ALTER SEQUENCE last_reviewers_split_uid_seq OWNED BY last_reviewers_split.uid;


--
-- Name: marked_arguments; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE marked_arguments (
    uid integer NOT NULL,
    argument_uid integer,
    author_uid integer,
    "timestamp" timestamp without time zone
);


ALTER TABLE marked_arguments OWNER TO dbas;

--
-- Name: marked_arguments_uid_seq; Type: SEQUENCE; Schema: public; Owner: dbas
--

CREATE SEQUENCE marked_arguments_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE marked_arguments_uid_seq OWNER TO dbas;

--
-- Name: marked_arguments_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbas
--

ALTER SEQUENCE marked_arguments_uid_seq OWNED BY marked_arguments.uid;


--
-- Name: marked_statements; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE marked_statements (
    uid integer NOT NULL,
    statement_uid integer,
    author_uid integer,
    "timestamp" timestamp without time zone
);


ALTER TABLE marked_statements OWNER TO dbas;

--
-- Name: marked_statements_uid_seq; Type: SEQUENCE; Schema: public; Owner: dbas
--

CREATE SEQUENCE marked_statements_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE marked_statements_uid_seq OWNER TO dbas;

--
-- Name: marked_statements_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbas
--

ALTER SEQUENCE marked_statements_uid_seq OWNED BY marked_statements.uid;


--
-- Name: messages; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE messages (
    uid integer NOT NULL,
    from_author_uid integer,
    to_author_uid integer,
    topic text NOT NULL,
    content text NOT NULL,
    "timestamp" timestamp without time zone,
    read boolean NOT NULL,
    is_inbox boolean NOT NULL
);


ALTER TABLE messages OWNER TO dbas;

--
-- Name: messages_uid_seq; Type: SEQUENCE; Schema: public; Owner: dbas
--

CREATE SEQUENCE messages_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE messages_uid_seq OWNER TO dbas;

--
-- Name: messages_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbas
--

ALTER SEQUENCE messages_uid_seq OWNED BY messages.uid;


--
-- Name: optimization_review_locks; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE optimization_review_locks (
    author_uid integer NOT NULL,
    review_optimization_uid integer,
    locked_since timestamp without time zone
);


ALTER TABLE optimization_review_locks OWNER TO dbas;

--
-- Name: premisegroup_merged; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE premisegroup_merged (
    uid integer NOT NULL,
    review_uid integer,
    old_premisegroup_uid integer,
    new_premisegroup_uid integer,
    "timestamp" timestamp without time zone
);


ALTER TABLE premisegroup_merged OWNER TO dbas;

--
-- Name: premisegroup_merged_uid_seq; Type: SEQUENCE; Schema: public; Owner: dbas
--

CREATE SEQUENCE premisegroup_merged_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE premisegroup_merged_uid_seq OWNER TO dbas;

--
-- Name: premisegroup_merged_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbas
--

ALTER SEQUENCE premisegroup_merged_uid_seq OWNED BY premisegroup_merged.uid;


--
-- Name: premisegroup_splitted; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE premisegroup_splitted (
    uid integer NOT NULL,
    review_uid integer,
    old_premisegroup_uid integer,
    new_premisegroup_uid integer,
    "timestamp" timestamp without time zone
);


ALTER TABLE premisegroup_splitted OWNER TO dbas;

--
-- Name: premisegroup_splitted_uid_seq; Type: SEQUENCE; Schema: public; Owner: dbas
--

CREATE SEQUENCE premisegroup_splitted_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE premisegroup_splitted_uid_seq OWNER TO dbas;

--
-- Name: premisegroup_splitted_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbas
--

ALTER SEQUENCE premisegroup_splitted_uid_seq OWNED BY premisegroup_splitted.uid;


--
-- Name: premisegroups; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE premisegroups (
    uid integer NOT NULL,
    author_uid integer
);


ALTER TABLE premisegroups OWNER TO dbas;

--
-- Name: premisegroups_uid_seq; Type: SEQUENCE; Schema: public; Owner: dbas
--

CREATE SEQUENCE premisegroups_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE premisegroups_uid_seq OWNER TO dbas;

--
-- Name: premisegroups_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbas
--

ALTER SEQUENCE premisegroups_uid_seq OWNED BY premisegroups.uid;


--
-- Name: premises; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE premises (
    uid integer NOT NULL,
    premisesgroup_uid integer,
    statement_uid integer,
    is_negated boolean NOT NULL,
    author_uid integer,
    "timestamp" timestamp without time zone,
    issue_uid integer,
    is_disabled boolean NOT NULL
);


ALTER TABLE premises OWNER TO dbas;

--
-- Name: premises_uid_seq; Type: SEQUENCE; Schema: public; Owner: dbas
--

CREATE SEQUENCE premises_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE premises_uid_seq OWNER TO dbas;

--
-- Name: premises_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbas
--

ALTER SEQUENCE premises_uid_seq OWNED BY premises.uid;


--
-- Name: reputation_history; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE reputation_history (
    uid integer NOT NULL,
    reputator_uid integer,
    reputation_uid integer,
    "timestamp" timestamp without time zone
);


ALTER TABLE reputation_history OWNER TO dbas;

--
-- Name: reputation_history_uid_seq; Type: SEQUENCE; Schema: public; Owner: dbas
--

CREATE SEQUENCE reputation_history_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE reputation_history_uid_seq OWNER TO dbas;

--
-- Name: reputation_history_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbas
--

ALTER SEQUENCE reputation_history_uid_seq OWNED BY reputation_history.uid;


--
-- Name: reputation_reasons; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE reputation_reasons (
    uid integer NOT NULL,
    reason text NOT NULL,
    points integer NOT NULL
);


ALTER TABLE reputation_reasons OWNER TO dbas;

--
-- Name: reputation_reasons_uid_seq; Type: SEQUENCE; Schema: public; Owner: dbas
--

CREATE SEQUENCE reputation_reasons_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE reputation_reasons_uid_seq OWNER TO dbas;

--
-- Name: reputation_reasons_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbas
--

ALTER SEQUENCE reputation_reasons_uid_seq OWNED BY reputation_reasons.uid;


--
-- Name: review_canceled; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE review_canceled (
    uid integer NOT NULL,
    author_uid integer,
    review_edit_uid integer,
    review_delete_uid integer,
    review_optimization_uid integer,
    review_duplicate_uid integer,
    review_merge_uid integer,
    review_split_uid integer,
    was_ongoing boolean,
    "timestamp" timestamp without time zone
);


ALTER TABLE review_canceled OWNER TO dbas;

--
-- Name: review_canceled_uid_seq; Type: SEQUENCE; Schema: public; Owner: dbas
--

CREATE SEQUENCE review_canceled_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE review_canceled_uid_seq OWNER TO dbas;

--
-- Name: review_canceled_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbas
--

ALTER SEQUENCE review_canceled_uid_seq OWNED BY review_canceled.uid;


--
-- Name: review_delete_reasons; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE review_delete_reasons (
    uid integer NOT NULL,
    reason text NOT NULL
);


ALTER TABLE review_delete_reasons OWNER TO dbas;

--
-- Name: review_delete_reasons_uid_seq; Type: SEQUENCE; Schema: public; Owner: dbas
--

CREATE SEQUENCE review_delete_reasons_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE review_delete_reasons_uid_seq OWNER TO dbas;

--
-- Name: review_delete_reasons_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbas
--

ALTER SEQUENCE review_delete_reasons_uid_seq OWNED BY review_delete_reasons.uid;


--
-- Name: review_deletes; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE review_deletes (
    uid integer NOT NULL,
    detector_uid integer,
    argument_uid integer,
    statement_uid integer,
    "timestamp" timestamp without time zone,
    is_executed boolean NOT NULL,
    reason_uid integer,
    is_revoked boolean NOT NULL
);


ALTER TABLE review_deletes OWNER TO dbas;

--
-- Name: review_deletes_uid_seq; Type: SEQUENCE; Schema: public; Owner: dbas
--

CREATE SEQUENCE review_deletes_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE review_deletes_uid_seq OWNER TO dbas;

--
-- Name: review_deletes_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbas
--

ALTER SEQUENCE review_deletes_uid_seq OWNED BY review_deletes.uid;


--
-- Name: review_duplicates; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE review_duplicates (
    uid integer NOT NULL,
    detector_uid integer,
    duplicate_statement_uid integer,
    original_statement_uid integer,
    "timestamp" timestamp without time zone,
    is_executed boolean NOT NULL,
    is_revoked boolean NOT NULL
);


ALTER TABLE review_duplicates OWNER TO dbas;

--
-- Name: review_duplicates_uid_seq; Type: SEQUENCE; Schema: public; Owner: dbas
--

CREATE SEQUENCE review_duplicates_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE review_duplicates_uid_seq OWNER TO dbas;

--
-- Name: review_duplicates_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbas
--

ALTER SEQUENCE review_duplicates_uid_seq OWNED BY review_duplicates.uid;


--
-- Name: review_edit_values; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE review_edit_values (
    uid integer NOT NULL,
    review_edit_uid integer,
    statement_uid integer,
    typeof text NOT NULL,
    content text NOT NULL
);


ALTER TABLE review_edit_values OWNER TO dbas;

--
-- Name: review_edit_values_uid_seq; Type: SEQUENCE; Schema: public; Owner: dbas
--

CREATE SEQUENCE review_edit_values_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE review_edit_values_uid_seq OWNER TO dbas;

--
-- Name: review_edit_values_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbas
--

ALTER SEQUENCE review_edit_values_uid_seq OWNED BY review_edit_values.uid;


--
-- Name: review_edits; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE review_edits (
    uid integer NOT NULL,
    detector_uid integer,
    argument_uid integer,
    statement_uid integer,
    "timestamp" timestamp without time zone,
    is_executed boolean NOT NULL,
    is_revoked boolean NOT NULL
);


ALTER TABLE review_edits OWNER TO dbas;

--
-- Name: review_edits_uid_seq; Type: SEQUENCE; Schema: public; Owner: dbas
--

CREATE SEQUENCE review_edits_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE review_edits_uid_seq OWNER TO dbas;

--
-- Name: review_edits_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbas
--

ALTER SEQUENCE review_edits_uid_seq OWNED BY review_edits.uid;


--
-- Name: review_merge; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE review_merge (
    uid integer NOT NULL,
    detector_uid integer,
    premisesgroup_uid integer,
    "timestamp" timestamp without time zone,
    is_executed boolean NOT NULL,
    is_revoked boolean NOT NULL
);


ALTER TABLE review_merge OWNER TO dbas;

--
-- Name: review_merge_uid_seq; Type: SEQUENCE; Schema: public; Owner: dbas
--

CREATE SEQUENCE review_merge_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE review_merge_uid_seq OWNER TO dbas;

--
-- Name: review_merge_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbas
--

ALTER SEQUENCE review_merge_uid_seq OWNED BY review_merge.uid;


--
-- Name: review_merge_values; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE review_merge_values (
    uid integer NOT NULL,
    review_uid integer,
    content text NOT NULL
);


ALTER TABLE review_merge_values OWNER TO dbas;

--
-- Name: review_merge_values_uid_seq; Type: SEQUENCE; Schema: public; Owner: dbas
--

CREATE SEQUENCE review_merge_values_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE review_merge_values_uid_seq OWNER TO dbas;

--
-- Name: review_merge_values_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbas
--

ALTER SEQUENCE review_merge_values_uid_seq OWNED BY review_merge_values.uid;


--
-- Name: review_optimizations; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE review_optimizations (
    uid integer NOT NULL,
    detector_uid integer,
    argument_uid integer,
    statement_uid integer,
    "timestamp" timestamp without time zone,
    is_executed boolean NOT NULL,
    is_revoked boolean NOT NULL
);


ALTER TABLE review_optimizations OWNER TO dbas;

--
-- Name: review_optimizations_uid_seq; Type: SEQUENCE; Schema: public; Owner: dbas
--

CREATE SEQUENCE review_optimizations_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE review_optimizations_uid_seq OWNER TO dbas;

--
-- Name: review_optimizations_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbas
--

ALTER SEQUENCE review_optimizations_uid_seq OWNED BY review_optimizations.uid;


--
-- Name: review_split; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE review_split (
    uid integer NOT NULL,
    detector_uid integer,
    premisesgroup_uid integer,
    "timestamp" timestamp without time zone,
    is_executed boolean NOT NULL,
    is_revoked boolean NOT NULL
);


ALTER TABLE review_split OWNER TO dbas;

--
-- Name: review_split_uid_seq; Type: SEQUENCE; Schema: public; Owner: dbas
--

CREATE SEQUENCE review_split_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE review_split_uid_seq OWNER TO dbas;

--
-- Name: review_split_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbas
--

ALTER SEQUENCE review_split_uid_seq OWNED BY review_split.uid;


--
-- Name: review_split_values; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE review_split_values (
    uid integer NOT NULL,
    review_uid integer,
    content text NOT NULL
);


ALTER TABLE review_split_values OWNER TO dbas;

--
-- Name: review_split_values_uid_seq; Type: SEQUENCE; Schema: public; Owner: dbas
--

CREATE SEQUENCE review_split_values_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE review_split_values_uid_seq OWNER TO dbas;

--
-- Name: review_split_values_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbas
--

ALTER SEQUENCE review_split_values_uid_seq OWNED BY review_split_values.uid;


--
-- Name: revoked_content; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE revoked_content (
    uid integer NOT NULL,
    author_uid integer,
    argument_uid integer,
    statement_uid integer,
    "timestamp" timestamp without time zone
);


ALTER TABLE revoked_content OWNER TO dbas;

--
-- Name: revoked_content_history; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE revoked_content_history (
    uid integer NOT NULL,
    old_author_uid integer,
    new_author_uid integer,
    textversion_uid integer,
    argument_uid integer
);


ALTER TABLE revoked_content_history OWNER TO dbas;

--
-- Name: revoked_content_history_uid_seq; Type: SEQUENCE; Schema: public; Owner: dbas
--

CREATE SEQUENCE revoked_content_history_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE revoked_content_history_uid_seq OWNER TO dbas;

--
-- Name: revoked_content_history_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbas
--

ALTER SEQUENCE revoked_content_history_uid_seq OWNED BY revoked_content_history.uid;


--
-- Name: revoked_content_uid_seq; Type: SEQUENCE; Schema: public; Owner: dbas
--

CREATE SEQUENCE revoked_content_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE revoked_content_uid_seq OWNER TO dbas;

--
-- Name: revoked_content_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbas
--

ALTER SEQUENCE revoked_content_uid_seq OWNED BY revoked_content.uid;


--
-- Name: revoked_duplicate; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE revoked_duplicate (
    uid integer NOT NULL,
    review_uid integer,
    bend_position boolean NOT NULL,
    statement_uid integer,
    argument_uid integer,
    premise_uid integer,
    "timestamp" timestamp without time zone
);


ALTER TABLE revoked_duplicate OWNER TO dbas;

--
-- Name: revoked_duplicate_uid_seq; Type: SEQUENCE; Schema: public; Owner: dbas
--

CREATE SEQUENCE revoked_duplicate_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE revoked_duplicate_uid_seq OWNER TO dbas;

--
-- Name: revoked_duplicate_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbas
--

ALTER SEQUENCE revoked_duplicate_uid_seq OWNED BY revoked_duplicate.uid;


--
-- Name: rss; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE rss (
    uid integer NOT NULL,
    author_uid integer,
    issue_uid integer,
    title text NOT NULL,
    description text NOT NULL,
    "timestamp" timestamp without time zone
);


ALTER TABLE rss OWNER TO dbas;

--
-- Name: rss_uid_seq; Type: SEQUENCE; Schema: public; Owner: dbas
--

CREATE SEQUENCE rss_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE rss_uid_seq OWNER TO dbas;

--
-- Name: rss_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbas
--

ALTER SEQUENCE rss_uid_seq OWNED BY rss.uid;


--
-- Name: seen_arguments; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE seen_arguments (
    uid integer NOT NULL,
    argument_uid integer,
    user_uid integer
);


ALTER TABLE seen_arguments OWNER TO dbas;

--
-- Name: seen_arguments_uid_seq; Type: SEQUENCE; Schema: public; Owner: dbas
--

CREATE SEQUENCE seen_arguments_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE seen_arguments_uid_seq OWNER TO dbas;

--
-- Name: seen_arguments_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbas
--

ALTER SEQUENCE seen_arguments_uid_seq OWNED BY seen_arguments.uid;


--
-- Name: seen_statements; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE seen_statements (
    uid integer NOT NULL,
    statement_uid integer,
    user_uid integer
);


ALTER TABLE seen_statements OWNER TO dbas;

--
-- Name: seen_statements_uid_seq; Type: SEQUENCE; Schema: public; Owner: dbas
--

CREATE SEQUENCE seen_statements_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE seen_statements_uid_seq OWNER TO dbas;

--
-- Name: seen_statements_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbas
--

ALTER SEQUENCE seen_statements_uid_seq OWNED BY seen_statements.uid;


--
-- Name: settings; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE settings (
    author_uid integer NOT NULL,
    should_send_mails boolean NOT NULL,
    should_send_notifications boolean NOT NULL,
    should_show_public_nickname boolean NOT NULL,
    last_topic_uid integer NOT NULL,
    lang_uid integer,
    keep_logged_in boolean NOT NULL
);


ALTER TABLE settings OWNER TO dbas;

--
-- Name: statement_references; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE statement_references (
    uid integer NOT NULL,
    reference text NOT NULL,
    host text NOT NULL,
    path text NOT NULL,
    author_uid integer NOT NULL,
    statement_uid integer NOT NULL,
    issue_uid integer NOT NULL,
    created timestamp without time zone
);


ALTER TABLE statement_references OWNER TO dbas;

--
-- Name: statement_references_uid_seq; Type: SEQUENCE; Schema: public; Owner: dbas
--

CREATE SEQUENCE statement_references_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE statement_references_uid_seq OWNER TO dbas;

--
-- Name: statement_references_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbas
--

ALTER SEQUENCE statement_references_uid_seq OWNED BY statement_references.uid;


--
-- Name: statements; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE statements (
    uid integer NOT NULL,
    textversion_uid integer,
    is_startpoint boolean NOT NULL,
    issue_uid integer,
    is_disabled boolean NOT NULL
);


ALTER TABLE statements OWNER TO dbas;

--
-- Name: statements_uid_seq; Type: SEQUENCE; Schema: public; Owner: dbas
--

CREATE SEQUENCE statements_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE statements_uid_seq OWNER TO dbas;

--
-- Name: statements_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbas
--

ALTER SEQUENCE statements_uid_seq OWNED BY statements.uid;


--
-- Name: textversions; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE textversions (
    uid integer NOT NULL,
    statement_uid integer,
    content text NOT NULL,
    author_uid integer,
    "timestamp" timestamp without time zone,
    is_disabled boolean NOT NULL
);


ALTER TABLE textversions OWNER TO dbas;

--
-- Name: textversions_uid_seq; Type: SEQUENCE; Schema: public; Owner: dbas
--

CREATE SEQUENCE textversions_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE textversions_uid_seq OWNER TO dbas;

--
-- Name: textversions_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbas
--

ALTER SEQUENCE textversions_uid_seq OWNED BY textversions.uid;


--
-- Name: users; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE users (
    uid integer NOT NULL,
    firstname text NOT NULL,
    surname text NOT NULL,
    nickname text NOT NULL,
    public_nickname text NOT NULL,
    email text NOT NULL,
    gender text NOT NULL,
    password text NOT NULL,
    group_uid integer,
    last_action timestamp without time zone,
    last_login timestamp without time zone,
    registered timestamp without time zone,
    token text,
    token_timestamp timestamp without time zone
);


ALTER TABLE users OWNER TO dbas;

--
-- Name: users_uid_seq; Type: SEQUENCE; Schema: public; Owner: dbas
--

CREATE SEQUENCE users_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE users_uid_seq OWNER TO dbas;

--
-- Name: users_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbas
--

ALTER SEQUENCE users_uid_seq OWNED BY users.uid;


--
-- Name: arguments uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY arguments ALTER COLUMN uid SET DEFAULT nextval('arguments_uid_seq'::regclass);


--
-- Name: clicked_arguments uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY clicked_arguments ALTER COLUMN uid SET DEFAULT nextval('clicked_arguments_uid_seq'::regclass);


--
-- Name: clicked_statements uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY clicked_statements ALTER COLUMN uid SET DEFAULT nextval('clicked_statements_uid_seq'::regclass);


--
-- Name: groups uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY groups ALTER COLUMN uid SET DEFAULT nextval('groups_uid_seq'::regclass);


--
-- Name: history uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY history ALTER COLUMN uid SET DEFAULT nextval('history_uid_seq'::regclass);


--
-- Name: issues uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY issues ALTER COLUMN uid SET DEFAULT nextval('issues_uid_seq'::regclass);


--
-- Name: languages uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY languages ALTER COLUMN uid SET DEFAULT nextval('languages_uid_seq'::regclass);


--
-- Name: last_reviewers_delete uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY last_reviewers_delete ALTER COLUMN uid SET DEFAULT nextval('last_reviewers_delete_uid_seq'::regclass);


--
-- Name: last_reviewers_duplicates uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY last_reviewers_duplicates ALTER COLUMN uid SET DEFAULT nextval('last_reviewers_duplicates_uid_seq'::regclass);


--
-- Name: last_reviewers_edit uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY last_reviewers_edit ALTER COLUMN uid SET DEFAULT nextval('last_reviewers_edit_uid_seq'::regclass);


--
-- Name: last_reviewers_merge uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY last_reviewers_merge ALTER COLUMN uid SET DEFAULT nextval('last_reviewers_merge_uid_seq'::regclass);


--
-- Name: last_reviewers_optimization uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY last_reviewers_optimization ALTER COLUMN uid SET DEFAULT nextval('last_reviewers_optimization_uid_seq'::regclass);


--
-- Name: last_reviewers_split uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY last_reviewers_split ALTER COLUMN uid SET DEFAULT nextval('last_reviewers_split_uid_seq'::regclass);


--
-- Name: marked_arguments uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY marked_arguments ALTER COLUMN uid SET DEFAULT nextval('marked_arguments_uid_seq'::regclass);


--
-- Name: marked_statements uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY marked_statements ALTER COLUMN uid SET DEFAULT nextval('marked_statements_uid_seq'::regclass);


--
-- Name: messages uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY messages ALTER COLUMN uid SET DEFAULT nextval('messages_uid_seq'::regclass);


--
-- Name: premisegroup_merged uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY premisegroup_merged ALTER COLUMN uid SET DEFAULT nextval('premisegroup_merged_uid_seq'::regclass);


--
-- Name: premisegroup_splitted uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY premisegroup_splitted ALTER COLUMN uid SET DEFAULT nextval('premisegroup_splitted_uid_seq'::regclass);


--
-- Name: premisegroups uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY premisegroups ALTER COLUMN uid SET DEFAULT nextval('premisegroups_uid_seq'::regclass);


--
-- Name: premises uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY premises ALTER COLUMN uid SET DEFAULT nextval('premises_uid_seq'::regclass);


--
-- Name: reputation_history uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY reputation_history ALTER COLUMN uid SET DEFAULT nextval('reputation_history_uid_seq'::regclass);


--
-- Name: reputation_reasons uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY reputation_reasons ALTER COLUMN uid SET DEFAULT nextval('reputation_reasons_uid_seq'::regclass);


--
-- Name: review_canceled uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_canceled ALTER COLUMN uid SET DEFAULT nextval('review_canceled_uid_seq'::regclass);


--
-- Name: review_delete_reasons uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_delete_reasons ALTER COLUMN uid SET DEFAULT nextval('review_delete_reasons_uid_seq'::regclass);


--
-- Name: review_deletes uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_deletes ALTER COLUMN uid SET DEFAULT nextval('review_deletes_uid_seq'::regclass);


--
-- Name: review_duplicates uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_duplicates ALTER COLUMN uid SET DEFAULT nextval('review_duplicates_uid_seq'::regclass);


--
-- Name: review_edit_values uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_edit_values ALTER COLUMN uid SET DEFAULT nextval('review_edit_values_uid_seq'::regclass);


--
-- Name: review_edits uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_edits ALTER COLUMN uid SET DEFAULT nextval('review_edits_uid_seq'::regclass);


--
-- Name: review_merge uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_merge ALTER COLUMN uid SET DEFAULT nextval('review_merge_uid_seq'::regclass);


--
-- Name: review_merge_values uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_merge_values ALTER COLUMN uid SET DEFAULT nextval('review_merge_values_uid_seq'::regclass);


--
-- Name: review_optimizations uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_optimizations ALTER COLUMN uid SET DEFAULT nextval('review_optimizations_uid_seq'::regclass);


--
-- Name: review_split uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_split ALTER COLUMN uid SET DEFAULT nextval('review_split_uid_seq'::regclass);


--
-- Name: review_split_values uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_split_values ALTER COLUMN uid SET DEFAULT nextval('review_split_values_uid_seq'::regclass);


--
-- Name: revoked_content uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY revoked_content ALTER COLUMN uid SET DEFAULT nextval('revoked_content_uid_seq'::regclass);


--
-- Name: revoked_content_history uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY revoked_content_history ALTER COLUMN uid SET DEFAULT nextval('revoked_content_history_uid_seq'::regclass);


--
-- Name: revoked_duplicate uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY revoked_duplicate ALTER COLUMN uid SET DEFAULT nextval('revoked_duplicate_uid_seq'::regclass);


--
-- Name: rss uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY rss ALTER COLUMN uid SET DEFAULT nextval('rss_uid_seq'::regclass);


--
-- Name: seen_arguments uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY seen_arguments ALTER COLUMN uid SET DEFAULT nextval('seen_arguments_uid_seq'::regclass);


--
-- Name: seen_statements uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY seen_statements ALTER COLUMN uid SET DEFAULT nextval('seen_statements_uid_seq'::regclass);


--
-- Name: statement_references uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY statement_references ALTER COLUMN uid SET DEFAULT nextval('statement_references_uid_seq'::regclass);


--
-- Name: statements uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY statements ALTER COLUMN uid SET DEFAULT nextval('statements_uid_seq'::regclass);


--
-- Name: textversions uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY textversions ALTER COLUMN uid SET DEFAULT nextval('textversions_uid_seq'::regclass);


--
-- Name: users uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY users ALTER COLUMN uid SET DEFAULT nextval('users_uid_seq'::regclass);


--
-- Data for Name: arguments; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY arguments (uid, premisesgroup_uid, conclusion_uid, argument_uid, is_supportive, author_uid, "timestamp", issue_uid, is_disabled) FROM stdin;
1	1	2	\N	f	1	2017-08-17 11:57:15.311509	2	t
2	2	2	\N	t	1	2017-08-17 11:57:15.311673	2	f
3	3	2	\N	f	1	2017-08-17 11:57:15.311781	2	f
4	4	3	\N	t	1	2017-08-17 11:57:15.311885	2	f
5	5	3	\N	f	1	2017-08-17 11:57:15.311987	2	f
8	8	4	\N	t	1	2017-08-17 11:57:15.312285	2	f
10	10	11	\N	f	1	2017-08-17 11:57:15.312483	2	f
11	11	2	\N	t	1	2017-08-17 11:57:15.312581	2	f
12	12	2	\N	t	1	2017-08-17 11:57:15.312679	2	f
15	15	5	\N	t	1	2017-08-17 11:57:15.312975	2	f
16	16	5	\N	f	1	2017-08-17 11:57:15.313073	2	f
17	17	5	\N	t	1	2017-08-17 11:57:15.313171	2	f
19	19	6	\N	t	1	2017-08-17 11:57:15.313365	2	f
20	20	6	\N	f	1	2017-08-17 11:57:15.313462	2	f
21	21	6	\N	f	1	2017-08-17 11:57:15.313558	2	f
23	23	14	\N	f	1	2017-08-17 11:57:15.31388	2	f
24	24	14	\N	t	1	2017-08-17 11:57:15.313975	2	f
26	26	14	\N	t	1	2017-08-17 11:57:15.314147	2	f
27	27	15	\N	t	1	2017-08-17 11:57:15.314233	2	f
28	27	16	\N	t	1	2017-08-17 11:57:15.314318	2	f
29	28	15	\N	t	1	2017-08-17 11:57:15.314403	2	f
30	29	15	\N	f	1	2017-08-17 11:57:15.314488	2	f
32	31	36	\N	t	3	2017-08-17 11:57:15.314658	1	f
34	33	39	\N	t	3	2017-08-17 11:57:15.31485	1	f
35	34	41	\N	t	1	2017-08-17 11:57:15.314932	1	f
36	35	36	\N	f	1	2017-08-17 11:57:15.315014	1	f
39	38	37	\N	t	1	2017-08-17 11:57:15.315261	1	f
40	39	37	\N	t	1	2017-08-17 11:57:15.315348	1	f
41	41	46	\N	f	1	2017-08-17 11:57:15.315433	1	f
42	42	37	\N	f	1	2017-08-17 11:57:15.315602	1	f
44	44	50	\N	f	1	2017-08-17 11:57:15.315782	1	f
46	45	50	\N	t	1	2017-08-17 11:57:15.315867	1	f
47	46	38	\N	t	1	2017-08-17 11:57:15.315951	1	f
49	48	38	\N	f	1	2017-08-17 11:57:15.316124	1	f
50	49	49	\N	f	1	2017-08-17 11:57:15.316209	1	f
51	51	58	\N	f	1	2017-08-17 11:57:15.316378	4	f
54	54	59	\N	t	1	2017-08-17 11:57:15.316638	4	f
55	55	59	\N	f	1	2017-08-17 11:57:15.316732	4	f
56	56	60	\N	t	1	2017-08-17 11:57:15.316817	4	f
57	57	60	\N	f	1	2017-08-17 11:57:15.316902	4	f
58	50	58	\N	t	1	2017-08-17 11:57:15.316294	4	f
59	61	67	\N	t	1	2017-08-17 11:57:15.316987	4	f
60	62	69	\N	t	1	2017-08-17 11:57:15.317068	5	f
61	63	69	\N	t	1	2017-08-17 11:57:15.317151	5	f
62	64	69	\N	f	1	2017-08-17 11:57:15.317235	5	f
63	65	70	\N	f	1	2017-08-17 11:57:15.317317	5	f
64	66	70	\N	f	1	2017-08-17 11:57:15.317398	5	f
65	67	76	\N	t	1	2017-08-17 11:57:15.317481	7	f
66	68	76	\N	f	1	2017-08-17 11:57:15.317566	7	f
67	69	76	\N	f	1	2017-08-17 11:57:15.317649	7	f
68	70	79	\N	f	1	2017-08-17 11:57:15.317731	7	f
6	6	\N	4	f	1	2017-08-17 11:57:15.312086	2	f
7	7	\N	5	f	1	2017-08-17 11:57:15.312184	2	f
9	9	\N	8	f	1	2017-08-17 11:57:15.312383	2	f
13	13	\N	12	f	1	2017-08-17 11:57:15.312778	2	f
14	14	\N	13	f	1	2017-08-17 11:57:15.312875	2	f
18	18	\N	2	f	1	2017-08-17 11:57:15.313268	2	f
22	22	\N	3	f	1	2017-08-17 11:57:15.313746	2	f
25	25	\N	11	f	1	2017-08-17 11:57:15.314061	2	f
31	30	\N	15	f	1	2017-08-17 11:57:15.314572	2	f
33	32	\N	32	f	3	2017-08-17 11:57:15.314764	1	f
37	36	\N	36	f	1	2017-08-17 11:57:15.315096	1	f
38	37	\N	36	f	1	2017-08-17 11:57:15.315177	1	f
43	43	\N	42	f	1	2017-08-17 11:57:15.315686	1	f
45	40	\N	39	f	1	2017-08-17 11:57:15.31552	1	f
48	47	\N	47	f	1	2017-08-17 11:57:15.316037	1	f
52	52	\N	58	f	1	2017-08-17 11:57:15.316463	4	f
53	53	\N	51	f	1	2017-08-17 11:57:15.31655	4	f
69	71	\N	65	f	1	2017-08-17 11:57:15.317812	7	f
\.


--
-- Name: arguments_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('arguments_uid_seq', 69, true);


--
-- Data for Name: clicked_arguments; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY clicked_arguments (uid, argument_uid, author_uid, "timestamp", is_up_vote, is_valid) FROM stdin;
1084	1	25	2017-07-24 11:57:23.287546	t	t
1085	1	33	2017-08-04 11:57:23.287646	t	t
1086	1	29	2017-07-31 11:57:23.287684	t	t
1087	1	36	2017-08-10 11:57:23.287717	f	t
1088	1	8	2017-08-17 11:57:23.287747	f	t
1089	1	29	2017-07-28 11:57:23.287777	f	t
1090	1	24	2017-08-13 11:57:23.287808	f	t
1091	1	9	2017-08-17 11:57:23.287838	f	t
1092	1	16	2017-07-25 11:57:23.287867	f	t
1093	2	17	2017-07-28 11:57:23.287897	t	t
1094	2	37	2017-08-01 11:57:23.287925	t	t
1095	2	16	2017-08-02 11:57:23.287954	t	t
1096	2	9	2017-08-07 11:57:23.287983	t	t
1097	2	9	2017-07-29 11:57:23.288011	f	t
1098	2	11	2017-08-08 11:57:23.28804	f	t
1099	2	25	2017-08-02 11:57:23.288068	f	t
1100	2	34	2017-08-14 11:57:23.288097	f	t
1101	2	32	2017-08-05 11:57:23.288125	f	t
1102	2	33	2017-07-30 11:57:23.288154	f	t
1103	2	26	2017-08-13 11:57:23.288182	f	t
1104	2	29	2017-08-10 11:57:23.288211	f	t
1105	2	21	2017-08-11 11:57:23.288239	f	t
1106	2	23	2017-07-23 11:57:23.288268	f	t
1107	2	7	2017-08-11 11:57:23.288296	f	t
1108	3	29	2017-07-25 11:57:23.288324	f	t
1109	4	31	2017-07-24 11:57:23.288353	t	t
1110	4	25	2017-07-29 11:57:23.288381	t	t
1111	4	29	2017-07-26 11:57:23.288409	t	t
1112	4	21	2017-08-09 11:57:23.288438	f	t
1113	4	29	2017-08-01 11:57:23.288466	f	t
1114	4	8	2017-08-05 11:57:23.288495	f	t
1115	4	27	2017-07-26 11:57:23.288523	f	t
1116	5	25	2017-08-15 11:57:23.288551	t	t
1117	5	18	2017-08-12 11:57:23.28858	t	t
1118	5	23	2017-08-12 11:57:23.288607	t	t
1119	5	26	2017-07-30 11:57:23.288637	t	t
1120	5	9	2017-08-04 11:57:23.288666	t	t
1121	5	36	2017-07-24 11:57:23.288694	t	t
1122	5	29	2017-08-06 11:57:23.288723	t	t
1123	5	32	2017-07-26 11:57:23.288751	t	t
1124	5	10	2017-08-15 11:57:23.288779	t	t
1125	5	23	2017-08-07 11:57:23.288807	f	t
1126	8	18	2017-08-13 11:57:23.288836	f	t
1127	8	10	2017-08-11 11:57:23.288865	f	t
1128	8	20	2017-08-10 11:57:23.288893	f	t
1129	8	8	2017-08-12 11:57:23.288921	f	t
1130	8	28	2017-07-25 11:57:23.288949	f	t
1131	8	15	2017-08-08 11:57:23.288977	f	t
1132	8	36	2017-08-10 11:57:23.289005	f	t
1133	8	23	2017-08-13 11:57:23.289034	f	t
1134	8	12	2017-08-02 11:57:23.289062	f	t
1135	8	25	2017-07-31 11:57:23.28909	f	t
1136	8	31	2017-07-23 11:57:23.289119	f	t
1137	8	16	2017-08-02 11:57:23.289147	f	t
1138	8	21	2017-08-10 11:57:23.289175	f	t
1139	8	29	2017-08-08 11:57:23.289204	f	t
1140	8	29	2017-08-17 11:57:23.289243	f	t
1141	8	13	2017-07-26 11:57:23.289288	f	t
1142	8	14	2017-08-14 11:57:23.289352	f	t
1143	8	22	2017-07-30 11:57:23.289439	f	t
1144	8	7	2017-08-07 11:57:23.289485	f	t
1145	8	27	2017-08-04 11:57:23.289545	f	t
1146	8	11	2017-08-14 11:57:23.289626	f	t
1147	8	34	2017-08-10 11:57:23.289681	f	t
1148	10	37	2017-08-11 11:57:23.289731	t	t
1149	10	21	2017-07-26 11:57:23.289762	t	t
1150	10	20	2017-08-02 11:57:23.289792	t	t
1151	10	8	2017-08-07 11:57:23.289821	t	t
1152	10	18	2017-08-01 11:57:23.289868	t	t
1153	10	15	2017-07-28 11:57:23.28991	t	t
1154	10	34	2017-08-08 11:57:23.289941	t	t
1155	10	9	2017-08-09 11:57:23.289971	t	t
1156	10	31	2017-08-03 11:57:23.290001	t	t
1157	10	10	2017-08-09 11:57:23.290032	t	t
1158	10	16	2017-07-28 11:57:23.290062	f	t
1159	10	22	2017-08-05 11:57:23.290092	f	t
1160	10	34	2017-08-03 11:57:23.290122	f	t
1161	10	8	2017-08-14 11:57:23.290152	f	t
1162	10	12	2017-08-11 11:57:23.290182	f	t
1163	10	13	2017-08-07 11:57:23.290212	f	t
1164	10	27	2017-08-04 11:57:23.290242	f	t
1165	10	29	2017-08-07 11:57:23.290273	f	t
1166	10	17	2017-08-03 11:57:23.290303	f	t
1167	10	32	2017-07-27 11:57:23.290333	f	t
1168	10	11	2017-08-09 11:57:23.290363	f	t
1169	10	35	2017-07-27 11:57:23.290392	f	t
1170	10	19	2017-07-23 11:57:23.290421	f	t
1171	10	29	2017-07-25 11:57:23.290451	f	t
1172	11	7	2017-08-17 11:57:23.290481	f	t
1173	11	16	2017-08-17 11:57:23.290511	f	t
1174	11	17	2017-08-06 11:57:23.29054	f	t
1175	11	8	2017-08-10 11:57:23.290571	f	t
1176	12	24	2017-08-09 11:57:23.2906	t	t
1177	12	17	2017-08-02 11:57:23.29063	t	t
1178	12	36	2017-08-04 11:57:23.29066	f	t
1179	15	11	2017-08-01 11:57:23.29069	f	t
1180	16	23	2017-08-12 11:57:23.290719	t	t
1181	16	10	2017-08-03 11:57:23.290749	f	t
1182	16	27	2017-08-01 11:57:23.290779	f	t
1183	16	9	2017-08-10 11:57:23.290808	f	t
1184	17	17	2017-08-12 11:57:23.290837	t	t
1185	17	25	2017-07-30 11:57:23.290867	t	t
1186	17	9	2017-08-15 11:57:23.290896	t	t
1187	17	20	2017-08-01 11:57:23.290926	t	t
1188	17	28	2017-07-29 11:57:23.290977	t	t
1189	17	13	2017-07-24 11:57:23.291007	t	t
1190	17	31	2017-07-30 11:57:23.291046	t	t
1191	17	37	2017-07-24 11:57:23.291077	t	t
1192	17	28	2017-07-28 11:57:23.291108	f	t
1193	17	17	2017-07-25 11:57:23.291138	f	t
1194	17	24	2017-08-16 11:57:23.291181	f	t
1195	17	31	2017-08-10 11:57:23.291241	f	t
1196	19	10	2017-07-26 11:57:23.291302	t	t
1197	19	29	2017-07-28 11:57:23.291341	t	t
1198	19	9	2017-07-30 11:57:23.291375	t	t
1199	19	14	2017-07-29 11:57:23.291406	t	t
1200	19	8	2017-08-08 11:57:23.291438	t	t
1201	19	33	2017-08-07 11:57:23.291471	t	t
1202	19	31	2017-08-01 11:57:23.291502	f	t
1203	19	11	2017-08-01 11:57:23.291533	f	t
1204	19	23	2017-08-09 11:57:23.291565	f	t
1205	19	29	2017-08-02 11:57:23.291596	f	t
1206	19	25	2017-07-27 11:57:23.291628	f	t
1207	19	36	2017-08-11 11:57:23.291684	f	t
1208	19	19	2017-07-23 11:57:23.29174	f	t
1209	19	35	2017-07-30 11:57:23.291798	f	t
1210	19	18	2017-07-30 11:57:23.29185	f	t
1211	19	24	2017-07-28 11:57:23.291905	f	t
1212	19	9	2017-08-14 11:57:23.291967	f	t
1213	19	33	2017-08-15 11:57:23.292041	f	t
1214	19	22	2017-07-27 11:57:23.292104	f	t
1215	19	13	2017-07-31 11:57:23.29216	f	t
1216	19	20	2017-08-09 11:57:23.292228	f	t
1217	19	8	2017-08-15 11:57:23.292299	f	t
1218	19	37	2017-07-24 11:57:23.292383	f	t
1219	19	15	2017-07-28 11:57:23.29242	f	t
1220	19	29	2017-07-29 11:57:23.292481	f	t
1221	19	27	2017-07-28 11:57:23.29253	f	t
1222	19	7	2017-08-06 11:57:23.292591	f	t
1223	19	17	2017-08-12 11:57:23.292644	f	t
1224	19	12	2017-08-14 11:57:23.292679	f	t
1225	19	16	2017-08-16 11:57:23.29271	f	t
1226	19	21	2017-07-31 11:57:23.29274	f	t
1227	19	10	2017-08-15 11:57:23.292771	f	t
1228	20	14	2017-08-17 11:57:23.292812	t	t
1229	20	11	2017-08-02 11:57:23.292844	t	t
1230	20	31	2017-08-03 11:57:23.292885	t	t
1231	20	29	2017-08-06 11:57:23.292916	t	t
1232	20	36	2017-08-09 11:57:23.292947	f	t
1233	20	8	2017-08-08 11:57:23.292977	f	t
1234	20	7	2017-08-04 11:57:23.293008	f	t
1235	20	10	2017-08-04 11:57:23.293039	f	t
1236	20	13	2017-07-26 11:57:23.293069	f	t
1237	20	24	2017-08-06 11:57:23.293099	f	t
1238	20	18	2017-08-04 11:57:23.29313	f	t
1239	20	33	2017-08-14 11:57:23.29316	f	t
1240	20	27	2017-07-28 11:57:23.29319	f	t
1241	21	28	2017-08-14 11:57:23.293221	t	t
1242	21	27	2017-07-24 11:57:23.293252	t	t
1243	21	34	2017-08-05 11:57:23.293283	t	t
1244	21	8	2017-07-23 11:57:23.293313	t	t
1245	21	10	2017-08-12 11:57:23.293343	t	t
1246	21	35	2017-08-13 11:57:23.293373	t	t
1247	21	9	2017-07-28 11:57:23.293403	t	t
1248	21	21	2017-08-13 11:57:23.293433	t	t
1249	21	22	2017-08-06 11:57:23.293464	t	t
1250	21	25	2017-08-11 11:57:23.293494	t	t
1251	21	26	2017-08-10 11:57:23.293523	t	t
1252	21	13	2017-07-28 11:57:23.293554	t	t
1253	21	18	2017-07-24 11:57:23.293585	t	t
1254	21	15	2017-07-31 11:57:23.293615	t	t
1255	21	25	2017-07-28 11:57:23.293645	f	t
1256	21	16	2017-07-30 11:57:23.293675	f	t
1257	21	22	2017-08-13 11:57:23.293724	f	t
1258	21	8	2017-08-10 11:57:23.293775	f	t
1259	21	37	2017-08-04 11:57:23.293825	f	t
1260	21	7	2017-08-10 11:57:23.293897	f	t
1261	21	23	2017-07-24 11:57:23.29395	f	t
1262	21	18	2017-07-26 11:57:23.294004	f	t
1263	21	20	2017-07-23 11:57:23.294073	f	t
1264	21	29	2017-07-28 11:57:23.294134	f	t
1265	21	33	2017-08-01 11:57:23.294193	f	t
1266	21	17	2017-08-04 11:57:23.294252	f	t
1267	21	28	2017-08-11 11:57:23.294313	f	t
1268	21	9	2017-07-27 11:57:23.294372	f	t
1269	21	26	2017-08-09 11:57:23.294431	f	t
1270	21	31	2017-08-13 11:57:23.294489	f	t
1271	23	12	2017-08-15 11:57:23.294544	t	t
1272	23	24	2017-08-04 11:57:23.294581	t	t
1273	23	13	2017-07-30 11:57:23.294616	t	t
1274	23	35	2017-07-24 11:57:23.294651	t	t
1275	23	17	2017-07-28 11:57:23.294686	t	t
1276	23	18	2017-08-06 11:57:23.294721	t	t
1277	23	20	2017-08-16 11:57:23.294756	t	t
1278	23	16	2017-08-04 11:57:23.29479	t	t
1279	23	11	2017-08-08 11:57:23.294824	t	t
1280	23	9	2017-07-25 11:57:23.294857	t	t
1281	23	10	2017-07-27 11:57:23.294903	t	t
1282	23	22	2017-08-04 11:57:23.294961	t	t
1283	23	23	2017-08-09 11:57:23.295017	t	t
1284	23	20	2017-08-17 11:57:23.295077	f	t
1285	23	16	2017-08-12 11:57:23.295127	f	t
1286	24	25	2017-08-11 11:57:23.295179	t	t
1287	24	37	2017-07-24 11:57:23.295231	t	t
1288	24	24	2017-08-11 11:57:23.295284	f	t
1289	26	33	2017-07-31 11:57:23.295336	t	t
1290	26	10	2017-07-28 11:57:23.295389	t	t
1291	26	11	2017-08-15 11:57:23.295443	t	t
1292	26	27	2017-08-09 11:57:23.295499	t	t
1293	26	21	2017-08-08 11:57:23.295552	t	t
1294	26	9	2017-07-31 11:57:23.295612	t	t
1295	26	29	2017-08-13 11:57:23.295674	t	t
1296	26	17	2017-08-08 11:57:23.295738	t	t
1297	26	37	2017-08-01 11:57:23.295802	t	t
1298	27	15	2017-08-15 11:57:23.295867	t	t
1299	27	19	2017-08-17 11:57:23.295929	t	t
1300	27	33	2017-08-01 11:57:23.29599	t	t
1301	27	16	2017-08-04 11:57:23.296043	t	t
1302	27	18	2017-07-29 11:57:23.296095	t	t
1303	27	24	2017-07-31 11:57:23.296153	t	t
1304	27	14	2017-07-31 11:57:23.296237	t	t
1305	27	26	2017-08-07 11:57:23.296292	t	t
1306	27	23	2017-07-27 11:57:23.296358	t	t
1307	27	22	2017-08-13 11:57:23.296418	t	t
1308	27	13	2017-08-07 11:57:23.296476	t	t
1309	28	15	2017-07-25 11:57:23.296536	t	t
1310	28	11	2017-07-31 11:57:23.296598	t	t
1311	28	23	2017-08-11 11:57:23.29666	f	t
1312	29	12	2017-07-24 11:57:23.296725	t	t
1313	29	25	2017-07-23 11:57:23.296789	t	t
1314	29	16	2017-08-04 11:57:23.296851	t	t
1315	29	15	2017-08-13 11:57:23.296911	t	t
1316	29	10	2017-07-26 11:57:23.29698	t	t
1317	29	28	2017-08-04 11:57:23.297046	t	t
1318	29	34	2017-07-30 11:57:23.297108	t	t
1319	29	14	2017-07-23 11:57:23.297168	t	t
1320	29	20	2017-08-09 11:57:23.297229	t	t
1321	29	24	2017-07-30 11:57:23.297291	t	t
1322	29	33	2017-07-28 11:57:23.297356	t	t
1323	29	35	2017-07-31 11:57:23.29742	t	t
1324	29	36	2017-08-01 11:57:23.297481	t	t
1325	29	27	2017-08-16 11:57:23.297548	t	t
1326	29	9	2017-08-14 11:57:23.297615	t	t
1327	29	18	2017-08-15 11:57:23.29768	t	t
1328	29	31	2017-08-14 11:57:23.297738	t	t
1329	29	21	2017-08-04 11:57:23.297791	t	t
1330	29	8	2017-08-07 11:57:23.297877	t	t
1331	29	37	2017-07-26 11:57:23.297945	t	t
1332	29	23	2017-08-03 11:57:23.298003	f	t
1333	29	29	2017-08-15 11:57:23.298052	f	t
1334	29	24	2017-08-05 11:57:23.29809	f	t
1335	29	12	2017-08-10 11:57:23.298125	f	t
1336	29	36	2017-08-10 11:57:23.29816	f	t
1337	29	29	2017-08-07 11:57:23.298196	f	t
1338	29	35	2017-08-05 11:57:23.29823	f	t
1339	29	33	2017-08-01 11:57:23.298265	f	t
1340	29	20	2017-07-26 11:57:23.298301	f	t
1341	29	16	2017-07-29 11:57:23.298387	f	t
1342	29	25	2017-07-31 11:57:23.298429	f	t
1343	29	15	2017-08-06 11:57:23.298465	f	t
1344	29	31	2017-08-10 11:57:23.2985	f	t
1345	29	27	2017-08-03 11:57:23.298534	f	t
1346	29	32	2017-08-13 11:57:23.298569	f	t
1347	29	11	2017-08-04 11:57:23.298604	f	t
1348	29	22	2017-08-08 11:57:23.298638	f	t
1349	30	36	2017-07-26 11:57:23.298672	t	t
1350	30	35	2017-08-13 11:57:23.298707	t	t
1351	30	31	2017-08-14 11:57:23.298744	t	t
1352	30	33	2017-08-05 11:57:23.298779	t	t
1353	30	11	2017-08-03 11:57:23.298813	t	t
1354	30	29	2017-08-11 11:57:23.298848	t	t
1355	30	32	2017-08-08 11:57:23.298882	t	t
1356	30	20	2017-08-15 11:57:23.298918	t	t
1357	30	19	2017-08-02 11:57:23.298954	t	t
1358	30	13	2017-07-26 11:57:23.298989	t	t
1359	30	24	2017-08-02 11:57:23.299023	t	t
1360	30	12	2017-07-27 11:57:23.299074	t	t
1361	30	21	2017-07-30 11:57:23.299104	t	t
1362	30	18	2017-07-29 11:57:23.299134	t	t
1363	30	22	2017-08-11 11:57:23.299181	t	t
1364	30	14	2017-07-23 11:57:23.299214	t	t
1365	30	34	2017-08-01 11:57:23.299244	t	t
1366	30	7	2017-08-17 11:57:23.299274	t	t
1367	30	26	2017-08-15 11:57:23.299304	t	t
1368	30	27	2017-07-30 11:57:23.299333	t	t
1369	30	37	2017-07-31 11:57:23.299363	t	t
1370	30	9	2017-08-08 11:57:23.299392	t	t
1371	30	16	2017-07-30 11:57:23.299421	t	t
1372	30	10	2017-07-30 11:57:23.299451	t	t
1373	30	11	2017-08-06 11:57:23.299481	f	t
1374	30	28	2017-07-28 11:57:23.29951	f	t
1375	30	25	2017-07-28 11:57:23.299539	f	t
1376	30	29	2017-07-26 11:57:23.299568	f	t
1377	30	37	2017-08-05 11:57:23.299597	f	t
1378	30	22	2017-08-07 11:57:23.299626	f	t
1379	30	34	2017-07-29 11:57:23.299656	f	t
1380	30	24	2017-08-07 11:57:23.299685	f	t
1381	30	15	2017-07-30 11:57:23.299714	f	t
1382	30	33	2017-08-05 11:57:23.299744	f	t
1383	32	17	2017-08-10 11:57:23.299773	t	t
1384	32	23	2017-08-11 11:57:23.299803	t	t
1385	32	18	2017-07-24 11:57:23.299832	t	t
1386	32	10	2017-08-01 11:57:23.299861	t	t
1387	32	36	2017-08-11 11:57:23.29989	t	t
1388	32	8	2017-08-12 11:57:23.299919	f	t
1389	32	18	2017-08-01 11:57:23.299949	f	t
1390	32	24	2017-08-16 11:57:23.299979	f	t
1391	32	20	2017-08-17 11:57:23.300009	f	t
1392	32	13	2017-08-16 11:57:23.300048	f	t
1393	32	10	2017-07-23 11:57:23.300079	f	t
1394	32	22	2017-08-06 11:57:23.30011	f	t
1395	32	23	2017-08-09 11:57:23.300142	f	t
1396	32	29	2017-08-16 11:57:23.300173	f	t
1397	32	28	2017-08-08 11:57:23.300204	f	t
1398	32	37	2017-07-28 11:57:23.300235	f	t
1399	32	7	2017-08-04 11:57:23.300266	f	t
1400	34	7	2017-08-10 11:57:23.300296	t	t
1401	34	28	2017-07-25 11:57:23.300327	t	t
1402	34	33	2017-07-29 11:57:23.300358	t	t
1403	34	34	2017-08-01 11:57:23.300389	t	t
1404	34	20	2017-07-23 11:57:23.30042	t	t
1405	34	31	2017-07-24 11:57:23.30045	t	t
1406	34	11	2017-07-25 11:57:23.300481	t	t
1407	34	9	2017-07-27 11:57:23.300512	t	t
1408	34	16	2017-08-14 11:57:23.300542	t	t
1409	34	36	2017-07-31 11:57:23.300573	t	t
1410	34	15	2017-07-29 11:57:23.300604	t	t
1411	34	32	2017-08-10 11:57:23.300635	t	t
1412	34	25	2017-08-08 11:57:23.300666	t	t
1413	34	31	2017-07-29 11:57:23.300697	f	t
1414	34	37	2017-07-28 11:57:23.300728	f	t
1415	34	18	2017-07-27 11:57:23.300759	f	t
1416	34	19	2017-07-26 11:57:23.30079	f	t
1417	34	16	2017-08-13 11:57:23.300821	f	t
1418	34	26	2017-08-04 11:57:23.300852	f	t
1419	34	13	2017-08-11 11:57:23.300884	f	t
1420	35	28	2017-07-24 11:57:23.300915	t	t
1421	35	22	2017-08-07 11:57:23.300946	t	t
1422	35	19	2017-08-07 11:57:23.300977	t	t
1423	35	15	2017-07-30 11:57:23.301008	t	t
1424	35	16	2017-08-13 11:57:23.301048	t	t
1425	35	37	2017-08-16 11:57:23.301079	t	t
1426	35	32	2017-08-17 11:57:23.301108	t	t
1427	35	9	2017-08-11 11:57:23.301138	t	t
1428	35	21	2017-08-06 11:57:23.301167	t	t
1429	35	13	2017-08-17 11:57:23.301197	t	t
1430	35	29	2017-07-27 11:57:23.301226	t	t
1431	35	34	2017-08-03 11:57:23.301256	t	t
1432	35	25	2017-08-08 11:57:23.301286	t	t
1433	35	33	2017-08-02 11:57:23.301315	t	t
1434	35	10	2017-07-23 11:57:23.301343	t	t
1435	35	12	2017-07-27 11:57:23.301373	t	t
1436	35	26	2017-07-24 11:57:23.301403	f	t
1437	35	23	2017-08-16 11:57:23.301432	f	t
1438	35	10	2017-08-06 11:57:23.301462	f	t
1439	35	29	2017-07-27 11:57:23.301491	f	t
1440	35	37	2017-07-27 11:57:23.301521	f	t
1441	35	24	2017-08-09 11:57:23.30155	f	t
1442	35	35	2017-08-15 11:57:23.301579	f	t
1443	35	13	2017-08-16 11:57:23.301608	f	t
1444	35	11	2017-08-12 11:57:23.301637	f	t
1445	35	7	2017-07-24 11:57:23.301667	f	t
1446	35	36	2017-08-03 11:57:23.301697	f	t
1447	36	25	2017-08-05 11:57:23.301727	t	t
1448	36	29	2017-08-09 11:57:23.301756	t	t
1449	36	34	2017-08-12 11:57:23.301786	t	t
1450	36	31	2017-08-16 11:57:23.301816	t	t
1451	36	10	2017-08-07 11:57:23.301845	t	t
1452	36	15	2017-07-26 11:57:23.301894	t	t
1453	36	32	2017-08-09 11:57:23.301924	t	t
1454	36	18	2017-07-30 11:57:23.301955	t	t
1455	36	27	2017-08-05 11:57:23.301985	t	t
1456	36	26	2017-08-14 11:57:23.302015	t	t
1457	36	8	2017-08-13 11:57:23.302045	t	t
1458	36	35	2017-08-17 11:57:23.302076	t	t
1459	36	29	2017-08-17 11:57:23.302107	t	t
1460	36	21	2017-08-06 11:57:23.302136	t	t
1461	36	9	2017-07-23 11:57:23.302166	t	t
1462	36	11	2017-08-12 11:57:23.302197	t	t
1463	36	24	2017-08-12 11:57:23.302228	t	t
1464	36	16	2017-08-15 11:57:23.302258	t	t
1465	39	35	2017-07-31 11:57:23.302288	t	t
1466	39	13	2017-08-14 11:57:23.302319	f	t
1467	39	8	2017-08-17 11:57:23.302349	f	t
1468	39	34	2017-08-15 11:57:23.30238	f	t
1469	39	20	2017-08-08 11:57:23.30241	f	t
1470	39	25	2017-08-01 11:57:23.30244	f	t
1471	39	15	2017-08-01 11:57:23.302471	f	t
1472	39	26	2017-08-13 11:57:23.302501	f	t
1473	39	32	2017-07-30 11:57:23.302532	f	t
1474	40	37	2017-07-24 11:57:23.302563	t	t
1475	40	32	2017-08-13 11:57:23.302594	f	t
1476	40	33	2017-08-15 11:57:23.302624	f	t
1477	40	17	2017-08-09 11:57:23.302654	f	t
1478	40	34	2017-08-08 11:57:23.302685	f	t
1479	40	10	2017-08-17 11:57:23.302716	f	t
1480	40	19	2017-07-28 11:57:23.302747	f	t
1481	40	24	2017-08-17 11:57:23.302777	f	t
1482	40	14	2017-07-27 11:57:23.302807	f	t
1483	40	18	2017-08-05 11:57:23.302838	f	t
1484	40	8	2017-07-24 11:57:23.302868	f	t
1485	40	11	2017-08-08 11:57:23.302898	f	t
1486	40	25	2017-08-09 11:57:23.302929	f	t
1487	40	12	2017-08-03 11:57:23.302959	f	t
1488	41	33	2017-07-28 11:57:23.302989	t	t
1489	41	14	2017-08-12 11:57:23.303019	t	t
1490	41	11	2017-07-30 11:57:23.303049	f	t
1491	41	19	2017-08-10 11:57:23.30308	f	t
1492	41	21	2017-08-08 11:57:23.30311	f	t
1493	41	12	2017-08-17 11:57:23.30314	f	t
1494	41	22	2017-07-23 11:57:23.30317	f	t
1495	41	29	2017-07-31 11:57:23.303199	f	t
1496	41	13	2017-07-29 11:57:23.30323	f	t
1497	41	7	2017-07-29 11:57:23.30326	f	t
1498	41	29	2017-07-24 11:57:23.30329	f	t
1499	42	9	2017-08-12 11:57:23.303319	t	t
1500	42	33	2017-08-04 11:57:23.30335	t	t
1501	42	24	2017-08-04 11:57:23.303379	t	t
1502	42	23	2017-08-08 11:57:23.303409	t	t
1503	42	26	2017-07-24 11:57:23.303439	t	t
1504	42	27	2017-08-02 11:57:23.303469	t	t
1505	42	17	2017-08-15 11:57:23.303499	t	t
1506	42	13	2017-07-28 11:57:23.30353	t	t
1507	42	11	2017-08-01 11:57:23.303561	t	t
1508	42	14	2017-07-25 11:57:23.303591	t	t
1509	42	28	2017-07-25 11:57:23.303621	t	t
1510	42	16	2017-08-05 11:57:23.303652	t	t
1511	42	34	2017-07-29 11:57:23.303682	t	t
1512	42	29	2017-08-04 11:57:23.303712	t	t
1513	42	8	2017-07-25 11:57:23.303741	t	t
1514	42	25	2017-08-12 11:57:23.303772	t	t
1515	42	37	2017-08-16 11:57:23.303802	t	t
1516	42	29	2017-08-16 11:57:23.303833	t	t
1517	42	32	2017-08-03 11:57:23.303864	f	t
1518	42	28	2017-08-01 11:57:23.303894	f	t
1519	42	9	2017-07-26 11:57:23.303925	f	t
1520	42	35	2017-08-17 11:57:23.303956	f	t
1521	42	21	2017-08-05 11:57:23.303986	f	t
1522	42	10	2017-08-01 11:57:23.304016	f	t
1523	42	29	2017-07-27 11:57:23.304047	f	t
1524	42	29	2017-08-07 11:57:23.304077	f	t
1525	42	12	2017-08-05 11:57:23.304107	f	t
1526	42	23	2017-07-27 11:57:23.304137	f	t
1527	42	26	2017-07-28 11:57:23.304167	f	t
1528	42	24	2017-08-06 11:57:23.304196	f	t
1529	42	19	2017-08-15 11:57:23.304226	f	t
1530	42	15	2017-08-17 11:57:23.304256	f	t
1531	42	18	2017-07-31 11:57:23.304286	f	t
1532	42	25	2017-07-24 11:57:23.304316	f	t
1533	42	16	2017-07-29 11:57:23.304347	f	t
1534	42	14	2017-08-10 11:57:23.304376	f	t
1535	42	37	2017-08-04 11:57:23.304407	f	t
1536	42	20	2017-08-03 11:57:23.304437	f	t
1537	42	13	2017-07-31 11:57:23.304466	f	t
1538	42	7	2017-08-03 11:57:23.304496	f	t
1539	42	33	2017-08-03 11:57:23.304526	f	t
1540	44	19	2017-08-14 11:57:23.304556	t	t
1541	44	17	2017-08-13 11:57:23.304587	t	t
1542	44	16	2017-07-31 11:57:23.304616	f	t
1543	44	20	2017-07-24 11:57:23.304647	f	t
1544	46	11	2017-08-10 11:57:23.304677	t	t
1545	46	27	2017-08-12 11:57:23.304707	f	t
1546	46	35	2017-08-05 11:57:23.304737	f	t
1547	46	14	2017-07-27 11:57:23.304767	f	t
1548	46	29	2017-08-03 11:57:23.304797	f	t
1549	46	22	2017-07-27 11:57:23.304826	f	t
1550	46	33	2017-08-12 11:57:23.304857	f	t
1551	46	31	2017-07-23 11:57:23.304888	f	t
1552	46	36	2017-07-24 11:57:23.304918	f	t
1553	46	7	2017-07-26 11:57:23.304948	f	t
1554	46	17	2017-08-08 11:57:23.304979	f	t
1555	46	13	2017-08-08 11:57:23.30502	f	t
1556	47	31	2017-08-16 11:57:23.305074	t	t
1557	47	36	2017-07-30 11:57:23.305107	t	t
1558	47	12	2017-07-25 11:57:23.305138	t	t
1559	47	29	2017-08-04 11:57:23.305168	t	t
1560	47	32	2017-08-04 11:57:23.305199	f	t
1561	47	9	2017-08-11 11:57:23.305229	f	t
1562	47	7	2017-07-23 11:57:23.305259	f	t
1563	49	27	2017-07-23 11:57:23.305289	t	t
1564	49	17	2017-07-24 11:57:23.305319	t	t
1565	49	25	2017-08-16 11:57:23.305349	t	t
1566	49	20	2017-07-25 11:57:23.305379	t	t
1567	49	22	2017-08-01 11:57:23.30541	t	t
1568	49	36	2017-07-26 11:57:23.305439	t	t
1569	49	9	2017-08-03 11:57:23.30547	t	t
1570	49	26	2017-08-04 11:57:23.305514	t	t
1571	49	23	2017-08-11 11:57:23.30558	t	t
1572	49	14	2017-07-26 11:57:23.305669	t	t
1573	49	7	2017-08-02 11:57:23.305726	f	t
1574	49	34	2017-07-24 11:57:23.305796	f	t
1575	49	13	2017-07-28 11:57:23.305827	f	t
1576	49	8	2017-08-13 11:57:23.305864	f	t
1577	49	33	2017-08-13 11:57:23.305895	f	t
1578	49	9	2017-08-12 11:57:23.305925	f	t
1579	49	17	2017-08-15 11:57:23.305954	f	t
1580	49	29	2017-07-26 11:57:23.305984	f	t
1581	49	21	2017-08-13 11:57:23.306013	f	t
1582	50	24	2017-08-08 11:57:23.306043	t	t
1583	50	20	2017-07-23 11:57:23.306072	t	t
1584	50	29	2017-08-07 11:57:23.306101	t	t
1585	50	13	2017-07-25 11:57:23.30613	t	t
1586	50	15	2017-08-07 11:57:23.30616	t	t
1587	50	11	2017-08-06 11:57:23.30619	f	t
1588	50	12	2017-07-28 11:57:23.306219	f	t
1589	50	9	2017-08-05 11:57:23.306248	f	t
1590	50	28	2017-07-31 11:57:23.306277	f	t
1591	50	36	2017-08-17 11:57:23.306307	f	t
1592	50	23	2017-07-30 11:57:23.306337	f	t
1593	50	37	2017-07-29 11:57:23.306367	f	t
1594	50	29	2017-08-02 11:57:23.306396	f	t
1595	50	21	2017-08-06 11:57:23.306426	f	t
1596	50	7	2017-08-05 11:57:23.306456	f	t
1597	51	19	2017-08-09 11:57:23.306486	t	t
1598	51	8	2017-08-02 11:57:23.306516	t	t
1599	51	31	2017-08-03 11:57:23.306546	t	t
1600	51	37	2017-08-05 11:57:23.306576	t	t
1601	51	29	2017-07-28 11:57:23.306605	t	t
1602	51	17	2017-07-27 11:57:23.306634	t	t
1603	51	27	2017-07-31 11:57:23.306663	t	t
1604	51	20	2017-07-26 11:57:23.306693	f	t
1605	51	12	2017-08-13 11:57:23.306722	f	t
1606	51	18	2017-08-02 11:57:23.306752	f	t
1607	51	23	2017-07-27 11:57:23.306781	f	t
1608	51	14	2017-08-14 11:57:23.306811	f	t
1609	51	33	2017-07-28 11:57:23.30684	f	t
1610	51	34	2017-08-11 11:57:23.306869	f	t
1611	51	36	2017-08-08 11:57:23.306898	f	t
1612	51	19	2017-07-29 11:57:23.306928	f	t
1613	51	17	2017-07-29 11:57:23.306957	f	t
1614	51	29	2017-08-16 11:57:23.306986	f	t
1615	51	29	2017-08-08 11:57:23.307015	f	t
1616	51	37	2017-08-15 11:57:23.307044	f	t
1617	51	35	2017-08-13 11:57:23.307073	f	t
1618	51	27	2017-08-15 11:57:23.307102	f	t
1619	51	16	2017-08-17 11:57:23.307132	f	t
1620	51	25	2017-07-27 11:57:23.307161	f	t
1621	54	33	2017-08-08 11:57:23.30719	t	t
1622	54	35	2017-07-26 11:57:23.307219	t	t
1623	54	31	2017-08-10 11:57:23.307249	t	t
1624	54	10	2017-07-26 11:57:23.307278	t	t
1625	54	15	2017-08-09 11:57:23.307307	t	t
1626	54	27	2017-08-10 11:57:23.307336	t	t
1627	54	13	2017-07-25 11:57:23.307365	t	t
1628	54	16	2017-07-23 11:57:23.307394	t	t
1629	54	32	2017-08-16 11:57:23.307423	t	t
1630	54	8	2017-07-27 11:57:23.307453	t	t
1631	54	7	2017-08-17 11:57:23.307483	t	t
1632	54	25	2017-08-06 11:57:23.307513	t	t
1633	54	9	2017-08-14 11:57:23.307542	t	t
1634	54	29	2017-08-03 11:57:23.307572	t	t
1635	54	16	2017-08-13 11:57:23.307601	f	t
1636	54	17	2017-08-01 11:57:23.30763	f	t
1637	54	24	2017-08-01 11:57:23.307659	f	t
1638	54	23	2017-08-02 11:57:23.307688	f	t
1639	54	13	2017-08-06 11:57:23.307716	f	t
1640	54	9	2017-08-04 11:57:23.307745	f	t
1641	54	22	2017-08-10 11:57:23.307774	f	t
1642	54	29	2017-07-31 11:57:23.307802	f	t
1643	54	31	2017-07-23 11:57:23.307832	f	t
1644	54	33	2017-08-10 11:57:23.30786	f	t
1645	54	12	2017-08-12 11:57:23.307889	f	t
1646	54	15	2017-07-28 11:57:23.307918	f	t
1647	54	8	2017-08-11 11:57:23.307948	f	t
1648	54	29	2017-07-28 11:57:23.307978	f	t
1649	54	36	2017-08-05 11:57:23.308008	f	t
1650	54	18	2017-08-11 11:57:23.308037	f	t
1651	55	15	2017-08-17 11:57:23.308066	t	t
1652	55	20	2017-08-03 11:57:23.308095	t	t
1653	55	15	2017-07-25 11:57:23.308123	f	t
1654	55	9	2017-08-04 11:57:23.308152	f	t
1655	56	33	2017-08-05 11:57:23.308181	t	t
1656	56	25	2017-07-25 11:57:23.308211	t	t
1657	56	33	2017-08-02 11:57:23.308239	f	t
1658	56	29	2017-07-26 11:57:23.308269	f	t
1659	57	22	2017-07-25 11:57:23.308298	t	t
1660	57	27	2017-08-05 11:57:23.308327	t	t
1661	57	19	2017-08-03 11:57:23.308356	t	t
1662	57	16	2017-08-05 11:57:23.308409	t	t
1663	57	24	2017-08-15 11:57:23.308449	t	t
1664	57	34	2017-07-27 11:57:23.308488	t	t
1665	57	36	2017-08-01 11:57:23.308517	t	t
1666	57	8	2017-08-14 11:57:23.308557	t	t
1667	57	23	2017-08-06 11:57:23.308587	t	t
1668	57	29	2017-07-30 11:57:23.308626	t	t
1669	57	21	2017-08-03 11:57:23.308656	t	t
1670	57	17	2017-08-06 11:57:23.308685	t	t
1671	57	36	2017-07-25 11:57:23.308715	f	t
1672	57	29	2017-08-14 11:57:23.308744	f	t
1673	57	17	2017-08-01 11:57:23.308773	f	t
1674	57	9	2017-08-12 11:57:23.308802	f	t
1675	57	34	2017-08-15 11:57:23.308832	f	t
1676	57	37	2017-07-26 11:57:23.308861	f	t
1677	57	33	2017-08-02 11:57:23.30889	f	t
1678	57	32	2017-08-17 11:57:23.308929	f	t
1679	57	22	2017-08-16 11:57:23.30896	f	t
1680	57	25	2017-07-24 11:57:23.308999	f	t
1681	57	35	2017-07-27 11:57:23.309028	f	t
1682	57	19	2017-08-17 11:57:23.309067	f	t
1683	57	11	2017-07-31 11:57:23.309097	f	t
1684	57	24	2017-08-15 11:57:23.309129	f	t
1685	57	13	2017-08-10 11:57:23.309161	f	t
1686	57	12	2017-08-08 11:57:23.309193	f	t
1687	57	26	2017-07-29 11:57:23.309224	f	t
1688	58	7	2017-08-07 11:57:23.309255	t	t
1689	58	11	2017-08-12 11:57:23.309287	t	t
1690	58	16	2017-08-16 11:57:23.309319	t	t
1691	58	15	2017-07-29 11:57:23.30935	t	t
1692	58	20	2017-08-15 11:57:23.309381	t	t
1693	58	23	2017-08-16 11:57:23.309412	t	t
1694	58	10	2017-07-26 11:57:23.309443	t	t
1695	58	31	2017-07-25 11:57:23.309474	t	t
1696	58	17	2017-07-26 11:57:23.309504	t	t
1697	58	8	2017-07-25 11:57:23.309535	t	t
1698	58	18	2017-08-03 11:57:23.309565	t	t
1699	58	27	2017-07-25 11:57:23.309596	f	t
1700	58	36	2017-08-09 11:57:23.309627	f	t
1701	58	33	2017-08-13 11:57:23.309658	f	t
1702	58	24	2017-08-15 11:57:23.309689	f	t
1703	58	31	2017-08-07 11:57:23.30972	f	t
1704	58	22	2017-07-29 11:57:23.309751	f	t
1705	58	9	2017-08-02 11:57:23.309782	f	t
1706	58	18	2017-07-24 11:57:23.309812	f	t
1707	58	35	2017-07-26 11:57:23.309843	f	t
1708	58	8	2017-08-08 11:57:23.309879	f	t
1709	58	13	2017-08-08 11:57:23.30991	f	t
1710	58	20	2017-08-03 11:57:23.309943	f	t
1711	59	29	2017-07-27 11:57:23.309984	t	t
1712	59	26	2017-08-16 11:57:23.310031	t	t
1713	59	37	2017-08-17 11:57:23.310072	t	t
1714	59	25	2017-08-07 11:57:23.310102	t	t
1715	59	19	2017-08-01 11:57:23.310132	t	t
1716	59	31	2017-08-13 11:57:23.310161	t	t
1717	59	14	2017-07-25 11:57:23.310191	t	t
1718	59	34	2017-08-03 11:57:23.31022	t	t
1719	59	21	2017-07-28 11:57:23.310249	t	t
1720	59	35	2017-08-12 11:57:23.310279	t	t
1721	59	7	2017-07-23 11:57:23.310309	t	t
1722	59	12	2017-08-09 11:57:23.310339	f	t
1723	59	20	2017-08-13 11:57:23.310368	f	t
1724	59	18	2017-07-26 11:57:23.310398	f	t
1725	59	14	2017-08-03 11:57:23.310428	f	t
1726	59	24	2017-07-24 11:57:23.310457	f	t
1727	59	36	2017-07-28 11:57:23.310486	f	t
1728	59	11	2017-08-14 11:57:23.310516	f	t
1729	59	17	2017-08-01 11:57:23.310546	f	t
1730	59	25	2017-07-28 11:57:23.310575	f	t
1731	59	37	2017-08-08 11:57:23.310605	f	t
1732	59	33	2017-07-26 11:57:23.310635	f	t
1733	60	29	2017-08-02 11:57:23.310665	t	t
1734	60	27	2017-08-07 11:57:23.310694	f	t
1735	60	8	2017-08-09 11:57:23.310723	f	t
1736	60	28	2017-07-29 11:57:23.310753	f	t
1737	60	12	2017-08-11 11:57:23.310781	f	t
1738	60	17	2017-07-25 11:57:23.31081	f	t
1739	60	35	2017-07-23 11:57:23.310839	f	t
1740	60	19	2017-08-12 11:57:23.310869	f	t
1741	60	11	2017-08-15 11:57:23.310898	f	t
1742	60	9	2017-08-03 11:57:23.310927	f	t
1743	60	25	2017-07-27 11:57:23.310956	f	t
1744	60	10	2017-07-27 11:57:23.310986	f	t
1745	61	28	2017-08-09 11:57:23.311015	f	t
1746	61	22	2017-08-02 11:57:23.311045	f	t
1747	62	34	2017-08-10 11:57:23.311074	t	t
1748	62	36	2017-08-03 11:57:23.311104	t	t
1749	62	22	2017-08-05 11:57:23.311133	t	t
1750	63	21	2017-08-02 11:57:23.311163	t	t
1751	63	12	2017-07-28 11:57:23.311194	t	t
1752	63	15	2017-07-25 11:57:23.311223	t	t
1753	64	7	2017-08-07 11:57:23.311252	f	t
1754	64	29	2017-07-23 11:57:23.311281	f	t
1755	64	15	2017-07-31 11:57:23.31131	f	t
1756	64	26	2017-08-07 11:57:23.311339	f	t
1757	64	19	2017-08-04 11:57:23.311368	f	t
1758	64	13	2017-08-07 11:57:23.311397	f	t
1759	64	36	2017-08-15 11:57:23.311426	f	t
1760	64	34	2017-08-09 11:57:23.311455	f	t
1761	64	10	2017-07-30 11:57:23.311484	f	t
1762	64	33	2017-08-17 11:57:23.311514	f	t
1763	64	11	2017-08-09 11:57:23.311544	f	t
1764	64	21	2017-07-31 11:57:23.311573	f	t
1765	65	8	2017-07-31 11:57:23.311603	t	t
1766	65	26	2017-08-17 11:57:23.311633	t	t
1767	65	36	2017-08-12 11:57:23.311663	t	t
1768	66	17	2017-08-08 11:57:23.311693	t	t
1769	66	16	2017-08-14 11:57:23.311723	t	t
1770	66	7	2017-07-23 11:57:23.311752	t	t
1771	66	9	2017-08-16 11:57:23.311783	t	t
1772	66	22	2017-07-24 11:57:23.311813	t	t
1773	66	13	2017-08-02 11:57:23.311842	t	t
1774	66	12	2017-07-25 11:57:23.311871	f	t
1775	66	10	2017-07-27 11:57:23.311901	f	t
1776	66	35	2017-08-12 11:57:23.31193	f	t
1777	66	14	2017-08-16 11:57:23.311959	f	t
1778	66	31	2017-08-12 11:57:23.311988	f	t
1779	66	21	2017-08-04 11:57:23.312017	f	t
1780	66	7	2017-08-17 11:57:23.312046	f	t
1781	66	17	2017-07-28 11:57:23.312076	f	t
1782	66	18	2017-08-08 11:57:23.312106	f	t
1783	66	20	2017-08-08 11:57:23.312135	f	t
1784	66	29	2017-07-30 11:57:23.312164	f	t
1785	66	34	2017-08-05 11:57:23.312193	f	t
1786	66	33	2017-07-29 11:57:23.312221	f	t
1787	66	32	2017-07-28 11:57:23.31225	f	t
1788	66	9	2017-08-01 11:57:23.312279	f	t
1789	66	11	2017-07-31 11:57:23.312308	f	t
1790	66	25	2017-08-03 11:57:23.312338	f	t
1791	66	27	2017-07-28 11:57:23.312367	f	t
1792	66	26	2017-08-15 11:57:23.312395	f	t
1793	66	37	2017-07-31 11:57:23.312425	f	t
1794	66	36	2017-08-15 11:57:23.312454	f	t
1795	66	24	2017-08-11 11:57:23.312483	f	t
1796	66	16	2017-08-08 11:57:23.312512	f	t
1797	67	35	2017-08-02 11:57:23.312542	t	t
1798	67	19	2017-07-31 11:57:23.312571	t	t
1799	67	25	2017-07-29 11:57:23.3126	t	t
1800	67	9	2017-08-05 11:57:23.31263	t	t
1801	67	12	2017-08-03 11:57:23.312659	t	t
1802	67	14	2017-08-02 11:57:23.312688	t	t
1803	67	36	2017-07-28 11:57:23.312718	t	t
1804	67	35	2017-08-01 11:57:23.312747	f	t
1805	67	15	2017-08-04 11:57:23.312776	f	t
1806	67	14	2017-08-15 11:57:23.312805	f	t
1807	67	11	2017-08-03 11:57:23.312854	f	t
1808	68	31	2017-07-28 11:57:23.312885	t	t
1809	68	12	2017-08-07 11:57:23.312915	t	t
1810	68	14	2017-07-26 11:57:23.312944	t	t
1811	68	36	2017-08-06 11:57:23.312973	t	t
1812	68	23	2017-08-04 11:57:23.313003	t	t
1813	68	26	2017-07-23 11:57:23.313032	t	t
1814	68	22	2017-07-31 11:57:23.313061	t	t
1815	68	28	2017-07-27 11:57:23.31309	t	t
1816	68	16	2017-08-03 11:57:23.313119	t	t
1817	68	29	2017-08-15 11:57:23.313148	t	t
1818	68	27	2017-08-16 11:57:23.313178	t	t
1819	68	8	2017-07-31 11:57:23.313206	t	t
1820	68	32	2017-08-06 11:57:23.313236	t	t
1821	68	18	2017-08-15 11:57:23.313265	t	t
1822	68	11	2017-08-08 11:57:23.313296	t	t
1823	68	9	2017-07-31 11:57:23.313324	t	t
1824	68	34	2017-08-13 11:57:23.313354	t	t
1825	68	20	2017-08-02 11:57:23.313385	t	t
1826	68	37	2017-08-04 11:57:23.313414	t	t
1827	68	25	2017-08-12 11:57:23.313443	t	t
1828	68	15	2017-07-27 11:57:23.313473	t	t
1829	68	13	2017-08-02 11:57:23.313502	t	t
1830	68	31	2017-08-17 11:57:23.313531	f	t
1831	68	22	2017-08-01 11:57:23.313561	f	t
1832	6	14	2017-08-15 11:57:23.31359	f	t
1833	7	11	2017-08-13 11:57:23.313619	t	t
1834	7	12	2017-08-03 11:57:23.313649	t	t
1835	7	18	2017-07-30 11:57:23.313678	t	t
1836	7	24	2017-08-02 11:57:23.313708	t	t
1837	7	17	2017-08-15 11:57:23.313737	t	t
1838	7	23	2017-08-12 11:57:23.313767	t	t
1839	7	15	2017-08-10 11:57:23.313796	t	t
1840	7	33	2017-08-05 11:57:23.313825	t	t
1841	7	32	2017-08-04 11:57:23.31386	f	t
1842	7	25	2017-07-28 11:57:23.313891	f	t
1843	7	7	2017-08-17 11:57:23.31392	f	t
1844	7	34	2017-07-31 11:57:23.31395	f	t
1845	7	16	2017-08-07 11:57:23.313979	f	t
1846	7	12	2017-08-04 11:57:23.314009	f	t
1847	7	22	2017-07-28 11:57:23.314038	f	t
1848	7	36	2017-08-08 11:57:23.314068	f	t
1849	7	29	2017-07-27 11:57:23.314097	f	t
1850	7	23	2017-08-15 11:57:23.314127	f	t
1851	7	13	2017-07-28 11:57:23.314156	f	t
1852	7	33	2017-08-01 11:57:23.314186	f	t
1853	9	18	2017-08-16 11:57:23.314215	t	t
1854	9	17	2017-08-11 11:57:23.314245	t	t
1855	9	12	2017-07-27 11:57:23.314275	t	t
1856	9	29	2017-07-23 11:57:23.314305	t	t
1857	9	32	2017-07-29 11:57:23.314334	t	t
1858	9	26	2017-08-10 11:57:23.314363	t	t
1859	9	28	2017-08-15 11:57:23.314393	f	t
1860	9	15	2017-08-13 11:57:23.314423	f	t
1861	9	18	2017-08-09 11:57:23.314452	f	t
1862	9	37	2017-08-09 11:57:23.314481	f	t
1863	9	33	2017-08-17 11:57:23.314511	f	t
1864	9	29	2017-08-16 11:57:23.314541	f	t
1865	13	34	2017-07-30 11:57:23.31457	t	t
1866	13	17	2017-08-01 11:57:23.3146	t	t
1867	13	24	2017-08-09 11:57:23.31463	t	t
1868	13	37	2017-08-06 11:57:23.314658	t	t
1869	13	20	2017-08-06 11:57:23.314688	t	t
1870	13	31	2017-08-06 11:57:23.314717	t	t
1871	13	26	2017-08-14 11:57:23.314746	t	t
1872	13	29	2017-07-25 11:57:23.314775	t	t
1873	13	14	2017-08-09 11:57:23.314804	t	t
1874	13	12	2017-08-12 11:57:23.314834	t	t
1875	13	11	2017-08-03 11:57:23.314863	t	t
1876	13	28	2017-07-24 11:57:23.314893	t	t
1877	13	16	2017-08-13 11:57:23.314923	t	t
1878	13	23	2017-08-03 11:57:23.314952	t	t
1879	13	10	2017-07-31 11:57:23.314981	t	t
1880	13	22	2017-07-31 11:57:23.31501	t	t
1881	13	19	2017-08-02 11:57:23.31504	t	t
1882	13	21	2017-08-07 11:57:23.31507	t	t
1883	13	33	2017-07-31 11:57:23.315099	t	t
1884	13	25	2017-07-23 11:57:23.315129	t	t
1885	13	26	2017-08-16 11:57:23.315158	f	t
1886	13	19	2017-07-29 11:57:23.315187	f	t
1887	13	24	2017-08-12 11:57:23.315217	f	t
1888	13	7	2017-08-09 11:57:23.315247	f	t
1889	13	17	2017-08-11 11:57:23.315275	f	t
1890	13	29	2017-08-05 11:57:23.315304	f	t
1891	13	10	2017-07-23 11:57:23.315334	f	t
1892	13	37	2017-08-08 11:57:23.315363	f	t
1893	13	36	2017-08-02 11:57:23.315393	f	t
1894	13	9	2017-08-10 11:57:23.315421	f	t
1895	13	15	2017-07-23 11:57:23.31545	f	t
1896	13	20	2017-08-01 11:57:23.315479	f	t
1897	13	21	2017-08-10 11:57:23.315509	f	t
1898	13	22	2017-07-27 11:57:23.315548	f	t
1899	13	35	2017-07-29 11:57:23.315579	f	t
1900	14	36	2017-08-15 11:57:23.315609	f	t
1901	14	12	2017-07-25 11:57:23.31564	f	t
1902	14	27	2017-08-02 11:57:23.31567	f	t
1903	14	7	2017-07-31 11:57:23.315709	f	t
1904	14	29	2017-08-12 11:57:23.315738	f	t
1905	14	25	2017-07-31 11:57:23.315768	f	t
1906	14	8	2017-08-10 11:57:23.315797	f	t
1907	14	18	2017-07-30 11:57:23.315826	f	t
1908	14	21	2017-08-04 11:57:23.315855	f	t
1909	14	20	2017-08-11 11:57:23.315885	f	t
1910	14	19	2017-08-08 11:57:23.315914	f	t
1911	14	29	2017-08-09 11:57:23.315944	f	t
1912	14	33	2017-08-11 11:57:23.315974	f	t
1913	14	13	2017-08-17 11:57:23.316003	f	t
1914	14	37	2017-08-15 11:57:23.316032	f	t
1915	14	31	2017-08-02 11:57:23.316062	f	t
1916	14	26	2017-08-14 11:57:23.316091	f	t
1917	18	10	2017-07-30 11:57:23.316121	t	t
1918	22	7	2017-08-08 11:57:23.31615	t	t
1919	22	36	2017-07-24 11:57:23.316179	t	t
1920	22	29	2017-07-24 11:57:23.316208	t	t
1921	22	17	2017-08-13 11:57:23.316237	f	t
1922	22	21	2017-07-30 11:57:23.316266	f	t
1923	22	31	2017-08-15 11:57:23.316296	f	t
1924	22	24	2017-07-23 11:57:23.316325	f	t
1925	22	36	2017-07-31 11:57:23.316355	f	t
1926	25	15	2017-08-08 11:57:23.316385	t	t
1927	25	17	2017-08-05 11:57:23.316414	t	t
1928	25	19	2017-07-23 11:57:23.316443	t	t
1929	25	23	2017-08-01 11:57:23.316472	t	t
1930	25	32	2017-07-28 11:57:23.316501	t	t
1931	25	28	2017-07-23 11:57:23.316531	t	t
1932	25	14	2017-07-30 11:57:23.316561	t	t
1933	25	36	2017-08-14 11:57:23.316591	t	t
1934	25	18	2017-08-09 11:57:23.316621	t	t
1935	25	22	2017-07-26 11:57:23.316651	t	t
1936	25	8	2017-08-03 11:57:23.316682	t	t
1937	25	34	2017-07-25 11:57:23.316711	t	t
1938	25	12	2017-08-12 11:57:23.31674	t	t
1939	25	27	2017-08-06 11:57:23.31677	t	t
1940	25	29	2017-08-03 11:57:23.316799	f	t
1941	25	33	2017-08-02 11:57:23.316829	f	t
1942	25	11	2017-08-03 11:57:23.316859	f	t
1943	25	13	2017-08-04 11:57:23.316888	f	t
1944	25	10	2017-07-23 11:57:23.316918	f	t
1945	25	19	2017-07-26 11:57:23.316947	f	t
1946	25	16	2017-08-16 11:57:23.316976	f	t
1947	25	32	2017-08-16 11:57:23.317005	f	t
1948	31	19	2017-07-27 11:57:23.317034	t	t
1949	31	8	2017-07-28 11:57:23.317064	t	t
1950	31	14	2017-07-27 11:57:23.317093	t	t
1951	31	20	2017-08-03 11:57:23.317122	t	t
1952	31	29	2017-07-24 11:57:23.317151	t	t
1953	31	22	2017-07-27 11:57:23.31718	t	t
1954	31	17	2017-07-30 11:57:23.317209	f	t
1955	31	9	2017-08-13 11:57:23.317239	f	t
1956	31	29	2017-08-10 11:57:23.317268	f	t
1957	31	11	2017-07-24 11:57:23.317297	f	t
1958	33	28	2017-08-07 11:57:23.317326	t	t
1959	33	19	2017-07-25 11:57:23.317355	t	t
1960	33	29	2017-08-03 11:57:23.317384	t	t
1961	33	21	2017-08-06 11:57:23.317413	t	t
1962	33	24	2017-07-25 11:57:23.317442	t	t
1963	33	26	2017-07-27 11:57:23.317472	t	t
1964	33	18	2017-08-05 11:57:23.317501	t	t
1965	33	11	2017-08-14 11:57:23.317531	t	t
1966	33	37	2017-08-15 11:57:23.31756	f	t
1967	33	35	2017-08-01 11:57:23.31759	f	t
1968	33	26	2017-07-25 11:57:23.317619	f	t
1969	33	32	2017-07-31 11:57:23.317649	f	t
1970	37	29	2017-08-13 11:57:23.317678	t	t
1971	37	35	2017-08-08 11:57:23.317708	t	t
1972	37	21	2017-08-05 11:57:23.317737	t	t
1973	37	22	2017-07-25 11:57:23.317766	t	t
1974	37	19	2017-07-30 11:57:23.317795	t	t
1975	37	28	2017-08-09 11:57:23.317824	t	t
1976	37	25	2017-08-01 11:57:23.317857	t	t
1977	37	7	2017-07-26 11:57:23.317888	t	t
1978	37	26	2017-08-12 11:57:23.317918	t	t
1979	37	17	2017-07-24 11:57:23.317947	t	t
1980	37	29	2017-07-29 11:57:23.317977	t	t
1981	37	31	2017-07-25 11:57:23.318006	t	t
1982	37	16	2017-08-15 11:57:23.318035	t	t
1983	37	9	2017-08-06 11:57:23.318064	t	t
1984	37	24	2017-08-10 11:57:23.318094	t	t
1985	37	27	2017-07-30 11:57:23.318123	t	t
1986	37	37	2017-08-16 11:57:23.318153	t	t
1987	37	15	2017-08-06 11:57:23.318182	t	t
1988	37	16	2017-08-04 11:57:23.318212	f	t
1989	38	32	2017-08-10 11:57:23.318241	f	t
1990	38	8	2017-08-16 11:57:23.318271	f	t
1991	38	9	2017-08-07 11:57:23.318301	f	t
1992	43	18	2017-08-03 11:57:23.31833	t	t
1993	43	16	2017-08-02 11:57:23.31836	t	t
1994	43	15	2017-08-10 11:57:23.318389	t	t
1995	43	22	2017-08-01 11:57:23.318418	t	t
1996	43	36	2017-08-02 11:57:23.318447	t	t
1997	43	20	2017-08-04 11:57:23.318475	t	t
1998	43	17	2017-07-26 11:57:23.318505	t	t
1999	43	34	2017-07-26 11:57:23.318534	t	t
2000	43	33	2017-07-30 11:57:23.318563	t	t
2001	43	24	2017-08-07 11:57:23.318593	t	t
2002	43	28	2017-08-08 11:57:23.318622	t	t
2003	43	25	2017-08-04 11:57:23.318651	t	t
2004	43	26	2017-08-08 11:57:23.31868	f	t
2005	43	25	2017-08-10 11:57:23.318709	f	t
2006	43	9	2017-08-01 11:57:23.318737	f	t
2007	43	20	2017-08-11 11:57:23.318767	f	t
2008	43	17	2017-07-30 11:57:23.318796	f	t
2009	43	16	2017-08-16 11:57:23.318825	f	t
2010	43	24	2017-08-08 11:57:23.318854	f	t
2011	43	33	2017-07-23 11:57:23.318885	f	t
2012	45	36	2017-08-01 11:57:23.318914	t	t
2013	45	22	2017-08-12 11:57:23.318943	t	t
2014	45	15	2017-08-03 11:57:23.318973	t	t
2015	45	25	2017-08-15 11:57:23.319002	t	t
2016	45	18	2017-07-30 11:57:23.319031	t	t
2017	45	27	2017-08-15 11:57:23.31906	t	t
2018	45	13	2017-08-13 11:57:23.31909	t	t
2019	45	16	2017-08-08 11:57:23.31912	t	t
2020	45	23	2017-08-14 11:57:23.319148	t	t
2021	45	19	2017-08-08 11:57:23.319178	t	t
2022	45	7	2017-07-28 11:57:23.319207	t	t
2023	45	14	2017-07-24 11:57:23.319236	t	t
2024	45	33	2017-08-13 11:57:23.319265	t	t
2025	45	21	2017-07-27 11:57:23.319294	t	t
2026	45	20	2017-07-29 11:57:23.319324	t	t
2027	45	26	2017-08-10 11:57:23.319353	t	t
2028	45	29	2017-07-28 11:57:23.319382	t	t
2029	45	29	2017-07-30 11:57:23.319412	t	t
2030	45	27	2017-07-29 11:57:23.319441	f	t
2031	45	22	2017-08-02 11:57:23.31947	f	t
2032	45	11	2017-07-24 11:57:23.3195	f	t
2033	48	25	2017-07-23 11:57:23.319529	t	t
2034	48	31	2017-08-13 11:57:23.319559	t	t
2035	48	34	2017-08-15 11:57:23.319588	t	t
2036	48	18	2017-07-25 11:57:23.319617	t	t
2037	48	24	2017-07-24 11:57:23.319647	t	t
2038	48	22	2017-08-12 11:57:23.319676	t	t
2039	48	36	2017-08-16 11:57:23.319706	f	t
2040	48	11	2017-07-26 11:57:23.319754	f	t
2041	48	15	2017-08-11 11:57:23.319785	f	t
2042	48	35	2017-07-28 11:57:23.319815	f	t
2043	48	8	2017-07-31 11:57:23.319844	f	t
2044	48	9	2017-08-15 11:57:23.319873	f	t
2045	48	7	2017-08-07 11:57:23.319903	f	t
2046	48	25	2017-07-24 11:57:23.319932	f	t
2047	48	33	2017-07-24 11:57:23.319961	f	t
2048	48	13	2017-08-01 11:57:23.319991	f	t
2049	48	31	2017-07-29 11:57:23.32002	f	t
2050	52	15	2017-08-03 11:57:23.32005	t	t
2051	53	16	2017-07-23 11:57:23.32008	f	t
2052	69	33	2017-08-04 11:57:23.320109	t	t
2053	69	17	2017-07-25 11:57:23.320139	t	t
2054	69	22	2017-08-10 11:57:23.320169	t	t
2055	69	11	2017-08-05 11:57:23.320198	t	t
2056	69	7	2017-08-10 11:57:23.320227	t	t
2057	69	8	2017-08-17 11:57:23.320256	t	t
2058	69	36	2017-07-25 11:57:23.320285	t	t
2059	69	35	2017-08-15 11:57:23.320315	t	t
2060	69	10	2017-08-12 11:57:23.320344	t	t
2061	69	18	2017-07-23 11:57:23.320373	t	t
2062	69	13	2017-07-26 11:57:23.320403	t	t
2063	69	9	2017-08-05 11:57:23.320433	t	t
2064	69	21	2017-07-31 11:57:23.320462	t	t
2065	69	27	2017-08-16 11:57:23.320491	t	t
2066	69	15	2017-08-15 11:57:23.32052	t	t
2067	69	28	2017-08-15 11:57:23.320549	t	t
2068	69	28	2017-08-13 11:57:23.320579	f	t
2069	69	22	2017-08-09 11:57:23.320608	f	t
2070	69	37	2017-08-16 11:57:23.320638	f	t
2071	69	15	2017-08-06 11:57:23.320668	f	t
2072	69	27	2017-07-26 11:57:23.320697	f	t
2073	69	24	2017-08-12 11:57:23.320726	f	t
2074	69	19	2017-07-27 11:57:23.320756	f	t
2075	69	7	2017-07-28 11:57:23.320785	f	t
2076	69	26	2017-07-28 11:57:23.320815	f	t
2077	69	8	2017-08-13 11:57:23.320844	f	t
2078	69	18	2017-08-02 11:57:23.320874	f	t
2079	69	25	2017-08-08 11:57:23.320903	f	t
\.


--
-- Name: clicked_arguments_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('clicked_arguments_uid_seq', 2079, true);


--
-- Data for Name: clicked_statements; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY clicked_statements (uid, statement_uid, author_uid, "timestamp", is_up_vote, is_valid) FROM stdin;
1224	1	7	2017-08-03 11:57:23.001869	t	t
1225	1	10	2017-08-10 11:57:23.002002	t	t
1226	1	14	2017-07-23 11:57:23.002042	t	t
1227	1	10	2017-08-11 11:57:23.002076	t	t
1228	1	27	2017-08-04 11:57:23.002107	t	t
1229	1	7	2017-07-27 11:57:23.002138	t	t
1230	1	15	2017-08-07 11:57:23.002168	t	t
1231	1	17	2017-07-25 11:57:23.002197	t	t
1232	1	36	2017-08-13 11:57:23.002226	t	t
1233	1	7	2017-08-07 11:57:23.002256	t	t
1234	1	28	2017-08-07 11:57:23.002286	t	t
1235	1	35	2017-08-03 11:57:23.002315	t	t
1236	1	8	2017-08-14 11:57:23.002344	t	t
1237	1	29	2017-08-01 11:57:23.002373	t	t
1238	1	29	2017-08-14 11:57:23.002403	t	t
1239	1	21	2017-08-01 11:57:23.002432	t	t
1240	1	23	2017-07-23 11:57:23.002461	f	t
1241	1	16	2017-08-09 11:57:23.00249	f	t
1242	1	13	2017-08-17 11:57:23.002519	f	t
1243	1	31	2017-08-12 11:57:23.002547	f	t
1244	1	25	2017-08-04 11:57:23.002576	f	t
1245	1	31	2017-07-28 11:57:23.002604	f	t
1246	1	32	2017-08-14 11:57:23.002633	f	t
1247	1	34	2017-08-03 11:57:23.002663	f	t
1248	1	35	2017-08-01 11:57:23.002692	f	t
1249	1	36	2017-07-24 11:57:23.00272	f	t
1250	1	35	2017-08-10 11:57:23.002749	f	t
1251	1	37	2017-08-08 11:57:23.002778	f	t
1252	1	34	2017-08-13 11:57:23.002806	f	t
1253	1	34	2017-08-13 11:57:23.002835	f	t
1254	1	11	2017-07-30 11:57:23.002864	f	t
1255	1	35	2017-08-09 11:57:23.002893	f	t
1256	1	9	2017-07-23 11:57:23.002921	f	t
1257	1	8	2017-08-05 11:57:23.00295	f	t
1258	2	36	2017-07-23 11:57:23.002978	t	t
1259	3	36	2017-08-14 11:57:23.003006	t	t
1260	3	16	2017-08-06 11:57:23.003034	t	t
1261	3	36	2017-07-30 11:57:23.003062	t	t
1262	3	32	2017-08-11 11:57:23.003091	t	t
1263	3	9	2017-07-24 11:57:23.003118	t	t
1264	3	15	2017-08-05 11:57:23.003147	f	t
1265	3	31	2017-08-02 11:57:23.003176	f	t
1266	3	12	2017-08-02 11:57:23.003205	f	t
1267	3	12	2017-07-26 11:57:23.003233	f	t
1268	3	22	2017-08-14 11:57:23.003261	f	t
1269	4	36	2017-08-13 11:57:23.003289	t	t
1270	4	33	2017-08-15 11:57:23.003317	t	t
1271	4	18	2017-07-31 11:57:23.003345	t	t
1272	4	22	2017-07-23 11:57:23.003373	t	t
1273	4	28	2017-07-31 11:57:23.003402	t	t
1274	4	15	2017-07-30 11:57:23.00343	t	t
1275	4	16	2017-08-07 11:57:23.003458	t	t
1276	4	22	2017-08-07 11:57:23.003487	t	t
1277	4	31	2017-08-05 11:57:23.003515	t	t
1278	4	35	2017-08-14 11:57:23.003543	t	t
1279	4	20	2017-07-27 11:57:23.003572	t	t
1280	4	17	2017-08-04 11:57:23.0036	t	t
1281	4	36	2017-07-30 11:57:23.003628	t	t
1282	4	19	2017-08-03 11:57:23.003657	t	t
1283	4	37	2017-08-12 11:57:23.003686	t	t
1284	4	31	2017-07-25 11:57:23.003714	t	t
1285	4	13	2017-08-03 11:57:23.003742	t	t
1286	4	23	2017-08-12 11:57:23.00377	t	t
1287	4	29	2017-08-05 11:57:23.003799	f	t
1288	4	8	2017-08-05 11:57:23.003828	f	t
1289	4	29	2017-08-07 11:57:23.003864	f	t
1290	4	35	2017-07-29 11:57:23.003912	f	t
1291	4	27	2017-08-10 11:57:23.003961	f	t
1292	4	37	2017-07-28 11:57:23.004003	f	t
1293	4	33	2017-07-23 11:57:23.004034	f	t
1294	4	35	2017-08-10 11:57:23.004064	f	t
1295	4	37	2017-07-29 11:57:23.004093	f	t
1296	4	9	2017-08-10 11:57:23.004122	f	t
1297	4	25	2017-08-05 11:57:23.004151	f	t
1298	4	22	2017-08-06 11:57:23.004181	f	t
1299	4	13	2017-07-29 11:57:23.004209	f	t
1300	4	27	2017-08-13 11:57:23.004239	f	t
1301	4	34	2017-08-11 11:57:23.004268	f	t
1302	4	23	2017-07-31 11:57:23.004298	f	t
1303	4	32	2017-08-10 11:57:23.004327	f	t
1304	4	7	2017-07-24 11:57:23.004355	f	t
1305	4	29	2017-07-26 11:57:23.004384	f	t
1306	4	33	2017-08-12 11:57:23.004413	f	t
1307	4	27	2017-08-13 11:57:23.004442	f	t
1308	4	35	2017-08-04 11:57:23.00447	f	t
1309	4	20	2017-07-27 11:57:23.004499	f	t
1310	5	20	2017-07-24 11:57:23.004527	t	t
1311	5	27	2017-08-15 11:57:23.004556	t	t
1312	5	34	2017-07-29 11:57:23.004585	t	t
1313	5	37	2017-08-05 11:57:23.004614	t	t
1314	5	11	2017-08-07 11:57:23.004642	f	t
1315	5	13	2017-07-23 11:57:23.004671	f	t
1316	6	24	2017-08-01 11:57:23.004699	t	t
1317	6	24	2017-07-23 11:57:23.004728	t	t
1318	6	20	2017-07-26 11:57:23.004768	t	t
1319	6	28	2017-08-10 11:57:23.004808	t	t
1320	6	12	2017-07-29 11:57:23.004849	t	t
1321	6	29	2017-08-02 11:57:23.004879	t	t
1322	6	32	2017-08-16 11:57:23.004907	t	t
1323	6	27	2017-08-08 11:57:23.004937	t	t
1324	6	16	2017-08-13 11:57:23.004966	t	t
1325	6	31	2017-07-27 11:57:23.004994	t	t
1326	6	32	2017-08-02 11:57:23.005023	t	t
1327	6	29	2017-08-02 11:57:23.005052	t	t
1328	6	7	2017-08-07 11:57:23.005081	t	t
1329	6	17	2017-07-31 11:57:23.00511	t	t
1330	6	36	2017-07-25 11:57:23.005139	t	t
1331	6	36	2017-08-15 11:57:23.005168	t	t
1332	6	20	2017-08-11 11:57:23.005197	t	t
1333	6	29	2017-07-28 11:57:23.005226	t	t
1334	6	17	2017-07-30 11:57:23.005254	t	t
1335	6	29	2017-08-09 11:57:23.005283	t	t
1336	6	21	2017-08-17 11:57:23.005311	t	t
1337	6	36	2017-08-13 11:57:23.00534	t	t
1338	6	21	2017-08-13 11:57:23.005368	f	t
1339	6	36	2017-08-17 11:57:23.005407	f	t
1340	6	17	2017-08-02 11:57:23.005437	f	t
1341	6	9	2017-07-23 11:57:23.005467	f	t
1342	6	28	2017-08-03 11:57:23.005509	f	t
1343	7	29	2017-08-16 11:57:23.00554	t	t
1344	7	21	2017-07-24 11:57:23.00557	t	t
1345	7	9	2017-07-24 11:57:23.00561	t	t
1346	7	29	2017-08-09 11:57:23.005655	f	t
1347	7	19	2017-07-31 11:57:23.005709	f	t
1348	8	9	2017-08-01 11:57:23.005744	f	t
1349	8	11	2017-08-03 11:57:23.005775	f	t
1350	8	27	2017-08-15 11:57:23.005805	f	t
1351	8	11	2017-08-03 11:57:23.005836	f	t
1352	9	14	2017-07-26 11:57:23.005874	t	t
1353	9	25	2017-08-03 11:57:23.005914	t	t
1354	9	14	2017-07-25 11:57:23.005942	t	t
1355	9	17	2017-08-15 11:57:23.005971	t	t
1356	9	13	2017-08-06 11:57:23.006	t	t
1357	9	7	2017-07-29 11:57:23.006029	t	t
1358	9	19	2017-08-07 11:57:23.006057	t	t
1359	9	9	2017-08-02 11:57:23.006086	t	t
1360	9	24	2017-07-31 11:57:23.006116	t	t
1361	9	18	2017-08-17 11:57:23.006145	t	t
1362	9	11	2017-08-13 11:57:23.006174	t	t
1363	9	27	2017-08-07 11:57:23.006202	t	t
1364	9	23	2017-08-12 11:57:23.006232	t	t
1365	9	7	2017-07-31 11:57:23.006261	t	t
1366	9	31	2017-08-17 11:57:23.006289	t	t
1367	9	23	2017-08-06 11:57:23.006318	t	t
1368	9	34	2017-07-29 11:57:23.006347	t	t
1369	9	29	2017-08-08 11:57:23.006375	t	t
1370	9	24	2017-08-11 11:57:23.006404	t	t
1371	9	18	2017-08-11 11:57:23.006433	t	t
1372	9	32	2017-07-28 11:57:23.006462	t	t
1373	9	33	2017-07-28 11:57:23.00649	t	t
1374	9	29	2017-08-01 11:57:23.00652	t	t
1375	9	24	2017-08-07 11:57:23.006549	t	t
1376	9	17	2017-08-05 11:57:23.006578	f	t
1377	9	10	2017-08-13 11:57:23.006607	f	t
1378	9	25	2017-07-25 11:57:23.006635	f	t
1379	9	14	2017-07-30 11:57:23.006664	f	t
1380	9	12	2017-08-13 11:57:23.006693	f	t
1381	9	19	2017-07-30 11:57:23.006721	f	t
1382	9	29	2017-07-30 11:57:23.006749	f	t
1383	10	25	2017-08-17 11:57:23.006778	t	t
1384	10	17	2017-08-16 11:57:23.006807	t	t
1385	10	24	2017-08-17 11:57:23.006835	t	t
1386	10	7	2017-07-25 11:57:23.006863	f	t
1387	10	16	2017-08-01 11:57:23.006892	f	t
1388	11	21	2017-07-25 11:57:23.00692	t	t
1389	11	27	2017-08-07 11:57:23.006949	t	t
1390	11	31	2017-07-31 11:57:23.006977	t	t
1391	11	27	2017-08-08 11:57:23.007006	t	t
1392	11	17	2017-08-15 11:57:23.007034	t	t
1393	11	9	2017-08-15 11:57:23.007063	t	t
1394	11	26	2017-08-16 11:57:23.007092	t	t
1395	11	18	2017-08-01 11:57:23.007122	t	t
1396	11	8	2017-07-31 11:57:23.00715	t	t
1397	11	25	2017-08-04 11:57:23.007178	t	t
1398	11	9	2017-08-08 11:57:23.007207	t	t
1399	11	26	2017-08-09 11:57:23.007235	t	t
1400	11	13	2017-07-29 11:57:23.007264	t	t
1401	11	34	2017-07-23 11:57:23.007292	f	t
1402	11	14	2017-07-25 11:57:23.007321	f	t
1403	11	26	2017-08-01 11:57:23.007349	f	t
1404	11	13	2017-08-05 11:57:23.007379	f	t
1405	11	25	2017-07-26 11:57:23.007407	f	t
1406	11	7	2017-08-04 11:57:23.007435	f	t
1407	11	16	2017-08-05 11:57:23.007464	f	t
1408	11	9	2017-08-04 11:57:23.007493	f	t
1409	11	29	2017-07-25 11:57:23.007522	f	t
1410	11	20	2017-07-26 11:57:23.00755	f	t
1411	11	13	2017-08-05 11:57:23.00758	f	t
1412	11	35	2017-08-09 11:57:23.007608	f	t
1413	11	31	2017-08-03 11:57:23.007637	f	t
1414	11	7	2017-07-25 11:57:23.007666	f	t
1415	12	22	2017-07-27 11:57:23.007694	f	t
1416	12	24	2017-08-16 11:57:23.007722	f	t
1417	12	23	2017-08-09 11:57:23.007751	f	t
1418	12	35	2017-08-04 11:57:23.007779	f	t
1419	12	32	2017-08-16 11:57:23.007808	f	t
1420	12	31	2017-07-26 11:57:23.007837	f	t
1421	12	29	2017-07-31 11:57:23.007866	f	t
1422	12	34	2017-07-23 11:57:23.007895	f	t
1423	12	16	2017-07-27 11:57:23.007924	f	t
1424	14	25	2017-07-23 11:57:23.007952	t	t
1425	14	15	2017-08-12 11:57:23.007981	t	t
1426	14	26	2017-07-23 11:57:23.008009	t	t
1427	14	9	2017-08-01 11:57:23.008038	t	t
1428	14	10	2017-08-17 11:57:23.008066	t	t
1429	14	37	2017-08-09 11:57:23.008095	t	t
1430	14	33	2017-07-23 11:57:23.008123	t	t
1431	14	10	2017-08-01 11:57:23.008152	t	t
1432	14	9	2017-07-26 11:57:23.008181	t	t
1433	14	19	2017-07-31 11:57:23.008209	t	t
1434	14	15	2017-08-09 11:57:23.008238	f	t
1435	14	26	2017-07-27 11:57:23.008266	f	t
1436	14	34	2017-08-09 11:57:23.008294	f	t
1437	14	22	2017-08-01 11:57:23.008322	f	t
1438	14	20	2017-08-04 11:57:23.008351	f	t
1439	14	19	2017-07-23 11:57:23.008379	f	t
1440	14	11	2017-07-23 11:57:23.008408	f	t
1441	14	25	2017-08-09 11:57:23.008436	f	t
1442	14	25	2017-07-26 11:57:23.008465	f	t
1443	14	18	2017-08-13 11:57:23.008494	f	t
1444	14	28	2017-08-07 11:57:23.008523	f	t
1445	14	10	2017-07-28 11:57:23.008551	f	t
1446	14	11	2017-08-08 11:57:23.00858	f	t
1447	14	36	2017-08-17 11:57:23.008609	f	t
1448	15	28	2017-08-17 11:57:23.008637	t	t
1449	15	31	2017-07-23 11:57:23.008665	t	t
1450	15	34	2017-08-01 11:57:23.008694	t	t
1451	15	34	2017-07-30 11:57:23.008722	t	t
1452	15	26	2017-08-08 11:57:23.00875	t	t
1453	15	19	2017-08-13 11:57:23.008779	t	t
1454	15	28	2017-08-07 11:57:23.008808	t	t
1455	15	19	2017-07-31 11:57:23.008836	t	t
1456	15	13	2017-07-30 11:57:23.008865	t	t
1457	15	14	2017-08-15 11:57:23.008893	t	t
1458	15	37	2017-08-15 11:57:23.008922	t	t
1459	15	28	2017-07-30 11:57:23.008951	f	t
1460	15	14	2017-08-02 11:57:23.00898	f	t
1461	15	29	2017-07-31 11:57:23.009008	f	t
1462	15	37	2017-08-06 11:57:23.009037	f	t
1463	15	27	2017-08-03 11:57:23.009066	f	t
1464	16	15	2017-08-05 11:57:23.009094	t	t
1465	16	9	2017-08-03 11:57:23.009122	t	t
1466	16	15	2017-07-28 11:57:23.009151	t	t
1467	16	29	2017-08-12 11:57:23.00918	t	t
1468	16	33	2017-07-25 11:57:23.009208	t	t
1469	16	16	2017-08-04 11:57:23.009247	t	t
1470	16	10	2017-07-30 11:57:23.009277	t	t
1471	16	27	2017-08-02 11:57:23.009327	t	t
1472	16	37	2017-07-23 11:57:23.009367	t	t
1473	16	28	2017-07-27 11:57:23.009484	t	t
1474	16	18	2017-08-06 11:57:23.009529	f	t
1475	16	11	2017-08-14 11:57:23.009582	f	t
1476	16	13	2017-08-15 11:57:23.009613	f	t
1477	16	19	2017-08-09 11:57:23.009643	f	t
1478	16	27	2017-07-27 11:57:23.009674	f	t
1479	16	14	2017-08-10 11:57:23.009704	f	t
1480	16	22	2017-08-13 11:57:23.009733	f	t
1481	16	24	2017-08-09 11:57:23.009764	f	t
1482	16	24	2017-08-12 11:57:23.009795	f	t
1483	17	13	2017-08-12 11:57:23.009825	t	t
1484	17	12	2017-07-30 11:57:23.009871	t	t
1485	17	37	2017-07-25 11:57:23.009904	f	t
1486	18	31	2017-07-27 11:57:23.009945	t	t
1487	18	27	2017-08-11 11:57:23.009975	t	t
1488	18	18	2017-08-07 11:57:23.010005	f	t
1489	19	21	2017-08-05 11:57:23.010034	t	t
1490	19	26	2017-08-04 11:57:23.010065	t	t
1491	19	34	2017-07-23 11:57:23.010094	t	t
1492	19	29	2017-08-02 11:57:23.010124	t	t
1493	19	25	2017-08-11 11:57:23.010154	t	t
1494	19	8	2017-07-23 11:57:23.010183	t	t
1495	19	15	2017-07-30 11:57:23.010213	t	t
1496	19	14	2017-08-08 11:57:23.010244	t	t
1497	19	24	2017-07-30 11:57:23.010274	f	t
1498	19	28	2017-08-05 11:57:23.010304	f	t
1499	19	34	2017-08-10 11:57:23.010346	f	t
1500	19	27	2017-08-15 11:57:23.010376	f	t
1501	19	22	2017-08-16 11:57:23.010417	f	t
1502	19	17	2017-07-26 11:57:23.010446	f	t
1503	19	36	2017-07-26 11:57:23.010476	f	t
1504	19	33	2017-07-26 11:57:23.010507	f	t
1505	19	29	2017-07-27 11:57:23.010537	f	t
1506	20	11	2017-07-30 11:57:23.010568	t	t
1507	20	29	2017-07-30 11:57:23.010597	t	t
1508	20	34	2017-07-24 11:57:23.010627	t	t
1509	20	31	2017-08-01 11:57:23.010657	t	t
1510	20	32	2017-07-23 11:57:23.010687	f	t
1511	20	28	2017-07-26 11:57:23.010717	f	t
1512	20	18	2017-07-28 11:57:23.010746	f	t
1513	20	16	2017-08-07 11:57:23.010776	f	t
1514	21	18	2017-08-11 11:57:23.010806	t	t
1515	21	9	2017-07-26 11:57:23.010846	t	t
1516	21	21	2017-08-02 11:57:23.010885	t	t
1517	22	25	2017-08-01 11:57:23.010926	t	t
1518	22	23	2017-08-12 11:57:23.010956	t	t
1519	22	16	2017-08-17 11:57:23.010996	t	t
1520	22	16	2017-08-05 11:57:23.011026	t	t
1521	22	27	2017-07-31 11:57:23.011068	t	t
1522	22	24	2017-08-03 11:57:23.011124	t	t
1523	22	23	2017-07-27 11:57:23.011165	t	t
1524	22	22	2017-08-11 11:57:23.011216	t	t
1525	22	25	2017-08-14 11:57:23.011246	t	t
1526	22	33	2017-08-15 11:57:23.011276	t	t
1527	22	19	2017-08-17 11:57:23.011306	t	t
1528	22	11	2017-08-07 11:57:23.011336	f	t
1529	22	12	2017-08-11 11:57:23.011375	f	t
1530	22	32	2017-08-11 11:57:23.011406	f	t
1531	22	23	2017-07-25 11:57:23.011437	f	t
1532	22	13	2017-08-09 11:57:23.011469	f	t
1533	23	12	2017-08-06 11:57:23.0115	t	t
1534	23	26	2017-07-28 11:57:23.011538	t	t
1535	23	7	2017-08-01 11:57:23.011594	t	t
1536	23	17	2017-07-27 11:57:23.011653	t	t
1537	23	37	2017-07-24 11:57:23.011708	t	t
1538	23	12	2017-08-06 11:57:23.011761	t	t
1539	23	27	2017-08-10 11:57:23.011818	t	t
1540	23	34	2017-07-24 11:57:23.011882	t	t
1541	23	28	2017-08-12 11:57:23.011951	t	t
1542	23	33	2017-08-07 11:57:23.012009	t	t
1543	23	10	2017-07-31 11:57:23.012068	t	t
1544	23	35	2017-08-14 11:57:23.012125	t	t
1545	23	10	2017-08-11 11:57:23.012197	t	t
1546	23	23	2017-08-09 11:57:23.012254	t	t
1547	23	29	2017-08-14 11:57:23.012294	t	t
1548	23	27	2017-08-03 11:57:23.012354	t	t
1549	23	7	2017-07-31 11:57:23.012411	t	t
1550	23	8	2017-08-17 11:57:23.012463	t	t
1551	23	9	2017-08-05 11:57:23.012512	f	t
1552	23	34	2017-07-24 11:57:23.012545	f	t
1553	23	11	2017-07-24 11:57:23.012576	f	t
1554	23	20	2017-08-16 11:57:23.012607	f	t
1555	23	16	2017-08-03 11:57:23.012638	f	t
1556	23	15	2017-08-12 11:57:23.012668	f	t
1557	23	23	2017-07-27 11:57:23.012698	f	t
1558	24	29	2017-08-04 11:57:23.012729	t	t
1559	24	29	2017-08-16 11:57:23.012759	t	t
1560	24	34	2017-07-30 11:57:23.01279	t	t
1561	24	20	2017-08-02 11:57:23.01282	t	t
1562	24	36	2017-08-04 11:57:23.01285	t	t
1563	24	17	2017-07-27 11:57:23.012881	t	t
1564	24	14	2017-07-23 11:57:23.012913	t	t
1565	24	8	2017-07-30 11:57:23.012943	t	t
1566	24	31	2017-08-10 11:57:23.012974	t	t
1567	24	12	2017-07-30 11:57:23.013003	t	t
1568	24	22	2017-07-23 11:57:23.013034	t	t
1569	24	27	2017-08-06 11:57:23.013064	t	t
1570	24	12	2017-08-14 11:57:23.013094	t	t
1571	24	7	2017-08-04 11:57:23.013124	t	t
1572	24	36	2017-08-07 11:57:23.013154	t	t
1573	24	28	2017-08-04 11:57:23.013184	t	t
1574	24	23	2017-08-07 11:57:23.013214	t	t
1575	24	25	2017-07-26 11:57:23.013245	t	t
1576	24	29	2017-08-10 11:57:23.013275	t	t
1577	24	31	2017-08-01 11:57:23.013305	f	t
1578	24	28	2017-07-25 11:57:23.013335	f	t
1579	24	32	2017-08-08 11:57:23.013365	f	t
1580	24	23	2017-08-02 11:57:23.013394	f	t
1581	24	36	2017-08-01 11:57:23.013424	f	t
1582	24	25	2017-08-11 11:57:23.013454	f	t
1583	24	34	2017-08-05 11:57:23.013484	f	t
1584	24	29	2017-07-30 11:57:23.013514	f	t
1585	24	36	2017-08-09 11:57:23.01355	f	t
1586	24	24	2017-07-25 11:57:23.013604	f	t
1587	25	35	2017-08-16 11:57:23.013654	t	t
1588	25	19	2017-07-27 11:57:23.013703	t	t
1589	25	20	2017-08-17 11:57:23.013751	t	t
1590	25	23	2017-07-24 11:57:23.013804	t	t
1591	25	31	2017-07-27 11:57:23.013885	t	t
1592	25	21	2017-07-26 11:57:23.013953	f	t
1593	25	23	2017-08-01 11:57:23.014026	f	t
1594	25	27	2017-07-29 11:57:23.014108	f	t
1595	25	19	2017-08-14 11:57:23.014171	f	t
1596	25	28	2017-08-05 11:57:23.014225	f	t
1597	26	16	2017-08-17 11:57:23.014278	t	t
1598	26	29	2017-07-24 11:57:23.01433	t	t
1599	26	25	2017-08-11 11:57:23.014382	f	t
1600	26	24	2017-07-24 11:57:23.014438	f	t
1601	26	35	2017-07-30 11:57:23.014501	f	t
1602	26	7	2017-08-07 11:57:23.014551	f	t
1603	26	25	2017-08-06 11:57:23.014604	f	t
1604	26	32	2017-08-15 11:57:23.014654	f	t
1605	27	31	2017-08-02 11:57:23.014705	t	t
1606	27	37	2017-08-02 11:57:23.014758	t	t
1607	27	13	2017-07-24 11:57:23.01481	f	t
1608	27	18	2017-08-17 11:57:23.01486	f	t
1609	27	10	2017-08-05 11:57:23.014913	f	t
1610	27	36	2017-08-05 11:57:23.014966	f	t
1611	27	23	2017-07-29 11:57:23.015022	f	t
1612	27	16	2017-08-10 11:57:23.015074	f	t
1613	27	34	2017-08-16 11:57:23.015134	f	t
1614	27	31	2017-07-25 11:57:23.015197	f	t
1615	27	28	2017-07-23 11:57:23.01526	f	t
1616	27	13	2017-08-10 11:57:23.015324	f	t
1617	27	10	2017-07-23 11:57:23.015398	f	t
1618	28	10	2017-07-24 11:57:23.015461	f	t
1619	29	25	2017-07-23 11:57:23.015521	t	t
1620	29	23	2017-07-30 11:57:23.015576	t	t
1621	29	18	2017-07-25 11:57:23.015632	t	t
1622	29	27	2017-07-24 11:57:23.015701	t	t
1623	29	23	2017-07-31 11:57:23.015776	t	t
1624	29	31	2017-07-29 11:57:23.015834	t	t
1625	29	37	2017-07-31 11:57:23.0159	t	t
1626	29	33	2017-07-29 11:57:23.015959	t	t
1627	29	32	2017-08-05 11:57:23.016019	t	t
1628	29	20	2017-08-16 11:57:23.016079	t	t
1629	29	33	2017-08-06 11:57:23.01614	t	t
1630	29	29	2017-08-09 11:57:23.016205	t	t
1631	29	29	2017-08-12 11:57:23.01627	f	t
1632	29	8	2017-08-01 11:57:23.016338	f	t
1633	29	27	2017-07-30 11:57:23.016405	f	t
1634	29	7	2017-08-06 11:57:23.016466	f	t
1635	29	14	2017-07-31 11:57:23.016538	f	t
1636	29	14	2017-08-06 11:57:23.016603	f	t
1637	29	8	2017-08-12 11:57:23.016669	f	t
1638	29	34	2017-08-07 11:57:23.016731	f	t
1639	30	32	2017-08-15 11:57:23.016794	t	t
1640	30	19	2017-08-15 11:57:23.016859	t	t
1641	30	23	2017-07-23 11:57:23.016924	t	t
1642	30	7	2017-08-16 11:57:23.01699	t	t
1643	30	25	2017-07-31 11:57:23.017054	t	t
1644	30	16	2017-08-06 11:57:23.017118	t	t
1645	30	8	2017-07-30 11:57:23.01719	t	t
1646	30	9	2017-07-30 11:57:23.017258	t	t
1647	30	19	2017-08-06 11:57:23.01732	t	t
1648	30	9	2017-08-07 11:57:23.017386	t	t
1649	30	20	2017-07-29 11:57:23.017439	t	t
1650	30	31	2017-07-26 11:57:23.017513	t	t
1651	30	35	2017-07-28 11:57:23.017573	t	t
1652	30	37	2017-08-08 11:57:23.017613	t	t
1653	30	16	2017-08-06 11:57:23.017648	t	t
1654	30	10	2017-08-17 11:57:23.017682	t	t
1655	30	25	2017-07-31 11:57:23.017714	t	t
1656	30	10	2017-07-24 11:57:23.017747	t	t
1657	30	16	2017-07-24 11:57:23.017778	f	t
1658	30	35	2017-07-27 11:57:23.01781	f	t
1659	30	9	2017-07-23 11:57:23.017842	f	t
1660	30	29	2017-08-04 11:57:23.017889	f	t
1661	30	17	2017-08-15 11:57:23.017921	f	t
1662	30	14	2017-07-23 11:57:23.017965	f	t
1663	30	29	2017-07-30 11:57:23.018	f	t
1664	30	36	2017-08-14 11:57:23.018034	f	t
1665	30	18	2017-08-17 11:57:23.018067	f	t
1666	30	22	2017-08-17 11:57:23.018099	f	t
1667	30	20	2017-07-30 11:57:23.018131	f	t
1668	30	20	2017-08-08 11:57:23.018161	f	t
1669	30	36	2017-07-28 11:57:23.018192	f	t
1670	30	12	2017-08-06 11:57:23.018223	f	t
1671	30	16	2017-08-15 11:57:23.018255	f	t
1672	31	17	2017-08-06 11:57:23.018285	t	t
1673	31	10	2017-07-25 11:57:23.018316	t	t
1674	31	25	2017-08-03 11:57:23.018349	t	t
1675	31	9	2017-07-27 11:57:23.018381	t	t
1676	31	31	2017-07-31 11:57:23.018411	t	t
1677	31	29	2017-08-08 11:57:23.018443	t	t
1678	31	28	2017-08-14 11:57:23.018474	t	t
1679	31	29	2017-08-02 11:57:23.018505	t	t
1680	31	10	2017-08-06 11:57:23.018536	t	t
1681	31	26	2017-08-15 11:57:23.018566	t	t
1682	31	26	2017-08-05 11:57:23.018611	t	t
1683	31	14	2017-08-07 11:57:23.018666	t	t
1684	31	8	2017-07-25 11:57:23.018697	f	t
1685	31	33	2017-08-09 11:57:23.018728	f	t
1686	31	31	2017-07-27 11:57:23.018758	f	t
1687	31	32	2017-07-27 11:57:23.018789	f	t
1688	31	12	2017-08-06 11:57:23.01882	f	t
1689	31	29	2017-08-09 11:57:23.018851	f	t
1690	31	33	2017-07-25 11:57:23.018881	f	t
1691	31	14	2017-08-06 11:57:23.018911	f	t
1692	31	7	2017-08-02 11:57:23.018941	f	t
1693	31	14	2017-08-16 11:57:23.018971	f	t
1694	31	23	2017-07-23 11:57:23.019002	f	t
1695	31	26	2017-07-23 11:57:23.019032	f	t
1696	31	16	2017-07-31 11:57:23.019062	f	t
1697	31	7	2017-08-03 11:57:23.019092	f	t
1698	31	19	2017-08-01 11:57:23.019122	f	t
1699	31	8	2017-07-25 11:57:23.019152	f	t
1700	31	26	2017-08-08 11:57:23.019182	f	t
1701	32	35	2017-08-11 11:57:23.019212	f	t
1702	32	27	2017-08-09 11:57:23.019244	f	t
1703	32	8	2017-07-30 11:57:23.019274	f	t
1704	32	11	2017-07-31 11:57:23.019304	f	t
1705	32	36	2017-07-28 11:57:23.019335	f	t
1706	32	14	2017-08-14 11:57:23.019386	f	t
1707	32	33	2017-08-01 11:57:23.019418	f	t
1708	32	18	2017-08-15 11:57:23.01945	f	t
1709	32	9	2017-07-23 11:57:23.01948	f	t
1710	32	15	2017-08-05 11:57:23.019511	f	t
1711	32	13	2017-08-02 11:57:23.019541	f	t
1712	32	27	2017-07-28 11:57:23.019572	f	t
1713	33	37	2017-08-12 11:57:23.019602	t	t
1714	33	20	2017-07-24 11:57:23.019633	t	t
1715	33	25	2017-08-05 11:57:23.019663	t	t
1716	33	35	2017-08-10 11:57:23.019693	t	t
1717	33	15	2017-08-05 11:57:23.019723	t	t
1718	33	8	2017-08-14 11:57:23.019754	t	t
1719	33	13	2017-08-05 11:57:23.019786	t	t
1720	33	25	2017-08-09 11:57:23.019816	t	t
1721	33	13	2017-07-28 11:57:23.019847	t	t
1722	33	17	2017-08-14 11:57:23.019877	t	t
1723	33	10	2017-08-12 11:57:23.019908	t	t
1724	33	13	2017-08-07 11:57:23.019937	t	t
1725	33	37	2017-08-06 11:57:23.019968	t	t
1726	33	12	2017-07-31 11:57:23.019998	t	t
1727	33	22	2017-07-25 11:57:23.020029	t	t
1728	33	35	2017-07-23 11:57:23.020059	t	t
1729	33	8	2017-08-15 11:57:23.020089	t	t
1730	33	36	2017-07-23 11:57:23.020119	t	t
1731	33	22	2017-07-25 11:57:23.02015	f	t
1732	33	32	2017-07-28 11:57:23.02018	f	t
1733	33	34	2017-08-10 11:57:23.02021	f	t
1734	33	34	2017-07-25 11:57:23.020239	f	t
1735	33	9	2017-08-13 11:57:23.02027	f	t
1736	34	33	2017-08-09 11:57:23.0203	t	t
1737	34	29	2017-07-23 11:57:23.02033	t	t
1738	34	33	2017-08-17 11:57:23.02036	f	t
1739	34	8	2017-07-25 11:57:23.020391	f	t
1740	34	20	2017-08-10 11:57:23.020421	f	t
1741	34	24	2017-07-24 11:57:23.02045	f	t
1742	34	34	2017-08-06 11:57:23.020481	f	t
1743	34	32	2017-08-15 11:57:23.020519	f	t
1744	35	24	2017-08-12 11:57:23.02057	t	t
1745	35	36	2017-07-23 11:57:23.02062	t	t
1746	35	10	2017-07-30 11:57:23.020669	t	t
1747	35	19	2017-08-13 11:57:23.02072	t	t
1748	35	31	2017-07-27 11:57:23.020771	f	t
1749	35	10	2017-07-25 11:57:23.020821	f	t
1750	35	15	2017-08-08 11:57:23.020872	f	t
1751	35	18	2017-07-30 11:57:23.020923	f	t
1752	35	14	2017-08-11 11:57:23.020972	f	t
1753	35	28	2017-08-13 11:57:23.021022	f	t
1754	35	27	2017-08-09 11:57:23.021071	f	t
1755	36	11	2017-08-17 11:57:23.021122	t	t
1756	36	21	2017-07-27 11:57:23.021173	t	t
1757	36	18	2017-08-11 11:57:23.021225	t	t
1758	36	36	2017-07-23 11:57:23.021276	t	t
1759	37	26	2017-08-09 11:57:23.021327	t	t
1760	37	7	2017-08-12 11:57:23.021379	t	t
1761	37	10	2017-07-31 11:57:23.02143	t	t
1762	37	31	2017-08-01 11:57:23.02148	t	t
1763	37	32	2017-07-25 11:57:23.021532	t	t
1764	37	21	2017-08-05 11:57:23.021582	t	t
1765	37	10	2017-08-06 11:57:23.02162	t	t
1766	37	20	2017-07-27 11:57:23.021651	t	t
1767	37	11	2017-08-17 11:57:23.021682	t	t
1768	37	35	2017-08-01 11:57:23.021722	t	t
1769	37	27	2017-08-02 11:57:23.021752	t	t
1770	37	20	2017-07-28 11:57:23.021781	t	t
1771	37	26	2017-07-24 11:57:23.021811	t	t
1772	37	22	2017-08-05 11:57:23.021841	t	t
1773	37	29	2017-08-13 11:57:23.02189	f	t
1774	37	14	2017-07-25 11:57:23.02193	f	t
1775	37	31	2017-07-28 11:57:23.02196	f	t
1776	38	33	2017-08-16 11:57:23.021989	t	t
1777	38	13	2017-08-14 11:57:23.022019	f	t
1778	39	17	2017-08-13 11:57:23.022049	t	t
1779	39	19	2017-08-13 11:57:23.022088	f	t
1780	40	35	2017-07-26 11:57:23.022128	t	t
1781	40	23	2017-08-16 11:57:23.022157	t	t
1782	40	22	2017-07-25 11:57:23.022187	t	t
1783	40	34	2017-07-26 11:57:23.022216	t	t
1784	40	9	2017-08-07 11:57:23.022246	t	t
1785	40	28	2017-08-09 11:57:23.022274	t	t
1786	40	19	2017-08-06 11:57:23.022303	t	t
1787	40	34	2017-08-07 11:57:23.022332	t	t
1788	40	27	2017-07-24 11:57:23.02236	t	t
1789	40	16	2017-07-28 11:57:23.022405	t	t
1790	40	18	2017-08-13 11:57:23.022459	t	t
1791	40	28	2017-08-08 11:57:23.022512	t	t
1792	40	11	2017-07-23 11:57:23.022547	t	t
1793	40	9	2017-08-16 11:57:23.02258	t	t
1794	40	32	2017-08-08 11:57:23.022612	f	t
1795	40	26	2017-08-13 11:57:23.022644	f	t
1796	40	23	2017-08-17 11:57:23.022676	f	t
1797	40	11	2017-08-06 11:57:23.022707	f	t
1798	40	12	2017-08-08 11:57:23.022738	f	t
1799	41	13	2017-08-04 11:57:23.022769	t	t
1800	41	18	2017-07-27 11:57:23.0228	t	t
1801	41	15	2017-08-13 11:57:23.022831	t	t
1802	41	21	2017-08-15 11:57:23.022862	t	t
1803	41	12	2017-07-25 11:57:23.022893	t	t
1804	41	21	2017-08-11 11:57:23.022925	t	t
1805	41	10	2017-08-10 11:57:23.022956	t	t
1806	41	23	2017-08-17 11:57:23.022987	f	t
1807	41	37	2017-08-01 11:57:23.023019	f	t
1808	41	10	2017-07-23 11:57:23.02305	f	t
1809	41	13	2017-08-05 11:57:23.023081	f	t
1810	41	32	2017-08-02 11:57:23.023112	f	t
1811	41	19	2017-07-29 11:57:23.023144	f	t
1812	41	16	2017-08-11 11:57:23.023174	f	t
1813	42	13	2017-07-27 11:57:23.023205	f	t
1814	43	13	2017-08-10 11:57:23.023236	t	t
1815	43	37	2017-07-26 11:57:23.023267	t	t
1816	43	27	2017-08-01 11:57:23.023298	t	t
1817	43	15	2017-07-24 11:57:23.023328	t	t
1818	43	33	2017-08-02 11:57:23.023359	t	t
1819	43	10	2017-08-01 11:57:23.02339	t	t
1820	43	29	2017-07-31 11:57:23.02342	t	t
1821	43	29	2017-07-30 11:57:23.023451	t	t
1822	43	26	2017-07-23 11:57:23.023483	t	t
1823	43	9	2017-08-16 11:57:23.023514	t	t
1824	43	37	2017-08-02 11:57:23.023546	t	t
1825	43	14	2017-08-10 11:57:23.023577	t	t
1826	43	7	2017-07-24 11:57:23.023608	f	t
1827	43	17	2017-08-14 11:57:23.02365	f	t
1828	43	36	2017-07-30 11:57:23.023686	f	t
1829	43	33	2017-07-28 11:57:23.023717	f	t
1830	43	23	2017-07-23 11:57:23.023748	f	t
1831	43	21	2017-08-13 11:57:23.02378	f	t
1832	43	8	2017-08-03 11:57:23.023811	f	t
1833	43	37	2017-08-15 11:57:23.023842	f	t
1834	43	17	2017-07-27 11:57:23.023874	f	t
1835	43	15	2017-08-05 11:57:23.023905	f	t
1836	43	27	2017-08-07 11:57:23.023936	f	t
1837	44	23	2017-07-23 11:57:23.023967	t	t
1838	44	37	2017-07-30 11:57:23.023998	f	t
1839	44	16	2017-07-30 11:57:23.02403	f	t
1840	44	34	2017-07-31 11:57:23.024061	f	t
1841	44	29	2017-08-08 11:57:23.024092	f	t
1842	44	31	2017-08-05 11:57:23.024124	f	t
1843	44	28	2017-07-24 11:57:23.024156	f	t
1844	45	16	2017-07-24 11:57:23.024187	t	t
1845	45	23	2017-08-16 11:57:23.024218	t	t
1846	45	34	2017-07-29 11:57:23.024249	t	t
1847	45	27	2017-08-10 11:57:23.02428	t	t
1848	45	21	2017-08-14 11:57:23.024311	t	t
1849	45	37	2017-07-25 11:57:23.024343	t	t
1850	45	25	2017-08-16 11:57:23.024374	t	t
1851	45	26	2017-08-06 11:57:23.024405	t	t
1852	45	12	2017-08-17 11:57:23.024437	t	t
1853	45	19	2017-07-24 11:57:23.024468	t	t
1854	45	37	2017-08-16 11:57:23.024499	t	t
1855	46	11	2017-07-28 11:57:23.02453	t	t
1856	46	16	2017-08-09 11:57:23.024562	t	t
1857	46	24	2017-08-05 11:57:23.024593	t	t
1858	46	32	2017-08-15 11:57:23.024625	t	t
1859	46	24	2017-07-31 11:57:23.024656	t	t
1860	46	37	2017-07-27 11:57:23.024687	t	t
1861	46	32	2017-08-06 11:57:23.024718	t	t
1862	46	26	2017-08-11 11:57:23.024749	t	t
1863	46	29	2017-07-30 11:57:23.024781	t	t
1864	46	35	2017-08-13 11:57:23.024813	t	t
1865	46	15	2017-07-30 11:57:23.024844	t	t
1866	46	14	2017-07-29 11:57:23.024875	t	t
1867	46	29	2017-08-03 11:57:23.024906	t	t
1868	46	7	2017-08-02 11:57:23.024937	t	t
1869	46	36	2017-08-06 11:57:23.024968	t	t
1870	46	27	2017-07-30 11:57:23.024999	t	t
1871	46	24	2017-07-23 11:57:23.02503	t	t
1872	46	25	2017-07-23 11:57:23.025061	t	t
1873	46	15	2017-07-27 11:57:23.025092	f	t
1874	46	12	2017-07-31 11:57:23.025123	f	t
1875	46	25	2017-08-07 11:57:23.025153	f	t
1876	46	24	2017-07-23 11:57:23.025184	f	t
1877	46	24	2017-08-05 11:57:23.025214	f	t
1878	46	35	2017-07-25 11:57:23.025246	f	t
1879	46	15	2017-07-29 11:57:23.025277	f	t
1880	46	27	2017-07-31 11:57:23.025308	f	t
1881	46	34	2017-08-17 11:57:23.025339	f	t
1882	46	35	2017-07-30 11:57:23.02537	f	t
1883	46	20	2017-08-16 11:57:23.02541	f	t
1884	47	31	2017-08-10 11:57:23.025439	t	t
1885	47	28	2017-08-03 11:57:23.025468	t	t
1886	47	33	2017-07-27 11:57:23.025497	t	t
1887	47	24	2017-08-10 11:57:23.025526	t	t
1888	47	36	2017-07-23 11:57:23.025555	t	t
1889	47	12	2017-08-10 11:57:23.025584	t	t
1890	47	20	2017-08-12 11:57:23.025614	t	t
1891	47	29	2017-07-25 11:57:23.025643	t	t
1892	47	15	2017-08-10 11:57:23.025672	f	t
1893	48	19	2017-08-03 11:57:23.025701	t	t
1894	48	8	2017-08-15 11:57:23.02573	t	t
1895	48	32	2017-07-29 11:57:23.025759	t	t
1896	48	21	2017-08-13 11:57:23.025788	t	t
1897	48	16	2017-07-29 11:57:23.025818	t	t
1898	48	11	2017-07-27 11:57:23.025862	t	t
1899	48	36	2017-08-01 11:57:23.025908	t	t
1900	48	18	2017-08-08 11:57:23.025958	f	t
1901	48	25	2017-08-06 11:57:23.025988	f	t
1902	48	35	2017-08-02 11:57:23.026018	f	t
1903	48	17	2017-07-23 11:57:23.026058	f	t
1904	48	35	2017-08-16 11:57:23.026089	f	t
1905	49	29	2017-07-30 11:57:23.026129	t	t
1906	49	32	2017-08-13 11:57:23.026158	t	t
1907	49	17	2017-08-04 11:57:23.026187	t	t
1908	49	35	2017-07-30 11:57:23.026216	t	t
1909	49	36	2017-08-13 11:57:23.026246	t	t
1910	49	24	2017-07-31 11:57:23.026274	t	t
1911	49	23	2017-07-26 11:57:23.026304	t	t
1912	49	12	2017-07-23 11:57:23.026334	t	t
1913	49	19	2017-08-02 11:57:23.026363	f	t
1914	50	10	2017-08-04 11:57:23.026393	t	t
1915	50	18	2017-08-16 11:57:23.026434	t	t
1916	50	25	2017-08-05 11:57:23.026465	t	t
1917	50	23	2017-07-29 11:57:23.026534	t	t
1918	50	11	2017-08-13 11:57:23.026567	t	t
1919	50	24	2017-08-08 11:57:23.026597	t	t
1920	50	14	2017-07-24 11:57:23.026626	t	t
1921	50	37	2017-08-07 11:57:23.026656	t	t
1922	50	22	2017-08-12 11:57:23.026686	t	t
1923	50	7	2017-07-27 11:57:23.026716	t	t
1924	50	9	2017-08-05 11:57:23.026745	t	t
1925	50	25	2017-07-28 11:57:23.026774	t	t
1926	50	29	2017-07-30 11:57:23.026803	t	t
1927	50	16	2017-08-07 11:57:23.026832	t	t
1928	50	26	2017-07-31 11:57:23.026861	t	t
1929	50	14	2017-08-07 11:57:23.02689	t	t
1930	50	20	2017-08-15 11:57:23.026919	t	t
1931	50	28	2017-08-12 11:57:23.026948	t	t
1932	50	33	2017-08-14 11:57:23.026977	t	t
1933	50	28	2017-08-08 11:57:23.027007	t	t
1934	50	20	2017-08-09 11:57:23.027036	t	t
1935	50	36	2017-07-29 11:57:23.027066	t	t
1936	50	9	2017-08-12 11:57:23.027096	t	t
1937	50	28	2017-08-16 11:57:23.027125	f	t
1938	50	32	2017-07-25 11:57:23.027154	f	t
1939	50	26	2017-07-29 11:57:23.0272	f	t
1940	50	12	2017-07-31 11:57:23.02723	f	t
1941	51	35	2017-07-28 11:57:23.027258	f	t
1942	51	18	2017-08-09 11:57:23.027287	f	t
1943	51	23	2017-08-10 11:57:23.027316	f	t
1944	51	7	2017-08-01 11:57:23.027346	f	t
1945	51	10	2017-08-11 11:57:23.027376	f	t
1946	51	16	2017-08-17 11:57:23.027415	f	t
1947	51	16	2017-07-28 11:57:23.027446	f	t
1948	51	9	2017-07-31 11:57:23.027477	f	t
1949	51	27	2017-08-14 11:57:23.027508	f	t
1950	52	12	2017-08-11 11:57:23.027539	t	t
1951	52	15	2017-08-12 11:57:23.027571	f	t
1952	52	29	2017-08-08 11:57:23.027602	f	t
1953	52	7	2017-08-12 11:57:23.027633	f	t
1954	52	16	2017-08-10 11:57:23.027665	f	t
1955	52	37	2017-07-29 11:57:23.027695	f	t
1956	52	32	2017-08-04 11:57:23.027726	f	t
1957	52	10	2017-07-29 11:57:23.027757	f	t
1958	52	29	2017-07-27 11:57:23.027788	f	t
1959	53	19	2017-08-08 11:57:23.027819	t	t
1960	53	24	2017-08-04 11:57:23.027849	t	t
1961	53	23	2017-08-12 11:57:23.02788	t	t
1962	53	11	2017-08-04 11:57:23.027911	t	t
1963	53	36	2017-08-05 11:57:23.027941	t	t
1964	53	28	2017-08-13 11:57:23.027971	t	t
1965	53	13	2017-08-09 11:57:23.028002	t	t
1966	53	15	2017-08-12 11:57:23.028033	t	t
1967	53	36	2017-08-02 11:57:23.028064	t	t
1968	53	23	2017-08-02 11:57:23.028095	t	t
1969	53	7	2017-08-12 11:57:23.028126	t	t
1970	53	27	2017-07-26 11:57:23.028156	t	t
1971	53	16	2017-07-31 11:57:23.028187	t	t
1972	53	19	2017-08-08 11:57:23.028218	f	t
1973	53	10	2017-08-08 11:57:23.028248	f	t
1974	53	27	2017-08-07 11:57:23.028278	f	t
1975	53	31	2017-08-02 11:57:23.028309	f	t
1976	53	36	2017-08-01 11:57:23.028339	f	t
1977	53	8	2017-08-10 11:57:23.02837	f	t
1978	53	13	2017-08-07 11:57:23.0284	f	t
1979	53	33	2017-08-16 11:57:23.028438	f	t
1980	53	32	2017-07-25 11:57:23.028467	f	t
1981	53	31	2017-08-01 11:57:23.028496	f	t
1982	53	15	2017-08-09 11:57:23.028525	f	t
1983	53	35	2017-08-10 11:57:23.028554	f	t
1984	53	31	2017-08-09 11:57:23.028583	f	t
1985	53	37	2017-08-12 11:57:23.028612	f	t
1986	54	14	2017-08-06 11:57:23.02864	t	t
1987	54	32	2017-08-07 11:57:23.028669	t	t
1988	54	32	2017-07-30 11:57:23.028697	t	t
1989	54	31	2017-08-07 11:57:23.028727	t	t
1990	54	22	2017-08-15 11:57:23.028756	t	t
1991	54	19	2017-08-04 11:57:23.028785	t	t
1992	54	28	2017-07-25 11:57:23.028814	t	t
1993	54	33	2017-08-01 11:57:23.028843	t	t
1994	54	11	2017-08-03 11:57:23.028873	t	t
1995	54	12	2017-07-24 11:57:23.028901	t	t
1996	54	33	2017-08-08 11:57:23.02893	t	t
1997	54	13	2017-08-09 11:57:23.02896	f	t
1998	54	29	2017-08-09 11:57:23.028989	f	t
1999	55	7	2017-08-16 11:57:23.029018	t	t
2000	55	10	2017-08-07 11:57:23.029048	t	t
2001	55	37	2017-07-28 11:57:23.029077	t	t
2002	55	22	2017-08-08 11:57:23.029105	f	t
2003	55	27	2017-08-13 11:57:23.029135	f	t
2004	56	14	2017-07-28 11:57:23.029164	t	t
2005	56	24	2017-08-13 11:57:23.029193	t	t
2006	56	18	2017-08-02 11:57:23.029222	t	t
2007	56	31	2017-08-13 11:57:23.029251	t	t
2008	56	21	2017-07-24 11:57:23.029281	t	t
2009	56	8	2017-07-31 11:57:23.02931	f	t
2010	56	16	2017-08-17 11:57:23.02934	f	t
2011	56	14	2017-08-13 11:57:23.02937	f	t
2012	56	13	2017-08-06 11:57:23.029399	f	t
2013	56	9	2017-08-10 11:57:23.029428	f	t
2014	56	14	2017-08-08 11:57:23.029457	f	t
2015	57	8	2017-08-09 11:57:23.029486	t	t
2016	57	10	2017-07-23 11:57:23.029515	t	t
2017	58	27	2017-08-03 11:57:23.029544	t	t
2018	58	9	2017-08-07 11:57:23.029574	t	t
2019	58	10	2017-08-04 11:57:23.029602	t	t
2020	58	22	2017-07-23 11:57:23.029632	t	t
2021	58	35	2017-08-14 11:57:23.029661	t	t
2022	58	18	2017-08-17 11:57:23.029691	t	t
2023	58	14	2017-07-24 11:57:23.02972	f	t
2024	58	35	2017-07-26 11:57:23.029749	f	t
2025	59	16	2017-08-14 11:57:23.029778	t	t
2026	59	37	2017-07-28 11:57:23.029807	t	t
2027	59	35	2017-08-09 11:57:23.029837	t	t
2028	59	31	2017-08-12 11:57:23.029872	t	t
2029	59	28	2017-07-30 11:57:23.029903	t	t
2030	59	12	2017-08-06 11:57:23.029932	t	t
2031	59	16	2017-08-15 11:57:23.029962	t	t
2032	59	16	2017-08-04 11:57:23.029991	t	t
2033	59	10	2017-07-31 11:57:23.030021	t	t
2034	59	15	2017-07-23 11:57:23.030049	t	t
2035	59	29	2017-08-11 11:57:23.030078	t	t
2036	59	26	2017-07-24 11:57:23.030107	t	t
2037	59	36	2017-08-16 11:57:23.030136	t	t
2038	59	26	2017-08-06 11:57:23.030165	f	t
2039	59	21	2017-07-27 11:57:23.030205	f	t
2040	59	16	2017-07-31 11:57:23.030245	f	t
2041	59	11	2017-08-13 11:57:23.030296	f	t
2042	59	11	2017-07-27 11:57:23.030346	f	t
2043	59	10	2017-07-26 11:57:23.030378	f	t
2044	59	34	2017-07-24 11:57:23.030437	f	t
2045	60	13	2017-08-01 11:57:23.030468	t	t
2046	60	14	2017-08-06 11:57:23.030499	t	t
2047	60	37	2017-08-05 11:57:23.030531	t	t
2048	60	29	2017-08-06 11:57:23.030562	f	t
2049	60	7	2017-08-04 11:57:23.030593	f	t
2050	60	18	2017-08-15 11:57:23.030624	f	t
2051	60	35	2017-08-13 11:57:23.030655	f	t
2052	60	29	2017-08-11 11:57:23.030687	f	t
2053	60	21	2017-08-13 11:57:23.030718	f	t
2054	60	29	2017-08-11 11:57:23.030749	f	t
2055	61	11	2017-08-09 11:57:23.03078	t	t
2056	61	21	2017-08-06 11:57:23.030811	t	t
2057	61	23	2017-08-06 11:57:23.030842	t	t
2058	61	18	2017-07-26 11:57:23.030873	t	t
2059	61	22	2017-07-23 11:57:23.030903	t	t
2060	61	13	2017-08-09 11:57:23.030933	t	t
2061	61	36	2017-08-17 11:57:23.030963	f	t
2062	61	23	2017-08-13 11:57:23.030994	f	t
2063	61	10	2017-08-12 11:57:23.031026	f	t
2064	61	10	2017-07-23 11:57:23.031058	f	t
2065	61	24	2017-08-14 11:57:23.031088	f	t
2066	61	16	2017-07-29 11:57:23.031119	f	t
2067	61	15	2017-07-23 11:57:23.031149	f	t
2068	61	34	2017-08-06 11:57:23.03118	f	t
2069	61	16	2017-07-30 11:57:23.031211	f	t
2070	61	23	2017-08-02 11:57:23.031242	f	t
2071	61	18	2017-08-09 11:57:23.031273	f	t
2072	61	27	2017-08-01 11:57:23.031303	f	t
2073	61	33	2017-07-25 11:57:23.031334	f	t
2074	61	21	2017-08-12 11:57:23.031364	f	t
2075	61	19	2017-08-11 11:57:23.031395	f	t
2076	61	33	2017-07-31 11:57:23.031433	f	t
2077	61	34	2017-07-27 11:57:23.031462	f	t
2078	61	16	2017-08-10 11:57:23.031491	f	t
2079	61	28	2017-08-09 11:57:23.031521	f	t
2080	61	29	2017-08-09 11:57:23.03155	f	t
2081	62	8	2017-07-31 11:57:23.031579	t	t
2082	62	26	2017-08-10 11:57:23.031608	t	t
2083	62	32	2017-08-09 11:57:23.031637	t	t
2084	62	14	2017-07-26 11:57:23.031666	t	t
2085	62	9	2017-08-13 11:57:23.031695	t	t
2086	62	37	2017-08-17 11:57:23.031725	t	t
2087	62	7	2017-08-09 11:57:23.031755	f	t
2088	62	29	2017-08-16 11:57:23.031784	f	t
2089	62	8	2017-08-03 11:57:23.031812	f	t
2090	62	29	2017-08-05 11:57:23.031841	f	t
2091	62	12	2017-08-11 11:57:23.031869	f	t
2092	62	10	2017-07-27 11:57:23.031898	f	t
2093	63	15	2017-08-17 11:57:23.031928	t	t
2094	64	28	2017-08-13 11:57:23.031957	t	t
2095	64	7	2017-07-28 11:57:23.031986	t	t
2096	64	29	2017-07-28 11:57:23.032015	f	t
2097	64	25	2017-08-16 11:57:23.032044	f	t
2098	64	34	2017-07-28 11:57:23.032074	f	t
2099	64	7	2017-07-30 11:57:23.032103	f	t
2100	64	31	2017-08-16 11:57:23.032132	f	t
2101	64	7	2017-08-06 11:57:23.032161	f	t
2102	65	33	2017-08-02 11:57:23.032191	t	t
2103	65	21	2017-08-13 11:57:23.03222	t	t
2104	65	23	2017-08-05 11:57:23.032249	t	t
2105	65	18	2017-08-02 11:57:23.032278	t	t
2106	65	11	2017-08-02 11:57:23.032307	t	t
2107	65	26	2017-08-17 11:57:23.032337	t	t
2108	65	28	2017-07-30 11:57:23.032366	t	t
2109	65	10	2017-08-12 11:57:23.032395	t	t
2110	65	28	2017-08-15 11:57:23.032425	t	t
2111	65	26	2017-07-24 11:57:23.032455	t	t
2112	65	23	2017-08-10 11:57:23.032484	t	t
2113	65	16	2017-07-25 11:57:23.032514	t	t
2114	65	34	2017-07-29 11:57:23.032544	t	t
2115	65	28	2017-08-02 11:57:23.032573	t	t
2116	65	8	2017-08-17 11:57:23.032602	t	t
2117	65	29	2017-08-02 11:57:23.032632	t	t
2118	65	31	2017-07-31 11:57:23.032661	t	t
2119	65	32	2017-08-07 11:57:23.03269	f	t
2120	65	7	2017-08-07 11:57:23.03272	f	t
2121	65	14	2017-07-30 11:57:23.032749	f	t
2122	65	19	2017-07-31 11:57:23.032778	f	t
2123	65	36	2017-07-28 11:57:23.032807	f	t
2124	65	21	2017-07-28 11:57:23.032837	f	t
2125	65	18	2017-07-24 11:57:23.032866	f	t
2126	65	8	2017-08-04 11:57:23.032895	f	t
2127	65	11	2017-08-01 11:57:23.032925	f	t
2128	65	24	2017-08-01 11:57:23.032954	f	t
2129	65	11	2017-07-27 11:57:23.032984	f	t
2130	66	25	2017-08-04 11:57:23.033013	t	t
2131	66	29	2017-08-04 11:57:23.033042	f	t
2132	67	29	2017-08-01 11:57:23.033071	t	t
2133	67	16	2017-07-27 11:57:23.033101	t	t
2134	67	31	2017-08-07 11:57:23.03313	t	t
2135	67	29	2017-07-24 11:57:23.03316	t	t
2136	67	21	2017-08-05 11:57:23.03319	t	t
2137	67	8	2017-08-01 11:57:23.033219	t	t
2138	67	8	2017-08-03 11:57:23.033249	t	t
2139	67	37	2017-07-24 11:57:23.033279	t	t
2140	67	37	2017-08-14 11:57:23.033308	t	t
2141	67	29	2017-07-28 11:57:23.033337	t	t
2142	67	32	2017-07-29 11:57:23.033366	f	t
2143	67	32	2017-08-04 11:57:23.033396	f	t
2144	67	25	2017-08-09 11:57:23.033425	f	t
2145	67	29	2017-08-17 11:57:23.033454	f	t
2146	67	33	2017-08-03 11:57:23.033483	f	t
2147	67	20	2017-07-28 11:57:23.033512	f	t
2148	67	10	2017-08-08 11:57:23.033542	f	t
2149	67	22	2017-08-13 11:57:23.033572	f	t
2150	67	31	2017-07-29 11:57:23.033601	f	t
2151	67	15	2017-08-10 11:57:23.03363	f	t
2152	67	26	2017-07-29 11:57:23.033659	f	t
2153	67	12	2017-08-10 11:57:23.033688	f	t
2154	67	31	2017-07-26 11:57:23.033717	f	t
2155	67	7	2017-08-17 11:57:23.033746	f	t
2156	67	31	2017-08-06 11:57:23.033775	f	t
2157	67	36	2017-07-27 11:57:23.033804	f	t
2158	67	20	2017-08-03 11:57:23.033833	f	t
2159	68	9	2017-08-06 11:57:23.03388	t	t
2160	68	23	2017-08-09 11:57:23.033931	t	t
2161	68	11	2017-07-31 11:57:23.03396	t	t
2162	68	14	2017-08-09 11:57:23.033989	t	t
2163	68	26	2017-08-06 11:57:23.034019	t	t
2164	68	26	2017-07-29 11:57:23.034048	t	t
2165	68	29	2017-08-02 11:57:23.034078	t	t
2166	68	34	2017-08-13 11:57:23.034106	t	t
2167	68	23	2017-08-14 11:57:23.034136	t	t
2168	68	14	2017-07-29 11:57:23.034165	t	t
2169	68	29	2017-07-28 11:57:23.034195	t	t
2170	68	26	2017-08-03 11:57:23.034224	t	t
2171	68	35	2017-07-25 11:57:23.034253	t	t
2172	68	29	2017-08-02 11:57:23.034299	t	t
2173	68	31	2017-08-07 11:57:23.034329	t	t
2174	68	8	2017-08-01 11:57:23.034359	t	t
2175	68	25	2017-08-17 11:57:23.034388	f	t
2176	68	18	2017-08-10 11:57:23.034426	f	t
2177	68	13	2017-08-17 11:57:23.034458	f	t
2178	68	32	2017-08-09 11:57:23.034489	f	t
2179	68	17	2017-08-01 11:57:23.03452	f	t
2180	68	32	2017-07-30 11:57:23.034551	f	t
2181	68	35	2017-07-30 11:57:23.034582	f	t
2182	68	11	2017-08-15 11:57:23.034613	f	t
2183	68	15	2017-08-10 11:57:23.034644	f	t
2184	68	18	2017-08-10 11:57:23.034675	f	t
2185	69	29	2017-08-13 11:57:23.034706	t	t
2186	69	24	2017-07-27 11:57:23.034737	f	t
2187	69	34	2017-08-17 11:57:23.034768	f	t
2188	69	9	2017-07-23 11:57:23.034799	f	t
2189	69	31	2017-07-24 11:57:23.03483	f	t
2190	70	29	2017-07-31 11:57:23.034861	t	t
2191	70	11	2017-07-28 11:57:23.034892	t	t
2192	70	17	2017-07-24 11:57:23.034923	t	t
2193	70	12	2017-07-31 11:57:23.034954	t	t
2194	70	14	2017-08-17 11:57:23.034985	t	t
2195	70	34	2017-08-13 11:57:23.035015	f	t
2196	70	31	2017-08-07 11:57:23.035047	f	t
2197	70	29	2017-08-10 11:57:23.035078	f	t
2198	70	32	2017-08-08 11:57:23.035108	f	t
2199	70	25	2017-07-24 11:57:23.03514	f	t
2200	70	20	2017-08-11 11:57:23.035171	f	t
2201	70	35	2017-08-09 11:57:23.035202	f	t
2202	71	13	2017-08-03 11:57:23.035233	t	t
2203	71	20	2017-08-13 11:57:23.035265	t	t
2204	71	14	2017-08-10 11:57:23.035295	t	t
2205	71	15	2017-08-02 11:57:23.035327	t	t
2206	71	18	2017-08-03 11:57:23.035358	t	t
2207	71	13	2017-07-26 11:57:23.035388	t	t
2208	71	18	2017-07-27 11:57:23.035427	t	t
2209	71	14	2017-07-24 11:57:23.035456	t	t
2210	71	13	2017-07-24 11:57:23.035485	f	t
2211	71	35	2017-08-09 11:57:23.035514	f	t
2212	71	21	2017-07-27 11:57:23.035543	f	t
2213	71	9	2017-08-07 11:57:23.035571	f	t
2214	71	29	2017-08-17 11:57:23.0356	f	t
2215	71	12	2017-08-07 11:57:23.03563	f	t
2216	71	36	2017-07-23 11:57:23.035659	f	t
2217	71	35	2017-07-26 11:57:23.035688	f	t
2218	71	12	2017-08-13 11:57:23.035717	f	t
2219	71	18	2017-08-04 11:57:23.035747	f	t
2220	71	18	2017-08-05 11:57:23.035776	f	t
2221	71	35	2017-08-15 11:57:23.035805	f	t
2222	71	27	2017-07-25 11:57:23.035834	f	t
2223	71	37	2017-07-31 11:57:23.035864	f	t
2224	71	36	2017-08-10 11:57:23.035893	f	t
2225	71	17	2017-08-12 11:57:23.035922	f	t
2226	72	33	2017-08-06 11:57:23.03595	t	t
2227	72	37	2017-07-24 11:57:23.03598	t	t
2228	72	14	2017-07-24 11:57:23.036009	t	t
2229	72	19	2017-08-03 11:57:23.036038	t	t
2230	72	29	2017-08-03 11:57:23.036068	t	t
2231	72	10	2017-08-16 11:57:23.036097	t	t
2232	72	28	2017-07-27 11:57:23.036127	t	t
2233	72	35	2017-07-27 11:57:23.036156	t	t
2234	72	36	2017-08-14 11:57:23.036185	t	t
2235	72	25	2017-08-17 11:57:23.036214	t	t
2236	72	34	2017-07-28 11:57:23.036243	t	t
2237	72	35	2017-08-07 11:57:23.036272	t	t
2238	72	12	2017-07-25 11:57:23.036301	t	t
2239	72	23	2017-07-27 11:57:23.03633	t	t
2240	72	10	2017-07-25 11:57:23.036359	f	t
2241	72	29	2017-08-11 11:57:23.036388	f	t
2242	73	20	2017-07-27 11:57:23.036418	t	t
2243	73	25	2017-07-29 11:57:23.036447	t	t
2244	73	32	2017-08-11 11:57:23.036476	t	t
2245	73	14	2017-08-10 11:57:23.036506	f	t
2246	73	10	2017-08-01 11:57:23.036535	f	t
2247	73	13	2017-08-01 11:57:23.036564	f	t
2248	73	13	2017-08-07 11:57:23.036594	f	t
2249	73	27	2017-08-10 11:57:23.036623	f	t
2250	73	19	2017-08-03 11:57:23.036652	f	t
2251	73	20	2017-08-07 11:57:23.036681	f	t
2252	73	21	2017-08-02 11:57:23.036711	f	t
2253	73	36	2017-08-17 11:57:23.03674	f	t
2254	73	24	2017-07-31 11:57:23.036771	f	t
2255	73	22	2017-08-08 11:57:23.0368	f	t
2256	73	14	2017-07-25 11:57:23.036829	f	t
2257	73	37	2017-07-26 11:57:23.036858	f	t
2258	73	15	2017-08-11 11:57:23.036887	f	t
2259	74	15	2017-08-13 11:57:23.036916	t	t
2260	74	35	2017-08-06 11:57:23.036947	t	t
2261	74	9	2017-08-17 11:57:23.036975	t	t
2262	74	35	2017-08-15 11:57:23.037004	t	t
2263	74	8	2017-08-08 11:57:23.037033	t	t
2264	74	27	2017-08-08 11:57:23.037063	t	t
2265	74	12	2017-08-05 11:57:23.037092	t	t
2266	74	35	2017-07-23 11:57:23.037122	t	t
2267	74	22	2017-08-03 11:57:23.037151	t	t
2268	74	29	2017-08-12 11:57:23.03718	t	t
2269	74	21	2017-08-17 11:57:23.037209	f	t
2270	74	34	2017-08-12 11:57:23.037239	f	t
2271	74	24	2017-08-15 11:57:23.037268	f	t
2272	74	33	2017-08-05 11:57:23.037297	f	t
2273	74	21	2017-08-02 11:57:23.037326	f	t
2274	74	19	2017-08-10 11:57:23.037355	f	t
2275	74	17	2017-08-15 11:57:23.037384	f	t
2276	75	28	2017-08-03 11:57:23.037414	t	t
2277	75	12	2017-08-16 11:57:23.037443	t	t
2278	75	21	2017-08-02 11:57:23.037473	t	t
2279	75	11	2017-08-01 11:57:23.037502	f	t
2280	75	35	2017-07-24 11:57:23.037532	f	t
2281	75	29	2017-08-11 11:57:23.037561	f	t
2282	75	21	2017-08-15 11:57:23.037591	f	t
2283	75	15	2017-07-25 11:57:23.03762	f	t
2284	75	16	2017-08-13 11:57:23.037649	f	t
2285	75	37	2017-07-26 11:57:23.037678	f	t
2286	75	32	2017-07-25 11:57:23.037708	f	t
2287	75	7	2017-07-24 11:57:23.037737	f	t
2288	75	22	2017-08-04 11:57:23.037766	f	t
2289	75	10	2017-08-17 11:57:23.037795	f	t
2290	75	23	2017-08-14 11:57:23.037824	f	t
2291	76	36	2017-08-13 11:57:23.037857	t	t
2292	76	11	2017-07-31 11:57:23.037887	t	t
2293	76	15	2017-08-16 11:57:23.037917	t	t
2294	76	19	2017-07-26 11:57:23.037947	t	t
2295	76	11	2017-07-29 11:57:23.037976	t	t
2296	76	17	2017-08-13 11:57:23.038006	t	t
2297	76	22	2017-07-31 11:57:23.038036	t	t
2298	76	29	2017-08-06 11:57:23.038065	t	t
2299	76	19	2017-08-07 11:57:23.038095	t	t
2300	76	22	2017-08-17 11:57:23.038124	t	t
2301	76	21	2017-08-04 11:57:23.038153	t	t
2302	76	26	2017-07-25 11:57:23.038182	t	t
2303	76	7	2017-08-10 11:57:23.038211	t	t
2304	76	31	2017-08-13 11:57:23.03824	t	t
2305	76	29	2017-08-10 11:57:23.038269	t	t
2306	76	29	2017-08-16 11:57:23.038298	t	t
2307	76	12	2017-07-31 11:57:23.038328	t	t
2308	76	16	2017-08-17 11:57:23.038357	t	t
2309	76	36	2017-08-17 11:57:23.038386	t	t
2310	76	14	2017-08-03 11:57:23.038415	t	t
2311	76	19	2017-07-30 11:57:23.038444	t	t
2312	76	24	2017-07-30 11:57:23.038473	t	t
2313	76	15	2017-07-30 11:57:23.038503	f	t
2314	76	16	2017-08-10 11:57:23.038531	f	t
2315	76	12	2017-07-31 11:57:23.03856	f	t
2316	76	29	2017-08-14 11:57:23.038589	f	t
2317	76	14	2017-08-16 11:57:23.038618	f	t
2318	76	36	2017-08-06 11:57:23.038648	f	t
2319	76	34	2017-08-05 11:57:23.038677	f	t
2320	76	15	2017-07-23 11:57:23.038706	f	t
2321	77	21	2017-07-30 11:57:23.038745	t	t
2322	77	7	2017-07-31 11:57:23.038775	t	t
2323	77	12	2017-08-17 11:57:23.038816	f	t
2324	77	33	2017-07-28 11:57:23.038847	f	t
2325	77	10	2017-08-14 11:57:23.03888	f	t
2326	77	13	2017-08-10 11:57:23.038954	f	t
2327	77	18	2017-08-09 11:57:23.038991	f	t
2328	77	27	2017-08-11 11:57:23.039021	f	t
2329	77	35	2017-08-05 11:57:23.039051	f	t
2330	77	11	2017-08-10 11:57:23.039081	f	t
2331	77	26	2017-08-08 11:57:23.03911	f	t
2332	77	20	2017-08-09 11:57:23.039139	f	t
2333	77	20	2017-08-07 11:57:23.039168	f	t
2334	77	37	2017-08-17 11:57:23.039198	f	t
2335	77	37	2017-07-23 11:57:23.039227	f	t
2336	77	11	2017-08-02 11:57:23.039256	f	t
2337	77	28	2017-08-16 11:57:23.039286	f	t
2338	77	21	2017-07-26 11:57:23.039315	f	t
2339	77	37	2017-07-24 11:57:23.039345	f	t
2340	78	16	2017-08-09 11:57:23.039374	t	t
2341	78	9	2017-07-25 11:57:23.039403	t	t
2342	78	23	2017-08-06 11:57:23.039433	t	t
2343	78	35	2017-08-13 11:57:23.039462	t	t
2344	78	34	2017-07-25 11:57:23.039492	t	t
2345	78	11	2017-07-31 11:57:23.039521	t	t
2346	78	11	2017-08-14 11:57:23.039551	t	t
2347	78	27	2017-07-27 11:57:23.03958	t	t
2348	78	8	2017-08-05 11:57:23.039609	t	t
2349	78	29	2017-08-08 11:57:23.039639	t	t
2350	78	16	2017-08-17 11:57:23.039668	t	t
2351	78	16	2017-08-16 11:57:23.039697	f	t
2352	78	11	2017-07-26 11:57:23.039727	f	t
2353	78	10	2017-07-26 11:57:23.039756	f	t
2354	78	27	2017-08-16 11:57:23.039785	f	t
2355	78	15	2017-07-23 11:57:23.039815	f	t
2356	78	12	2017-07-28 11:57:23.039844	f	t
2357	79	24	2017-08-05 11:57:23.039873	f	t
2358	79	29	2017-08-03 11:57:23.039902	f	t
2359	79	15	2017-08-11 11:57:23.039931	f	t
2360	80	25	2017-08-11 11:57:23.03996	t	t
2361	80	15	2017-08-12 11:57:23.039989	f	t
2362	80	13	2017-07-29 11:57:23.040018	f	t
2363	80	19	2017-08-04 11:57:23.040047	f	t
2364	80	27	2017-08-01 11:57:23.040076	f	t
2365	80	8	2017-08-12 11:57:23.040105	f	t
2366	80	34	2017-08-04 11:57:23.040134	f	t
2367	80	14	2017-07-27 11:57:23.040163	f	t
2368	80	18	2017-08-13 11:57:23.040191	f	t
2369	80	9	2017-07-29 11:57:23.040221	f	t
2370	80	21	2017-08-10 11:57:23.04025	f	t
2371	80	22	2017-08-04 11:57:23.04028	f	t
2372	80	11	2017-07-31 11:57:23.040308	f	t
2373	80	33	2017-08-07 11:57:23.040337	f	t
2374	80	31	2017-08-02 11:57:23.040366	f	t
2375	80	14	2017-07-30 11:57:23.040395	f	t
2376	80	23	2017-08-02 11:57:23.040424	f	t
2377	81	9	2017-08-07 11:57:23.040453	t	t
2378	81	27	2017-08-07 11:57:23.040482	f	t
2379	81	32	2017-08-03 11:57:23.040511	f	t
2380	81	28	2017-08-09 11:57:23.04054	f	t
2381	81	13	2017-07-24 11:57:23.040569	f	t
2382	81	26	2017-08-08 11:57:23.040598	f	t
2383	81	22	2017-07-30 11:57:23.040627	f	t
2384	81	34	2017-07-30 11:57:23.040656	f	t
2385	81	27	2017-07-29 11:57:23.040685	f	t
2386	81	26	2017-07-28 11:57:23.040714	f	t
2387	81	14	2017-07-30 11:57:23.040743	f	t
2388	82	35	2017-07-30 11:57:23.040772	t	t
2389	82	25	2017-07-23 11:57:23.040801	t	t
2390	82	14	2017-08-11 11:57:23.040829	t	t
2391	82	20	2017-08-15 11:57:23.040858	t	t
2392	82	29	2017-08-09 11:57:23.040888	t	t
2393	82	35	2017-08-05 11:57:23.040916	t	t
2394	82	34	2017-08-01 11:57:23.040945	t	t
2395	82	35	2017-08-10 11:57:23.040975	f	t
2396	82	26	2017-07-31 11:57:23.041004	f	t
2397	82	18	2017-08-09 11:57:23.041033	f	t
2398	82	24	2017-07-30 11:57:23.041062	f	t
2399	82	24	2017-08-07 11:57:23.04109	f	t
2400	82	22	2017-08-09 11:57:23.041119	f	t
\.


--
-- Name: clicked_statements_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('clicked_statements_uid_seq', 2400, true);


--
-- Data for Name: groups; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY groups (uid, name) FROM stdin;
1	admins
2	authors
3	users
\.


--
-- Name: groups_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('groups_uid_seq', 3, true);


--
-- Data for Name: history; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY history (uid, author_uid, path, "timestamp") FROM stdin;
\.


--
-- Name: history_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('history_uid_seq', 1, false);


--
-- Data for Name: issues; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY issues (uid, title, slug, info, long_info, date, author_uid, lang_uid, is_disabled) FROM stdin;
1	Town has to cut spending 	town-has-to-cut-spending	Our town needs to cut spending. Please discuss ideas how this should be done.		2017-08-17 11:57:14.995596	2	1	t
2	Cat or Dog	cat-or-dog	Your family argues about whether to buy a cat or dog as pet. Now your opinion matters!		2017-08-17 11:57:14.995771	2	1	f
3	Make the world better	make-the-world-better	How can we make this world a better place?		2017-08-17 11:57:14.995905	2	1	f
4	Elektroautos	elektroautos	Elektroautos - Die Autos der Zukunft? Bitte diskutieren Sie dazu.		2017-08-17 11:57:14.99603	2	2	f
5	Unterstützung der Sekretariate	unterstutzung-der-sekretariate	Unsere Sekretariate in der Informatik sind arbeitsmäßig stark überlastet. Bitte diskutieren Sie Möglichkeiten um dies zu verbessern.		2017-08-17 11:57:14.996884	2	2	f
6	Verbesserung des Informatik-Studiengangs	verbesserung-des-informatik-studiengangs	Wie können der Informatik-Studiengang verbessert und die Probleme, die durch die große Anzahl der Studierenden entstanden sind, gelöst werden?	Die Anzahl der Studierenden in der Informatik hat sich in den letzten Jahren stark erhöht. Dadurch treten zahlreiche Probleme auf, wie z.B. Raumknappheit, überfüllte Lehrveranstaltungen und ein Mangel an Plätzen zum Lernen. Wir möchten Sie gerne dazu einladen, gemeinsam mit den Dozierenden der Informatik über Lösungsmöglichkeiten zu diskutieren: Wie können der Studiengang verbessert und die Probleme, die durch die große Anzahl der Studierenden entstanden sind, gelöst werden?	2017-08-17 11:57:14.997031	2	2	t
7	Bürgerbeteiligung in der Kommune	burgerbeteiligung-in-der-kommune	Es werden Vorschläge zur Verbesserung des Zusammenlebens in unserer Kommune gesammelt.		2017-08-17 11:57:14.997178	2	2	f
\.


--
-- Name: issues_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('issues_uid_seq', 7, true);


--
-- Data for Name: languages; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY languages (uid, name, ui_locales) FROM stdin;
1	English	en
2	Deutsch	de
\.


--
-- Name: languages_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('languages_uid_seq', 2, true);


--
-- Data for Name: last_reviewers_delete; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY last_reviewers_delete (uid, reviewer_uid, review_uid, is_okay, "timestamp") FROM stdin;
1	14	1	t	2017-08-17 11:57:18.278297
2	16	1	f	2017-08-17 11:57:18.278386
3	17	1	t	2017-08-17 11:57:18.278471
4	22	1	t	2017-08-17 11:57:18.278555
5	23	1	t	2017-08-17 11:57:18.278648
6	20	2	f	2017-08-17 11:57:18.278726
7	21	2	t	2017-08-17 11:57:18.278803
8	18	2	f	2017-08-17 11:57:18.27888
9	34	2	t	2017-08-17 11:57:18.278957
10	24	2	f	2017-08-17 11:57:18.279034
11	25	2	f	2017-08-17 11:57:18.27911
12	26	2	f	2017-08-17 11:57:18.279187
13	27	3	f	2017-08-17 11:57:18.279263
14	28	3	f	2017-08-17 11:57:18.279341
15	33	3	f	2017-08-17 11:57:18.279417
16	19	8	t	2017-08-17 11:57:18.279494
17	35	8	t	2017-08-17 11:57:18.27957
18	36	8	t	2017-08-17 11:57:18.279647
\.


--
-- Name: last_reviewers_delete_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('last_reviewers_delete_uid_seq', 18, true);


--
-- Data for Name: last_reviewers_duplicates; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY last_reviewers_duplicates (uid, reviewer_uid, review_uid, is_okay, "timestamp") FROM stdin;
1	12	1	t	2017-08-17 11:57:18.279749
2	13	2	t	2017-08-17 11:57:18.279888
3	14	2	t	2017-08-17 11:57:18.279976
\.


--
-- Name: last_reviewers_duplicates_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('last_reviewers_duplicates_uid_seq', 3, true);


--
-- Data for Name: last_reviewers_edit; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY last_reviewers_edit (uid, reviewer_uid, review_uid, is_okay, "timestamp") FROM stdin;
\.


--
-- Name: last_reviewers_edit_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('last_reviewers_edit_uid_seq', 1, false);


--
-- Data for Name: last_reviewers_merge; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY last_reviewers_merge (uid, reviewer_uid, review_uid, should_merge, "timestamp") FROM stdin;
\.


--
-- Name: last_reviewers_merge_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('last_reviewers_merge_uid_seq', 1, false);


--
-- Data for Name: last_reviewers_optimization; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY last_reviewers_optimization (uid, reviewer_uid, review_uid, is_okay, "timestamp") FROM stdin;
1	29	1	t	2017-08-17 11:57:18.2776
2	31	1	t	2017-08-17 11:57:18.277785
3	32	1	t	2017-08-17 11:57:18.277926
4	12	2	f	2017-08-17 11:57:18.278019
5	13	2	f	2017-08-17 11:57:18.278107
6	15	2	f	2017-08-17 11:57:18.278192
\.


--
-- Name: last_reviewers_optimization_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('last_reviewers_optimization_uid_seq', 6, true);


--
-- Data for Name: last_reviewers_split; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY last_reviewers_split (uid, reviewer_uid, review_uid, should_split, "timestamp") FROM stdin;
\.


--
-- Name: last_reviewers_split_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('last_reviewers_split_uid_seq', 1, false);


--
-- Data for Name: marked_arguments; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY marked_arguments (uid, argument_uid, author_uid, "timestamp") FROM stdin;
\.


--
-- Name: marked_arguments_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('marked_arguments_uid_seq', 1, false);


--
-- Data for Name: marked_statements; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY marked_statements (uid, statement_uid, author_uid, "timestamp") FROM stdin;
\.


--
-- Name: marked_statements_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('marked_statements_uid_seq', 1, false);


--
-- Data for Name: messages; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY messages (uid, from_author_uid, to_author_uid, topic, content, "timestamp", read, is_inbox) FROM stdin;
\.


--
-- Name: messages_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('messages_uid_seq', 1, false);


--
-- Data for Name: optimization_review_locks; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY optimization_review_locks (author_uid, review_optimization_uid, locked_since) FROM stdin;
\.


--
-- Data for Name: premisegroup_merged; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY premisegroup_merged (uid, review_uid, old_premisegroup_uid, new_premisegroup_uid, "timestamp") FROM stdin;
\.


--
-- Name: premisegroup_merged_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('premisegroup_merged_uid_seq', 1, false);


--
-- Data for Name: premisegroup_splitted; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY premisegroup_splitted (uid, review_uid, old_premisegroup_uid, new_premisegroup_uid, "timestamp") FROM stdin;
\.


--
-- Name: premisegroup_splitted_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('premisegroup_splitted_uid_seq', 1, false);


--
-- Data for Name: premisegroups; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY premisegroups (uid, author_uid) FROM stdin;
1	1
2	1
3	1
4	1
5	1
6	1
7	1
8	1
9	1
10	1
11	1
12	1
13	1
14	1
15	1
16	1
17	1
18	1
19	1
20	1
21	1
22	1
23	1
24	1
25	1
26	1
27	1
28	1
29	1
30	1
31	1
32	1
33	1
34	1
35	1
36	1
37	1
38	1
39	1
40	1
41	1
42	1
43	1
44	1
45	1
46	1
47	1
48	1
49	1
50	1
51	1
52	1
53	1
54	1
55	1
56	1
57	1
58	1
59	1
60	1
61	5
62	1
63	1
64	1
65	1
66	1
67	1
68	1
69	1
70	1
71	1
\.


--
-- Name: premisegroups_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('premisegroups_uid_seq', 71, true);


--
-- Data for Name: premises; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY premises (uid, premisesgroup_uid, statement_uid, is_negated, author_uid, "timestamp", issue_uid, is_disabled) FROM stdin;
1	1	1	f	1	2017-08-17 11:57:15.263887	2	t
2	2	5	f	1	2017-08-17 11:57:15.264088	2	f
3	3	6	f	1	2017-08-17 11:57:15.264215	2	f
4	4	7	f	1	2017-08-17 11:57:15.264336	2	f
5	5	8	f	1	2017-08-17 11:57:15.264455	2	f
6	6	9	f	1	2017-08-17 11:57:15.264572	2	f
7	7	10	f	1	2017-08-17 11:57:15.264687	2	f
8	8	11	f	1	2017-08-17 11:57:15.264847	2	f
9	9	12	f	1	2017-08-17 11:57:15.26497	2	f
10	10	13	f	1	2017-08-17 11:57:15.265086	2	f
11	11	14	f	1	2017-08-17 11:57:15.2652	2	f
12	12	15	f	1	2017-08-17 11:57:15.265314	2	f
13	12	16	f	1	2017-08-17 11:57:15.265427	2	f
14	13	17	f	1	2017-08-17 11:57:15.265542	2	f
15	14	18	f	1	2017-08-17 11:57:15.265657	2	f
16	15	19	f	1	2017-08-17 11:57:15.265771	2	f
17	16	20	f	1	2017-08-17 11:57:15.265897	2	f
18	17	21	f	1	2017-08-17 11:57:15.266015	2	f
19	18	22	f	1	2017-08-17 11:57:15.26613	2	f
20	19	23	f	1	2017-08-17 11:57:15.266244	2	f
21	20	24	f	1	2017-08-17 11:57:15.266358	2	f
22	21	25	f	1	2017-08-17 11:57:15.266473	2	f
23	22	26	f	1	2017-08-17 11:57:15.266588	2	f
24	23	27	f	1	2017-08-17 11:57:15.266702	2	f
25	24	28	f	1	2017-08-17 11:57:15.266816	2	f
26	25	29	f	1	2017-08-17 11:57:15.266931	2	f
27	26	30	f	1	2017-08-17 11:57:15.267046	2	f
28	27	31	f	1	2017-08-17 11:57:15.267164	2	f
29	28	32	f	1	2017-08-17 11:57:15.267278	2	f
30	29	33	f	1	2017-08-17 11:57:15.267392	2	f
31	30	34	f	1	2017-08-17 11:57:15.267506	2	f
32	9	35	f	1	2017-08-17 11:57:15.26762	2	f
33	31	39	f	1	2017-08-17 11:57:15.267735	1	f
34	32	40	f	1	2017-08-17 11:57:15.267849	1	f
35	33	41	f	1	2017-08-17 11:57:15.267963	1	f
36	34	42	f	1	2017-08-17 11:57:15.268076	1	f
37	35	43	f	1	2017-08-17 11:57:15.26819	1	f
38	36	44	f	1	2017-08-17 11:57:15.268304	1	f
39	37	45	f	1	2017-08-17 11:57:15.268419	1	f
40	38	46	f	1	2017-08-17 11:57:15.268533	1	f
41	39	47	f	1	2017-08-17 11:57:15.268647	1	f
42	40	48	f	1	2017-08-17 11:57:15.26876	1	f
43	41	49	f	1	2017-08-17 11:57:15.268873	1	f
44	42	50	f	1	2017-08-17 11:57:15.268986	1	f
45	43	51	f	1	2017-08-17 11:57:15.269101	1	f
46	44	52	f	1	2017-08-17 11:57:15.269217	1	f
47	45	53	f	1	2017-08-17 11:57:15.269332	1	f
48	46	54	f	1	2017-08-17 11:57:15.269446	1	f
49	47	55	f	1	2017-08-17 11:57:15.269559	1	f
50	48	56	f	1	2017-08-17 11:57:15.269672	1	f
51	49	57	f	1	2017-08-17 11:57:15.269786	1	f
52	52	61	f	1	2017-08-17 11:57:15.270102	4	f
53	53	62	f	1	2017-08-17 11:57:15.270192	4	f
54	54	63	f	1	2017-08-17 11:57:15.270361	4	f
55	55	64	f	1	2017-08-17 11:57:15.270457	4	f
56	56	65	f	1	2017-08-17 11:57:15.27055	4	f
57	57	66	f	1	2017-08-17 11:57:15.270642	4	f
58	50	59	f	1	2017-08-17 11:57:15.269916	4	f
59	51	60	f	1	2017-08-17 11:57:15.270009	4	f
60	61	68	f	5	2017-08-17 11:57:15.270734	4	f
61	62	71	f	1	2017-08-17 11:57:15.270825	5	f
62	63	72	f	1	2017-08-17 11:57:15.270917	5	f
63	64	73	f	1	2017-08-17 11:57:15.271008	5	f
64	65	74	f	1	2017-08-17 11:57:15.271102	5	f
65	66	75	f	1	2017-08-17 11:57:15.271183	5	f
66	67	77	f	1	2017-08-17 11:57:15.271255	7	f
67	68	78	f	1	2017-08-17 11:57:15.271325	7	f
68	69	79	f	1	2017-08-17 11:57:15.271395	7	f
69	70	80	f	1	2017-08-17 11:57:15.271467	7	f
70	70	81	f	1	2017-08-17 11:57:15.271538	7	f
71	71	82	f	1	2017-08-17 11:57:15.271617	7	f
\.


--
-- Name: premises_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('premises_uid_seq', 71, true);


--
-- Data for Name: reputation_history; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY reputation_history (uid, reputator_uid, reputation_uid, "timestamp") FROM stdin;
1	23	1	2017-08-15 11:57:18.311621
2	23	2	2017-08-16 11:57:18.311621
3	23	3	2017-08-17 11:57:18.311621
4	25	1	2017-08-15 11:57:18.311621
5	25	2	2017-08-16 11:57:18.311621
6	25	3	2017-08-17 11:57:18.311621
7	22	1	2017-08-15 11:57:18.311621
8	22	2	2017-08-16 11:57:18.311621
9	22	3	2017-08-17 11:57:18.311621
10	34	1	2017-08-15 11:57:18.311621
11	34	2	2017-08-16 11:57:18.311621
12	34	3	2017-08-17 11:57:18.311621
13	3	1	2017-08-15 11:57:18.311621
14	3	2	2017-08-16 11:57:18.311621
15	3	3	2017-08-17 11:57:18.311621
16	3	8	2017-08-17 11:57:18.311621
17	3	3	2017-08-15 11:57:18.311621
18	3	4	2017-08-15 11:57:18.311621
19	3	5	2017-08-16 11:57:18.311621
20	3	6	2017-08-16 11:57:18.311621
21	3	9	2017-08-17 11:57:18.311621
22	3	8	2017-08-17 11:57:18.311621
23	2	4	2017-08-15 11:57:18.311621
24	2	5	2017-08-15 11:57:18.311621
25	2	6	2017-08-16 11:57:18.311621
26	2	9	2017-08-16 11:57:18.311621
27	2	7	2017-08-17 11:57:18.311621
28	2	10	2017-08-17 11:57:18.311621
29	2	8	2017-08-17 11:57:18.311621
30	2	11	2017-08-17 11:57:18.311621
31	2	12	2017-08-17 11:57:18.311621
\.


--
-- Name: reputation_history_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('reputation_history_uid_seq', 31, true);


--
-- Data for Name: reputation_reasons; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY reputation_reasons (uid, reason, points) FROM stdin;
1	rep_reason_first_position	10
2	rep_reason_first_justification	10
3	rep_reason_first_argument_click	10
4	rep_reason_first_confrontation	10
5	rep_reason_first_new_argument	10
6	rep_reason_new_statement	2
7	rep_reason_success_flag	3
8	rep_reason_success_edit	3
9	rep_reason_success_duplicate	3
10	rep_reason_bad_flag	-1
11	rep_reason_bad_edit	-1
12	rep_reason_bad_duplicate	-1
\.


--
-- Name: reputation_reasons_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('reputation_reasons_uid_seq', 12, true);


--
-- Data for Name: review_canceled; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY review_canceled (uid, author_uid, review_edit_uid, review_delete_uid, review_optimization_uid, review_duplicate_uid, review_merge_uid, review_split_uid, was_ongoing, "timestamp") FROM stdin;
\.


--
-- Name: review_canceled_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('review_canceled_uid_seq', 1, false);


--
-- Data for Name: review_delete_reasons; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY review_delete_reasons (uid, reason) FROM stdin;
1	offtopic
2	harmful
\.


--
-- Name: review_delete_reasons_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('review_delete_reasons_uid_seq', 2, true);


--
-- Data for Name: review_deletes; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY review_deletes (uid, detector_uid, argument_uid, statement_uid, "timestamp", is_executed, reason_uid, is_revoked) FROM stdin;
1	18	26	\N	2017-08-17 11:57:18.248907	t	1	f
2	19	9	\N	2017-08-17 11:57:18.248987	t	1	f
3	20	\N	26	2017-08-17 11:57:18.249062	t	1	f
4	21	\N	19	2017-08-17 11:57:18.249135	f	1	f
5	22	\N	25	2017-08-17 11:57:18.249208	f	2	f
6	23	\N	21	2017-08-17 11:57:18.249298	f	2	f
7	24	22	\N	2017-08-17 11:57:18.24941	f	2	f
8	25	8	\N	2017-08-17 11:57:18.249524	f	1	f
9	26	20	\N	2017-08-17 11:57:18.249614	f	1	f
10	27	1	\N	2017-08-17 11:57:18.249691	t	1	f
\.


--
-- Name: review_deletes_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('review_deletes_uid_seq', 10, true);


--
-- Data for Name: review_duplicates; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY review_duplicates (uid, detector_uid, duplicate_statement_uid, original_statement_uid, "timestamp", is_executed, is_revoked) FROM stdin;
1	28	6	1	2017-08-17 11:57:18.249773	f	f
2	29	4	1	2017-08-17 11:57:18.249873	t	f
3	29	22	7	2017-08-17 11:57:18.249977	f	f
\.


--
-- Name: review_duplicates_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('review_duplicates_uid_seq', 3, true);


--
-- Data for Name: review_edit_values; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY review_edit_values (uid, review_edit_uid, statement_uid, typeof, content) FROM stdin;
1	1	2		as
\.


--
-- Name: review_edit_values_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('review_edit_values_uid_seq', 1, true);


--
-- Data for Name: review_edits; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY review_edits (uid, detector_uid, argument_uid, statement_uid, "timestamp", is_executed, is_revoked) FROM stdin;
1	3	\N	2	2017-08-17 11:57:18.326078	f	f
\.


--
-- Name: review_edits_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('review_edits_uid_seq', 1, true);


--
-- Data for Name: review_merge; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY review_merge (uid, detector_uid, premisesgroup_uid, "timestamp", is_executed, is_revoked) FROM stdin;
1	31	1	2017-08-17 11:57:18.250053	f	f
2	32	5	2017-08-17 11:57:18.250123	f	f
\.


--
-- Name: review_merge_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('review_merge_uid_seq', 2, true);


--
-- Data for Name: review_merge_values; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY review_merge_values (uid, review_uid, content) FROM stdin;
1	1	Lorem ipsum dolor sit amet, consetetur (value01)
\.


--
-- Name: review_merge_values_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('review_merge_values_uid_seq', 1, true);


--
-- Data for Name: review_optimizations; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY review_optimizations (uid, detector_uid, argument_uid, statement_uid, "timestamp", is_executed, is_revoked) FROM stdin;
1	12	6	\N	2017-08-17 11:57:18.248413	t	f
2	13	\N	22	2017-08-17 11:57:18.248533	t	f
3	14	\N	23	2017-08-17 11:57:18.248608	f	f
4	16	27	\N	2017-08-17 11:57:18.24875	f	f
5	17	20	\N	2017-08-17 11:57:18.248819	f	f
6	15	\N	29	2017-08-17 11:57:18.24868	f	f
\.


--
-- Name: review_optimizations_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('review_optimizations_uid_seq', 6, true);


--
-- Data for Name: review_split; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY review_split (uid, detector_uid, premisesgroup_uid, "timestamp", is_executed, is_revoked) FROM stdin;
1	33	10	2017-08-17 11:57:18.250196	f	f
2	34	12	2017-08-17 11:57:18.250266	f	f
\.


--
-- Name: review_split_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('review_split_uid_seq', 2, true);


--
-- Data for Name: review_split_values; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY review_split_values (uid, review_uid, content) FROM stdin;
1	2	ea rebum.Stet clita kasd gubergren, no (value06)
2	2	sea takimata sanctus est Lorem ipsum (value07)
3	2	dolor sit amet.Lorem ipsum dolor sit (value08)
4	2	amet, consetetur sadipscing elitr, sed (value09)
5	2	diam nonumy eirmod tempor invidunt ut (value10)
\.


--
-- Name: review_split_values_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('review_split_values_uid_seq', 5, true);


--
-- Data for Name: revoked_content; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY revoked_content (uid, author_uid, argument_uid, statement_uid, "timestamp") FROM stdin;
\.


--
-- Data for Name: revoked_content_history; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY revoked_content_history (uid, old_author_uid, new_author_uid, textversion_uid, argument_uid) FROM stdin;
\.


--
-- Name: revoked_content_history_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('revoked_content_history_uid_seq', 1, false);


--
-- Name: revoked_content_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('revoked_content_uid_seq', 1, false);


--
-- Data for Name: revoked_duplicate; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY revoked_duplicate (uid, review_uid, bend_position, statement_uid, argument_uid, premise_uid, "timestamp") FROM stdin;
\.


--
-- Name: revoked_duplicate_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('revoked_duplicate_uid_seq', 1, false);


--
-- Data for Name: rss; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY rss (uid, author_uid, issue_uid, title, description, "timestamp") FROM stdin;
\.


--
-- Name: rss_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('rss_uid_seq', 1, false);


--
-- Data for Name: seen_arguments; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY seen_arguments (uid, argument_uid, user_uid) FROM stdin;
1203	1	23
1204	1	15
1205	1	34
1206	1	11
1207	1	12
1208	1	33
1209	1	21
1210	1	17
1211	2	33
1212	2	21
1213	2	23
1214	2	14
1215	2	24
1216	2	15
1217	2	12
1218	2	9
1219	2	18
1220	2	28
1221	2	8
1222	2	27
1223	2	35
1224	2	16
1225	2	7
1226	2	34
1227	2	29
1228	2	31
1229	2	32
1230	2	36
1231	2	29
1232	2	13
1233	2	17
1234	2	11
1235	2	20
1236	3	9
1237	3	14
1238	3	13
1239	3	7
1240	3	19
1241	3	36
1242	3	27
1243	4	32
1244	4	10
1245	4	18
1246	4	9
1247	4	22
1248	4	17
1249	4	7
1250	5	31
1251	5	8
1252	5	11
1253	5	32
1254	5	26
1255	5	12
1256	5	22
1257	5	23
1258	5	29
1259	5	19
1260	5	20
1261	5	18
1262	8	31
1263	8	34
1264	8	28
1265	8	24
1266	8	7
1267	8	36
1268	8	12
1269	8	22
1270	8	13
1271	8	37
1272	8	25
1273	8	10
1274	8	27
1275	8	23
1276	8	19
1277	8	16
1278	8	18
1279	8	29
1280	8	26
1281	8	15
1282	8	9
1283	8	17
1284	8	29
1285	8	32
1286	10	37
1287	10	17
1288	10	35
1289	10	16
1290	10	21
1291	10	19
1292	10	12
1293	10	9
1294	10	34
1295	10	10
1296	10	18
1297	10	20
1298	10	22
1299	10	11
1300	10	7
1301	10	36
1302	10	24
1303	10	31
1304	10	33
1305	10	15
1306	10	29
1307	10	28
1308	10	8
1309	11	37
1310	11	11
1311	11	16
1312	11	10
1313	11	33
1314	11	14
1315	11	21
1316	11	7
1317	11	19
1318	12	26
1319	12	36
1320	12	29
1321	12	12
1322	12	16
1323	12	34
1324	12	22
1325	12	19
1326	12	18
1327	12	37
1328	12	31
1329	12	8
1330	12	7
1331	12	13
1332	12	27
1333	15	9
1334	15	36
1335	15	19
1336	15	21
1337	16	29
1338	16	34
1339	16	9
1340	16	32
1341	16	20
1342	16	22
1343	16	24
1344	16	13
1345	16	16
1346	16	17
1347	16	31
1348	16	15
1349	16	14
1350	16	10
1351	16	28
1352	16	23
1353	16	27
1354	16	7
1355	16	35
1356	16	33
1357	16	36
1358	16	26
1359	16	29
1360	16	37
1361	16	19
1362	16	25
1363	16	21
1364	16	11
1365	17	22
1366	17	28
1367	17	36
1368	17	12
1369	17	35
1370	17	13
1371	17	18
1372	17	37
1373	17	29
1374	17	20
1375	17	21
1376	17	31
1377	17	11
1378	17	24
1379	19	29
1380	19	10
1381	19	27
1382	19	16
1383	19	33
1384	19	26
1385	19	35
1386	19	8
1387	19	18
1388	19	20
1389	19	14
1390	19	23
1391	19	31
1392	19	36
1393	19	32
1394	19	12
1395	19	29
1396	19	9
1397	19	22
1398	19	37
1399	19	25
1400	19	13
1401	19	11
1402	19	28
1403	19	17
1404	19	34
1405	19	24
1406	19	15
1407	20	35
1408	20	36
1409	20	31
1410	20	25
1411	20	21
1412	20	28
1413	20	37
1414	20	8
1415	20	26
1416	20	10
1417	20	23
1418	20	15
1419	20	34
1420	20	14
1421	20	19
1422	20	11
1423	20	33
1424	20	17
1425	20	32
1426	20	7
1427	20	29
1428	20	27
1429	20	9
1430	21	8
1431	21	36
1432	21	27
1433	21	22
1434	21	25
1435	21	29
1436	21	15
1437	21	7
1438	21	20
1439	21	32
1440	21	29
1441	21	21
1442	21	10
1443	21	12
1444	21	13
1445	21	24
1446	21	18
1447	21	17
1448	21	34
1449	21	23
1450	21	35
1451	21	26
1452	21	11
1453	21	16
1454	23	20
1455	23	22
1456	23	34
1457	23	36
1458	23	13
1459	23	29
1460	23	31
1461	23	15
1462	23	7
1463	23	26
1464	23	10
1465	23	25
1466	23	32
1467	23	11
1468	23	17
1469	23	33
1470	23	19
1471	24	29
1472	24	22
1473	24	12
1474	24	25
1475	26	24
1476	26	22
1477	26	35
1478	26	18
1479	26	29
1480	26	31
1481	26	29
1482	26	23
1483	26	27
1484	26	28
1485	26	10
1486	26	17
1487	26	16
1488	27	35
1489	27	18
1490	27	34
1491	27	15
1492	27	20
1493	27	21
1494	27	37
1495	27	31
1496	27	17
1497	27	14
1498	27	7
1499	27	23
1500	27	10
1501	27	12
1502	27	26
1503	28	36
1504	28	29
1505	28	15
1506	28	23
1507	28	34
1508	28	19
1509	28	33
1510	28	26
1511	29	7
1512	29	19
1513	29	12
1514	29	31
1515	29	37
1516	29	13
1517	29	18
1518	29	36
1519	29	22
1520	29	17
1521	29	21
1522	29	32
1523	29	29
1524	29	9
1525	29	26
1526	29	35
1527	29	15
1528	29	20
1529	29	11
1530	29	33
1531	29	14
1532	29	24
1533	29	27
1534	30	19
1535	30	21
1536	30	25
1537	30	9
1538	30	14
1539	30	31
1540	30	8
1541	30	7
1542	30	26
1543	30	35
1544	30	20
1545	30	37
1546	30	24
1547	30	28
1548	30	16
1549	30	15
1550	30	36
1551	30	17
1552	30	29
1553	30	29
1554	30	10
1555	30	18
1556	30	23
1557	30	34
1558	30	22
1559	30	13
1560	30	12
1561	32	28
1562	32	20
1563	32	16
1564	32	29
1565	32	32
1566	32	12
1567	32	14
1568	32	36
1569	32	37
1570	32	23
1571	32	33
1572	32	22
1573	32	9
1574	32	8
1575	32	24
1576	34	33
1577	34	32
1578	34	19
1579	34	26
1580	34	35
1581	34	24
1582	34	23
1583	34	15
1584	34	12
1585	34	8
1586	34	29
1587	34	25
1588	34	9
1589	34	16
1590	34	7
1591	34	14
1592	35	16
1593	35	24
1594	35	32
1595	35	27
1596	35	34
1597	35	15
1598	35	26
1599	35	23
1600	35	29
1601	35	21
1602	35	12
1603	35	8
1604	35	29
1605	35	36
1606	35	7
1607	35	14
1608	35	9
1609	35	35
1610	35	10
1611	35	13
1612	35	19
1613	36	12
1614	36	22
1615	36	7
1616	36	15
1617	36	8
1618	36	35
1619	36	28
1620	36	36
1621	36	34
1622	36	11
1623	36	9
1624	36	16
1625	36	20
1626	36	29
1627	36	33
1628	36	19
1629	36	14
1630	36	26
1631	36	17
1632	36	27
1633	36	31
1634	39	10
1635	39	24
1636	39	31
1637	39	13
1638	39	29
1639	39	16
1640	39	25
1641	39	28
1642	39	20
1643	39	7
1644	39	9
1645	39	35
1646	40	14
1647	40	24
1648	40	28
1649	40	33
1650	40	20
1651	40	29
1652	40	27
1653	40	36
1654	40	25
1655	40	34
1656	40	9
1657	40	22
1658	40	11
1659	40	17
1660	40	21
1661	40	12
1662	40	8
1663	40	15
1664	41	34
1665	41	15
1666	41	31
1667	41	20
1668	41	7
1669	41	12
1670	41	25
1671	41	32
1672	41	22
1673	41	8
1674	41	18
1675	42	21
1676	42	13
1677	42	33
1678	42	8
1679	42	36
1680	42	26
1681	42	32
1682	42	16
1683	42	19
1684	42	37
1685	42	18
1686	42	14
1687	42	28
1688	42	7
1689	42	15
1690	42	17
1691	42	11
1692	42	31
1693	42	34
1694	42	24
1695	42	22
1696	42	35
1697	42	29
1698	42	25
1699	42	20
1700	42	9
1701	42	12
1702	44	20
1703	44	22
1704	44	10
1705	44	36
1706	44	24
1707	44	18
1708	46	20
1709	46	27
1710	46	15
1711	46	14
1712	46	18
1713	46	26
1714	46	12
1715	46	28
1716	46	21
1717	46	25
1718	46	22
1719	46	29
1720	46	8
1721	47	13
1722	47	8
1723	47	29
1724	47	17
1725	47	19
1726	47	22
1727	49	7
1728	49	24
1729	49	22
1730	49	20
1731	49	19
1732	49	10
1733	49	17
1734	49	16
1735	49	33
1736	49	15
1737	49	26
1738	49	11
1739	49	29
1740	49	32
1741	49	25
1742	49	29
1743	49	34
1744	49	8
1745	49	27
1746	49	14
1747	49	18
1748	49	9
1749	49	35
1750	49	23
1751	49	21
1752	50	36
1753	50	13
1754	50	15
1755	50	34
1756	50	27
1757	50	24
1758	50	29
1759	50	21
1760	50	28
1761	50	33
1762	50	7
1763	50	19
1764	51	7
1765	51	29
1766	51	16
1767	51	29
1768	51	14
1769	51	37
1770	51	15
1771	51	35
1772	51	33
1773	51	12
1774	51	21
1775	51	22
1776	51	24
1777	51	34
1778	51	11
1779	51	26
1780	51	32
1781	51	23
1782	51	13
1783	51	28
1784	51	9
1785	51	20
1786	51	25
1787	51	31
1788	51	19
1789	51	36
1790	51	10
1791	54	26
1792	54	29
1793	54	11
1794	54	29
1795	54	12
1796	54	32
1797	54	15
1798	54	13
1799	54	21
1800	54	17
1801	54	20
1802	54	37
1803	54	16
1804	54	9
1805	54	35
1806	54	23
1807	54	7
1808	54	36
1809	54	27
1810	54	31
1811	54	22
1812	54	8
1813	54	24
1814	54	33
1815	54	18
1816	54	28
1817	55	29
1818	55	17
1819	55	15
1820	55	33
1821	56	8
1822	56	10
1823	56	26
1824	56	25
1825	56	36
1826	57	26
1827	57	12
1828	57	36
1829	57	7
1830	57	10
1831	57	11
1832	57	15
1833	57	25
1834	57	13
1835	57	8
1836	57	27
1837	57	21
1838	57	37
1839	57	28
1840	57	20
1841	57	29
1842	57	9
1843	57	17
1844	57	34
1845	58	35
1846	58	24
1847	58	21
1848	58	15
1849	58	10
1850	58	25
1851	58	28
1852	58	29
1853	58	26
1854	58	27
1855	58	14
1856	58	32
1857	58	22
1858	58	37
1859	58	8
1860	58	18
1861	59	35
1862	59	7
1863	59	32
1864	59	24
1865	59	12
1866	59	13
1867	59	10
1868	59	9
1869	59	16
1870	59	19
1871	59	26
1872	59	34
1873	59	29
1874	59	31
1875	59	11
1876	59	29
1877	59	22
1878	59	27
1879	59	28
1880	59	8
1881	59	20
1882	60	28
1883	60	21
1884	60	25
1885	60	35
1886	60	11
1887	60	36
1888	60	33
1889	60	29
1890	60	7
1891	60	14
1892	60	10
1893	60	20
1894	60	32
1895	60	29
1896	61	26
1897	61	11
1898	61	24
1899	61	12
1900	61	27
1901	62	31
1902	62	37
1903	62	25
1904	62	27
1905	62	12
1906	62	14
1907	62	23
1908	62	29
1909	62	22
1910	62	9
1911	62	21
1912	62	17
1913	63	23
1914	63	34
1915	63	17
1916	63	26
1917	63	24
1918	64	26
1919	64	34
1920	64	11
1921	64	31
1922	64	12
1923	64	28
1924	64	9
1925	64	36
1926	64	21
1927	64	19
1928	64	27
1929	64	16
1930	64	29
1931	64	35
1932	64	23
1933	64	10
1934	64	13
1935	64	7
1936	64	20
1937	65	29
1938	65	35
1939	65	18
1940	65	10
1941	65	20
1942	65	7
1943	65	22
1944	65	19
1945	66	20
1946	66	16
1947	66	22
1948	66	15
1949	66	24
1950	66	23
1951	66	36
1952	66	17
1953	66	21
1954	66	37
1955	66	27
1956	66	7
1957	66	9
1958	66	26
1959	66	11
1960	66	19
1961	66	28
1962	66	29
1963	66	29
1964	66	33
1965	66	32
1966	66	8
1967	66	18
1968	66	14
1969	66	35
1970	66	25
1971	67	37
1972	67	8
1973	67	28
1974	67	34
1975	67	12
1976	67	24
1977	67	10
1978	67	13
1979	67	7
1980	67	15
1981	67	29
1982	67	26
1983	68	35
1984	68	13
1985	68	12
1986	68	36
1987	68	33
1988	68	14
1989	68	19
1990	68	31
1991	68	17
1992	68	8
1993	68	10
1994	68	22
1995	68	34
1996	68	27
1997	68	25
1998	68	29
1999	68	24
2000	68	16
2001	68	23
2002	68	29
2003	68	28
2004	68	18
2005	68	21
2006	68	7
2007	68	9
2008	68	37
2009	68	32
2010	68	26
2011	6	28
2012	6	23
2013	6	35
2014	6	33
2015	6	18
2016	7	7
2017	7	12
2018	7	17
2019	7	21
2020	7	25
2021	7	16
2022	7	26
2023	7	33
2024	7	8
2025	7	36
2026	7	28
2027	7	13
2028	7	37
2029	7	18
2030	7	23
2031	7	10
2032	7	31
2033	7	27
2034	7	29
2035	7	14
2036	7	34
2037	7	32
2038	7	9
2039	9	29
2040	9	7
2041	9	35
2042	9	31
2043	9	17
2044	9	27
2045	9	11
2046	9	23
2047	13	22
2048	13	34
2049	13	36
2050	13	13
2051	13	15
2052	13	32
2053	13	23
2054	13	37
2055	13	14
2056	13	24
2057	13	18
2058	13	27
2059	13	9
2060	13	7
2061	13	21
2062	13	16
2063	13	25
2064	13	17
2065	13	28
2066	13	20
2067	13	29
2068	13	19
2069	13	31
2070	13	11
2071	14	22
2072	14	12
2073	14	23
2074	14	15
2075	14	37
2076	14	13
2077	14	25
2078	14	21
2079	14	14
2080	14	18
2081	14	26
2082	14	8
2083	14	7
2084	14	29
2085	14	27
2086	14	32
2087	14	28
2088	14	36
2089	14	16
2090	14	24
2091	14	29
2092	14	10
2093	14	34
2094	14	20
2095	14	19
2096	18	13
2097	18	11
2098	18	15
2099	18	28
2100	22	20
2101	22	17
2102	22	12
2103	22	22
2104	22	18
2105	22	25
2106	22	10
2107	22	8
2108	22	16
2109	22	29
2110	25	8
2111	25	26
2112	25	32
2113	25	36
2114	25	16
2115	25	10
2116	25	19
2117	25	34
2118	25	7
2119	25	11
2120	25	13
2121	25	25
2122	25	27
2123	25	31
2124	25	20
2125	25	18
2126	25	29
2127	25	9
2128	25	14
2129	25	12
2130	25	22
2131	25	35
2132	25	24
2133	25	17
2134	25	28
2135	25	37
2136	31	36
2137	31	12
2138	31	32
2139	31	20
2140	31	11
2141	31	31
2142	31	18
2143	31	22
2144	31	33
2145	31	34
2146	31	9
2147	31	13
2148	31	19
2149	31	23
2150	31	17
2151	31	26
2152	33	25
2153	33	18
2154	33	24
2155	33	14
2156	33	36
2157	33	11
2158	33	31
2159	33	17
2160	33	8
2161	33	27
2162	33	21
2163	33	28
2164	33	35
2165	33	23
2166	33	15
2167	33	37
2168	37	32
2169	37	11
2170	37	31
2171	37	37
2172	37	8
2173	37	21
2174	37	19
2175	37	17
2176	37	29
2177	37	10
2178	37	22
2179	37	34
2180	37	14
2181	37	12
2182	37	7
2183	37	29
2184	37	23
2185	37	26
2186	37	18
2187	37	33
2188	37	13
2189	38	35
2190	38	21
2191	38	9
2192	38	18
2193	38	29
2194	38	8
2195	43	34
2196	43	33
2197	43	15
2198	43	7
2199	43	10
2200	43	24
2201	43	28
2202	43	21
2203	43	37
2204	43	11
2205	43	23
2206	43	27
2207	43	17
2208	43	20
2209	43	9
2210	45	37
2211	45	34
2212	45	20
2213	45	33
2214	45	27
2215	45	29
2216	45	9
2217	45	23
2218	45	36
2219	45	14
2220	45	16
2221	45	12
2222	45	25
2223	45	19
2224	45	7
2225	45	32
2226	45	18
2227	45	13
2228	45	26
2229	45	35
2230	45	31
2231	45	8
2232	45	10
2233	45	17
2234	45	11
2235	45	22
2236	45	15
2237	45	24
2238	48	13
2239	48	25
2240	48	28
2241	48	36
2242	48	26
2243	48	8
2244	48	29
2245	48	12
2246	48	7
2247	48	23
2248	48	32
2249	48	21
2250	48	31
2251	48	37
2252	52	15
2253	52	32
2254	52	18
2255	52	16
2256	52	28
2257	53	16
2258	53	7
2259	53	23
2260	53	33
2261	53	28
2262	53	31
2263	53	9
2264	53	29
2265	53	34
2266	53	29
2267	53	19
2268	53	17
2269	69	17
2270	69	19
2271	69	21
2272	69	37
2273	69	29
2274	69	24
2275	69	26
2276	69	11
2277	69	22
2278	69	33
2279	69	15
2280	69	27
2281	69	28
2282	69	18
2283	69	13
2284	69	34
2285	69	31
2286	69	8
2287	69	20
2288	69	14
2289	69	23
2290	69	7
2291	69	29
2292	69	32
2293	69	25
\.


--
-- Name: seen_arguments_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('seen_arguments_uid_seq', 2293, true);


--
-- Data for Name: seen_statements; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY seen_statements (uid, statement_uid, user_uid) FROM stdin;
1524	1	27
1525	1	20
1526	1	21
1527	1	10
1528	1	37
1529	1	23
1530	1	14
1531	1	32
1532	1	29
1533	1	34
1534	1	25
1535	1	36
1536	1	18
1537	1	8
1538	1	15
1539	1	16
1540	1	31
1541	1	24
1542	1	29
1543	1	26
1544	2	11
1545	2	27
1546	2	17
1547	2	33
1548	2	8
1549	2	22
1550	2	12
1551	2	21
1552	2	7
1553	2	14
1554	2	26
1555	2	29
1556	2	24
1557	2	9
1558	2	13
1559	2	10
1560	2	15
1561	2	37
1562	2	23
1563	2	31
1564	2	32
1565	3	37
1566	3	23
1567	3	20
1568	3	18
1569	3	21
1570	3	13
1571	3	25
1572	3	16
1573	3	14
1574	3	12
1575	3	29
1576	3	15
1577	3	19
1578	3	7
1579	3	22
1580	3	33
1581	3	27
1582	3	35
1583	3	24
1584	3	17
1585	3	32
1586	3	10
1587	3	36
1588	3	34
1589	3	8
1590	3	31
1591	3	28
1592	3	9
1593	4	26
1594	4	20
1595	4	33
1596	4	28
1597	4	18
1598	4	25
1599	4	9
1600	4	7
1601	4	21
1602	4	8
1603	4	15
1604	4	13
1605	4	34
1606	4	27
1607	4	29
1608	4	36
1609	4	11
1610	4	10
1611	4	35
1612	4	12
1613	4	24
1614	4	37
1615	4	31
1616	4	14
1617	4	23
1618	5	32
1619	5	19
1620	5	22
1621	5	31
1622	5	24
1623	5	29
1624	5	35
1625	6	31
1626	6	12
1627	6	33
1628	6	16
1629	6	36
1630	6	14
1631	6	35
1632	6	18
1633	6	32
1634	6	24
1635	6	34
1636	6	19
1637	6	37
1638	6	25
1639	6	22
1640	6	15
1641	6	17
1642	6	9
1643	6	10
1644	6	29
1645	6	21
1646	6	26
1647	6	23
1648	6	7
1649	6	8
1650	6	13
1651	6	11
1652	6	20
1653	7	12
1654	7	32
1655	7	29
1656	7	23
1657	7	22
1658	7	7
1659	7	34
1660	7	16
1661	7	27
1662	7	26
1663	7	37
1664	7	10
1665	7	14
1666	8	15
1667	8	28
1668	8	34
1669	8	35
1670	8	16
1671	8	29
1672	9	36
1673	9	34
1674	9	10
1675	9	17
1676	9	12
1677	9	37
1678	9	23
1679	9	26
1680	9	33
1681	9	18
1682	9	35
1683	9	22
1684	9	9
1685	9	14
1686	9	32
1687	9	27
1688	9	28
1689	9	8
1690	9	31
1691	9	16
1692	9	29
1693	9	20
1694	9	21
1695	9	13
1696	9	19
1697	9	11
1698	9	15
1699	9	29
1700	9	24
1701	10	21
1702	10	18
1703	10	29
1704	10	8
1705	10	29
1706	11	29
1707	11	15
1708	11	29
1709	11	13
1710	11	10
1711	11	21
1712	11	19
1713	11	32
1714	11	37
1715	11	22
1716	11	24
1717	11	18
1718	11	12
1719	11	26
1720	11	36
1721	11	23
1722	11	33
1723	11	8
1724	11	14
1725	11	9
1726	11	27
1727	12	27
1728	12	33
1729	12	29
1730	12	9
1731	12	19
1732	12	34
1733	12	15
1734	12	13
1735	12	37
1736	12	12
1737	12	7
1738	12	23
1739	12	36
1740	12	26
1741	12	24
1742	12	31
1743	12	22
1744	12	28
1745	12	18
1746	12	8
1747	12	11
1748	12	14
1749	12	16
1750	13	32
1751	13	11
1752	13	9
1753	13	31
1754	13	12
1755	13	10
1756	13	21
1757	14	36
1758	14	8
1759	14	33
1760	14	34
1761	14	10
1762	14	24
1763	14	22
1764	14	29
1765	14	16
1766	14	15
1767	14	19
1768	14	13
1769	14	12
1770	14	37
1771	14	9
1772	14	20
1773	15	11
1774	15	35
1775	15	13
1776	15	9
1777	15	21
1778	15	8
1779	15	12
1780	15	18
1781	15	28
1782	15	24
1783	15	27
1784	15	10
1785	15	19
1786	16	27
1787	16	17
1788	16	12
1789	16	16
1790	16	14
1791	16	8
1792	16	29
1793	16	37
1794	16	7
1795	16	10
1796	16	26
1797	16	21
1798	16	28
1799	16	32
1800	16	36
1801	16	34
1802	16	9
1803	16	18
1804	17	28
1805	17	36
1806	17	16
1807	17	11
1808	17	29
1809	17	32
1810	17	23
1811	17	17
1812	17	8
1813	18	24
1814	18	27
1815	18	21
1816	18	13
1817	18	23
1818	18	20
1819	18	28
1820	18	29
1821	18	18
1822	18	36
1823	19	22
1824	19	29
1825	19	19
1826	19	20
1827	19	25
1828	19	21
1829	19	16
1830	19	29
1831	19	26
1832	19	17
1833	19	23
1834	19	15
1835	19	35
1836	19	33
1837	19	27
1838	19	37
1839	20	37
1840	20	34
1841	20	27
1842	20	22
1843	20	11
1844	20	36
1845	20	10
1846	20	24
1847	20	35
1848	20	32
1849	20	7
1850	20	25
1851	20	17
1852	21	11
1853	21	10
1854	21	14
1855	21	28
1856	21	34
1857	21	31
1858	22	22
1859	22	21
1860	22	33
1861	22	12
1862	22	23
1863	22	16
1864	22	20
1865	22	7
1866	22	35
1867	22	27
1868	22	28
1869	22	19
1870	22	36
1871	22	24
1872	23	20
1873	23	10
1874	23	17
1875	23	7
1876	23	28
1877	23	26
1878	23	14
1879	23	16
1880	23	24
1881	23	33
1882	23	21
1883	23	11
1884	23	19
1885	23	9
1886	23	36
1887	23	34
1888	23	13
1889	23	22
1890	23	27
1891	23	35
1892	23	18
1893	24	20
1894	24	24
1895	24	11
1896	24	9
1897	24	36
1898	24	18
1899	24	17
1900	24	8
1901	24	28
1902	24	12
1903	24	34
1904	24	32
1905	24	13
1906	24	37
1907	24	14
1908	24	10
1909	24	19
1910	24	31
1911	24	15
1912	24	23
1913	24	27
1914	24	29
1915	24	25
1916	24	16
1917	24	21
1918	24	22
1919	24	35
1920	25	28
1921	25	19
1922	25	29
1923	25	29
1924	25	27
1925	25	32
1926	25	33
1927	25	11
1928	26	24
1929	26	9
1930	26	23
1931	26	19
1932	26	21
1933	26	12
1934	26	20
1935	26	29
1936	26	27
1937	26	36
1938	26	8
1939	26	18
1940	26	26
1941	26	14
1942	26	22
1943	26	28
1944	26	17
1945	26	35
1946	26	13
1947	26	34
1948	26	31
1949	27	37
1950	27	19
1951	27	9
1952	27	8
1953	27	16
1954	27	25
1955	27	33
1956	27	26
1957	27	31
1958	27	11
1959	27	27
1960	27	28
1961	27	35
1962	27	10
1963	27	21
1964	27	20
1965	28	26
1966	28	27
1967	28	31
1968	28	24
1969	28	17
1970	28	28
1971	28	14
1972	28	20
1973	28	12
1974	29	36
1975	29	24
1976	29	11
1977	29	32
1978	29	20
1979	29	26
1980	29	31
1981	29	37
1982	29	13
1983	29	19
1984	29	28
1985	29	33
1986	29	27
1987	29	17
1988	29	8
1989	29	29
1990	29	18
1991	29	14
1992	29	34
1993	29	23
1994	29	35
1995	29	22
1996	29	10
1997	29	15
1998	29	25
1999	29	12
2000	30	20
2001	30	18
2002	30	34
2003	30	25
2004	30	28
2005	30	24
2006	30	15
2007	30	26
2008	30	23
2009	30	29
2010	30	8
2011	30	29
2012	30	13
2013	30	36
2014	30	19
2015	30	9
2016	30	11
2017	30	27
2018	30	37
2019	30	33
2020	31	24
2021	31	9
2022	31	31
2023	31	7
2024	31	32
2025	31	8
2026	31	13
2027	31	16
2028	31	37
2029	31	33
2030	31	35
2031	31	21
2032	31	22
2033	31	10
2034	31	28
2035	31	14
2036	31	36
2037	31	29
2038	31	11
2039	31	18
2040	31	19
2041	32	28
2042	32	16
2043	32	20
2044	32	34
2045	32	32
2046	32	22
2047	32	23
2048	32	19
2049	32	35
2050	32	8
2051	32	10
2052	32	15
2053	32	21
2054	32	14
2055	32	17
2056	33	13
2057	33	15
2058	33	23
2059	33	25
2060	33	27
2061	33	22
2062	33	7
2063	33	37
2064	33	14
2065	33	24
2066	33	18
2067	33	32
2068	33	35
2069	33	29
2070	33	28
2071	33	10
2072	33	33
2073	33	26
2074	33	8
2075	33	20
2076	33	9
2077	33	21
2078	33	31
2079	33	16
2080	34	28
2081	34	35
2082	34	33
2083	34	29
2084	34	10
2085	34	23
2086	34	7
2087	34	14
2088	34	37
2089	34	12
2090	34	29
2091	35	15
2092	35	18
2093	35	27
2094	35	33
2095	35	19
2096	35	28
2097	35	16
2098	35	20
2099	35	37
2100	35	17
2101	35	34
2102	35	31
2103	35	29
2104	36	29
2105	36	35
2106	36	34
2107	36	25
2108	36	28
2109	36	17
2110	36	24
2111	36	20
2112	36	31
2113	36	11
2114	36	23
2115	37	12
2116	37	11
2117	37	29
2118	37	28
2119	37	34
2120	37	25
2121	37	21
2122	37	37
2123	37	33
2124	37	32
2125	37	13
2126	37	26
2127	37	27
2128	37	16
2129	37	9
2130	37	19
2131	37	15
2132	37	22
2133	37	24
2134	38	9
2135	38	19
2136	38	32
2137	38	11
2138	39	31
2139	39	33
2140	39	27
2141	39	12
2142	39	9
2143	39	11
2144	39	14
2145	39	13
2146	39	25
2147	39	18
2148	39	19
2149	39	22
2150	39	17
2151	39	29
2152	39	20
2153	40	15
2154	40	12
2155	40	17
2156	40	24
2157	40	20
2158	40	35
2159	40	19
2160	40	10
2161	40	14
2162	40	18
2163	40	34
2164	40	26
2165	40	32
2166	40	25
2167	40	33
2168	40	21
2169	41	24
2170	41	9
2171	41	25
2172	41	31
2173	41	28
2174	41	37
2175	41	22
2176	41	29
2177	41	13
2178	41	32
2179	41	16
2180	41	14
2181	41	18
2182	42	11
2183	42	17
2184	42	13
2185	42	18
2186	42	33
2187	43	12
2188	43	21
2189	43	22
2190	43	18
2191	43	24
2192	43	36
2193	43	35
2194	43	19
2195	43	9
2196	43	28
2197	43	16
2198	43	27
2199	43	37
2200	43	15
2201	43	29
2202	43	33
2203	43	23
2204	43	8
2205	43	7
2206	43	20
2207	44	23
2208	44	29
2209	44	8
2210	44	14
2211	44	27
2212	44	37
2213	44	32
2214	44	31
2215	44	11
2216	45	14
2217	45	15
2218	45	37
2219	45	32
2220	45	19
2221	45	24
2222	45	16
2223	45	11
2224	45	10
2225	45	35
2226	45	29
2227	45	8
2228	45	36
2229	45	25
2230	45	26
2231	45	23
2232	45	22
2233	45	7
2234	45	12
2235	45	33
2236	45	13
2237	46	12
2238	46	15
2239	46	22
2240	46	23
2241	46	32
2242	46	24
2243	46	21
2244	46	31
2245	46	19
2246	46	34
2247	46	8
2248	46	27
2249	46	25
2250	46	16
2251	46	11
2252	46	26
2253	46	35
2254	46	20
2255	46	36
2256	46	29
2257	46	18
2258	46	13
2259	46	17
2260	46	10
2261	46	33
2262	47	7
2263	47	14
2264	47	32
2265	47	29
2266	47	21
2267	47	35
2268	47	18
2269	47	19
2270	47	16
2271	47	23
2272	47	33
2273	47	12
2274	47	20
2275	47	11
2276	48	20
2277	48	34
2278	48	28
2279	48	15
2280	48	7
2281	48	26
2282	48	10
2283	48	29
2284	48	37
2285	48	9
2286	48	14
2287	48	16
2288	48	23
2289	48	29
2290	48	12
2291	48	25
2292	48	11
2293	48	33
2294	48	19
2295	48	31
2296	48	18
2297	48	8
2298	48	17
2299	48	32
2300	49	26
2301	49	28
2302	49	27
2303	49	33
2304	49	8
2305	49	29
2306	49	36
2307	49	21
2308	49	29
2309	49	16
2310	49	32
2311	49	10
2312	49	34
2313	49	37
2314	50	32
2315	50	31
2316	50	18
2317	50	10
2318	50	29
2319	50	26
2320	50	33
2321	50	28
2322	50	25
2323	50	15
2324	50	13
2325	50	19
2326	50	37
2327	50	27
2328	50	34
2329	50	29
2330	50	17
2331	50	20
2332	50	12
2333	50	11
2334	50	36
2335	50	7
2336	50	23
2337	50	24
2338	50	16
2339	50	14
2340	50	35
2341	50	21
2342	50	9
2343	51	23
2344	51	37
2345	51	12
2346	51	10
2347	51	15
2348	51	32
2349	51	27
2350	51	19
2351	51	14
2352	51	20
2353	51	35
2354	51	17
2355	51	34
2356	51	11
2357	51	22
2358	51	24
2359	51	16
2360	51	25
2361	51	9
2362	52	27
2363	52	7
2364	52	25
2365	52	15
2366	52	9
2367	52	19
2368	52	21
2369	52	37
2370	52	24
2371	52	13
2372	53	23
2373	53	9
2374	53	21
2375	53	11
2376	53	19
2377	53	13
2378	53	25
2379	53	16
2380	53	31
2381	53	34
2382	53	20
2383	53	29
2384	53	29
2385	53	28
2386	53	8
2387	53	27
2388	53	7
2389	53	22
2390	53	14
2391	53	32
2392	53	26
2393	53	15
2394	54	12
2395	54	11
2396	54	33
2397	54	34
2398	54	35
2399	54	20
2400	54	8
2401	54	7
2402	54	25
2403	54	32
2404	54	17
2405	54	18
2406	54	29
2407	54	10
2408	54	23
2409	54	13
2410	54	31
2411	54	21
2412	54	15
2413	54	37
2414	54	16
2415	54	9
2416	54	19
2417	54	14
2418	55	35
2419	55	20
2420	55	26
2421	55	7
2422	55	24
2423	55	25
2424	55	8
2425	56	33
2426	56	18
2427	56	10
2428	56	16
2429	56	37
2430	56	7
2431	56	9
2432	56	24
2433	56	34
2434	56	29
2435	57	31
2436	57	29
2437	57	21
2438	57	11
2439	57	16
2440	57	8
2441	57	34
2442	57	27
2443	57	37
2444	57	17
2445	57	26
2446	57	18
2447	57	13
2448	57	10
2449	57	23
2450	57	15
2451	58	16
2452	58	23
2453	58	20
2454	58	19
2455	58	9
2456	58	34
2457	58	29
2458	58	21
2459	58	26
2460	58	28
2461	58	17
2462	58	29
2463	59	15
2464	59	27
2465	59	17
2466	59	11
2467	59	20
2468	59	36
2469	59	33
2470	59	37
2471	59	34
2472	59	9
2473	59	32
2474	59	14
2475	59	12
2476	59	29
2477	59	13
2478	59	23
2479	60	24
2480	60	15
2481	60	26
2482	60	32
2483	60	33
2484	60	27
2485	60	20
2486	60	12
2487	60	35
2488	60	36
2489	60	19
2490	60	34
2491	61	16
2492	61	26
2493	61	35
2494	61	8
2495	61	10
2496	61	22
2497	61	34
2498	61	31
2499	61	25
2500	61	27
2501	61	18
2502	61	36
2503	61	20
2504	61	12
2505	61	14
2506	61	7
2507	61	32
2508	61	37
2509	61	19
2510	61	29
2511	61	29
2512	61	13
2513	62	27
2514	62	16
2515	62	7
2516	62	31
2517	62	26
2518	62	11
2519	62	13
2520	62	29
2521	62	14
2522	62	28
2523	62	9
2524	62	19
2525	62	34
2526	62	35
2527	62	10
2528	62	24
2529	62	23
2530	62	36
2531	62	37
2532	62	32
2533	62	12
2534	62	17
2535	62	25
2536	62	22
2537	62	15
2538	62	29
2539	62	21
2540	63	19
2541	63	33
2542	63	37
2543	63	36
2544	64	15
2545	64	12
2546	64	21
2547	64	29
2548	64	27
2549	64	36
2550	64	23
2551	64	22
2552	65	16
2553	65	37
2554	65	31
2555	65	27
2556	65	23
2557	65	22
2558	65	21
2559	65	35
2560	65	33
2561	65	13
2562	65	8
2563	65	9
2564	65	11
2565	65	24
2566	65	19
2567	65	28
2568	65	29
2569	65	29
2570	65	32
2571	65	25
2572	65	36
2573	65	26
2574	65	7
2575	65	20
2576	65	34
2577	65	12
2578	66	8
2579	66	28
2580	66	23
2581	66	36
2582	66	11
2583	67	26
2584	67	19
2585	67	25
2586	67	10
2587	67	35
2588	67	27
2589	67	20
2590	67	9
2591	67	31
2592	67	21
2593	67	18
2594	67	11
2595	67	28
2596	67	37
2597	67	8
2598	67	33
2599	67	13
2600	67	15
2601	67	34
2602	67	29
2603	67	14
2604	67	23
2605	67	32
2606	67	36
2607	67	24
2608	67	22
2609	67	16
2610	67	7
2611	68	13
2612	68	9
2613	68	12
2614	68	14
2615	68	31
2616	68	37
2617	68	26
2618	68	35
2619	68	16
2620	68	18
2621	68	15
2622	68	11
2623	68	28
2624	68	8
2625	68	7
2626	68	36
2627	68	23
2628	68	25
2629	69	19
2630	69	10
2631	69	34
2632	69	15
2633	69	23
2634	69	21
2635	69	7
2636	69	22
2637	69	27
2638	69	12
2639	69	13
2640	69	28
2641	70	33
2642	70	31
2643	70	12
2644	70	15
2645	70	9
2646	70	16
2647	70	14
2648	70	29
2649	70	32
2650	70	35
2651	70	24
2652	70	28
2653	70	13
2654	70	26
2655	70	23
2656	70	21
2657	70	29
2658	70	34
2659	71	21
2660	71	11
2661	71	13
2662	71	7
2663	71	19
2664	71	22
2665	71	24
2666	71	14
2667	71	27
2668	71	35
2669	71	17
2670	71	18
2671	71	23
2672	71	20
2673	71	34
2674	71	37
2675	71	15
2676	71	36
2677	71	8
2678	71	31
2679	72	36
2680	72	26
2681	72	17
2682	72	33
2683	72	16
2684	72	18
2685	72	19
2686	72	14
2687	72	21
2688	72	37
2689	72	29
2690	72	31
2691	72	29
2692	72	9
2693	72	35
2694	72	13
2695	72	12
2696	72	24
2697	72	34
2698	72	15
2699	72	11
2700	72	28
2701	72	23
2702	72	8
2703	72	20
2704	72	10
2705	72	32
2706	73	14
2707	73	21
2708	73	13
2709	73	25
2710	73	8
2711	73	15
2712	73	26
2713	73	36
2714	73	22
2715	73	24
2716	73	11
2717	73	31
2718	73	12
2719	73	7
2720	73	17
2721	73	27
2722	73	19
2723	73	10
2724	73	16
2725	73	35
2726	73	29
2727	74	20
2728	74	32
2729	74	28
2730	74	29
2731	74	18
2732	74	36
2733	74	22
2734	74	16
2735	74	23
2736	74	17
2737	74	31
2738	74	14
2739	74	13
2740	74	24
2741	74	29
2742	74	35
2743	74	11
2744	74	7
2745	74	19
2746	74	12
2747	75	24
2748	75	25
2749	75	20
2750	75	37
2751	75	18
2752	75	16
2753	75	27
2754	75	12
2755	75	9
2756	75	15
2757	75	22
2758	75	21
2759	75	19
2760	75	7
2761	76	35
2762	76	18
2763	76	28
2764	76	37
2765	76	10
2766	76	9
2767	76	19
2768	76	29
2769	76	12
2770	76	14
2771	76	21
2772	76	26
2773	76	20
2774	76	32
2775	76	29
2776	76	27
2777	76	16
2778	76	24
2779	76	25
2780	76	13
2781	76	11
2782	76	36
2783	76	17
2784	76	33
2785	77	32
2786	77	21
2787	77	26
2788	77	9
2789	77	23
2790	77	35
2791	77	29
2792	77	28
2793	77	13
2794	77	31
2795	77	16
2796	77	36
2797	77	37
2798	77	34
2799	77	25
2800	77	7
2801	77	27
2802	77	14
2803	77	10
2804	78	17
2805	78	35
2806	78	21
2807	78	37
2808	78	15
2809	78	29
2810	78	25
2811	78	28
2812	78	20
2813	78	16
2814	78	12
2815	78	11
2816	78	33
2817	78	19
2818	78	29
2819	78	8
2820	78	22
2821	79	37
2822	79	11
2823	79	23
2824	79	15
2825	79	13
2826	79	14
2827	79	16
2828	79	24
2829	79	21
2830	79	22
2831	79	19
2832	79	18
2833	79	10
2834	80	18
2835	80	7
2836	80	13
2837	80	33
2838	80	25
2839	80	32
2840	80	22
2841	80	15
2842	80	10
2843	80	14
2844	80	17
2845	80	21
2846	80	19
2847	80	29
2848	80	36
2849	80	34
2850	80	27
2851	80	8
2852	80	16
2853	80	26
2854	80	28
2855	80	11
2856	80	23
2857	80	9
2858	81	25
2859	81	31
2860	81	32
2861	81	27
2862	81	22
2863	81	37
2864	81	34
2865	81	29
2866	81	28
2867	81	10
2868	81	7
2869	81	23
2870	82	31
2871	82	7
2872	82	12
2873	82	24
2874	82	19
2875	82	34
2876	82	37
2877	82	21
2878	82	14
2879	82	15
2880	82	22
\.


--
-- Name: seen_statements_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('seen_statements_uid_seq', 2880, true);


--
-- Data for Name: settings; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY settings (author_uid, should_send_mails, should_send_notifications, should_show_public_nickname, last_topic_uid, lang_uid, keep_logged_in) FROM stdin;
1	f	t	t	1	2	f
2	f	t	t	1	2	f
3	f	t	t	1	2	f
4	f	t	t	1	2	f
5	f	t	t	1	2	f
6	f	t	t	1	2	f
7	f	t	t	1	2	f
8	f	t	t	1	2	f
9	f	t	t	1	2	f
10	f	t	t	1	2	f
11	f	t	f	1	2	f
12	f	t	f	1	2	f
13	f	t	f	1	2	f
14	f	t	f	1	2	f
15	f	t	f	1	2	f
16	f	t	f	1	2	f
17	f	t	f	1	2	f
18	f	t	f	1	2	f
19	f	t	f	1	2	f
20	f	t	f	1	2	f
21	f	t	f	1	2	f
22	f	t	t	1	2	f
23	f	t	t	1	2	f
24	f	t	t	1	2	f
25	f	t	t	1	2	f
26	f	t	t	1	2	f
27	f	t	t	1	2	f
28	f	t	t	1	2	f
29	f	t	t	1	2	f
30	f	t	t	1	2	f
31	f	t	t	1	2	f
32	f	t	t	1	2	f
33	f	t	t	1	2	f
34	f	t	t	1	2	f
35	f	t	t	1	2	f
36	f	t	t	1	2	f
37	f	t	t	1	2	f
\.


--
-- Data for Name: statement_references; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY statement_references (uid, reference, host, path, author_uid, statement_uid, issue_uid, created) FROM stdin;
1	Ein Radar überwacht den Abstand, eine Frontkamera erkennt Fahrspuren und andere Verkehrsteilnehmer, und je sechs Ultraschallsensoren vorne und hinten helfen beim Einparken und messen während der Fahrt Distanzen im Zentimeterbereich	localhost:3449	/devcards/index.html	5	68	4	2017-08-17 11:57:14.378552
2	Zunächst einmal unterscheidet sich die Hardware für den Autopiloten nicht oder nur marginal von dem, was selbst für einen VW Polo erhältlich ist	localhost:3449	/	5	68	4	2017-08-17 11:57:14.378552
3	Katzen sind kleine Tiger	http://www.iflscience.com/	plants-and-animals/no-your-cat-isnt-plotting-kill-youbut-it-has-lions-personality/	2	15	2	2017-08-17 11:57:14.378552
4	Katzen sind kleine Tiger	http://www.iflscience.com/	plants-and-animals/no-your-cat-isnt-plotting-kill-youbut-it-has-lions-personality/	2	16	2	2017-08-17 11:57:14.378552
\.


--
-- Name: statement_references_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('statement_references_uid_seq', 4, true);


--
-- Data for Name: statements; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY statements (uid, textversion_uid, is_startpoint, issue_uid, is_disabled) FROM stdin;
1	75	t	2	t
2	1	t	2	f
3	2	t	2	f
4	3	t	2	f
5	4	f	2	f
6	5	f	2	f
7	6	f	2	f
8	7	f	2	f
9	8	f	2	f
10	9	f	2	f
11	10	f	2	f
12	11	f	2	f
13	12	f	2	f
14	13	f	2	f
15	14	f	2	f
16	15	f	2	f
17	16	f	2	f
18	17	f	2	f
19	18	f	2	f
20	19	f	2	f
21	20	f	2	f
22	21	f	2	f
23	22	f	2	f
24	23	f	2	f
25	24	f	2	f
26	25	f	2	f
27	26	f	2	f
28	27	f	2	f
29	28	f	2	f
30	29	f	2	f
31	30	f	2	f
32	31	f	2	f
33	32	f	2	f
34	33	f	2	f
35	34	f	2	f
36	35	t	1	f
37	36	t	1	f
38	37	t	1	f
39	38	f	1	f
40	39	f	1	f
41	40	f	1	f
42	41	f	1	f
43	42	f	1	f
44	43	f	1	f
45	44	f	1	f
46	45	f	1	f
47	46	f	1	f
48	47	f	1	f
49	48	f	1	f
50	49	f	1	f
51	50	f	1	f
52	51	f	1	f
53	52	f	1	f
54	53	f	1	f
55	54	f	1	f
56	55	f	1	f
57	56	f	1	f
58	57	t	4	f
59	58	f	4	f
60	59	f	4	f
61	60	f	4	f
62	61	f	4	f
63	62	f	4	f
64	63	f	4	f
65	64	f	4	f
66	65	f	4	f
67	66	t	4	f
68	67	f	4	f
69	68	t	5	f
70	69	t	5	f
71	70	f	5	f
72	71	f	5	f
73	72	f	5	f
74	73	f	5	f
75	74	f	5	f
76	76	t	7	f
77	77	f	7	f
78	78	f	7	f
79	79	f	7	f
80	80	f	7	f
81	81	f	7	f
82	82	f	7	f
\.


--
-- Name: statements_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('statements_uid_seq', 82, true);


--
-- Data for Name: textversions; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY textversions (uid, statement_uid, content, author_uid, "timestamp", is_disabled) FROM stdin;
1	2	we should get a cat	1	2017-08-16 11:57:15.156419	f
2	3	we should get a dog	1	2017-07-29 11:57:15.156563	f
3	4	we could get both, a cat and a dog	1	2017-08-07 11:57:15.156617	f
4	5	cats are very independent	1	2017-08-13 11:57:15.156678	f
5	6	cats are capricious	1	2017-08-09 11:57:15.156734	f
6	7	dogs can act as watch dogs	1	2017-08-05 11:57:15.156798	f
7	8	you have to take the dog for a walk every day, which is tedious	1	2017-07-28 11:57:15.156861	f
8	9	we have no use for a watch dog	1	2017-08-14 11:57:15.156929	f
9	10	going for a walk with the dog every day is good for social interaction and physical exercise	1	2017-08-07 11:57:15.15699	f
10	11	it would be no problem	1	2017-07-23 11:57:15.157053	f
11	12	a cat and a dog will generally not get along well	1	2017-08-17 11:57:15.157115	f
12	13	we do not have enough money for two pets	1	2017-08-10 11:57:15.157171	f
13	14	a dog costs taxes and will be more expensive than a cat	1	2017-08-10 11:57:15.157213	f
14	15	cats are fluffy	1	2017-08-14 11:57:15.15725	f
15	16	cats are small	1	2017-08-12 11:57:15.157287	f
16	17	fluffy animals losing much hair and I'm allergic to animal hair	1	2017-07-31 11:57:15.157324	f
17	18	you could use a automatic vacuum cleaner	1	2017-08-14 11:57:15.157361	f
18	19	cats ancestors are animals in wildlife, who are hunting alone and not in groups	1	2017-08-15 11:57:15.157398	f
19	20	this is not true for overbred races	1	2017-08-05 11:57:15.157435	f
20	21	this lies in their the natural conditions	1	2017-08-16 11:57:15.15747	f
21	22	the purpose of a pet is to have something to take care of	1	2017-08-14 11:57:15.157506	f
22	23	several cats of friends of mine are real as*holes	1	2017-08-11 11:57:15.157542	f
23	24	the fact, that cats are capricious, is based on the cats race	1	2017-07-29 11:57:15.157578	f
24	25	not every cat is capricious	1	2017-08-05 11:57:15.157614	f
25	26	this is based on the cats race and a little bit on the breeding	1	2017-07-29 11:57:15.157651	f
26	27	next to the taxes you will need equipment like a dog lead, anti-flea-spray, and so on	1	2017-07-23 11:57:15.157687	f
27	28	the equipment for running costs of cats and dogs are nearly the same	1	2017-08-11 11:57:15.157724	f
28	29	this is just a claim without any justification	1	2017-07-23 11:57:15.15776	f
29	30	in Germany you have to pay for your second dog even more taxes!	1	2017-08-09 11:57:15.157796	f
30	31	it is important, that pets are small and fluffy!	1	2017-07-26 11:57:15.157832	f
31	32	cats are little, sweet and innocent cuddle toys	1	2017-07-26 11:57:15.157892	f
32	33	do you have ever seen a sphinx cat or savannah cats?	1	2017-08-07 11:57:15.15793	f
33	34	it is much work to take care of both animals	1	2017-08-04 11:57:15.157966	f
34	35	won't be best friends	1	2017-07-27 11:57:15.158002	f
35	36	the city should reduce the number of street festivals	3	2017-07-30 11:57:15.158039	f
36	37	we should shut down University Park	3	2017-08-16 11:57:15.158076	f
37	38	we should close public swimming pools	1	2017-08-16 11:57:15.158112	f
38	39	reducing the number of street festivals can save up to $50.000 a year	1	2017-08-15 11:57:15.158147	f
39	40	every street festival is funded by large companies	1	2017-07-23 11:57:15.158183	f
40	41	then we will have more money to expand out pedestrian zone	1	2017-08-01 11:57:15.158218	f
41	42	our city will get more attractive for shopping	1	2017-07-26 11:57:15.158253	f
42	43	street festivals attract many people, which will increase the citys income	1	2017-08-03 11:57:15.158287	f
43	44	spending of the city for these festivals are higher than the earnings	1	2017-08-12 11:57:15.158322	f
44	45	money does not solve problems of our society	1	2017-08-04 11:57:15.158358	f
45	46	criminals use University Park to sell drugs	1	2017-07-25 11:57:15.158393	f
46	47	shutting down University Park will save $100.000 a year	1	2017-08-11 11:57:15.158429	f
47	48	we should not give in to criminals	1	2017-08-05 11:57:15.158464	f
48	49	the number of police patrols has been increased recently	1	2017-08-09 11:57:15.158499	f
49	50	this is the only park in our city	1	2017-08-17 11:57:15.158534	f
50	51	there are many parks in neighbouring towns	1	2017-08-02 11:57:15.158569	f
51	52	the city is planing a new park in the upcoming month	3	2017-08-16 11:57:15.158605	f
52	53	parks are very important for our climate	3	2017-08-08 11:57:15.15864	f
53	54	our swimming pools are very old and it would take a major investment to repair them	3	2017-08-11 11:57:15.158676	f
54	55	schools need the swimming pools for their sports lessons	1	2017-08-14 11:57:15.158711	f
55	56	the rate of non-swimmers is too high	1	2017-08-07 11:57:15.158746	f
56	57	the police cannot patrol in the park for 24/7	1	2017-08-01 11:57:15.158782	f
57	58	E-Autos "optimal" für den Stadtverkehr sind	1	2017-08-05 11:57:15.158818	f
58	59	dadurch die Lärmbelästigung in der Stadt sinkt	1	2017-08-08 11:57:15.158853	f
77	77	Straßenfeste viel Lärm verursachen	1	2017-08-14 11:57:15.159533	f
59	60	die Anzahl an Ladestationen in der Stadt nicht ausreichend ist	1	2017-07-30 11:57:15.158888	f
60	61	das Unfallrisiko steigt, da die Autos kaum Geräusche verursachen	1	2017-08-02 11:57:15.158924	f
61	62	die Autos auch zuhause geladen werden können und das pro Tag ausreichen sollte	1	2017-08-04 11:57:15.15896	f
62	63	Elektroautos keine lauten Geräusche beim Anfahren produzieren	1	2017-08-17 11:57:15.158995	f
63	64	Lärmbelästigung kein wirkliches Problem in den Städten ist	1	2017-07-27 11:57:15.15903	f
64	65	nicht jede normale Tankstelle auch Stromtankstellen hat	1	2017-08-05 11:57:15.159066	f
65	66	die Länder und Kommunen den Ausbau nun stark fördern wollen	1	2017-07-31 11:57:15.159102	f
66	67	E-Autos das autonome Fahren vorantreiben	5	2017-08-09 11:57:15.159138	f
67	68	Tesla mutig bestehende Techniken einsetzt und zeigt was sie können	5	2017-07-25 11:57:15.159174	f
68	69	durch rücksichtsvolle Verhaltensanpassungen der wissenschaftlichen Mitarbeitenden der Arbeitsaufwand der Sekretärinnen gesenkt werden könnte	1	2017-07-24 11:57:15.15921	f
69	70	wir Standard-Formulare, wie Urlaubsanträge, selbst faxen können	1	2017-08-07 11:57:15.159245	f
70	71	etliche Abläufe durch ein besseres Zusammenarbeiten optimiert werden können. Dies sollte auch schriftlich als Anleitungen festgehalten werden, damit neue Angestellt einen leichten Einstieg finden	1	2017-07-30 11:57:15.159281	f
71	72	viele Arbeiten auch durch die Mitarbeiter erledigt werden können	1	2017-08-13 11:57:15.159317	f
72	73	"rücksichtsvolle Verhaltensanpassungen" viel zu allgemein gehalten ist	1	2017-08-16 11:57:15.159354	f
73	74	das Faxgerät nicht immer zugänglich ist, wenn die Sekretärinnen nicht anwesend sind	1	2017-08-04 11:57:15.159391	f
74	75	wir keine eigenen Faxgeräte haben und so oder so entweder bei Martin stören müssten oder doch bei Sabine im Büro landen würden	1	2017-08-07 11:57:15.159426	f
75	1	Cats are fucking stupid and bloody fuzzy critters!	1	2017-08-10 11:57:15.159462	f
76	76	Die Anzahl der Straßenfeste sollte reduziert werden	1	2017-08-09 11:57:15.159498	f
78	78	Straßenfeste ein wichtiger Bestandteil unserer Kultur sind	1	2017-07-30 11:57:15.159569	f
79	79	Straßenfeste der Kommune Geld einbringen	1	2017-07-27 11:57:15.159604	f
80	80	die Einnahmen der Kommune durch Straßenfeste nur gering sind	1	2017-08-10 11:57:15.15964	f
81	81	Straßenfeste der Kommune hohe Kosten verursachen durch Polizeieinsätze, Säuberung, etc.	1	2017-08-06 11:57:15.159676	f
82	82	die Innenstadt ohnehin sehr laut ist	1	2017-07-23 11:57:15.159711	f
\.


--
-- Name: textversions_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('textversions_uid_seq', 82, true);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY users (uid, firstname, surname, nickname, public_nickname, email, gender, password, group_uid, last_action, last_login, registered, token, token_timestamp) FROM stdin;
1	anonymous	anonymous	anonymous	anonymous		m	$2a$10$vq0iUCoeP37ot3km4VriBOUTx4zw3HzR4mYlG/reVfw1rwVNJAJR.	3	2017-08-17 11:57:14.957296	2017-08-17 11:57:14.957413	2017-08-17 11:57:14.957465		\N
2	Tobias	Krauthoff	Tobias	Tobias	krauthoff@cs.uni-duesseldorf.de	m	$2a$10$9P5biPvyX2xVeMcCLm82tO0XFQhmdMFwgAhPaUkCHoVL1F5kEAjIa	1	2017-08-17 11:57:14.957553	2017-08-17 11:57:14.957603	2017-08-17 11:57:14.957648		\N
3	Christian	Meter	Christian	Christian	meter@cs.uni-duesseldorf.de	m	$2a$10$Ou/pHV1MoZRqvt5U8cV09up0qqbIz70ZjwEeanRkyyfR/rrMHcBfe	1	2017-08-17 11:57:14.957729	2017-08-17 11:57:14.957786	2017-08-17 11:57:14.957832		\N
4	Björn	Ebbinghaus	Björn	Björn	bjoern.ebbinghaus@uni-duesseldorf.de	m	$2a$10$vXBSjqq4Jfil4orAkOTpcO7lHt65zhbIwyZNY2.ITd2VhloxaXZLC	1	2017-08-17 11:57:14.962912	2017-08-17 11:57:14.963004	2017-08-17 11:57:14.963068		\N
5	Teresa	Uebber	Teresa	Teresa	teresa.uebber@uni-duesseldorf.de	f	$2a$10$5kXljZWSRdXWIoKYs6/LgeSboOtPJFdlI0q1ncKvt1QIu1btsEQka	1	2017-08-17 11:57:14.963179	2017-08-17 11:57:14.963245	2017-08-17 11:57:14.963306		\N
6	Bob	Bubbles	Bob	Bob	tobias.krauthoff+dbas.usert31@gmail.com	n	$2a$10$LrQYZZjVzZCJohjNTXawpuM5zH.Tlf8RGfMSqLdCdWWjbAfK/e8/q	1	2017-08-17 11:57:14.963412	2017-08-17 11:57:14.963476	2017-08-17 11:57:14.963536		\N
7	Pascal	Lux	Pascal	Pascal	tobias.krauthoff+dbas.usert00@gmail.com	m	$2a$10$LrQYZZjVzZCJohjNTXawpuM5zH.Tlf8RGfMSqLdCdWWjbAfK/e8/q	3	2017-08-17 11:57:14.963734	2017-08-17 11:57:14.963786	2017-08-17 11:57:14.96383		\N
8	Kurt	Hecht	Kurt	Kurt	tobias.krauthoff+dbas.usert01@gmail.com	m	$2a$10$LrQYZZjVzZCJohjNTXawpuM5zH.Tlf8RGfMSqLdCdWWjbAfK/e8/q	3	2017-08-17 11:57:14.963907	2017-08-17 11:57:14.963954	2017-08-17 11:57:14.963999		\N
9	Torben	Hartl	Torben	Torben	tobias.krauthoff+dbas.usert02@gmail.com	m	$2a$10$LrQYZZjVzZCJohjNTXawpuM5zH.Tlf8RGfMSqLdCdWWjbAfK/e8/q	3	2017-08-17 11:57:14.964075	2017-08-17 11:57:14.964123	2017-08-17 11:57:14.964168		\N
10	Thorsten	Scherer	Thorsten	Thorsten	tobias.krauthoff+dbas.usert03@gmail.com	m	$2a$10$LrQYZZjVzZCJohjNTXawpuM5zH.Tlf8RGfMSqLdCdWWjbAfK/e8/q	3	2017-08-17 11:57:14.964243	2017-08-17 11:57:14.96429	2017-08-17 11:57:14.964334		\N
11	Friedrich	Schutte	Friedrich	Friedrich	tobias.krauthoff+dbas.usert04@gmail.com	m	$2a$10$LrQYZZjVzZCJohjNTXawpuM5zH.Tlf8RGfMSqLdCdWWjbAfK/e8/q	3	2017-08-17 11:57:14.964409	2017-08-17 11:57:14.964456	2017-08-17 11:57:14.9645		\N
12	Aayden	Westermann	Aayden	Aayden	tobias.krauthoff+dbas.usert05@gmail.com	m	$2a$10$LrQYZZjVzZCJohjNTXawpuM5zH.Tlf8RGfMSqLdCdWWjbAfK/e8/q	3	2017-08-17 11:57:14.964575	2017-08-17 11:57:14.964621	2017-08-17 11:57:14.964666		\N
13	Hermann	Grasshoff	Hermann	Hermann	tobias.krauthoff+dbas.usert06@gmail.com	m	$2a$10$LrQYZZjVzZCJohjNTXawpuM5zH.Tlf8RGfMSqLdCdWWjbAfK/e8/q	3	2017-08-17 11:57:14.96474	2017-08-17 11:57:14.964787	2017-08-17 11:57:14.964831		\N
14	Wolf	Himmler	Wolf	Wolf	tobias.krauthoff+dbas.usert07@gmail.com	m	$2a$10$LrQYZZjVzZCJohjNTXawpuM5zH.Tlf8RGfMSqLdCdWWjbAfK/e8/q	3	2017-08-17 11:57:14.964905	2017-08-17 11:57:14.964951	2017-08-17 11:57:14.964995		\N
15	Jakob	Winter	Jakob	Jakob	tobias.krauthoff+dbas.usert08@gmail.com	m	$2a$10$LrQYZZjVzZCJohjNTXawpuM5zH.Tlf8RGfMSqLdCdWWjbAfK/e8/q	3	2017-08-17 11:57:14.965069	2017-08-17 11:57:14.965115	2017-08-17 11:57:14.965159		\N
16	Alwin	Wechter	Alwin	Alwin	tobias.krauthoff+dbas.usert09@gmail.com	m	$2a$10$LrQYZZjVzZCJohjNTXawpuM5zH.Tlf8RGfMSqLdCdWWjbAfK/e8/q	3	2017-08-17 11:57:14.965234	2017-08-17 11:57:14.965281	2017-08-17 11:57:14.965325		\N
17	Walter	Weisser	Walter	Walter	tobias.krauthoff+dbas.usert10@gmail.com	m	$2a$10$LrQYZZjVzZCJohjNTXawpuM5zH.Tlf8RGfMSqLdCdWWjbAfK/e8/q	3	2017-08-17 11:57:14.9654	2017-08-17 11:57:14.965446	2017-08-17 11:57:14.96549		\N
18	Volker	Keitel	Volker	Volker	tobias.krauthoff+dbas.usert11@gmail.com	m	$2a$10$LrQYZZjVzZCJohjNTXawpuM5zH.Tlf8RGfMSqLdCdWWjbAfK/e8/q	3	2017-08-17 11:57:14.965565	2017-08-17 11:57:14.965611	2017-08-17 11:57:14.965655		\N
19	Benedikt	Feuerstein	Benedikt	Benedikt	tobias.krauthoff+dbas.usert12@gmail.com	m	$2a$10$LrQYZZjVzZCJohjNTXawpuM5zH.Tlf8RGfMSqLdCdWWjbAfK/e8/q	3	2017-08-17 11:57:14.965733	2017-08-17 11:57:14.96578	2017-08-17 11:57:14.965824		\N
20	Engelbert	Gottlieb	Engelbert	Engelbert	tobias.krauthoff+dbas.usert13@gmail.com	m	$2a$10$LrQYZZjVzZCJohjNTXawpuM5zH.Tlf8RGfMSqLdCdWWjbAfK/e8/q	3	2017-08-17 11:57:14.965937	2017-08-17 11:57:14.965984	2017-08-17 11:57:14.966028		\N
21	Elias	Auerbach	Elias	Elias	tobias.krauthoff+dbas.usert14@gmail.com	m	$2a$10$LrQYZZjVzZCJohjNTXawpuM5zH.Tlf8RGfMSqLdCdWWjbAfK/e8/q	3	2017-08-17 11:57:14.966103	2017-08-17 11:57:14.966149	2017-08-17 11:57:14.966193		\N
22	Rupert	Wenz	Rupert	Rupert	tobias.krauthoff+dbas.usert15@gmail.com	m	$2a$10$LrQYZZjVzZCJohjNTXawpuM5zH.Tlf8RGfMSqLdCdWWjbAfK/e8/q	3	2017-08-17 11:57:14.966267	2017-08-17 11:57:14.966313	2017-08-17 11:57:14.966359		\N
23	Marga	Wegscheider	Marga	Marga	tobias.krauthoff+dbas.usert16@gmail.com	f	$2a$10$LrQYZZjVzZCJohjNTXawpuM5zH.Tlf8RGfMSqLdCdWWjbAfK/e8/q	3	2017-08-17 11:57:14.966435	2017-08-17 11:57:14.966482	2017-08-17 11:57:14.966525		\N
24	Larissa	Clauberg	Larissa	Larissa	tobias.krauthoff+dbas.usert17@gmail.com	f	$2a$10$LrQYZZjVzZCJohjNTXawpuM5zH.Tlf8RGfMSqLdCdWWjbAfK/e8/q	3	2017-08-17 11:57:14.9666	2017-08-17 11:57:14.966659	2017-08-17 11:57:14.966713		\N
25	Emmi	Rosch	Emmi	Emmi	tobias.krauthoff+dbas.usert18@gmail.com	f	$2a$10$LrQYZZjVzZCJohjNTXawpuM5zH.Tlf8RGfMSqLdCdWWjbAfK/e8/q	3	2017-08-17 11:57:14.966787	2017-08-17 11:57:14.966833	2017-08-17 11:57:14.966877		\N
26	Konstanze	Krebs	Konstanze	Konstanze	tobias.krauthoff+dbas.usert19@gmail.com	f	$2a$10$LrQYZZjVzZCJohjNTXawpuM5zH.Tlf8RGfMSqLdCdWWjbAfK/e8/q	3	2017-08-17 11:57:14.966953	2017-08-17 11:57:14.966999	2017-08-17 11:57:14.967043		\N
27	Catrin	Fahnrich	Catrin	Catrin	tobias.krauthoff+dbas.usert20@gmail.com	f	$2a$10$LrQYZZjVzZCJohjNTXawpuM5zH.Tlf8RGfMSqLdCdWWjbAfK/e8/q	3	2017-08-17 11:57:14.967129	2017-08-17 11:57:14.967177	2017-08-17 11:57:14.967231		\N
28	Antonia	Bartram	Antonia	Antonia	tobias.krauthoff+dbas.usert21@gmail.com	f	$2a$10$LrQYZZjVzZCJohjNTXawpuM5zH.Tlf8RGfMSqLdCdWWjbAfK/e8/q	3	2017-08-17 11:57:14.967306	2017-08-17 11:57:14.967352	2017-08-17 11:57:14.967396		\N
29	Nora	Kempf	Nora	Nora	tobias.krauthoff+dbas.usert22@gmail.com	f	$2a$10$LrQYZZjVzZCJohjNTXawpuM5zH.Tlf8RGfMSqLdCdWWjbAfK/e8/q	3	2017-08-17 11:57:14.967471	2017-08-17 11:57:14.967519	2017-08-17 11:57:14.967564		\N
30	Julia	Wetter	Julia	Julia	tobias.krauthoff+dbas.usert23@gmail.com	f	$2a$10$LrQYZZjVzZCJohjNTXawpuM5zH.Tlf8RGfMSqLdCdWWjbAfK/e8/q	3	2017-08-17 11:57:14.96764	2017-08-17 11:57:14.967688	2017-08-17 11:57:14.967732		\N
31	Jutta	Munch	Jutta	Jutta	tobias.krauthoff+dbas.usert24@gmail.com	f	$2a$10$LrQYZZjVzZCJohjNTXawpuM5zH.Tlf8RGfMSqLdCdWWjbAfK/e8/q	3	2017-08-17 11:57:14.967808	2017-08-17 11:57:14.967855	2017-08-17 11:57:14.967899		\N
32	Helga	Heilmann	Helga	Helga	tobias.krauthoff+dbas.usert25@gmail.com	f	$2a$10$LrQYZZjVzZCJohjNTXawpuM5zH.Tlf8RGfMSqLdCdWWjbAfK/e8/q	3	2017-08-17 11:57:14.967973	2017-08-17 11:57:14.968019	2017-08-17 11:57:14.968063		\N
33	Denise	Tietjen	Denise	Denise	tobias.krauthoff+dbas.usert26@gmail.com	f	$2a$10$LrQYZZjVzZCJohjNTXawpuM5zH.Tlf8RGfMSqLdCdWWjbAfK/e8/q	3	2017-08-17 11:57:14.968139	2017-08-17 11:57:14.968188	2017-08-17 11:57:14.968232		\N
34	Hanne	Beckmann	Hanne	Hanne	tobias.krauthoff+dbas.usert27@gmail.com	f	$2a$10$LrQYZZjVzZCJohjNTXawpuM5zH.Tlf8RGfMSqLdCdWWjbAfK/e8/q	3	2017-08-17 11:57:14.968308	2017-08-17 11:57:14.968408	2017-08-17 11:57:14.968453		\N
35	Elly	Landauer	Elly	Elly	tobias.krauthoff+dbas.usert28@gmail.com	f	$2a$10$LrQYZZjVzZCJohjNTXawpuM5zH.Tlf8RGfMSqLdCdWWjbAfK/e8/q	3	2017-08-17 11:57:14.968529	2017-08-17 11:57:14.968576	2017-08-17 11:57:14.968619		\N
36	Sybille	Redlich	Sybille	Sybille	tobias.krauthoff+dbas.usert29@gmail.com	f	$2a$10$LrQYZZjVzZCJohjNTXawpuM5zH.Tlf8RGfMSqLdCdWWjbAfK/e8/q	3	2017-08-17 11:57:14.968694	2017-08-17 11:57:14.968743	2017-08-17 11:57:14.96879		\N
37	Ingeburg	Fischer	Ingeburg	Ingeburg	tobias.krauthoff+dbas.usert30@gmail.com	f	$2a$10$LrQYZZjVzZCJohjNTXawpuM5zH.Tlf8RGfMSqLdCdWWjbAfK/e8/q	3	2017-08-17 11:57:14.968865	2017-08-17 11:57:14.968912	2017-08-17 11:57:14.968955		\N
\.


--
-- Name: users_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('users_uid_seq', 37, true);


--
-- Name: arguments arguments_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY arguments
    ADD CONSTRAINT arguments_pkey PRIMARY KEY (uid);


--
-- Name: clicked_arguments clicked_arguments_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY clicked_arguments
    ADD CONSTRAINT clicked_arguments_pkey PRIMARY KEY (uid);


--
-- Name: clicked_statements clicked_statements_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY clicked_statements
    ADD CONSTRAINT clicked_statements_pkey PRIMARY KEY (uid);


--
-- Name: groups groups_name_key; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY groups
    ADD CONSTRAINT groups_name_key UNIQUE (name);


--
-- Name: groups groups_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY groups
    ADD CONSTRAINT groups_pkey PRIMARY KEY (uid);


--
-- Name: history history_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY history
    ADD CONSTRAINT history_pkey PRIMARY KEY (uid);


--
-- Name: issues issues_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY issues
    ADD CONSTRAINT issues_pkey PRIMARY KEY (uid);


--
-- Name: issues issues_slug_key; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY issues
    ADD CONSTRAINT issues_slug_key UNIQUE (slug);


--
-- Name: languages languages_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY languages
    ADD CONSTRAINT languages_pkey PRIMARY KEY (uid);


--
-- Name: languages languages_ui_locales_key; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY languages
    ADD CONSTRAINT languages_ui_locales_key UNIQUE (ui_locales);


--
-- Name: last_reviewers_delete last_reviewers_delete_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY last_reviewers_delete
    ADD CONSTRAINT last_reviewers_delete_pkey PRIMARY KEY (uid);


--
-- Name: last_reviewers_duplicates last_reviewers_duplicates_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY last_reviewers_duplicates
    ADD CONSTRAINT last_reviewers_duplicates_pkey PRIMARY KEY (uid);


--
-- Name: last_reviewers_edit last_reviewers_edit_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY last_reviewers_edit
    ADD CONSTRAINT last_reviewers_edit_pkey PRIMARY KEY (uid);


--
-- Name: last_reviewers_merge last_reviewers_merge_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY last_reviewers_merge
    ADD CONSTRAINT last_reviewers_merge_pkey PRIMARY KEY (uid);


--
-- Name: last_reviewers_optimization last_reviewers_optimization_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY last_reviewers_optimization
    ADD CONSTRAINT last_reviewers_optimization_pkey PRIMARY KEY (uid);


--
-- Name: last_reviewers_split last_reviewers_split_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY last_reviewers_split
    ADD CONSTRAINT last_reviewers_split_pkey PRIMARY KEY (uid);


--
-- Name: marked_arguments marked_arguments_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY marked_arguments
    ADD CONSTRAINT marked_arguments_pkey PRIMARY KEY (uid);


--
-- Name: marked_statements marked_statements_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY marked_statements
    ADD CONSTRAINT marked_statements_pkey PRIMARY KEY (uid);


--
-- Name: messages messages_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY messages
    ADD CONSTRAINT messages_pkey PRIMARY KEY (uid);


--
-- Name: optimization_review_locks optimization_review_locks_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY optimization_review_locks
    ADD CONSTRAINT optimization_review_locks_pkey PRIMARY KEY (author_uid);


--
-- Name: premisegroup_merged premisegroup_merged_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY premisegroup_merged
    ADD CONSTRAINT premisegroup_merged_pkey PRIMARY KEY (uid);


--
-- Name: premisegroup_splitted premisegroup_splitted_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY premisegroup_splitted
    ADD CONSTRAINT premisegroup_splitted_pkey PRIMARY KEY (uid);


--
-- Name: premisegroups premisegroups_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY premisegroups
    ADD CONSTRAINT premisegroups_pkey PRIMARY KEY (uid);


--
-- Name: premises premises_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY premises
    ADD CONSTRAINT premises_pkey PRIMARY KEY (uid);


--
-- Name: reputation_history reputation_history_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY reputation_history
    ADD CONSTRAINT reputation_history_pkey PRIMARY KEY (uid);


--
-- Name: reputation_reasons reputation_reasons_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY reputation_reasons
    ADD CONSTRAINT reputation_reasons_pkey PRIMARY KEY (uid);


--
-- Name: reputation_reasons reputation_reasons_reason_key; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY reputation_reasons
    ADD CONSTRAINT reputation_reasons_reason_key UNIQUE (reason);


--
-- Name: review_canceled review_canceled_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_canceled
    ADD CONSTRAINT review_canceled_pkey PRIMARY KEY (uid);


--
-- Name: review_delete_reasons review_delete_reasons_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_delete_reasons
    ADD CONSTRAINT review_delete_reasons_pkey PRIMARY KEY (uid);


--
-- Name: review_delete_reasons review_delete_reasons_reason_key; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_delete_reasons
    ADD CONSTRAINT review_delete_reasons_reason_key UNIQUE (reason);


--
-- Name: review_deletes review_deletes_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_deletes
    ADD CONSTRAINT review_deletes_pkey PRIMARY KEY (uid);


--
-- Name: review_duplicates review_duplicates_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_duplicates
    ADD CONSTRAINT review_duplicates_pkey PRIMARY KEY (uid);


--
-- Name: review_edit_values review_edit_values_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_edit_values
    ADD CONSTRAINT review_edit_values_pkey PRIMARY KEY (uid);


--
-- Name: review_edits review_edits_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_edits
    ADD CONSTRAINT review_edits_pkey PRIMARY KEY (uid);


--
-- Name: review_merge review_merge_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_merge
    ADD CONSTRAINT review_merge_pkey PRIMARY KEY (uid);


--
-- Name: review_merge_values review_merge_values_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_merge_values
    ADD CONSTRAINT review_merge_values_pkey PRIMARY KEY (uid);


--
-- Name: review_optimizations review_optimizations_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_optimizations
    ADD CONSTRAINT review_optimizations_pkey PRIMARY KEY (uid);


--
-- Name: review_split review_split_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_split
    ADD CONSTRAINT review_split_pkey PRIMARY KEY (uid);


--
-- Name: review_split_values review_split_values_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_split_values
    ADD CONSTRAINT review_split_values_pkey PRIMARY KEY (uid);


--
-- Name: revoked_content_history revoked_content_history_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY revoked_content_history
    ADD CONSTRAINT revoked_content_history_pkey PRIMARY KEY (uid);


--
-- Name: revoked_content revoked_content_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY revoked_content
    ADD CONSTRAINT revoked_content_pkey PRIMARY KEY (uid);


--
-- Name: revoked_duplicate revoked_duplicate_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY revoked_duplicate
    ADD CONSTRAINT revoked_duplicate_pkey PRIMARY KEY (uid);


--
-- Name: rss rss_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY rss
    ADD CONSTRAINT rss_pkey PRIMARY KEY (uid);


--
-- Name: seen_arguments seen_arguments_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY seen_arguments
    ADD CONSTRAINT seen_arguments_pkey PRIMARY KEY (uid);


--
-- Name: seen_statements seen_statements_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY seen_statements
    ADD CONSTRAINT seen_statements_pkey PRIMARY KEY (uid);


--
-- Name: settings settings_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY settings
    ADD CONSTRAINT settings_pkey PRIMARY KEY (author_uid);


--
-- Name: statement_references statement_references_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY statement_references
    ADD CONSTRAINT statement_references_pkey PRIMARY KEY (uid);


--
-- Name: statements statements_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY statements
    ADD CONSTRAINT statements_pkey PRIMARY KEY (uid);


--
-- Name: textversions textversions_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY textversions
    ADD CONSTRAINT textversions_pkey PRIMARY KEY (uid);


--
-- Name: users users_nickname_key; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_nickname_key UNIQUE (nickname);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (uid);


--
-- Name: arguments arguments_argument_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY arguments
    ADD CONSTRAINT arguments_argument_uid_fkey FOREIGN KEY (argument_uid) REFERENCES arguments(uid);


--
-- Name: arguments arguments_author_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY arguments
    ADD CONSTRAINT arguments_author_uid_fkey FOREIGN KEY (author_uid) REFERENCES users(uid);


--
-- Name: arguments arguments_conclusion_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY arguments
    ADD CONSTRAINT arguments_conclusion_uid_fkey FOREIGN KEY (conclusion_uid) REFERENCES statements(uid);


--
-- Name: arguments arguments_issue_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY arguments
    ADD CONSTRAINT arguments_issue_uid_fkey FOREIGN KEY (issue_uid) REFERENCES issues(uid);


--
-- Name: arguments arguments_premisesgroup_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY arguments
    ADD CONSTRAINT arguments_premisesgroup_uid_fkey FOREIGN KEY (premisesgroup_uid) REFERENCES premisegroups(uid);


--
-- Name: clicked_arguments clicked_arguments_argument_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY clicked_arguments
    ADD CONSTRAINT clicked_arguments_argument_uid_fkey FOREIGN KEY (argument_uid) REFERENCES arguments(uid);


--
-- Name: clicked_arguments clicked_arguments_author_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY clicked_arguments
    ADD CONSTRAINT clicked_arguments_author_uid_fkey FOREIGN KEY (author_uid) REFERENCES users(uid);


--
-- Name: clicked_statements clicked_statements_author_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY clicked_statements
    ADD CONSTRAINT clicked_statements_author_uid_fkey FOREIGN KEY (author_uid) REFERENCES users(uid);


--
-- Name: clicked_statements clicked_statements_statement_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY clicked_statements
    ADD CONSTRAINT clicked_statements_statement_uid_fkey FOREIGN KEY (statement_uid) REFERENCES statements(uid);


--
-- Name: history history_author_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY history
    ADD CONSTRAINT history_author_uid_fkey FOREIGN KEY (author_uid) REFERENCES users(uid);


--
-- Name: issues issues_author_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY issues
    ADD CONSTRAINT issues_author_uid_fkey FOREIGN KEY (author_uid) REFERENCES users(uid);


--
-- Name: issues issues_lang_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY issues
    ADD CONSTRAINT issues_lang_uid_fkey FOREIGN KEY (lang_uid) REFERENCES languages(uid);


--
-- Name: last_reviewers_delete last_reviewers_delete_review_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY last_reviewers_delete
    ADD CONSTRAINT last_reviewers_delete_review_uid_fkey FOREIGN KEY (review_uid) REFERENCES review_deletes(uid);


--
-- Name: last_reviewers_delete last_reviewers_delete_reviewer_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY last_reviewers_delete
    ADD CONSTRAINT last_reviewers_delete_reviewer_uid_fkey FOREIGN KEY (reviewer_uid) REFERENCES users(uid);


--
-- Name: last_reviewers_duplicates last_reviewers_duplicates_review_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY last_reviewers_duplicates
    ADD CONSTRAINT last_reviewers_duplicates_review_uid_fkey FOREIGN KEY (review_uid) REFERENCES review_duplicates(uid);


--
-- Name: last_reviewers_duplicates last_reviewers_duplicates_reviewer_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY last_reviewers_duplicates
    ADD CONSTRAINT last_reviewers_duplicates_reviewer_uid_fkey FOREIGN KEY (reviewer_uid) REFERENCES users(uid);


--
-- Name: last_reviewers_edit last_reviewers_edit_review_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY last_reviewers_edit
    ADD CONSTRAINT last_reviewers_edit_review_uid_fkey FOREIGN KEY (review_uid) REFERENCES review_edits(uid);


--
-- Name: last_reviewers_edit last_reviewers_edit_reviewer_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY last_reviewers_edit
    ADD CONSTRAINT last_reviewers_edit_reviewer_uid_fkey FOREIGN KEY (reviewer_uid) REFERENCES users(uid);


--
-- Name: last_reviewers_merge last_reviewers_merge_review_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY last_reviewers_merge
    ADD CONSTRAINT last_reviewers_merge_review_uid_fkey FOREIGN KEY (review_uid) REFERENCES review_merge(uid);


--
-- Name: last_reviewers_merge last_reviewers_merge_reviewer_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY last_reviewers_merge
    ADD CONSTRAINT last_reviewers_merge_reviewer_uid_fkey FOREIGN KEY (reviewer_uid) REFERENCES users(uid);


--
-- Name: last_reviewers_optimization last_reviewers_optimization_review_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY last_reviewers_optimization
    ADD CONSTRAINT last_reviewers_optimization_review_uid_fkey FOREIGN KEY (review_uid) REFERENCES review_optimizations(uid);


--
-- Name: last_reviewers_optimization last_reviewers_optimization_reviewer_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY last_reviewers_optimization
    ADD CONSTRAINT last_reviewers_optimization_reviewer_uid_fkey FOREIGN KEY (reviewer_uid) REFERENCES users(uid);


--
-- Name: last_reviewers_split last_reviewers_split_review_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY last_reviewers_split
    ADD CONSTRAINT last_reviewers_split_review_uid_fkey FOREIGN KEY (review_uid) REFERENCES review_split(uid);


--
-- Name: last_reviewers_split last_reviewers_split_reviewer_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY last_reviewers_split
    ADD CONSTRAINT last_reviewers_split_reviewer_uid_fkey FOREIGN KEY (reviewer_uid) REFERENCES users(uid);


--
-- Name: marked_arguments marked_arguments_argument_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY marked_arguments
    ADD CONSTRAINT marked_arguments_argument_uid_fkey FOREIGN KEY (argument_uid) REFERENCES arguments(uid);


--
-- Name: marked_arguments marked_arguments_author_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY marked_arguments
    ADD CONSTRAINT marked_arguments_author_uid_fkey FOREIGN KEY (author_uid) REFERENCES users(uid);


--
-- Name: marked_statements marked_statements_author_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY marked_statements
    ADD CONSTRAINT marked_statements_author_uid_fkey FOREIGN KEY (author_uid) REFERENCES users(uid);


--
-- Name: marked_statements marked_statements_statement_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY marked_statements
    ADD CONSTRAINT marked_statements_statement_uid_fkey FOREIGN KEY (statement_uid) REFERENCES statements(uid);


--
-- Name: messages messages_from_author_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY messages
    ADD CONSTRAINT messages_from_author_uid_fkey FOREIGN KEY (from_author_uid) REFERENCES users(uid);


--
-- Name: messages messages_to_author_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY messages
    ADD CONSTRAINT messages_to_author_uid_fkey FOREIGN KEY (to_author_uid) REFERENCES users(uid);


--
-- Name: optimization_review_locks optimization_review_locks_author_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY optimization_review_locks
    ADD CONSTRAINT optimization_review_locks_author_uid_fkey FOREIGN KEY (author_uid) REFERENCES users(uid);


--
-- Name: optimization_review_locks optimization_review_locks_review_optimization_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY optimization_review_locks
    ADD CONSTRAINT optimization_review_locks_review_optimization_uid_fkey FOREIGN KEY (review_optimization_uid) REFERENCES review_optimizations(uid);


--
-- Name: premisegroup_merged premisegroup_merged_new_premisegroup_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY premisegroup_merged
    ADD CONSTRAINT premisegroup_merged_new_premisegroup_uid_fkey FOREIGN KEY (new_premisegroup_uid) REFERENCES premisegroups(uid);


--
-- Name: premisegroup_merged premisegroup_merged_old_premisegroup_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY premisegroup_merged
    ADD CONSTRAINT premisegroup_merged_old_premisegroup_uid_fkey FOREIGN KEY (old_premisegroup_uid) REFERENCES premisegroups(uid);


--
-- Name: premisegroup_merged premisegroup_merged_review_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY premisegroup_merged
    ADD CONSTRAINT premisegroup_merged_review_uid_fkey FOREIGN KEY (review_uid) REFERENCES review_merge(uid);


--
-- Name: premisegroup_splitted premisegroup_splitted_new_premisegroup_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY premisegroup_splitted
    ADD CONSTRAINT premisegroup_splitted_new_premisegroup_uid_fkey FOREIGN KEY (new_premisegroup_uid) REFERENCES premisegroups(uid);


--
-- Name: premisegroup_splitted premisegroup_splitted_old_premisegroup_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY premisegroup_splitted
    ADD CONSTRAINT premisegroup_splitted_old_premisegroup_uid_fkey FOREIGN KEY (old_premisegroup_uid) REFERENCES premisegroups(uid);


--
-- Name: premisegroup_splitted premisegroup_splitted_review_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY premisegroup_splitted
    ADD CONSTRAINT premisegroup_splitted_review_uid_fkey FOREIGN KEY (review_uid) REFERENCES review_split(uid);


--
-- Name: premisegroups premisegroups_author_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY premisegroups
    ADD CONSTRAINT premisegroups_author_uid_fkey FOREIGN KEY (author_uid) REFERENCES users(uid);


--
-- Name: premises premises_author_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY premises
    ADD CONSTRAINT premises_author_uid_fkey FOREIGN KEY (author_uid) REFERENCES users(uid);


--
-- Name: premises premises_issue_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY premises
    ADD CONSTRAINT premises_issue_uid_fkey FOREIGN KEY (issue_uid) REFERENCES issues(uid);


--
-- Name: premises premises_premisesgroup_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY premises
    ADD CONSTRAINT premises_premisesgroup_uid_fkey FOREIGN KEY (premisesgroup_uid) REFERENCES premisegroups(uid);


--
-- Name: premises premises_statement_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY premises
    ADD CONSTRAINT premises_statement_uid_fkey FOREIGN KEY (statement_uid) REFERENCES statements(uid);


--
-- Name: reputation_history reputation_history_reputation_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY reputation_history
    ADD CONSTRAINT reputation_history_reputation_uid_fkey FOREIGN KEY (reputation_uid) REFERENCES reputation_reasons(uid);


--
-- Name: reputation_history reputation_history_reputator_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY reputation_history
    ADD CONSTRAINT reputation_history_reputator_uid_fkey FOREIGN KEY (reputator_uid) REFERENCES users(uid);


--
-- Name: review_canceled review_canceled_author_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_canceled
    ADD CONSTRAINT review_canceled_author_uid_fkey FOREIGN KEY (author_uid) REFERENCES users(uid);


--
-- Name: review_canceled review_canceled_review_delete_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_canceled
    ADD CONSTRAINT review_canceled_review_delete_uid_fkey FOREIGN KEY (review_delete_uid) REFERENCES review_deletes(uid);


--
-- Name: review_canceled review_canceled_review_duplicate_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_canceled
    ADD CONSTRAINT review_canceled_review_duplicate_uid_fkey FOREIGN KEY (review_duplicate_uid) REFERENCES review_duplicates(uid);


--
-- Name: review_canceled review_canceled_review_edit_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_canceled
    ADD CONSTRAINT review_canceled_review_edit_uid_fkey FOREIGN KEY (review_edit_uid) REFERENCES review_edits(uid);


--
-- Name: review_canceled review_canceled_review_merge_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_canceled
    ADD CONSTRAINT review_canceled_review_merge_uid_fkey FOREIGN KEY (review_merge_uid) REFERENCES review_merge(uid);


--
-- Name: review_canceled review_canceled_review_optimization_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_canceled
    ADD CONSTRAINT review_canceled_review_optimization_uid_fkey FOREIGN KEY (review_optimization_uid) REFERENCES review_optimizations(uid);


--
-- Name: review_canceled review_canceled_review_split_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_canceled
    ADD CONSTRAINT review_canceled_review_split_uid_fkey FOREIGN KEY (review_split_uid) REFERENCES review_split(uid);


--
-- Name: review_deletes review_deletes_argument_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_deletes
    ADD CONSTRAINT review_deletes_argument_uid_fkey FOREIGN KEY (argument_uid) REFERENCES arguments(uid);


--
-- Name: review_deletes review_deletes_detector_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_deletes
    ADD CONSTRAINT review_deletes_detector_uid_fkey FOREIGN KEY (detector_uid) REFERENCES users(uid);


--
-- Name: review_deletes review_deletes_reason_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_deletes
    ADD CONSTRAINT review_deletes_reason_uid_fkey FOREIGN KEY (reason_uid) REFERENCES review_delete_reasons(uid);


--
-- Name: review_deletes review_deletes_statement_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_deletes
    ADD CONSTRAINT review_deletes_statement_uid_fkey FOREIGN KEY (statement_uid) REFERENCES statements(uid);


--
-- Name: review_duplicates review_duplicates_detector_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_duplicates
    ADD CONSTRAINT review_duplicates_detector_uid_fkey FOREIGN KEY (detector_uid) REFERENCES users(uid);


--
-- Name: review_duplicates review_duplicates_duplicate_statement_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_duplicates
    ADD CONSTRAINT review_duplicates_duplicate_statement_uid_fkey FOREIGN KEY (duplicate_statement_uid) REFERENCES statements(uid);


--
-- Name: review_duplicates review_duplicates_original_statement_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_duplicates
    ADD CONSTRAINT review_duplicates_original_statement_uid_fkey FOREIGN KEY (original_statement_uid) REFERENCES statements(uid);


--
-- Name: review_edit_values review_edit_values_review_edit_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_edit_values
    ADD CONSTRAINT review_edit_values_review_edit_uid_fkey FOREIGN KEY (review_edit_uid) REFERENCES review_edits(uid);


--
-- Name: review_edit_values review_edit_values_statement_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_edit_values
    ADD CONSTRAINT review_edit_values_statement_uid_fkey FOREIGN KEY (statement_uid) REFERENCES statements(uid);


--
-- Name: review_edits review_edits_argument_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_edits
    ADD CONSTRAINT review_edits_argument_uid_fkey FOREIGN KEY (argument_uid) REFERENCES arguments(uid);


--
-- Name: review_edits review_edits_detector_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_edits
    ADD CONSTRAINT review_edits_detector_uid_fkey FOREIGN KEY (detector_uid) REFERENCES users(uid);


--
-- Name: review_edits review_edits_statement_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_edits
    ADD CONSTRAINT review_edits_statement_uid_fkey FOREIGN KEY (statement_uid) REFERENCES statements(uid);


--
-- Name: review_merge review_merge_detector_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_merge
    ADD CONSTRAINT review_merge_detector_uid_fkey FOREIGN KEY (detector_uid) REFERENCES users(uid);


--
-- Name: review_merge review_merge_premisesgroup_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_merge
    ADD CONSTRAINT review_merge_premisesgroup_uid_fkey FOREIGN KEY (premisesgroup_uid) REFERENCES premisegroups(uid);


--
-- Name: review_merge_values review_merge_values_review_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_merge_values
    ADD CONSTRAINT review_merge_values_review_uid_fkey FOREIGN KEY (review_uid) REFERENCES review_merge(uid);


--
-- Name: review_optimizations review_optimizations_argument_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_optimizations
    ADD CONSTRAINT review_optimizations_argument_uid_fkey FOREIGN KEY (argument_uid) REFERENCES arguments(uid);


--
-- Name: review_optimizations review_optimizations_detector_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_optimizations
    ADD CONSTRAINT review_optimizations_detector_uid_fkey FOREIGN KEY (detector_uid) REFERENCES users(uid);


--
-- Name: review_optimizations review_optimizations_statement_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_optimizations
    ADD CONSTRAINT review_optimizations_statement_uid_fkey FOREIGN KEY (statement_uid) REFERENCES statements(uid);


--
-- Name: review_split review_split_detector_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_split
    ADD CONSTRAINT review_split_detector_uid_fkey FOREIGN KEY (detector_uid) REFERENCES users(uid);


--
-- Name: review_split review_split_premisesgroup_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_split
    ADD CONSTRAINT review_split_premisesgroup_uid_fkey FOREIGN KEY (premisesgroup_uid) REFERENCES premisegroups(uid);


--
-- Name: review_split_values review_split_values_review_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_split_values
    ADD CONSTRAINT review_split_values_review_uid_fkey FOREIGN KEY (review_uid) REFERENCES review_split(uid);


--
-- Name: revoked_content revoked_content_argument_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY revoked_content
    ADD CONSTRAINT revoked_content_argument_uid_fkey FOREIGN KEY (argument_uid) REFERENCES arguments(uid);


--
-- Name: revoked_content revoked_content_author_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY revoked_content
    ADD CONSTRAINT revoked_content_author_uid_fkey FOREIGN KEY (author_uid) REFERENCES users(uid);


--
-- Name: revoked_content_history revoked_content_history_argument_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY revoked_content_history
    ADD CONSTRAINT revoked_content_history_argument_uid_fkey FOREIGN KEY (argument_uid) REFERENCES arguments(uid);


--
-- Name: revoked_content_history revoked_content_history_new_author_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY revoked_content_history
    ADD CONSTRAINT revoked_content_history_new_author_uid_fkey FOREIGN KEY (new_author_uid) REFERENCES users(uid);


--
-- Name: revoked_content_history revoked_content_history_old_author_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY revoked_content_history
    ADD CONSTRAINT revoked_content_history_old_author_uid_fkey FOREIGN KEY (old_author_uid) REFERENCES users(uid);


--
-- Name: revoked_content_history revoked_content_history_textversion_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY revoked_content_history
    ADD CONSTRAINT revoked_content_history_textversion_uid_fkey FOREIGN KEY (textversion_uid) REFERENCES textversions(uid);


--
-- Name: revoked_content revoked_content_statement_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY revoked_content
    ADD CONSTRAINT revoked_content_statement_uid_fkey FOREIGN KEY (statement_uid) REFERENCES statements(uid);


--
-- Name: revoked_duplicate revoked_duplicate_argument_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY revoked_duplicate
    ADD CONSTRAINT revoked_duplicate_argument_uid_fkey FOREIGN KEY (argument_uid) REFERENCES arguments(uid);


--
-- Name: revoked_duplicate revoked_duplicate_premise_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY revoked_duplicate
    ADD CONSTRAINT revoked_duplicate_premise_uid_fkey FOREIGN KEY (premise_uid) REFERENCES premises(uid);


--
-- Name: revoked_duplicate revoked_duplicate_review_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY revoked_duplicate
    ADD CONSTRAINT revoked_duplicate_review_uid_fkey FOREIGN KEY (review_uid) REFERENCES review_duplicates(uid);


--
-- Name: revoked_duplicate revoked_duplicate_statement_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY revoked_duplicate
    ADD CONSTRAINT revoked_duplicate_statement_uid_fkey FOREIGN KEY (statement_uid) REFERENCES statements(uid);


--
-- Name: rss rss_author_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY rss
    ADD CONSTRAINT rss_author_uid_fkey FOREIGN KEY (author_uid) REFERENCES users(uid);


--
-- Name: rss rss_issue_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY rss
    ADD CONSTRAINT rss_issue_uid_fkey FOREIGN KEY (issue_uid) REFERENCES issues(uid);


--
-- Name: seen_arguments seen_arguments_argument_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY seen_arguments
    ADD CONSTRAINT seen_arguments_argument_uid_fkey FOREIGN KEY (argument_uid) REFERENCES arguments(uid);


--
-- Name: seen_arguments seen_arguments_user_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY seen_arguments
    ADD CONSTRAINT seen_arguments_user_uid_fkey FOREIGN KEY (user_uid) REFERENCES users(uid);


--
-- Name: seen_statements seen_statements_statement_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY seen_statements
    ADD CONSTRAINT seen_statements_statement_uid_fkey FOREIGN KEY (statement_uid) REFERENCES statements(uid);


--
-- Name: seen_statements seen_statements_user_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY seen_statements
    ADD CONSTRAINT seen_statements_user_uid_fkey FOREIGN KEY (user_uid) REFERENCES users(uid);


--
-- Name: settings settings_author_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY settings
    ADD CONSTRAINT settings_author_uid_fkey FOREIGN KEY (author_uid) REFERENCES users(uid);


--
-- Name: settings settings_lang_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY settings
    ADD CONSTRAINT settings_lang_uid_fkey FOREIGN KEY (lang_uid) REFERENCES languages(uid);


--
-- Name: settings settings_last_topic_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY settings
    ADD CONSTRAINT settings_last_topic_uid_fkey FOREIGN KEY (last_topic_uid) REFERENCES issues(uid);


--
-- Name: statement_references statement_references_author_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY statement_references
    ADD CONSTRAINT statement_references_author_uid_fkey FOREIGN KEY (author_uid) REFERENCES users(uid);


--
-- Name: statement_references statement_references_issue_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY statement_references
    ADD CONSTRAINT statement_references_issue_uid_fkey FOREIGN KEY (issue_uid) REFERENCES issues(uid);


--
-- Name: statement_references statement_references_statement_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY statement_references
    ADD CONSTRAINT statement_references_statement_uid_fkey FOREIGN KEY (statement_uid) REFERENCES statements(uid);


--
-- Name: statements statements_issue_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY statements
    ADD CONSTRAINT statements_issue_uid_fkey FOREIGN KEY (issue_uid) REFERENCES issues(uid);


--
-- Name: statements statements_textversion_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY statements
    ADD CONSTRAINT statements_textversion_uid_fkey FOREIGN KEY (textversion_uid) REFERENCES textversions(uid);


--
-- Name: textversions textversions_author_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY textversions
    ADD CONSTRAINT textversions_author_uid_fkey FOREIGN KEY (author_uid) REFERENCES users(uid);


--
-- Name: textversions textversions_statement_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY textversions
    ADD CONSTRAINT textversions_statement_uid_fkey FOREIGN KEY (statement_uid) REFERENCES statements(uid);


--
-- Name: users users_group_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_group_uid_fkey FOREIGN KEY (group_uid) REFERENCES groups(uid);


--
-- Name: arguments; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE arguments TO read_only_discussion;


--
-- Name: clicked_arguments; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE clicked_arguments TO read_only_discussion;


--
-- Name: clicked_statements; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE clicked_statements TO read_only_discussion;


--
-- Name: groups; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE groups TO read_only_discussion;


--
-- Name: history; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE history TO read_only_discussion;


--
-- Name: issues; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE issues TO read_only_discussion;


--
-- Name: languages; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE languages TO read_only_discussion;


--
-- Name: last_reviewers_delete; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE last_reviewers_delete TO read_only_discussion;


--
-- Name: last_reviewers_duplicates; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE last_reviewers_duplicates TO read_only_discussion;


--
-- Name: last_reviewers_edit; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE last_reviewers_edit TO read_only_discussion;


--
-- Name: last_reviewers_merge; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE last_reviewers_merge TO read_only_discussion;


--
-- Name: last_reviewers_optimization; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE last_reviewers_optimization TO read_only_discussion;


--
-- Name: last_reviewers_split; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE last_reviewers_split TO read_only_discussion;


--
-- Name: marked_arguments; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE marked_arguments TO read_only_discussion;


--
-- Name: marked_statements; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE marked_statements TO read_only_discussion;


--
-- Name: messages; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE messages TO read_only_discussion;


--
-- Name: optimization_review_locks; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE optimization_review_locks TO read_only_discussion;


--
-- Name: premisegroup_merged; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE premisegroup_merged TO read_only_discussion;


--
-- Name: premisegroup_splitted; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE premisegroup_splitted TO read_only_discussion;


--
-- Name: premisegroups; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE premisegroups TO read_only_discussion;


--
-- Name: premises; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE premises TO read_only_discussion;


--
-- Name: reputation_history; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE reputation_history TO read_only_discussion;


--
-- Name: reputation_reasons; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE reputation_reasons TO read_only_discussion;


--
-- Name: review_canceled; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE review_canceled TO read_only_discussion;


--
-- Name: review_delete_reasons; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE review_delete_reasons TO read_only_discussion;


--
-- Name: review_deletes; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE review_deletes TO read_only_discussion;


--
-- Name: review_duplicates; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE review_duplicates TO read_only_discussion;


--
-- Name: review_edit_values; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE review_edit_values TO read_only_discussion;


--
-- Name: review_edits; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE review_edits TO read_only_discussion;


--
-- Name: review_merge; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE review_merge TO read_only_discussion;


--
-- Name: review_merge_values; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE review_merge_values TO read_only_discussion;


--
-- Name: review_optimizations; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE review_optimizations TO read_only_discussion;


--
-- Name: review_split; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE review_split TO read_only_discussion;


--
-- Name: review_split_values; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE review_split_values TO read_only_discussion;


--
-- Name: revoked_content; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE revoked_content TO read_only_discussion;


--
-- Name: revoked_content_history; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE revoked_content_history TO read_only_discussion;


--
-- Name: revoked_duplicate; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE revoked_duplicate TO read_only_discussion;


--
-- Name: rss; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE rss TO read_only_discussion;


--
-- Name: seen_arguments; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE seen_arguments TO read_only_discussion;


--
-- Name: seen_statements; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE seen_statements TO read_only_discussion;


--
-- Name: settings; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE settings TO read_only_discussion;


--
-- Name: statement_references; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE statement_references TO read_only_discussion;


--
-- Name: statements; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE statements TO read_only_discussion;


--
-- Name: textversions; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE textversions TO read_only_discussion;


--
-- Name: users; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE users TO read_only_discussion;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: public; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public REVOKE ALL ON TABLES  FROM postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT SELECT ON TABLES  TO read_only_discussion;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: public; Owner: dbas
--

ALTER DEFAULT PRIVILEGES FOR ROLE dbas IN SCHEMA public REVOKE ALL ON TABLES  FROM dbas;
ALTER DEFAULT PRIVILEGES FOR ROLE dbas IN SCHEMA public GRANT SELECT ON TABLES  TO read_only_discussion;


--
-- PostgreSQL database dump complete
--

\connect news

SET default_transaction_read_only = off;

--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.3
-- Dumped by pg_dump version 9.6.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: news; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA news;


ALTER SCHEMA news OWNER TO postgres;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: news; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE news (
    uid integer NOT NULL,
    title text NOT NULL,
    author text NOT NULL,
    date timestamp without time zone NOT NULL,
    news text NOT NULL
);


ALTER TABLE news OWNER TO dbas;

--
-- Name: news_uid_seq; Type: SEQUENCE; Schema: public; Owner: dbas
--

CREATE SEQUENCE news_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE news_uid_seq OWNER TO dbas;

--
-- Name: news_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbas
--

ALTER SEQUENCE news_uid_seq OWNED BY news.uid;


--
-- Name: news uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY news ALTER COLUMN uid SET DEFAULT nextval('news_uid_seq'::regclass);


--
-- Data for Name: news; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY news (uid, title, author, date, news) FROM stdin;
1	Finding from our fieldtest	Tobias Krauthoff	2017-07-28 00:00:00	In the meantime we have finished the evaluation of our first fieldtest, which was done carried out to our complete satisfaction. At the moment we are working on our new paper, which will be finished soon. Stay tuned!
2	HCI in Canada	Tobias Krauthoff	2017-07-19 00:00:00	Last week we had the chance to introduce our work about embedding dialog-based discussion into the real world at the HCI in Vancouver. It was a very huge and broad conference with many interesting talks and workshops. Thanks to all listeners during Christians talk.
3	First fieldtest	Tobias Krauthoff	2017-05-09 00:00:00	Today we have started our first, real fieldtest, where we invited every student of computer science to talk about improvements of our study programme. Our number of students drastic increased during the last years, therefore we have to manage some problems like a shortage of space for working places and a lack of place classrooms. Our fieldtest will be supported by sociology students, who will also do an survey based on our metrics we invented mid 2015.
4	Great Test	Tobias Krauthoff	2017-03-09 00:00:00	Finally we have a version of D-BAS which can be used during a large fieldtest at our university. Nevertheless the same version is capable to be viewed by some reviewers of our latest paper. Stay tuned!
5	Docker	Tobias Krauthoff	2017-03-09 00:00:00	Last weeks we have spend to make D-BAS more stable, writing some analyzers as well as dockerize everything. The complete project can be found on https://github.com/hhucn/dbas soon.
6	Experiment	Tobias Krauthoff	2017-02-09 00:00:00	Last week we finished our second experiment at our professorial chair. In short we are very happy with the results and with the first, bigger argumentation map created by inexperienced participants! Now we will fix a few smaller things and looking forward to out first field test!
7	Final version and Captachs	Tobias Krauthoff	2017-01-21 00:00:00	Today we submitted a journal paper about D-BAS and its implementation at Springers CSCW.
8	Final version and Captachs	Tobias Krauthoff	2017-01-03 00:00:00	We have a delayed christmas present for you. D-BAS reached it's first final version including reCAPTCHAS and several minor fixes!
9	Work goes on	Tobias Krauthoff	2016-11-29 00:00:00	After the positive feedback at COMMA16, we decided to do a first field tests with D-BAS at our university. Therefore we are working on current issues, so that we will releasing v1.0. soon.
10	COMMA16	Tobias Krauthoff	2016-09-14 00:00:00	Based on the hard work of the last month, we are attending the 6th International Conference on Computational Models of Argument (COMMA16) in Potsdam. There we are going to show the first demo of D-BAS and present the paper of Krauthoff T., Betz G., Baurmann M. & Mauve, M. (2016) "Dialog-Based Online Argumentation". Looking forward to see you!
11	Review Process	Tobias Krauthoff	2016-09-06 00:00:00	Our first version of the review-module is now online. Every confronting argument can be flagged regarding a specific reason now. Theses flagged argument will be reviewed by other participants, who have enough reputation. Have a look at the review-section!
12	Review Process	Tobias Krauthoff	2016-08-11 00:00:00	I regret that i have neglected the news section, but this is in your interest. In the meantime we are working on an graph view for our argumentation model, a review section for statements and we are improving the ways how we act with each kind of user input. Stay tuned!
13	Sidebar	Tobias Krauthoff	2016-07-05 00:00:00	Today we released a new text-based sidebar for a better experience. Have fun!
14	COMMA16	Tobias Krauthoff	2016-06-24 00:00:00	We are happy to announce, that our paper for the COMMA16 was accepted. In the meantime many little improvements as well as first user tests were done.
15	Development is going on	Tobias Krauthoff	2016-04-05 00:00:00	Recently we improved some features, which will be released in future. Firstly there will be an island view for every argument, where the participants can see every premise for current reactions. Secondly the opinion barometer is still under development. For a more recent update, have a look at our imprint.
16	History Management	Tobias Krauthoff	2016-04-26 00:00:00	We have changed D-BAS' history management. Now you can bookmark any link in any discussion and your history will always be with you!
17	COMMA16	Tobias Krauthoff	2016-04-05 00:00:00	After much work, testing and debugging, we now have version of D-BAS, which will be submitted  to <a href="http://www.ling.uni-potsdam.de/comma2016" target="_blank">COMMA 2016</a>.
18	Speech Bubble System	Tobias Krauthoff	2016-03-02 00:00:00	After one week of testing, we released a new minor version of D-BAS. Instead of the text presentation,we will use chat-like style :) Come on and try it! Additionally anonymous users will have a history now!
19	Notification System	Tobias Krauthoff	2016-02-16 00:00:00	Yesterday we have develope a minimal notification system. This system could send information to every author, if one of their statement was edited. More features are coming soon!
20	Premisegroups	Tobias Krauthoff	2016-02-09 00:00:00	Now we have a mechanism for unclear statements. For example the user enters "I want something because A and B". The we do not know, whether A and B must hold at the same time, or if she wants something when A or B holds. Therefore the system requests feedback.
21	Voting Model	Tobias Krauthoff	2016-01-05 00:00:00	Currently we are improving out model of voting for arguments as well as statements. Therefore we are working together with our colleagues from the theoretical computer science... because D-BAS data structure can be formalized to be compatible with frameworks of Dung.
22	API	Tobias Krauthoff	2016-01-29 00:00:00	Now D-BAS has an API. Just replace the "discuss"-tag in your url with api to get your current steps raw data.
23	Refactoring	Tobias Krauthoff	2016-01-27 00:00:00	D-BAS refactored the last two weeks. During this time, a lot of JavaScript was removed. Therefore D-BAS uses Chameleon with TAL in the Pyramid-Framework. So D-BAS will be more stable and faster. The next period all functions will be tested and recovered.
24	Island View and Pictures	Tobias Krauthoff	2016-01-06 00:00:00	D-BAS will be more personal and results driven. Therefore the new release has profile pictures for everyone. They are powered by gravatar and are based on a md5-hash of the users email. Next to this a new view was published - the island view. Do not be shy and try it in discussions ;-) Last improvement just collects the attacks and supports for arguments...this is needed for our next big thing :) Stay tuned!
25	Happy new Year	Tobias Krauthoff	2016-01-01 00:00:00	Frohes Neues Jahr ... Bonne Annee ... Happy New Year ... Feliz Ano Nuevo ... Feliz Ano Novo
26	Piwik	Tobias Krauthoff	2015-12-08 00:00:00	Today Piwik was installed. It will help to improve the services of D-BAS!
27	Logic improvements	Tobias Krauthoff	2015-12-01 00:00:00	Every week we try to improve the look and feel of the discussions navigation. Sometimes just a few words are edited, but on other day the logic itself gets an update. So keep on testing :)
28	Breadcrumbs	Tobias Krauthoff	2015-11-24 00:00:00	Now we have a breadcrumbs with shortcuts for every step in our discussion. This feature will be im improved soon!
29	Improved Bootstrapping	Tobias Krauthoff	2015-11-16 00:00:00	Bootstraping is one of the main challenges in discussion. Therefore we have a two-step process for this task!
30	Design Update	Tobias Krauthoff	2015-11-11 00:00:00	Today we released a new material-oriented design. Enjoy it!
31	Stable release	Tobias Krauthoff	2015-11-10 00:00:00	After two weeks of debugging, a first and stable version is online. Now we can start with the interesting things!
32	Different topics	Tobias Krauthoff	2015-10-15 00:00:00	Since today we can switch between different topics :) Unfortunately this feature is not really tested ;-)
33	First steps	Tobias Krauthoff	2014-12-01 00:00:00	I've started with with my PhD.
34	Start	Tobias Krauthoff	2015-04-14 00:00:00	I've started with the Prototype.
35	First mockup	Tobias Krauthoff	2015-05-01 00:00:00	The webpage has now a contact, login and register site.
36	Page is growing	Tobias Krauthoff	2015-05-05 00:00:00	The contact page is now working as well as the password-request option.
37	First set of tests	Tobias Krauthoff	2015-05-06 00:00:00	Finished first set of unit- and integration tests for the database and frontend.
38	System will be build up	Tobias Krauthoff	2015-05-01 00:00:00	Currently I am working a lot at the system. This work includes:<br><ul><li>frontend-design with CSS and jQuery</li><li>backend-development with pything</li><li>development of unit- and integration tests</li><li>a database scheme</li><li>validating and deserializing data with <a href="http://docs.pylonsproject.org/projects/colander/en/latest/">Colander</a></li><li>translating string with <a href="http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/i18n.html#localization-deployment-settings">internationalization</a></li></ul>
39	Workshop in Karlsruhe	Tobias Krauthoff	2015-05-07 00:00:00	The working group 'functionality' will drive to Karlsruhe for a workshop with Jun.-Prof. Dr. Betz as well as with C. Voigt until 08.05.2015. Our main topics will be the measurement of quality of discussions and the design of online-participation. I think, this will be very interesting!
40	About the Workshop in Karlsruhe	Tobias Krauthoff	2015-05-09 00:00:00	The workshop was very interesting. We have had very interesting talks and got much great feedback vom Jun.-Prof. Dr. Betz and Mr. Voigt. A repetition will be planed for the middle of july.
41	Settings	Tobias Krauthoff	2015-05-10 00:00:00	New part of the website is finished: a settings page for every user.
42	I18N + L10N	Tobias Krauthoff	2015-05-12 00:00:00	D-BAS, now with internationalization and translation.
43	No I18N + L10N	Tobias Krauthoff	2015-05-18 00:00:00	Interationalization and localization is much more difficult than described by pyramid. This has something todo with Chameleon 2, Lingua and Babel, so this feature has to wait.
44	New logic for inserting	Tobias Krauthoff	2015-10-14 00:00:00	Logic for inserting statements was redone. Every time, where the user can add information via a text area, only the area is visible, which is logically correct. Therefore the decisions are based on argumentation theory.
45	JS Starts	Tobias Krauthoff	2015-05-18 00:00:00	Today started the funny part about the dialog based part, embedded in the content page.
46	Tests and JS	Tobias Krauthoff	2015-05-26 00:00:00	Front-end tests with Splinter are now finished. They are great and easy to manage. Additionally I'am working on JS, so we can navigate in a static graph. Next to this, the I18N is waiting...
47	Sharing	Tobias Krauthoff	2015-05-27 00:00:00	Every news can now be shared via FB, G+, Twitter and Mail. Not very important, but in some kind it is...
48	Admin Interface	Tobias Krauthoff	2015-05-29 00:00:00	Everything is growing, we have now a little admin interface and a navigation for the discussion is finished, but this is very basic and simple
49	Workshop	Tobias Krauthoff	2015-05-27 00:00:00	Today: A new workshop at the O.A.S.E. :)
50	Simple Navigation ready	Tobias Krauthoff	2015-06-09 00:00:00	First beta of D-BAS navigation is now ready. Within this kind the user will be permanently confronted with arguments, which have a attack relation to the current selected argument/position. For an justification the user can select out of all arguments, which have a attack relation to the 'attacking' argument. Unfortunately the support-relation are currently useless except for the justification for the position at start.
51	Simple Navigation was improved	Tobias Krauthoff	2015-06-19 00:00:00	Because the first kind of navigation was finished recently, D-BAS is now dynamically. That means, that each user can add positions and arguments on his own.<br><i>Open issues</i> are i18n, a framework for JS-tests as well as the content of the popups.
52	Edit/Changelog	Tobias Krauthoff	2015-06-24 00:00:00	Now, each user can edit positions and arguments. All changes will be saved and can be watched. Future work is the chance to edit the relations between positions.
53	Session Management / CSRF	Tobias Krauthoff	2015-06-25 00:00:00	D-BAS is no able to manage a session as well as it has protection against CSRF.
54	Design & Research	Tobias Krauthoff	2015-07-13 00:00:00	D-BAS is still under construction. Meanwhile the index page was recreated and we are improving our algorithm for the guided view mode. Next to this we are inventing a bunch of metrics for measuring the quality of discussion in several software programs.
55	i18n	Tobias Krauthoff	2015-07-22 00:00:00	Still working on i18n-problems of chameleon templates due to lingua. If this is fixed, i18n of jQuery will happen. Afterwards l10n will take place.
56	i18n/l10n	Tobias Krauthoff	2015-07-28 00:00:00	Internationalization is now working :)
57	Long time, no see!	Tobias Krauthoff	2015-08-31 00:00:00	In the mean time we have developed a new, better, more logically data structure. Additionally the navigation was refreshed.
58	New URL-Schemes	Tobias Krauthoff	2015-09-01 00:00:00	Now D-BAS has unique urls for the discussion, therefore these urls can be shared.
59	Vacation done	Tobias Krauthoff	2015-09-23 00:00:00	After two and a half weeks of vacation a new feature was done. Hence anonymous users can participate, the discussion is open for all, but committing and editing statements is for registered users only.
60	Anonymous users after vacation	Tobias Krauthoff	2015-09-24 00:00:00	After two and a half week of vacation we have a new feature. The discussion is now available for anonymous users, therefore everyone can participate, but only registered users can make and edit statements.
\.


--
-- Name: news_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('news_uid_seq', 60, true);


--
-- Name: news news_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY news
    ADD CONSTRAINT news_pkey PRIMARY KEY (uid);


--
-- Name: news; Type: ACL; Schema: -; Owner: postgres
--

GRANT ALL ON SCHEMA news TO writer;


--
-- PostgreSQL database dump complete
--

\connect postgres

SET default_transaction_read_only = off;

--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.3
-- Dumped by pg_dump version 9.6.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: postgres; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON DATABASE postgres IS 'default administrative connection database';


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: public; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public REVOKE ALL ON TABLES  FROM postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT ALL ON TABLES  TO writer;


--
-- PostgreSQL database dump complete
--

\connect template1

SET default_transaction_read_only = off;

--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.3
-- Dumped by pg_dump version 9.6.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: template1; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON DATABASE template1 IS 'default template for new databases';


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database cluster dump complete
--

