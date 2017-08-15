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
    is_okay boolean NOT NULL,
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
    is_okay boolean NOT NULL,
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
-- Name: statements_merged; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE statements_merged (
    uid integer NOT NULL,
    review_uid integer,
    statement_uid integer,
    new_statement_uid integer,
    "timestamp" timestamp without time zone
);


ALTER TABLE statements_merged OWNER TO dbas;

--
-- Name: statements_merged_uid_seq; Type: SEQUENCE; Schema: public; Owner: dbas
--

CREATE SEQUENCE statements_merged_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE statements_merged_uid_seq OWNER TO dbas;

--
-- Name: statements_merged_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbas
--

ALTER SEQUENCE statements_merged_uid_seq OWNED BY statements_merged.uid;


--
-- Name: statements_splitted; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE statements_splitted (
    uid integer NOT NULL,
    review_uid integer,
    new_statement_uid integer,
    "timestamp" timestamp without time zone
);


ALTER TABLE statements_splitted OWNER TO dbas;

--
-- Name: statements_splitted_uid_seq; Type: SEQUENCE; Schema: public; Owner: dbas
--

CREATE SEQUENCE statements_splitted_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE statements_splitted_uid_seq OWNER TO dbas;

--
-- Name: statements_splitted_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbas
--

ALTER SEQUENCE statements_splitted_uid_seq OWNED BY statements_splitted.uid;


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
-- Name: statements_merged uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY statements_merged ALTER COLUMN uid SET DEFAULT nextval('statements_merged_uid_seq'::regclass);


--
-- Name: statements_splitted uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY statements_splitted ALTER COLUMN uid SET DEFAULT nextval('statements_splitted_uid_seq'::regclass);


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
1	1	2	\N	f	1	2017-08-15 08:49:42.789393	2	t
2	2	2	\N	t	1	2017-08-15 08:49:42.789551	2	f
3	3	2	\N	f	1	2017-08-15 08:49:42.789666	2	f
4	4	3	\N	t	1	2017-08-15 08:49:42.789831	2	f
5	5	3	\N	f	1	2017-08-15 08:49:42.790028	2	f
8	8	4	\N	t	1	2017-08-15 08:49:42.790547	2	f
10	10	11	\N	f	1	2017-08-15 08:49:42.790966	2	f
11	11	2	\N	t	1	2017-08-15 08:49:42.791164	2	f
12	12	2	\N	t	1	2017-08-15 08:49:42.791366	2	f
15	15	5	\N	t	1	2017-08-15 08:49:42.792016	2	f
16	16	5	\N	f	1	2017-08-15 08:49:42.792244	2	f
17	17	5	\N	t	1	2017-08-15 08:49:42.792459	2	f
19	19	6	\N	t	1	2017-08-15 08:49:42.792777	2	f
20	20	6	\N	f	1	2017-08-15 08:49:42.792885	2	f
21	21	6	\N	f	1	2017-08-15 08:49:42.792998	2	f
23	23	14	\N	f	1	2017-08-15 08:49:42.793299	2	f
24	24	14	\N	t	1	2017-08-15 08:49:42.793383	2	f
26	26	14	\N	t	1	2017-08-15 08:49:42.793566	2	f
27	27	15	\N	t	1	2017-08-15 08:49:42.793648	2	f
28	27	16	\N	t	1	2017-08-15 08:49:42.793729	2	f
29	28	15	\N	t	1	2017-08-15 08:49:42.793809	2	f
30	29	15	\N	f	1	2017-08-15 08:49:42.793888	2	f
32	31	36	\N	t	3	2017-08-15 08:49:42.794047	1	f
34	33	39	\N	t	3	2017-08-15 08:49:42.794203	1	f
35	34	41	\N	t	1	2017-08-15 08:49:42.794288	1	f
36	35	36	\N	f	1	2017-08-15 08:49:42.794371	1	f
39	38	37	\N	t	1	2017-08-15 08:49:42.794609	1	f
40	39	37	\N	t	1	2017-08-15 08:49:42.794689	1	f
41	41	46	\N	f	1	2017-08-15 08:49:42.794768	1	f
42	42	37	\N	f	1	2017-08-15 08:49:42.794925	1	f
44	44	50	\N	f	1	2017-08-15 08:49:42.795081	1	f
46	45	50	\N	t	1	2017-08-15 08:49:42.79516	1	f
47	46	38	\N	t	1	2017-08-15 08:49:42.795241	1	f
49	48	38	\N	f	1	2017-08-15 08:49:42.795398	1	f
50	49	49	\N	f	1	2017-08-15 08:49:42.795477	1	f
51	51	58	\N	f	1	2017-08-15 08:49:42.795638	4	f
54	54	59	\N	t	1	2017-08-15 08:49:42.795877	4	f
55	55	59	\N	f	1	2017-08-15 08:49:42.796003	4	f
56	56	60	\N	t	1	2017-08-15 08:49:42.796092	4	f
57	57	60	\N	f	1	2017-08-15 08:49:42.796174	4	f
58	50	58	\N	t	1	2017-08-15 08:49:42.795557	4	f
59	61	67	\N	t	1	2017-08-15 08:49:42.796257	4	f
60	62	69	\N	t	1	2017-08-15 08:49:42.796338	5	f
61	63	69	\N	t	1	2017-08-15 08:49:42.79642	5	f
62	64	69	\N	f	1	2017-08-15 08:49:42.796501	5	f
63	65	70	\N	f	1	2017-08-15 08:49:42.796581	5	f
64	66	70	\N	f	1	2017-08-15 08:49:42.796659	5	f
65	67	76	\N	t	1	2017-08-15 08:49:42.796739	7	f
66	68	76	\N	f	1	2017-08-15 08:49:42.796819	7	f
67	69	76	\N	f	1	2017-08-15 08:49:42.796899	7	f
68	70	79	\N	f	1	2017-08-15 08:49:42.796979	7	f
6	6	\N	4	f	1	2017-08-15 08:49:42.790197	2	f
7	7	\N	5	f	1	2017-08-15 08:49:42.79037	2	f
9	9	\N	8	f	1	2017-08-15 08:49:42.790744	2	f
13	13	\N	12	f	1	2017-08-15 08:49:42.791576	2	f
14	14	\N	13	f	1	2017-08-15 08:49:42.791799	2	f
18	18	\N	2	f	1	2017-08-15 08:49:42.792643	2	f
22	22	\N	3	f	1	2017-08-15 08:49:42.793207	2	f
25	25	\N	11	f	1	2017-08-15 08:49:42.793479	2	f
31	30	\N	15	f	1	2017-08-15 08:49:42.793966	2	f
33	32	\N	32	f	3	2017-08-15 08:49:42.794124	1	f
37	36	\N	36	f	1	2017-08-15 08:49:42.79445	1	f
38	37	\N	36	f	1	2017-08-15 08:49:42.794527	1	f
43	43	\N	42	f	1	2017-08-15 08:49:42.795002	1	f
45	40	\N	39	f	1	2017-08-15 08:49:42.794846	1	f
48	47	\N	47	f	1	2017-08-15 08:49:42.795319	1	f
52	52	\N	58	f	1	2017-08-15 08:49:42.795719	4	f
53	53	\N	51	f	1	2017-08-15 08:49:42.795798	4	f
69	71	\N	65	f	1	2017-08-15 08:49:42.797071	7	f
\.


--
-- Name: arguments_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('arguments_uid_seq', 69, true);


--
-- Data for Name: clicked_arguments; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY clicked_arguments (uid, argument_uid, author_uid, "timestamp", is_up_vote, is_valid) FROM stdin;
772	1	7	2017-07-25 08:49:50.548008	t	t
773	1	13	2017-08-04 08:49:50.548175	f	t
774	1	19	2017-07-29 08:49:50.548258	f	t
775	1	29	2017-08-02 08:49:50.548327	f	t
776	2	20	2017-08-06 08:49:50.548393	t	t
777	2	35	2017-08-07 08:49:50.548455	t	t
778	2	32	2017-08-03 08:49:50.548518	t	t
779	2	29	2017-08-12 08:49:50.54858	t	t
780	2	21	2017-08-09 08:49:50.548641	t	t
781	2	28	2017-07-25 08:49:50.548702	t	t
782	2	27	2017-08-15 08:49:50.548761	t	t
783	2	36	2017-07-30 08:49:50.54882	t	t
784	2	25	2017-08-03 08:49:50.548879	t	t
785	2	26	2017-07-31 08:49:50.54894	t	t
786	2	34	2017-08-10 08:49:50.549	t	t
787	2	29	2017-07-28 08:49:50.549058	t	t
788	2	23	2017-07-21 08:49:50.549117	t	t
789	2	19	2017-08-05 08:49:50.549208	t	t
790	2	12	2017-07-28 08:49:50.549268	t	t
791	2	33	2017-07-24 08:49:50.549328	t	t
792	2	13	2017-07-24 08:49:50.549389	t	t
793	2	16	2017-07-24 08:49:50.549448	t	t
794	2	9	2017-08-13 08:49:50.54953	t	t
795	2	10	2017-08-15 08:49:50.549589	t	t
796	2	37	2017-07-30 08:49:50.549649	t	t
797	2	18	2017-08-08 08:49:50.549709	t	t
798	2	7	2017-08-11 08:49:50.549768	t	t
799	2	31	2017-08-04 08:49:50.549827	t	t
800	2	8	2017-08-07 08:49:50.549886	t	t
801	2	24	2017-07-28 08:49:50.549944	t	t
802	2	27	2017-08-10 08:49:50.550002	f	t
803	2	25	2017-08-13 08:49:50.55006	f	t
804	2	26	2017-07-25 08:49:50.550118	f	t
805	2	29	2017-07-29 08:49:50.550176	f	t
806	2	23	2017-08-13 08:49:50.550246	f	t
807	2	29	2017-07-29 08:49:50.550344	f	t
808	2	37	2017-08-08 08:49:50.550412	f	t
809	2	10	2017-07-27 08:49:50.550471	f	t
810	2	8	2017-07-25 08:49:50.550543	f	t
811	2	20	2017-07-29 08:49:50.55061	f	t
812	2	32	2017-08-14 08:49:50.550668	f	t
813	2	12	2017-08-15 08:49:50.550727	f	t
814	2	35	2017-07-23 08:49:50.550784	f	t
815	3	10	2017-08-06 08:49:50.550843	t	t
816	3	36	2017-07-24 08:49:50.550901	t	t
817	3	7	2017-07-27 08:49:50.550961	t	t
818	3	35	2017-07-22 08:49:50.55102	t	t
819	3	29	2017-08-15 08:49:50.551079	t	t
820	3	25	2017-07-31 08:49:50.551138	t	t
821	3	12	2017-08-03 08:49:50.551197	t	t
822	3	16	2017-07-24 08:49:50.551255	f	t
823	3	14	2017-08-03 08:49:50.551314	f	t
824	3	29	2017-07-29 08:49:50.551372	f	t
825	3	9	2017-07-27 08:49:50.551432	f	t
826	3	13	2017-07-26 08:49:50.551492	f	t
827	3	21	2017-07-26 08:49:50.551551	f	t
828	5	13	2017-07-25 08:49:50.551609	t	t
829	5	20	2017-07-23 08:49:50.551668	t	t
830	5	11	2017-08-01 08:49:50.551726	t	t
831	5	28	2017-08-11 08:49:50.551785	t	t
832	5	13	2017-08-02 08:49:50.551843	f	t
833	5	23	2017-07-22 08:49:50.551901	f	t
834	5	25	2017-08-06 08:49:50.551959	f	t
835	5	31	2017-08-09 08:49:50.552018	f	t
836	5	34	2017-08-12 08:49:50.552075	f	t
837	5	7	2017-08-10 08:49:50.552134	f	t
838	5	19	2017-07-22 08:49:50.552193	f	t
839	8	27	2017-08-08 08:49:50.552253	t	t
840	8	17	2017-07-23 08:49:50.55231	t	t
841	8	36	2017-07-29 08:49:50.552369	t	t
842	8	13	2017-08-06 08:49:50.552428	t	t
843	8	29	2017-08-13 08:49:50.552494	t	t
844	8	32	2017-08-12 08:49:50.552552	t	t
845	8	32	2017-08-03 08:49:50.552609	f	t
846	8	17	2017-07-26 08:49:50.552666	f	t
847	8	18	2017-08-07 08:49:50.552723	f	t
848	8	36	2017-07-30 08:49:50.552779	f	t
849	8	7	2017-07-29 08:49:50.552836	f	t
850	8	8	2017-08-06 08:49:50.552894	f	t
851	10	37	2017-08-14 08:49:50.552951	t	t
852	10	27	2017-08-04 08:49:50.553009	t	t
853	10	17	2017-08-14 08:49:50.553066	t	t
854	10	33	2017-07-29 08:49:50.553141	t	t
855	10	22	2017-08-07 08:49:50.553223	t	t
856	10	16	2017-07-27 08:49:50.553282	t	t
857	10	11	2017-07-22 08:49:50.55334	t	t
858	10	12	2017-07-31 08:49:50.5534	f	t
859	10	35	2017-07-28 08:49:50.553458	f	t
860	10	21	2017-08-08 08:49:50.553515	f	t
861	10	37	2017-08-12 08:49:50.553572	f	t
862	10	7	2017-08-06 08:49:50.55363	f	t
863	10	8	2017-07-31 08:49:50.553687	f	t
864	10	24	2017-08-02 08:49:50.553744	f	t
865	10	15	2017-07-23 08:49:50.553802	f	t
866	10	18	2017-07-26 08:49:50.55388	f	t
867	11	9	2017-08-07 08:49:50.553959	t	t
868	11	29	2017-08-10 08:49:50.554047	t	t
869	11	31	2017-07-25 08:49:50.554114	t	t
870	11	17	2017-08-02 08:49:50.554171	t	t
871	11	18	2017-07-29 08:49:50.554228	t	t
872	12	34	2017-08-14 08:49:50.554284	t	t
873	12	23	2017-08-12 08:49:50.554341	t	t
874	12	21	2017-07-24 08:49:50.554398	t	t
875	12	18	2017-08-02 08:49:50.554454	t	t
876	12	15	2017-08-06 08:49:50.554511	t	t
877	12	25	2017-07-26 08:49:50.554569	t	t
878	12	14	2017-08-07 08:49:50.55464	t	t
879	12	24	2017-08-01 08:49:50.554708	t	t
880	12	16	2017-07-31 08:49:50.554767	t	t
881	12	37	2017-07-30 08:49:50.554824	t	t
882	12	29	2017-07-23 08:49:50.554882	t	t
883	12	28	2017-07-26 08:49:50.554939	t	t
884	12	9	2017-08-03 08:49:50.554997	t	t
885	12	17	2017-07-22 08:49:50.555054	t	t
886	12	36	2017-08-02 08:49:50.555112	t	t
887	12	35	2017-07-28 08:49:50.555169	t	t
888	12	12	2017-08-09 08:49:50.555227	t	t
889	12	13	2017-08-03 08:49:50.555283	t	t
890	12	11	2017-08-05 08:49:50.55534	t	t
891	12	35	2017-07-23 08:49:50.555397	f	t
892	12	32	2017-07-29 08:49:50.555466	f	t
893	12	10	2017-07-30 08:49:50.555527	f	t
894	12	18	2017-08-15 08:49:50.555589	f	t
895	12	25	2017-07-21 08:49:50.555649	f	t
896	12	15	2017-07-26 08:49:50.555709	f	t
897	12	22	2017-08-15 08:49:50.555769	f	t
898	12	17	2017-07-23 08:49:50.555829	f	t
899	12	24	2017-08-13 08:49:50.555889	f	t
900	12	14	2017-08-04 08:49:50.55595	f	t
901	12	19	2017-08-01 08:49:50.55601	f	t
902	12	16	2017-07-21 08:49:50.55607	f	t
903	12	29	2017-08-02 08:49:50.55613	f	t
904	12	21	2017-07-21 08:49:50.556191	f	t
905	12	36	2017-08-08 08:49:50.556251	f	t
906	12	23	2017-08-03 08:49:50.556312	f	t
907	12	33	2017-08-04 08:49:50.556373	f	t
908	12	28	2017-08-04 08:49:50.556442	f	t
909	12	13	2017-08-03 08:49:50.556498	f	t
910	12	26	2017-08-05 08:49:50.556555	f	t
911	12	9	2017-07-22 08:49:50.556611	f	t
912	12	11	2017-07-29 08:49:50.556668	f	t
913	12	20	2017-08-14 08:49:50.556724	f	t
914	15	37	2017-08-01 08:49:50.556781	t	t
915	15	29	2017-08-05 08:49:50.556839	t	t
916	15	25	2017-07-21 08:49:50.556896	t	t
917	15	14	2017-07-31 08:49:50.556954	t	t
918	15	23	2017-07-27 08:49:50.557011	t	t
919	15	12	2017-08-08 08:49:50.557067	f	t
920	15	11	2017-08-13 08:49:50.557142	f	t
921	16	28	2017-07-24 08:49:50.557215	t	t
922	16	21	2017-07-30 08:49:50.557284	t	t
923	16	7	2017-07-26 08:49:50.557351	t	t
924	16	28	2017-08-01 08:49:50.557409	f	t
925	16	11	2017-07-24 08:49:50.557466	f	t
926	16	27	2017-07-25 08:49:50.557522	f	t
927	16	13	2017-07-24 08:49:50.557579	f	t
928	16	19	2017-08-08 08:49:50.557636	f	t
929	16	15	2017-07-25 08:49:50.557694	f	t
930	16	7	2017-08-14 08:49:50.557751	f	t
931	16	29	2017-08-07 08:49:50.557808	f	t
932	16	16	2017-07-24 08:49:50.557865	f	t
933	16	23	2017-07-21 08:49:50.557922	f	t
934	16	20	2017-08-06 08:49:50.557979	f	t
935	16	33	2017-08-02 08:49:50.558036	f	t
936	16	14	2017-07-31 08:49:50.558092	f	t
937	16	10	2017-08-11 08:49:50.558149	f	t
938	16	9	2017-07-23 08:49:50.558205	f	t
939	16	18	2017-08-13 08:49:50.558261	f	t
940	16	21	2017-07-22 08:49:50.558317	f	t
941	16	8	2017-08-02 08:49:50.558374	f	t
942	16	37	2017-07-31 08:49:50.55843	f	t
943	16	24	2017-08-05 08:49:50.558486	f	t
944	17	22	2017-08-04 08:49:50.558543	t	t
945	17	35	2017-07-29 08:49:50.5586	t	t
946	17	29	2017-08-10 08:49:50.558657	t	t
947	17	34	2017-07-23 08:49:50.558713	t	t
948	17	37	2017-08-05 08:49:50.55877	t	t
949	17	8	2017-08-04 08:49:50.558826	t	t
950	17	14	2017-08-14 08:49:50.558883	t	t
951	17	27	2017-08-15 08:49:50.558941	t	t
952	17	20	2017-08-07 08:49:50.558998	f	t
953	17	14	2017-07-22 08:49:50.559055	f	t
954	17	22	2017-08-04 08:49:50.559112	f	t
955	17	12	2017-08-08 08:49:50.559169	f	t
956	19	9	2017-07-23 08:49:50.559237	t	t
957	19	27	2017-07-27 08:49:50.559304	t	t
958	19	29	2017-07-31 08:49:50.55936	t	t
959	19	36	2017-07-23 08:49:50.559417	t	t
960	19	19	2017-07-31 08:49:50.559485	t	t
961	19	21	2017-08-11 08:49:50.559545	t	t
962	19	8	2017-07-31 08:49:50.559605	t	t
963	19	18	2017-07-26 08:49:50.559664	t	t
964	19	18	2017-08-07 08:49:50.559725	f	t
965	19	24	2017-07-24 08:49:50.559785	f	t
966	19	20	2017-08-03 08:49:50.559849	f	t
967	19	27	2017-07-25 08:49:50.559911	f	t
968	19	26	2017-07-29 08:49:50.559972	f	t
969	19	29	2017-08-08 08:49:50.560032	f	t
970	19	17	2017-08-15 08:49:50.560093	f	t
971	19	8	2017-08-01 08:49:50.560153	f	t
972	19	15	2017-08-01 08:49:50.560214	f	t
973	19	25	2017-08-01 08:49:50.560274	f	t
974	19	12	2017-08-03 08:49:50.560334	f	t
975	19	13	2017-08-10 08:49:50.560395	f	t
976	19	10	2017-08-09 08:49:50.560463	f	t
977	19	9	2017-08-11 08:49:50.56052	f	t
978	19	22	2017-07-26 08:49:50.560576	f	t
979	19	21	2017-08-15 08:49:50.560633	f	t
980	19	14	2017-08-15 08:49:50.560691	f	t
981	19	29	2017-08-01 08:49:50.56075	f	t
982	19	23	2017-08-01 08:49:50.560809	f	t
983	20	16	2017-08-06 08:49:50.560866	t	t
984	20	18	2017-07-23 08:49:50.560924	t	t
985	20	17	2017-07-29 08:49:50.560981	t	t
986	20	7	2017-07-30 08:49:50.561038	t	t
987	20	22	2017-08-06 08:49:50.561094	t	t
988	20	37	2017-08-02 08:49:50.561181	t	t
989	20	36	2017-08-08 08:49:50.561249	t	t
990	20	19	2017-08-09 08:49:50.561305	t	t
991	20	16	2017-07-27 08:49:50.561362	f	t
992	21	13	2017-08-06 08:49:50.561419	t	t
993	21	14	2017-08-13 08:49:50.561476	t	t
994	21	12	2017-07-27 08:49:50.561535	t	t
995	21	21	2017-07-27 08:49:50.561592	f	t
996	21	26	2017-08-11 08:49:50.561649	f	t
997	21	32	2017-08-10 08:49:50.561706	f	t
998	21	12	2017-08-14 08:49:50.561762	f	t
999	21	10	2017-08-14 08:49:50.561819	f	t
1000	21	27	2017-08-11 08:49:50.561876	f	t
1001	21	13	2017-08-11 08:49:50.561933	f	t
1002	21	8	2017-08-12 08:49:50.561991	f	t
1003	21	23	2017-07-29 08:49:50.562047	f	t
1004	21	37	2017-07-22 08:49:50.562104	f	t
1005	21	29	2017-07-30 08:49:50.562161	f	t
1006	21	33	2017-08-07 08:49:50.562218	f	t
1007	21	36	2017-08-14 08:49:50.562275	f	t
1008	21	17	2017-07-31 08:49:50.562332	f	t
1009	21	18	2017-08-01 08:49:50.562388	f	t
1010	21	22	2017-08-07 08:49:50.562445	f	t
1011	21	20	2017-08-11 08:49:50.562501	f	t
1012	21	24	2017-07-27 08:49:50.562559	f	t
1013	21	9	2017-08-10 08:49:50.562616	f	t
1014	21	11	2017-08-05 08:49:50.562673	f	t
1015	21	28	2017-08-06 08:49:50.56273	f	t
1016	21	14	2017-08-11 08:49:50.562786	f	t
1017	21	7	2017-07-28 08:49:50.562844	f	t
1018	21	19	2017-08-03 08:49:50.562901	f	t
1019	21	16	2017-07-29 08:49:50.562958	f	t
1020	21	34	2017-08-15 08:49:50.563015	f	t
1021	23	16	2017-08-03 08:49:50.563071	t	t
1022	23	31	2017-08-01 08:49:50.563129	t	t
1023	23	18	2017-07-25 08:49:50.563185	t	t
1024	23	29	2017-07-24 08:49:50.563242	t	t
1025	24	7	2017-08-12 08:49:50.563299	f	t
1026	24	20	2017-08-11 08:49:50.563356	f	t
1027	26	29	2017-07-22 08:49:50.563412	t	t
1028	26	15	2017-08-10 08:49:50.563469	t	t
1029	26	21	2017-08-13 08:49:50.563557	t	t
1030	26	22	2017-08-10 08:49:50.563616	t	t
1031	26	28	2017-08-13 08:49:50.563659	t	t
1032	26	25	2017-07-22 08:49:50.56369	t	t
1033	26	27	2017-08-10 08:49:50.56372	t	t
1034	26	9	2017-07-21 08:49:50.56375	t	t
1035	26	12	2017-07-24 08:49:50.563779	t	t
1036	26	17	2017-08-02 08:49:50.563809	t	t
1037	26	23	2017-08-09 08:49:50.563838	t	t
1038	26	19	2017-08-04 08:49:50.563867	t	t
1039	26	18	2017-08-12 08:49:50.563896	t	t
1040	26	32	2017-07-23 08:49:50.563925	t	t
1041	26	29	2017-08-09 08:49:50.563955	t	t
1042	26	19	2017-07-31 08:49:50.563985	f	t
1043	26	16	2017-08-06 08:49:50.564014	f	t
1044	26	28	2017-08-09 08:49:50.564044	f	t
1045	26	34	2017-07-22 08:49:50.564073	f	t
1046	26	13	2017-08-01 08:49:50.564102	f	t
1047	26	11	2017-08-03 08:49:50.56413	f	t
1048	26	10	2017-08-04 08:49:50.564159	f	t
1049	26	15	2017-08-05 08:49:50.564189	f	t
1050	26	17	2017-08-15 08:49:50.564218	f	t
1051	26	35	2017-08-15 08:49:50.564247	f	t
1052	26	20	2017-07-23 08:49:50.564276	f	t
1053	26	26	2017-07-29 08:49:50.564305	f	t
1054	26	21	2017-08-09 08:49:50.564334	f	t
1055	26	32	2017-07-22 08:49:50.564363	f	t
1056	26	29	2017-08-13 08:49:50.564391	f	t
1057	26	22	2017-07-21 08:49:50.56442	f	t
1058	26	25	2017-07-25 08:49:50.564449	f	t
1059	26	33	2017-08-15 08:49:50.564478	f	t
1060	26	29	2017-07-25 08:49:50.564507	f	t
1061	26	18	2017-07-27 08:49:50.564536	f	t
1062	26	37	2017-08-12 08:49:50.564564	f	t
1063	26	31	2017-07-29 08:49:50.564593	f	t
1064	26	9	2017-08-12 08:49:50.564622	f	t
1065	26	23	2017-07-21 08:49:50.56465	f	t
1066	26	7	2017-07-22 08:49:50.564679	f	t
1067	27	8	2017-07-28 08:49:50.564708	f	t
1068	27	11	2017-07-23 08:49:50.564738	f	t
1069	27	18	2017-07-22 08:49:50.564767	f	t
1070	27	36	2017-07-29 08:49:50.564796	f	t
1071	27	13	2017-08-13 08:49:50.564825	f	t
1072	27	19	2017-07-29 08:49:50.564855	f	t
1073	27	35	2017-07-26 08:49:50.564884	f	t
1074	27	37	2017-08-02 08:49:50.564914	f	t
1075	27	15	2017-08-10 08:49:50.564943	f	t
1076	27	34	2017-08-11 08:49:50.564973	f	t
1077	27	32	2017-08-12 08:49:50.565002	f	t
1078	27	7	2017-07-27 08:49:50.565031	f	t
1079	27	22	2017-07-27 08:49:50.565061	f	t
1080	28	28	2017-08-05 08:49:50.56509	t	t
1081	28	33	2017-08-10 08:49:50.565119	t	t
1082	28	17	2017-07-29 08:49:50.565157	f	t
1083	28	10	2017-07-25 08:49:50.565186	f	t
1084	28	25	2017-07-26 08:49:50.565215	f	t
1085	28	35	2017-08-15 08:49:50.565244	f	t
1086	28	37	2017-07-25 08:49:50.565273	f	t
1087	28	32	2017-07-31 08:49:50.565302	f	t
1088	28	36	2017-08-14 08:49:50.565331	f	t
1089	28	28	2017-07-31 08:49:50.56536	f	t
1090	28	29	2017-08-01 08:49:50.565389	f	t
1091	29	36	2017-08-04 08:49:50.565418	t	t
1092	29	10	2017-07-27 08:49:50.565447	f	t
1093	29	25	2017-08-02 08:49:50.565477	f	t
1094	29	12	2017-08-03 08:49:50.565506	f	t
1095	30	28	2017-08-03 08:49:50.565535	f	t
1096	32	21	2017-07-24 08:49:50.565564	f	t
1097	32	27	2017-07-31 08:49:50.565594	f	t
1098	34	27	2017-07-24 08:49:50.565622	t	t
1099	34	14	2017-07-25 08:49:50.565651	t	t
1100	34	9	2017-07-28 08:49:50.56568	t	t
1101	34	16	2017-07-29 08:49:50.565708	f	t
1102	34	37	2017-07-23 08:49:50.565737	f	t
1103	34	35	2017-07-25 08:49:50.565766	f	t
1104	35	28	2017-07-28 08:49:50.565795	t	t
1105	35	16	2017-08-07 08:49:50.565824	t	t
1106	35	15	2017-08-12 08:49:50.565852	f	t
1107	35	25	2017-08-08 08:49:50.565881	f	t
1108	35	32	2017-07-21 08:49:50.56591	f	t
1109	36	25	2017-08-15 08:49:50.565939	f	t
1110	36	8	2017-07-24 08:49:50.565967	f	t
1111	36	17	2017-08-07 08:49:50.565996	f	t
1112	36	18	2017-08-15 08:49:50.566025	f	t
1113	36	28	2017-07-31 08:49:50.566065	f	t
1114	36	35	2017-07-29 08:49:50.566113	f	t
1115	36	36	2017-08-10 08:49:50.56615	f	t
1116	39	9	2017-07-27 08:49:50.566182	t	t
1117	39	34	2017-07-30 08:49:50.566222	t	t
1118	39	13	2017-07-31 08:49:50.566252	t	t
1119	39	22	2017-08-07 08:49:50.566292	t	t
1120	39	26	2017-07-22 08:49:50.56632	f	t
1121	39	29	2017-08-03 08:49:50.566349	f	t
1122	39	34	2017-08-11 08:49:50.566378	f	t
1123	39	31	2017-08-13 08:49:50.566407	f	t
1124	39	22	2017-07-25 08:49:50.566437	f	t
1125	39	20	2017-07-26 08:49:50.566466	f	t
1126	39	23	2017-07-22 08:49:50.566496	f	t
1127	40	28	2017-08-07 08:49:50.566524	t	t
1128	40	29	2017-08-13 08:49:50.566554	f	t
1129	40	35	2017-08-12 08:49:50.566583	f	t
1130	40	29	2017-07-21 08:49:50.566611	f	t
1131	40	18	2017-08-04 08:49:50.56664	f	t
1132	40	15	2017-07-28 08:49:50.566669	f	t
1133	40	27	2017-07-28 08:49:50.566698	f	t
1134	40	23	2017-07-29 08:49:50.566727	f	t
1135	40	32	2017-08-08 08:49:50.566756	f	t
1136	41	31	2017-07-30 08:49:50.566785	t	t
1137	41	21	2017-08-04 08:49:50.566814	t	t
1138	41	10	2017-07-21 08:49:50.566843	t	t
1139	41	7	2017-08-10 08:49:50.566872	t	t
1140	41	11	2017-08-01 08:49:50.566901	t	t
1141	41	23	2017-07-26 08:49:50.566929	t	t
1142	41	37	2017-08-15 08:49:50.566957	t	t
1143	41	9	2017-08-06 08:49:50.566986	t	t
1144	41	15	2017-08-05 08:49:50.567014	t	t
1145	41	13	2017-07-31 08:49:50.567042	t	t
1146	41	14	2017-07-27 08:49:50.567071	t	t
1147	41	29	2017-08-08 08:49:50.5671	t	t
1148	41	20	2017-07-21 08:49:50.567128	t	t
1149	41	12	2017-08-15 08:49:50.567157	t	t
1150	41	26	2017-08-03 08:49:50.567186	f	t
1151	41	33	2017-07-31 08:49:50.567214	f	t
1152	41	17	2017-08-13 08:49:50.567243	f	t
1153	41	25	2017-07-21 08:49:50.567272	f	t
1154	41	9	2017-07-28 08:49:50.5673	f	t
1155	41	23	2017-07-31 08:49:50.567329	f	t
1156	41	27	2017-08-02 08:49:50.567357	f	t
1157	41	11	2017-07-25 08:49:50.567386	f	t
1158	41	34	2017-07-28 08:49:50.567414	f	t
1159	41	18	2017-07-31 08:49:50.567443	f	t
1160	41	22	2017-07-27 08:49:50.567471	f	t
1161	41	21	2017-07-30 08:49:50.5675	f	t
1162	41	28	2017-07-28 08:49:50.567528	f	t
1163	41	7	2017-08-13 08:49:50.567557	f	t
1164	41	16	2017-07-27 08:49:50.567586	f	t
1165	41	12	2017-08-12 08:49:50.567615	f	t
1166	41	29	2017-08-02 08:49:50.567644	f	t
1167	41	29	2017-07-25 08:49:50.567672	f	t
1168	41	19	2017-07-23 08:49:50.5677	f	t
1169	42	14	2017-08-10 08:49:50.567729	t	t
1170	42	13	2017-08-04 08:49:50.567758	t	t
1171	42	20	2017-08-02 08:49:50.567788	t	t
1172	42	31	2017-08-08 08:49:50.567817	t	t
1173	42	28	2017-07-31 08:49:50.567846	t	t
1174	42	8	2017-08-14 08:49:50.567874	f	t
1175	42	13	2017-07-25 08:49:50.567903	f	t
1176	42	20	2017-08-02 08:49:50.567933	f	t
1177	42	33	2017-08-15 08:49:50.567961	f	t
1178	42	17	2017-08-14 08:49:50.56799	f	t
1179	42	10	2017-07-27 08:49:50.56802	f	t
1180	42	32	2017-07-21 08:49:50.568049	f	t
1181	42	29	2017-08-06 08:49:50.568079	f	t
1182	42	29	2017-07-21 08:49:50.568107	f	t
1183	42	23	2017-08-13 08:49:50.568136	f	t
1184	42	21	2017-07-23 08:49:50.568165	f	t
1185	42	27	2017-07-30 08:49:50.568194	f	t
1186	42	24	2017-08-04 08:49:50.568223	f	t
1187	42	12	2017-08-05 08:49:50.568252	f	t
1188	42	36	2017-08-05 08:49:50.56828	f	t
1189	42	19	2017-07-22 08:49:50.568309	f	t
1190	44	24	2017-08-10 08:49:50.568338	t	t
1191	44	14	2017-08-03 08:49:50.568367	t	t
1192	44	9	2017-07-31 08:49:50.568405	t	t
1193	44	25	2017-07-27 08:49:50.568435	t	t
1194	44	29	2017-08-02 08:49:50.568464	t	t
1195	44	16	2017-08-01 08:49:50.568494	t	t
1196	44	36	2017-07-29 08:49:50.568533	t	t
1197	44	34	2017-07-21 08:49:50.568562	t	t
1198	44	20	2017-08-06 08:49:50.56859	t	t
1199	44	37	2017-08-06 08:49:50.568619	t	t
1200	44	8	2017-08-05 08:49:50.568647	t	t
1201	44	32	2017-08-14 08:49:50.568676	t	t
1202	44	31	2017-07-29 08:49:50.568704	t	t
1203	44	21	2017-08-09 08:49:50.568733	t	t
1204	44	11	2017-08-09 08:49:50.568762	t	t
1205	44	18	2017-08-05 08:49:50.568791	t	t
1206	44	33	2017-08-12 08:49:50.568819	t	t
1207	44	28	2017-07-24 08:49:50.568848	t	t
1208	44	12	2017-08-07 08:49:50.568877	t	t
1209	44	19	2017-08-13 08:49:50.568905	t	t
1210	44	27	2017-08-12 08:49:50.568934	t	t
1211	44	26	2017-08-08 08:49:50.568962	t	t
1212	44	15	2017-07-23 08:49:50.568991	t	t
1213	44	7	2017-07-25 08:49:50.569019	t	t
1214	44	25	2017-08-07 08:49:50.569048	f	t
1215	44	18	2017-08-04 08:49:50.569076	f	t
1216	44	11	2017-08-02 08:49:50.569104	f	t
1217	44	10	2017-08-04 08:49:50.569149	f	t
1218	44	23	2017-08-14 08:49:50.56919	f	t
1219	44	37	2017-07-27 08:49:50.569219	f	t
1220	44	24	2017-07-28 08:49:50.569248	f	t
1221	46	11	2017-08-03 08:49:50.569277	t	t
1222	46	10	2017-08-02 08:49:50.569306	t	t
1223	46	23	2017-07-22 08:49:50.569334	t	t
1224	46	36	2017-08-14 08:49:50.569363	t	t
1225	46	16	2017-08-07 08:49:50.569392	t	t
1226	46	24	2017-07-23 08:49:50.56942	t	t
1227	46	12	2017-07-31 08:49:50.569449	t	t
1228	46	35	2017-07-21 08:49:50.569477	t	t
1229	46	29	2017-08-04 08:49:50.569506	t	t
1230	46	27	2017-08-13 08:49:50.569534	t	t
1231	46	12	2017-07-22 08:49:50.569563	f	t
1232	46	10	2017-08-05 08:49:50.569592	f	t
1233	46	35	2017-08-07 08:49:50.569621	f	t
1234	47	27	2017-07-28 08:49:50.569649	f	t
1235	47	23	2017-08-13 08:49:50.569677	f	t
1236	49	27	2017-08-01 08:49:50.569707	t	t
1237	49	16	2017-07-29 08:49:50.569735	t	t
1238	49	9	2017-07-21 08:49:50.569765	t	t
1239	49	34	2017-08-14 08:49:50.569794	t	t
1240	49	12	2017-08-08 08:49:50.569823	t	t
1241	49	20	2017-08-14 08:49:50.569852	t	t
1242	49	29	2017-08-02 08:49:50.569881	f	t
1243	49	14	2017-08-04 08:49:50.569909	f	t
1244	49	26	2017-07-25 08:49:50.569937	f	t
1245	49	36	2017-08-14 08:49:50.569966	f	t
1246	49	33	2017-08-14 08:49:50.569995	f	t
1247	49	11	2017-07-29 08:49:50.570023	f	t
1248	49	37	2017-07-22 08:49:50.570052	f	t
1249	49	27	2017-08-01 08:49:50.570081	f	t
1250	49	23	2017-08-05 08:49:50.570109	f	t
1251	50	23	2017-08-04 08:49:50.570138	t	t
1252	50	36	2017-08-11 08:49:50.570166	t	t
1253	51	31	2017-07-22 08:49:50.570194	t	t
1254	51	9	2017-08-14 08:49:50.570224	t	t
1255	51	12	2017-07-31 08:49:50.570253	t	t
1256	51	16	2017-08-07 08:49:50.570282	t	t
1257	51	22	2017-07-25 08:49:50.570311	t	t
1258	51	20	2017-08-15 08:49:50.57034	t	t
1259	51	33	2017-08-13 08:49:50.570369	t	t
1260	51	13	2017-08-11 08:49:50.570398	f	t
1261	51	32	2017-07-23 08:49:50.570427	f	t
1262	51	17	2017-08-04 08:49:50.570478	f	t
1263	51	29	2017-08-01 08:49:50.570507	f	t
1264	51	12	2017-08-07 08:49:50.570537	f	t
1265	51	24	2017-08-08 08:49:50.570566	f	t
1266	51	19	2017-07-23 08:49:50.570595	f	t
1267	51	36	2017-08-03 08:49:50.570624	f	t
1268	51	8	2017-08-09 08:49:50.570653	f	t
1269	51	21	2017-07-27 08:49:50.570682	f	t
1270	51	14	2017-08-08 08:49:50.570711	f	t
1271	54	27	2017-08-03 08:49:50.570739	t	t
1272	54	35	2017-07-29 08:49:50.570768	t	t
1273	54	13	2017-07-22 08:49:50.570796	t	t
1274	54	34	2017-07-22 08:49:50.570825	t	t
1275	54	36	2017-07-30 08:49:50.570854	t	t
1276	54	11	2017-08-05 08:49:50.570883	t	t
1277	54	18	2017-08-10 08:49:50.570912	t	t
1278	54	25	2017-07-25 08:49:50.570941	t	t
1279	54	26	2017-07-21 08:49:50.570969	f	t
1280	54	11	2017-08-04 08:49:50.571008	f	t
1281	54	25	2017-08-09 08:49:50.571048	f	t
1282	54	32	2017-07-27 08:49:50.571077	f	t
1283	55	37	2017-07-28 08:49:50.571106	t	t
1284	55	22	2017-08-10 08:49:50.571135	t	t
1285	55	31	2017-08-10 08:49:50.571163	t	t
1286	55	13	2017-08-01 08:49:50.571192	t	t
1287	55	12	2017-08-10 08:49:50.57122	t	t
1288	55	11	2017-07-29 08:49:50.57126	t	t
1289	55	16	2017-07-27 08:49:50.57129	t	t
1290	55	18	2017-07-27 08:49:50.57133	t	t
1291	55	26	2017-08-11 08:49:50.571359	t	t
1292	55	29	2017-07-24 08:49:50.571387	t	t
1293	55	21	2017-08-12 08:49:50.571416	t	t
1294	55	29	2017-08-06 08:49:50.571446	t	t
1295	55	23	2017-08-04 08:49:50.571475	t	t
1296	55	10	2017-08-02 08:49:50.571503	t	t
1297	55	35	2017-08-11 08:49:50.571532	t	t
1298	55	7	2017-07-27 08:49:50.571561	t	t
1299	55	14	2017-07-22 08:49:50.57159	t	t
1300	55	27	2017-07-26 08:49:50.571619	f	t
1301	55	7	2017-08-14 08:49:50.571647	f	t
1302	57	33	2017-08-01 08:49:50.571677	t	t
1303	57	35	2017-07-25 08:49:50.571706	t	t
1304	57	24	2017-07-28 08:49:50.571734	t	t
1305	57	16	2017-07-27 08:49:50.571763	t	t
1306	57	7	2017-07-22 08:49:50.571792	t	t
1307	57	26	2017-07-23 08:49:50.57182	t	t
1308	57	11	2017-07-27 08:49:50.571848	t	t
1309	57	32	2017-08-01 08:49:50.571877	t	t
1310	57	8	2017-08-08 08:49:50.571906	t	t
1311	57	34	2017-08-02 08:49:50.571934	t	t
1312	57	10	2017-08-08 08:49:50.571963	t	t
1313	57	14	2017-07-23 08:49:50.571991	t	t
1314	57	17	2017-08-14 08:49:50.57202	t	t
1315	57	22	2017-07-24 08:49:50.572048	t	t
1316	57	15	2017-08-14 08:49:50.572077	t	t
1317	57	20	2017-08-05 08:49:50.572105	f	t
1318	58	7	2017-08-07 08:49:50.572134	t	t
1319	58	10	2017-08-02 08:49:50.572162	t	t
1320	58	33	2017-08-01 08:49:50.57219	t	t
1321	58	9	2017-08-02 08:49:50.572218	t	t
1322	58	13	2017-08-13 08:49:50.572246	t	t
1323	58	29	2017-07-30 08:49:50.572275	t	t
1324	58	24	2017-07-22 08:49:50.572304	t	t
1325	58	32	2017-07-28 08:49:50.572332	f	t
1326	58	23	2017-08-03 08:49:50.572361	f	t
1327	58	37	2017-08-01 08:49:50.57239	f	t
1328	58	34	2017-08-09 08:49:50.572419	f	t
1329	58	10	2017-08-05 08:49:50.572448	f	t
1330	58	29	2017-07-24 08:49:50.572478	f	t
1331	58	13	2017-08-10 08:49:50.572507	f	t
1332	58	11	2017-08-09 08:49:50.572536	f	t
1333	59	21	2017-08-11 08:49:50.572564	t	t
1334	59	33	2017-07-21 08:49:50.572592	t	t
1335	59	19	2017-08-10 08:49:50.572621	f	t
1336	59	17	2017-07-25 08:49:50.57265	f	t
1337	59	34	2017-08-12 08:49:50.572679	f	t
1338	60	10	2017-07-25 08:49:50.572706	t	t
1339	60	19	2017-07-23 08:49:50.572735	t	t
1340	60	20	2017-07-26 08:49:50.572764	t	t
1341	60	29	2017-08-06 08:49:50.572792	t	t
1342	61	31	2017-07-25 08:49:50.572821	t	t
1343	61	19	2017-08-09 08:49:50.572849	t	t
1344	61	24	2017-07-29 08:49:50.572877	t	t
1345	61	16	2017-07-29 08:49:50.572905	t	t
1346	61	17	2017-08-06 08:49:50.572933	t	t
1347	61	34	2017-07-25 08:49:50.572962	f	t
1348	61	33	2017-07-31 08:49:50.572991	f	t
1349	61	36	2017-08-08 08:49:50.57302	f	t
1350	61	7	2017-08-01 08:49:50.573048	f	t
1351	61	18	2017-08-14 08:49:50.573077	f	t
1352	61	13	2017-07-30 08:49:50.573106	f	t
1353	61	21	2017-08-06 08:49:50.57315	f	t
1354	61	32	2017-08-14 08:49:50.573191	f	t
1355	62	33	2017-07-26 08:49:50.57322	f	t
1356	62	20	2017-07-28 08:49:50.573248	f	t
1357	62	24	2017-07-25 08:49:50.573278	f	t
1358	62	12	2017-07-29 08:49:50.573307	f	t
1359	62	10	2017-07-29 08:49:50.573336	f	t
1360	62	36	2017-08-02 08:49:50.573365	f	t
1361	62	18	2017-08-04 08:49:50.573394	f	t
1362	62	35	2017-08-05 08:49:50.573423	f	t
1363	62	21	2017-07-25 08:49:50.573451	f	t
1364	62	31	2017-08-05 08:49:50.57348	f	t
1365	62	11	2017-08-08 08:49:50.573509	f	t
1366	63	18	2017-08-07 08:49:50.573551	t	t
1367	63	11	2017-07-31 08:49:50.573598	f	t
1368	63	35	2017-07-24 08:49:50.573627	f	t
1369	64	21	2017-08-12 08:49:50.573656	t	t
1370	64	10	2017-08-05 08:49:50.573686	t	t
1371	64	15	2017-08-15 08:49:50.573715	t	t
1372	64	29	2017-08-02 08:49:50.573744	t	t
1373	64	28	2017-08-04 08:49:50.573773	t	t
1374	64	13	2017-08-04 08:49:50.573802	t	t
1375	64	37	2017-08-11 08:49:50.57383	t	t
1376	64	14	2017-08-14 08:49:50.573858	t	t
1377	64	35	2017-07-30 08:49:50.573889	t	t
1378	64	22	2017-07-23 08:49:50.573917	t	t
1379	64	18	2017-08-07 08:49:50.573946	t	t
1380	64	36	2017-08-08 08:49:50.573974	t	t
1381	64	12	2017-08-06 08:49:50.574004	t	t
1382	64	27	2017-07-31 08:49:50.574033	t	t
1383	64	8	2017-08-09 08:49:50.574062	f	t
1384	64	32	2017-08-06 08:49:50.574091	f	t
1385	64	13	2017-08-10 08:49:50.574119	f	t
1386	64	7	2017-07-28 08:49:50.574149	f	t
1387	64	18	2017-08-15 08:49:50.574178	f	t
1388	64	19	2017-07-22 08:49:50.574207	f	t
1389	64	15	2017-08-08 08:49:50.574236	f	t
1390	64	10	2017-07-21 08:49:50.574264	f	t
1391	64	34	2017-08-08 08:49:50.574293	f	t
1392	64	11	2017-08-09 08:49:50.574322	f	t
1393	64	12	2017-07-30 08:49:50.57435	f	t
1394	65	15	2017-08-04 08:49:50.574379	t	t
1395	65	11	2017-07-28 08:49:50.574408	t	t
1396	65	17	2017-07-31 08:49:50.574437	t	t
1397	65	22	2017-07-27 08:49:50.574466	f	t
1398	65	7	2017-08-02 08:49:50.574494	f	t
1399	65	15	2017-07-28 08:49:50.574523	f	t
1400	66	34	2017-07-28 08:49:50.574552	t	t
1401	66	20	2017-08-06 08:49:50.57458	t	t
1402	66	29	2017-08-13 08:49:50.574609	t	t
1403	66	26	2017-08-01 08:49:50.574637	t	t
1404	66	19	2017-07-21 08:49:50.574665	t	t
1405	66	27	2017-08-01 08:49:50.574694	t	t
1406	66	13	2017-07-22 08:49:50.574722	t	t
1407	66	21	2017-07-24 08:49:50.574751	t	t
1408	66	24	2017-07-21 08:49:50.574779	t	t
1409	66	31	2017-08-09 08:49:50.574808	t	t
1410	66	28	2017-07-31 08:49:50.574836	t	t
1411	66	33	2017-08-10 08:49:50.574865	t	t
1412	66	25	2017-07-28 08:49:50.574894	t	t
1413	66	12	2017-08-02 08:49:50.574922	t	t
1414	66	7	2017-07-21 08:49:50.57495	t	t
1415	66	32	2017-08-08 08:49:50.574979	t	t
1416	66	15	2017-07-30 08:49:50.575008	t	t
1417	66	14	2017-08-13 08:49:50.575037	t	t
1418	66	16	2017-08-04 08:49:50.575066	t	t
1419	66	11	2017-08-05 08:49:50.575096	t	t
1420	66	36	2017-07-26 08:49:50.575124	t	t
1421	66	10	2017-08-14 08:49:50.575153	t	t
1422	66	35	2017-07-23 08:49:50.575182	t	t
1423	66	17	2017-08-15 08:49:50.575211	t	t
1424	66	18	2017-08-10 08:49:50.575239	t	t
1425	66	35	2017-08-02 08:49:50.575267	f	t
1426	66	22	2017-07-30 08:49:50.575296	f	t
1427	66	31	2017-07-21 08:49:50.575325	f	t
1428	66	15	2017-07-26 08:49:50.575354	f	t
1429	66	29	2017-08-06 08:49:50.575383	f	t
1430	66	11	2017-07-23 08:49:50.575411	f	t
1431	66	34	2017-08-12 08:49:50.575439	f	t
1432	66	25	2017-08-10 08:49:50.575468	f	t
1433	66	19	2017-07-23 08:49:50.575497	f	t
1434	66	20	2017-08-04 08:49:50.575527	f	t
1435	66	14	2017-08-11 08:49:50.575555	f	t
1436	66	27	2017-08-03 08:49:50.575584	f	t
1437	66	7	2017-07-29 08:49:50.575613	f	t
1438	66	23	2017-07-21 08:49:50.575642	f	t
1439	66	32	2017-07-24 08:49:50.575672	f	t
1440	66	24	2017-07-29 08:49:50.575701	f	t
1441	67	27	2017-08-07 08:49:50.57573	t	t
1442	67	17	2017-08-14 08:49:50.575759	t	t
1443	67	36	2017-07-26 08:49:50.575788	t	t
1444	67	16	2017-08-09 08:49:50.575818	t	t
1445	67	7	2017-08-01 08:49:50.575868	t	t
1446	67	29	2017-08-14 08:49:50.575899	t	t
1447	67	26	2017-08-08 08:49:50.575939	t	t
1448	67	31	2017-07-25 08:49:50.57599	t	t
1449	67	10	2017-08-01 08:49:50.57604	t	t
1450	67	12	2017-08-13 08:49:50.576091	t	t
1451	67	20	2017-07-31 08:49:50.576142	t	t
1452	67	18	2017-07-27 08:49:50.576181	t	t
1453	67	15	2017-07-23 08:49:50.57621	t	t
1454	68	36	2017-07-22 08:49:50.576238	t	t
1455	68	37	2017-07-31 08:49:50.576267	t	t
1456	68	13	2017-08-11 08:49:50.576296	t	t
1457	68	22	2017-08-14 08:49:50.576325	t	t
1458	68	17	2017-08-13 08:49:50.576353	t	t
1459	68	34	2017-08-01 08:49:50.576381	t	t
1460	68	9	2017-08-10 08:49:50.57641	t	t
1461	68	14	2017-08-09 08:49:50.576438	t	t
1462	68	8	2017-07-28 08:49:50.576467	t	t
1463	68	29	2017-08-05 08:49:50.576495	t	t
1464	68	24	2017-08-05 08:49:50.576524	t	t
1465	68	27	2017-08-08 08:49:50.576553	t	t
1466	68	19	2017-08-15 08:49:50.576581	t	t
1467	68	32	2017-08-02 08:49:50.57662	t	t
1468	68	29	2017-08-10 08:49:50.57665	t	t
1469	68	20	2017-08-07 08:49:50.576689	t	t
1470	68	15	2017-07-30 08:49:50.576718	t	t
1471	68	23	2017-07-28 08:49:50.576747	t	t
1472	68	21	2017-08-02 08:49:50.576775	t	t
1473	68	7	2017-08-07 08:49:50.576804	t	t
1474	68	31	2017-07-27 08:49:50.576833	t	t
1475	68	12	2017-08-03 08:49:50.576861	f	t
1476	68	14	2017-07-26 08:49:50.57689	f	t
1477	68	37	2017-08-09 08:49:50.576918	f	t
1478	68	11	2017-07-21 08:49:50.576946	f	t
1479	68	24	2017-08-14 08:49:50.576975	f	t
1480	68	22	2017-07-30 08:49:50.577004	f	t
1481	68	10	2017-08-04 08:49:50.577033	f	t
1482	68	23	2017-07-22 08:49:50.577062	f	t
1483	68	20	2017-08-05 08:49:50.577091	f	t
1484	68	35	2017-07-29 08:49:50.577119	f	t
1485	68	15	2017-08-03 08:49:50.577177	f	t
1486	68	17	2017-08-11 08:49:50.577208	f	t
1487	68	25	2017-07-25 08:49:50.577237	f	t
1488	68	36	2017-07-30 08:49:50.577267	f	t
1489	68	19	2017-07-28 08:49:50.577297	f	t
1490	68	32	2017-08-04 08:49:50.577327	f	t
1491	68	18	2017-08-06 08:49:50.577356	f	t
1492	6	26	2017-07-26 08:49:50.577385	t	t
1493	6	18	2017-07-26 08:49:50.577414	t	t
1494	6	11	2017-07-31 08:49:50.577442	t	t
1495	6	20	2017-07-31 08:49:50.577492	f	t
1496	6	37	2017-07-22 08:49:50.577522	f	t
1497	6	21	2017-08-06 08:49:50.577552	f	t
1498	6	19	2017-08-06 08:49:50.57758	f	t
1499	6	33	2017-08-10 08:49:50.577609	f	t
1500	7	27	2017-08-08 08:49:50.577638	t	t
1501	7	7	2017-08-05 08:49:50.577667	t	t
1502	9	19	2017-08-14 08:49:50.577695	t	t
1503	9	22	2017-08-01 08:49:50.577724	t	t
1504	9	10	2017-08-04 08:49:50.577753	t	t
1505	9	23	2017-07-21 08:49:50.577782	f	t
1506	9	37	2017-08-15 08:49:50.577811	f	t
1507	9	26	2017-07-25 08:49:50.577839	f	t
1508	9	29	2017-07-23 08:49:50.577868	f	t
1509	9	29	2017-08-05 08:49:50.577897	f	t
1510	9	27	2017-07-30 08:49:50.577926	f	t
1511	13	32	2017-08-07 08:49:50.577956	t	t
1512	13	15	2017-08-08 08:49:50.577984	f	t
1513	13	27	2017-07-28 08:49:50.578013	f	t
1514	14	34	2017-07-29 08:49:50.578042	t	t
1515	14	21	2017-08-10 08:49:50.578071	t	t
1516	14	37	2017-08-14 08:49:50.578099	t	t
1517	14	19	2017-07-27 08:49:50.578127	t	t
1518	14	29	2017-08-09 08:49:50.578156	f	t
1519	14	32	2017-07-23 08:49:50.578184	f	t
1520	14	25	2017-08-15 08:49:50.578213	f	t
1521	14	23	2017-08-05 08:49:50.578242	f	t
1522	18	36	2017-08-13 08:49:50.57827	t	t
1523	18	25	2017-08-02 08:49:50.578299	t	t
1524	18	24	2017-08-01 08:49:50.578328	t	t
1525	18	33	2017-07-25 08:49:50.578356	t	t
1526	18	37	2017-08-14 08:49:50.578385	f	t
1527	18	25	2017-07-23 08:49:50.578413	f	t
1528	18	8	2017-08-09 08:49:50.578442	f	t
1529	18	28	2017-08-12 08:49:50.57847	f	t
1530	22	26	2017-08-13 08:49:50.578498	t	t
1531	22	23	2017-08-15 08:49:50.578528	t	t
1532	22	31	2017-08-12 08:49:50.578556	t	t
1533	22	7	2017-08-07 08:49:50.578585	t	t
1534	22	33	2017-08-01 08:49:50.578614	t	t
1535	22	21	2017-08-08 08:49:50.578643	t	t
1536	22	29	2017-08-11 08:49:50.578673	t	t
1537	22	23	2017-08-08 08:49:50.578701	f	t
1538	22	17	2017-08-13 08:49:50.578729	f	t
1539	25	16	2017-08-02 08:49:50.578758	t	t
1540	25	29	2017-08-01 08:49:50.578787	t	t
1541	25	14	2017-07-25 08:49:50.578816	t	t
1542	25	37	2017-07-26 08:49:50.578845	t	t
1543	25	17	2017-08-06 08:49:50.578875	t	t
1544	25	27	2017-08-10 08:49:50.578904	f	t
1545	25	11	2017-07-26 08:49:50.578933	f	t
1546	25	9	2017-08-02 08:49:50.578962	f	t
1547	25	34	2017-07-25 08:49:50.57899	f	t
1548	25	16	2017-08-13 08:49:50.579019	f	t
1549	25	10	2017-07-24 08:49:50.579048	f	t
1550	25	15	2017-07-26 08:49:50.579077	f	t
1551	25	28	2017-07-29 08:49:50.579106	f	t
1552	25	35	2017-08-08 08:49:50.579134	f	t
1553	31	28	2017-08-01 08:49:50.579163	t	t
1554	31	7	2017-08-08 08:49:50.579192	t	t
1555	31	9	2017-08-06 08:49:50.579221	t	t
1556	31	29	2017-08-09 08:49:50.57925	t	t
1557	31	37	2017-08-15 08:49:50.579279	t	t
1558	31	27	2017-08-10 08:49:50.579308	t	t
1559	31	17	2017-07-31 08:49:50.579337	f	t
1560	31	25	2017-07-27 08:49:50.579365	f	t
1561	31	20	2017-08-14 08:49:50.579394	f	t
1562	31	23	2017-08-07 08:49:50.579422	f	t
1563	31	34	2017-08-02 08:49:50.579451	f	t
1564	31	12	2017-07-24 08:49:50.579479	f	t
1565	31	10	2017-07-31 08:49:50.579507	f	t
1566	31	9	2017-07-23 08:49:50.579536	f	t
1567	31	37	2017-07-23 08:49:50.579564	f	t
1568	31	22	2017-07-30 08:49:50.579593	f	t
1569	31	15	2017-07-31 08:49:50.579622	f	t
1570	31	14	2017-08-14 08:49:50.57965	f	t
1571	31	35	2017-08-15 08:49:50.579679	f	t
1572	33	29	2017-08-04 08:49:50.579707	t	t
1573	33	11	2017-08-15 08:49:50.579737	f	t
1574	33	13	2017-08-10 08:49:50.579765	f	t
1575	33	23	2017-07-30 08:49:50.579794	f	t
1576	33	22	2017-08-15 08:49:50.579822	f	t
1577	33	25	2017-08-10 08:49:50.57985	f	t
1578	33	32	2017-07-23 08:49:50.579879	f	t
1579	37	10	2017-07-23 08:49:50.579908	t	t
1580	37	11	2017-08-12 08:49:50.579937	t	t
1581	37	18	2017-07-28 08:49:50.579965	t	t
1582	37	19	2017-07-28 08:49:50.579995	t	t
1583	37	12	2017-08-02 08:49:50.580023	t	t
1584	37	32	2017-08-09 08:49:50.580052	t	t
1585	37	8	2017-07-23 08:49:50.580082	t	t
1586	37	13	2017-08-06 08:49:50.58011	t	t
1587	37	10	2017-08-08 08:49:50.580139	f	t
1588	37	17	2017-08-11 08:49:50.580168	f	t
1589	37	35	2017-08-01 08:49:50.580196	f	t
1590	37	29	2017-07-25 08:49:50.580225	f	t
1591	37	16	2017-08-10 08:49:50.580254	f	t
1592	37	8	2017-08-01 08:49:50.580283	f	t
1593	37	11	2017-08-07 08:49:50.580311	f	t
1594	37	20	2017-08-03 08:49:50.58034	f	t
1595	37	34	2017-08-08 08:49:50.580368	f	t
1596	37	37	2017-07-26 08:49:50.580396	f	t
1597	37	32	2017-08-05 08:49:50.580424	f	t
1598	37	9	2017-08-11 08:49:50.580453	f	t
1599	38	13	2017-07-23 08:49:50.580481	t	t
1600	38	37	2017-08-09 08:49:50.58051	t	t
1601	38	8	2017-07-25 08:49:50.580539	t	t
1602	38	17	2017-07-28 08:49:50.580567	t	t
1603	38	16	2017-07-27 08:49:50.580595	t	t
1604	38	11	2017-07-26 08:49:50.580623	t	t
1605	38	22	2017-07-29 08:49:50.580651	f	t
1606	38	15	2017-08-03 08:49:50.58068	f	t
1607	38	17	2017-08-05 08:49:50.580709	f	t
1608	38	10	2017-08-10 08:49:50.580738	f	t
1609	38	32	2017-07-29 08:49:50.580767	f	t
1610	38	27	2017-07-21 08:49:50.580795	f	t
1611	38	23	2017-07-25 08:49:50.580823	f	t
1612	38	24	2017-08-06 08:49:50.580853	f	t
1613	38	33	2017-08-01 08:49:50.580882	f	t
1614	38	11	2017-08-02 08:49:50.58091	f	t
1615	38	29	2017-07-29 08:49:50.580939	f	t
1616	38	8	2017-07-24 08:49:50.580967	f	t
1617	38	21	2017-08-15 08:49:50.580996	f	t
1618	38	16	2017-07-22 08:49:50.581025	f	t
1619	43	22	2017-08-12 08:49:50.581053	t	t
1620	45	32	2017-08-08 08:49:50.581081	t	t
1621	45	35	2017-07-21 08:49:50.581109	t	t
1622	45	33	2017-07-23 08:49:50.581154	t	t
1623	45	34	2017-08-09 08:49:50.581195	t	t
1624	45	14	2017-07-23 08:49:50.581224	t	t
1625	45	36	2017-07-25 08:49:50.581252	t	t
1626	45	20	2017-08-11 08:49:50.581281	t	t
1627	45	24	2017-07-31 08:49:50.58131	f	t
1628	45	20	2017-07-24 08:49:50.581339	f	t
1629	45	35	2017-07-25 08:49:50.581367	f	t
1630	45	23	2017-08-11 08:49:50.581396	f	t
1631	45	32	2017-07-25 08:49:50.581425	f	t
1632	45	29	2017-08-06 08:49:50.581454	f	t
1633	45	36	2017-07-31 08:49:50.581482	f	t
1634	45	19	2017-08-10 08:49:50.581512	f	t
1635	45	22	2017-08-04 08:49:50.58154	f	t
1636	45	37	2017-08-10 08:49:50.581569	f	t
1637	45	11	2017-07-27 08:49:50.581597	f	t
1638	48	23	2017-08-01 08:49:50.581626	t	t
1639	52	13	2017-08-06 08:49:50.581655	t	t
1640	52	24	2017-08-07 08:49:50.581684	t	t
1641	52	19	2017-08-12 08:49:50.581714	t	t
1642	52	21	2017-08-04 08:49:50.581742	t	t
1643	52	25	2017-08-09 08:49:50.581771	t	t
1644	52	18	2017-07-24 08:49:50.5818	t	t
1645	52	19	2017-08-06 08:49:50.581829	f	t
1646	52	34	2017-07-31 08:49:50.581857	f	t
1647	52	16	2017-08-08 08:49:50.581886	f	t
1648	52	35	2017-08-01 08:49:50.581915	f	t
1649	52	27	2017-07-23 08:49:50.581943	f	t
1650	52	14	2017-08-01 08:49:50.581971	f	t
1651	52	31	2017-08-10 08:49:50.582	f	t
1652	53	37	2017-07-27 08:49:50.582029	t	t
1653	53	27	2017-08-09 08:49:50.582058	t	t
1654	53	32	2017-07-29 08:49:50.582088	t	t
1655	53	26	2017-07-31 08:49:50.582117	f	t
1656	53	35	2017-08-04 08:49:50.582146	f	t
1657	53	31	2017-07-22 08:49:50.582175	f	t
1658	53	25	2017-08-12 08:49:50.582204	f	t
1659	53	37	2017-08-07 08:49:50.582232	f	t
1660	53	20	2017-08-06 08:49:50.582261	f	t
1661	53	29	2017-07-25 08:49:50.58229	f	t
1662	53	10	2017-08-02 08:49:50.582318	f	t
1663	53	34	2017-08-08 08:49:50.582347	f	t
1664	53	24	2017-07-29 08:49:50.582377	f	t
1665	53	11	2017-07-30 08:49:50.582405	f	t
1666	53	8	2017-08-06 08:49:50.582434	f	t
1667	53	12	2017-07-27 08:49:50.582463	f	t
1668	53	15	2017-07-22 08:49:50.582492	f	t
1669	69	15	2017-07-25 08:49:50.58252	f	t
1670	69	32	2017-08-01 08:49:50.582549	f	t
\.


--
-- Name: clicked_arguments_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('clicked_arguments_uid_seq', 1670, true);


--
-- Data for Name: clicked_statements; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY clicked_statements (uid, statement_uid, author_uid, "timestamp", is_up_vote, is_valid) FROM stdin;
1369	1	14	2017-08-09 08:49:50.243351	t	t
1370	1	37	2017-07-29 08:49:50.243488	t	t
1371	1	29	2017-07-24 08:49:50.24353	t	t
1372	1	32	2017-07-25 08:49:50.243565	t	t
1373	1	19	2017-08-15 08:49:50.243598	t	t
1374	1	34	2017-07-29 08:49:50.243629	f	t
1375	1	22	2017-07-22 08:49:50.243659	f	t
1376	1	13	2017-07-31 08:49:50.243689	f	t
1377	1	14	2017-08-06 08:49:50.243719	f	t
1378	2	12	2017-07-27 08:49:50.243748	t	t
1379	2	23	2017-08-09 08:49:50.243779	t	t
1380	2	7	2017-08-15 08:49:50.243808	t	t
1381	2	22	2017-07-28 08:49:50.243839	t	t
1382	2	11	2017-08-06 08:49:50.243868	f	t
1383	2	12	2017-08-09 08:49:50.243897	f	t
1384	2	34	2017-08-14 08:49:50.243927	f	t
1385	2	10	2017-08-03 08:49:50.243956	f	t
1386	2	20	2017-07-31 08:49:50.243985	f	t
1387	2	24	2017-08-04 08:49:50.244015	f	t
1388	2	35	2017-07-23 08:49:50.244044	f	t
1389	3	8	2017-07-23 08:49:50.244073	f	t
1390	3	25	2017-07-26 08:49:50.244103	f	t
1391	3	35	2017-07-25 08:49:50.244132	f	t
1392	4	21	2017-08-12 08:49:50.244161	t	t
1393	4	36	2017-08-07 08:49:50.24419	f	t
1394	4	12	2017-07-25 08:49:50.24422	f	t
1395	5	22	2017-08-10 08:49:50.244249	t	t
1396	5	24	2017-07-26 08:49:50.244278	t	t
1397	5	31	2017-08-08 08:49:50.244308	t	t
1398	5	28	2017-07-26 08:49:50.244336	t	t
1399	5	36	2017-08-14 08:49:50.244364	t	t
1400	5	31	2017-07-27 08:49:50.244394	t	t
1401	5	26	2017-08-05 08:49:50.244423	f	t
1402	5	36	2017-07-23 08:49:50.244452	f	t
1403	6	9	2017-08-05 08:49:50.244481	t	t
1404	6	29	2017-08-14 08:49:50.24451	t	t
1405	6	10	2017-07-24 08:49:50.244538	t	t
1406	6	12	2017-08-14 08:49:50.244567	t	t
1407	6	18	2017-08-02 08:49:50.244597	t	t
1408	6	37	2017-08-05 08:49:50.244626	t	t
1409	6	31	2017-08-01 08:49:50.244656	t	t
1410	6	17	2017-07-22 08:49:50.244686	t	t
1411	6	36	2017-08-03 08:49:50.244715	t	t
1412	6	20	2017-08-13 08:49:50.244744	t	t
1413	6	37	2017-07-21 08:49:50.244773	t	t
1414	6	36	2017-08-15 08:49:50.244802	t	t
1415	6	27	2017-08-13 08:49:50.244831	f	t
1416	6	15	2017-08-01 08:49:50.244861	f	t
1417	6	19	2017-08-06 08:49:50.24489	f	t
1418	6	11	2017-07-21 08:49:50.244919	f	t
1419	6	36	2017-08-12 08:49:50.244948	f	t
1420	6	36	2017-07-23 08:49:50.244977	f	t
1421	6	29	2017-08-01 08:49:50.245006	f	t
1422	6	24	2017-07-28 08:49:50.245035	f	t
1423	6	12	2017-07-21 08:49:50.245063	f	t
1424	6	14	2017-07-27 08:49:50.245092	f	t
1425	6	33	2017-07-27 08:49:50.245137	f	t
1426	6	7	2017-07-24 08:49:50.245171	f	t
1427	6	27	2017-08-06 08:49:50.245202	f	t
1428	7	26	2017-08-04 08:49:50.245231	t	t
1429	7	20	2017-07-28 08:49:50.24526	f	t
1430	7	11	2017-07-26 08:49:50.24529	f	t
1431	8	9	2017-07-23 08:49:50.24532	t	t
1432	8	31	2017-08-05 08:49:50.245349	t	t
1433	8	8	2017-07-23 08:49:50.245379	t	t
1434	8	23	2017-07-21 08:49:50.245408	t	t
1435	8	10	2017-07-23 08:49:50.245437	t	t
1436	8	17	2017-07-28 08:49:50.245466	t	t
1437	8	19	2017-07-21 08:49:50.245496	t	t
1438	8	31	2017-07-21 08:49:50.245525	t	t
1439	8	36	2017-08-02 08:49:50.245554	t	t
1440	8	14	2017-07-26 08:49:50.245584	t	t
1441	8	33	2017-07-23 08:49:50.245613	t	t
1442	8	23	2017-08-12 08:49:50.245643	t	t
1443	8	14	2017-07-27 08:49:50.245673	t	t
1444	8	37	2017-07-26 08:49:50.245703	t	t
1445	8	13	2017-07-23 08:49:50.245732	t	t
1446	8	8	2017-08-09 08:49:50.245761	t	t
1447	8	21	2017-08-12 08:49:50.24579	t	t
1448	8	10	2017-07-25 08:49:50.24582	t	t
1449	8	22	2017-07-25 08:49:50.245849	t	t
1450	8	8	2017-07-31 08:49:50.245878	t	t
1451	8	31	2017-08-13 08:49:50.245907	t	t
1452	8	13	2017-07-26 08:49:50.245936	t	t
1453	8	22	2017-08-10 08:49:50.245965	t	t
1454	8	24	2017-08-04 08:49:50.245994	f	t
1455	8	25	2017-07-31 08:49:50.246024	f	t
1456	8	19	2017-08-08 08:49:50.246053	f	t
1457	9	36	2017-08-07 08:49:50.246082	t	t
1458	9	31	2017-08-04 08:49:50.24611	f	t
1459	9	11	2017-08-06 08:49:50.246139	f	t
1460	9	23	2017-08-10 08:49:50.246167	f	t
1461	9	10	2017-08-07 08:49:50.246196	f	t
1462	9	31	2017-08-03 08:49:50.246224	f	t
1463	9	20	2017-08-13 08:49:50.246252	f	t
1464	10	17	2017-07-23 08:49:50.246281	t	t
1465	10	17	2017-08-02 08:49:50.24631	f	t
1466	10	9	2017-07-27 08:49:50.246339	f	t
1467	11	37	2017-07-26 08:49:50.246368	t	t
1468	11	8	2017-08-01 08:49:50.246396	t	t
1469	11	20	2017-07-28 08:49:50.246424	t	t
1470	11	34	2017-08-14 08:49:50.246453	t	t
1471	11	7	2017-08-05 08:49:50.246483	f	t
1472	11	18	2017-08-09 08:49:50.246512	f	t
1473	11	37	2017-08-07 08:49:50.246541	f	t
1474	11	35	2017-07-30 08:49:50.24657	f	t
1475	11	34	2017-08-04 08:49:50.246599	f	t
1476	11	35	2017-07-28 08:49:50.246628	f	t
1477	12	32	2017-08-05 08:49:50.246657	t	t
1478	12	36	2017-08-04 08:49:50.246686	t	t
1479	12	23	2017-08-08 08:49:50.246715	t	t
1480	12	32	2017-07-31 08:49:50.246744	t	t
1481	12	21	2017-07-27 08:49:50.246772	t	t
1482	12	13	2017-07-28 08:49:50.246801	t	t
1483	12	11	2017-08-04 08:49:50.24683	t	t
1484	12	15	2017-07-27 08:49:50.246859	t	t
1485	12	26	2017-07-23 08:49:50.246888	t	t
1486	12	19	2017-07-26 08:49:50.246917	f	t
1487	12	37	2017-08-09 08:49:50.246946	f	t
1488	12	21	2017-07-23 08:49:50.246975	f	t
1489	12	33	2017-07-28 08:49:50.247004	f	t
1490	12	10	2017-08-05 08:49:50.247032	f	t
1491	12	8	2017-08-08 08:49:50.247061	f	t
1492	12	29	2017-07-28 08:49:50.24709	f	t
1493	12	12	2017-07-25 08:49:50.247118	f	t
1494	12	28	2017-08-13 08:49:50.247147	f	t
1495	12	35	2017-07-25 08:49:50.247175	f	t
1496	12	10	2017-08-01 08:49:50.247204	f	t
1497	13	7	2017-08-13 08:49:50.247233	t	t
1498	13	35	2017-08-03 08:49:50.247261	t	t
1499	13	31	2017-08-03 08:49:50.247289	t	t
1500	13	32	2017-07-21 08:49:50.247318	t	t
1501	13	23	2017-08-09 08:49:50.247346	t	t
1502	13	26	2017-08-11 08:49:50.247374	t	t
1503	13	34	2017-08-12 08:49:50.247403	f	t
1504	14	17	2017-07-21 08:49:50.247431	f	t
1505	14	10	2017-08-13 08:49:50.247461	f	t
1506	14	19	2017-07-28 08:49:50.247489	f	t
1507	14	14	2017-07-25 08:49:50.247519	f	t
1508	14	16	2017-08-11 08:49:50.247547	f	t
1509	14	17	2017-08-14 08:49:50.247576	f	t
1510	14	8	2017-07-29 08:49:50.247605	f	t
1511	14	29	2017-07-29 08:49:50.247634	f	t
1512	14	18	2017-07-21 08:49:50.247663	f	t
1513	14	9	2017-08-06 08:49:50.247691	f	t
1514	14	14	2017-08-11 08:49:50.24772	f	t
1515	15	7	2017-07-21 08:49:50.247748	t	t
1516	15	11	2017-08-11 08:49:50.247777	t	t
1517	15	24	2017-07-27 08:49:50.247806	t	t
1518	15	36	2017-07-28 08:49:50.247834	t	t
1519	15	14	2017-07-30 08:49:50.247862	t	t
1520	15	36	2017-07-29 08:49:50.247891	t	t
1521	15	31	2017-08-03 08:49:50.24792	t	t
1522	15	33	2017-08-06 08:49:50.247949	t	t
1523	15	29	2017-07-29 08:49:50.247978	t	t
1524	15	28	2017-07-30 08:49:50.248007	t	t
1525	15	29	2017-08-14 08:49:50.248035	f	t
1526	15	25	2017-07-24 08:49:50.248063	f	t
1527	15	31	2017-07-24 08:49:50.248092	f	t
1528	15	15	2017-08-10 08:49:50.24812	f	t
1529	15	37	2017-07-31 08:49:50.248149	f	t
1530	15	33	2017-08-09 08:49:50.248178	f	t
1531	15	9	2017-08-10 08:49:50.248207	f	t
1532	15	21	2017-07-23 08:49:50.248236	f	t
1533	15	18	2017-07-22 08:49:50.248265	f	t
1534	15	26	2017-07-29 08:49:50.248294	f	t
1535	15	13	2017-07-31 08:49:50.248323	f	t
1536	15	26	2017-08-05 08:49:50.248352	f	t
1537	15	16	2017-07-31 08:49:50.248381	f	t
1538	15	34	2017-07-24 08:49:50.248409	f	t
1539	15	14	2017-07-28 08:49:50.248438	f	t
1540	16	11	2017-08-06 08:49:50.248467	f	t
1541	17	10	2017-08-09 08:49:50.248495	t	t
1542	17	35	2017-07-31 08:49:50.248524	t	t
1543	17	17	2017-08-12 08:49:50.248553	t	t
1544	17	18	2017-07-29 08:49:50.248581	t	t
1545	17	10	2017-07-24 08:49:50.24861	f	t
1546	17	31	2017-08-11 08:49:50.24864	f	t
1547	17	27	2017-08-08 08:49:50.248668	f	t
1548	17	10	2017-07-23 08:49:50.248697	f	t
1549	18	27	2017-07-23 08:49:50.248726	t	t
1550	18	32	2017-08-13 08:49:50.248755	t	t
1551	18	10	2017-08-08 08:49:50.248784	t	t
1552	18	21	2017-07-30 08:49:50.248812	t	t
1553	18	21	2017-08-07 08:49:50.248841	t	t
1554	18	24	2017-08-13 08:49:50.24887	t	t
1555	18	32	2017-07-31 08:49:50.248898	t	t
1556	18	27	2017-08-12 08:49:50.248927	f	t
1557	18	16	2017-07-23 08:49:50.248956	f	t
1558	18	10	2017-08-10 08:49:50.248984	f	t
1559	18	24	2017-07-27 08:49:50.249013	f	t
1560	18	13	2017-08-01 08:49:50.249041	f	t
1561	19	14	2017-07-24 08:49:50.24907	t	t
1562	19	22	2017-07-28 08:49:50.249098	t	t
1563	20	22	2017-08-07 08:49:50.249131	t	t
1564	20	28	2017-08-06 08:49:50.249162	t	t
1565	20	35	2017-08-12 08:49:50.249192	t	t
1566	20	29	2017-07-31 08:49:50.249232	t	t
1567	20	15	2017-08-15 08:49:50.249276	t	t
1568	20	22	2017-07-23 08:49:50.249325	t	t
1569	20	12	2017-07-26 08:49:50.249354	t	t
1570	20	33	2017-07-29 08:49:50.249393	t	t
1571	20	10	2017-08-15 08:49:50.249422	t	t
1572	20	23	2017-08-12 08:49:50.249461	t	t
1573	20	14	2017-07-21 08:49:50.24949	t	t
1574	20	32	2017-08-08 08:49:50.249519	t	t
1575	20	36	2017-07-27 08:49:50.249548	t	t
1576	20	14	2017-08-02 08:49:50.249577	t	t
1577	20	22	2017-07-30 08:49:50.249605	f	t
1578	20	31	2017-08-01 08:49:50.249634	f	t
1579	20	29	2017-07-29 08:49:50.249663	f	t
1580	20	34	2017-07-21 08:49:50.249691	f	t
1581	20	9	2017-08-09 08:49:50.24972	f	t
1582	20	24	2017-07-31 08:49:50.249749	f	t
1583	20	35	2017-08-08 08:49:50.249778	f	t
1584	21	13	2017-08-11 08:49:50.249807	t	t
1585	21	10	2017-08-12 08:49:50.249836	t	t
1586	21	11	2017-08-01 08:49:50.249875	t	t
1587	21	32	2017-08-09 08:49:50.249906	t	t
1588	21	29	2017-07-31 08:49:50.249942	t	t
1589	21	18	2017-08-01 08:49:50.25001	t	t
1590	21	33	2017-08-05 08:49:50.250053	t	t
1591	21	14	2017-08-02 08:49:50.250094	t	t
1592	21	19	2017-08-06 08:49:50.250133	t	t
1593	21	32	2017-08-02 08:49:50.250162	f	t
1594	21	9	2017-08-12 08:49:50.250191	f	t
1595	21	25	2017-08-15 08:49:50.25022	f	t
1596	21	10	2017-08-06 08:49:50.250248	f	t
1597	21	31	2017-07-23 08:49:50.250298	f	t
1598	21	28	2017-08-13 08:49:50.250348	f	t
1599	21	20	2017-08-01 08:49:50.250376	f	t
1600	21	37	2017-07-31 08:49:50.250405	f	t
1601	21	7	2017-07-29 08:49:50.250433	f	t
1602	21	12	2017-07-28 08:49:50.250461	f	t
1603	21	17	2017-07-25 08:49:50.25049	f	t
1604	21	32	2017-07-27 08:49:50.250518	f	t
1605	21	35	2017-08-10 08:49:50.250546	f	t
1606	21	23	2017-08-03 08:49:50.250574	f	t
1607	21	13	2017-07-23 08:49:50.250603	f	t
1608	21	32	2017-08-05 08:49:50.250632	f	t
1609	21	16	2017-08-02 08:49:50.25066	f	t
1610	21	10	2017-08-07 08:49:50.250688	f	t
1611	21	9	2017-08-05 08:49:50.250716	f	t
1612	21	26	2017-07-23 08:49:50.250744	f	t
1613	22	22	2017-08-10 08:49:50.250772	t	t
1614	22	9	2017-08-03 08:49:50.250801	t	t
1615	22	31	2017-08-13 08:49:50.250829	t	t
1616	22	34	2017-07-28 08:49:50.250858	t	t
1617	22	28	2017-08-02 08:49:50.250886	t	t
1618	22	22	2017-08-04 08:49:50.250934	t	t
1619	22	34	2017-08-04 08:49:50.250963	t	t
1620	22	34	2017-07-29 08:49:50.250992	t	t
1621	22	18	2017-07-27 08:49:50.251021	t	t
1622	22	15	2017-08-04 08:49:50.25105	t	t
1623	22	7	2017-07-21 08:49:50.251079	t	t
1624	22	24	2017-08-07 08:49:50.251108	t	t
1625	22	28	2017-08-06 08:49:50.251137	t	t
1626	22	20	2017-07-31 08:49:50.251165	t	t
1627	22	16	2017-07-28 08:49:50.251194	t	t
1628	22	9	2017-08-12 08:49:50.251223	t	t
1629	22	8	2017-08-15 08:49:50.251252	f	t
1630	22	29	2017-08-12 08:49:50.251279	f	t
1631	22	21	2017-08-04 08:49:50.251309	f	t
1632	22	15	2017-07-28 08:49:50.251337	f	t
1633	22	28	2017-08-06 08:49:50.251365	f	t
1634	22	26	2017-08-15 08:49:50.251393	f	t
1635	22	20	2017-08-11 08:49:50.251421	f	t
1636	22	34	2017-08-07 08:49:50.25145	f	t
1637	22	18	2017-07-21 08:49:50.251479	f	t
1638	22	18	2017-08-15 08:49:50.251508	f	t
1639	22	33	2017-08-06 08:49:50.251536	f	t
1640	22	11	2017-07-26 08:49:50.251564	f	t
1641	22	18	2017-07-24 08:49:50.251592	f	t
1642	22	24	2017-08-09 08:49:50.251621	f	t
1643	23	12	2017-08-03 08:49:50.25165	t	t
1644	23	16	2017-07-30 08:49:50.251678	t	t
1645	23	23	2017-08-10 08:49:50.251707	t	t
1646	23	19	2017-08-07 08:49:50.251736	t	t
1647	23	31	2017-08-02 08:49:50.251765	t	t
1648	23	23	2017-07-31 08:49:50.251794	t	t
1649	23	18	2017-07-31 08:49:50.251822	t	t
1650	23	8	2017-07-25 08:49:50.251851	t	t
1651	23	33	2017-08-06 08:49:50.251879	t	t
1652	23	10	2017-08-06 08:49:50.251908	t	t
1653	23	27	2017-07-23 08:49:50.251936	t	t
1654	23	18	2017-07-30 08:49:50.251965	f	t
1655	23	7	2017-08-07 08:49:50.251993	f	t
1656	23	32	2017-08-05 08:49:50.252021	f	t
1657	23	29	2017-07-25 08:49:50.252049	f	t
1658	23	20	2017-08-10 08:49:50.252077	f	t
1659	23	36	2017-07-22 08:49:50.252106	f	t
1660	23	23	2017-08-14 08:49:50.252135	f	t
1661	23	16	2017-08-15 08:49:50.252163	f	t
1662	23	19	2017-08-15 08:49:50.252191	f	t
1663	23	33	2017-08-05 08:49:50.25222	f	t
1664	23	21	2017-08-05 08:49:50.252248	f	t
1665	24	11	2017-07-21 08:49:50.252276	t	t
1666	24	20	2017-08-15 08:49:50.252306	t	t
1667	24	20	2017-08-12 08:49:50.252333	t	t
1668	24	11	2017-07-23 08:49:50.252362	t	t
1669	24	14	2017-07-29 08:49:50.252391	t	t
1670	24	15	2017-08-15 08:49:50.252419	t	t
1671	24	36	2017-07-29 08:49:50.252448	f	t
1672	24	31	2017-08-13 08:49:50.252476	f	t
1673	24	13	2017-07-26 08:49:50.252505	f	t
1674	25	29	2017-07-25 08:49:50.252533	t	t
1675	25	22	2017-07-22 08:49:50.252562	t	t
1676	25	24	2017-08-14 08:49:50.252591	t	t
1677	25	32	2017-07-24 08:49:50.25262	t	t
1678	25	24	2017-08-15 08:49:50.252649	t	t
1679	25	23	2017-08-02 08:49:50.252678	t	t
1680	25	29	2017-07-30 08:49:50.252707	t	t
1681	26	19	2017-08-08 08:49:50.252736	t	t
1682	26	8	2017-07-29 08:49:50.252765	f	t
1683	26	29	2017-07-28 08:49:50.252793	f	t
1684	27	12	2017-08-06 08:49:50.252822	t	t
1685	27	27	2017-07-21 08:49:50.25285	t	t
1686	27	33	2017-08-08 08:49:50.252879	t	t
1687	27	26	2017-08-15 08:49:50.252908	t	t
1688	27	17	2017-08-07 08:49:50.252936	f	t
1689	27	24	2017-07-23 08:49:50.252964	f	t
1690	27	34	2017-08-09 08:49:50.252993	f	t
1691	28	34	2017-07-31 08:49:50.253021	t	t
1692	28	31	2017-07-28 08:49:50.25305	t	t
1693	28	27	2017-07-27 08:49:50.253078	t	t
1694	28	34	2017-08-07 08:49:50.253107	t	t
1695	28	15	2017-07-21 08:49:50.253142	f	t
1696	28	27	2017-08-11 08:49:50.253171	f	t
1697	28	25	2017-08-01 08:49:50.253201	f	t
1698	28	14	2017-08-12 08:49:50.253229	f	t
1699	28	29	2017-08-08 08:49:50.253257	f	t
1700	28	25	2017-08-09 08:49:50.253287	f	t
1701	28	7	2017-07-23 08:49:50.253315	f	t
1702	28	34	2017-08-01 08:49:50.253344	f	t
1703	29	29	2017-08-02 08:49:50.253372	t	t
1704	29	24	2017-08-07 08:49:50.2534	t	t
1705	29	33	2017-07-22 08:49:50.253429	t	t
1706	29	19	2017-08-09 08:49:50.253457	t	t
1707	29	10	2017-08-07 08:49:50.253485	t	t
1708	29	36	2017-07-26 08:49:50.253514	t	t
1709	29	13	2017-07-29 08:49:50.253542	t	t
1710	29	8	2017-07-21 08:49:50.253571	t	t
1711	29	29	2017-07-21 08:49:50.253601	t	t
1712	29	31	2017-07-30 08:49:50.253643	t	t
1713	29	12	2017-07-30 08:49:50.253673	t	t
1714	29	15	2017-08-13 08:49:50.253702	f	t
1715	29	29	2017-08-15 08:49:50.253741	f	t
1716	29	18	2017-08-10 08:49:50.253781	f	t
1717	29	37	2017-08-09 08:49:50.253822	f	t
1718	29	13	2017-08-10 08:49:50.253851	f	t
1719	29	20	2017-07-22 08:49:50.25389	f	t
1720	29	20	2017-08-01 08:49:50.253918	f	t
1721	29	29	2017-08-07 08:49:50.253947	f	t
1722	29	32	2017-08-10 08:49:50.253975	f	t
1723	29	22	2017-08-04 08:49:50.254004	f	t
1724	29	31	2017-08-11 08:49:50.254032	f	t
1725	29	9	2017-07-23 08:49:50.25406	f	t
1726	29	18	2017-08-15 08:49:50.25409	f	t
1727	30	29	2017-07-22 08:49:50.254118	t	t
1728	30	19	2017-08-12 08:49:50.254147	f	t
1729	30	35	2017-08-02 08:49:50.254175	f	t
1730	30	11	2017-08-01 08:49:50.254215	f	t
1731	30	36	2017-08-11 08:49:50.254254	f	t
1732	30	34	2017-07-26 08:49:50.254282	f	t
1733	31	27	2017-08-09 08:49:50.254311	t	t
1734	31	36	2017-07-23 08:49:50.254339	t	t
1735	31	29	2017-08-15 08:49:50.254369	t	t
1736	31	34	2017-08-11 08:49:50.254397	t	t
1737	31	8	2017-07-31 08:49:50.254425	t	t
1738	31	26	2017-08-09 08:49:50.254454	t	t
1739	31	8	2017-08-14 08:49:50.254483	f	t
1740	31	26	2017-07-30 08:49:50.254511	f	t
1741	31	29	2017-07-27 08:49:50.254539	f	t
1742	31	19	2017-08-15 08:49:50.254567	f	t
1743	31	34	2017-08-03 08:49:50.254596	f	t
1744	31	31	2017-08-09 08:49:50.254625	f	t
1745	31	7	2017-08-05 08:49:50.254653	f	t
1746	31	24	2017-08-03 08:49:50.254681	f	t
1747	32	28	2017-07-31 08:49:50.25471	t	t
1748	32	7	2017-08-04 08:49:50.254739	f	t
1749	32	21	2017-08-10 08:49:50.254767	f	t
1750	32	18	2017-07-22 08:49:50.254796	f	t
1751	33	11	2017-08-05 08:49:50.254825	t	t
1752	33	33	2017-07-22 08:49:50.254854	t	t
1753	33	16	2017-07-31 08:49:50.254882	t	t
1754	33	24	2017-08-02 08:49:50.254911	t	t
1755	33	23	2017-07-21 08:49:50.254939	t	t
1756	33	11	2017-07-24 08:49:50.254968	t	t
1757	33	35	2017-07-23 08:49:50.254997	t	t
1758	33	17	2017-08-01 08:49:50.255026	t	t
1759	33	7	2017-08-05 08:49:50.255054	f	t
1760	33	31	2017-07-30 08:49:50.255082	f	t
1761	33	35	2017-08-13 08:49:50.25511	f	t
1762	33	8	2017-07-29 08:49:50.255139	f	t
1763	33	35	2017-07-23 08:49:50.255168	f	t
1764	33	34	2017-08-05 08:49:50.255197	f	t
1765	33	33	2017-08-03 08:49:50.255225	f	t
1766	33	29	2017-07-31 08:49:50.255254	f	t
1767	33	9	2017-07-28 08:49:50.255283	f	t
1768	33	17	2017-08-09 08:49:50.255312	f	t
1769	33	36	2017-07-28 08:49:50.25534	f	t
1770	33	34	2017-08-01 08:49:50.255369	f	t
1771	34	19	2017-07-25 08:49:50.255398	t	t
1772	34	11	2017-07-28 08:49:50.255426	t	t
1773	34	12	2017-08-05 08:49:50.255454	t	t
1774	34	35	2017-07-23 08:49:50.255483	t	t
1775	34	20	2017-08-10 08:49:50.255512	t	t
1776	34	14	2017-08-15 08:49:50.25554	t	t
1777	34	16	2017-08-04 08:49:50.255569	t	t
1778	34	12	2017-08-14 08:49:50.255597	t	t
1779	34	25	2017-08-12 08:49:50.255626	t	t
1780	34	7	2017-08-12 08:49:50.255654	t	t
1781	34	16	2017-07-22 08:49:50.255683	t	t
1782	34	7	2017-08-09 08:49:50.255711	t	t
1783	34	13	2017-07-29 08:49:50.25574	t	t
1784	34	26	2017-07-28 08:49:50.255769	f	t
1785	34	10	2017-08-03 08:49:50.255798	f	t
1786	34	13	2017-08-03 08:49:50.255827	f	t
1787	34	33	2017-08-04 08:49:50.255856	f	t
1788	35	20	2017-08-07 08:49:50.255885	t	t
1789	35	19	2017-08-14 08:49:50.255914	t	t
1790	35	17	2017-08-03 08:49:50.255943	t	t
1791	35	25	2017-07-23 08:49:50.255972	t	t
1792	35	31	2017-07-30 08:49:50.256001	t	t
1793	35	28	2017-08-02 08:49:50.256029	t	t
1794	35	7	2017-07-25 08:49:50.256057	t	t
1795	35	34	2017-07-22 08:49:50.256085	t	t
1796	35	33	2017-07-21 08:49:50.256114	t	t
1797	35	28	2017-07-28 08:49:50.256142	t	t
1798	35	34	2017-08-05 08:49:50.256171	f	t
1799	35	22	2017-07-22 08:49:50.256199	f	t
1800	35	18	2017-08-15 08:49:50.256228	f	t
1801	35	18	2017-08-05 08:49:50.256257	f	t
1802	35	14	2017-07-30 08:49:50.256286	f	t
1803	35	29	2017-07-30 08:49:50.256314	f	t
1804	35	10	2017-07-31 08:49:50.256343	f	t
1805	35	35	2017-08-14 08:49:50.256372	f	t
1806	35	26	2017-08-05 08:49:50.2564	f	t
1807	35	32	2017-07-28 08:49:50.256428	f	t
1808	35	34	2017-08-14 08:49:50.256456	f	t
1809	35	9	2017-07-27 08:49:50.256484	f	t
1810	35	33	2017-08-08 08:49:50.256513	f	t
1811	35	17	2017-08-12 08:49:50.256542	f	t
1812	35	13	2017-08-01 08:49:50.256571	f	t
1813	35	8	2017-08-11 08:49:50.256599	f	t
1814	35	21	2017-08-03 08:49:50.256627	f	t
1815	35	32	2017-07-22 08:49:50.256656	f	t
1816	35	23	2017-08-02 08:49:50.256684	f	t
1817	35	37	2017-08-07 08:49:50.256713	f	t
1818	36	36	2017-08-11 08:49:50.256741	t	t
1819	36	12	2017-07-24 08:49:50.256769	t	t
1820	36	18	2017-08-10 08:49:50.256798	t	t
1821	36	8	2017-07-27 08:49:50.256826	t	t
1822	36	36	2017-08-05 08:49:50.256855	t	t
1823	36	13	2017-08-03 08:49:50.256883	t	t
1824	36	8	2017-08-10 08:49:50.256911	t	t
1825	36	12	2017-07-31 08:49:50.25694	t	t
1826	36	27	2017-07-25 08:49:50.256969	t	t
1827	36	11	2017-07-23 08:49:50.256997	t	t
1828	36	27	2017-08-02 08:49:50.257026	t	t
1829	36	15	2017-07-29 08:49:50.257055	t	t
1830	36	37	2017-08-14 08:49:50.257084	t	t
1831	36	22	2017-07-23 08:49:50.257112	t	t
1832	36	11	2017-07-24 08:49:50.257146	t	t
1833	36	12	2017-08-01 08:49:50.257175	t	t
1834	36	34	2017-08-06 08:49:50.257204	t	t
1835	36	35	2017-08-10 08:49:50.257232	f	t
1836	36	28	2017-08-13 08:49:50.257261	f	t
1837	36	16	2017-07-27 08:49:50.257289	f	t
1838	36	23	2017-07-26 08:49:50.257319	f	t
1839	36	9	2017-08-09 08:49:50.257348	f	t
1840	36	13	2017-08-14 08:49:50.257377	f	t
1841	36	37	2017-08-10 08:49:50.257405	f	t
1842	36	31	2017-07-31 08:49:50.257433	f	t
1843	36	20	2017-08-09 08:49:50.257463	f	t
1844	36	9	2017-08-11 08:49:50.257491	f	t
1845	36	29	2017-08-14 08:49:50.25752	f	t
1846	36	35	2017-08-01 08:49:50.257548	f	t
1847	36	20	2017-08-03 08:49:50.257587	f	t
1848	36	8	2017-07-31 08:49:50.257617	f	t
1849	36	33	2017-07-29 08:49:50.257646	f	t
1850	36	16	2017-08-12 08:49:50.257675	f	t
1851	37	34	2017-07-30 08:49:50.257722	t	t
1852	37	27	2017-07-23 08:49:50.257752	t	t
1853	37	9	2017-08-09 08:49:50.257782	t	t
1854	37	24	2017-07-29 08:49:50.257812	t	t
1855	37	24	2017-07-30 08:49:50.257841	t	t
1856	37	15	2017-08-08 08:49:50.25787	t	t
1857	37	11	2017-07-31 08:49:50.257899	t	t
1858	37	17	2017-08-05 08:49:50.257929	t	t
1859	37	28	2017-07-25 08:49:50.257968	f	t
1860	37	32	2017-07-26 08:49:50.258019	f	t
1861	37	36	2017-08-03 08:49:50.258059	f	t
1862	37	37	2017-08-02 08:49:50.25811	f	t
1863	37	13	2017-08-03 08:49:50.258138	f	t
1864	37	9	2017-08-04 08:49:50.258168	f	t
1865	37	31	2017-08-06 08:49:50.258211	f	t
1866	37	16	2017-08-03 08:49:50.258241	f	t
1867	37	35	2017-08-04 08:49:50.258282	f	t
1868	37	18	2017-07-29 08:49:50.258333	f	t
1869	37	22	2017-07-24 08:49:50.258372	f	t
1870	37	12	2017-08-02 08:49:50.2584	f	t
1871	37	27	2017-07-30 08:49:50.258429	f	t
1872	37	13	2017-08-03 08:49:50.258457	f	t
1873	37	25	2017-08-13 08:49:50.258486	f	t
1874	37	37	2017-07-29 08:49:50.258515	f	t
1875	37	26	2017-07-21 08:49:50.258544	f	t
1876	37	15	2017-08-15 08:49:50.258572	f	t
1877	38	18	2017-08-12 08:49:50.258601	f	t
1878	38	27	2017-08-07 08:49:50.258629	f	t
1879	38	14	2017-07-29 08:49:50.258657	f	t
1880	38	37	2017-08-07 08:49:50.258685	f	t
1881	38	35	2017-07-30 08:49:50.258714	f	t
1882	38	28	2017-07-25 08:49:50.258742	f	t
1883	39	16	2017-08-01 08:49:50.258771	t	t
1884	39	33	2017-07-25 08:49:50.2588	t	t
1885	39	29	2017-08-10 08:49:50.258829	t	t
1886	39	18	2017-08-02 08:49:50.258867	t	t
1887	39	29	2017-08-14 08:49:50.258907	t	t
1888	39	28	2017-08-02 08:49:50.258937	t	t
1889	39	19	2017-07-27 08:49:50.258987	t	t
1890	39	25	2017-08-02 08:49:50.259037	t	t
1891	39	37	2017-08-13 08:49:50.259088	t	t
1892	39	32	2017-08-09 08:49:50.259127	f	t
1893	39	12	2017-07-22 08:49:50.259166	f	t
1894	39	32	2017-07-25 08:49:50.259195	f	t
1895	39	17	2017-08-07 08:49:50.259223	f	t
1896	39	7	2017-07-29 08:49:50.259271	f	t
1897	39	9	2017-07-24 08:49:50.25931	f	t
1898	39	10	2017-08-10 08:49:50.259339	f	t
1899	39	27	2017-08-12 08:49:50.259368	f	t
1900	40	11	2017-07-26 08:49:50.259397	t	t
1901	40	14	2017-07-25 08:49:50.259427	t	t
1902	40	33	2017-07-23 08:49:50.259455	t	t
1903	40	25	2017-08-12 08:49:50.259484	t	t
1904	41	10	2017-07-27 08:49:50.259513	t	t
1905	41	31	2017-07-23 08:49:50.259542	t	t
1906	41	8	2017-08-04 08:49:50.259571	t	t
1907	41	26	2017-07-22 08:49:50.2596	t	t
1908	41	12	2017-08-09 08:49:50.259629	t	t
1909	41	37	2017-08-07 08:49:50.259658	t	t
1910	41	26	2017-07-26 08:49:50.259688	t	t
1911	41	28	2017-07-26 08:49:50.259717	t	t
1912	41	11	2017-08-07 08:49:50.259746	f	t
1913	41	34	2017-08-07 08:49:50.259775	f	t
1914	41	35	2017-07-24 08:49:50.259803	f	t
1915	41	16	2017-08-12 08:49:50.259832	f	t
1916	41	14	2017-08-12 08:49:50.259861	f	t
1917	42	11	2017-07-27 08:49:50.25989	t	t
1918	42	17	2017-08-15 08:49:50.259918	t	t
1919	42	29	2017-08-05 08:49:50.259947	t	t
1920	42	37	2017-08-04 08:49:50.259976	t	t
1921	42	37	2017-07-30 08:49:50.260004	t	t
1922	43	27	2017-07-22 08:49:50.260033	t	t
1923	43	35	2017-07-30 08:49:50.260061	t	t
1924	43	12	2017-08-02 08:49:50.26009	f	t
1925	43	17	2017-08-11 08:49:50.260118	f	t
1926	43	21	2017-07-23 08:49:50.260147	f	t
1927	43	11	2017-08-06 08:49:50.260175	f	t
1928	43	23	2017-07-23 08:49:50.260204	f	t
1929	44	22	2017-08-02 08:49:50.260233	t	t
1930	45	25	2017-08-10 08:49:50.260261	t	t
1931	45	25	2017-07-28 08:49:50.260289	t	t
1932	45	9	2017-07-23 08:49:50.260318	t	t
1933	45	17	2017-08-11 08:49:50.260346	t	t
1934	45	18	2017-08-13 08:49:50.260375	t	t
1935	45	11	2017-08-13 08:49:50.260403	t	t
1936	45	12	2017-08-13 08:49:50.260432	t	t
1937	45	18	2017-07-26 08:49:50.26046	t	t
1938	45	26	2017-08-11 08:49:50.260488	t	t
1939	45	20	2017-07-24 08:49:50.260516	t	t
1940	45	31	2017-07-25 08:49:50.260545	t	t
1941	45	11	2017-08-11 08:49:50.260574	f	t
1942	46	8	2017-08-09 08:49:50.260603	f	t
1943	46	14	2017-07-24 08:49:50.260631	f	t
1944	46	23	2017-07-26 08:49:50.26066	f	t
1945	46	34	2017-07-31 08:49:50.260689	f	t
1946	46	26	2017-07-29 08:49:50.260717	f	t
1947	46	32	2017-08-07 08:49:50.260746	f	t
1948	46	11	2017-08-10 08:49:50.260775	f	t
1949	46	17	2017-07-21 08:49:50.260804	f	t
1950	46	19	2017-08-10 08:49:50.260832	f	t
1951	46	18	2017-07-29 08:49:50.260861	f	t
1952	46	11	2017-08-07 08:49:50.26089	f	t
1953	46	11	2017-08-09 08:49:50.260919	f	t
1954	46	9	2017-08-09 08:49:50.260948	f	t
1955	46	17	2017-08-04 08:49:50.260976	f	t
1956	46	8	2017-07-27 08:49:50.261006	f	t
1957	46	7	2017-07-26 08:49:50.261035	f	t
1958	46	19	2017-07-26 08:49:50.261063	f	t
1959	46	14	2017-07-27 08:49:50.261091	f	t
1960	47	36	2017-08-04 08:49:50.261138	f	t
1961	47	15	2017-08-11 08:49:50.261171	f	t
1962	47	24	2017-07-21 08:49:50.2612	f	t
1963	47	29	2017-08-04 08:49:50.261229	f	t
1964	47	14	2017-07-27 08:49:50.261258	f	t
1965	47	7	2017-08-14 08:49:50.261287	f	t
1966	47	24	2017-07-25 08:49:50.261316	f	t
1967	47	9	2017-07-29 08:49:50.261344	f	t
1968	47	29	2017-08-03 08:49:50.261372	f	t
1969	47	17	2017-07-29 08:49:50.2614	f	t
1970	47	29	2017-07-24 08:49:50.261429	f	t
1971	48	27	2017-08-08 08:49:50.261458	f	t
1972	49	29	2017-07-28 08:49:50.261486	t	t
1973	49	33	2017-08-15 08:49:50.261514	t	t
1974	49	16	2017-07-23 08:49:50.261543	t	t
1975	49	29	2017-08-08 08:49:50.261572	t	t
1976	49	27	2017-07-25 08:49:50.261601	t	t
1977	49	15	2017-08-01 08:49:50.26163	t	t
1978	49	10	2017-07-26 08:49:50.261659	t	t
1979	49	32	2017-07-22 08:49:50.261688	t	t
1980	49	23	2017-07-27 08:49:50.261717	t	t
1981	49	25	2017-07-24 08:49:50.261746	t	t
1982	49	31	2017-07-23 08:49:50.261775	t	t
1983	49	28	2017-08-10 08:49:50.261804	t	t
1984	49	24	2017-08-02 08:49:50.261833	t	t
1985	49	19	2017-08-14 08:49:50.261861	t	t
1986	49	27	2017-08-07 08:49:50.26189	t	t
1987	49	27	2017-08-09 08:49:50.261918	t	t
1988	49	28	2017-08-14 08:49:50.261947	t	t
1989	49	14	2017-07-21 08:49:50.261975	t	t
1990	49	37	2017-08-01 08:49:50.262003	t	t
1991	49	29	2017-07-31 08:49:50.262031	t	t
1992	49	25	2017-08-01 08:49:50.262059	f	t
1993	49	13	2017-07-26 08:49:50.262087	f	t
1994	49	26	2017-08-12 08:49:50.262116	f	t
1995	49	29	2017-08-10 08:49:50.262144	f	t
1996	49	9	2017-07-27 08:49:50.262173	f	t
1997	49	9	2017-08-03 08:49:50.262201	f	t
1998	49	15	2017-08-07 08:49:50.26223	f	t
1999	49	10	2017-08-15 08:49:50.262258	f	t
2000	49	7	2017-07-23 08:49:50.262287	f	t
2001	49	8	2017-08-15 08:49:50.262315	f	t
2002	49	20	2017-07-26 08:49:50.262344	f	t
2003	49	13	2017-07-24 08:49:50.262372	f	t
2004	49	12	2017-07-25 08:49:50.2624	f	t
2005	49	7	2017-07-31 08:49:50.262429	f	t
2006	49	20	2017-08-10 08:49:50.262457	f	t
2007	49	35	2017-07-22 08:49:50.262486	f	t
2008	49	27	2017-08-08 08:49:50.262514	f	t
2009	49	19	2017-07-21 08:49:50.262543	f	t
2010	49	14	2017-08-03 08:49:50.262572	f	t
2011	49	28	2017-08-04 08:49:50.262601	f	t
2012	49	9	2017-08-01 08:49:50.262629	f	t
2013	50	15	2017-08-15 08:49:50.262658	t	t
2014	50	11	2017-07-26 08:49:50.262687	t	t
2015	50	7	2017-08-06 08:49:50.262715	t	t
2016	50	25	2017-08-05 08:49:50.262745	f	t
2017	51	37	2017-07-31 08:49:50.262774	t	t
2018	51	32	2017-08-02 08:49:50.262803	t	t
2019	51	25	2017-07-22 08:49:50.262832	t	t
2020	51	16	2017-08-14 08:49:50.26286	t	t
2021	51	37	2017-08-13 08:49:50.262889	t	t
2022	51	36	2017-07-30 08:49:50.262917	t	t
2023	51	22	2017-08-02 08:49:50.262946	t	t
2024	51	29	2017-08-09 08:49:50.262974	t	t
2025	51	22	2017-07-27 08:49:50.263003	t	t
2026	51	22	2017-08-11 08:49:50.263031	t	t
2027	51	28	2017-07-22 08:49:50.26306	t	t
2028	51	19	2017-07-23 08:49:50.263088	t	t
2029	51	15	2017-07-26 08:49:50.263117	t	t
2030	51	29	2017-07-21 08:49:50.263145	t	t
2031	51	14	2017-07-30 08:49:50.263173	t	t
2032	51	11	2017-08-06 08:49:50.263201	t	t
2033	51	29	2017-08-14 08:49:50.26323	t	t
2034	51	19	2017-08-07 08:49:50.263258	t	t
2035	51	31	2017-08-11 08:49:50.263288	t	t
2036	51	15	2017-08-07 08:49:50.263316	t	t
2037	51	32	2017-08-02 08:49:50.263345	f	t
2038	51	27	2017-07-30 08:49:50.263373	f	t
2039	51	34	2017-07-27 08:49:50.263402	f	t
2040	51	29	2017-08-15 08:49:50.26343	f	t
2041	51	13	2017-08-13 08:49:50.263459	f	t
2042	51	11	2017-08-12 08:49:50.263487	f	t
2043	51	33	2017-07-25 08:49:50.263516	f	t
2044	52	20	2017-08-04 08:49:50.263545	t	t
2045	52	19	2017-07-22 08:49:50.263574	f	t
2046	52	15	2017-07-22 08:49:50.263602	f	t
2047	52	13	2017-08-13 08:49:50.263631	f	t
2048	52	29	2017-08-02 08:49:50.26366	f	t
2049	52	22	2017-07-25 08:49:50.263688	f	t
2050	52	11	2017-07-29 08:49:50.263718	f	t
2051	52	19	2017-08-02 08:49:50.263746	f	t
2052	52	24	2017-07-25 08:49:50.263774	f	t
2053	52	17	2017-07-26 08:49:50.263803	f	t
2054	52	29	2017-08-01 08:49:50.263833	f	t
2055	52	35	2017-07-23 08:49:50.263861	f	t
2056	52	33	2017-08-04 08:49:50.26389	f	t
2057	52	10	2017-08-15 08:49:50.263918	f	t
2058	52	16	2017-08-12 08:49:50.263947	f	t
2059	52	23	2017-08-08 08:49:50.263975	f	t
2060	52	16	2017-08-08 08:49:50.264004	f	t
2061	52	28	2017-08-14 08:49:50.264033	f	t
2062	52	9	2017-08-08 08:49:50.264061	f	t
2063	52	34	2017-08-04 08:49:50.264089	f	t
2064	52	26	2017-07-29 08:49:50.264117	f	t
2065	52	32	2017-08-09 08:49:50.264146	f	t
2066	52	34	2017-08-04 08:49:50.264175	f	t
2067	52	17	2017-08-04 08:49:50.264203	f	t
2068	52	21	2017-08-14 08:49:50.264232	f	t
2069	53	28	2017-07-24 08:49:50.26426	t	t
2070	53	35	2017-07-27 08:49:50.264288	t	t
2071	53	36	2017-08-12 08:49:50.264316	t	t
2072	53	29	2017-08-07 08:49:50.264345	f	t
2073	53	22	2017-08-01 08:49:50.264374	f	t
2074	54	13	2017-07-28 08:49:50.264402	t	t
2075	54	26	2017-08-11 08:49:50.264431	t	t
2076	54	25	2017-08-11 08:49:50.264459	t	t
2077	54	13	2017-07-26 08:49:50.264488	t	t
2078	54	17	2017-08-01 08:49:50.264517	t	t
2079	54	15	2017-07-24 08:49:50.264545	t	t
2080	54	34	2017-08-13 08:49:50.264574	t	t
2081	54	31	2017-08-12 08:49:50.264603	t	t
2082	54	18	2017-07-22 08:49:50.264632	t	t
2083	54	10	2017-08-03 08:49:50.264661	t	t
2084	54	10	2017-08-03 08:49:50.264707	t	t
2085	54	13	2017-08-09 08:49:50.264736	t	t
2086	54	13	2017-08-15 08:49:50.264765	t	t
2087	54	25	2017-08-02 08:49:50.264794	t	t
2088	54	11	2017-07-23 08:49:50.264823	t	t
2089	54	12	2017-08-04 08:49:50.264852	t	t
2090	54	16	2017-08-07 08:49:50.264881	t	t
2091	54	21	2017-07-28 08:49:50.26491	t	t
2092	54	31	2017-08-07 08:49:50.264939	t	t
2093	54	36	2017-07-27 08:49:50.264967	t	t
2094	54	37	2017-07-22 08:49:50.264996	t	t
2095	54	19	2017-07-29 08:49:50.265025	f	t
2096	54	12	2017-08-06 08:49:50.265054	f	t
2097	54	29	2017-07-24 08:49:50.265083	f	t
2098	54	32	2017-08-10 08:49:50.265112	f	t
2099	54	29	2017-07-31 08:49:50.265145	f	t
2100	54	34	2017-08-07 08:49:50.265175	f	t
2101	54	33	2017-08-11 08:49:50.265205	f	t
2102	54	34	2017-07-29 08:49:50.265234	f	t
2103	54	10	2017-07-24 08:49:50.265262	f	t
2104	54	22	2017-07-23 08:49:50.265291	f	t
2105	54	36	2017-08-06 08:49:50.265319	f	t
2106	54	15	2017-08-01 08:49:50.265348	f	t
2107	54	36	2017-08-01 08:49:50.265376	f	t
2108	54	13	2017-08-09 08:49:50.265404	f	t
2109	54	24	2017-08-10 08:49:50.265433	f	t
2110	54	24	2017-08-10 08:49:50.265461	f	t
2111	54	26	2017-08-12 08:49:50.26549	f	t
2112	54	23	2017-07-28 08:49:50.265519	f	t
2113	55	7	2017-08-12 08:49:50.265548	t	t
2114	55	12	2017-08-05 08:49:50.265576	t	t
2115	55	11	2017-07-25 08:49:50.265606	t	t
2116	55	17	2017-08-12 08:49:50.265635	t	t
2117	55	8	2017-08-09 08:49:50.265663	t	t
2118	55	29	2017-08-05 08:49:50.265692	t	t
2119	55	32	2017-08-14 08:49:50.265721	t	t
2120	55	18	2017-08-12 08:49:50.265749	t	t
2121	55	21	2017-08-03 08:49:50.265778	t	t
2122	55	7	2017-08-01 08:49:50.265807	t	t
2123	55	35	2017-07-22 08:49:50.265835	t	t
2124	55	21	2017-08-04 08:49:50.265864	t	t
2125	55	29	2017-08-04 08:49:50.265892	t	t
2126	55	25	2017-07-30 08:49:50.26592	t	t
2127	55	22	2017-07-29 08:49:50.265949	t	t
2128	55	23	2017-07-26 08:49:50.265978	t	t
2129	55	18	2017-07-29 08:49:50.266006	t	t
2130	55	33	2017-07-23 08:49:50.266035	f	t
2131	55	35	2017-08-11 08:49:50.266074	f	t
2132	55	10	2017-08-01 08:49:50.266104	f	t
2133	55	8	2017-07-27 08:49:50.266146	f	t
2134	55	11	2017-07-28 08:49:50.266213	f	t
2135	55	16	2017-07-30 08:49:50.266249	f	t
2136	55	16	2017-08-10 08:49:50.266289	f	t
2137	55	33	2017-07-30 08:49:50.266319	f	t
2138	55	34	2017-08-09 08:49:50.266348	f	t
2139	55	11	2017-07-25 08:49:50.266378	f	t
2140	55	21	2017-08-09 08:49:50.266408	f	t
2141	55	7	2017-08-06 08:49:50.266437	f	t
2142	55	25	2017-08-04 08:49:50.266465	f	t
2143	55	21	2017-08-09 08:49:50.266495	f	t
2144	55	18	2017-08-14 08:49:50.266524	f	t
2145	55	27	2017-08-01 08:49:50.266553	f	t
2146	55	34	2017-07-23 08:49:50.266582	f	t
2147	55	14	2017-08-04 08:49:50.266611	f	t
2148	55	29	2017-08-09 08:49:50.26664	f	t
2149	55	19	2017-08-13 08:49:50.266669	f	t
2150	56	15	2017-08-12 08:49:50.266697	t	t
2151	56	28	2017-08-14 08:49:50.266726	t	t
2152	56	15	2017-08-09 08:49:50.266754	t	t
2153	56	9	2017-07-21 08:49:50.266783	t	t
2154	56	24	2017-07-28 08:49:50.266812	t	t
2155	56	26	2017-07-27 08:49:50.266841	t	t
2156	56	8	2017-07-31 08:49:50.266869	t	t
2157	56	37	2017-07-27 08:49:50.266898	t	t
2158	56	31	2017-08-08 08:49:50.266926	t	t
2159	56	17	2017-08-05 08:49:50.266955	t	t
2160	56	8	2017-08-03 08:49:50.266983	t	t
2161	56	8	2017-08-11 08:49:50.267013	t	t
2162	57	31	2017-08-09 08:49:50.267042	t	t
2163	57	27	2017-08-03 08:49:50.26707	t	t
2164	57	11	2017-08-04 08:49:50.267099	f	t
2165	57	18	2017-07-27 08:49:50.267128	f	t
2166	57	26	2017-07-25 08:49:50.267157	f	t
2167	57	27	2017-07-31 08:49:50.267185	f	t
2168	57	32	2017-08-04 08:49:50.267214	f	t
2169	57	20	2017-08-12 08:49:50.267242	f	t
2170	57	37	2017-08-14 08:49:50.267271	f	t
2171	57	24	2017-08-11 08:49:50.2673	f	t
2172	58	16	2017-08-04 08:49:50.267329	t	t
2173	58	11	2017-07-27 08:49:50.267358	t	t
2174	58	19	2017-08-12 08:49:50.267387	t	t
2175	58	28	2017-08-09 08:49:50.267416	f	t
2176	58	24	2017-08-15 08:49:50.267445	f	t
2177	58	26	2017-07-24 08:49:50.267484	f	t
2178	58	32	2017-07-27 08:49:50.267514	f	t
2179	59	17	2017-08-08 08:49:50.267544	t	t
2180	59	27	2017-07-26 08:49:50.267573	t	t
2181	59	32	2017-07-27 08:49:50.267611	t	t
2182	59	25	2017-07-25 08:49:50.26764	f	t
2183	59	35	2017-08-10 08:49:50.267668	f	t
2184	59	9	2017-08-03 08:49:50.267696	f	t
2185	59	28	2017-08-15 08:49:50.267725	f	t
2186	60	22	2017-08-15 08:49:50.267754	t	t
2187	60	27	2017-07-30 08:49:50.267782	t	t
2188	60	29	2017-07-27 08:49:50.267811	t	t
2189	60	35	2017-08-05 08:49:50.26784	t	t
2190	60	7	2017-07-21 08:49:50.267869	t	t
2191	60	7	2017-08-03 08:49:50.267897	t	t
2192	60	37	2017-08-06 08:49:50.267925	t	t
2193	60	10	2017-08-02 08:49:50.267953	t	t
2194	60	25	2017-07-24 08:49:50.267982	t	t
2195	60	18	2017-08-02 08:49:50.268011	t	t
2196	60	33	2017-07-22 08:49:50.26804	t	t
2197	60	37	2017-08-07 08:49:50.268068	t	t
2198	60	25	2017-08-13 08:49:50.268097	f	t
2199	60	22	2017-08-03 08:49:50.268126	f	t
2200	60	32	2017-08-12 08:49:50.268155	f	t
2201	60	33	2017-08-11 08:49:50.268183	f	t
2202	60	23	2017-07-31 08:49:50.268212	f	t
2203	60	14	2017-08-07 08:49:50.26824	f	t
2204	60	31	2017-08-15 08:49:50.268269	f	t
2205	60	29	2017-08-11 08:49:50.268298	f	t
2206	60	28	2017-07-22 08:49:50.268326	f	t
2207	60	10	2017-08-14 08:49:50.268355	f	t
2208	60	24	2017-08-06 08:49:50.268384	f	t
2209	61	19	2017-07-28 08:49:50.268413	t	t
2210	61	21	2017-08-12 08:49:50.268442	f	t
2211	61	12	2017-07-27 08:49:50.268471	f	t
2212	61	31	2017-07-21 08:49:50.268501	f	t
2213	61	24	2017-08-11 08:49:50.26853	f	t
2214	61	29	2017-08-11 08:49:50.268559	f	t
2215	61	18	2017-08-10 08:49:50.268588	f	t
2216	61	18	2017-08-02 08:49:50.268617	f	t
2217	61	29	2017-07-28 08:49:50.268646	f	t
2218	61	15	2017-08-03 08:49:50.268674	f	t
2219	61	21	2017-08-14 08:49:50.268703	f	t
2220	61	33	2017-07-27 08:49:50.268731	f	t
2221	62	20	2017-08-15 08:49:50.26876	t	t
2222	62	11	2017-08-13 08:49:50.268788	t	t
2223	62	29	2017-07-29 08:49:50.268817	t	t
2224	62	19	2017-07-24 08:49:50.268846	t	t
2225	62	33	2017-08-07 08:49:50.268874	t	t
2226	62	11	2017-07-24 08:49:50.268903	t	t
2227	62	17	2017-08-13 08:49:50.268931	t	t
2228	62	36	2017-08-02 08:49:50.26896	t	t
2229	62	14	2017-07-24 08:49:50.268989	t	t
2230	62	11	2017-08-09 08:49:50.269017	t	t
2231	62	10	2017-08-14 08:49:50.269046	t	t
2232	62	37	2017-07-28 08:49:50.269076	t	t
2233	62	33	2017-08-07 08:49:50.269105	t	t
2234	62	9	2017-07-29 08:49:50.269141	t	t
2235	62	18	2017-07-28 08:49:50.269171	t	t
2236	62	8	2017-07-22 08:49:50.2692	t	t
2237	62	20	2017-08-07 08:49:50.269229	t	t
2238	62	22	2017-07-25 08:49:50.269258	t	t
2239	62	20	2017-08-12 08:49:50.269287	t	t
2240	62	37	2017-08-13 08:49:50.269316	f	t
2241	62	18	2017-07-25 08:49:50.269344	f	t
2242	62	12	2017-08-05 08:49:50.269374	f	t
2243	62	27	2017-08-10 08:49:50.269403	f	t
2244	62	10	2017-07-25 08:49:50.269432	f	t
2245	63	10	2017-08-07 08:49:50.26946	t	t
2246	63	17	2017-08-10 08:49:50.269488	t	t
2247	63	27	2017-07-23 08:49:50.269517	t	t
2248	63	7	2017-08-12 08:49:50.269546	t	t
2249	63	9	2017-08-11 08:49:50.269575	t	t
2250	63	26	2017-08-09 08:49:50.269603	t	t
2251	63	13	2017-07-21 08:49:50.269632	t	t
2252	63	16	2017-07-27 08:49:50.26966	t	t
2253	63	14	2017-08-03 08:49:50.269689	t	t
2254	63	24	2017-08-06 08:49:50.269717	t	t
2255	63	27	2017-08-12 08:49:50.269746	t	t
2256	63	36	2017-07-24 08:49:50.269774	t	t
2257	63	22	2017-08-04 08:49:50.269803	t	t
2258	63	13	2017-07-23 08:49:50.269832	t	t
2259	63	14	2017-07-24 08:49:50.26986	f	t
2260	63	14	2017-07-23 08:49:50.269889	f	t
2261	63	16	2017-08-12 08:49:50.269918	f	t
2262	63	7	2017-07-21 08:49:50.269946	f	t
2263	63	23	2017-08-15 08:49:50.269974	f	t
2264	63	24	2017-07-22 08:49:50.270003	f	t
2265	63	25	2017-07-30 08:49:50.270031	f	t
2266	63	18	2017-08-15 08:49:50.270059	f	t
2267	63	26	2017-07-26 08:49:50.270088	f	t
2268	63	18	2017-07-22 08:49:50.270137	f	t
2269	63	22	2017-08-13 08:49:50.270176	f	t
2270	63	21	2017-08-01 08:49:50.270238	f	t
2271	63	32	2017-08-05 08:49:50.270274	f	t
2272	63	31	2017-07-21 08:49:50.270303	f	t
2273	63	37	2017-08-15 08:49:50.270333	f	t
2274	63	22	2017-07-21 08:49:50.270361	f	t
2275	63	31	2017-07-23 08:49:50.27039	f	t
2276	63	18	2017-08-08 08:49:50.27042	f	t
2277	64	32	2017-08-03 08:49:50.270448	t	t
2278	64	36	2017-08-14 08:49:50.270477	t	t
2279	64	8	2017-08-13 08:49:50.270505	t	t
2280	64	9	2017-08-15 08:49:50.270534	t	t
2281	64	9	2017-07-29 08:49:50.270574	t	t
2282	64	8	2017-08-09 08:49:50.270616	t	t
2283	64	33	2017-07-29 08:49:50.270646	f	t
2284	64	20	2017-08-10 08:49:50.270674	f	t
2285	64	10	2017-08-12 08:49:50.270703	f	t
2286	64	37	2017-08-13 08:49:50.270732	f	t
2287	64	34	2017-07-27 08:49:50.270761	f	t
2288	64	37	2017-08-06 08:49:50.270791	f	t
2289	64	9	2017-07-23 08:49:50.27082	f	t
2290	64	16	2017-08-13 08:49:50.270849	f	t
2291	64	14	2017-07-24 08:49:50.270878	f	t
2292	64	33	2017-08-04 08:49:50.270909	f	t
2293	64	13	2017-08-11 08:49:50.270938	f	t
2294	65	13	2017-08-03 08:49:50.270967	t	t
2295	65	14	2017-07-29 08:49:50.270996	t	t
2296	65	29	2017-08-11 08:49:50.271025	t	t
2297	65	11	2017-08-13 08:49:50.271054	t	t
2298	65	18	2017-07-28 08:49:50.271083	t	t
2299	65	13	2017-08-07 08:49:50.271111	t	t
2300	65	22	2017-07-23 08:49:50.27114	t	t
2301	65	7	2017-08-03 08:49:50.271169	t	t
2302	65	12	2017-07-21 08:49:50.271198	t	t
2303	65	36	2017-07-27 08:49:50.271226	f	t
2304	65	35	2017-08-09 08:49:50.271256	f	t
2305	65	13	2017-07-24 08:49:50.271284	f	t
2306	65	14	2017-07-23 08:49:50.271315	f	t
2307	65	23	2017-08-01 08:49:50.271344	f	t
2308	65	18	2017-08-13 08:49:50.271372	f	t
2309	65	19	2017-08-03 08:49:50.271401	f	t
2310	66	15	2017-08-07 08:49:50.27143	t	t
2311	66	17	2017-08-04 08:49:50.271458	t	t
2312	66	35	2017-07-29 08:49:50.271486	t	t
2313	66	24	2017-08-13 08:49:50.271514	f	t
2314	66	28	2017-08-02 08:49:50.271543	f	t
2315	66	19	2017-08-08 08:49:50.271574	f	t
2316	66	17	2017-08-01 08:49:50.271603	f	t
2317	66	24	2017-08-09 08:49:50.271647	f	t
2318	66	21	2017-08-03 08:49:50.271677	f	t
2319	66	16	2017-07-29 08:49:50.271706	f	t
2320	66	24	2017-08-11 08:49:50.271735	f	t
2321	66	12	2017-07-23 08:49:50.271763	f	t
2322	66	22	2017-08-11 08:49:50.271791	f	t
2323	66	16	2017-08-15 08:49:50.27182	f	t
2324	66	22	2017-07-30 08:49:50.271848	f	t
2325	66	32	2017-08-08 08:49:50.271877	f	t
2326	66	23	2017-08-14 08:49:50.271905	f	t
2327	66	31	2017-07-28 08:49:50.271934	f	t
2328	66	7	2017-08-12 08:49:50.271962	f	t
2329	66	15	2017-07-30 08:49:50.27199	f	t
2330	67	7	2017-08-03 08:49:50.272019	t	t
2331	67	9	2017-08-12 08:49:50.272049	t	t
2332	67	36	2017-08-15 08:49:50.272079	t	t
2333	67	21	2017-08-03 08:49:50.272107	t	t
2334	67	22	2017-07-23 08:49:50.272135	t	t
2335	67	19	2017-07-21 08:49:50.272163	t	t
2336	67	26	2017-07-23 08:49:50.272192	t	t
2337	67	34	2017-08-06 08:49:50.27222	t	t
2338	67	20	2017-07-21 08:49:50.272249	t	t
2339	67	23	2017-07-27 08:49:50.272279	t	t
2340	67	31	2017-07-25 08:49:50.272307	t	t
2341	67	25	2017-08-12 08:49:50.272336	t	t
2342	67	7	2017-07-25 08:49:50.272365	t	t
2343	67	9	2017-07-28 08:49:50.272396	f	t
2344	67	8	2017-08-07 08:49:50.272425	f	t
2345	67	8	2017-07-30 08:49:50.272454	f	t
2346	68	28	2017-08-11 08:49:50.272482	t	t
2347	68	20	2017-07-26 08:49:50.272511	t	t
2348	68	28	2017-08-12 08:49:50.272539	t	t
2349	68	21	2017-08-10 08:49:50.272569	t	t
2350	68	29	2017-08-12 08:49:50.272607	t	t
2351	68	13	2017-07-30 08:49:50.272657	t	t
2352	68	31	2017-07-23 08:49:50.272696	t	t
2353	68	9	2017-07-31 08:49:50.272724	f	t
2354	68	36	2017-08-15 08:49:50.272753	f	t
2355	68	24	2017-08-08 08:49:50.272781	f	t
2356	68	24	2017-08-04 08:49:50.272809	f	t
2357	68	7	2017-08-04 08:49:50.272838	f	t
2358	68	32	2017-07-24 08:49:50.272867	f	t
2359	69	35	2017-08-15 08:49:50.272895	t	t
2360	69	27	2017-08-09 08:49:50.272923	t	t
2361	69	29	2017-08-08 08:49:50.272951	t	t
2362	69	11	2017-08-15 08:49:50.27298	t	t
2363	69	24	2017-08-14 08:49:50.273008	t	t
2364	69	34	2017-08-03 08:49:50.273037	t	t
2365	69	36	2017-07-23 08:49:50.273067	t	t
2366	69	21	2017-08-02 08:49:50.273097	t	t
2367	69	10	2017-08-05 08:49:50.273141	t	t
2368	69	27	2017-08-09 08:49:50.273183	t	t
2369	69	28	2017-08-03 08:49:50.273212	t	t
2370	69	15	2017-08-05 08:49:50.273241	t	t
2371	69	33	2017-08-15 08:49:50.273272	f	t
2372	69	29	2017-08-13 08:49:50.273301	f	t
2373	69	34	2017-08-08 08:49:50.27333	f	t
2374	69	20	2017-07-30 08:49:50.273359	f	t
2375	69	24	2017-08-12 08:49:50.273388	f	t
2376	69	33	2017-08-08 08:49:50.273417	f	t
2377	69	16	2017-08-01 08:49:50.273446	f	t
2378	69	18	2017-07-24 08:49:50.273476	f	t
2379	70	13	2017-07-28 08:49:50.273506	t	t
2380	70	23	2017-08-06 08:49:50.273535	t	t
2381	70	10	2017-08-09 08:49:50.273566	t	t
2382	70	25	2017-07-28 08:49:50.273596	t	t
2383	70	36	2017-07-22 08:49:50.273625	t	t
2384	70	27	2017-08-06 08:49:50.273653	t	t
2385	70	16	2017-08-03 08:49:50.273681	t	t
2386	70	34	2017-07-21 08:49:50.27371	t	t
2387	70	27	2017-07-21 08:49:50.27374	t	t
2388	70	10	2017-08-06 08:49:50.273781	t	t
2389	70	10	2017-07-24 08:49:50.273814	t	t
2390	70	10	2017-08-05 08:49:50.273848	t	t
2391	70	32	2017-08-07 08:49:50.273881	t	t
2392	70	20	2017-08-10 08:49:50.273915	t	t
2393	70	19	2017-07-31 08:49:50.273948	t	t
2394	70	18	2017-07-29 08:49:50.273981	t	t
2395	70	29	2017-07-26 08:49:50.274014	t	t
2396	70	8	2017-08-14 08:49:50.274046	t	t
2397	70	29	2017-07-23 08:49:50.27408	t	t
2398	70	13	2017-07-21 08:49:50.274113	f	t
2399	70	20	2017-08-13 08:49:50.274146	f	t
2400	70	31	2017-07-22 08:49:50.274179	f	t
2401	70	36	2017-08-02 08:49:50.274211	f	t
2402	70	7	2017-08-12 08:49:50.274245	f	t
2403	70	34	2017-08-05 08:49:50.274278	f	t
2404	70	22	2017-07-28 08:49:50.274311	f	t
2405	70	34	2017-07-25 08:49:50.274344	f	t
2406	70	23	2017-08-09 08:49:50.274378	f	t
2407	70	27	2017-07-24 08:49:50.274411	f	t
2408	70	25	2017-07-29 08:49:50.274444	f	t
2409	70	31	2017-07-24 08:49:50.274477	f	t
2410	70	16	2017-08-06 08:49:50.274509	f	t
2411	70	27	2017-07-26 08:49:50.274544	f	t
2412	70	25	2017-08-06 08:49:50.274577	f	t
2413	70	20	2017-07-24 08:49:50.27461	f	t
2414	70	33	2017-07-27 08:49:50.274646	f	t
2415	71	7	2017-07-21 08:49:50.274681	t	t
2416	71	35	2017-08-15 08:49:50.274716	t	t
2417	71	29	2017-08-11 08:49:50.274749	t	t
2418	71	12	2017-07-21 08:49:50.274788	t	t
2419	71	14	2017-07-27 08:49:50.274817	t	t
2420	71	26	2017-08-09 08:49:50.274846	t	t
2421	71	18	2017-08-01 08:49:50.274875	t	t
2422	71	36	2017-07-23 08:49:50.274904	t	t
2423	71	23	2017-07-22 08:49:50.274932	f	t
2424	71	11	2017-08-06 08:49:50.274961	f	t
2425	71	31	2017-08-05 08:49:50.274989	f	t
2426	71	33	2017-08-02 08:49:50.275018	f	t
2427	71	34	2017-07-25 08:49:50.275049	f	t
2428	72	16	2017-07-25 08:49:50.275078	t	t
2429	72	23	2017-07-21 08:49:50.275107	t	t
2430	72	33	2017-08-02 08:49:50.275136	t	t
2431	72	18	2017-08-10 08:49:50.275165	t	t
2432	72	11	2017-07-25 08:49:50.275204	f	t
2433	72	20	2017-08-12 08:49:50.275245	f	t
2434	72	15	2017-08-14 08:49:50.275285	f	t
2435	73	8	2017-08-10 08:49:50.275335	t	t
2436	73	14	2017-07-24 08:49:50.275375	t	t
2437	73	32	2017-08-05 08:49:50.27544	t	t
2438	73	36	2017-08-13 08:49:50.27548	t	t
2439	73	21	2017-08-14 08:49:50.275509	t	t
2440	73	32	2017-08-12 08:49:50.275538	t	t
2441	73	7	2017-08-15 08:49:50.275566	t	t
2442	73	25	2017-07-24 08:49:50.275595	t	t
2443	73	29	2017-07-21 08:49:50.275634	t	t
2444	73	36	2017-08-12 08:49:50.275673	t	t
2445	73	36	2017-07-29 08:49:50.275702	t	t
2446	73	26	2017-08-02 08:49:50.275731	t	t
2447	73	22	2017-07-31 08:49:50.27576	t	t
2448	73	13	2017-07-25 08:49:50.275789	t	t
2449	73	22	2017-07-24 08:49:50.275818	t	t
2450	73	21	2017-07-22 08:49:50.275848	t	t
2451	73	34	2017-08-08 08:49:50.275876	t	t
2452	73	36	2017-07-25 08:49:50.275905	t	t
2453	73	28	2017-08-08 08:49:50.275934	t	t
2454	73	24	2017-07-30 08:49:50.275963	t	t
2455	73	36	2017-08-09 08:49:50.275993	t	t
2456	73	7	2017-08-06 08:49:50.276022	t	t
2457	73	18	2017-07-28 08:49:50.27605	t	t
2458	73	36	2017-08-09 08:49:50.27608	t	t
2459	73	27	2017-08-04 08:49:50.27611	t	t
2460	73	36	2017-07-31 08:49:50.276139	f	t
2461	73	37	2017-08-06 08:49:50.276168	f	t
2462	73	34	2017-07-25 08:49:50.276197	f	t
2463	73	15	2017-08-12 08:49:50.276226	f	t
2464	73	36	2017-07-28 08:49:50.276255	f	t
2465	73	13	2017-08-02 08:49:50.276284	f	t
2466	73	29	2017-07-24 08:49:50.276313	f	t
2467	73	31	2017-07-23 08:49:50.276359	f	t
2468	73	17	2017-07-22 08:49:50.2764	f	t
2469	73	24	2017-08-04 08:49:50.27643	f	t
2470	74	23	2017-08-07 08:49:50.27646	t	t
2471	74	29	2017-08-09 08:49:50.276488	t	t
2472	74	13	2017-08-13 08:49:50.276517	t	t
2473	74	26	2017-08-14 08:49:50.276546	t	t
2474	74	33	2017-08-11 08:49:50.276575	t	t
2475	74	11	2017-07-24 08:49:50.276604	t	t
2476	74	19	2017-08-12 08:49:50.276632	t	t
2477	74	36	2017-07-31 08:49:50.276661	t	t
2478	74	23	2017-07-29 08:49:50.276689	t	t
2479	74	11	2017-08-15 08:49:50.276718	t	t
2480	74	11	2017-07-27 08:49:50.276746	t	t
2481	74	14	2017-07-28 08:49:50.276776	t	t
2482	74	24	2017-07-21 08:49:50.276808	t	t
2483	74	11	2017-07-31 08:49:50.276839	t	t
2484	74	34	2017-07-22 08:49:50.276868	t	t
2485	74	22	2017-07-31 08:49:50.276897	t	t
2486	74	17	2017-08-03 08:49:50.276929	t	t
2487	74	21	2017-07-29 08:49:50.276958	t	t
2488	74	14	2017-08-04 08:49:50.276987	t	t
2489	74	34	2017-07-26 08:49:50.277016	f	t
2490	74	19	2017-08-12 08:49:50.277045	f	t
2491	74	29	2017-08-09 08:49:50.277074	f	t
2492	74	29	2017-08-12 08:49:50.277102	f	t
2493	74	9	2017-08-12 08:49:50.277147	f	t
2494	75	25	2017-08-05 08:49:50.277178	t	t
2495	75	19	2017-07-29 08:49:50.277217	t	t
2496	75	12	2017-07-26 08:49:50.277246	t	t
2497	75	34	2017-08-14 08:49:50.277275	t	t
2498	75	12	2017-08-14 08:49:50.277304	t	t
2499	75	31	2017-08-03 08:49:50.277332	t	t
2500	75	37	2017-08-10 08:49:50.277363	t	t
2501	75	29	2017-07-22 08:49:50.277393	t	t
2502	75	14	2017-08-03 08:49:50.277422	t	t
2503	75	11	2017-07-25 08:49:50.277451	t	t
2504	75	34	2017-07-24 08:49:50.277479	t	t
2505	75	23	2017-07-26 08:49:50.277508	f	t
2506	76	15	2017-08-09 08:49:50.277537	t	t
2507	76	29	2017-07-29 08:49:50.277568	t	t
2508	76	20	2017-08-14 08:49:50.277597	t	t
2509	76	12	2017-08-08 08:49:50.277626	t	t
2510	76	15	2017-07-28 08:49:50.277655	f	t
2511	76	11	2017-07-27 08:49:50.277684	f	t
2512	76	36	2017-08-09 08:49:50.277712	f	t
2513	76	33	2017-07-31 08:49:50.277741	f	t
2514	76	35	2017-08-14 08:49:50.277779	f	t
2515	77	7	2017-08-09 08:49:50.277809	t	t
2516	77	14	2017-07-21 08:49:50.277839	t	t
2517	77	26	2017-08-09 08:49:50.27787	t	t
2518	77	21	2017-08-05 08:49:50.2779	t	t
2519	77	16	2017-08-14 08:49:50.27793	t	t
2520	77	29	2017-08-07 08:49:50.277961	t	t
2521	77	26	2017-07-26 08:49:50.277991	t	t
2522	77	11	2017-08-10 08:49:50.278024	t	t
2523	77	22	2017-08-05 08:49:50.278056	t	t
2524	77	15	2017-07-31 08:49:50.278087	f	t
2525	77	32	2017-08-07 08:49:50.278117	f	t
2526	77	23	2017-08-12 08:49:50.278148	f	t
2527	77	12	2017-07-29 08:49:50.278178	f	t
2528	77	22	2017-08-01 08:49:50.278208	f	t
2529	77	24	2017-08-07 08:49:50.278243	f	t
2530	77	21	2017-08-04 08:49:50.278275	f	t
2531	77	23	2017-07-29 08:49:50.278308	f	t
2532	77	27	2017-08-09 08:49:50.278339	f	t
2533	77	31	2017-07-22 08:49:50.27837	f	t
2534	77	37	2017-07-31 08:49:50.2784	f	t
2535	78	28	2017-08-02 08:49:50.27843	t	t
2536	78	17	2017-08-12 08:49:50.27846	t	t
2537	78	29	2017-08-01 08:49:50.27849	f	t
2538	79	35	2017-07-29 08:49:50.27852	t	t
2539	79	9	2017-07-31 08:49:50.278552	t	t
2540	79	16	2017-07-27 08:49:50.278582	t	t
2541	79	21	2017-08-12 08:49:50.278613	t	t
2542	79	26	2017-08-08 08:49:50.278643	t	t
2543	79	12	2017-08-02 08:49:50.278673	t	t
2544	79	15	2017-07-28 08:49:50.278704	t	t
2545	79	34	2017-07-23 08:49:50.278734	t	t
2546	79	29	2017-08-03 08:49:50.278764	t	t
2547	79	15	2017-07-26 08:49:50.278795	t	t
2548	79	27	2017-08-08 08:49:50.278832	t	t
2549	79	29	2017-08-01 08:49:50.278861	t	t
2550	79	8	2017-08-07 08:49:50.279147	t	t
2551	79	9	2017-08-07 08:49:50.279198	t	t
2552	79	8	2017-07-21 08:49:50.279231	t	t
2553	79	33	2017-08-08 08:49:50.27926	t	t
2554	79	28	2017-07-30 08:49:50.27929	f	t
2555	79	18	2017-08-07 08:49:50.27932	f	t
2556	79	35	2017-07-21 08:49:50.279349	f	t
2557	79	9	2017-07-25 08:49:50.279378	f	t
2558	79	32	2017-08-09 08:49:50.279407	f	t
2559	79	21	2017-08-15 08:49:50.279436	f	t
2560	79	15	2017-07-31 08:49:50.279467	f	t
2561	79	34	2017-08-08 08:49:50.279499	f	t
2562	79	15	2017-08-14 08:49:50.279528	f	t
2563	79	12	2017-07-24 08:49:50.279557	f	t
2564	79	19	2017-08-14 08:49:50.279587	f	t
2565	79	9	2017-08-13 08:49:50.279616	f	t
2566	80	27	2017-07-25 08:49:50.279645	t	t
2567	80	21	2017-07-27 08:49:50.279673	t	t
2568	80	29	2017-08-04 08:49:50.279702	t	t
2569	80	29	2017-07-24 08:49:50.27973	t	t
2570	80	34	2017-08-06 08:49:50.279759	t	t
2571	80	8	2017-08-14 08:49:50.279788	t	t
2572	80	22	2017-07-27 08:49:50.279817	t	t
2573	80	36	2017-07-25 08:49:50.279845	t	t
2574	80	18	2017-07-25 08:49:50.279874	t	t
2575	80	10	2017-07-23 08:49:50.279904	t	t
2576	80	36	2017-07-26 08:49:50.279932	t	t
2577	80	26	2017-08-12 08:49:50.279961	t	t
2578	80	20	2017-08-14 08:49:50.27999	t	t
2579	80	13	2017-08-12 08:49:50.280019	t	t
2580	80	29	2017-08-03 08:49:50.280047	t	t
2581	80	31	2017-08-03 08:49:50.280076	f	t
2582	80	20	2017-08-15 08:49:50.280105	f	t
2583	81	33	2017-08-12 08:49:50.280133	t	t
2584	81	18	2017-07-30 08:49:50.280163	t	t
2585	81	34	2017-08-11 08:49:50.280195	t	t
2586	81	12	2017-08-14 08:49:50.280224	t	t
2587	81	26	2017-07-24 08:49:50.280252	t	t
2588	81	35	2017-07-29 08:49:50.28028	f	t
2589	81	25	2017-08-05 08:49:50.280309	f	t
2590	81	12	2017-08-04 08:49:50.280338	f	t
2591	81	23	2017-07-31 08:49:50.280368	f	t
2592	81	26	2017-07-25 08:49:50.280397	f	t
2593	82	29	2017-08-06 08:49:50.280426	t	t
2594	82	20	2017-08-10 08:49:50.280454	t	t
2595	82	35	2017-07-26 08:49:50.280483	t	t
2596	82	18	2017-08-08 08:49:50.280513	t	t
2597	82	15	2017-08-02 08:49:50.280542	t	t
2598	82	23	2017-07-22 08:49:50.280571	t	t
2599	82	22	2017-08-03 08:49:50.280599	t	t
2600	82	29	2017-07-29 08:49:50.280627	t	t
2601	82	15	2017-07-22 08:49:50.280655	t	t
2602	82	37	2017-08-04 08:49:50.280683	t	t
2603	82	16	2017-07-24 08:49:50.280711	t	t
2604	82	20	2017-07-30 08:49:50.280739	t	t
2605	82	29	2017-08-07 08:49:50.280768	t	t
2606	82	20	2017-07-24 08:49:50.280797	t	t
2607	82	11	2017-08-10 08:49:50.280825	t	t
2608	82	18	2017-07-22 08:49:50.280853	t	t
2609	82	31	2017-08-02 08:49:50.280883	t	t
2610	82	17	2017-07-25 08:49:50.280913	t	t
2611	82	8	2017-08-01 08:49:50.280941	t	t
2612	82	26	2017-07-31 08:49:50.280969	t	t
2613	82	28	2017-07-25 08:49:50.280998	t	t
2614	82	21	2017-08-11 08:49:50.281026	f	t
2615	82	31	2017-08-05 08:49:50.281055	f	t
2616	82	32	2017-08-06 08:49:50.281085	f	t
2617	82	14	2017-08-05 08:49:50.281113	f	t
2618	82	12	2017-07-23 08:49:50.281159	f	t
2619	82	17	2017-07-25 08:49:50.281199	f	t
2620	82	21	2017-08-11 08:49:50.281227	f	t
2621	82	32	2017-08-14 08:49:50.281256	f	t
2622	82	8	2017-07-21 08:49:50.281284	f	t
2623	82	29	2017-07-23 08:49:50.281312	f	t
2624	82	36	2017-08-13 08:49:50.281341	f	t
2625	82	24	2017-08-05 08:49:50.281369	f	t
2626	82	20	2017-08-02 08:49:50.281397	f	t
2627	82	37	2017-07-24 08:49:50.281425	f	t
2628	82	26	2017-08-09 08:49:50.281453	f	t
2629	82	34	2017-08-01 08:49:50.281481	f	t
2630	82	7	2017-07-27 08:49:50.281509	f	t
2631	82	28	2017-07-28 08:49:50.281538	f	t
2632	82	12	2017-07-23 08:49:50.28157	f	t
2633	82	26	2017-07-21 08:49:50.281598	f	t
2634	82	18	2017-07-30 08:49:50.281626	f	t
\.


--
-- Name: clicked_statements_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('clicked_statements_uid_seq', 2634, true);


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
1	Town has to cut spending 	town-has-to-cut-spending	Our town needs to cut spending. Please discuss ideas how this should be done.		2017-08-15 08:49:42.497813	2	1	t
2	Cat or Dog	cat-or-dog	Your family argues about whether to buy a cat or dog as pet. Now your opinion matters!		2017-08-15 08:49:42.49799	2	1	f
3	Make the world better	make-the-world-better	How can we make this world a better place?		2017-08-15 08:49:42.498125	2	1	f
4	Elektroautos	elektroautos	Elektroautos - Die Autos der Zukunft? Bitte diskutieren Sie dazu.		2017-08-15 08:49:42.498255	2	2	f
5	Unterstützung der Sekretariate	unterstutzung-der-sekretariate	Unsere Sekretariate in der Informatik sind arbeitsmäßig stark überlastet. Bitte diskutieren Sie Möglichkeiten um dies zu verbessern.		2017-08-15 08:49:42.499135	2	2	f
6	Verbesserung des Informatik-Studiengangs	verbesserung-des-informatik-studiengangs	Wie können der Informatik-Studiengang verbessert und die Probleme, die durch die große Anzahl der Studierenden entstanden sind, gelöst werden?	Die Anzahl der Studierenden in der Informatik hat sich in den letzten Jahren stark erhöht. Dadurch treten zahlreiche Probleme auf, wie z.B. Raumknappheit, überfüllte Lehrveranstaltungen und ein Mangel an Plätzen zum Lernen. Wir möchten Sie gerne dazu einladen, gemeinsam mit den Dozierenden der Informatik über Lösungsmöglichkeiten zu diskutieren: Wie können der Studiengang verbessert und die Probleme, die durch die große Anzahl der Studierenden entstanden sind, gelöst werden?	2017-08-15 08:49:42.499274	2	2	t
7	Bürgerbeteiligung in der Kommune	burgerbeteiligung-in-der-kommune	Es werden Vorschläge zur Verbesserung des Zusammenlebens in unserer Kommune gesammelt.		2017-08-15 08:49:42.499411	2	2	f
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
1	14	1	t	2017-08-15 08:49:45.522244
2	16	1	f	2017-08-15 08:49:45.522409
3	17	1	t	2017-08-15 08:49:45.522596
4	22	1	t	2017-08-15 08:49:45.522708
5	23	1	t	2017-08-15 08:49:45.52279
6	20	2	f	2017-08-15 08:49:45.522869
7	21	2	t	2017-08-15 08:49:45.522946
8	18	2	f	2017-08-15 08:49:45.523024
9	34	2	t	2017-08-15 08:49:45.523101
10	24	2	f	2017-08-15 08:49:45.523178
11	25	2	f	2017-08-15 08:49:45.523271
12	26	2	f	2017-08-15 08:49:45.52335
13	27	3	f	2017-08-15 08:49:45.523427
14	28	3	f	2017-08-15 08:49:45.523505
15	33	3	f	2017-08-15 08:49:45.523582
16	19	8	t	2017-08-15 08:49:45.523659
17	35	8	t	2017-08-15 08:49:45.523737
18	36	8	t	2017-08-15 08:49:45.523813
19	14	11	t	2017-08-15 08:49:50.844339
20	16	11	f	2017-08-15 08:49:50.844425
21	17	11	t	2017-08-15 08:49:50.844515
22	22	11	t	2017-08-15 08:49:50.844592
23	23	11	t	2017-08-15 08:49:50.844669
24	20	12	f	2017-08-15 08:49:50.844746
25	21	12	t	2017-08-15 08:49:50.844822
26	18	12	f	2017-08-15 08:49:50.8449
27	34	12	t	2017-08-15 08:49:50.844977
28	24	12	f	2017-08-15 08:49:50.845055
29	25	12	f	2017-08-15 08:49:50.845163
30	26	12	f	2017-08-15 08:49:50.845236
31	27	13	f	2017-08-15 08:49:50.845298
32	28	13	f	2017-08-15 08:49:50.845358
33	33	13	f	2017-08-15 08:49:50.845419
34	19	18	t	2017-08-15 08:49:50.84548
35	35	18	t	2017-08-15 08:49:50.845541
36	36	18	t	2017-08-15 08:49:50.845603
\.


--
-- Name: last_reviewers_delete_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('last_reviewers_delete_uid_seq', 36, true);


--
-- Data for Name: last_reviewers_duplicates; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY last_reviewers_duplicates (uid, reviewer_uid, review_uid, is_okay, "timestamp") FROM stdin;
1	12	1	t	2017-08-15 08:49:45.523909
2	13	2	t	2017-08-15 08:49:45.523991
3	14	2	t	2017-08-15 08:49:45.524068
4	12	4	t	2017-08-15 08:49:50.845677
5	13	5	t	2017-08-15 08:49:50.845741
6	14	5	t	2017-08-15 08:49:50.845802
\.


--
-- Name: last_reviewers_duplicates_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('last_reviewers_duplicates_uid_seq', 6, true);


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

COPY last_reviewers_merge (uid, reviewer_uid, review_uid, is_okay, "timestamp") FROM stdin;
\.


--
-- Name: last_reviewers_merge_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('last_reviewers_merge_uid_seq', 1, false);


--
-- Data for Name: last_reviewers_optimization; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY last_reviewers_optimization (uid, reviewer_uid, review_uid, is_okay, "timestamp") FROM stdin;
1	29	1	t	2017-08-15 08:49:45.521603
2	31	1	t	2017-08-15 08:49:45.521735
3	32	1	t	2017-08-15 08:49:45.521827
4	12	2	f	2017-08-15 08:49:45.521914
5	13	2	f	2017-08-15 08:49:45.521998
6	15	2	f	2017-08-15 08:49:45.522088
7	29	7	t	2017-08-15 08:49:50.843747
8	31	7	t	2017-08-15 08:49:50.843896
9	32	7	t	2017-08-15 08:49:50.843987
10	12	8	f	2017-08-15 08:49:50.844073
11	13	8	f	2017-08-15 08:49:50.844156
12	15	8	f	2017-08-15 08:49:50.84424
\.


--
-- Name: last_reviewers_optimization_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('last_reviewers_optimization_uid_seq', 12, true);


--
-- Data for Name: last_reviewers_split; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY last_reviewers_split (uid, reviewer_uid, review_uid, is_okay, "timestamp") FROM stdin;
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
1	1	1	f	1	2017-08-15 08:49:42.743093	2	t
2	2	5	f	1	2017-08-15 08:49:42.743269	2	f
3	3	6	f	1	2017-08-15 08:49:42.743364	2	f
4	4	7	f	1	2017-08-15 08:49:42.743462	2	f
5	5	8	f	1	2017-08-15 08:49:42.743551	2	f
6	6	9	f	1	2017-08-15 08:49:42.743638	2	f
7	7	10	f	1	2017-08-15 08:49:42.743723	2	f
8	8	11	f	1	2017-08-15 08:49:42.743808	2	f
9	9	12	f	1	2017-08-15 08:49:42.743893	2	f
10	10	13	f	1	2017-08-15 08:49:42.743978	2	f
11	11	14	f	1	2017-08-15 08:49:42.744062	2	f
12	12	15	f	1	2017-08-15 08:49:42.744146	2	f
13	12	16	f	1	2017-08-15 08:49:42.744231	2	f
14	13	17	f	1	2017-08-15 08:49:42.744316	2	f
15	14	18	f	1	2017-08-15 08:49:42.744401	2	f
16	15	19	f	1	2017-08-15 08:49:42.744486	2	f
17	16	20	f	1	2017-08-15 08:49:42.74457	2	f
18	17	21	f	1	2017-08-15 08:49:42.744655	2	f
19	18	22	f	1	2017-08-15 08:49:42.74474	2	f
20	19	23	f	1	2017-08-15 08:49:42.744826	2	f
21	20	24	f	1	2017-08-15 08:49:42.744911	2	f
22	21	25	f	1	2017-08-15 08:49:42.744996	2	f
23	22	26	f	1	2017-08-15 08:49:42.745081	2	f
24	23	27	f	1	2017-08-15 08:49:42.745213	2	f
25	24	28	f	1	2017-08-15 08:49:42.745307	2	f
26	25	29	f	1	2017-08-15 08:49:42.7454	2	f
27	26	30	f	1	2017-08-15 08:49:42.745492	2	f
28	27	31	f	1	2017-08-15 08:49:42.745584	2	f
29	28	32	f	1	2017-08-15 08:49:42.745676	2	f
30	29	33	f	1	2017-08-15 08:49:42.745767	2	f
31	30	34	f	1	2017-08-15 08:49:42.745859	2	f
32	9	35	f	1	2017-08-15 08:49:42.74595	2	f
33	31	39	f	1	2017-08-15 08:49:42.746042	1	f
34	32	40	f	1	2017-08-15 08:49:42.746132	1	f
35	33	41	f	1	2017-08-15 08:49:42.746222	1	f
36	34	42	f	1	2017-08-15 08:49:42.746311	1	f
37	35	43	f	1	2017-08-15 08:49:42.746402	1	f
38	36	44	f	1	2017-08-15 08:49:42.746492	1	f
39	37	45	f	1	2017-08-15 08:49:42.746583	1	f
40	38	46	f	1	2017-08-15 08:49:42.746674	1	f
41	39	47	f	1	2017-08-15 08:49:42.746765	1	f
42	40	48	f	1	2017-08-15 08:49:42.746858	1	f
43	41	49	f	1	2017-08-15 08:49:42.746962	1	f
44	42	50	f	1	2017-08-15 08:49:42.747054	1	f
45	43	51	f	1	2017-08-15 08:49:42.747145	1	f
46	44	52	f	1	2017-08-15 08:49:42.747236	1	f
47	45	53	f	1	2017-08-15 08:49:42.747327	1	f
48	46	54	f	1	2017-08-15 08:49:42.747418	1	f
49	47	55	f	1	2017-08-15 08:49:42.747509	1	f
50	48	56	f	1	2017-08-15 08:49:42.747599	1	f
51	49	57	f	1	2017-08-15 08:49:42.74769	1	f
52	52	61	f	1	2017-08-15 08:49:42.747978	4	f
53	53	62	f	1	2017-08-15 08:49:42.748072	4	f
54	54	63	f	1	2017-08-15 08:49:42.748167	4	f
55	55	64	f	1	2017-08-15 08:49:42.748339	4	f
56	56	65	f	1	2017-08-15 08:49:42.748433	4	f
57	57	66	f	1	2017-08-15 08:49:42.748524	4	f
58	50	59	f	1	2017-08-15 08:49:42.747792	4	f
59	51	60	f	1	2017-08-15 08:49:42.747886	4	f
60	61	68	f	5	2017-08-15 08:49:42.74862	4	f
61	62	71	f	1	2017-08-15 08:49:42.748713	5	f
62	63	72	f	1	2017-08-15 08:49:42.748806	5	f
63	64	73	f	1	2017-08-15 08:49:42.748901	5	f
64	65	74	f	1	2017-08-15 08:49:42.748993	5	f
65	66	75	f	1	2017-08-15 08:49:42.749088	5	f
66	67	77	f	1	2017-08-15 08:49:42.749186	7	f
67	68	78	f	1	2017-08-15 08:49:42.749281	7	f
68	69	79	f	1	2017-08-15 08:49:42.749373	7	f
69	70	80	f	1	2017-08-15 08:49:42.749467	7	f
70	70	81	f	1	2017-08-15 08:49:42.749559	7	f
71	71	82	f	1	2017-08-15 08:49:42.74965	7	f
\.


--
-- Name: premises_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('premises_uid_seq', 71, true);


--
-- Data for Name: reputation_history; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY reputation_history (uid, reputator_uid, reputation_uid, "timestamp") FROM stdin;
1	23	1	2017-08-13 08:49:45.555833
2	23	2	2017-08-14 08:49:45.555833
3	23	3	2017-08-15 08:49:45.555833
4	25	1	2017-08-13 08:49:45.555833
5	25	2	2017-08-14 08:49:45.555833
6	25	3	2017-08-15 08:49:45.555833
7	22	1	2017-08-13 08:49:45.555833
8	22	2	2017-08-14 08:49:45.555833
9	22	3	2017-08-15 08:49:45.555833
10	34	1	2017-08-13 08:49:45.555833
11	34	2	2017-08-14 08:49:45.555833
12	34	3	2017-08-15 08:49:45.555833
13	3	1	2017-08-13 08:49:45.555833
14	3	2	2017-08-14 08:49:45.555833
15	3	3	2017-08-15 08:49:45.555833
16	3	8	2017-08-15 08:49:45.555833
17	3	3	2017-08-13 08:49:45.555833
18	3	4	2017-08-13 08:49:45.555833
19	3	5	2017-08-14 08:49:45.555833
20	3	6	2017-08-14 08:49:45.555833
21	3	9	2017-08-15 08:49:45.555833
22	3	8	2017-08-15 08:49:45.555833
23	2	4	2017-08-13 08:49:45.555833
24	2	5	2017-08-13 08:49:45.555833
25	2	6	2017-08-14 08:49:45.555833
26	2	9	2017-08-14 08:49:45.555833
27	2	7	2017-08-15 08:49:45.555833
28	2	10	2017-08-15 08:49:45.555833
29	2	8	2017-08-15 08:49:45.555833
30	2	11	2017-08-15 08:49:45.555833
31	2	12	2017-08-15 08:49:45.555833
32	23	1	2017-08-13 08:49:50.875802
33	23	2	2017-08-14 08:49:50.875802
34	23	3	2017-08-15 08:49:50.875802
35	25	1	2017-08-13 08:49:50.875802
36	25	2	2017-08-14 08:49:50.875802
37	25	3	2017-08-15 08:49:50.875802
38	22	1	2017-08-13 08:49:50.875802
39	22	2	2017-08-14 08:49:50.875802
40	22	3	2017-08-15 08:49:50.875802
41	34	1	2017-08-13 08:49:50.875802
42	34	2	2017-08-14 08:49:50.875802
43	34	3	2017-08-15 08:49:50.875802
44	3	1	2017-08-13 08:49:50.875802
45	3	2	2017-08-14 08:49:50.875802
46	3	3	2017-08-15 08:49:50.875802
47	3	8	2017-08-15 08:49:50.875802
48	3	3	2017-08-13 08:49:50.875802
49	3	4	2017-08-13 08:49:50.875802
50	3	5	2017-08-14 08:49:50.875802
51	3	6	2017-08-14 08:49:50.875802
52	3	9	2017-08-15 08:49:50.875802
53	3	8	2017-08-15 08:49:50.875802
54	2	4	2017-08-13 08:49:50.875802
55	2	5	2017-08-13 08:49:50.875802
56	2	6	2017-08-14 08:49:50.875802
57	2	9	2017-08-14 08:49:50.875802
58	2	7	2017-08-15 08:49:50.875802
59	2	10	2017-08-15 08:49:50.875802
60	2	8	2017-08-15 08:49:50.875802
61	2	11	2017-08-15 08:49:50.875802
62	2	12	2017-08-15 08:49:50.875802
\.


--
-- Name: reputation_history_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('reputation_history_uid_seq', 62, true);


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
1	18	11	\N	2017-08-15 08:49:45.493751	t	2	f
2	19	9	\N	2017-08-15 08:49:45.493829	t	1	f
3	20	\N	23	2017-08-15 08:49:45.493904	t	2	f
4	21	\N	25	2017-08-15 08:49:45.493976	f	2	f
5	22	\N	7	2017-08-15 08:49:45.494049	f	2	f
6	23	\N	7	2017-08-15 08:49:45.494121	f	1	f
7	24	27	\N	2017-08-15 08:49:45.494192	f	2	f
8	25	24	\N	2017-08-15 08:49:45.494265	f	1	f
9	26	27	\N	2017-08-15 08:49:45.494336	f	1	f
10	27	1	\N	2017-08-15 08:49:45.49441	t	1	f
11	18	7	\N	2017-08-15 08:49:50.815778	t	1	f
12	19	23	\N	2017-08-15 08:49:50.815858	t	1	f
13	20	\N	28	2017-08-15 08:49:50.815932	t	2	f
14	21	\N	21	2017-08-15 08:49:50.816004	f	1	f
15	22	\N	18	2017-08-15 08:49:50.816089	f	2	f
16	23	\N	22	2017-08-15 08:49:50.816218	f	1	f
17	24	24	\N	2017-08-15 08:49:50.81631	f	2	f
18	25	30	\N	2017-08-15 08:49:50.816384	f	1	f
19	26	12	\N	2017-08-15 08:49:50.816457	f	2	f
20	27	1	\N	2017-08-15 08:49:50.816532	t	1	f
\.


--
-- Name: review_deletes_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('review_deletes_uid_seq', 20, true);


--
-- Data for Name: review_duplicates; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY review_duplicates (uid, detector_uid, duplicate_statement_uid, original_statement_uid, "timestamp", is_executed, is_revoked) FROM stdin;
1	28	6	1	2017-08-15 08:49:45.494489	f	f
2	29	4	1	2017-08-15 08:49:45.49456	t	f
3	29	22	7	2017-08-15 08:49:45.494626	f	f
4	28	6	1	2017-08-15 08:49:50.816611	f	f
5	29	4	1	2017-08-15 08:49:50.816682	t	f
6	29	22	7	2017-08-15 08:49:50.816749	f	f
\.


--
-- Name: review_duplicates_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('review_duplicates_uid_seq', 6, true);


--
-- Data for Name: review_edit_values; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY review_edit_values (uid, review_edit_uid, statement_uid, typeof, content) FROM stdin;
1	1	2		as
2	1	2		as
\.


--
-- Name: review_edit_values_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('review_edit_values_uid_seq', 2, true);


--
-- Data for Name: review_edits; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY review_edits (uid, detector_uid, argument_uid, statement_uid, "timestamp", is_executed, is_revoked) FROM stdin;
1	3	\N	2	2017-08-15 08:49:45.571379	f	f
2	3	\N	2	2017-08-15 08:49:50.890522	f	f
\.


--
-- Name: review_edits_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('review_edits_uid_seq', 2, true);


--
-- Data for Name: review_merge; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY review_merge (uid, detector_uid, premisesgroup_uid, "timestamp", is_executed, is_revoked) FROM stdin;
1	31	1	2017-08-15 08:49:45.4947	f	f
2	32	5	2017-08-15 08:49:45.494769	f	f
3	31	1	2017-08-15 08:49:50.816824	f	f
4	32	5	2017-08-15 08:49:50.816894	f	f
\.


--
-- Name: review_merge_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('review_merge_uid_seq', 4, true);


--
-- Data for Name: review_merge_values; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY review_merge_values (uid, review_uid, content) FROM stdin;
1	1	lorem ipsum dolorem sit value01
2	2	lorem ipsum dolorem sit value02
3	3	lorem ipsum dolorem sit value01
4	4	lorem ipsum dolorem sit value02
\.


--
-- Name: review_merge_values_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('review_merge_values_uid_seq', 4, true);


--
-- Data for Name: review_optimizations; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY review_optimizations (uid, detector_uid, argument_uid, statement_uid, "timestamp", is_executed, is_revoked) FROM stdin;
1	12	15	\N	2017-08-15 08:49:45.493257	t	f
2	13	\N	6	2017-08-15 08:49:45.493377	t	f
3	14	\N	18	2017-08-15 08:49:45.493452	f	f
4	16	30	\N	2017-08-15 08:49:45.493592	f	f
5	17	24	\N	2017-08-15 08:49:45.493661	f	f
6	15	\N	24	2017-08-15 08:49:45.493523	f	f
7	12	9	\N	2017-08-15 08:49:50.815277	t	f
8	13	\N	19	2017-08-15 08:49:50.815402	t	f
9	14	\N	13	2017-08-15 08:49:50.815478	f	f
10	16	14	\N	2017-08-15 08:49:50.81562	f	f
11	17	6	\N	2017-08-15 08:49:50.815689	f	f
12	15	\N	22	2017-08-15 08:49:50.81555	f	f
\.


--
-- Name: review_optimizations_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('review_optimizations_uid_seq', 12, true);


--
-- Data for Name: review_split; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY review_split (uid, detector_uid, premisesgroup_uid, "timestamp", is_executed, is_revoked) FROM stdin;
1	33	10	2017-08-15 08:49:45.494874	f	f
2	34	12	2017-08-15 08:49:45.494959	f	f
3	33	10	2017-08-15 08:49:50.816967	f	f
4	34	12	2017-08-15 08:49:50.817036	f	f
\.


--
-- Name: review_split_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('review_split_uid_seq', 4, true);


--
-- Data for Name: review_split_values; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY review_split_values (uid, review_uid, content) FROM stdin;
1	1	lorem ipsum dolorem sit value03
2	1	lorem ipsum dolorem sit value04
3	1	lorem ipsum dolorem sit value05
4	2	lorem ipsum dolorem sit value06
5	2	lorem ipsum dolorem sit value07
6	2	lorem ipsum dolorem sit value08
7	2	lorem ipsum dolorem sit value09
8	2	lorem ipsum dolorem sit value10
9	3	lorem ipsum dolorem sit value03
10	3	lorem ipsum dolorem sit value04
11	3	lorem ipsum dolorem sit value05
12	4	lorem ipsum dolorem sit value06
13	4	lorem ipsum dolorem sit value07
14	4	lorem ipsum dolorem sit value08
15	4	lorem ipsum dolorem sit value09
16	4	lorem ipsum dolorem sit value10
\.


--
-- Name: review_split_values_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('review_split_values_uid_seq', 16, true);


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
1153	1	31
1154	1	22
1155	1	27
1156	1	12
1157	1	20
1158	1	24
1159	1	34
1160	1	8
1161	2	32
1162	2	19
1163	2	26
1164	2	34
1165	2	24
1166	2	14
1167	2	16
1168	2	35
1169	2	21
1170	2	37
1171	2	15
1172	2	18
1173	2	11
1174	2	22
1175	2	23
1176	2	20
1177	2	10
1178	2	9
1179	2	33
1180	2	12
1181	2	7
1182	2	25
1183	2	13
1184	2	17
1185	2	31
1186	2	27
1187	2	29
1188	2	29
1189	3	13
1190	3	10
1191	3	32
1192	3	21
1193	3	37
1194	3	34
1195	3	31
1196	3	20
1197	3	29
1198	3	35
1199	3	28
1200	3	8
1201	3	24
1202	3	7
1203	3	19
1204	3	16
1205	3	29
1206	3	27
1207	4	19
1208	4	21
1209	4	32
1210	4	17
1211	5	27
1212	5	33
1213	5	36
1214	5	22
1215	5	13
1216	5	29
1217	5	12
1218	5	26
1219	5	16
1220	5	34
1221	5	35
1222	8	25
1223	8	27
1224	8	17
1225	8	11
1226	8	31
1227	8	10
1228	8	29
1229	8	28
1230	8	35
1231	8	23
1232	8	12
1233	8	37
1234	8	36
1235	10	35
1236	10	11
1237	10	15
1238	10	8
1239	10	20
1240	10	14
1241	10	13
1242	10	36
1243	10	12
1244	10	37
1245	10	9
1246	10	32
1247	10	28
1248	11	31
1249	11	29
1250	11	20
1251	11	26
1252	11	36
1253	11	13
1254	11	16
1255	12	35
1256	12	11
1257	12	27
1258	12	20
1259	12	25
1260	12	7
1261	12	26
1262	12	29
1263	12	19
1264	12	9
1265	12	15
1266	12	36
1267	12	12
1268	12	37
1269	12	22
1270	12	14
1271	12	23
1272	12	24
1273	12	28
1274	12	17
1275	12	29
1276	12	31
1277	12	10
1278	12	13
1279	12	32
1280	12	16
1281	12	18
1282	12	34
1283	12	8
1284	15	17
1285	15	33
1286	15	15
1287	15	23
1288	15	22
1289	15	36
1290	15	19
1291	16	10
1292	16	9
1293	16	13
1294	16	32
1295	16	21
1296	16	27
1297	16	28
1298	16	35
1299	16	29
1300	16	23
1301	16	19
1302	16	29
1303	16	20
1304	16	7
1305	16	14
1306	16	8
1307	16	34
1308	16	17
1309	16	25
1310	16	26
1311	16	11
1312	16	37
1313	16	36
1314	16	16
1315	16	18
1316	17	16
1317	17	34
1318	17	8
1319	17	31
1320	17	19
1321	17	14
1322	17	13
1323	17	9
1324	17	12
1325	17	37
1326	17	21
1327	17	29
1328	17	32
1329	17	17
1330	17	25
1331	17	27
1332	17	11
1333	17	20
1334	17	29
1335	19	8
1336	19	25
1337	19	24
1338	19	28
1339	19	34
1340	19	14
1341	19	17
1342	19	15
1343	19	21
1344	19	10
1345	19	35
1346	19	18
1347	19	9
1348	19	19
1349	19	29
1350	19	16
1351	19	12
1352	19	11
1353	19	36
1354	19	29
1355	19	20
1356	19	37
1357	20	18
1358	20	32
1359	20	35
1360	20	8
1361	20	22
1362	20	37
1363	20	12
1364	20	36
1365	20	10
1366	20	31
1367	20	14
1368	21	11
1369	21	29
1370	21	28
1371	21	19
1372	21	7
1373	21	24
1374	21	34
1375	21	10
1376	21	26
1377	21	15
1378	21	36
1379	21	27
1380	21	37
1381	21	13
1382	21	12
1383	21	18
1384	21	32
1385	21	35
1386	21	29
1387	21	23
1388	21	25
1389	21	31
1390	21	21
1391	21	9
1392	21	20
1393	21	16
1394	21	33
1395	21	17
1396	21	14
1397	23	34
1398	23	15
1399	23	35
1400	23	28
1401	23	19
1402	23	22
1403	23	29
1404	23	36
1405	23	18
1406	24	12
1407	24	33
1408	24	26
1409	24	32
1410	24	36
1411	24	29
1412	24	9
1413	26	36
1414	26	15
1415	26	17
1416	26	18
1417	26	7
1418	26	13
1419	26	16
1420	26	14
1421	26	32
1422	26	29
1423	26	33
1424	26	23
1425	26	10
1426	26	37
1427	26	27
1428	26	31
1429	26	12
1430	26	8
1431	26	21
1432	26	20
1433	26	19
1434	26	28
1435	26	25
1436	26	29
1437	26	9
1438	26	34
1439	26	22
1440	26	11
1441	27	12
1442	27	26
1443	27	16
1444	27	25
1445	27	13
1446	27	37
1447	27	31
1448	27	17
1449	27	15
1450	27	22
1451	27	29
1452	27	32
1453	27	21
1454	27	35
1455	27	8
1456	27	28
1457	27	14
1458	27	24
1459	27	29
1460	27	36
1461	27	20
1462	27	18
1463	27	33
1464	27	34
1465	28	23
1466	28	37
1467	28	17
1468	28	9
1469	28	16
1470	28	35
1471	28	27
1472	28	28
1473	28	22
1474	28	26
1475	28	32
1476	28	10
1477	28	29
1478	28	14
1479	28	33
1480	28	13
1481	28	8
1482	28	19
1483	28	21
1484	28	24
1485	28	20
1486	28	36
1487	28	34
1488	28	29
1489	28	18
1490	28	31
1491	29	24
1492	29	36
1493	29	17
1494	29	23
1495	29	19
1496	30	29
1497	30	15
1498	30	24
1499	30	16
1500	32	12
1501	32	9
1502	32	25
1503	32	15
1504	32	13
1505	32	10
1506	32	23
1507	34	36
1508	34	22
1509	34	24
1510	34	19
1511	34	17
1512	35	8
1513	35	7
1514	35	34
1515	35	27
1516	35	20
1517	35	21
1518	35	17
1519	35	37
1520	35	32
1521	35	28
1522	35	22
1523	35	36
1524	35	25
1525	35	29
1526	35	10
1527	35	23
1528	35	13
1529	35	15
1530	35	14
1531	35	16
1532	36	29
1533	36	7
1534	36	24
1535	36	27
1536	36	28
1537	36	34
1538	36	26
1539	36	32
1540	36	16
1541	39	12
1542	39	29
1543	39	8
1544	39	23
1545	39	29
1546	39	26
1547	39	20
1548	39	16
1549	39	11
1550	39	19
1551	39	25
1552	39	13
1553	39	21
1554	39	17
1555	39	28
1556	39	32
1557	39	34
1558	39	18
1559	39	22
1560	39	14
1561	39	36
1562	39	27
1563	39	31
1564	39	15
1565	39	9
1566	39	7
1567	39	35
1568	39	24
1569	40	12
1570	40	15
1571	40	18
1572	40	35
1573	40	23
1574	40	29
1575	40	33
1576	40	29
1577	40	26
1578	40	36
1579	40	34
1580	40	37
1581	40	31
1582	40	20
1583	41	32
1584	41	26
1585	41	9
1586	41	28
1587	41	25
1588	41	21
1589	41	37
1590	41	31
1591	41	35
1592	41	34
1593	41	13
1594	41	19
1595	41	12
1596	41	8
1597	41	15
1598	41	27
1599	41	16
1600	41	29
1601	41	10
1602	41	33
1603	41	23
1604	41	18
1605	41	11
1606	41	7
1607	41	22
1608	41	29
1609	41	17
1610	42	21
1611	42	18
1612	42	34
1613	42	20
1614	42	27
1615	42	9
1616	42	14
1617	42	24
1618	42	13
1619	42	17
1620	42	25
1621	42	22
1622	42	23
1623	42	31
1624	42	29
1625	42	28
1626	42	10
1627	42	7
1628	42	11
1629	42	33
1630	42	29
1631	42	12
1632	42	19
1633	42	8
1634	42	32
1635	42	15
1636	42	26
1637	42	16
1638	42	35
1639	44	23
1640	44	29
1641	44	7
1642	44	32
1643	44	35
1644	44	27
1645	44	13
1646	44	33
1647	44	34
1648	44	18
1649	44	20
1650	44	36
1651	44	31
1652	44	11
1653	44	25
1654	44	29
1655	44	19
1656	44	14
1657	44	9
1658	44	21
1659	44	12
1660	44	16
1661	44	28
1662	44	26
1663	44	8
1664	44	24
1665	46	12
1666	46	27
1667	46	28
1668	46	19
1669	46	26
1670	46	31
1671	46	22
1672	46	36
1673	46	14
1674	46	23
1675	46	11
1676	46	8
1677	47	36
1678	47	25
1679	47	9
1680	47	19
1681	47	16
1682	49	28
1683	49	20
1684	49	25
1685	49	27
1686	49	7
1687	49	37
1688	49	14
1689	49	12
1690	49	11
1691	49	33
1692	49	29
1693	50	23
1694	50	24
1695	50	8
1696	50	19
1697	50	15
1698	50	21
1699	50	20
1700	50	13
1701	50	17
1702	50	35
1703	50	29
1704	51	29
1705	51	26
1706	51	23
1707	51	17
1708	51	25
1709	51	14
1710	51	16
1711	51	18
1712	51	19
1713	51	27
1714	51	9
1715	51	12
1716	51	32
1717	51	7
1718	51	8
1719	51	21
1720	51	33
1721	51	37
1722	51	13
1723	51	34
1724	51	22
1725	51	36
1726	51	10
1727	54	13
1728	54	26
1729	54	22
1730	54	32
1731	54	27
1732	54	12
1733	54	8
1734	54	20
1735	54	34
1736	54	16
1737	54	33
1738	54	19
1739	54	7
1740	54	25
1741	54	36
1742	54	21
1743	54	11
1744	54	17
1745	54	10
1746	54	29
1747	54	37
1748	54	18
1749	54	24
1750	54	31
1751	54	29
1752	54	15
1753	54	28
1754	54	9
1755	54	35
1756	55	36
1757	55	33
1758	55	21
1759	55	20
1760	55	8
1761	55	17
1762	55	10
1763	55	37
1764	55	22
1765	55	29
1766	55	16
1767	55	13
1768	55	23
1769	55	34
1770	55	25
1771	55	18
1772	55	11
1773	55	32
1774	55	9
1775	55	29
1776	55	31
1777	55	14
1778	55	24
1779	55	12
1780	55	27
1781	55	19
1782	55	7
1783	56	32
1784	56	13
1785	56	28
1786	56	35
1787	57	21
1788	57	29
1789	57	10
1790	57	34
1791	57	23
1792	57	9
1793	57	33
1794	57	29
1795	57	13
1796	57	31
1797	57	12
1798	57	16
1799	57	11
1800	57	22
1801	57	17
1802	57	24
1803	57	25
1804	57	27
1805	57	18
1806	57	32
1807	57	28
1808	58	35
1809	58	23
1810	58	19
1811	58	20
1812	58	37
1813	58	25
1814	58	26
1815	58	17
1816	58	31
1817	58	28
1818	58	16
1819	58	18
1820	58	22
1821	58	29
1822	58	32
1823	58	34
1824	58	29
1825	58	27
1826	58	21
1827	58	14
1828	58	36
1829	58	12
1830	59	17
1831	59	21
1832	59	14
1833	59	34
1834	59	37
1835	59	35
1836	59	20
1837	60	23
1838	60	9
1839	60	36
1840	60	13
1841	60	11
1842	60	20
1843	60	31
1844	61	25
1845	61	8
1846	61	34
1847	61	11
1848	61	22
1849	61	15
1850	61	16
1851	61	20
1852	61	35
1853	61	7
1854	61	32
1855	61	19
1856	61	27
1857	61	24
1858	61	28
1859	61	13
1860	61	23
1861	61	18
1862	61	21
1863	61	14
1864	62	14
1865	62	26
1866	62	32
1867	62	33
1868	62	23
1869	62	35
1870	62	20
1871	62	22
1872	62	18
1873	62	8
1874	62	36
1875	62	19
1876	62	28
1877	62	11
1878	62	7
1879	62	29
1880	62	13
1881	62	25
1882	62	10
1883	62	17
1884	62	27
1885	63	29
1886	63	21
1887	63	9
1888	63	29
1889	63	14
1890	63	37
1891	64	12
1892	64	31
1893	64	28
1894	64	23
1895	64	25
1896	64	29
1897	64	7
1898	64	11
1899	64	36
1900	64	34
1901	64	29
1902	64	17
1903	64	19
1904	64	18
1905	64	9
1906	64	32
1907	64	20
1908	64	8
1909	64	13
1910	64	27
1911	64	24
1912	64	10
1913	64	16
1914	64	21
1915	64	22
1916	65	8
1917	65	35
1918	65	21
1919	65	18
1920	65	14
1921	65	34
1922	65	23
1923	65	36
1924	65	31
1925	65	32
1926	66	28
1927	66	20
1928	66	12
1929	66	29
1930	66	25
1931	66	10
1932	66	13
1933	66	18
1934	66	29
1935	66	19
1936	66	23
1937	66	33
1938	66	14
1939	66	34
1940	66	31
1941	66	7
1942	66	35
1943	66	26
1944	66	11
1945	66	8
1946	66	17
1947	66	24
1948	66	16
1949	66	9
1950	66	27
1951	66	32
1952	66	37
1953	67	15
1954	67	14
1955	67	7
1956	67	27
1957	67	12
1958	67	21
1959	67	32
1960	67	8
1961	67	22
1962	67	31
1963	67	35
1964	67	11
1965	67	20
1966	67	34
1967	67	24
1968	67	25
1969	68	13
1970	68	7
1971	68	36
1972	68	8
1973	68	28
1974	68	21
1975	68	15
1976	68	24
1977	68	14
1978	68	22
1979	68	32
1980	68	26
1981	68	35
1982	68	12
1983	68	10
1984	68	16
1985	68	19
1986	68	31
1987	68	11
1988	68	27
1989	68	29
1990	68	29
1991	68	33
1992	68	18
1993	6	31
1994	6	25
1995	6	7
1996	6	28
1997	6	27
1998	6	37
1999	6	18
2000	6	19
2001	6	11
2002	6	8
2003	6	21
2004	6	9
2005	6	16
2006	6	13
2007	6	23
2008	6	35
2009	6	20
2010	6	32
2011	6	26
2012	6	17
2013	6	29
2014	6	24
2015	6	12
2016	6	22
2017	6	29
2018	6	14
2019	6	10
2020	6	15
2021	7	36
2022	7	11
2023	7	33
2024	7	18
2025	7	23
2026	7	24
2027	9	19
2028	9	36
2029	9	26
2030	9	12
2031	9	23
2032	9	14
2033	9	11
2034	9	7
2035	9	33
2036	9	32
2037	9	25
2038	9	31
2039	9	29
2040	9	21
2041	9	20
2042	9	29
2043	9	8
2044	9	35
2045	9	27
2046	9	18
2047	13	32
2048	13	10
2049	13	15
2050	13	16
2051	13	31
2052	13	14
2053	14	18
2054	14	35
2055	14	17
2056	14	11
2057	14	34
2058	14	27
2059	14	25
2060	14	9
2061	14	33
2062	14	37
2063	14	13
2064	14	22
2065	14	24
2066	14	31
2067	14	19
2068	18	32
2069	18	31
2070	18	23
2071	18	11
2072	18	15
2073	18	18
2074	22	27
2075	22	12
2076	22	31
2077	22	23
2078	22	20
2079	22	9
2080	22	21
2081	22	14
2082	22	29
2083	22	15
2084	22	17
2085	22	32
2086	22	13
2087	22	24
2088	22	29
2089	22	28
2090	22	26
2091	22	37
2092	22	19
2093	22	34
2094	22	16
2095	22	18
2096	22	25
2097	25	24
2098	25	32
2099	25	22
2100	25	21
2101	25	18
2102	25	7
2103	25	29
2104	25	11
2105	25	27
2106	25	33
2107	25	16
2108	25	17
2109	25	35
2110	25	20
2111	25	34
2112	25	10
2113	25	37
2114	25	25
2115	25	12
2116	25	15
2117	25	36
2118	25	31
2119	25	26
2120	25	23
2121	25	19
2122	31	18
2123	31	36
2124	31	25
2125	31	29
2126	31	20
2127	31	8
2128	31	14
2129	31	24
2130	31	11
2131	31	19
2132	31	12
2133	31	7
2134	31	34
2135	31	37
2136	31	33
2137	31	16
2138	31	23
2139	31	10
2140	31	32
2141	31	9
2142	33	22
2143	33	24
2144	33	12
2145	33	34
2146	33	23
2147	33	14
2148	33	29
2149	33	32
2150	33	19
2151	37	29
2152	37	35
2153	37	32
2154	37	36
2155	37	17
2156	37	23
2157	37	28
2158	37	8
2159	37	16
2160	37	19
2161	37	21
2162	37	33
2163	37	24
2164	37	31
2165	37	13
2166	37	26
2167	37	27
2168	37	12
2169	37	29
2170	37	22
2171	37	20
2172	37	7
2173	38	32
2174	38	29
2175	38	17
2176	38	29
2177	38	13
2178	38	16
2179	38	28
2180	38	37
2181	38	11
2182	38	24
2183	38	7
2184	38	9
2185	38	26
2186	38	25
2187	38	8
2188	38	10
2189	38	15
2190	38	23
2191	38	34
2192	38	35
2193	38	12
2194	38	20
2195	38	19
2196	38	31
2197	43	33
2198	43	28
2199	43	24
2200	43	7
2201	43	19
2202	45	20
2203	45	27
2204	45	21
2205	45	14
2206	45	32
2207	45	29
2208	45	16
2209	45	17
2210	45	22
2211	45	11
2212	45	35
2213	45	31
2214	45	28
2215	45	24
2216	45	23
2217	45	37
2218	48	24
2219	48	13
2220	48	27
2221	48	12
2222	52	18
2223	52	29
2224	52	22
2225	52	13
2226	52	14
2227	52	28
2228	52	19
2229	52	20
2230	52	36
2231	52	17
2232	53	12
2233	53	21
2234	53	34
2235	53	15
2236	53	7
2237	53	33
2238	53	29
2239	53	31
2240	53	37
2241	53	16
2242	53	20
2243	53	11
2244	53	29
2245	53	9
2246	53	8
2247	53	27
2248	53	17
2249	53	18
2250	53	19
2251	53	28
2252	53	32
2253	53	26
2254	53	22
2255	53	24
2256	53	14
2257	53	35
2258	53	25
2259	53	23
2260	53	36
2261	69	18
2262	69	12
2263	69	11
2264	69	27
2265	69	21
2266	69	33
\.


--
-- Name: seen_arguments_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('seen_arguments_uid_seq', 2266, true);


--
-- Data for Name: seen_statements; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY seen_statements (uid, statement_uid, user_uid) FROM stdin;
1527	1	7
1528	1	15
1529	1	10
1530	1	11
1531	1	14
1532	1	12
1533	1	17
1534	1	18
1535	1	22
1536	1	8
1537	2	8
1538	2	27
1539	2	12
1540	2	11
1541	2	21
1542	2	9
1543	2	20
1544	2	28
1545	2	18
1546	2	15
1547	2	36
1548	2	33
1549	2	14
1550	2	23
1551	2	37
1552	2	22
1553	2	25
1554	2	13
1555	2	17
1556	2	35
1557	2	10
1558	2	31
1559	2	7
1560	2	29
1561	3	15
1562	3	23
1563	3	27
1564	3	20
1565	3	26
1566	4	10
1567	4	24
1568	4	22
1569	4	29
1570	5	12
1571	5	10
1572	5	11
1573	5	16
1574	5	8
1575	5	25
1576	5	35
1577	5	33
1578	5	19
1579	5	32
1580	5	34
1581	5	29
1582	5	36
1583	5	13
1584	5	18
1585	5	28
1586	5	7
1587	5	24
1588	6	13
1589	6	23
1590	6	7
1591	6	24
1592	6	20
1593	6	22
1594	6	18
1595	6	15
1596	6	17
1597	6	12
1598	6	35
1599	6	10
1600	6	21
1601	6	37
1602	6	26
1603	6	25
1604	6	34
1605	6	11
1606	6	9
1607	6	14
1608	6	29
1609	6	19
1610	7	10
1611	7	20
1612	7	16
1613	7	21
1614	7	25
1615	7	8
1616	7	23
1617	7	19
1618	7	35
1619	7	24
1620	7	29
1621	7	29
1622	7	26
1623	7	33
1624	7	11
1625	7	15
1626	7	37
1627	7	18
1628	7	12
1629	7	17
1630	7	27
1631	7	7
1632	7	13
1633	7	28
1634	7	9
1635	8	35
1636	8	29
1637	8	32
1638	8	11
1639	8	12
1640	8	21
1641	8	37
1642	8	28
1643	8	10
1644	8	23
1645	8	29
1646	8	27
1647	8	14
1648	8	25
1649	8	34
1650	8	22
1651	8	7
1652	8	20
1653	8	16
1654	8	13
1655	8	33
1656	8	9
1657	8	17
1658	8	36
1659	8	26
1660	8	31
1661	8	18
1662	8	8
1663	9	13
1664	9	9
1665	9	21
1666	9	23
1667	9	10
1668	9	12
1669	9	34
1670	9	11
1671	9	22
1672	9	32
1673	9	18
1674	10	33
1675	10	25
1676	10	32
1677	10	19
1678	10	15
1679	10	8
1680	11	28
1681	11	11
1682	11	31
1683	11	21
1684	11	9
1685	11	16
1686	11	35
1687	11	25
1688	11	10
1689	11	14
1690	11	29
1691	11	29
1692	11	22
1693	11	8
1694	11	37
1695	11	32
1696	11	12
1697	11	34
1698	11	17
1699	12	25
1700	12	12
1701	12	33
1702	12	7
1703	12	28
1704	12	36
1705	12	19
1706	12	29
1707	12	29
1708	12	35
1709	12	8
1710	12	10
1711	12	17
1712	12	20
1713	12	22
1714	12	11
1715	12	16
1716	12	27
1717	13	12
1718	13	31
1719	13	19
1720	13	18
1721	13	21
1722	13	33
1723	13	29
1724	13	34
1725	13	32
1726	13	24
1727	13	17
1728	13	22
1729	13	25
1730	13	36
1731	13	27
1732	13	23
1733	13	14
1734	13	26
1735	13	10
1736	13	16
1737	13	11
1738	13	35
1739	13	28
1740	14	26
1741	14	20
1742	14	17
1743	14	7
1744	14	15
1745	14	9
1746	14	28
1747	14	19
1748	14	33
1749	14	32
1750	14	21
1751	14	36
1752	14	23
1753	14	31
1754	14	12
1755	14	11
1756	14	13
1757	14	14
1758	14	16
1759	14	22
1760	14	8
1761	14	10
1762	15	36
1763	15	8
1764	15	25
1765	15	26
1766	15	31
1767	15	32
1768	15	22
1769	15	15
1770	15	29
1771	15	14
1772	15	13
1773	15	21
1774	15	34
1775	15	23
1776	15	24
1777	15	37
1778	15	10
1779	15	19
1780	15	17
1781	15	29
1782	15	35
1783	16	25
1784	16	21
1785	16	34
1786	16	12
1787	16	20
1788	17	33
1789	17	9
1790	17	32
1791	17	29
1792	17	28
1793	17	8
1794	17	14
1795	17	34
1796	18	13
1797	18	7
1798	18	16
1799	18	21
1800	18	19
1801	18	22
1802	18	33
1803	18	35
1804	18	8
1805	18	20
1806	19	27
1807	19	34
1808	19	28
1809	19	11
1810	19	14
1811	19	7
1812	19	25
1813	19	26
1814	19	36
1815	19	8
1816	20	19
1817	20	27
1818	20	14
1819	20	15
1820	20	35
1821	20	33
1822	20	16
1823	20	22
1824	20	29
1825	20	29
1826	20	37
1827	20	7
1828	20	17
1829	20	18
1830	20	36
1831	20	11
1832	20	34
1833	20	23
1834	20	10
1835	20	21
1836	20	9
1837	20	32
1838	20	20
1839	21	15
1840	21	10
1841	21	26
1842	21	19
1843	21	34
1844	21	21
1845	21	14
1846	21	17
1847	21	22
1848	21	37
1849	21	29
1850	21	20
1851	21	8
1852	21	29
1853	21	16
1854	21	24
1855	21	32
1856	21	18
1857	21	25
1858	21	27
1859	21	11
1860	21	35
1861	21	9
1862	21	28
1863	22	14
1864	22	9
1865	22	36
1866	22	17
1867	22	12
1868	22	31
1869	22	35
1870	22	22
1871	22	25
1872	22	11
1873	22	34
1874	22	37
1875	22	15
1876	22	16
1877	22	7
1878	22	32
1879	22	21
1880	22	27
1881	22	29
1882	22	28
1883	22	33
1884	22	29
1885	23	33
1886	23	27
1887	23	18
1888	23	34
1889	23	24
1890	23	8
1891	23	23
1892	23	15
1893	23	12
1894	23	16
1895	23	37
1896	23	10
1897	23	21
1898	23	11
1899	23	14
1900	24	34
1901	24	29
1902	24	32
1903	24	11
1904	24	26
1905	24	23
1906	24	35
1907	24	17
1908	24	9
1909	25	13
1910	25	35
1911	25	29
1912	25	20
1913	25	37
1914	25	27
1915	25	29
1916	25	24
1917	25	23
1918	25	25
1919	26	24
1920	26	18
1921	26	32
1922	26	26
1923	27	16
1924	27	28
1925	27	13
1926	27	25
1927	27	12
1928	27	17
1929	27	33
1930	27	10
1931	27	29
1932	27	19
1933	28	24
1934	28	20
1935	28	29
1936	28	28
1937	28	36
1938	28	23
1939	28	31
1940	28	17
1941	28	14
1942	28	22
1943	28	12
1944	28	33
1945	28	13
1946	28	8
1947	28	19
1948	28	10
1949	28	7
1950	28	18
1951	29	20
1952	29	9
1953	29	16
1954	29	11
1955	29	8
1956	29	12
1957	29	35
1958	29	37
1959	29	19
1960	29	10
1961	29	26
1962	29	32
1963	29	23
1964	29	36
1965	29	15
1966	29	27
1967	29	34
1968	29	13
1969	29	21
1970	29	7
1971	29	29
1972	29	17
1973	29	29
1974	29	31
1975	29	28
1976	29	14
1977	29	33
1978	29	18
1979	30	23
1980	30	12
1981	30	11
1982	30	25
1983	30	31
1984	30	20
1985	30	8
1986	30	7
1987	30	21
1988	30	32
1989	30	37
1990	30	14
1991	30	13
1992	31	35
1993	31	8
1994	31	7
1995	31	34
1996	31	32
1997	31	10
1998	31	19
1999	31	33
2000	31	31
2001	31	15
2002	31	21
2003	31	37
2004	31	18
2005	31	29
2006	31	12
2007	31	24
2008	31	16
2009	31	28
2010	31	11
2011	31	36
2012	32	32
2013	32	37
2014	32	11
2015	32	10
2016	32	23
2017	32	18
2018	32	28
2019	32	36
2020	32	24
2021	32	20
2022	32	15
2023	32	16
2024	32	29
2025	32	12
2026	32	26
2027	32	35
2028	32	25
2029	32	22
2030	33	34
2031	33	23
2032	33	37
2033	33	36
2034	33	18
2035	33	13
2036	33	20
2037	33	25
2038	33	9
2039	33	17
2040	33	19
2041	33	33
2042	33	16
2043	33	32
2044	33	31
2045	33	35
2046	33	21
2047	33	27
2048	34	29
2049	34	28
2050	34	14
2051	34	17
2052	34	27
2053	34	36
2054	34	25
2055	34	15
2056	34	18
2057	34	7
2058	34	16
2059	34	32
2060	34	22
2061	34	12
2062	34	9
2063	35	16
2064	35	29
2065	35	23
2066	35	34
2067	35	31
2068	35	10
2069	35	35
2070	35	29
2071	35	28
2072	35	36
2073	35	12
2074	35	7
2075	35	8
2076	35	20
2077	35	13
2078	35	24
2079	35	19
2080	35	32
2081	35	9
2082	35	25
2083	35	37
2084	35	22
2085	36	9
2086	36	32
2087	36	10
2088	36	31
2089	36	7
2090	36	14
2091	36	11
2092	36	21
2093	36	36
2094	36	12
2095	36	15
2096	36	25
2097	36	33
2098	36	8
2099	36	24
2100	36	34
2101	36	29
2102	36	22
2103	36	16
2104	36	28
2105	37	15
2106	37	12
2107	37	27
2108	37	29
2109	37	29
2110	37	8
2111	37	7
2112	37	34
2113	37	31
2114	37	37
2115	37	24
2116	37	17
2117	37	33
2118	37	26
2119	37	21
2120	37	19
2121	37	11
2122	37	14
2123	37	36
2124	37	32
2125	37	23
2126	37	9
2127	38	8
2128	38	12
2129	38	27
2130	38	13
2131	38	7
2132	38	11
2133	38	28
2134	38	17
2135	38	24
2136	39	23
2137	39	31
2138	39	35
2139	39	25
2140	39	34
2141	39	32
2142	39	18
2143	39	29
2144	39	13
2145	39	7
2146	39	12
2147	39	29
2148	39	36
2149	39	17
2150	40	36
2151	40	14
2152	40	31
2153	40	9
2154	40	29
2155	40	7
2156	40	22
2157	41	20
2158	41	32
2159	41	33
2160	41	29
2161	41	10
2162	41	36
2163	41	8
2164	41	28
2165	41	35
2166	41	13
2167	41	16
2168	41	14
2169	41	11
2170	41	9
2171	42	37
2172	42	11
2173	42	29
2174	42	18
2175	42	16
2176	42	8
2177	42	22
2178	43	13
2179	43	29
2180	43	32
2181	43	20
2182	43	24
2183	43	37
2184	43	31
2185	43	33
2186	43	27
2187	43	11
2188	43	9
2189	43	34
2190	43	18
2191	43	17
2192	43	23
2193	43	29
2194	43	14
2195	43	10
2196	43	19
2197	43	16
2198	43	25
2199	43	26
2200	44	32
2201	44	22
2202	44	17
2203	44	7
2204	45	12
2205	45	17
2206	45	11
2207	45	29
2208	45	22
2209	45	31
2210	45	19
2211	45	35
2212	45	15
2213	45	27
2214	45	37
2215	45	21
2216	45	33
2217	45	29
2218	45	32
2219	45	24
2220	45	18
2221	45	26
2222	45	13
2223	45	28
2224	45	10
2225	45	25
2226	45	34
2227	45	16
2228	45	14
2229	45	7
2230	45	23
2231	46	25
2232	46	27
2233	46	14
2234	46	35
2235	46	29
2236	46	32
2237	46	29
2238	46	24
2239	46	21
2240	46	23
2241	46	13
2242	46	15
2243	46	8
2244	46	22
2245	46	10
2246	46	7
2247	46	36
2248	46	16
2249	46	34
2250	46	26
2251	46	31
2252	46	37
2253	46	9
2254	46	28
2255	46	19
2256	46	33
2257	47	16
2258	47	20
2259	47	8
2260	47	7
2261	47	23
2262	47	11
2263	47	14
2264	47	19
2265	47	31
2266	47	28
2267	47	25
2268	47	17
2269	47	34
2270	47	22
2271	47	21
2272	47	12
2273	47	33
2274	47	32
2275	47	24
2276	47	13
2277	47	10
2278	47	29
2279	47	18
2280	47	37
2281	47	35
2282	47	15
2283	47	26
2284	47	27
2285	47	29
2286	48	17
2287	48	31
2288	48	13
2289	48	32
2290	49	7
2291	49	25
2292	49	36
2293	49	15
2294	49	34
2295	49	10
2296	49	9
2297	49	31
2298	49	22
2299	49	26
2300	49	32
2301	49	20
2302	49	28
2303	49	11
2304	49	14
2305	49	29
2306	49	24
2307	49	29
2308	49	18
2309	49	12
2310	49	37
2311	49	23
2312	49	13
2313	49	27
2314	49	8
2315	50	14
2316	50	15
2317	50	28
2318	50	32
2319	50	16
2320	51	31
2321	51	25
2322	51	33
2323	51	18
2324	51	35
2325	51	36
2326	51	12
2327	51	8
2328	51	22
2329	51	28
2330	51	16
2331	51	29
2332	51	37
2333	51	11
2334	51	14
2335	51	19
2336	51	7
2337	51	27
2338	51	23
2339	51	20
2340	51	26
2341	51	29
2342	51	34
2343	51	13
2344	51	32
2345	51	17
2346	51	24
2347	51	10
2348	52	11
2349	52	29
2350	52	27
2351	52	35
2352	52	7
2353	52	28
2354	52	26
2355	52	16
2356	52	12
2357	52	32
2358	52	19
2359	52	14
2360	52	17
2361	52	22
2362	52	15
2363	52	33
2364	52	23
2365	52	13
2366	52	24
2367	52	9
2368	52	21
2369	52	29
2370	52	8
2371	52	20
2372	52	34
2373	52	10
2374	53	23
2375	53	18
2376	53	8
2377	53	33
2378	53	21
2379	53	29
2380	53	20
2381	53	12
2382	53	17
2383	53	24
2384	53	10
2385	53	13
2386	53	22
2387	53	29
2388	53	19
2389	53	16
2390	53	14
2391	54	29
2392	54	11
2393	54	20
2394	54	25
2395	54	13
2396	54	17
2397	54	33
2398	54	31
2399	54	24
2400	54	12
2401	54	26
2402	54	23
2403	54	9
2404	54	27
2405	54	18
2406	54	35
2407	54	16
2408	54	10
2409	54	15
2410	54	7
2411	54	8
2412	54	29
2413	54	21
2414	54	36
2415	54	14
2416	55	35
2417	55	34
2418	55	16
2419	55	7
2420	55	28
2421	55	24
2422	55	32
2423	55	19
2424	55	8
2425	55	11
2426	55	15
2427	55	10
2428	55	23
2429	55	31
2430	55	25
2431	55	29
2432	55	26
2433	55	18
2434	55	22
2435	55	29
2436	55	12
2437	55	27
2438	55	36
2439	55	17
2440	55	9
2441	55	37
2442	55	13
2443	56	27
2444	56	29
2445	56	10
2446	56	17
2447	56	15
2448	56	36
2449	56	21
2450	56	13
2451	56	34
2452	56	25
2453	56	14
2454	56	31
2455	56	29
2456	56	8
2457	56	22
2458	56	28
2459	56	19
2460	56	16
2461	56	18
2462	56	7
2463	56	12
2464	56	23
2465	57	28
2466	57	33
2467	57	14
2468	57	8
2469	57	26
2470	57	31
2471	57	29
2472	57	11
2473	57	10
2474	57	32
2475	58	31
2476	58	22
2477	58	15
2478	58	35
2479	58	16
2480	58	11
2481	58	23
2482	58	8
2483	58	18
2484	58	17
2485	58	10
2486	59	8
2487	59	7
2488	59	9
2489	59	32
2490	59	29
2491	59	23
2492	59	14
2493	59	34
2494	60	24
2495	60	12
2496	60	20
2497	60	29
2498	60	36
2499	60	31
2500	60	8
2501	60	27
2502	60	17
2503	60	16
2504	60	37
2505	60	32
2506	60	25
2507	60	26
2508	60	11
2509	60	15
2510	60	23
2511	60	28
2512	60	13
2513	60	34
2514	61	13
2515	61	19
2516	61	14
2517	61	33
2518	61	11
2519	61	16
2520	61	35
2521	61	28
2522	61	12
2523	61	7
2524	61	29
2525	61	8
2526	61	36
2527	61	23
2528	61	17
2529	61	9
2530	61	29
2531	61	25
2532	61	20
2533	61	32
2534	61	24
2535	61	18
2536	61	27
2537	62	31
2538	62	11
2539	62	19
2540	62	28
2541	62	33
2542	62	25
2543	62	7
2544	62	16
2545	62	20
2546	62	36
2547	62	13
2548	62	18
2549	62	17
2550	62	32
2551	62	23
2552	62	34
2553	62	26
2554	62	37
2555	62	12
2556	62	35
2557	62	29
2558	62	27
2559	62	15
2560	62	14
2561	62	29
2562	63	15
2563	63	10
2564	63	14
2565	63	36
2566	63	25
2567	63	11
2568	63	17
2569	63	19
2570	63	32
2571	63	12
2572	63	21
2573	63	29
2574	63	35
2575	63	37
2576	63	34
2577	63	22
2578	63	27
2579	63	28
2580	63	13
2581	63	26
2582	63	24
2583	63	7
2584	63	18
2585	64	27
2586	64	25
2587	64	7
2588	64	17
2589	64	23
2590	64	34
2591	64	20
2592	64	33
2593	64	32
2594	64	29
2595	64	31
2596	64	10
2597	64	29
2598	64	24
2599	64	12
2600	64	22
2601	64	8
2602	64	28
2603	64	19
2604	64	18
2605	64	9
2606	64	11
2607	64	14
2608	64	36
2609	65	27
2610	65	34
2611	65	28
2612	65	36
2613	65	37
2614	65	29
2615	65	7
2616	65	14
2617	65	19
2618	65	32
2619	65	11
2620	65	18
2621	66	14
2622	66	31
2623	66	21
2624	66	29
2625	66	18
2626	66	19
2627	66	13
2628	66	29
2629	66	35
2630	66	11
2631	66	23
2632	66	7
2633	66	24
2634	66	28
2635	66	36
2636	66	37
2637	66	10
2638	66	32
2639	66	25
2640	66	27
2641	66	12
2642	66	20
2643	67	22
2644	67	11
2645	67	10
2646	67	18
2647	67	24
2648	67	29
2649	67	33
2650	67	23
2651	67	16
2652	67	21
2653	67	20
2654	67	34
2655	67	26
2656	67	32
2657	67	25
2658	67	28
2659	67	27
2660	67	7
2661	68	19
2662	68	24
2663	68	15
2664	68	23
2665	68	29
2666	68	9
2667	68	31
2668	68	28
2669	68	26
2670	69	11
2671	69	35
2672	69	32
2673	69	16
2674	69	23
2675	69	25
2676	69	33
2677	69	29
2678	69	18
2679	69	37
2680	69	24
2681	69	8
2682	69	31
2683	69	7
2684	69	19
2685	69	12
2686	69	10
2687	69	26
2688	69	36
2689	69	21
2690	69	17
2691	69	27
2692	70	15
2693	70	26
2694	70	27
2695	70	17
2696	70	35
2697	70	11
2698	70	18
2699	70	34
2700	70	14
2701	70	8
2702	70	33
2703	70	19
2704	70	29
2705	70	32
2706	70	13
2707	70	20
2708	70	12
2709	70	7
2710	70	9
2711	70	37
2712	70	36
2713	70	21
2714	71	35
2715	71	17
2716	71	14
2717	71	9
2718	71	26
2719	71	23
2720	71	20
2721	71	24
2722	71	13
2723	71	19
2724	72	23
2725	72	14
2726	72	29
2727	72	19
2728	72	31
2729	72	35
2730	73	31
2731	73	9
2732	73	8
2733	73	19
2734	73	17
2735	73	21
2736	73	7
2737	73	34
2738	73	13
2739	73	23
2740	73	25
2741	73	35
2742	73	33
2743	73	16
2744	73	26
2745	73	24
2746	73	36
2747	73	15
2748	73	28
2749	73	32
2750	73	20
2751	73	22
2752	73	11
2753	73	18
2754	73	10
2755	73	27
2756	73	12
2757	73	37
2758	74	16
2759	74	23
2760	74	34
2761	74	25
2762	74	28
2763	74	31
2764	74	9
2765	74	21
2766	74	19
2767	74	20
2768	74	22
2769	74	35
2770	74	37
2771	74	29
2772	74	27
2773	74	8
2774	74	33
2775	74	15
2776	74	18
2777	74	14
2778	74	36
2779	74	29
2780	74	11
2781	74	13
2782	74	24
2783	75	11
2784	75	14
2785	75	37
2786	75	15
2787	75	23
2788	75	33
2789	75	12
2790	75	29
2791	75	24
2792	75	31
2793	75	25
2794	75	26
2795	75	18
2796	75	8
2797	75	36
2798	75	28
2799	76	18
2800	76	17
2801	76	36
2802	76	11
2803	76	23
2804	76	26
2805	76	20
2806	76	31
2807	76	14
2808	76	7
2809	76	22
2810	76	10
2811	77	14
2812	77	9
2813	77	19
2814	77	18
2815	77	36
2816	77	15
2817	77	21
2818	77	35
2819	77	26
2820	77	23
2821	77	29
2822	77	32
2823	77	34
2824	77	20
2825	77	16
2826	77	25
2827	78	29
2828	78	13
2829	78	23
2830	78	31
2831	78	18
2832	79	21
2833	79	16
2834	79	22
2835	79	24
2836	79	17
2837	79	14
2838	79	9
2839	79	10
2840	79	26
2841	79	25
2842	79	13
2843	79	35
2844	79	36
2845	79	31
2846	79	19
2847	79	32
2848	79	29
2849	79	23
2850	79	27
2851	79	7
2852	79	18
2853	79	8
2854	79	28
2855	80	8
2856	80	14
2857	80	33
2858	80	10
2859	80	12
2860	80	31
2861	80	13
2862	80	7
2863	80	29
2864	80	18
2865	80	11
2866	80	32
2867	80	29
2868	80	23
2869	80	22
2870	80	9
2871	80	19
2872	80	28
2873	80	26
2874	80	36
2875	80	20
2876	80	34
2877	80	17
2878	80	35
2879	81	37
2880	81	13
2881	81	26
2882	81	24
2883	81	20
2884	81	17
2885	81	10
2886	81	18
2887	81	32
2888	81	27
2889	82	15
2890	82	17
2891	82	32
2892	82	16
2893	82	8
2894	82	35
2895	82	33
2896	82	27
2897	82	34
2898	82	28
2899	82	11
2900	82	13
2901	82	23
2902	82	31
2903	82	21
2904	82	18
2905	82	37
2906	82	12
2907	82	25
2908	82	29
2909	82	22
2910	82	9
2911	82	26
2912	82	7
2913	82	20
2914	82	36
2915	82	29
2916	82	24
\.


--
-- Name: seen_statements_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('seen_statements_uid_seq', 2916, true);


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
1	Ein Radar überwacht den Abstand, eine Frontkamera erkennt Fahrspuren und andere Verkehrsteilnehmer, und je sechs Ultraschallsensoren vorne und hinten helfen beim Einparken und messen während der Fahrt Distanzen im Zentimeterbereich	localhost:3449	/devcards/index.html	5	68	4	2017-08-15 08:49:41.862787
2	Zunächst einmal unterscheidet sich die Hardware für den Autopiloten nicht oder nur marginal von dem, was selbst für einen VW Polo erhältlich ist	localhost:3449	/	5	68	4	2017-08-15 08:49:41.862787
3	Katzen sind kleine Tiger	http://www.iflscience.com/	plants-and-animals/no-your-cat-isnt-plotting-kill-youbut-it-has-lions-personality/	2	15	2	2017-08-15 08:49:41.862787
4	Katzen sind kleine Tiger	http://www.iflscience.com/	plants-and-animals/no-your-cat-isnt-plotting-kill-youbut-it-has-lions-personality/	2	16	2	2017-08-15 08:49:41.862787
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
-- Data for Name: statements_merged; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY statements_merged (uid, review_uid, statement_uid, new_statement_uid, "timestamp") FROM stdin;
\.


--
-- Name: statements_merged_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('statements_merged_uid_seq', 1, false);


--
-- Data for Name: statements_splitted; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY statements_splitted (uid, review_uid, new_statement_uid, "timestamp") FROM stdin;
\.


--
-- Name: statements_splitted_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('statements_splitted_uid_seq', 1, false);


--
-- Name: statements_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('statements_uid_seq', 82, true);


--
-- Data for Name: textversions; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY textversions (uid, statement_uid, content, author_uid, "timestamp", is_disabled) FROM stdin;
1	2	we should get a cat	1	2017-08-06 08:49:42.642988	f
2	3	we should get a dog	1	2017-08-13 08:49:42.643131	f
3	4	we could get both, a cat and a dog	1	2017-07-29 08:49:42.64318	f
4	5	cats are very independent	1	2017-08-11 08:49:42.643222	f
5	6	cats are capricious	1	2017-08-02 08:49:42.643259	f
6	7	dogs can act as watch dogs	1	2017-08-03 08:49:42.643295	f
7	8	you have to take the dog for a walk every day, which is tedious	1	2017-07-30 08:49:42.64333	f
8	9	we have no use for a watch dog	1	2017-08-08 08:49:42.643365	f
9	10	going for a walk with the dog every day is good for social interaction and physical exercise	1	2017-08-04 08:49:42.643401	f
10	11	it would be no problem	1	2017-07-21 08:49:42.643435	f
11	12	a cat and a dog will generally not get along well	1	2017-07-31 08:49:42.643469	f
12	13	we do not have enough money for two pets	1	2017-08-05 08:49:42.643504	f
13	14	a dog costs taxes and will be more expensive than a cat	1	2017-07-26 08:49:42.64354	f
14	15	cats are fluffy	1	2017-08-11 08:49:42.643576	f
15	16	cats are small	1	2017-07-22 08:49:42.64361	f
16	17	fluffy animals losing much hair and I'm allergic to animal hair	1	2017-08-07 08:49:42.643645	f
17	18	you could use a automatic vacuum cleaner	1	2017-08-13 08:49:42.643679	f
18	19	cats ancestors are animals in wildlife, who are hunting alone and not in groups	1	2017-08-06 08:49:42.643713	f
19	20	this is not true for overbred races	1	2017-08-11 08:49:42.643748	f
20	21	this lies in their the natural conditions	1	2017-07-26 08:49:42.643781	f
21	22	the purpose of a pet is to have something to take care of	1	2017-08-04 08:49:42.643815	f
22	23	several cats of friends of mine are real as*holes	1	2017-08-01 08:49:42.643849	f
23	24	the fact, that cats are capricious, is based on the cats race	1	2017-07-25 08:49:42.643883	f
24	25	not every cat is capricious	1	2017-07-30 08:49:42.643916	f
25	26	this is based on the cats race and a little bit on the breeding	1	2017-08-01 08:49:42.64395	f
26	27	next to the taxes you will need equipment like a dog lead, anti-flea-spray, and so on	1	2017-08-10 08:49:42.643983	f
27	28	the equipment for running costs of cats and dogs are nearly the same	1	2017-07-28 08:49:42.644017	f
28	29	this is just a claim without any justification	1	2017-08-12 08:49:42.644052	f
29	30	in Germany you have to pay for your second dog even more taxes!	1	2017-07-31 08:49:42.644085	f
30	31	it is important, that pets are small and fluffy!	1	2017-08-06 08:49:42.644119	f
31	32	cats are little, sweet and innocent cuddle toys	1	2017-08-05 08:49:42.644154	f
32	33	do you have ever seen a sphinx cat or savannah cats?	1	2017-07-25 08:49:42.644188	f
33	34	it is much work to take care of both animals	1	2017-08-02 08:49:42.644222	f
34	35	won't be best friends	1	2017-07-29 08:49:42.644255	f
35	36	the city should reduce the number of street festivals	3	2017-08-06 08:49:42.644301	f
36	37	we should shut down University Park	3	2017-07-30 08:49:42.644335	f
37	38	we should close public swimming pools	1	2017-08-06 08:49:42.64437	f
38	39	reducing the number of street festivals can save up to $50.000 a year	1	2017-07-28 08:49:42.644405	f
39	40	every street festival is funded by large companies	1	2017-07-22 08:49:42.64444	f
40	41	then we will have more money to expand out pedestrian zone	1	2017-07-27 08:49:42.644475	f
41	42	our city will get more attractive for shopping	1	2017-07-23 08:49:42.644509	f
42	43	street festivals attract many people, which will increase the citys income	1	2017-08-13 08:49:42.644545	f
43	44	spending of the city for these festivals are higher than the earnings	1	2017-07-23 08:49:42.644579	f
44	45	money does not solve problems of our society	1	2017-08-15 08:49:42.644614	f
45	46	criminals use University Park to sell drugs	1	2017-07-25 08:49:42.644648	f
46	47	shutting down University Park will save $100.000 a year	1	2017-08-06 08:49:42.644683	f
47	48	we should not give in to criminals	1	2017-08-08 08:49:42.644717	f
48	49	the number of police patrols has been increased recently	1	2017-07-25 08:49:42.644752	f
49	50	this is the only park in our city	1	2017-08-02 08:49:42.644786	f
50	51	there are many parks in neighbouring towns	1	2017-08-10 08:49:42.644821	f
51	52	the city is planing a new park in the upcoming month	3	2017-07-26 08:49:42.644856	f
52	53	parks are very important for our climate	3	2017-07-22 08:49:42.64489	f
53	54	our swimming pools are very old and it would take a major investment to repair them	3	2017-08-12 08:49:42.644925	f
54	55	schools need the swimming pools for their sports lessons	1	2017-07-29 08:49:42.644959	f
55	56	the rate of non-swimmers is too high	1	2017-08-13 08:49:42.644994	f
56	57	the police cannot patrol in the park for 24/7	1	2017-08-05 08:49:42.645029	f
57	58	E-Autos "optimal" für den Stadtverkehr sind	1	2017-08-15 08:49:42.645063	f
58	59	dadurch die Lärmbelästigung in der Stadt sinkt	1	2017-08-11 08:49:42.645097	f
77	77	Straßenfeste viel Lärm verursachen	1	2017-08-15 08:49:42.64578	f
59	60	die Anzahl an Ladestationen in der Stadt nicht ausreichend ist	1	2017-08-15 08:49:42.645157	f
60	61	das Unfallrisiko steigt, da die Autos kaum Geräusche verursachen	1	2017-08-05 08:49:42.645195	f
61	62	die Autos auch zuhause geladen werden können und das pro Tag ausreichen sollte	1	2017-08-10 08:49:42.64523	f
62	63	Elektroautos keine lauten Geräusche beim Anfahren produzieren	1	2017-07-24 08:49:42.645276	f
63	64	Lärmbelästigung kein wirkliches Problem in den Städten ist	1	2017-08-02 08:49:42.64531	f
64	65	nicht jede normale Tankstelle auch Stromtankstellen hat	1	2017-07-26 08:49:42.645343	f
65	66	die Länder und Kommunen den Ausbau nun stark fördern wollen	1	2017-07-26 08:49:42.645376	f
66	67	E-Autos das autonome Fahren vorantreiben	5	2017-07-24 08:49:42.645409	f
67	68	Tesla mutig bestehende Techniken einsetzt und zeigt was sie können	5	2017-08-01 08:49:42.645443	f
68	69	durch rücksichtsvolle Verhaltensanpassungen der wissenschaftlichen Mitarbeitenden der Arbeitsaufwand der Sekretärinnen gesenkt werden könnte	1	2017-08-13 08:49:42.645477	f
69	70	wir Standard-Formulare, wie Urlaubsanträge, selbst faxen können	1	2017-07-28 08:49:42.645511	f
70	71	etliche Abläufe durch ein besseres Zusammenarbeiten optimiert werden können. Dies sollte auch schriftlich als Anleitungen festgehalten werden, damit neue Angestellt einen leichten Einstieg finden	1	2017-08-12 08:49:42.645545	f
71	72	viele Arbeiten auch durch die Mitarbeiter erledigt werden können	1	2017-07-26 08:49:42.645578	f
72	73	"rücksichtsvolle Verhaltensanpassungen" viel zu allgemein gehalten ist	1	2017-08-01 08:49:42.645611	f
73	74	das Faxgerät nicht immer zugänglich ist, wenn die Sekretärinnen nicht anwesend sind	1	2017-08-04 08:49:42.645645	f
74	75	wir keine eigenen Faxgeräte haben und so oder so entweder bei Martin stören müssten oder doch bei Sabine im Büro landen würden	1	2017-08-15 08:49:42.64568	f
75	1	Cats are fucking stupid and bloody fuzzy critters!	1	2017-07-31 08:49:42.645713	f
76	76	Die Anzahl der Straßenfeste sollte reduziert werden	1	2017-07-24 08:49:42.645747	f
78	78	Straßenfeste ein wichtiger Bestandteil unserer Kultur sind	1	2017-08-03 08:49:42.645813	f
79	79	Straßenfeste der Kommune Geld einbringen	1	2017-07-30 08:49:42.645846	f
80	80	die Einnahmen der Kommune durch Straßenfeste nur gering sind	1	2017-07-25 08:49:42.645879	f
81	81	Straßenfeste der Kommune hohe Kosten verursachen durch Polizeieinsätze, Säuberung, etc.	1	2017-07-22 08:49:42.645921	f
82	82	die Innenstadt ohnehin sehr laut ist	1	2017-08-11 08:49:42.645956	f
\.


--
-- Name: textversions_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('textversions_uid_seq', 82, true);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY users (uid, firstname, surname, nickname, public_nickname, email, gender, password, group_uid, last_action, last_login, registered, token, token_timestamp) FROM stdin;
1	anonymous	anonymous	anonymous	anonymous		m	$2a$10$oYZMOLZyGGp0b/CWY6Y2MO.uyQkiAAvNsnMRCIEUwG4F3sYJF2wG6	3	2017-08-15 08:49:42.457938	2017-08-15 08:49:42.458186	2017-08-15 08:49:42.458299		\N
3	Christian	Meter	Christian	Christian	meter@cs.uni-duesseldorf.de	m	$2a$10$Ou/pHV1MoZRqvt5U8cV09up0qqbIz70ZjwEeanRkyyfR/rrMHcBfe	1	2017-08-15 08:49:42.458799	2017-08-15 08:49:42.458871	2017-08-15 08:49:42.458927		\N
4	Björn	Ebbinghaus	Björn	Björn	bjoern.ebbinghaus@uni-duesseldorf.de	m	$2a$10$LZgst1jCYPxA6vqcVCEsZ.27ksOWA8uYjAD/1IatOIXwgfasbP3E.	1	2017-08-15 08:49:42.465232	2017-08-15 08:49:42.46533	2017-08-15 08:49:42.465395		\N
5	Teresa	Uebber	Teresa	Teresa	teresa.uebber@uni-duesseldorf.de	f	$2a$10$42fgly7zwzYnnxMr6iuMvOY8r8NfyEH6qLLgsibYkHBD3SasSd3hG	1	2017-08-15 08:49:42.465507	2017-08-15 08:49:42.465572	2017-08-15 08:49:42.465632		\N
6	Bob	Bubbles	Bob	Bob	tobias.krauthoff+dbas.usert31@gmail.com	n	$2a$10$U5zi0Qlu96bgAQtNYoTgleaLtlpQUZa/LuLAM7zestAY2Ev/doIzm	1	2017-08-15 08:49:42.465736	2017-08-15 08:49:42.465798	2017-08-15 08:49:42.465857		\N
7	Pascal	Lux	Pascal	Pascal	tobias.krauthoff+dbas.usert00@gmail.com	m	$2a$10$U5zi0Qlu96bgAQtNYoTgleaLtlpQUZa/LuLAM7zestAY2Ev/doIzm	3	2017-08-15 08:49:42.466069	2017-08-15 08:49:42.466125	2017-08-15 08:49:42.466174		\N
8	Kurt	Hecht	Kurt	Kurt	tobias.krauthoff+dbas.usert01@gmail.com	m	$2a$10$U5zi0Qlu96bgAQtNYoTgleaLtlpQUZa/LuLAM7zestAY2Ev/doIzm	3	2017-08-15 08:49:42.466258	2017-08-15 08:49:42.466309	2017-08-15 08:49:42.466358		\N
9	Torben	Hartl	Torben	Torben	tobias.krauthoff+dbas.usert02@gmail.com	m	$2a$10$U5zi0Qlu96bgAQtNYoTgleaLtlpQUZa/LuLAM7zestAY2Ev/doIzm	3	2017-08-15 08:49:42.466442	2017-08-15 08:49:42.466493	2017-08-15 08:49:42.466541		\N
10	Thorsten	Scherer	Thorsten	Thorsten	tobias.krauthoff+dbas.usert03@gmail.com	m	$2a$10$U5zi0Qlu96bgAQtNYoTgleaLtlpQUZa/LuLAM7zestAY2Ev/doIzm	3	2017-08-15 08:49:42.466624	2017-08-15 08:49:42.466675	2017-08-15 08:49:42.466723		\N
11	Friedrich	Schutte	Friedrich	Friedrich	tobias.krauthoff+dbas.usert04@gmail.com	m	$2a$10$U5zi0Qlu96bgAQtNYoTgleaLtlpQUZa/LuLAM7zestAY2Ev/doIzm	3	2017-08-15 08:49:42.466805	2017-08-15 08:49:42.466855	2017-08-15 08:49:42.466903		\N
12	Aayden	Westermann	Aayden	Aayden	tobias.krauthoff+dbas.usert05@gmail.com	m	$2a$10$U5zi0Qlu96bgAQtNYoTgleaLtlpQUZa/LuLAM7zestAY2Ev/doIzm	3	2017-08-15 08:49:42.466992	2017-08-15 08:49:42.467038	2017-08-15 08:49:42.467082		\N
13	Hermann	Grasshoff	Hermann	Hermann	tobias.krauthoff+dbas.usert06@gmail.com	m	$2a$10$U5zi0Qlu96bgAQtNYoTgleaLtlpQUZa/LuLAM7zestAY2Ev/doIzm	3	2017-08-15 08:49:42.467156	2017-08-15 08:49:42.467201	2017-08-15 08:49:42.467244		\N
14	Wolf	Himmler	Wolf	Wolf	tobias.krauthoff+dbas.usert07@gmail.com	m	$2a$10$U5zi0Qlu96bgAQtNYoTgleaLtlpQUZa/LuLAM7zestAY2Ev/doIzm	3	2017-08-15 08:49:42.467318	2017-08-15 08:49:42.467364	2017-08-15 08:49:42.467409		\N
15	Jakob	Winter	Jakob	Jakob	tobias.krauthoff+dbas.usert08@gmail.com	m	$2a$10$U5zi0Qlu96bgAQtNYoTgleaLtlpQUZa/LuLAM7zestAY2Ev/doIzm	3	2017-08-15 08:49:42.467483	2017-08-15 08:49:42.467529	2017-08-15 08:49:42.467572		\N
16	Alwin	Wechter	Alwin	Alwin	tobias.krauthoff+dbas.usert09@gmail.com	m	$2a$10$U5zi0Qlu96bgAQtNYoTgleaLtlpQUZa/LuLAM7zestAY2Ev/doIzm	3	2017-08-15 08:49:42.467649	2017-08-15 08:49:42.467695	2017-08-15 08:49:42.467739		\N
17	Walter	Weisser	Walter	Walter	tobias.krauthoff+dbas.usert10@gmail.com	m	$2a$10$U5zi0Qlu96bgAQtNYoTgleaLtlpQUZa/LuLAM7zestAY2Ev/doIzm	3	2017-08-15 08:49:42.467814	2017-08-15 08:49:42.46786	2017-08-15 08:49:42.467903		\N
18	Volker	Keitel	Volker	Volker	tobias.krauthoff+dbas.usert11@gmail.com	m	$2a$10$U5zi0Qlu96bgAQtNYoTgleaLtlpQUZa/LuLAM7zestAY2Ev/doIzm	3	2017-08-15 08:49:42.467977	2017-08-15 08:49:42.468023	2017-08-15 08:49:42.468066		\N
19	Benedikt	Feuerstein	Benedikt	Benedikt	tobias.krauthoff+dbas.usert12@gmail.com	m	$2a$10$U5zi0Qlu96bgAQtNYoTgleaLtlpQUZa/LuLAM7zestAY2Ev/doIzm	3	2017-08-15 08:49:42.46814	2017-08-15 08:49:42.468186	2017-08-15 08:49:42.468231		\N
20	Engelbert	Gottlieb	Engelbert	Engelbert	tobias.krauthoff+dbas.usert13@gmail.com	m	$2a$10$U5zi0Qlu96bgAQtNYoTgleaLtlpQUZa/LuLAM7zestAY2Ev/doIzm	3	2017-08-15 08:49:42.468306	2017-08-15 08:49:42.468351	2017-08-15 08:49:42.468394		\N
21	Elias	Auerbach	Elias	Elias	tobias.krauthoff+dbas.usert14@gmail.com	m	$2a$10$U5zi0Qlu96bgAQtNYoTgleaLtlpQUZa/LuLAM7zestAY2Ev/doIzm	3	2017-08-15 08:49:42.468467	2017-08-15 08:49:42.468512	2017-08-15 08:49:42.468555		\N
22	Rupert	Wenz	Rupert	Rupert	tobias.krauthoff+dbas.usert15@gmail.com	m	$2a$10$U5zi0Qlu96bgAQtNYoTgleaLtlpQUZa/LuLAM7zestAY2Ev/doIzm	3	2017-08-15 08:49:42.468628	2017-08-15 08:49:42.468673	2017-08-15 08:49:42.468717		\N
23	Marga	Wegscheider	Marga	Marga	tobias.krauthoff+dbas.usert16@gmail.com	f	$2a$10$U5zi0Qlu96bgAQtNYoTgleaLtlpQUZa/LuLAM7zestAY2Ev/doIzm	3	2017-08-15 08:49:42.468793	2017-08-15 08:49:42.468841	2017-08-15 08:49:42.468885		\N
24	Larissa	Clauberg	Larissa	Larissa	tobias.krauthoff+dbas.usert17@gmail.com	f	$2a$10$U5zi0Qlu96bgAQtNYoTgleaLtlpQUZa/LuLAM7zestAY2Ev/doIzm	3	2017-08-15 08:49:42.468964	2017-08-15 08:49:42.46901	2017-08-15 08:49:42.469053		\N
25	Emmi	Rosch	Emmi	Emmi	tobias.krauthoff+dbas.usert18@gmail.com	f	$2a$10$U5zi0Qlu96bgAQtNYoTgleaLtlpQUZa/LuLAM7zestAY2Ev/doIzm	3	2017-08-15 08:49:42.469132	2017-08-15 08:49:42.469179	2017-08-15 08:49:42.469222		\N
26	Konstanze	Krebs	Konstanze	Konstanze	tobias.krauthoff+dbas.usert19@gmail.com	f	$2a$10$U5zi0Qlu96bgAQtNYoTgleaLtlpQUZa/LuLAM7zestAY2Ev/doIzm	3	2017-08-15 08:49:42.4693	2017-08-15 08:49:42.469346	2017-08-15 08:49:42.46939		\N
27	Catrin	Fahnrich	Catrin	Catrin	tobias.krauthoff+dbas.usert20@gmail.com	f	$2a$10$U5zi0Qlu96bgAQtNYoTgleaLtlpQUZa/LuLAM7zestAY2Ev/doIzm	3	2017-08-15 08:49:42.469465	2017-08-15 08:49:42.46951	2017-08-15 08:49:42.469553		\N
28	Antonia	Bartram	Antonia	Antonia	tobias.krauthoff+dbas.usert21@gmail.com	f	$2a$10$U5zi0Qlu96bgAQtNYoTgleaLtlpQUZa/LuLAM7zestAY2Ev/doIzm	3	2017-08-15 08:49:42.469626	2017-08-15 08:49:42.469671	2017-08-15 08:49:42.469713		\N
29	Nora	Kempf	Nora	Nora	tobias.krauthoff+dbas.usert22@gmail.com	f	$2a$10$U5zi0Qlu96bgAQtNYoTgleaLtlpQUZa/LuLAM7zestAY2Ev/doIzm	3	2017-08-15 08:49:42.469786	2017-08-15 08:49:42.469831	2017-08-15 08:49:42.469874		\N
30	Julia	Wetter	Julia	Julia	tobias.krauthoff+dbas.usert23@gmail.com	f	$2a$10$U5zi0Qlu96bgAQtNYoTgleaLtlpQUZa/LuLAM7zestAY2Ev/doIzm	3	2017-08-15 08:49:42.469964	2017-08-15 08:49:42.470013	2017-08-15 08:49:42.470057		\N
31	Jutta	Munch	Jutta	Jutta	tobias.krauthoff+dbas.usert24@gmail.com	f	$2a$10$U5zi0Qlu96bgAQtNYoTgleaLtlpQUZa/LuLAM7zestAY2Ev/doIzm	3	2017-08-15 08:49:42.470133	2017-08-15 08:49:42.47018	2017-08-15 08:49:42.470224		\N
32	Helga	Heilmann	Helga	Helga	tobias.krauthoff+dbas.usert25@gmail.com	f	$2a$10$U5zi0Qlu96bgAQtNYoTgleaLtlpQUZa/LuLAM7zestAY2Ev/doIzm	3	2017-08-15 08:49:42.4703	2017-08-15 08:49:42.470347	2017-08-15 08:49:42.470392		\N
33	Denise	Tietjen	Denise	Denise	tobias.krauthoff+dbas.usert26@gmail.com	f	$2a$10$U5zi0Qlu96bgAQtNYoTgleaLtlpQUZa/LuLAM7zestAY2Ev/doIzm	3	2017-08-15 08:49:42.470471	2017-08-15 08:49:42.470517	2017-08-15 08:49:42.470562		\N
34	Hanne	Beckmann	Hanne	Hanne	tobias.krauthoff+dbas.usert27@gmail.com	f	$2a$10$U5zi0Qlu96bgAQtNYoTgleaLtlpQUZa/LuLAM7zestAY2Ev/doIzm	3	2017-08-15 08:49:42.470639	2017-08-15 08:49:42.470685	2017-08-15 08:49:42.470729		\N
35	Elly	Landauer	Elly	Elly	tobias.krauthoff+dbas.usert28@gmail.com	f	$2a$10$U5zi0Qlu96bgAQtNYoTgleaLtlpQUZa/LuLAM7zestAY2Ev/doIzm	3	2017-08-15 08:49:42.470805	2017-08-15 08:49:42.470851	2017-08-15 08:49:42.470903		\N
36	Sybille	Redlich	Sybille	Sybille	tobias.krauthoff+dbas.usert29@gmail.com	f	$2a$10$U5zi0Qlu96bgAQtNYoTgleaLtlpQUZa/LuLAM7zestAY2Ev/doIzm	3	2017-08-15 08:49:42.470976	2017-08-15 08:49:42.471021	2017-08-15 08:49:42.471066		\N
37	Ingeburg	Fischer	Ingeburg	Ingeburg	tobias.krauthoff+dbas.usert30@gmail.com	f	$2a$10$U5zi0Qlu96bgAQtNYoTgleaLtlpQUZa/LuLAM7zestAY2Ev/doIzm	3	2017-08-15 08:49:42.47114	2017-08-15 08:49:42.471186	2017-08-15 08:49:42.471228		\N
2	Tobias	Krauthoff	Tobias	Tobias	krauthoff@cs.uni-duesseldorf.de	m	$2a$10$9P5biPvyX2xVeMcCLm82tO0XFQhmdMFwgAhPaUkCHoVL1F5kEAjIa	1	2017-08-15 08:52:55.981318	2017-08-15 08:49:42.458554	2017-08-15 08:49:42.458631		\N
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
-- Name: statements_merged statements_merged_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY statements_merged
    ADD CONSTRAINT statements_merged_pkey PRIMARY KEY (uid);


--
-- Name: statements statements_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY statements
    ADD CONSTRAINT statements_pkey PRIMARY KEY (uid);


--
-- Name: statements_splitted statements_splitted_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY statements_splitted
    ADD CONSTRAINT statements_splitted_pkey PRIMARY KEY (uid);


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
-- Name: statements_merged statements_merged_new_statement_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY statements_merged
    ADD CONSTRAINT statements_merged_new_statement_uid_fkey FOREIGN KEY (new_statement_uid) REFERENCES statements(uid);


--
-- Name: statements_merged statements_merged_review_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY statements_merged
    ADD CONSTRAINT statements_merged_review_uid_fkey FOREIGN KEY (review_uid) REFERENCES review_merge(uid);


--
-- Name: statements_merged statements_merged_statement_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY statements_merged
    ADD CONSTRAINT statements_merged_statement_uid_fkey FOREIGN KEY (statement_uid) REFERENCES statements(uid);


--
-- Name: statements_splitted statements_splitted_new_statement_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY statements_splitted
    ADD CONSTRAINT statements_splitted_new_statement_uid_fkey FOREIGN KEY (new_statement_uid) REFERENCES statements(uid);


--
-- Name: statements_splitted statements_splitted_review_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY statements_splitted
    ADD CONSTRAINT statements_splitted_review_uid_fkey FOREIGN KEY (review_uid) REFERENCES review_split(uid);


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
-- Name: statements_merged; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE statements_merged TO read_only_discussion;


--
-- Name: statements_splitted; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE statements_splitted TO read_only_discussion;


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

