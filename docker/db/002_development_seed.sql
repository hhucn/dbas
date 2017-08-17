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
-- Name: premisegroup_merged; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE premisegroup_merged (
    uid integer NOT NULL,
    review_uid integer,
    premisegroup_uid integer,
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
    premisegroup_uid integer,
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
1	1	2	\N	f	1	2017-08-17 08:18:20.389286	2	t
2	2	2	\N	t	1	2017-08-17 08:18:20.389437	2	f
3	3	2	\N	f	1	2017-08-17 08:18:20.389556	2	f
4	4	3	\N	t	1	2017-08-17 08:18:20.389668	2	f
5	5	3	\N	f	1	2017-08-17 08:18:20.389778	2	f
8	8	4	\N	t	1	2017-08-17 08:18:20.390158	2	f
10	10	11	\N	f	1	2017-08-17 08:18:20.390399	2	f
11	11	2	\N	t	1	2017-08-17 08:18:20.390507	2	f
12	12	2	\N	t	1	2017-08-17 08:18:20.390622	2	f
15	15	5	\N	t	1	2017-08-17 08:18:20.39095	2	f
16	16	5	\N	f	1	2017-08-17 08:18:20.391057	2	f
17	17	5	\N	t	1	2017-08-17 08:18:20.39117	2	f
19	19	6	\N	t	1	2017-08-17 08:18:20.391389	2	f
20	20	6	\N	f	1	2017-08-17 08:18:20.391495	2	f
21	21	6	\N	f	1	2017-08-17 08:18:20.391601	2	f
23	23	14	\N	f	1	2017-08-17 08:18:20.391888	2	f
24	24	14	\N	t	1	2017-08-17 08:18:20.391997	2	f
26	26	14	\N	t	1	2017-08-17 08:18:20.39221	2	f
27	27	15	\N	t	1	2017-08-17 08:18:20.392317	2	f
28	27	16	\N	t	1	2017-08-17 08:18:20.392428	2	f
29	28	15	\N	t	1	2017-08-17 08:18:20.392534	2	f
30	29	15	\N	f	1	2017-08-17 08:18:20.39264	2	f
32	31	36	\N	t	3	2017-08-17 08:18:20.39286	1	f
34	33	39	\N	t	3	2017-08-17 08:18:20.39307	1	f
35	34	41	\N	t	1	2017-08-17 08:18:20.393176	1	f
36	35	36	\N	f	1	2017-08-17 08:18:20.393282	1	f
39	38	37	\N	t	1	2017-08-17 08:18:20.393608	1	f
40	39	37	\N	t	1	2017-08-17 08:18:20.393714	1	f
41	41	46	\N	f	1	2017-08-17 08:18:20.393821	1	f
42	42	37	\N	f	1	2017-08-17 08:18:20.394031	1	f
44	44	50	\N	f	1	2017-08-17 08:18:20.394206	1	f
46	45	50	\N	t	1	2017-08-17 08:18:20.394294	1	f
47	46	38	\N	t	1	2017-08-17 08:18:20.394382	1	f
49	48	38	\N	f	1	2017-08-17 08:18:20.394564	1	f
50	49	49	\N	f	1	2017-08-17 08:18:20.39465	1	f
51	51	58	\N	f	1	2017-08-17 08:18:20.394814	4	f
54	54	59	\N	t	1	2017-08-17 08:18:20.395052	4	f
55	55	59	\N	f	1	2017-08-17 08:18:20.395132	4	f
56	56	60	\N	t	1	2017-08-17 08:18:20.395219	4	f
57	57	60	\N	f	1	2017-08-17 08:18:20.395302	4	f
58	50	58	\N	t	1	2017-08-17 08:18:20.394732	4	f
59	61	67	\N	t	1	2017-08-17 08:18:20.395382	4	f
60	62	69	\N	t	1	2017-08-17 08:18:20.395462	5	f
61	63	69	\N	t	1	2017-08-17 08:18:20.395547	5	f
62	64	69	\N	f	1	2017-08-17 08:18:20.395652	5	f
63	65	70	\N	f	1	2017-08-17 08:18:20.395742	5	f
64	66	70	\N	f	1	2017-08-17 08:18:20.395823	5	f
65	67	76	\N	t	1	2017-08-17 08:18:20.395905	7	f
66	68	76	\N	f	1	2017-08-17 08:18:20.395986	7	f
67	69	76	\N	f	1	2017-08-17 08:18:20.396071	7	f
68	70	79	\N	f	1	2017-08-17 08:18:20.396155	7	f
6	6	\N	4	f	1	2017-08-17 08:18:20.389906	2	f
7	7	\N	5	f	1	2017-08-17 08:18:20.390018	2	f
9	9	\N	8	f	1	2017-08-17 08:18:20.390288	2	f
13	13	\N	12	f	1	2017-08-17 08:18:20.390731	2	f
14	14	\N	13	f	1	2017-08-17 08:18:20.390843	2	f
18	18	\N	2	f	1	2017-08-17 08:18:20.39128	2	f
22	22	\N	3	f	1	2017-08-17 08:18:20.391775	2	f
25	25	\N	11	f	1	2017-08-17 08:18:20.392104	2	f
31	30	\N	15	f	1	2017-08-17 08:18:20.39275	2	f
33	32	\N	32	f	3	2017-08-17 08:18:20.392965	1	f
37	36	\N	36	f	1	2017-08-17 08:18:20.393391	1	f
38	37	\N	36	f	1	2017-08-17 08:18:20.393497	1	f
43	43	\N	42	f	1	2017-08-17 08:18:20.394118	1	f
45	40	\N	39	f	1	2017-08-17 08:18:20.393942	1	f
48	47	\N	47	f	1	2017-08-17 08:18:20.39447	1	f
52	52	\N	58	f	1	2017-08-17 08:18:20.394895	4	f
53	53	\N	51	f	1	2017-08-17 08:18:20.394973	4	f
69	71	\N	65	f	1	2017-08-17 08:18:20.396235	7	f
\.


--
-- Name: arguments_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('arguments_uid_seq', 69, true);


--
-- Data for Name: clicked_arguments; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY clicked_arguments (uid, argument_uid, author_uid, "timestamp", is_up_vote, is_valid) FROM stdin;
1076	1	13	2017-07-23 08:18:28.025361	t	t
1077	1	18	2017-08-09 08:18:28.025465	t	t
1078	1	19	2017-08-11 08:18:28.025503	t	t
1079	1	22	2017-07-26 08:18:28.025536	t	t
1080	1	16	2017-07-31 08:18:28.025567	t	t
1081	1	25	2017-08-03 08:18:28.025599	t	t
1082	1	34	2017-07-27 08:18:28.025631	t	t
1083	1	26	2017-07-31 08:18:28.025661	t	t
1084	1	23	2017-07-25 08:18:28.025691	t	t
1085	1	33	2017-07-31 08:18:28.02572	t	t
1086	1	10	2017-08-08 08:18:28.02575	t	t
1087	1	29	2017-07-25 08:18:28.025779	t	t
1088	1	28	2017-08-08 08:18:28.025808	t	t
1089	1	12	2017-08-09 08:18:28.025838	t	t
1090	1	20	2017-07-31 08:18:28.025885	t	t
1091	1	9	2017-07-23 08:18:28.025916	t	t
1092	1	29	2017-08-05 08:18:28.025946	t	t
1093	1	32	2017-08-12 08:18:28.025977	t	t
1094	1	17	2017-07-25 08:18:28.026007	t	t
1095	1	31	2017-08-05 08:18:28.026036	t	t
1096	1	8	2017-08-08 08:18:28.026066	t	t
1097	1	21	2017-08-14 08:18:28.026095	t	t
1098	1	35	2017-07-30 08:18:28.026125	t	t
1099	1	15	2017-07-24 08:18:28.026155	t	t
1100	1	37	2017-08-12 08:18:28.026185	t	t
1101	1	10	2017-08-13 08:18:28.026214	f	t
1102	1	29	2017-08-05 08:18:28.026244	f	t
1103	1	29	2017-08-07 08:18:28.026274	f	t
1104	1	26	2017-08-12 08:18:28.026303	f	t
1105	1	33	2017-08-10 08:18:28.026332	f	t
1106	1	23	2017-08-13 08:18:28.026362	f	t
1107	1	37	2017-08-16 08:18:28.026392	f	t
1108	1	11	2017-07-29 08:18:28.026421	f	t
1109	1	15	2017-08-01 08:18:28.026461	f	t
1110	1	36	2017-07-26 08:18:28.02649	f	t
1111	1	25	2017-08-08 08:18:28.026521	f	t
1112	1	22	2017-08-02 08:18:28.026551	f	t
1113	1	20	2017-08-08 08:18:28.026583	f	t
1114	1	17	2017-08-17 08:18:28.026614	f	t
1115	1	9	2017-07-30 08:18:28.026644	f	t
1116	1	13	2017-07-27 08:18:28.026675	f	t
1117	1	18	2017-08-12 08:18:28.026706	f	t
1118	1	8	2017-08-08 08:18:28.026736	f	t
1119	2	26	2017-08-11 08:18:28.026767	t	t
1120	2	13	2017-07-27 08:18:28.026798	t	t
1121	2	28	2017-08-05 08:18:28.026828	t	t
1122	2	35	2017-07-28 08:18:28.026858	t	t
1123	2	26	2017-08-09 08:18:28.026889	f	t
1124	2	24	2017-08-09 08:18:28.026919	f	t
1125	2	14	2017-07-23 08:18:28.02695	f	t
1126	2	35	2017-07-27 08:18:28.02698	f	t
1127	2	22	2017-08-01 08:18:28.02701	f	t
1128	2	29	2017-08-01 08:18:28.027041	f	t
1129	2	34	2017-08-10 08:18:28.027071	f	t
1130	2	17	2017-07-27 08:18:28.027101	f	t
1131	2	29	2017-08-09 08:18:28.027132	f	t
1132	2	25	2017-08-11 08:18:28.027162	f	t
1133	3	19	2017-08-07 08:18:28.027192	t	t
1134	3	9	2017-08-05 08:18:28.027222	t	t
1135	3	32	2017-07-24 08:18:28.027253	t	t
1136	3	26	2017-07-25 08:18:28.027284	t	t
1137	3	28	2017-07-26 08:18:28.027315	t	t
1138	3	16	2017-08-01 08:18:28.027345	t	t
1139	4	18	2017-07-29 08:18:28.027377	t	t
1140	4	21	2017-08-11 08:18:28.027408	f	t
1141	4	24	2017-07-23 08:18:28.027446	f	t
1142	4	12	2017-08-02 08:18:28.027475	f	t
1143	5	37	2017-08-17 08:18:28.027505	t	t
1144	5	21	2017-08-06 08:18:28.027534	f	t
1145	5	12	2017-08-06 08:18:28.027563	f	t
1146	5	28	2017-08-09 08:18:28.027593	f	t
1147	5	29	2017-07-24 08:18:28.027622	f	t
1148	5	17	2017-07-26 08:18:28.027652	f	t
1149	5	34	2017-07-31 08:18:28.027681	f	t
1150	5	25	2017-07-28 08:18:28.027711	f	t
1151	5	16	2017-07-24 08:18:28.02774	f	t
1152	8	32	2017-08-07 08:18:28.027769	t	t
1153	8	14	2017-08-08 08:18:28.027799	t	t
1154	8	9	2017-07-31 08:18:28.027829	t	t
1155	8	11	2017-08-02 08:18:28.027858	t	t
1156	8	17	2017-08-01 08:18:28.027888	t	t
1157	8	29	2017-08-03 08:18:28.027918	t	t
1158	8	34	2017-08-10 08:18:28.027947	t	t
1159	8	13	2017-08-12 08:18:28.027976	t	t
1160	8	26	2017-08-07 08:18:28.028006	t	t
1161	10	24	2017-08-06 08:18:28.028036	t	t
1162	10	26	2017-07-23 08:18:28.028065	t	t
1163	10	13	2017-08-11 08:18:28.028094	t	t
1164	10	33	2017-08-08 08:18:28.028123	t	t
1165	10	36	2017-08-01 08:18:28.028153	t	t
1166	10	10	2017-07-26 08:18:28.028183	t	t
1167	10	29	2017-08-07 08:18:28.028212	f	t
1168	10	17	2017-07-25 08:18:28.028241	f	t
1169	10	12	2017-07-31 08:18:28.02827	f	t
1170	10	15	2017-08-06 08:18:28.028299	f	t
1171	10	7	2017-08-11 08:18:28.028328	f	t
1172	10	25	2017-08-14 08:18:28.028357	f	t
1173	11	14	2017-07-29 08:18:28.028387	t	t
1174	11	13	2017-08-01 08:18:28.028416	t	t
1175	11	28	2017-08-12 08:18:28.028458	t	t
1176	11	20	2017-07-24 08:18:28.028498	t	t
1177	11	32	2017-07-24 08:18:28.028538	t	t
1178	11	8	2017-07-25 08:18:28.028578	t	t
1179	11	16	2017-08-11 08:18:28.028618	t	t
1180	11	22	2017-08-03 08:18:28.028658	t	t
1181	11	31	2017-08-03 08:18:28.028697	t	t
1182	11	33	2017-07-31 08:18:28.028736	t	t
1183	11	23	2017-08-14 08:18:28.028775	t	t
1184	11	15	2017-08-14 08:18:28.028816	t	t
1185	11	12	2017-08-07 08:18:28.028855	t	t
1186	11	35	2017-08-12 08:18:28.028894	t	t
1187	11	26	2017-08-11 08:18:28.028934	t	t
1188	11	37	2017-08-06 08:18:28.028973	t	t
1189	11	10	2017-08-04 08:18:28.029012	t	t
1190	11	13	2017-08-06 08:18:28.029051	f	t
1191	11	24	2017-08-16 08:18:28.029091	f	t
1192	11	16	2017-07-27 08:18:28.029131	f	t
1193	11	26	2017-07-26 08:18:28.029171	f	t
1194	11	20	2017-08-01 08:18:28.029213	f	t
1195	11	7	2017-07-25 08:18:28.029252	f	t
1196	11	32	2017-08-15 08:18:28.029292	f	t
1197	11	19	2017-07-31 08:18:28.029333	f	t
1198	11	29	2017-08-05 08:18:28.029373	f	t
1199	11	9	2017-08-16 08:18:28.029412	f	t
1200	11	8	2017-08-06 08:18:28.029452	f	t
1201	11	22	2017-08-14 08:18:28.029493	f	t
1202	11	25	2017-08-12 08:18:28.029525	f	t
1203	11	34	2017-07-28 08:18:28.029555	f	t
1204	11	28	2017-07-24 08:18:28.029586	f	t
1205	11	15	2017-07-23 08:18:28.029617	f	t
1206	11	37	2017-07-25 08:18:28.029647	f	t
1207	11	14	2017-08-07 08:18:28.029678	f	t
1208	12	13	2017-08-14 08:18:28.029709	t	t
1209	12	26	2017-08-04 08:18:28.029739	t	t
1210	12	9	2017-08-12 08:18:28.02977	t	t
1211	12	32	2017-07-27 08:18:28.029801	f	t
1212	12	24	2017-08-03 08:18:28.029831	f	t
1213	12	27	2017-07-30 08:18:28.029867	f	t
1214	12	37	2017-08-10 08:18:28.029899	f	t
1215	12	9	2017-08-01 08:18:28.02993	f	t
1216	12	10	2017-08-12 08:18:28.02996	f	t
1217	12	23	2017-07-31 08:18:28.029991	f	t
1218	12	31	2017-08-10 08:18:28.030022	f	t
1219	12	22	2017-08-07 08:18:28.030053	f	t
1220	12	33	2017-07-25 08:18:28.030084	f	t
1221	12	25	2017-08-08 08:18:28.030114	f	t
1222	12	18	2017-08-05 08:18:28.030145	f	t
1223	12	14	2017-08-06 08:18:28.030175	f	t
1224	12	15	2017-08-17 08:18:28.030206	f	t
1225	12	28	2017-07-26 08:18:28.030236	f	t
1226	12	26	2017-08-09 08:18:28.030276	f	t
1227	15	20	2017-08-05 08:18:28.030305	t	t
1228	15	18	2017-08-05 08:18:28.030336	t	t
1229	15	36	2017-08-03 08:18:28.030365	t	t
1230	15	28	2017-08-10 08:18:28.030406	t	t
1231	15	26	2017-08-07 08:18:28.030446	t	t
1232	15	7	2017-08-03 08:18:28.030475	t	t
1233	15	9	2017-08-14 08:18:28.030504	t	t
1234	15	35	2017-08-15 08:18:28.030534	t	t
1235	15	27	2017-07-26 08:18:28.030564	t	t
1236	15	33	2017-07-27 08:18:28.030593	t	t
1237	15	24	2017-08-04 08:18:28.030623	t	t
1238	15	15	2017-08-12 08:18:28.030652	t	t
1239	15	29	2017-08-14 08:18:28.030682	t	t
1240	15	37	2017-08-09 08:18:28.030711	t	t
1241	15	11	2017-08-09 08:18:28.03074	t	t
1242	15	14	2017-07-30 08:18:28.030769	t	t
1243	15	25	2017-08-08 08:18:28.030798	t	t
1244	15	32	2017-08-13 08:18:28.030837	t	t
1245	15	29	2017-07-23 08:18:28.030874	t	t
1246	15	10	2017-07-27 08:18:28.030905	t	t
1247	15	21	2017-08-14 08:18:28.030935	f	t
1248	15	15	2017-08-12 08:18:28.030964	f	t
1249	15	8	2017-07-25 08:18:28.030994	f	t
1250	15	17	2017-07-27 08:18:28.031024	f	t
1251	15	35	2017-08-16 08:18:28.031054	f	t
1252	15	7	2017-08-04 08:18:28.031084	f	t
1253	15	9	2017-08-07 08:18:28.031114	f	t
1254	15	27	2017-07-29 08:18:28.031143	f	t
1255	15	29	2017-08-12 08:18:28.031172	f	t
1256	15	19	2017-08-15 08:18:28.031201	f	t
1257	15	32	2017-07-30 08:18:28.03123	f	t
1258	15	18	2017-07-29 08:18:28.031259	f	t
1259	15	24	2017-08-02 08:18:28.031289	f	t
1260	15	22	2017-08-09 08:18:28.031318	f	t
1261	15	26	2017-08-17 08:18:28.031348	f	t
1262	15	14	2017-08-12 08:18:28.031376	f	t
1263	15	37	2017-07-28 08:18:28.031406	f	t
1264	15	10	2017-08-15 08:18:28.031435	f	t
1265	15	20	2017-08-01 08:18:28.031464	f	t
1266	15	25	2017-08-08 08:18:28.031493	f	t
1267	15	11	2017-08-16 08:18:28.031523	f	t
1268	15	16	2017-08-08 08:18:28.031553	f	t
1269	16	12	2017-08-01 08:18:28.031582	t	t
1270	16	24	2017-07-28 08:18:28.031612	t	t
1271	16	19	2017-08-11 08:18:28.031641	t	t
1272	16	9	2017-08-16 08:18:28.03168	t	t
1273	16	20	2017-08-05 08:18:28.03171	t	t
1274	16	27	2017-08-13 08:18:28.03174	t	t
1275	16	15	2017-08-12 08:18:28.031771	t	t
1276	16	22	2017-07-24 08:18:28.031805	t	t
1277	16	32	2017-08-01 08:18:28.031861	f	t
1278	16	28	2017-07-24 08:18:28.031893	f	t
1279	16	22	2017-07-30 08:18:28.031923	f	t
1280	16	23	2017-07-28 08:18:28.031953	f	t
1281	17	34	2017-08-02 08:18:28.031983	t	t
1282	17	7	2017-08-09 08:18:28.032012	t	t
1283	17	23	2017-08-14 08:18:28.032041	t	t
1284	17	25	2017-08-16 08:18:28.03207	t	t
1285	17	11	2017-07-29 08:18:28.032099	t	t
1286	17	24	2017-07-24 08:18:28.032128	f	t
1287	19	33	2017-08-08 08:18:28.032157	t	t
1288	19	32	2017-08-16 08:18:28.032187	t	t
1289	19	27	2017-08-03 08:18:28.032216	t	t
1290	19	11	2017-08-14 08:18:28.032246	t	t
1291	19	15	2017-07-27 08:18:28.032275	t	t
1292	19	22	2017-08-12 08:18:28.032304	t	t
1293	19	36	2017-07-24 08:18:28.032333	t	t
1294	19	10	2017-07-30 08:18:28.032363	t	t
1295	19	8	2017-08-04 08:18:28.032392	t	t
1296	19	7	2017-07-27 08:18:28.032421	t	t
1297	19	14	2017-08-04 08:18:28.032451	t	t
1298	19	17	2017-07-28 08:18:28.03249	t	t
1299	19	24	2017-08-05 08:18:28.03253	t	t
1300	19	28	2017-07-25 08:18:28.032559	f	t
1301	19	17	2017-07-29 08:18:28.032588	f	t
1302	19	11	2017-07-28 08:18:28.032618	f	t
1303	19	33	2017-08-09 08:18:28.032647	f	t
1304	19	14	2017-08-17 08:18:28.032676	f	t
1305	19	35	2017-08-02 08:18:28.032705	f	t
1306	20	32	2017-07-31 08:18:28.032734	t	t
1307	20	12	2017-07-28 08:18:28.032763	t	t
1308	20	10	2017-08-02 08:18:28.032791	f	t
1309	21	18	2017-07-26 08:18:28.03282	f	t
1310	21	29	2017-08-13 08:18:28.032849	f	t
1311	23	33	2017-08-07 08:18:28.032878	t	t
1312	23	32	2017-07-23 08:18:28.032907	t	t
1313	23	12	2017-08-02 08:18:28.032936	f	t
1314	23	19	2017-07-30 08:18:28.032965	f	t
1315	23	11	2017-07-26 08:18:28.032994	f	t
1316	24	18	2017-07-26 08:18:28.033023	t	t
1317	24	29	2017-07-31 08:18:28.033052	t	t
1318	24	28	2017-08-12 08:18:28.03308	t	t
1319	24	11	2017-07-27 08:18:28.03311	t	t
1320	24	23	2017-07-30 08:18:28.033139	t	t
1321	24	33	2017-08-14 08:18:28.033168	t	t
1322	24	25	2017-08-01 08:18:28.033197	f	t
1323	24	22	2017-08-09 08:18:28.033227	f	t
1324	24	12	2017-08-09 08:18:28.033256	f	t
1325	24	36	2017-08-15 08:18:28.033285	f	t
1326	24	14	2017-08-02 08:18:28.033314	f	t
1327	24	31	2017-07-27 08:18:28.033344	f	t
1328	26	32	2017-08-06 08:18:28.033373	t	t
1329	26	21	2017-07-27 08:18:28.033413	t	t
1330	26	8	2017-07-29 08:18:28.033453	t	t
1331	26	28	2017-07-29 08:18:28.033482	t	t
1332	26	7	2017-07-31 08:18:28.033511	t	t
1333	26	35	2017-08-15 08:18:28.033565	t	t
1334	26	26	2017-08-13 08:18:28.033596	t	t
1335	26	34	2017-08-11 08:18:28.033626	f	t
1336	26	13	2017-07-28 08:18:28.033656	f	t
1337	26	23	2017-07-29 08:18:28.033685	f	t
1338	26	24	2017-08-12 08:18:28.033715	f	t
1339	26	11	2017-07-25 08:18:28.033745	f	t
1340	26	35	2017-08-07 08:18:28.033774	f	t
1341	26	32	2017-08-14 08:18:28.033803	f	t
1342	26	33	2017-08-11 08:18:28.033833	f	t
1343	27	31	2017-07-24 08:18:28.033869	t	t
1344	27	26	2017-08-14 08:18:28.0339	t	t
1345	27	11	2017-08-09 08:18:28.033929	t	t
1346	27	18	2017-08-12 08:18:28.033959	t	t
1347	27	24	2017-07-28 08:18:28.033988	t	t
1348	27	31	2017-08-15 08:18:28.034018	f	t
1349	27	34	2017-08-08 08:18:28.034048	f	t
1350	27	29	2017-08-07 08:18:28.034077	f	t
1351	27	25	2017-08-04 08:18:28.034106	f	t
1352	27	10	2017-08-13 08:18:28.034135	f	t
1353	28	9	2017-07-29 08:18:28.034164	t	t
1354	28	37	2017-07-30 08:18:28.034193	t	t
1355	28	36	2017-07-31 08:18:28.034222	t	t
1356	28	14	2017-08-01 08:18:28.034251	t	t
1357	28	11	2017-07-25 08:18:28.03428	t	t
1358	28	35	2017-08-03 08:18:28.034309	t	t
1359	28	29	2017-08-08 08:18:28.034338	t	t
1360	28	32	2017-08-12 08:18:28.034368	t	t
1361	28	19	2017-08-11 08:18:28.034397	t	t
1362	28	7	2017-08-06 08:18:28.034427	t	t
1363	28	15	2017-08-05 08:18:28.034456	t	t
1364	28	21	2017-08-08 08:18:28.034485	t	t
1365	28	8	2017-08-06 08:18:28.034514	t	t
1366	28	20	2017-08-14 08:18:28.034542	t	t
1367	28	25	2017-08-07 08:18:28.034583	t	t
1368	28	34	2017-07-23 08:18:28.034612	t	t
1369	28	15	2017-08-12 08:18:28.034642	f	t
1370	28	8	2017-07-28 08:18:28.034672	f	t
1371	28	35	2017-07-29 08:18:28.034702	f	t
1372	28	16	2017-08-04 08:18:28.034733	f	t
1373	28	26	2017-08-11 08:18:28.034772	f	t
1374	28	32	2017-07-28 08:18:28.034801	f	t
1375	28	19	2017-08-06 08:18:28.034831	f	t
1376	28	34	2017-07-26 08:18:28.03486	f	t
1377	28	29	2017-08-07 08:18:28.034889	f	t
1378	28	18	2017-08-13 08:18:28.034918	f	t
1379	28	14	2017-08-07 08:18:28.034948	f	t
1380	28	29	2017-08-12 08:18:28.034977	f	t
1381	28	24	2017-07-28 08:18:28.035007	f	t
1382	28	37	2017-08-05 08:18:28.035036	f	t
1383	28	31	2017-08-10 08:18:28.035065	f	t
1384	28	13	2017-07-27 08:18:28.035094	f	t
1385	28	17	2017-08-05 08:18:28.035124	f	t
1386	28	9	2017-07-25 08:18:28.035153	f	t
1387	28	10	2017-07-28 08:18:28.035182	f	t
1388	28	22	2017-08-04 08:18:28.035211	f	t
1389	29	37	2017-08-03 08:18:28.03524	t	t
1390	29	21	2017-08-12 08:18:28.035269	t	t
1391	29	18	2017-08-08 08:18:28.035298	t	t
1392	29	22	2017-07-24 08:18:28.035327	t	t
1393	29	36	2017-07-29 08:18:28.035356	t	t
1394	29	33	2017-07-31 08:18:28.035386	t	t
1395	29	13	2017-08-06 08:18:28.035415	t	t
1396	29	14	2017-08-13 08:18:28.035444	t	t
1397	29	27	2017-08-05 08:18:28.035482	t	t
1398	29	17	2017-08-09 08:18:28.035512	t	t
1399	29	9	2017-08-11 08:18:28.035542	t	t
1400	29	35	2017-08-02 08:18:28.035572	t	t
1401	29	28	2017-07-26 08:18:28.035602	t	t
1402	29	26	2017-08-13 08:18:28.035633	t	t
1403	29	11	2017-07-31 08:18:28.035664	t	t
1404	29	24	2017-07-28 08:18:28.035694	t	t
1405	29	20	2017-07-28 08:18:28.035725	t	t
1406	29	12	2017-08-02 08:18:28.035755	t	t
1407	29	18	2017-07-24 08:18:28.035785	f	t
1408	30	31	2017-07-28 08:18:28.035815	t	t
1409	30	28	2017-08-07 08:18:28.035845	t	t
1410	30	15	2017-08-10 08:18:28.035875	t	t
1411	30	27	2017-07-31 08:18:28.035905	t	t
1412	30	13	2017-07-27 08:18:28.035934	t	t
1413	30	10	2017-08-02 08:18:28.035965	t	t
1414	30	16	2017-08-16 08:18:28.035994	t	t
1415	30	37	2017-07-25 08:18:28.036024	t	t
1416	30	11	2017-08-12 08:18:28.036054	f	t
1417	30	29	2017-07-31 08:18:28.036084	f	t
1418	30	12	2017-07-24 08:18:28.036114	f	t
1419	34	31	2017-08-17 08:18:28.036144	t	t
1420	34	8	2017-07-28 08:18:28.036174	t	t
1421	34	36	2017-08-15 08:18:28.036204	t	t
1422	34	12	2017-08-05 08:18:28.036234	t	t
1423	34	27	2017-08-04 08:18:28.036264	t	t
1424	34	37	2017-08-11 08:18:28.036294	t	t
1425	34	28	2017-07-29 08:18:28.036324	t	t
1426	34	9	2017-08-11 08:18:28.036355	t	t
1427	34	20	2017-08-16 08:18:28.036385	t	t
1428	34	14	2017-07-28 08:18:28.036416	t	t
1429	34	15	2017-08-15 08:18:28.036446	t	t
1430	35	31	2017-07-23 08:18:28.036484	t	t
1431	35	25	2017-07-31 08:18:28.036514	t	t
1432	35	28	2017-08-02 08:18:28.036553	t	t
1433	35	11	2017-07-27 08:18:28.036593	t	t
1434	35	20	2017-07-24 08:18:28.036621	t	t
1435	35	27	2017-07-25 08:18:28.03665	f	t
1436	35	37	2017-08-08 08:18:28.036679	f	t
1437	35	8	2017-08-04 08:18:28.036708	f	t
1438	36	31	2017-08-16 08:18:28.036738	t	t
1439	36	7	2017-07-23 08:18:28.036767	t	t
1440	36	12	2017-07-30 08:18:28.036796	t	t
1441	36	24	2017-08-17 08:18:28.036826	t	t
1442	36	19	2017-07-27 08:18:28.036855	t	t
1443	36	33	2017-07-28 08:18:28.036884	f	t
1444	36	17	2017-08-11 08:18:28.036913	f	t
1445	36	20	2017-08-07 08:18:28.036943	f	t
1446	36	13	2017-07-23 08:18:28.036972	f	t
1447	36	32	2017-08-06 08:18:28.037002	f	t
1448	36	19	2017-08-04 08:18:28.037031	f	t
1449	36	24	2017-08-17 08:18:28.037061	f	t
1450	36	18	2017-08-10 08:18:28.03709	f	t
1451	36	11	2017-07-25 08:18:28.037119	f	t
1452	36	25	2017-07-31 08:18:28.037148	f	t
1453	36	26	2017-08-08 08:18:28.037177	f	t
1454	36	21	2017-08-10 08:18:28.037206	f	t
1455	36	29	2017-07-24 08:18:28.037235	f	t
1456	39	18	2017-07-29 08:18:28.037264	t	t
1457	39	8	2017-08-06 08:18:28.037294	t	t
1458	39	25	2017-08-11 08:18:28.037323	t	t
1459	39	32	2017-08-13 08:18:28.037368	t	t
1460	39	33	2017-07-28 08:18:28.037421	t	t
1461	39	15	2017-08-13 08:18:28.037468	f	t
1462	40	15	2017-08-04 08:18:28.0375	t	t
1463	40	24	2017-07-29 08:18:28.03753	t	t
1464	40	19	2017-08-05 08:18:28.03756	t	t
1465	40	17	2017-07-29 08:18:28.037589	t	t
1466	40	18	2017-07-23 08:18:28.037619	t	t
1467	40	7	2017-08-12 08:18:28.037648	t	t
1468	40	33	2017-08-13 08:18:28.037678	f	t
1469	40	32	2017-07-31 08:18:28.037707	f	t
1470	40	12	2017-08-15 08:18:28.037737	f	t
1471	41	33	2017-08-14 08:18:28.037767	t	t
1472	41	10	2017-08-12 08:18:28.037796	t	t
1473	41	13	2017-07-30 08:18:28.037825	t	t
1474	41	11	2017-08-11 08:18:28.037861	t	t
1475	41	29	2017-08-12 08:18:28.037892	f	t
1476	41	15	2017-08-10 08:18:28.037921	f	t
1477	41	34	2017-08-17 08:18:28.037951	f	t
1478	41	27	2017-07-25 08:18:28.03798	f	t
1479	41	23	2017-08-08 08:18:28.038009	f	t
1480	41	24	2017-08-01 08:18:28.038038	f	t
1481	41	36	2017-07-27 08:18:28.038067	f	t
1482	41	37	2017-07-31 08:18:28.038097	f	t
1483	42	21	2017-07-29 08:18:28.038125	t	t
1484	42	31	2017-08-16 08:18:28.038154	t	t
1485	42	23	2017-08-08 08:18:28.038184	f	t
1486	42	27	2017-08-02 08:18:28.038213	f	t
1487	42	37	2017-08-15 08:18:28.038242	f	t
1488	42	10	2017-08-11 08:18:28.038271	f	t
1489	42	19	2017-08-11 08:18:28.0383	f	t
1490	42	26	2017-08-03 08:18:28.038329	f	t
1491	44	23	2017-08-10 08:18:28.038358	f	t
1492	44	11	2017-07-29 08:18:28.038388	f	t
1493	44	8	2017-08-01 08:18:28.038417	f	t
1494	44	21	2017-08-07 08:18:28.038446	f	t
1495	44	13	2017-08-07 08:18:28.038475	f	t
1496	44	22	2017-07-23 08:18:28.038504	f	t
1497	46	27	2017-08-09 08:18:28.038532	t	t
1498	47	9	2017-07-30 08:18:28.038562	t	t
1499	47	10	2017-08-12 08:18:28.038591	t	t
1500	47	29	2017-07-27 08:18:28.03862	f	t
1501	47	33	2017-08-11 08:18:28.038648	f	t
1502	47	10	2017-08-05 08:18:28.038678	f	t
1503	47	13	2017-08-01 08:18:28.038706	f	t
1504	47	34	2017-08-10 08:18:28.038736	f	t
1505	47	15	2017-08-10 08:18:28.038765	f	t
1506	47	22	2017-08-10 08:18:28.038794	f	t
1507	47	32	2017-07-27 08:18:28.038823	f	t
1508	47	35	2017-08-17 08:18:28.038851	f	t
1509	47	18	2017-07-26 08:18:28.03888	f	t
1510	47	24	2017-08-01 08:18:28.03891	f	t
1511	47	28	2017-07-29 08:18:28.03894	f	t
1512	49	7	2017-07-26 08:18:28.03897	t	t
1513	49	33	2017-08-11 08:18:28.039	t	t
1514	49	14	2017-08-16 08:18:28.039029	t	t
1515	49	35	2017-07-26 08:18:28.039059	t	t
1516	49	7	2017-08-07 08:18:28.039088	f	t
1517	49	34	2017-08-05 08:18:28.039117	f	t
1518	49	18	2017-07-30 08:18:28.039146	f	t
1519	49	14	2017-08-03 08:18:28.039176	f	t
1520	49	8	2017-07-29 08:18:28.039205	f	t
1521	49	27	2017-08-01 08:18:28.039235	f	t
1522	50	13	2017-08-16 08:18:28.039264	t	t
1523	50	7	2017-08-14 08:18:28.039293	t	t
1524	50	25	2017-08-11 08:18:28.039323	t	t
1525	50	18	2017-08-17 08:18:28.039352	t	t
1526	50	9	2017-08-03 08:18:28.039382	t	t
1527	50	11	2017-08-13 08:18:28.039411	t	t
1528	50	35	2017-07-25 08:18:28.03944	t	t
1529	50	33	2017-08-04 08:18:28.039469	t	t
1530	50	10	2017-07-28 08:18:28.039499	t	t
1531	50	34	2017-08-01 08:18:28.039529	t	t
1532	50	14	2017-07-23 08:18:28.039558	t	t
1533	50	19	2017-07-31 08:18:28.039586	t	t
1534	50	32	2017-08-02 08:18:28.039616	t	t
1535	50	31	2017-07-25 08:18:28.039645	f	t
1536	50	18	2017-08-17 08:18:28.039674	f	t
1537	50	8	2017-07-23 08:18:28.039704	f	t
1538	51	25	2017-08-04 08:18:28.039733	t	t
1539	51	11	2017-08-03 08:18:28.039763	t	t
1540	51	27	2017-08-15 08:18:28.039792	t	t
1541	51	16	2017-08-11 08:18:28.039822	t	t
1542	51	28	2017-08-02 08:18:28.039852	f	t
1543	54	29	2017-07-27 08:18:28.039882	t	t
1544	54	31	2017-08-14 08:18:28.039912	t	t
1545	54	18	2017-08-06 08:18:28.039941	t	t
1546	54	27	2017-07-26 08:18:28.03997	f	t
1547	54	37	2017-08-03 08:18:28.039999	f	t
1548	54	31	2017-08-07 08:18:28.040028	f	t
1549	55	16	2017-08-08 08:18:28.040057	t	t
1550	55	21	2017-08-11 08:18:28.040086	t	t
1551	55	8	2017-08-02 08:18:28.040115	t	t
1552	55	13	2017-08-08 08:18:28.040144	f	t
1553	55	21	2017-08-03 08:18:28.040174	f	t
1554	55	35	2017-08-02 08:18:28.040203	f	t
1555	55	17	2017-08-03 08:18:28.040232	f	t
1556	55	37	2017-08-14 08:18:28.040261	f	t
1557	55	22	2017-07-27 08:18:28.04029	f	t
1558	55	10	2017-07-26 08:18:28.04032	f	t
1559	55	16	2017-07-31 08:18:28.040349	f	t
1560	55	20	2017-07-31 08:18:28.040379	f	t
1561	55	15	2017-08-02 08:18:28.040408	f	t
1562	55	23	2017-07-26 08:18:28.040437	f	t
1563	55	27	2017-08-14 08:18:28.040466	f	t
1564	56	32	2017-08-10 08:18:28.040496	t	t
1565	56	36	2017-07-28 08:18:28.040526	t	t
1566	56	15	2017-08-06 08:18:28.040575	t	t
1567	56	17	2017-08-13 08:18:28.040606	t	t
1568	56	18	2017-08-16 08:18:28.040636	t	t
1569	56	19	2017-08-06 08:18:28.040666	f	t
1570	56	15	2017-08-04 08:18:28.040695	f	t
1571	56	7	2017-08-02 08:18:28.040724	f	t
1572	56	8	2017-07-30 08:18:28.040753	f	t
1573	56	29	2017-08-07 08:18:28.040782	f	t
1574	56	17	2017-08-13 08:18:28.040812	f	t
1575	57	35	2017-08-11 08:18:28.040841	t	t
1576	57	24	2017-08-15 08:18:28.04087	t	t
1577	57	28	2017-08-05 08:18:28.0409	f	t
1578	57	24	2017-08-17 08:18:28.040929	f	t
1579	57	34	2017-08-04 08:18:28.04096	f	t
1580	57	22	2017-07-23 08:18:28.040991	f	t
1581	57	35	2017-08-16 08:18:28.04102	f	t
1582	57	23	2017-07-27 08:18:28.04105	f	t
1583	57	16	2017-08-06 08:18:28.041079	f	t
1584	57	27	2017-07-26 08:18:28.041108	f	t
1585	57	15	2017-08-03 08:18:28.041138	f	t
1586	57	11	2017-07-25 08:18:28.041167	f	t
1587	57	7	2017-08-14 08:18:28.041197	f	t
1588	59	33	2017-08-09 08:18:28.041226	t	t
1589	59	13	2017-08-07 08:18:28.041256	t	t
1590	59	14	2017-07-26 08:18:28.041285	t	t
1591	59	25	2017-08-06 08:18:28.041314	t	t
1592	59	37	2017-07-24 08:18:28.041345	t	t
1593	59	34	2017-08-15 08:18:28.041374	t	t
1594	59	8	2017-07-30 08:18:28.041403	t	t
1595	59	10	2017-07-28 08:18:28.041432	f	t
1596	59	11	2017-07-23 08:18:28.041461	f	t
1597	59	8	2017-08-10 08:18:28.04149	f	t
1598	59	14	2017-08-11 08:18:28.041519	f	t
1599	59	7	2017-08-07 08:18:28.041548	f	t
1600	59	20	2017-08-01 08:18:28.041577	f	t
1601	59	13	2017-08-04 08:18:28.041606	f	t
1602	59	23	2017-07-25 08:18:28.041636	f	t
1603	59	9	2017-07-30 08:18:28.041665	f	t
1604	59	33	2017-07-30 08:18:28.041694	f	t
1605	59	21	2017-08-10 08:18:28.041724	f	t
1606	59	26	2017-08-12 08:18:28.041754	f	t
1607	60	29	2017-08-01 08:18:28.041784	t	t
1608	60	12	2017-08-12 08:18:28.041813	t	t
1609	60	36	2017-08-05 08:18:28.041842	t	t
1610	60	7	2017-07-27 08:18:28.041886	t	t
1611	60	20	2017-07-27 08:18:28.041915	t	t
1612	60	24	2017-08-14 08:18:28.041944	t	t
1613	60	34	2017-07-31 08:18:28.041972	t	t
1614	60	10	2017-07-30 08:18:28.042001	t	t
1615	60	18	2017-08-10 08:18:28.042029	t	t
1616	60	26	2017-07-23 08:18:28.042058	t	t
1617	60	11	2017-08-02 08:18:28.042087	t	t
1618	60	31	2017-08-08 08:18:28.042115	t	t
1619	60	23	2017-08-12 08:18:28.042143	t	t
1620	60	33	2017-08-11 08:18:28.042172	t	t
1621	60	27	2017-08-06 08:18:28.0422	t	t
1622	60	32	2017-08-17 08:18:28.042228	t	t
1623	60	8	2017-07-31 08:18:28.042257	t	t
1624	60	15	2017-08-03 08:18:28.042285	t	t
1625	60	13	2017-08-02 08:18:28.042313	t	t
1626	60	19	2017-08-12 08:18:28.042341	t	t
1627	60	9	2017-07-30 08:18:28.04237	t	t
1628	60	29	2017-08-03 08:18:28.042399	t	t
1629	60	16	2017-08-16 08:18:28.042428	t	t
1630	60	21	2017-07-24 08:18:28.042456	f	t
1631	61	19	2017-08-15 08:18:28.042494	t	t
1632	61	18	2017-08-03 08:18:28.042525	t	t
1633	61	16	2017-08-11 08:18:28.042556	t	t
1634	61	10	2017-07-29 08:18:28.042586	t	t
1635	61	10	2017-07-23 08:18:28.042616	f	t
1636	61	19	2017-07-23 08:18:28.042646	f	t
1637	61	7	2017-08-06 08:18:28.042675	f	t
1638	61	26	2017-08-06 08:18:28.042705	f	t
1639	61	16	2017-08-17 08:18:28.042735	f	t
1640	61	12	2017-08-07 08:18:28.042765	f	t
1641	61	9	2017-08-15 08:18:28.042795	f	t
1642	61	31	2017-07-29 08:18:28.042826	f	t
1643	61	27	2017-08-03 08:18:28.042857	f	t
1644	61	22	2017-08-14 08:18:28.042886	f	t
1645	61	15	2017-08-13 08:18:28.042916	f	t
1646	61	32	2017-07-30 08:18:28.042946	f	t
1647	62	25	2017-07-26 08:18:28.042976	t	t
1648	62	9	2017-08-14 08:18:28.043006	t	t
1649	62	20	2017-07-30 08:18:28.043037	t	t
1650	62	12	2017-08-08 08:18:28.043068	t	t
1651	62	24	2017-08-11 08:18:28.043099	t	t
1652	62	15	2017-07-31 08:18:28.043129	t	t
1653	62	13	2017-08-11 08:18:28.043159	t	t
1654	62	16	2017-07-25 08:18:28.043189	t	t
1655	62	21	2017-07-23 08:18:28.043218	f	t
1656	62	23	2017-08-04 08:18:28.043248	f	t
1657	62	25	2017-08-13 08:18:28.043278	f	t
1658	62	36	2017-07-28 08:18:28.043308	f	t
1659	62	28	2017-08-08 08:18:28.043339	f	t
1660	62	13	2017-08-11 08:18:28.043369	f	t
1661	62	33	2017-07-27 08:18:28.043398	f	t
1662	62	10	2017-07-26 08:18:28.043428	f	t
1663	62	14	2017-07-27 08:18:28.043457	f	t
1664	62	34	2017-08-14 08:18:28.043495	f	t
1665	62	35	2017-08-16 08:18:28.043523	f	t
1666	62	11	2017-08-02 08:18:28.043552	f	t
1667	62	9	2017-07-25 08:18:28.04358	f	t
1668	62	15	2017-07-30 08:18:28.043607	f	t
1669	62	20	2017-07-27 08:18:28.043635	f	t
1670	62	29	2017-08-04 08:18:28.043663	f	t
1671	62	18	2017-08-15 08:18:28.043691	f	t
1672	62	37	2017-08-07 08:18:28.043719	f	t
1673	62	32	2017-08-06 08:18:28.043749	f	t
1674	63	26	2017-07-31 08:18:28.043777	t	t
1675	63	17	2017-07-23 08:18:28.043806	t	t
1676	63	29	2017-07-26 08:18:28.043834	t	t
1677	63	11	2017-08-07 08:18:28.043861	f	t
1678	63	18	2017-08-04 08:18:28.04389	f	t
1679	63	28	2017-07-28 08:18:28.043918	f	t
1680	63	19	2017-07-27 08:18:28.043946	f	t
1681	64	15	2017-07-31 08:18:28.043975	f	t
1682	64	35	2017-08-14 08:18:28.044003	f	t
1683	64	23	2017-08-03 08:18:28.044031	f	t
1684	64	22	2017-08-14 08:18:28.04406	f	t
1685	64	11	2017-08-06 08:18:28.044089	f	t
1686	64	25	2017-07-31 08:18:28.044117	f	t
1687	64	14	2017-07-31 08:18:28.044145	f	t
1688	64	9	2017-08-09 08:18:28.044173	f	t
1689	65	14	2017-08-13 08:18:28.044201	t	t
1690	65	24	2017-08-01 08:18:28.044229	t	t
1691	65	29	2017-08-12 08:18:28.044256	t	t
1692	65	12	2017-08-04 08:18:28.044285	t	t
1693	65	7	2017-07-30 08:18:28.044313	t	t
1694	65	22	2017-08-09 08:18:28.044342	t	t
1695	65	27	2017-07-24 08:18:28.04437	t	t
1696	65	21	2017-07-27 08:18:28.044399	t	t
1697	65	16	2017-08-14 08:18:28.044427	t	t
1698	65	22	2017-07-31 08:18:28.044456	f	t
1699	65	24	2017-08-07 08:18:28.044484	f	t
1700	65	14	2017-07-24 08:18:28.044513	f	t
1701	65	21	2017-07-30 08:18:28.044541	f	t
1702	65	20	2017-07-25 08:18:28.044569	f	t
1703	65	25	2017-08-04 08:18:28.044597	f	t
1704	65	28	2017-08-13 08:18:28.044636	f	t
1705	65	31	2017-08-09 08:18:28.044675	f	t
1706	65	17	2017-07-25 08:18:28.044703	f	t
1707	65	13	2017-08-08 08:18:28.044732	f	t
1708	65	18	2017-08-06 08:18:28.04476	f	t
1709	65	9	2017-08-12 08:18:28.044788	f	t
1710	65	26	2017-07-24 08:18:28.044816	f	t
1711	65	32	2017-08-17 08:18:28.044844	f	t
1712	65	10	2017-07-29 08:18:28.044872	f	t
1713	66	22	2017-07-31 08:18:28.0449	t	t
1714	66	8	2017-08-11 08:18:28.044928	t	t
1715	66	17	2017-08-04 08:18:28.044956	t	t
1716	66	10	2017-07-31 08:18:28.044984	t	t
1717	66	34	2017-08-09 08:18:28.045012	t	t
1718	66	12	2017-07-24 08:18:28.04504	t	t
1719	66	26	2017-08-04 08:18:28.045068	t	t
1720	66	35	2017-08-04 08:18:28.045096	t	t
1721	66	19	2017-07-29 08:18:28.045125	t	t
1722	66	18	2017-08-01 08:18:28.045154	t	t
1723	66	25	2017-08-07 08:18:28.045182	t	t
1724	66	14	2017-08-12 08:18:28.045211	t	t
1725	66	20	2017-08-01 08:18:28.045239	t	t
1726	66	35	2017-08-01 08:18:28.045266	f	t
1727	66	32	2017-08-11 08:18:28.045294	f	t
1728	66	37	2017-08-12 08:18:28.045323	f	t
1729	66	27	2017-07-23 08:18:28.045351	f	t
1730	66	33	2017-08-03 08:18:28.045379	f	t
1731	66	34	2017-08-06 08:18:28.045408	f	t
1732	66	31	2017-07-25 08:18:28.045436	f	t
1733	66	21	2017-08-08 08:18:28.045465	f	t
1734	66	15	2017-08-02 08:18:28.045492	f	t
1735	66	29	2017-08-14 08:18:28.045521	f	t
1736	66	20	2017-08-06 08:18:28.045549	f	t
1737	66	17	2017-08-11 08:18:28.045578	f	t
1738	66	18	2017-08-06 08:18:28.045606	f	t
1739	66	24	2017-07-23 08:18:28.045634	f	t
1740	66	7	2017-08-10 08:18:28.045662	f	t
1741	66	23	2017-07-23 08:18:28.04569	f	t
1742	66	28	2017-08-07 08:18:28.045718	f	t
1743	66	8	2017-07-23 08:18:28.045746	f	t
1744	66	25	2017-08-12 08:18:28.045774	f	t
1745	66	22	2017-07-30 08:18:28.045802	f	t
1746	66	10	2017-08-16 08:18:28.04583	f	t
1747	66	11	2017-08-06 08:18:28.045863	f	t
1748	66	13	2017-08-14 08:18:28.045892	f	t
1749	66	12	2017-07-23 08:18:28.045921	f	t
1750	67	7	2017-08-10 08:18:28.045951	t	t
1751	67	17	2017-07-27 08:18:28.04598	t	t
1752	67	9	2017-08-12 08:18:28.046008	t	t
1753	67	16	2017-08-15 08:18:28.046036	f	t
1754	67	21	2017-08-14 08:18:28.046066	f	t
1755	68	11	2017-08-03 08:18:28.046095	t	t
1756	68	27	2017-08-05 08:18:28.046123	t	t
1757	68	12	2017-08-06 08:18:28.046152	t	t
1758	68	25	2017-07-24 08:18:28.046181	t	t
1759	68	7	2017-08-15 08:18:28.046209	t	t
1760	68	10	2017-07-23 08:18:28.046237	t	t
1761	68	15	2017-08-09 08:18:28.046265	t	t
1762	68	18	2017-08-04 08:18:28.046294	t	t
1763	68	36	2017-08-09 08:18:28.046322	t	t
1764	68	16	2017-07-25 08:18:28.046352	t	t
1765	68	32	2017-08-01 08:18:28.046381	t	t
1766	68	24	2017-08-06 08:18:28.046409	t	t
1767	68	29	2017-07-26 08:18:28.046438	t	t
1768	68	20	2017-07-26 08:18:28.046466	t	t
1769	68	34	2017-07-27 08:18:28.046494	t	t
1770	68	28	2017-08-05 08:18:28.046522	t	t
1771	68	9	2017-07-29 08:18:28.046549	t	t
1772	68	34	2017-07-29 08:18:28.046578	f	t
1773	68	19	2017-07-24 08:18:28.046605	f	t
1774	68	9	2017-08-08 08:18:28.046634	f	t
1775	68	29	2017-07-27 08:18:28.046662	f	t
1776	68	26	2017-08-02 08:18:28.04669	f	t
1777	68	35	2017-08-05 08:18:28.046718	f	t
1778	68	10	2017-08-08 08:18:28.046746	f	t
1779	68	18	2017-08-01 08:18:28.046774	f	t
1780	68	25	2017-08-10 08:18:28.046802	f	t
1781	68	23	2017-08-04 08:18:28.04683	f	t
1782	6	21	2017-07-23 08:18:28.046858	t	t
1783	6	14	2017-07-28 08:18:28.046887	t	t
1784	6	9	2017-08-12 08:18:28.046915	f	t
1785	6	28	2017-07-24 08:18:28.046943	f	t
1786	6	33	2017-07-28 08:18:28.046971	f	t
1787	9	19	2017-08-12 08:18:28.047	t	t
1788	9	26	2017-08-06 08:18:28.047028	f	t
1789	9	11	2017-08-14 08:18:28.047056	f	t
1790	9	31	2017-08-16 08:18:28.047084	f	t
1791	9	29	2017-08-12 08:18:28.047113	f	t
1792	9	20	2017-07-23 08:18:28.047141	f	t
1793	9	15	2017-08-12 08:18:28.047169	f	t
1794	13	20	2017-07-28 08:18:28.047197	t	t
1795	13	16	2017-07-24 08:18:28.047225	t	t
1796	13	22	2017-07-24 08:18:28.047253	t	t
1797	13	10	2017-07-24 08:18:28.047281	f	t
1798	13	20	2017-07-30 08:18:28.047309	f	t
1799	13	8	2017-07-25 08:18:28.047357	f	t
1800	14	37	2017-07-30 08:18:28.047386	f	t
1801	14	33	2017-08-13 08:18:28.047415	f	t
1802	14	7	2017-07-23 08:18:28.047444	f	t
1803	14	25	2017-07-26 08:18:28.047473	f	t
1804	14	31	2017-08-15 08:18:28.047516	f	t
1805	18	20	2017-08-07 08:18:28.047593	t	t
1806	18	27	2017-08-11 08:18:28.047631	t	t
1807	18	7	2017-08-14 08:18:28.047673	f	t
1808	18	22	2017-07-30 08:18:28.047703	f	t
1809	18	8	2017-08-12 08:18:28.047742	f	t
1810	18	12	2017-08-11 08:18:28.047771	f	t
1811	18	19	2017-08-17 08:18:28.0478	f	t
1812	18	21	2017-08-04 08:18:28.047828	f	t
1813	18	37	2017-07-29 08:18:28.047857	f	t
1814	18	18	2017-08-10 08:18:28.047886	f	t
1815	18	15	2017-07-29 08:18:28.047915	f	t
1816	18	33	2017-08-11 08:18:28.047943	f	t
1817	18	10	2017-08-05 08:18:28.047972	f	t
1818	18	34	2017-08-05 08:18:28.048	f	t
1819	18	13	2017-08-02 08:18:28.048029	f	t
1820	18	27	2017-07-25 08:18:28.048057	f	t
1821	18	24	2017-07-24 08:18:28.048086	f	t
1822	18	25	2017-07-27 08:18:28.048115	f	t
1823	18	29	2017-07-29 08:18:28.048143	f	t
1824	22	27	2017-08-01 08:18:28.048172	t	t
1825	22	20	2017-07-23 08:18:28.048201	t	t
1826	22	18	2017-08-01 08:18:28.04823	t	t
1827	22	36	2017-08-03 08:18:28.048258	t	t
1828	22	25	2017-08-15 08:18:28.048286	t	t
1829	22	9	2017-07-30 08:18:28.048315	t	t
1830	22	33	2017-07-30 08:18:28.048344	t	t
1831	22	26	2017-08-08 08:18:28.048372	f	t
1832	22	21	2017-08-16 08:18:28.0484	f	t
1833	22	18	2017-08-14 08:18:28.048429	f	t
1834	22	25	2017-08-09 08:18:28.048457	f	t
1835	22	36	2017-08-13 08:18:28.048487	f	t
1836	25	12	2017-07-23 08:18:28.048516	t	t
1837	25	27	2017-08-03 08:18:28.048544	t	t
1838	25	16	2017-08-03 08:18:28.048572	t	t
1839	25	27	2017-08-02 08:18:28.048601	f	t
1840	31	33	2017-08-10 08:18:28.048629	t	t
1841	31	20	2017-08-03 08:18:28.048657	t	t
1842	31	12	2017-08-11 08:18:28.048685	t	t
1843	31	31	2017-07-23 08:18:28.048714	t	t
1844	31	11	2017-08-11 08:18:28.048743	t	t
1845	31	23	2017-08-10 08:18:28.048772	t	t
1846	31	26	2017-08-03 08:18:28.0488	t	t
1847	31	7	2017-08-15 08:18:28.048828	f	t
1848	31	9	2017-08-10 08:18:28.048856	f	t
1849	31	19	2017-08-16 08:18:28.048884	f	t
1850	31	37	2017-08-09 08:18:28.048912	f	t
1851	31	33	2017-08-04 08:18:28.048941	f	t
1852	31	27	2017-08-13 08:18:28.048969	f	t
1853	33	27	2017-07-24 08:18:28.048998	t	t
1854	33	17	2017-08-16 08:18:28.049026	t	t
1855	33	19	2017-08-03 08:18:28.049055	t	t
1856	33	21	2017-08-13 08:18:28.049083	t	t
1857	33	15	2017-08-01 08:18:28.049112	t	t
1858	33	11	2017-08-08 08:18:28.049139	t	t
1859	33	20	2017-08-15 08:18:28.049168	t	t
1860	33	22	2017-07-30 08:18:28.049196	f	t
1861	33	8	2017-08-15 08:18:28.049224	f	t
1862	33	9	2017-07-28 08:18:28.049253	f	t
1863	33	31	2017-08-11 08:18:28.049281	f	t
1864	33	29	2017-07-26 08:18:28.04931	f	t
1865	33	7	2017-07-25 08:18:28.049338	f	t
1866	33	25	2017-08-03 08:18:28.049366	f	t
1867	33	24	2017-07-25 08:18:28.049394	f	t
1868	33	35	2017-08-01 08:18:28.049423	f	t
1869	33	11	2017-07-31 08:18:28.049451	f	t
1870	33	14	2017-07-23 08:18:28.049479	f	t
1871	33	10	2017-07-28 08:18:28.049508	f	t
1872	33	16	2017-07-24 08:18:28.049536	f	t
1873	33	23	2017-07-29 08:18:28.049564	f	t
1874	33	27	2017-08-01 08:18:28.049592	f	t
1875	33	20	2017-07-25 08:18:28.04962	f	t
1876	33	32	2017-08-15 08:18:28.049648	f	t
1877	33	12	2017-07-27 08:18:28.049677	f	t
1878	33	21	2017-08-05 08:18:28.049705	f	t
1879	33	15	2017-08-17 08:18:28.049733	f	t
1880	33	13	2017-07-31 08:18:28.049761	f	t
1881	33	26	2017-08-04 08:18:28.049789	f	t
1882	37	29	2017-08-15 08:18:28.049817	t	t
1883	37	8	2017-08-06 08:18:28.04985	t	t
1884	37	26	2017-08-01 08:18:28.04988	t	t
1885	37	20	2017-07-28 08:18:28.049909	t	t
1886	37	27	2017-07-28 08:18:28.049937	t	t
1887	37	25	2017-07-25 08:18:28.049966	t	t
1888	37	12	2017-07-27 08:18:28.049995	f	t
1889	37	37	2017-07-26 08:18:28.050023	f	t
1890	37	27	2017-08-05 08:18:28.050051	f	t
1891	37	22	2017-08-15 08:18:28.050079	f	t
1892	37	18	2017-07-29 08:18:28.050108	f	t
1893	37	21	2017-08-14 08:18:28.050135	f	t
1894	37	10	2017-08-10 08:18:28.050165	f	t
1895	37	16	2017-08-16 08:18:28.050193	f	t
1896	38	34	2017-07-28 08:18:28.050222	t	t
1897	38	15	2017-08-15 08:18:28.050251	t	t
1898	38	18	2017-08-03 08:18:28.050279	t	t
1899	38	19	2017-07-31 08:18:28.050308	t	t
1900	38	31	2017-08-11 08:18:28.050336	t	t
1901	38	19	2017-08-03 08:18:28.050365	f	t
1902	38	23	2017-07-23 08:18:28.050394	f	t
1903	38	8	2017-08-05 08:18:28.050421	f	t
1904	38	21	2017-08-12 08:18:28.05045	f	t
1905	38	7	2017-07-29 08:18:28.050478	f	t
1906	43	28	2017-07-26 08:18:28.050507	t	t
1907	43	17	2017-08-01 08:18:28.050536	t	t
1908	43	33	2017-08-15 08:18:28.050565	t	t
1909	43	20	2017-07-29 08:18:28.050593	t	t
1910	43	12	2017-08-06 08:18:28.050621	t	t
1911	45	25	2017-08-04 08:18:28.05065	t	t
1912	45	8	2017-07-29 08:18:28.050679	t	t
1913	45	11	2017-07-28 08:18:28.050707	t	t
1914	45	13	2017-08-04 08:18:28.050736	t	t
1915	45	33	2017-08-14 08:18:28.050764	t	t
1916	45	12	2017-08-09 08:18:28.050815	t	t
1917	45	20	2017-08-13 08:18:28.050874	f	t
1918	48	15	2017-07-31 08:18:28.050915	t	t
1919	48	10	2017-08-05 08:18:28.050954	t	t
1920	48	26	2017-08-15 08:18:28.050993	t	t
1921	48	20	2017-08-11 08:18:28.051022	t	t
1922	48	17	2017-08-10 08:18:28.05105	t	t
1923	48	35	2017-08-12 08:18:28.051078	t	t
1924	48	9	2017-08-15 08:18:28.051107	t	t
1925	48	27	2017-07-24 08:18:28.051136	f	t
1926	48	7	2017-08-05 08:18:28.051164	f	t
1927	48	21	2017-07-29 08:18:28.051193	f	t
1928	48	14	2017-08-15 08:18:28.051222	f	t
1929	48	24	2017-07-30 08:18:28.051251	f	t
1930	48	9	2017-08-15 08:18:28.05128	f	t
1931	48	35	2017-08-01 08:18:28.051319	f	t
1932	48	22	2017-08-14 08:18:28.051349	f	t
1933	48	11	2017-08-03 08:18:28.051378	f	t
1934	48	13	2017-08-09 08:18:28.051408	f	t
1935	48	31	2017-08-07 08:18:28.051437	f	t
1936	52	22	2017-08-11 08:18:28.051466	t	t
1937	52	16	2017-07-24 08:18:28.051516	t	t
1938	52	7	2017-08-07 08:18:28.051566	t	t
1939	52	31	2017-07-29 08:18:28.051595	t	t
1940	52	10	2017-07-26 08:18:28.051634	t	t
1941	52	27	2017-08-17 08:18:28.051664	t	t
1942	52	26	2017-07-29 08:18:28.051703	t	t
1943	52	20	2017-08-09 08:18:28.051733	f	t
1944	52	24	2017-08-03 08:18:28.051774	f	t
1945	52	27	2017-07-25 08:18:28.051814	f	t
1946	52	34	2017-07-30 08:18:28.051844	f	t
1947	52	12	2017-08-10 08:18:28.051873	f	t
1948	52	33	2017-08-09 08:18:28.051903	f	t
1949	53	34	2017-08-08 08:18:28.051944	t	t
1950	53	10	2017-08-01 08:18:28.051973	t	t
1951	53	23	2017-07-27 08:18:28.052002	t	t
1952	53	15	2017-08-10 08:18:28.052031	t	t
1953	53	7	2017-08-10 08:18:28.052069	t	t
1954	53	29	2017-08-08 08:18:28.0521	t	t
1955	53	28	2017-08-16 08:18:28.052131	t	t
1956	53	27	2017-08-16 08:18:28.052161	t	t
1957	53	12	2017-07-27 08:18:28.052191	t	t
1958	53	16	2017-08-02 08:18:28.052221	t	t
1959	53	17	2017-08-10 08:18:28.05226	t	t
1960	53	31	2017-08-11 08:18:28.052289	t	t
1961	53	32	2017-07-24 08:18:28.052317	t	t
1962	53	9	2017-08-07 08:18:28.052346	t	t
1963	53	25	2017-08-17 08:18:28.052375	t	t
1964	53	20	2017-07-31 08:18:28.052405	t	t
1965	53	22	2017-07-31 08:18:28.052434	t	t
1966	53	23	2017-08-09 08:18:28.052463	f	t
1967	53	10	2017-07-23 08:18:28.052492	f	t
1968	53	24	2017-07-30 08:18:28.052521	f	t
1969	53	8	2017-08-14 08:18:28.052549	f	t
1970	53	15	2017-07-30 08:18:28.052579	f	t
1971	53	18	2017-08-10 08:18:28.052607	f	t
1972	53	14	2017-07-24 08:18:28.052636	f	t
1973	53	29	2017-07-26 08:18:28.052664	f	t
1974	53	31	2017-08-11 08:18:28.052693	f	t
1975	53	7	2017-08-06 08:18:28.052722	f	t
1976	53	13	2017-08-13 08:18:28.052762	f	t
1977	53	17	2017-08-02 08:18:28.052792	f	t
1978	53	12	2017-08-15 08:18:28.052832	f	t
1979	53	29	2017-08-02 08:18:28.052862	f	t
1980	53	26	2017-07-27 08:18:28.052891	f	t
1981	53	28	2017-08-13 08:18:28.052921	f	t
1982	53	25	2017-07-28 08:18:28.05295	f	t
1983	69	26	2017-08-02 08:18:28.05298	t	t
1984	69	10	2017-08-10 08:18:28.053008	f	t
1985	69	14	2017-08-14 08:18:28.053038	f	t
\.


--
-- Name: clicked_arguments_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('clicked_arguments_uid_seq', 1985, true);


--
-- Data for Name: clicked_statements; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY clicked_statements (uid, statement_uid, author_uid, "timestamp", is_up_vote, is_valid) FROM stdin;
1215	1	17	2017-08-17 08:18:27.764817	t	t
1216	1	9	2017-07-31 08:18:27.764941	t	t
1217	1	21	2017-07-24 08:18:27.764985	t	t
1218	1	21	2017-08-13 08:18:27.765021	f	t
1219	1	36	2017-08-14 08:18:27.765055	f	t
1220	2	32	2017-07-29 08:18:27.765087	t	t
1221	2	19	2017-07-26 08:18:27.76512	f	t
1222	2	11	2017-08-07 08:18:27.765152	f	t
1223	2	32	2017-08-02 08:18:27.765184	f	t
1224	2	11	2017-08-12 08:18:27.765215	f	t
1225	2	35	2017-08-08 08:18:27.765246	f	t
1226	2	25	2017-07-30 08:18:27.765277	f	t
1227	2	17	2017-07-28 08:18:27.765307	f	t
1228	2	28	2017-07-23 08:18:27.765338	f	t
1229	2	34	2017-07-27 08:18:27.765368	f	t
1230	2	26	2017-08-07 08:18:27.765399	f	t
1231	3	24	2017-08-17 08:18:27.765429	t	t
1232	3	34	2017-08-02 08:18:27.76546	t	t
1233	3	32	2017-08-06 08:18:27.765491	t	t
1234	3	7	2017-08-13 08:18:27.765521	t	t
1235	3	35	2017-07-23 08:18:27.765552	t	t
1236	3	29	2017-08-07 08:18:27.765582	t	t
1237	3	31	2017-08-14 08:18:27.765613	t	t
1238	3	7	2017-08-02 08:18:27.765643	t	t
1239	3	20	2017-08-10 08:18:27.765674	f	t
1240	3	31	2017-08-17 08:18:27.765703	f	t
1241	3	29	2017-08-07 08:18:27.765734	f	t
1242	4	10	2017-08-11 08:18:27.765763	t	t
1243	4	33	2017-07-27 08:18:27.765794	t	t
1244	4	32	2017-08-04 08:18:27.765824	t	t
1245	4	12	2017-07-30 08:18:27.76587	t	t
1246	4	29	2017-07-30 08:18:27.7659	t	t
1247	4	11	2017-08-03 08:18:27.76593	t	t
1248	4	31	2017-08-12 08:18:27.76596	t	t
1249	4	18	2017-07-24 08:18:27.765988	t	t
1250	4	26	2017-07-29 08:18:27.766017	t	t
1251	4	12	2017-08-06 08:18:27.766046	t	t
1252	4	27	2017-07-23 08:18:27.766075	t	t
1253	4	17	2017-08-04 08:18:27.766104	t	t
1254	4	16	2017-07-25 08:18:27.766133	t	t
1255	4	13	2017-07-27 08:18:27.766162	t	t
1256	4	33	2017-08-04 08:18:27.76619	t	t
1257	4	9	2017-08-15 08:18:27.766219	t	t
1258	4	35	2017-07-28 08:18:27.766248	t	t
1259	4	36	2017-08-17 08:18:27.766277	t	t
1260	4	35	2017-07-27 08:18:27.766305	t	t
1261	4	21	2017-07-25 08:18:27.766334	t	t
1262	4	15	2017-07-28 08:18:27.766364	t	t
1263	4	29	2017-07-28 08:18:27.766393	t	t
1264	5	27	2017-08-13 08:18:27.766422	t	t
1265	5	9	2017-08-01 08:18:27.766451	t	t
1266	5	17	2017-08-11 08:18:27.766479	t	t
1267	5	25	2017-07-28 08:18:27.766507	t	t
1268	5	18	2017-07-28 08:18:27.766535	t	t
1269	5	37	2017-07-28 08:18:27.766563	t	t
1270	5	13	2017-08-17 08:18:27.766592	t	t
1271	5	34	2017-08-17 08:18:27.766621	t	t
1272	5	14	2017-08-04 08:18:27.76665	t	t
1273	6	26	2017-07-31 08:18:27.766679	t	t
1274	6	25	2017-08-08 08:18:27.766708	t	t
1275	6	10	2017-08-05 08:18:27.766737	t	t
1276	6	11	2017-08-05 08:18:27.766765	t	t
1277	6	35	2017-08-13 08:18:27.766794	f	t
1278	6	35	2017-07-27 08:18:27.766822	f	t
1279	7	28	2017-07-27 08:18:27.766851	t	t
1280	7	14	2017-08-07 08:18:27.76688	t	t
1281	7	13	2017-07-25 08:18:27.766908	t	t
1282	7	29	2017-07-27 08:18:27.766937	t	t
1283	7	14	2017-07-26 08:18:27.766965	t	t
1284	8	29	2017-08-04 08:18:27.766994	t	t
1285	8	19	2017-08-15 08:18:27.767023	t	t
1286	8	12	2017-08-05 08:18:27.767052	t	t
1287	8	32	2017-08-10 08:18:27.76708	t	t
1288	8	33	2017-07-24 08:18:27.767109	t	t
1289	8	20	2017-08-17 08:18:27.767137	t	t
1290	8	14	2017-07-29 08:18:27.767167	t	t
1291	8	27	2017-07-25 08:18:27.767195	t	t
1292	8	26	2017-08-06 08:18:27.767224	f	t
1293	8	8	2017-08-03 08:18:27.767253	f	t
1294	8	26	2017-07-30 08:18:27.767282	f	t
1295	8	37	2017-08-09 08:18:27.767311	f	t
1296	8	29	2017-08-04 08:18:27.76734	f	t
1297	8	36	2017-08-02 08:18:27.767369	f	t
1298	8	10	2017-07-25 08:18:27.767398	f	t
1299	9	25	2017-08-02 08:18:27.767427	t	t
1300	9	10	2017-08-17 08:18:27.767456	t	t
1301	9	35	2017-08-15 08:18:27.767485	t	t
1302	9	7	2017-08-09 08:18:27.767514	t	t
1303	9	15	2017-08-03 08:18:27.767542	t	t
1304	9	19	2017-08-12 08:18:27.767571	t	t
1305	9	19	2017-07-27 08:18:27.7676	t	t
1306	9	26	2017-08-11 08:18:27.767628	t	t
1307	9	20	2017-07-31 08:18:27.767656	t	t
1308	9	11	2017-08-17 08:18:27.767684	f	t
1309	9	13	2017-08-04 08:18:27.767712	f	t
1310	9	12	2017-08-10 08:18:27.76774	f	t
1311	9	32	2017-07-23 08:18:27.767769	f	t
1312	9	10	2017-08-09 08:18:27.767798	f	t
1313	10	36	2017-07-29 08:18:27.767826	t	t
1314	10	8	2017-08-05 08:18:27.767854	t	t
1315	10	19	2017-08-14 08:18:27.767882	t	t
1316	10	35	2017-08-10 08:18:27.76791	t	t
1317	10	34	2017-08-02 08:18:27.767939	t	t
1318	10	12	2017-08-08 08:18:27.767967	t	t
1319	10	32	2017-08-14 08:18:27.767995	t	t
1320	10	31	2017-08-08 08:18:27.768024	t	t
1321	10	29	2017-07-25 08:18:27.768063	t	t
1322	10	23	2017-08-02 08:18:27.768113	f	t
1323	10	12	2017-08-04 08:18:27.768151	f	t
1324	11	7	2017-08-15 08:18:27.76818	t	t
1325	11	29	2017-08-09 08:18:27.768208	t	t
1326	11	10	2017-08-17 08:18:27.768236	t	t
1327	11	9	2017-08-04 08:18:27.768264	f	t
1328	11	19	2017-08-17 08:18:27.768292	f	t
1329	12	13	2017-08-05 08:18:27.768321	t	t
1330	12	21	2017-08-16 08:18:27.768349	t	t
1331	12	17	2017-08-17 08:18:27.768377	t	t
1332	12	29	2017-08-08 08:18:27.768406	t	t
1333	12	11	2017-08-01 08:18:27.768434	t	t
1334	12	33	2017-08-12 08:18:27.768463	f	t
1335	12	12	2017-08-16 08:18:27.768491	f	t
1336	12	14	2017-07-31 08:18:27.76852	f	t
1337	12	34	2017-08-14 08:18:27.768549	f	t
1338	13	24	2017-08-05 08:18:27.768578	t	t
1339	13	29	2017-08-07 08:18:27.768606	t	t
1340	13	17	2017-08-05 08:18:27.768635	t	t
1341	13	34	2017-08-05 08:18:27.768663	t	t
1342	13	25	2017-08-11 08:18:27.768692	t	t
1343	13	34	2017-08-07 08:18:27.76872	t	t
1344	13	9	2017-08-02 08:18:27.768748	t	t
1345	13	29	2017-08-06 08:18:27.768777	t	t
1346	13	27	2017-08-04 08:18:27.768805	t	t
1347	13	12	2017-08-08 08:18:27.768834	f	t
1348	13	21	2017-08-06 08:18:27.768862	f	t
1349	14	34	2017-07-23 08:18:27.76889	t	t
1350	14	16	2017-07-28 08:18:27.768918	t	t
1351	14	20	2017-08-03 08:18:27.768947	t	t
1352	14	19	2017-07-27 08:18:27.768975	f	t
1353	14	23	2017-07-28 08:18:27.769004	f	t
1354	15	19	2017-07-24 08:18:27.769032	t	t
1355	15	25	2017-07-27 08:18:27.769061	t	t
1356	16	31	2017-08-03 08:18:27.769089	t	t
1357	16	9	2017-08-09 08:18:27.769117	t	t
1358	16	14	2017-08-11 08:18:27.769145	f	t
1359	16	23	2017-08-11 08:18:27.769174	f	t
1360	17	34	2017-08-08 08:18:27.769203	t	t
1361	17	27	2017-08-12 08:18:27.769232	t	t
1362	17	20	2017-08-14 08:18:27.769261	t	t
1363	17	13	2017-07-28 08:18:27.76929	t	t
1364	17	11	2017-07-31 08:18:27.769318	t	t
1365	17	15	2017-07-31 08:18:27.769347	f	t
1366	17	18	2017-07-24 08:18:27.769376	f	t
1367	17	34	2017-07-29 08:18:27.769405	f	t
1368	17	18	2017-08-10 08:18:27.769434	f	t
1369	17	10	2017-07-23 08:18:27.769462	f	t
1370	17	29	2017-07-23 08:18:27.769491	f	t
1371	18	12	2017-07-30 08:18:27.76952	t	t
1372	18	17	2017-08-15 08:18:27.769548	t	t
1373	18	16	2017-07-30 08:18:27.769577	t	t
1374	18	27	2017-08-13 08:18:27.769606	t	t
1375	18	24	2017-08-02 08:18:27.769634	f	t
1376	18	22	2017-08-12 08:18:27.769662	f	t
1377	18	28	2017-08-13 08:18:27.769691	f	t
1378	18	36	2017-07-30 08:18:27.769719	f	t
1379	18	29	2017-07-30 08:18:27.769748	f	t
1380	18	33	2017-08-14 08:18:27.769776	f	t
1381	18	23	2017-07-30 08:18:27.769805	f	t
1382	18	20	2017-07-23 08:18:27.769833	f	t
1383	19	34	2017-08-13 08:18:27.769877	t	t
1384	19	17	2017-07-31 08:18:27.769917	t	t
1385	19	34	2017-07-26 08:18:27.769946	t	t
1386	19	24	2017-07-29 08:18:27.769975	t	t
1387	19	12	2017-08-17 08:18:27.770003	t	t
1388	19	37	2017-07-31 08:18:27.770032	t	t
1389	19	10	2017-08-15 08:18:27.77006	t	t
1390	19	29	2017-08-09 08:18:27.770089	t	t
1391	19	27	2017-07-24 08:18:27.770118	t	t
1392	19	29	2017-07-31 08:18:27.770146	t	t
1393	19	33	2017-07-29 08:18:27.770174	t	t
1394	19	21	2017-08-12 08:18:27.770202	t	t
1395	19	15	2017-08-05 08:18:27.770231	t	t
1396	19	14	2017-07-26 08:18:27.77026	t	t
1397	19	37	2017-07-30 08:18:27.770288	t	t
1398	19	14	2017-08-15 08:18:27.770316	t	t
1399	19	11	2017-08-10 08:18:27.770344	t	t
1400	19	9	2017-07-24 08:18:27.770373	f	t
1401	19	25	2017-08-08 08:18:27.7704	f	t
1402	19	22	2017-08-09 08:18:27.770428	f	t
1403	19	7	2017-07-29 08:18:27.770456	f	t
1404	19	27	2017-08-10 08:18:27.770484	f	t
1405	19	35	2017-07-28 08:18:27.770512	f	t
1406	19	34	2017-08-16 08:18:27.770541	f	t
1407	19	31	2017-07-31 08:18:27.770569	f	t
1408	19	37	2017-07-29 08:18:27.770597	f	t
1409	19	24	2017-08-15 08:18:27.770626	f	t
1410	19	37	2017-07-26 08:18:27.770654	f	t
1411	19	12	2017-08-05 08:18:27.770683	f	t
1412	19	35	2017-08-15 08:18:27.770711	f	t
1413	19	9	2017-08-11 08:18:27.77074	f	t
1414	19	34	2017-08-16 08:18:27.770769	f	t
1415	19	37	2017-07-28 08:18:27.770798	f	t
1416	19	29	2017-08-03 08:18:27.770827	f	t
1417	19	34	2017-07-26 08:18:27.770866	f	t
1418	19	12	2017-08-04 08:18:27.770897	f	t
1419	19	15	2017-08-07 08:18:27.770927	f	t
1420	19	34	2017-07-29 08:18:27.770957	f	t
1421	19	12	2017-08-11 08:18:27.770987	f	t
1422	19	29	2017-07-29 08:18:27.771017	f	t
1423	20	23	2017-07-31 08:18:27.771047	t	t
1424	20	16	2017-08-17 08:18:27.771076	t	t
1425	20	31	2017-07-28 08:18:27.771107	t	t
1426	20	8	2017-08-11 08:18:27.771137	t	t
1427	20	14	2017-08-06 08:18:27.771167	t	t
1428	20	7	2017-08-15 08:18:27.771197	t	t
1429	20	26	2017-08-14 08:18:27.771228	t	t
1430	20	32	2017-08-09 08:18:27.771259	t	t
1431	20	31	2017-08-17 08:18:27.771289	t	t
1432	20	10	2017-08-07 08:18:27.771319	f	t
1433	20	32	2017-07-29 08:18:27.771349	f	t
1434	21	31	2017-08-08 08:18:27.771379	t	t
1435	21	15	2017-07-29 08:18:27.77141	t	t
1436	21	7	2017-08-02 08:18:27.77144	t	t
1437	21	7	2017-07-26 08:18:27.77147	t	t
1438	21	19	2017-07-31 08:18:27.7715	t	t
1439	21	37	2017-07-29 08:18:27.77153	t	t
1440	21	8	2017-08-06 08:18:27.77156	t	t
1441	21	20	2017-08-02 08:18:27.771591	t	t
1442	21	29	2017-07-26 08:18:27.771621	f	t
1443	21	36	2017-07-23 08:18:27.771652	f	t
1444	21	13	2017-07-24 08:18:27.771681	f	t
1445	21	31	2017-07-31 08:18:27.771712	f	t
1446	21	32	2017-08-14 08:18:27.771742	f	t
1447	21	8	2017-07-30 08:18:27.771772	f	t
1448	21	23	2017-07-28 08:18:27.771802	f	t
1449	22	8	2017-08-06 08:18:27.771831	t	t
1450	22	32	2017-07-24 08:18:27.77187	t	t
1451	22	28	2017-07-23 08:18:27.771899	t	t
1452	22	28	2017-08-16 08:18:27.771927	t	t
1453	22	24	2017-07-30 08:18:27.771956	t	t
1454	22	15	2017-08-02 08:18:27.771985	f	t
1455	22	34	2017-08-09 08:18:27.772013	f	t
1456	22	25	2017-08-14 08:18:27.772042	f	t
1457	23	20	2017-07-31 08:18:27.77207	t	t
1458	23	26	2017-08-17 08:18:27.772099	t	t
1459	23	25	2017-08-15 08:18:27.772127	t	t
1460	23	20	2017-08-08 08:18:27.772156	t	t
1461	23	13	2017-07-24 08:18:27.772185	t	t
1462	23	28	2017-08-12 08:18:27.772213	t	t
1463	23	31	2017-08-12 08:18:27.772242	t	t
1464	23	35	2017-08-10 08:18:27.772289	t	t
1465	23	28	2017-07-31 08:18:27.772319	t	t
1466	23	11	2017-08-06 08:18:27.772349	f	t
1467	23	33	2017-08-12 08:18:27.772379	f	t
1468	23	28	2017-07-29 08:18:27.772408	f	t
1469	23	35	2017-08-05 08:18:27.772436	f	t
1470	23	11	2017-07-31 08:18:27.772465	f	t
1471	23	31	2017-08-08 08:18:27.772494	f	t
1472	23	24	2017-08-16 08:18:27.772523	f	t
1473	24	18	2017-07-23 08:18:27.772552	t	t
1474	24	22	2017-07-24 08:18:27.77258	t	t
1475	24	8	2017-07-27 08:18:27.772609	t	t
1476	24	16	2017-08-17 08:18:27.772638	t	t
1477	24	34	2017-08-09 08:18:27.772667	t	t
1478	24	14	2017-08-04 08:18:27.772696	t	t
1479	24	29	2017-08-07 08:18:27.772724	t	t
1480	24	14	2017-08-05 08:18:27.772753	t	t
1481	24	31	2017-08-08 08:18:27.772781	t	t
1482	24	15	2017-08-08 08:18:27.77281	f	t
1483	24	23	2017-08-06 08:18:27.772838	f	t
1484	24	35	2017-07-24 08:18:27.772866	f	t
1485	24	21	2017-07-25 08:18:27.772894	f	t
1486	24	25	2017-08-09 08:18:27.772923	f	t
1487	24	29	2017-07-24 08:18:27.772951	f	t
1488	24	31	2017-08-04 08:18:27.772979	f	t
1489	24	25	2017-07-27 08:18:27.773007	f	t
1490	24	31	2017-08-11 08:18:27.773036	f	t
1491	24	21	2017-08-16 08:18:27.773065	f	t
1492	24	10	2017-07-26 08:18:27.773093	f	t
1493	24	17	2017-08-02 08:18:27.773121	f	t
1494	24	25	2017-08-05 08:18:27.773149	f	t
1495	24	25	2017-07-23 08:18:27.773177	f	t
1496	24	21	2017-08-10 08:18:27.773217	f	t
1497	24	7	2017-08-12 08:18:27.773246	f	t
1498	24	31	2017-08-10 08:18:27.773285	f	t
1499	24	33	2017-07-29 08:18:27.773313	f	t
1500	24	13	2017-07-31 08:18:27.773342	f	t
1501	25	31	2017-07-31 08:18:27.77337	t	t
1502	25	9	2017-08-05 08:18:27.773398	t	t
1503	25	31	2017-08-08 08:18:27.773426	t	t
1504	25	20	2017-08-06 08:18:27.773454	t	t
1505	25	20	2017-07-24 08:18:27.773482	t	t
1506	25	21	2017-08-03 08:18:27.77351	t	t
1507	25	17	2017-08-07 08:18:27.773538	t	t
1508	25	37	2017-07-26 08:18:27.773566	t	t
1509	25	19	2017-08-17 08:18:27.773594	t	t
1510	25	17	2017-08-10 08:18:27.773623	f	t
1511	25	15	2017-08-14 08:18:27.773651	f	t
1512	25	36	2017-08-15 08:18:27.773681	f	t
1513	25	23	2017-08-15 08:18:27.773709	f	t
1514	25	21	2017-08-07 08:18:27.773738	f	t
1515	25	14	2017-08-13 08:18:27.773767	f	t
1516	25	32	2017-08-15 08:18:27.773806	f	t
1517	25	14	2017-07-24 08:18:27.773834	f	t
1518	25	15	2017-08-06 08:18:27.773898	f	t
1519	25	33	2017-08-16 08:18:27.773945	f	t
1520	25	33	2017-08-12 08:18:27.773996	f	t
1521	25	21	2017-08-08 08:18:27.774037	f	t
1522	25	29	2017-08-01 08:18:27.774077	f	t
1523	25	14	2017-08-05 08:18:27.774143	f	t
1524	25	25	2017-07-27 08:18:27.774182	f	t
1525	25	29	2017-08-10 08:18:27.774213	f	t
1526	25	37	2017-08-16 08:18:27.774242	f	t
1527	25	16	2017-07-27 08:18:27.774272	f	t
1528	25	10	2017-08-17 08:18:27.774303	f	t
1529	26	35	2017-07-26 08:18:27.774333	t	t
1530	26	37	2017-08-12 08:18:27.774363	t	t
1531	26	32	2017-07-28 08:18:27.774394	t	t
1532	26	28	2017-08-05 08:18:27.774424	t	t
1533	26	35	2017-07-26 08:18:27.774453	t	t
1534	26	32	2017-07-27 08:18:27.774482	t	t
1535	26	36	2017-08-07 08:18:27.774512	t	t
1536	26	37	2017-08-11 08:18:27.774541	t	t
1537	26	11	2017-08-02 08:18:27.77457	t	t
1538	26	15	2017-07-28 08:18:27.7746	t	t
1539	26	29	2017-07-28 08:18:27.77463	t	t
1540	26	36	2017-08-05 08:18:27.774659	t	t
1541	26	27	2017-08-15 08:18:27.774689	t	t
1542	26	11	2017-08-14 08:18:27.774719	t	t
1543	26	35	2017-08-08 08:18:27.774748	t	t
1544	26	31	2017-08-06 08:18:27.774777	t	t
1545	26	25	2017-08-13 08:18:27.774806	t	t
1546	26	35	2017-08-11 08:18:27.774847	f	t
1547	26	17	2017-07-26 08:18:27.774888	f	t
1548	26	23	2017-07-30 08:18:27.774916	f	t
1549	26	9	2017-08-06 08:18:27.774946	f	t
1550	26	14	2017-08-08 08:18:27.774976	f	t
1551	26	15	2017-07-30 08:18:27.775006	f	t
1552	27	9	2017-07-31 08:18:27.775035	t	t
1553	27	9	2017-07-28 08:18:27.775064	t	t
1554	27	29	2017-07-28 08:18:27.775094	t	t
1555	27	13	2017-07-26 08:18:27.775133	t	t
1556	27	16	2017-08-09 08:18:27.775196	t	t
1557	27	15	2017-07-23 08:18:27.77523	t	t
1558	27	32	2017-07-29 08:18:27.775286	t	t
1559	27	24	2017-08-07 08:18:27.775319	t	t
1560	27	11	2017-08-08 08:18:27.775349	t	t
1561	27	11	2017-07-27 08:18:27.775378	t	t
1562	27	31	2017-07-27 08:18:27.775408	t	t
1563	27	20	2017-07-26 08:18:27.775437	t	t
1564	27	14	2017-08-13 08:18:27.775467	t	t
1565	27	29	2017-08-13 08:18:27.775498	f	t
1566	28	19	2017-07-25 08:18:27.775528	t	t
1567	28	15	2017-08-08 08:18:27.775587	t	t
1568	28	33	2017-07-30 08:18:27.775652	t	t
1569	28	8	2017-08-14 08:18:27.775728	t	t
1570	28	17	2017-08-09 08:18:27.775796	t	t
1571	28	12	2017-07-27 08:18:27.77585	t	t
1572	28	13	2017-08-09 08:18:27.775905	t	t
1573	28	32	2017-08-01 08:18:27.775961	t	t
1574	28	19	2017-08-17 08:18:27.776014	t	t
1575	28	22	2017-08-14 08:18:27.776084	t	t
1576	28	29	2017-08-12 08:18:27.776139	f	t
1577	29	22	2017-07-25 08:18:27.77618	t	t
1578	29	21	2017-08-08 08:18:27.776211	t	t
1579	29	28	2017-07-29 08:18:27.776242	f	t
1580	29	26	2017-07-26 08:18:27.776272	f	t
1581	30	31	2017-07-31 08:18:27.776301	t	t
1582	30	13	2017-07-28 08:18:27.776332	t	t
1583	30	25	2017-07-30 08:18:27.776382	t	t
1584	30	12	2017-07-23 08:18:27.776418	t	t
1585	30	28	2017-08-12 08:18:27.776481	t	t
1586	30	25	2017-07-28 08:18:27.776523	t	t
1587	30	37	2017-07-29 08:18:27.776553	t	t
1588	30	27	2017-08-06 08:18:27.776582	t	t
1589	30	25	2017-07-31 08:18:27.776611	t	t
1590	30	35	2017-08-06 08:18:27.776639	t	t
1591	30	28	2017-08-15 08:18:27.776668	t	t
1592	30	16	2017-08-12 08:18:27.776697	t	t
1593	30	26	2017-07-23 08:18:27.776727	t	t
1594	30	15	2017-08-09 08:18:27.776756	t	t
1595	30	7	2017-08-13 08:18:27.776785	t	t
1596	30	28	2017-07-25 08:18:27.776815	t	t
1597	30	31	2017-07-23 08:18:27.776844	t	t
1598	30	8	2017-08-04 08:18:27.776873	t	t
1599	30	29	2017-08-11 08:18:27.776902	t	t
1600	30	29	2017-08-16 08:18:27.776931	t	t
1601	30	33	2017-07-23 08:18:27.776961	t	t
1602	30	7	2017-07-24 08:18:27.776989	t	t
1603	30	15	2017-08-13 08:18:27.777018	t	t
1604	30	31	2017-08-04 08:18:27.777046	f	t
1605	30	29	2017-08-15 08:18:27.777075	f	t
1606	30	33	2017-08-15 08:18:27.777103	f	t
1607	30	13	2017-08-17 08:18:27.777132	f	t
1608	30	26	2017-08-08 08:18:27.777161	f	t
1609	30	19	2017-07-27 08:18:27.777189	f	t
1610	30	33	2017-07-24 08:18:27.777217	f	t
1611	30	10	2017-08-08 08:18:27.777246	f	t
1612	30	17	2017-08-05 08:18:27.777275	f	t
1613	30	27	2017-08-16 08:18:27.777304	f	t
1614	30	7	2017-08-01 08:18:27.777332	f	t
1615	30	15	2017-08-14 08:18:27.777361	f	t
1616	30	27	2017-08-10 08:18:27.777389	f	t
1617	30	21	2017-08-15 08:18:27.777418	f	t
1618	30	12	2017-07-23 08:18:27.777447	f	t
1619	30	34	2017-08-05 08:18:27.777476	f	t
1620	30	31	2017-08-11 08:18:27.777505	f	t
1621	30	7	2017-07-26 08:18:27.777533	f	t
1622	31	29	2017-08-05 08:18:27.777562	t	t
1623	31	8	2017-08-08 08:18:27.777591	f	t
1624	31	29	2017-08-07 08:18:27.77762	f	t
1625	31	36	2017-08-17 08:18:27.777649	f	t
1626	32	29	2017-08-02 08:18:27.777678	t	t
1627	32	26	2017-08-13 08:18:27.777708	t	t
1628	32	23	2017-08-15 08:18:27.777738	t	t
1629	32	24	2017-07-27 08:18:27.777768	t	t
1630	32	7	2017-07-30 08:18:27.777796	t	t
1631	32	36	2017-08-13 08:18:27.777825	t	t
1632	32	26	2017-08-07 08:18:27.777863	t	t
1633	32	7	2017-08-04 08:18:27.777894	t	t
1634	32	11	2017-08-15 08:18:27.777923	t	t
1635	32	28	2017-08-10 08:18:27.777953	t	t
1636	32	11	2017-08-13 08:18:27.777982	f	t
1637	32	25	2017-07-28 08:18:27.778011	f	t
1638	32	37	2017-07-30 08:18:27.77804	f	t
1639	32	19	2017-08-06 08:18:27.778069	f	t
1640	32	23	2017-08-01 08:18:27.778098	f	t
1641	32	23	2017-08-07 08:18:27.778127	f	t
1642	32	19	2017-08-12 08:18:27.778155	f	t
1643	32	23	2017-08-08 08:18:27.778184	f	t
1644	32	14	2017-08-15 08:18:27.778213	f	t
1645	33	25	2017-08-16 08:18:27.778242	t	t
1646	33	16	2017-07-31 08:18:27.778271	t	t
1647	33	9	2017-08-11 08:18:27.7783	t	t
1648	33	7	2017-08-02 08:18:27.778329	t	t
1649	33	31	2017-07-24 08:18:27.778358	f	t
1650	34	22	2017-08-07 08:18:27.778386	t	t
1651	34	31	2017-07-31 08:18:27.778416	t	t
1652	34	37	2017-08-14 08:18:27.778444	t	t
1653	34	26	2017-07-26 08:18:27.778473	t	t
1654	34	24	2017-07-27 08:18:27.778501	t	t
1655	34	9	2017-08-16 08:18:27.778531	t	t
1656	34	23	2017-07-24 08:18:27.77856	t	t
1657	34	37	2017-07-27 08:18:27.778589	t	t
1658	34	28	2017-07-25 08:18:27.778619	t	t
1659	34	14	2017-07-24 08:18:27.778648	t	t
1660	34	18	2017-08-09 08:18:27.778676	t	t
1661	34	15	2017-07-29 08:18:27.778705	t	t
1662	34	12	2017-07-29 08:18:27.778733	t	t
1663	34	35	2017-08-01 08:18:27.778761	t	t
1664	34	10	2017-08-13 08:18:27.778791	t	t
1665	34	34	2017-08-01 08:18:27.778819	t	t
1666	34	15	2017-08-06 08:18:27.778847	t	t
1667	34	7	2017-08-10 08:18:27.778876	t	t
1668	34	23	2017-08-12 08:18:27.778905	t	t
1669	34	14	2017-07-30 08:18:27.778933	t	t
1670	34	24	2017-08-14 08:18:27.778962	t	t
1671	34	11	2017-08-11 08:18:27.778991	t	t
1672	34	21	2017-08-15 08:18:27.77902	t	t
1673	34	37	2017-07-23 08:18:27.779049	f	t
1674	35	32	2017-08-17 08:18:27.779076	t	t
1675	35	15	2017-08-03 08:18:27.779105	t	t
1676	35	15	2017-08-12 08:18:27.779133	t	t
1677	35	9	2017-08-09 08:18:27.77918	f	t
1678	35	15	2017-08-01 08:18:27.779232	f	t
1679	35	17	2017-07-31 08:18:27.779282	f	t
1680	35	16	2017-07-31 08:18:27.779337	f	t
1681	35	19	2017-08-15 08:18:27.779393	f	t
1682	35	13	2017-07-28 08:18:27.779425	f	t
1683	35	11	2017-08-04 08:18:27.779456	f	t
1684	35	10	2017-07-24 08:18:27.779487	f	t
1685	35	13	2017-08-05 08:18:27.779517	f	t
1686	35	13	2017-07-29 08:18:27.779558	f	t
1687	35	25	2017-08-05 08:18:27.779589	f	t
1688	35	12	2017-08-04 08:18:27.779646	f	t
1689	35	29	2017-07-29 08:18:27.779688	f	t
1690	35	21	2017-08-03 08:18:27.779718	f	t
1691	35	27	2017-07-23 08:18:27.779747	f	t
1692	35	10	2017-08-01 08:18:27.779776	f	t
1693	35	13	2017-08-14 08:18:27.779805	f	t
1694	35	18	2017-08-10 08:18:27.779835	f	t
1695	36	13	2017-07-27 08:18:27.779864	t	t
1696	36	29	2017-08-10 08:18:27.779892	t	t
1697	36	8	2017-07-28 08:18:27.780147	t	t
1698	36	15	2017-08-09 08:18:27.780181	t	t
1699	36	15	2017-07-23 08:18:27.780229	t	t
1700	36	24	2017-08-05 08:18:27.780269	t	t
1701	36	28	2017-07-30 08:18:27.780299	t	t
1702	36	20	2017-08-09 08:18:27.780329	t	t
1703	36	36	2017-07-30 08:18:27.780357	t	t
1704	36	21	2017-08-13 08:18:27.780387	t	t
1705	36	12	2017-08-01 08:18:27.780417	t	t
1706	36	28	2017-08-15 08:18:27.780446	t	t
1707	36	29	2017-07-25 08:18:27.780475	t	t
1708	36	20	2017-08-16 08:18:27.780504	f	t
1709	36	22	2017-08-08 08:18:27.780533	f	t
1710	36	9	2017-07-24 08:18:27.780563	f	t
1711	36	35	2017-08-13 08:18:27.780591	f	t
1712	36	36	2017-08-08 08:18:27.78062	f	t
1713	36	24	2017-08-10 08:18:27.780649	f	t
1714	36	14	2017-08-06 08:18:27.780678	f	t
1715	36	18	2017-08-09 08:18:27.780717	f	t
1716	36	13	2017-08-03 08:18:27.780747	f	t
1717	36	32	2017-08-12 08:18:27.780777	f	t
1718	36	29	2017-08-09 08:18:27.780807	f	t
1719	36	7	2017-08-01 08:18:27.780846	f	t
1720	37	8	2017-08-08 08:18:27.780889	f	t
1721	38	36	2017-08-03 08:18:27.780921	t	t
1722	38	20	2017-07-29 08:18:27.780951	t	t
1723	38	34	2017-07-26 08:18:27.780982	t	t
1724	38	33	2017-07-25 08:18:27.781013	t	t
1725	38	29	2017-08-03 08:18:27.781044	t	t
1726	38	18	2017-07-31 08:18:27.781075	t	t
1727	38	14	2017-08-12 08:18:27.781106	t	t
1728	38	36	2017-08-12 08:18:27.781137	t	t
1729	38	29	2017-08-09 08:18:27.781168	t	t
1730	38	27	2017-08-12 08:18:27.781199	t	t
1731	38	7	2017-07-29 08:18:27.781231	t	t
1732	38	18	2017-08-12 08:18:27.781261	t	t
1733	38	21	2017-07-23 08:18:27.781293	t	t
1734	38	22	2017-08-13 08:18:27.781323	f	t
1735	38	32	2017-08-05 08:18:27.781353	f	t
1736	38	33	2017-07-26 08:18:27.781384	f	t
1737	38	31	2017-07-31 08:18:27.781415	f	t
1738	38	22	2017-08-08 08:18:27.781445	f	t
1739	38	16	2017-08-07 08:18:27.781476	f	t
1740	38	31	2017-08-11 08:18:27.781507	f	t
1741	38	23	2017-07-30 08:18:27.781554	f	t
1742	38	31	2017-07-26 08:18:27.78159	f	t
1743	38	14	2017-08-11 08:18:27.781621	f	t
1744	38	33	2017-07-27 08:18:27.781652	f	t
1745	38	17	2017-07-24 08:18:27.781683	f	t
1746	38	28	2017-08-04 08:18:27.781713	f	t
1747	38	20	2017-08-02 08:18:27.781744	f	t
1748	38	34	2017-08-15 08:18:27.781774	f	t
1749	38	13	2017-07-24 08:18:27.781804	f	t
1750	38	19	2017-08-01 08:18:27.781835	f	t
1751	39	13	2017-08-06 08:18:27.781875	t	t
1752	39	12	2017-08-17 08:18:27.781907	t	t
1753	39	8	2017-07-28 08:18:27.781938	t	t
1754	39	10	2017-08-13 08:18:27.781978	t	t
1755	39	27	2017-07-31 08:18:27.782008	f	t
1756	39	13	2017-07-24 08:18:27.782037	f	t
1757	39	20	2017-08-01 08:18:27.782067	f	t
1758	39	29	2017-08-17 08:18:27.782097	f	t
1759	39	31	2017-07-27 08:18:27.782126	f	t
1760	39	27	2017-07-25 08:18:27.782156	f	t
1761	39	21	2017-08-04 08:18:27.782188	f	t
1762	39	24	2017-08-08 08:18:27.782218	f	t
1763	39	21	2017-07-23 08:18:27.782247	f	t
1764	39	33	2017-07-25 08:18:27.782277	f	t
1765	39	24	2017-07-25 08:18:27.782307	f	t
1766	39	36	2017-08-06 08:18:27.782337	f	t
1767	39	10	2017-07-30 08:18:27.782368	f	t
1768	39	9	2017-07-30 08:18:27.782399	f	t
1769	39	21	2017-08-11 08:18:27.782429	f	t
1770	40	26	2017-08-14 08:18:27.782458	t	t
1771	40	37	2017-08-16 08:18:27.782489	t	t
1772	40	31	2017-07-23 08:18:27.782519	t	t
1773	40	19	2017-08-16 08:18:27.782575	t	t
1774	40	8	2017-07-31 08:18:27.782621	t	t
1775	40	26	2017-08-04 08:18:27.782654	t	t
1776	40	28	2017-08-14 08:18:27.782684	t	t
1777	40	29	2017-07-23 08:18:27.782714	t	t
1778	40	34	2017-07-23 08:18:27.782745	t	t
1779	40	12	2017-08-11 08:18:27.782775	t	t
1780	40	13	2017-08-05 08:18:27.782805	t	t
1781	40	7	2017-08-07 08:18:27.782836	t	t
1782	40	37	2017-08-02 08:18:27.782866	t	t
1783	40	9	2017-08-10 08:18:27.782905	t	t
1784	40	23	2017-08-10 08:18:27.782936	t	t
1785	40	17	2017-07-25 08:18:27.782966	t	t
1786	40	37	2017-08-01 08:18:27.782998	t	t
1787	40	14	2017-08-07 08:18:27.783028	t	t
1788	40	20	2017-07-27 08:18:27.783058	f	t
1789	40	27	2017-07-26 08:18:27.783089	f	t
1790	40	17	2017-07-26 08:18:27.78312	f	t
1791	40	32	2017-08-07 08:18:27.78315	f	t
1792	40	34	2017-08-02 08:18:27.783181	f	t
1793	40	21	2017-07-26 08:18:27.783212	f	t
1794	40	8	2017-07-27 08:18:27.783243	f	t
1795	40	15	2017-08-09 08:18:27.783273	f	t
1796	40	7	2017-07-28 08:18:27.783304	f	t
1797	41	7	2017-08-11 08:18:27.783335	t	t
1798	41	26	2017-07-26 08:18:27.783366	f	t
1799	41	11	2017-08-08 08:18:27.783398	f	t
1800	41	35	2017-07-25 08:18:27.783431	f	t
1801	41	25	2017-08-13 08:18:27.783467	f	t
1802	42	19	2017-08-05 08:18:27.783499	t	t
1803	42	27	2017-07-30 08:18:27.783535	t	t
1804	42	8	2017-08-17 08:18:27.783567	t	t
1805	42	9	2017-08-04 08:18:27.783598	t	t
1806	42	28	2017-07-24 08:18:27.78363	t	t
1807	42	18	2017-07-26 08:18:27.783661	t	t
1808	42	29	2017-07-24 08:18:27.783692	t	t
1809	42	19	2017-08-11 08:18:27.783724	f	t
1810	43	24	2017-08-01 08:18:27.783756	f	t
1811	43	25	2017-08-06 08:18:27.783787	f	t
1812	43	27	2017-08-03 08:18:27.783818	f	t
1813	43	31	2017-08-05 08:18:27.783853	f	t
1814	44	8	2017-08-03 08:18:27.7839	t	t
1815	44	28	2017-08-13 08:18:27.783931	t	t
1816	44	12	2017-08-16 08:18:27.783961	t	t
1817	44	33	2017-08-04 08:18:27.784003	t	t
1818	44	17	2017-07-30 08:18:27.784032	t	t
1819	44	24	2017-08-12 08:18:27.784062	t	t
1820	44	27	2017-07-31 08:18:27.784091	t	t
1821	44	9	2017-08-07 08:18:27.784121	t	t
1822	44	37	2017-08-15 08:18:27.78415	t	t
1823	44	10	2017-07-30 08:18:27.78418	t	t
1824	44	37	2017-07-25 08:18:27.78421	t	t
1825	44	7	2017-08-17 08:18:27.78424	t	t
1826	44	31	2017-08-12 08:18:27.784269	t	t
1827	44	21	2017-08-03 08:18:27.784298	t	t
1828	44	36	2017-08-14 08:18:27.784326	t	t
1829	44	18	2017-08-03 08:18:27.784357	t	t
1830	44	14	2017-07-31 08:18:27.784387	f	t
1831	44	9	2017-08-05 08:18:27.784417	f	t
1832	44	8	2017-08-12 08:18:27.784446	f	t
1833	44	19	2017-08-03 08:18:27.784488	f	t
1834	44	25	2017-08-01 08:18:27.784548	f	t
1835	45	23	2017-08-15 08:18:27.784592	t	t
1836	45	8	2017-07-31 08:18:27.784621	f	t
1837	45	14	2017-08-11 08:18:27.78465	f	t
1838	46	24	2017-08-17 08:18:27.784679	t	t
1839	46	32	2017-08-05 08:18:27.78471	t	t
1840	46	8	2017-08-11 08:18:27.78474	t	t
1841	46	37	2017-07-24 08:18:27.78477	f	t
1842	46	37	2017-07-23 08:18:27.7848	f	t
1843	47	29	2017-08-04 08:18:27.784828	t	t
1844	47	8	2017-08-09 08:18:27.784857	t	t
1845	47	9	2017-08-10 08:18:27.784885	t	t
1846	47	25	2017-08-16 08:18:27.784914	t	t
1847	47	17	2017-08-11 08:18:27.784945	t	t
1848	47	9	2017-08-12 08:18:27.784975	t	t
1849	47	7	2017-08-01 08:18:27.785004	t	t
1850	47	19	2017-08-15 08:18:27.785033	t	t
1851	47	18	2017-08-05 08:18:27.785062	t	t
1852	47	7	2017-07-24 08:18:27.785091	f	t
1853	47	37	2017-07-24 08:18:27.785121	f	t
1854	47	29	2017-08-09 08:18:27.78515	f	t
1855	47	8	2017-07-28 08:18:27.78518	f	t
1856	47	18	2017-08-15 08:18:27.785209	f	t
1857	47	16	2017-08-17 08:18:27.785238	f	t
1858	47	12	2017-07-24 08:18:27.785267	f	t
1859	47	20	2017-08-15 08:18:27.785295	f	t
1860	47	25	2017-07-24 08:18:27.785324	f	t
1861	47	24	2017-07-25 08:18:27.785354	f	t
1862	47	25	2017-07-26 08:18:27.785383	f	t
1863	47	17	2017-07-28 08:18:27.785412	f	t
1864	47	13	2017-08-10 08:18:27.785442	f	t
1865	47	8	2017-07-26 08:18:27.785472	f	t
1866	48	11	2017-08-05 08:18:27.785503	t	t
1867	48	21	2017-08-05 08:18:27.785534	t	t
1868	48	14	2017-07-23 08:18:27.785562	t	t
1869	48	15	2017-08-04 08:18:27.785592	f	t
1870	48	9	2017-08-15 08:18:27.785622	f	t
1871	48	24	2017-08-10 08:18:27.785651	f	t
1872	48	36	2017-08-17 08:18:27.78568	f	t
1873	48	29	2017-08-17 08:18:27.785709	f	t
1874	49	31	2017-08-03 08:18:27.785738	f	t
1875	49	15	2017-07-26 08:18:27.78577	f	t
1876	49	35	2017-07-24 08:18:27.785799	f	t
1877	49	36	2017-08-09 08:18:27.785828	f	t
1878	49	20	2017-08-09 08:18:27.785866	f	t
1879	49	26	2017-08-10 08:18:27.785896	f	t
1880	50	20	2017-08-02 08:18:27.785926	t	t
1881	50	36	2017-07-25 08:18:27.785954	t	t
1882	50	7	2017-08-03 08:18:27.785983	t	t
1883	50	25	2017-07-31 08:18:27.786012	t	t
1884	50	21	2017-07-28 08:18:27.786041	t	t
1885	50	35	2017-08-06 08:18:27.786072	t	t
1886	50	13	2017-07-24 08:18:27.786102	t	t
1887	50	7	2017-08-13 08:18:27.786132	t	t
1888	50	11	2017-07-25 08:18:27.786161	t	t
1889	50	37	2017-07-25 08:18:27.78619	t	t
1890	50	14	2017-07-24 08:18:27.786219	t	t
1891	50	22	2017-08-14 08:18:27.786248	t	t
1892	50	13	2017-07-24 08:18:27.786278	t	t
1893	50	20	2017-07-29 08:18:27.786307	t	t
1894	50	35	2017-08-06 08:18:27.786335	t	t
1895	50	10	2017-07-31 08:18:27.786363	t	t
1896	50	23	2017-08-03 08:18:27.786392	t	t
1897	50	25	2017-08-08 08:18:27.786421	t	t
1898	50	24	2017-07-27 08:18:27.786449	f	t
1899	50	17	2017-08-08 08:18:27.786478	f	t
1900	50	27	2017-07-27 08:18:27.786507	f	t
1901	50	7	2017-08-08 08:18:27.786536	f	t
1902	50	23	2017-08-13 08:18:27.786564	f	t
1903	50	12	2017-08-05 08:18:27.786593	f	t
1904	50	20	2017-08-03 08:18:27.786622	f	t
1905	51	12	2017-07-24 08:18:27.786651	t	t
1906	51	36	2017-08-05 08:18:27.78668	t	t
1907	51	20	2017-08-17 08:18:27.786709	t	t
1908	51	17	2017-08-17 08:18:27.786738	t	t
1909	51	25	2017-07-28 08:18:27.786767	f	t
1910	51	24	2017-08-17 08:18:27.786797	f	t
1911	51	35	2017-08-15 08:18:27.786828	f	t
1912	52	7	2017-08-12 08:18:27.786858	t	t
1913	52	26	2017-07-31 08:18:27.786888	t	t
1914	52	11	2017-08-15 08:18:27.786917	t	t
1915	53	22	2017-08-04 08:18:27.786947	t	t
1916	53	7	2017-07-29 08:18:27.786976	t	t
1917	53	17	2017-08-07 08:18:27.787005	t	t
1918	53	15	2017-07-30 08:18:27.787035	t	t
1919	53	17	2017-08-08 08:18:27.787063	t	t
1920	53	14	2017-08-12 08:18:27.787092	t	t
1921	53	29	2017-07-25 08:18:27.787123	t	t
1922	53	14	2017-07-28 08:18:27.78717	f	t
1923	53	27	2017-07-23 08:18:27.787224	f	t
1924	53	12	2017-07-23 08:18:27.787276	f	t
1925	54	29	2017-08-05 08:18:27.787337	t	t
1926	54	34	2017-08-04 08:18:27.787375	f	t
1927	54	31	2017-08-07 08:18:27.787405	f	t
1928	55	32	2017-07-24 08:18:27.787435	t	t
1929	56	25	2017-07-28 08:18:27.787465	t	t
1930	56	20	2017-08-08 08:18:27.787494	t	t
1931	56	25	2017-08-14 08:18:27.787526	t	t
1932	56	10	2017-08-11 08:18:27.787557	t	t
1933	56	25	2017-07-29 08:18:27.787587	t	t
1934	56	35	2017-08-07 08:18:27.787636	t	t
1935	56	10	2017-08-03 08:18:27.787667	t	t
1936	56	8	2017-08-12 08:18:27.787697	f	t
1937	56	12	2017-07-31 08:18:27.787727	f	t
1938	56	26	2017-08-11 08:18:27.787756	f	t
1939	56	31	2017-08-02 08:18:27.787785	f	t
1940	56	27	2017-07-23 08:18:27.787814	f	t
1941	56	29	2017-07-27 08:18:27.787845	f	t
1942	56	12	2017-08-17 08:18:27.787875	f	t
1943	56	29	2017-08-06 08:18:27.787905	f	t
1944	56	29	2017-08-15 08:18:27.787934	f	t
1945	56	26	2017-07-23 08:18:27.787964	f	t
1946	56	7	2017-08-11 08:18:27.787993	f	t
1947	56	12	2017-08-04 08:18:27.788026	f	t
1948	56	11	2017-08-13 08:18:27.788055	f	t
1949	56	23	2017-07-23 08:18:27.788085	f	t
1950	56	11	2017-08-07 08:18:27.788116	f	t
1951	56	16	2017-08-17 08:18:27.788145	f	t
1952	56	28	2017-08-05 08:18:27.788175	f	t
1953	56	21	2017-08-03 08:18:27.788204	f	t
1954	57	34	2017-08-02 08:18:27.788234	t	t
1955	57	18	2017-08-06 08:18:27.788263	t	t
1956	57	28	2017-08-07 08:18:27.788292	t	t
1957	57	31	2017-08-03 08:18:27.788321	t	t
1958	57	25	2017-08-14 08:18:27.788351	t	t
1959	57	13	2017-07-31 08:18:27.78838	t	t
1960	57	27	2017-07-25 08:18:27.788411	f	t
1961	57	9	2017-07-24 08:18:27.788441	f	t
1962	57	20	2017-08-14 08:18:27.78847	f	t
1963	57	12	2017-08-10 08:18:27.7885	f	t
1964	58	17	2017-07-27 08:18:27.788529	t	t
1965	58	13	2017-08-13 08:18:27.788558	t	t
1966	58	31	2017-08-03 08:18:27.788587	t	t
1967	58	29	2017-07-30 08:18:27.788619	f	t
1968	58	8	2017-08-14 08:18:27.788649	f	t
1969	58	14	2017-08-10 08:18:27.788678	f	t
1970	58	7	2017-08-14 08:18:27.788708	f	t
1971	58	32	2017-08-14 08:18:27.788737	f	t
1972	59	19	2017-08-08 08:18:27.788766	t	t
1973	59	20	2017-08-08 08:18:27.788795	t	t
1974	59	18	2017-07-25 08:18:27.788824	t	t
1975	59	19	2017-07-23 08:18:27.788853	t	t
1976	59	29	2017-07-26 08:18:27.788882	t	t
1977	59	7	2017-08-12 08:18:27.78891	t	t
1978	59	17	2017-08-10 08:18:27.788939	t	t
1979	59	36	2017-08-06 08:18:27.788968	t	t
1980	59	8	2017-08-12 08:18:27.788997	t	t
1981	59	9	2017-08-02 08:18:27.789027	t	t
1982	59	22	2017-07-23 08:18:27.789056	t	t
1983	59	11	2017-07-30 08:18:27.789089	t	t
1984	59	27	2017-07-23 08:18:27.789119	t	t
1985	59	20	2017-08-13 08:18:27.789148	t	t
1986	59	25	2017-07-27 08:18:27.789177	f	t
1987	59	35	2017-08-14 08:18:27.789207	f	t
1988	60	27	2017-08-08 08:18:27.789236	t	t
1989	60	17	2017-08-11 08:18:27.789266	t	t
1990	60	7	2017-08-06 08:18:27.789294	t	t
1991	60	10	2017-08-15 08:18:27.789323	t	t
1992	60	20	2017-08-10 08:18:27.789352	t	t
1993	60	12	2017-08-16 08:18:27.789381	t	t
1994	60	12	2017-08-11 08:18:27.789409	t	t
1995	60	7	2017-07-28 08:18:27.789439	t	t
1996	60	25	2017-07-28 08:18:27.789468	t	t
1997	60	14	2017-08-02 08:18:27.789498	t	t
1998	60	35	2017-08-02 08:18:27.789528	t	t
1999	60	20	2017-08-11 08:18:27.789557	t	t
2000	60	22	2017-08-15 08:18:27.789586	t	t
2001	60	26	2017-07-28 08:18:27.789614	t	t
2002	60	25	2017-07-27 08:18:27.789643	t	t
2003	60	28	2017-08-02 08:18:27.789671	t	t
2004	60	33	2017-07-31 08:18:27.7897	t	t
2005	60	33	2017-07-29 08:18:27.789729	t	t
2006	60	29	2017-08-15 08:18:27.789758	t	t
2007	60	21	2017-07-30 08:18:27.789787	f	t
2008	60	17	2017-07-27 08:18:27.789816	f	t
2009	60	10	2017-07-23 08:18:27.789844	f	t
2010	60	35	2017-07-31 08:18:27.789881	f	t
2011	60	12	2017-08-08 08:18:27.78991	f	t
2012	60	21	2017-07-28 08:18:27.789939	f	t
2013	60	29	2017-07-23 08:18:27.789968	f	t
2014	60	32	2017-08-13 08:18:27.789998	f	t
2015	60	11	2017-08-14 08:18:27.790029	f	t
2016	60	23	2017-08-04 08:18:27.790059	f	t
2017	60	22	2017-07-28 08:18:27.790088	f	t
2018	60	27	2017-08-15 08:18:27.790118	f	t
2019	61	24	2017-08-04 08:18:27.79015	t	t
2020	61	17	2017-07-27 08:18:27.79018	t	t
2021	61	11	2017-07-29 08:18:27.79021	t	t
2022	61	13	2017-08-15 08:18:27.79024	t	t
2023	61	9	2017-08-01 08:18:27.790269	t	t
2024	61	27	2017-08-07 08:18:27.790298	t	t
2025	61	14	2017-07-26 08:18:27.790327	t	t
2026	61	21	2017-08-11 08:18:27.790356	t	t
2027	61	36	2017-08-15 08:18:27.790386	t	t
2028	61	24	2017-07-23 08:18:27.790415	t	t
2029	61	19	2017-08-14 08:18:27.790444	f	t
2030	61	18	2017-08-09 08:18:27.790473	f	t
2031	61	19	2017-07-23 08:18:27.790503	f	t
2032	61	33	2017-08-12 08:18:27.790532	f	t
2033	61	9	2017-07-27 08:18:27.790561	f	t
2034	61	23	2017-07-25 08:18:27.790589	f	t
2035	61	25	2017-08-04 08:18:27.790618	f	t
2036	61	8	2017-08-14 08:18:27.790647	f	t
2037	61	8	2017-08-02 08:18:27.790676	f	t
2038	61	10	2017-07-28 08:18:27.790705	f	t
2039	61	17	2017-08-06 08:18:27.790734	f	t
2040	61	33	2017-08-16 08:18:27.790763	f	t
2041	62	29	2017-08-16 08:18:27.790792	t	t
2042	62	19	2017-07-24 08:18:27.790821	t	t
2043	62	20	2017-08-02 08:18:27.790849	t	t
2044	62	9	2017-07-28 08:18:27.790878	t	t
2045	62	29	2017-08-07 08:18:27.790907	t	t
2046	62	25	2017-07-29 08:18:27.790936	f	t
2047	62	14	2017-07-25 08:18:27.790965	f	t
2048	62	23	2017-08-14 08:18:27.790994	f	t
2049	62	10	2017-08-16 08:18:27.791023	f	t
2050	62	37	2017-08-01 08:18:27.791052	f	t
2051	62	7	2017-07-27 08:18:27.791082	f	t
2052	62	23	2017-08-05 08:18:27.79111	f	t
2053	63	29	2017-08-13 08:18:27.791142	t	t
2054	63	17	2017-08-16 08:18:27.791172	t	t
2055	63	14	2017-08-11 08:18:27.791203	t	t
2056	63	37	2017-07-29 08:18:27.791233	t	t
2057	63	7	2017-08-06 08:18:27.791262	t	t
2058	64	35	2017-08-01 08:18:27.791291	t	t
2059	64	37	2017-08-15 08:18:27.791331	t	t
2060	64	35	2017-08-16 08:18:27.791367	t	t
2061	64	27	2017-08-17 08:18:27.791441	t	t
2062	64	14	2017-08-17 08:18:27.791525	t	t
2063	64	10	2017-08-12 08:18:27.791576	t	t
2064	64	29	2017-08-15 08:18:27.791606	t	t
2065	64	28	2017-08-14 08:18:27.791635	t	t
2066	64	34	2017-08-09 08:18:27.791665	t	t
2067	64	10	2017-07-31 08:18:27.791694	f	t
2068	64	29	2017-08-01 08:18:27.791728	f	t
2069	64	10	2017-08-03 08:18:27.791757	f	t
2070	64	18	2017-08-14 08:18:27.791786	f	t
2071	64	22	2017-07-26 08:18:27.791815	f	t
2072	64	35	2017-08-04 08:18:27.791845	f	t
2073	64	10	2017-08-04 08:18:27.791874	f	t
2074	64	34	2017-08-11 08:18:27.791903	f	t
2075	64	25	2017-08-04 08:18:27.791932	f	t
2076	64	32	2017-08-11 08:18:27.791961	f	t
2077	64	26	2017-08-08 08:18:27.79199	f	t
2078	64	12	2017-08-16 08:18:27.792019	f	t
2079	65	29	2017-08-10 08:18:27.792049	t	t
2080	65	29	2017-08-03 08:18:27.792078	f	t
2081	65	23	2017-07-30 08:18:27.792107	f	t
2082	65	27	2017-07-29 08:18:27.792136	f	t
2083	65	29	2017-08-12 08:18:27.792165	f	t
2084	65	32	2017-08-01 08:18:27.792194	f	t
2085	66	13	2017-08-06 08:18:27.792223	t	t
2086	66	22	2017-08-04 08:18:27.792252	f	t
2087	66	13	2017-08-02 08:18:27.79228	f	t
2088	66	22	2017-07-27 08:18:27.79231	f	t
2089	66	11	2017-08-04 08:18:27.79235	f	t
2090	67	7	2017-07-24 08:18:27.792379	t	t
2091	67	12	2017-08-02 08:18:27.792422	t	t
2092	68	35	2017-07-31 08:18:27.792453	t	t
2093	68	19	2017-07-24 08:18:27.792482	f	t
2094	68	32	2017-08-13 08:18:27.792511	f	t
2095	68	16	2017-07-30 08:18:27.792541	f	t
2096	68	14	2017-07-25 08:18:27.792569	f	t
2097	68	19	2017-08-07 08:18:27.792599	f	t
2098	69	15	2017-07-29 08:18:27.792628	t	t
2099	69	24	2017-08-16 08:18:27.792658	t	t
2100	69	15	2017-08-12 08:18:27.792688	t	t
2101	69	9	2017-08-01 08:18:27.792717	t	t
2102	69	16	2017-07-25 08:18:27.792747	t	t
2103	69	36	2017-08-13 08:18:27.792775	t	t
2104	69	26	2017-07-28 08:18:27.792804	t	t
2105	69	15	2017-07-27 08:18:27.792832	t	t
2106	69	31	2017-08-03 08:18:27.79286	t	t
2107	69	36	2017-07-25 08:18:27.792889	t	t
2108	69	21	2017-07-30 08:18:27.792927	f	t
2109	69	29	2017-07-29 08:18:27.79296	f	t
2110	69	9	2017-07-29 08:18:27.792991	f	t
2111	69	37	2017-08-01 08:18:27.793021	f	t
2112	69	10	2017-07-23 08:18:27.793052	f	t
2113	69	11	2017-07-30 08:18:27.793082	f	t
2114	69	32	2017-08-03 08:18:27.793112	f	t
2115	69	32	2017-07-25 08:18:27.793143	f	t
2116	69	31	2017-08-03 08:18:27.793175	f	t
2117	69	24	2017-08-17 08:18:27.793207	f	t
2118	69	19	2017-08-04 08:18:27.793237	f	t
2119	69	9	2017-07-23 08:18:27.793268	f	t
2120	69	22	2017-07-23 08:18:27.793298	f	t
2121	69	18	2017-08-04 08:18:27.793328	f	t
2122	69	32	2017-07-30 08:18:27.793358	f	t
2123	69	22	2017-07-25 08:18:27.793389	f	t
2124	70	33	2017-07-25 08:18:27.793419	t	t
2125	70	15	2017-08-06 08:18:27.793449	t	t
2126	70	32	2017-08-08 08:18:27.793479	t	t
2127	70	22	2017-08-16 08:18:27.793512	t	t
2128	70	17	2017-08-11 08:18:27.793544	f	t
2129	71	10	2017-07-23 08:18:27.793575	t	t
2130	71	34	2017-08-09 08:18:27.793605	t	t
2131	71	37	2017-08-08 08:18:27.793636	t	t
2132	71	35	2017-08-07 08:18:27.793666	f	t
2133	71	37	2017-07-31 08:18:27.793696	f	t
2134	71	16	2017-08-03 08:18:27.793727	f	t
2135	71	31	2017-07-24 08:18:27.793758	f	t
2136	72	16	2017-07-29 08:18:27.793787	t	t
2137	72	29	2017-08-11 08:18:27.793817	t	t
2138	72	32	2017-07-27 08:18:27.793853	t	t
2139	72	23	2017-08-17 08:18:27.793886	t	t
2140	72	35	2017-08-14 08:18:27.793926	t	t
2141	72	37	2017-07-29 08:18:27.793956	t	t
2142	72	32	2017-07-25 08:18:27.793985	t	t
2143	72	27	2017-08-11 08:18:27.794014	t	t
2144	72	36	2017-08-14 08:18:27.794043	t	t
2145	72	11	2017-08-05 08:18:27.794072	f	t
2146	73	8	2017-07-29 08:18:27.794101	t	t
2147	73	9	2017-08-10 08:18:27.79413	t	t
2148	73	19	2017-08-17 08:18:27.794159	t	t
2149	73	25	2017-08-17 08:18:27.794189	t	t
2150	73	33	2017-08-07 08:18:27.794218	t	t
2151	73	7	2017-08-01 08:18:27.794248	f	t
2152	73	32	2017-07-27 08:18:27.794278	f	t
2153	73	14	2017-08-06 08:18:27.794307	f	t
2154	73	9	2017-08-11 08:18:27.794335	f	t
2155	73	9	2017-08-02 08:18:27.794364	f	t
2156	73	17	2017-08-09 08:18:27.794393	f	t
2157	73	29	2017-07-31 08:18:27.794421	f	t
2158	73	19	2017-08-15 08:18:27.79445	f	t
2159	73	13	2017-07-29 08:18:27.794479	f	t
2160	74	27	2017-07-30 08:18:27.794508	t	t
2161	74	28	2017-07-27 08:18:27.794537	t	t
2162	74	14	2017-07-31 08:18:27.794566	t	t
2163	74	13	2017-08-07 08:18:27.794598	t	t
2164	74	15	2017-08-01 08:18:27.79463	t	t
2165	74	19	2017-08-10 08:18:27.794661	t	t
2166	74	16	2017-08-05 08:18:27.794691	f	t
2167	74	14	2017-08-01 08:18:27.794736	f	t
2168	74	15	2017-08-09 08:18:27.794765	f	t
2169	74	25	2017-08-06 08:18:27.794797	f	t
2170	74	37	2017-08-06 08:18:27.794826	f	t
2171	74	8	2017-08-02 08:18:27.794855	f	t
2172	74	18	2017-08-17 08:18:27.794884	f	t
2173	74	31	2017-07-27 08:18:27.794913	f	t
2174	74	12	2017-08-09 08:18:27.794941	f	t
2175	74	17	2017-08-15 08:18:27.79497	f	t
2176	74	34	2017-07-28 08:18:27.794999	f	t
2177	74	32	2017-07-29 08:18:27.795027	f	t
2178	75	7	2017-08-08 08:18:27.795056	t	t
2179	75	17	2017-08-13 08:18:27.795084	t	t
2180	75	8	2017-08-12 08:18:27.795113	t	t
2181	75	14	2017-07-26 08:18:27.795142	t	t
2182	75	32	2017-08-04 08:18:27.79517	t	t
2183	75	20	2017-07-30 08:18:27.795201	f	t
2184	75	32	2017-07-25 08:18:27.79523	f	t
2185	75	36	2017-08-01 08:18:27.79526	f	t
2186	75	22	2017-08-01 08:18:27.795288	f	t
2187	76	35	2017-08-09 08:18:27.795318	t	t
2188	76	26	2017-08-11 08:18:27.795349	t	t
2189	76	15	2017-08-03 08:18:27.795377	t	t
2190	76	10	2017-08-14 08:18:27.795407	t	t
2191	76	17	2017-07-23 08:18:27.795436	t	t
2192	76	9	2017-08-14 08:18:27.795465	t	t
2193	76	28	2017-08-05 08:18:27.795494	t	t
2194	76	23	2017-08-06 08:18:27.795523	t	t
2195	76	9	2017-08-14 08:18:27.795552	t	t
2196	76	36	2017-07-28 08:18:27.795582	f	t
2197	76	11	2017-08-05 08:18:27.79561	f	t
2198	76	29	2017-08-17 08:18:27.795638	f	t
2199	76	34	2017-08-12 08:18:27.79567	f	t
2200	76	23	2017-07-30 08:18:27.7957	f	t
2201	76	20	2017-07-30 08:18:27.795728	f	t
2202	76	22	2017-08-03 08:18:27.795757	f	t
2203	76	16	2017-08-09 08:18:27.795785	f	t
2204	76	10	2017-08-11 08:18:27.795814	f	t
2205	76	25	2017-07-23 08:18:27.795842	f	t
2206	76	29	2017-08-12 08:18:27.795871	f	t
2207	76	35	2017-08-09 08:18:27.7959	f	t
2208	77	18	2017-08-13 08:18:27.795929	t	t
2209	77	27	2017-08-11 08:18:27.795958	t	t
2210	77	27	2017-08-10 08:18:27.795987	t	t
2211	78	18	2017-08-09 08:18:27.796016	t	t
2212	78	21	2017-07-26 08:18:27.796047	t	t
2213	78	25	2017-08-04 08:18:27.796076	f	t
2214	79	15	2017-08-06 08:18:27.796106	t	t
2215	79	10	2017-08-10 08:18:27.796136	t	t
2216	79	7	2017-07-23 08:18:27.796165	t	t
2217	79	25	2017-08-13 08:18:27.796194	t	t
2218	79	27	2017-08-11 08:18:27.796223	t	t
2219	79	18	2017-08-16 08:18:27.796253	t	t
2220	79	9	2017-07-26 08:18:27.796282	t	t
2221	79	29	2017-08-02 08:18:27.796312	t	t
2222	79	22	2017-07-31 08:18:27.796341	t	t
2223	79	24	2017-08-16 08:18:27.79637	t	t
2224	79	14	2017-08-05 08:18:27.796398	t	t
2225	79	14	2017-08-13 08:18:27.796427	t	t
2226	79	23	2017-08-08 08:18:27.796455	t	t
2227	79	29	2017-08-03 08:18:27.796484	t	t
2228	79	35	2017-07-29 08:18:27.796512	f	t
2229	80	8	2017-08-17 08:18:27.796541	t	t
2230	80	22	2017-07-29 08:18:27.79657	f	t
2231	80	36	2017-08-09 08:18:27.796598	f	t
2232	80	36	2017-07-28 08:18:27.796627	f	t
2233	80	15	2017-08-12 08:18:27.796656	f	t
2234	80	35	2017-08-01 08:18:27.796685	f	t
2235	80	22	2017-08-07 08:18:27.796716	f	t
2236	80	35	2017-07-26 08:18:27.796747	f	t
2237	80	35	2017-08-16 08:18:27.796776	f	t
2238	81	32	2017-08-17 08:18:27.796805	t	t
2239	81	28	2017-08-07 08:18:27.796833	t	t
2240	81	17	2017-07-24 08:18:27.796862	t	t
2241	81	22	2017-07-31 08:18:27.79689	t	t
2242	81	13	2017-08-16 08:18:27.796919	t	t
2243	81	11	2017-07-26 08:18:27.796948	t	t
2244	81	16	2017-08-17 08:18:27.796978	t	t
2245	81	8	2017-08-12 08:18:27.797007	t	t
2246	81	29	2017-08-11 08:18:27.797035	t	t
2247	81	7	2017-07-28 08:18:27.797065	t	t
2248	81	10	2017-08-10 08:18:27.797094	t	t
2249	81	9	2017-07-27 08:18:27.797124	t	t
2250	81	12	2017-08-03 08:18:27.797152	t	t
2251	81	23	2017-08-05 08:18:27.797181	t	t
2252	81	36	2017-08-14 08:18:27.79721	t	t
2253	81	28	2017-08-05 08:18:27.797239	t	t
2254	81	26	2017-08-05 08:18:27.797268	t	t
2255	81	23	2017-08-10 08:18:27.797298	t	t
2256	81	32	2017-08-12 08:18:27.797326	t	t
2257	81	7	2017-08-10 08:18:27.797354	t	t
2258	81	32	2017-08-15 08:18:27.797383	t	t
2259	81	27	2017-08-12 08:18:27.797411	f	t
2260	81	22	2017-08-01 08:18:27.797465	f	t
2261	81	37	2017-08-11 08:18:27.797515	f	t
2262	81	35	2017-08-01 08:18:27.797581	f	t
2263	81	17	2017-08-10 08:18:27.797632	f	t
2264	81	32	2017-07-31 08:18:27.797675	f	t
2265	81	19	2017-08-09 08:18:27.797709	f	t
2266	81	11	2017-08-04 08:18:27.797751	f	t
2267	81	16	2017-08-10 08:18:27.797784	f	t
2268	81	35	2017-08-10 08:18:27.797816	f	t
2269	81	7	2017-08-05 08:18:27.797852	f	t
2270	81	26	2017-08-03 08:18:27.797896	f	t
2271	81	16	2017-08-02 08:18:27.79793	f	t
2272	81	27	2017-08-06 08:18:27.79796	f	t
2273	81	15	2017-07-30 08:18:27.79799	f	t
2274	81	29	2017-07-26 08:18:27.798019	f	t
2275	81	19	2017-08-03 08:18:27.798048	f	t
2276	81	8	2017-07-27 08:18:27.798078	f	t
2277	81	15	2017-08-12 08:18:27.798109	f	t
2278	81	28	2017-07-24 08:18:27.798139	f	t
2279	82	8	2017-08-13 08:18:27.798169	t	t
2280	82	8	2017-08-01 08:18:27.798198	t	t
2281	82	35	2017-07-26 08:18:27.798228	t	t
2282	82	35	2017-07-25 08:18:27.798257	t	t
2283	82	36	2017-07-31 08:18:27.798286	t	t
2284	82	32	2017-08-10 08:18:27.798317	f	t
2285	82	8	2017-08-15 08:18:27.798347	f	t
2286	82	29	2017-07-31 08:18:27.798376	f	t
2287	82	31	2017-08-08 08:18:27.798405	f	t
2288	82	8	2017-08-16 08:18:27.798435	f	t
2289	82	35	2017-08-07 08:18:27.798464	f	t
2290	82	36	2017-07-24 08:18:27.798493	f	t
2291	82	32	2017-08-11 08:18:27.798522	f	t
2292	82	20	2017-08-08 08:18:27.798551	f	t
2293	82	34	2017-07-31 08:18:27.79858	f	t
2294	82	22	2017-07-25 08:18:27.798608	f	t
2295	82	11	2017-08-06 08:18:27.79864	f	t
2296	82	28	2017-08-04 08:18:27.798669	f	t
2297	82	22	2017-07-29 08:18:27.798698	f	t
2298	82	14	2017-08-08 08:18:27.798727	f	t
2299	82	22	2017-08-05 08:18:27.798756	f	t
2300	82	29	2017-07-27 08:18:27.798785	f	t
2301	82	17	2017-08-17 08:18:27.798813	f	t
2302	82	21	2017-08-07 08:18:27.798843	f	t
\.


--
-- Name: clicked_statements_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('clicked_statements_uid_seq', 2302, true);


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
1	Town has to cut spending 	town-has-to-cut-spending	Our town needs to cut spending. Please discuss ideas how this should be done.		2017-08-17 08:18:20.085455	2	1	t
2	Cat or Dog	cat-or-dog	Your family argues about whether to buy a cat or dog as pet. Now your opinion matters!		2017-08-17 08:18:20.085604	2	1	f
3	Make the world better	make-the-world-better	How can we make this world a better place?		2017-08-17 08:18:20.085711	2	1	f
4	Elektroautos	elektroautos	Elektroautos - Die Autos der Zukunft? Bitte diskutieren Sie dazu.		2017-08-17 08:18:20.08581	2	2	f
5	Unterstützung der Sekretariate	unterstutzung-der-sekretariate	Unsere Sekretariate in der Informatik sind arbeitsmäßig stark überlastet. Bitte diskutieren Sie Möglichkeiten um dies zu verbessern.		2017-08-17 08:18:20.08659	2	2	f
6	Verbesserung des Informatik-Studiengangs	verbesserung-des-informatik-studiengangs	Wie können der Informatik-Studiengang verbessert und die Probleme, die durch die große Anzahl der Studierenden entstanden sind, gelöst werden?	Die Anzahl der Studierenden in der Informatik hat sich in den letzten Jahren stark erhöht. Dadurch treten zahlreiche Probleme auf, wie z.B. Raumknappheit, überfüllte Lehrveranstaltungen und ein Mangel an Plätzen zum Lernen. Wir möchten Sie gerne dazu einladen, gemeinsam mit den Dozierenden der Informatik über Lösungsmöglichkeiten zu diskutieren: Wie können der Studiengang verbessert und die Probleme, die durch die große Anzahl der Studierenden entstanden sind, gelöst werden?	2017-08-17 08:18:20.086718	2	2	t
7	Bürgerbeteiligung in der Kommune	burgerbeteiligung-in-der-kommune	Es werden Vorschläge zur Verbesserung des Zusammenlebens in unserer Kommune gesammelt.		2017-08-17 08:18:20.086847	2	2	f
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
1	14	1	t	2017-08-17 08:18:23.194786
2	16	1	f	2017-08-17 08:18:23.194894
3	17	1	t	2017-08-17 08:18:23.194998
4	22	1	t	2017-08-17 08:18:23.195102
5	23	1	t	2017-08-17 08:18:23.195205
6	20	2	f	2017-08-17 08:18:23.195308
7	21	2	t	2017-08-17 08:18:23.19541
8	18	2	f	2017-08-17 08:18:23.195511
9	34	2	t	2017-08-17 08:18:23.195613
10	24	2	f	2017-08-17 08:18:23.195715
11	25	2	f	2017-08-17 08:18:23.195815
12	26	2	f	2017-08-17 08:18:23.195917
13	27	3	f	2017-08-17 08:18:23.196018
14	28	3	f	2017-08-17 08:18:23.19612
15	33	3	f	2017-08-17 08:18:23.196228
16	19	8	t	2017-08-17 08:18:23.19633
17	35	8	t	2017-08-17 08:18:23.196459
18	36	8	t	2017-08-17 08:18:23.196556
\.


--
-- Name: last_reviewers_delete_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('last_reviewers_delete_uid_seq', 18, true);


--
-- Data for Name: last_reviewers_duplicates; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY last_reviewers_duplicates (uid, reviewer_uid, review_uid, is_okay, "timestamp") FROM stdin;
1	12	1	t	2017-08-17 08:18:23.196665
2	13	2	t	2017-08-17 08:18:23.19676
3	14	2	t	2017-08-17 08:18:23.196851
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
1	29	1	t	2017-08-17 08:18:23.194087
2	31	1	t	2017-08-17 08:18:23.194239
3	32	1	t	2017-08-17 08:18:23.194352
4	12	2	f	2017-08-17 08:18:23.194456
5	13	2	f	2017-08-17 08:18:23.194559
6	15	2	f	2017-08-17 08:18:23.194662
\.


--
-- Name: last_reviewers_optimization_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('last_reviewers_optimization_uid_seq', 6, true);


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
-- Data for Name: premisegroup_merged; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY premisegroup_merged (uid, review_uid, premisegroup_uid, "timestamp") FROM stdin;
\.


--
-- Name: premisegroup_merged_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('premisegroup_merged_uid_seq', 1, false);


--
-- Data for Name: premisegroup_splitted; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY premisegroup_splitted (uid, review_uid, premisegroup_uid, "timestamp") FROM stdin;
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
1	1	1	f	1	2017-08-17 08:18:20.342229	2	t
2	2	5	f	1	2017-08-17 08:18:20.342382	2	f
3	3	6	f	1	2017-08-17 08:18:20.342474	2	f
4	4	7	f	1	2017-08-17 08:18:20.34256	2	f
5	5	8	f	1	2017-08-17 08:18:20.342644	2	f
6	6	9	f	1	2017-08-17 08:18:20.342727	2	f
7	7	10	f	1	2017-08-17 08:18:20.342811	2	f
8	8	11	f	1	2017-08-17 08:18:20.342895	2	f
9	9	12	f	1	2017-08-17 08:18:20.342979	2	f
10	10	13	f	1	2017-08-17 08:18:20.343062	2	f
11	11	14	f	1	2017-08-17 08:18:20.343145	2	f
12	12	15	f	1	2017-08-17 08:18:20.343228	2	f
13	12	16	f	1	2017-08-17 08:18:20.343311	2	f
14	13	17	f	1	2017-08-17 08:18:20.343394	2	f
15	14	18	f	1	2017-08-17 08:18:20.343477	2	f
16	15	19	f	1	2017-08-17 08:18:20.34356	2	f
17	16	20	f	1	2017-08-17 08:18:20.343643	2	f
18	17	21	f	1	2017-08-17 08:18:20.343726	2	f
19	18	22	f	1	2017-08-17 08:18:20.34381	2	f
20	19	23	f	1	2017-08-17 08:18:20.343894	2	f
21	20	24	f	1	2017-08-17 08:18:20.343976	2	f
22	21	25	f	1	2017-08-17 08:18:20.344058	2	f
23	22	26	f	1	2017-08-17 08:18:20.344141	2	f
24	23	27	f	1	2017-08-17 08:18:20.344223	2	f
25	24	28	f	1	2017-08-17 08:18:20.344306	2	f
26	25	29	f	1	2017-08-17 08:18:20.344388	2	f
27	26	30	f	1	2017-08-17 08:18:20.344471	2	f
28	27	31	f	1	2017-08-17 08:18:20.344553	2	f
29	28	32	f	1	2017-08-17 08:18:20.344635	2	f
30	29	33	f	1	2017-08-17 08:18:20.344717	2	f
31	30	34	f	1	2017-08-17 08:18:20.344798	2	f
32	9	35	f	1	2017-08-17 08:18:20.344879	2	f
33	31	39	f	1	2017-08-17 08:18:20.344961	1	f
34	32	40	f	1	2017-08-17 08:18:20.345043	1	f
35	33	41	f	1	2017-08-17 08:18:20.345126	1	f
36	34	42	f	1	2017-08-17 08:18:20.345208	1	f
37	35	43	f	1	2017-08-17 08:18:20.345291	1	f
38	36	44	f	1	2017-08-17 08:18:20.345375	1	f
39	37	45	f	1	2017-08-17 08:18:20.345457	1	f
40	38	46	f	1	2017-08-17 08:18:20.345539	1	f
41	39	47	f	1	2017-08-17 08:18:20.345621	1	f
42	40	48	f	1	2017-08-17 08:18:20.345704	1	f
43	41	49	f	1	2017-08-17 08:18:20.345786	1	f
44	42	50	f	1	2017-08-17 08:18:20.345884	1	f
45	43	51	f	1	2017-08-17 08:18:20.345971	1	f
46	44	52	f	1	2017-08-17 08:18:20.346054	1	f
47	45	53	f	1	2017-08-17 08:18:20.346136	1	f
48	46	54	f	1	2017-08-17 08:18:20.346219	1	f
49	47	55	f	1	2017-08-17 08:18:20.346302	1	f
50	48	56	f	1	2017-08-17 08:18:20.346385	1	f
51	49	57	f	1	2017-08-17 08:18:20.346471	1	f
52	52	61	f	1	2017-08-17 08:18:20.34672	4	f
53	53	62	f	1	2017-08-17 08:18:20.346804	4	f
54	54	63	f	1	2017-08-17 08:18:20.346893	4	f
55	55	64	f	1	2017-08-17 08:18:20.347047	4	f
56	56	65	f	1	2017-08-17 08:18:20.347132	4	f
57	57	66	f	1	2017-08-17 08:18:20.347215	4	f
58	50	59	f	1	2017-08-17 08:18:20.346556	4	f
59	51	60	f	1	2017-08-17 08:18:20.346639	4	f
60	61	68	f	5	2017-08-17 08:18:20.3473	4	f
61	62	71	f	1	2017-08-17 08:18:20.347384	5	f
62	63	72	f	1	2017-08-17 08:18:20.347466	5	f
63	64	73	f	1	2017-08-17 08:18:20.347549	5	f
64	65	74	f	1	2017-08-17 08:18:20.347632	5	f
65	66	75	f	1	2017-08-17 08:18:20.347716	5	f
66	67	77	f	1	2017-08-17 08:18:20.347797	7	f
67	68	78	f	1	2017-08-17 08:18:20.347879	7	f
68	69	79	f	1	2017-08-17 08:18:20.347964	7	f
69	70	80	f	1	2017-08-17 08:18:20.348051	7	f
70	70	81	f	1	2017-08-17 08:18:20.348134	7	f
71	71	82	f	1	2017-08-17 08:18:20.348215	7	f
\.


--
-- Name: premises_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('premises_uid_seq', 71, true);


--
-- Data for Name: reputation_history; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY reputation_history (uid, reputator_uid, reputation_uid, "timestamp") FROM stdin;
1	23	1	2017-08-15 08:18:23.229119
2	23	2	2017-08-16 08:18:23.229119
3	23	3	2017-08-17 08:18:23.229119
4	25	1	2017-08-15 08:18:23.229119
5	25	2	2017-08-16 08:18:23.229119
6	25	3	2017-08-17 08:18:23.229119
7	22	1	2017-08-15 08:18:23.229119
8	22	2	2017-08-16 08:18:23.229119
9	22	3	2017-08-17 08:18:23.229119
10	34	1	2017-08-15 08:18:23.229119
11	34	2	2017-08-16 08:18:23.229119
12	34	3	2017-08-17 08:18:23.229119
13	3	1	2017-08-15 08:18:23.229119
14	3	2	2017-08-16 08:18:23.229119
15	3	3	2017-08-17 08:18:23.229119
16	3	8	2017-08-17 08:18:23.229119
17	3	3	2017-08-15 08:18:23.229119
18	3	4	2017-08-15 08:18:23.229119
19	3	5	2017-08-16 08:18:23.229119
20	3	6	2017-08-16 08:18:23.229119
21	3	9	2017-08-17 08:18:23.229119
22	3	8	2017-08-17 08:18:23.229119
23	2	4	2017-08-15 08:18:23.229119
24	2	5	2017-08-15 08:18:23.229119
25	2	6	2017-08-16 08:18:23.229119
26	2	9	2017-08-16 08:18:23.229119
27	2	7	2017-08-17 08:18:23.229119
28	2	10	2017-08-17 08:18:23.229119
29	2	8	2017-08-17 08:18:23.229119
30	2	11	2017-08-17 08:18:23.229119
31	2	12	2017-08-17 08:18:23.229119
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
1	18	15	\N	2017-08-17 08:18:23.166547	t	1	f
2	19	14	\N	2017-08-17 08:18:23.166629	t	2	f
3	20	\N	11	2017-08-17 08:18:23.166706	t	1	f
4	21	\N	9	2017-08-17 08:18:23.166787	f	1	f
5	22	\N	8	2017-08-17 08:18:23.166858	f	1	f
6	23	\N	19	2017-08-17 08:18:23.166928	f	1	f
7	24	23	\N	2017-08-17 08:18:23.166999	f	2	f
8	25	21	\N	2017-08-17 08:18:23.16707	f	2	f
9	26	7	\N	2017-08-17 08:18:23.16714	f	1	f
10	27	1	\N	2017-08-17 08:18:23.167213	t	1	f
\.


--
-- Name: review_deletes_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('review_deletes_uid_seq', 10, true);


--
-- Data for Name: review_duplicates; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY review_duplicates (uid, detector_uid, duplicate_statement_uid, original_statement_uid, "timestamp", is_executed, is_revoked) FROM stdin;
1	28	6	1	2017-08-17 08:18:23.167291	f	f
2	29	4	1	2017-08-17 08:18:23.167361	t	f
3	29	22	7	2017-08-17 08:18:23.167426	f	f
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
1	3	\N	2	2017-08-17 08:18:23.244243	f	f
\.


--
-- Name: review_edits_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('review_edits_uid_seq', 1, true);


--
-- Data for Name: review_merge; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY review_merge (uid, detector_uid, premisesgroup_uid, "timestamp", is_executed, is_revoked) FROM stdin;
1	31	1	2017-08-17 08:18:23.167499	f	f
2	32	5	2017-08-17 08:18:23.167566	f	f
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
1	12	6	\N	2017-08-17 08:18:23.166032	t	f
2	13	\N	15	2017-08-17 08:18:23.166157	t	f
3	14	\N	29	2017-08-17 08:18:23.166236	f	f
4	16	9	\N	2017-08-17 08:18:23.166383	f	f
5	17	17	\N	2017-08-17 08:18:23.166456	f	f
6	15	\N	14	2017-08-17 08:18:23.16631	f	f
\.


--
-- Name: review_optimizations_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('review_optimizations_uid_seq', 6, true);


--
-- Data for Name: review_split; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY review_split (uid, detector_uid, premisesgroup_uid, "timestamp", is_executed, is_revoked) FROM stdin;
1	33	10	2017-08-17 08:18:23.167638	f	f
2	34	12	2017-08-17 08:18:23.167705	f	f
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
1223	1	21
1224	1	32
1225	1	20
1226	1	25
1227	1	24
1228	1	29
1229	1	12
1230	1	34
1231	1	7
1232	1	28
1233	1	17
1234	1	8
1235	1	9
1236	1	36
1237	1	31
1238	1	19
1239	1	23
1240	1	22
1241	1	14
1242	1	29
1243	1	16
1244	1	10
1245	1	37
1246	1	13
1247	1	18
1248	1	35
1249	1	26
1250	1	27
1251	2	11
1252	2	29
1253	2	26
1254	2	14
1255	2	22
1256	2	31
1257	2	36
1258	2	32
1259	2	29
1260	2	7
1261	2	8
1262	2	17
1263	2	10
1264	2	12
1265	2	27
1266	2	9
1267	3	26
1268	3	18
1269	3	21
1270	3	19
1271	3	28
1272	3	13
1273	3	12
1274	3	25
1275	3	16
1276	4	29
1277	4	13
1278	4	34
1279	4	21
1280	4	19
1281	4	9
1282	4	18
1283	4	24
1284	4	32
1285	4	37
1286	4	23
1287	4	20
1288	4	35
1289	4	8
1290	4	26
1291	4	27
1292	5	15
1293	5	28
1294	5	20
1295	5	18
1296	5	19
1297	5	12
1298	5	34
1299	5	26
1300	5	33
1301	5	23
1302	5	32
1303	5	25
1304	5	31
1305	5	13
1306	8	22
1307	8	15
1308	8	35
1309	8	33
1310	8	21
1311	8	29
1312	8	12
1313	8	32
1314	8	7
1315	8	10
1316	8	29
1317	8	19
1318	8	31
1319	8	37
1320	8	24
1321	8	27
1322	8	23
1323	8	18
1324	8	17
1325	8	34
1326	8	8
1327	8	9
1328	10	22
1329	10	12
1330	10	24
1331	10	14
1332	10	16
1333	10	23
1334	10	13
1335	10	25
1336	10	20
1337	11	31
1338	11	17
1339	11	37
1340	11	32
1341	11	11
1342	11	36
1343	11	34
1344	11	35
1345	11	13
1346	11	33
1347	11	21
1348	11	9
1349	11	29
1350	11	18
1351	11	14
1352	11	10
1353	11	26
1354	11	19
1355	11	7
1356	11	16
1357	11	20
1358	12	16
1359	12	14
1360	12	27
1361	12	15
1362	12	22
1363	12	11
1364	12	36
1365	12	35
1366	12	33
1367	12	23
1368	12	8
1369	12	29
1370	12	29
1371	12	19
1372	12	20
1373	12	24
1374	12	26
1375	12	17
1376	12	10
1377	15	32
1378	15	10
1379	15	26
1380	15	36
1381	15	34
1382	15	12
1383	15	20
1384	15	24
1385	15	7
1386	15	23
1387	15	37
1388	15	29
1389	15	22
1390	15	8
1391	15	35
1392	15	33
1393	15	28
1394	15	14
1395	15	11
1396	15	9
1397	15	13
1398	15	29
1399	15	15
1400	15	16
1401	15	17
1402	15	19
1403	15	27
1404	15	18
1405	16	12
1406	16	16
1407	16	33
1408	16	31
1409	16	29
1410	16	32
1411	16	27
1412	16	26
1413	16	9
1414	16	34
1415	16	24
1416	16	19
1417	16	22
1418	16	17
1419	16	25
1420	16	35
1421	16	23
1422	16	13
1423	16	28
1424	16	18
1425	16	29
1426	16	8
1427	17	21
1428	17	7
1429	17	9
1430	17	33
1431	17	25
1432	17	20
1433	17	29
1434	17	26
1435	17	29
1436	19	23
1437	19	27
1438	19	36
1439	19	12
1440	19	21
1441	19	9
1442	19	29
1443	19	26
1444	19	35
1445	19	29
1446	19	34
1447	19	15
1448	19	33
1449	19	19
1450	19	8
1451	19	37
1452	19	22
1453	19	32
1454	19	10
1455	19	7
1456	19	31
1457	19	13
1458	20	29
1459	20	21
1460	20	16
1461	20	13
1462	20	19
1463	20	34
1464	20	17
1465	20	8
1466	20	35
1467	20	26
1468	20	20
1469	21	11
1470	21	21
1471	21	8
1472	21	19
1473	23	15
1474	23	14
1475	23	13
1476	23	34
1477	23	35
1478	24	11
1479	24	21
1480	24	16
1481	24	13
1482	24	17
1483	24	19
1484	24	29
1485	24	31
1486	24	22
1487	26	25
1488	26	26
1489	26	31
1490	26	32
1491	26	37
1492	26	13
1493	26	27
1494	26	16
1495	26	12
1496	26	24
1497	26	9
1498	26	14
1499	27	13
1500	27	14
1501	27	31
1502	27	12
1503	27	16
1504	27	19
1505	27	37
1506	27	28
1507	27	34
1508	27	26
1509	27	32
1510	27	29
1511	27	10
1512	27	35
1513	27	29
1514	27	7
1515	27	15
1516	27	8
1517	27	23
1518	28	22
1519	28	26
1520	28	7
1521	28	25
1522	28	24
1523	28	21
1524	28	32
1525	28	27
1526	28	16
1527	28	9
1528	28	13
1529	28	35
1530	28	36
1531	28	8
1532	28	29
1533	28	15
1534	28	34
1535	28	28
1536	28	20
1537	28	31
1538	28	18
1539	28	10
1540	29	36
1541	29	28
1542	29	14
1543	29	25
1544	29	20
1545	29	7
1546	29	27
1547	29	24
1548	29	15
1549	29	29
1550	29	21
1551	29	31
1552	29	33
1553	29	16
1554	29	23
1555	29	26
1556	29	22
1557	29	32
1558	29	18
1559	29	35
1560	29	8
1561	30	22
1562	30	9
1563	30	23
1564	30	17
1565	30	7
1566	30	11
1567	30	18
1568	30	24
1569	30	27
1570	30	19
1571	30	29
1572	32	23
1573	32	21
1574	32	10
1575	32	29
1576	32	29
1577	32	33
1578	32	11
1579	34	8
1580	34	25
1581	34	27
1582	34	19
1583	34	37
1584	34	12
1585	34	24
1586	34	21
1587	34	14
1588	34	29
1589	34	34
1590	34	31
1591	34	9
1592	34	13
1593	35	12
1594	35	9
1595	35	10
1596	35	24
1597	35	26
1598	35	17
1599	35	13
1600	35	8
1601	35	31
1602	35	19
1603	35	35
1604	35	7
1605	35	25
1606	35	14
1607	35	27
1608	36	22
1609	36	15
1610	36	35
1611	36	21
1612	36	7
1613	36	34
1614	36	36
1615	36	37
1616	36	14
1617	36	17
1618	36	12
1619	36	23
1620	36	10
1621	36	8
1622	36	20
1623	36	11
1624	36	13
1625	36	29
1626	36	27
1627	36	26
1628	36	32
1629	36	28
1630	36	31
1631	36	24
1632	36	29
1633	39	37
1634	39	31
1635	39	28
1636	39	35
1637	39	23
1638	39	7
1639	39	16
1640	39	21
1641	39	9
1642	39	22
1643	39	15
1644	39	11
1645	39	17
1646	39	29
1647	39	29
1648	39	24
1649	39	32
1650	39	25
1651	40	36
1652	40	31
1653	40	37
1654	40	20
1655	40	29
1656	40	34
1657	40	23
1658	40	11
1659	41	8
1660	41	11
1661	41	12
1662	41	21
1663	41	16
1664	41	29
1665	41	22
1666	41	27
1667	41	23
1668	41	20
1669	41	7
1670	41	14
1671	41	31
1672	41	18
1673	41	28
1674	41	25
1675	41	37
1676	42	21
1677	42	32
1678	42	33
1679	42	17
1680	42	13
1681	42	15
1682	42	9
1683	42	37
1684	44	20
1685	44	18
1686	44	24
1687	44	7
1688	44	15
1689	44	32
1690	44	31
1691	44	19
1692	46	37
1693	46	31
1694	46	25
1695	46	10
1696	47	8
1697	47	33
1698	47	29
1699	47	14
1700	47	24
1701	47	22
1702	47	26
1703	47	7
1704	47	16
1705	47	15
1706	47	10
1707	47	11
1708	47	9
1709	47	37
1710	47	34
1711	47	29
1712	47	23
1713	47	21
1714	47	28
1715	47	27
1716	47	25
1717	47	36
1718	47	35
1719	47	20
1720	47	19
1721	47	32
1722	49	23
1723	49	11
1724	49	35
1725	49	16
1726	49	8
1727	49	22
1728	49	36
1729	49	10
1730	49	26
1731	49	7
1732	49	34
1733	49	31
1734	49	21
1735	49	19
1736	49	15
1737	49	18
1738	49	27
1739	49	9
1740	49	29
1741	49	29
1742	49	13
1743	49	17
1744	49	33
1745	49	20
1746	49	37
1747	50	34
1748	50	20
1749	50	19
1750	50	22
1751	50	21
1752	50	13
1753	50	9
1754	50	26
1755	50	35
1756	50	17
1757	50	32
1758	50	37
1759	50	15
1760	50	24
1761	50	18
1762	50	23
1763	50	25
1764	50	7
1765	50	33
1766	50	29
1767	50	10
1768	50	31
1769	50	14
1770	50	36
1771	50	28
1772	50	8
1773	50	27
1774	50	29
1775	50	16
1776	51	17
1777	51	35
1778	51	11
1779	51	37
1780	51	18
1781	51	16
1782	51	29
1783	51	13
1784	54	11
1785	54	24
1786	54	25
1787	54	31
1788	54	35
1789	54	10
1790	54	12
1791	54	22
1792	54	29
1793	54	23
1794	54	28
1795	54	19
1796	54	27
1797	54	32
1798	54	8
1799	54	14
1800	54	16
1801	55	34
1802	55	29
1803	55	13
1804	55	12
1805	55	9
1806	55	28
1807	55	37
1808	55	15
1809	55	33
1810	55	25
1811	55	7
1812	55	17
1813	55	10
1814	55	22
1815	55	29
1816	55	35
1817	55	32
1818	55	11
1819	55	21
1820	55	14
1821	55	26
1822	55	8
1823	55	31
1824	55	20
1825	56	17
1826	56	27
1827	56	21
1828	56	15
1829	56	32
1830	56	29
1831	56	19
1832	56	16
1833	56	22
1834	56	23
1835	56	13
1836	57	8
1837	57	33
1838	57	28
1839	57	9
1840	57	31
1841	57	17
1842	57	29
1843	57	23
1844	57	11
1845	57	21
1846	57	36
1847	57	13
1848	57	26
1849	57	32
1850	57	18
1851	57	22
1852	57	10
1853	57	20
1854	57	27
1855	57	16
1856	57	37
1857	57	29
1858	57	12
1859	57	14
1860	58	18
1861	58	9
1862	58	19
1863	58	33
1864	58	28
1865	58	23
1866	58	21
1867	58	36
1868	58	7
1869	58	20
1870	58	17
1871	58	32
1872	58	15
1873	58	14
1874	59	11
1875	59	24
1876	59	23
1877	59	22
1878	59	28
1879	59	26
1880	59	31
1881	59	37
1882	59	29
1883	59	9
1884	59	7
1885	59	17
1886	59	14
1887	59	20
1888	59	13
1889	59	35
1890	59	19
1891	59	10
1892	60	36
1893	60	29
1894	60	34
1895	60	19
1896	60	31
1897	60	26
1898	60	18
1899	60	21
1900	60	8
1901	60	7
1902	60	29
1903	60	9
1904	60	23
1905	60	13
1906	60	25
1907	60	20
1908	60	22
1909	60	33
1910	60	24
1911	60	35
1912	60	28
1913	60	17
1914	60	27
1915	60	32
1916	60	16
1917	60	14
1918	60	11
1919	61	36
1920	61	31
1921	61	16
1922	61	23
1923	61	24
1924	61	25
1925	61	13
1926	61	29
1927	61	26
1928	61	18
1929	61	12
1930	61	32
1931	61	14
1932	61	7
1933	61	15
1934	61	9
1935	61	37
1936	61	10
1937	62	9
1938	62	26
1939	62	18
1940	62	8
1941	62	14
1942	62	35
1943	62	17
1944	62	19
1945	62	11
1946	62	16
1947	62	34
1948	62	22
1949	62	15
1950	62	29
1951	62	7
1952	62	28
1953	62	23
1954	62	13
1955	62	12
1956	62	27
1957	62	31
1958	62	37
1959	62	33
1960	62	20
1961	62	25
1962	63	27
1963	63	10
1964	63	7
1965	63	12
1966	63	37
1967	63	16
1968	63	9
1969	63	26
1970	63	36
1971	63	8
1972	63	29
1973	63	28
1974	63	23
1975	63	19
1976	63	31
1977	63	13
1978	64	15
1979	64	32
1980	64	12
1981	64	29
1982	64	35
1983	64	13
1984	64	34
1985	64	21
1986	64	11
1987	64	28
1988	64	33
1989	65	15
1990	65	16
1991	65	28
1992	65	36
1993	65	24
1994	65	8
1995	65	32
1996	65	21
1997	65	26
1998	65	13
1999	65	37
2000	65	33
2001	65	29
2002	65	10
2003	65	22
2004	65	34
2005	65	35
2006	65	18
2007	65	20
2008	65	31
2009	65	12
2010	65	19
2011	65	17
2012	65	23
2013	66	19
2014	66	34
2015	66	27
2016	66	12
2017	66	20
2018	66	8
2019	66	28
2020	66	18
2021	66	21
2022	66	32
2023	66	31
2024	66	22
2025	66	29
2026	66	26
2027	66	25
2028	66	7
2029	66	17
2030	66	16
2031	66	24
2032	66	37
2033	66	23
2034	66	14
2035	66	13
2036	66	11
2037	66	9
2038	66	35
2039	67	13
2040	67	32
2041	67	21
2042	67	15
2043	67	25
2044	67	33
2045	67	10
2046	67	29
2047	67	28
2048	67	8
2049	67	37
2050	67	14
2051	67	18
2052	67	20
2053	67	31
2054	67	29
2055	67	22
2056	67	27
2057	67	23
2058	68	10
2059	68	22
2060	68	8
2061	68	17
2062	68	34
2063	68	25
2064	68	12
2065	68	7
2066	68	15
2067	68	28
2068	68	11
2069	68	31
2070	68	35
2071	68	32
2072	68	29
2073	68	37
2074	68	14
2075	68	13
2076	68	9
2077	68	21
2078	68	36
2079	68	29
2080	6	7
2081	6	16
2082	6	33
2083	6	17
2084	6	11
2085	6	8
2086	6	24
2087	6	37
2088	6	18
2089	6	22
2090	6	9
2091	6	35
2092	6	21
2093	6	28
2094	6	29
2095	6	12
2096	6	32
2097	6	20
2098	6	14
2099	7	23
2100	7	28
2101	7	29
2102	7	27
2103	7	36
2104	7	34
2105	7	37
2106	9	14
2107	9	10
2108	9	8
2109	9	20
2110	9	27
2111	9	13
2112	9	7
2113	9	35
2114	9	17
2115	9	16
2116	9	34
2117	9	33
2118	13	8
2119	13	7
2120	13	14
2121	13	33
2122	13	31
2123	14	7
2124	14	34
2125	14	11
2126	14	13
2127	14	22
2128	14	12
2129	14	21
2130	18	31
2131	18	20
2132	18	29
2133	18	13
2134	18	10
2135	18	9
2136	18	29
2137	18	37
2138	18	24
2139	18	35
2140	18	12
2141	18	36
2142	18	16
2143	18	26
2144	18	14
2145	18	23
2146	18	18
2147	18	22
2148	18	19
2149	18	28
2150	22	21
2151	22	20
2152	22	11
2153	22	31
2154	22	27
2155	22	33
2156	22	34
2157	22	37
2158	22	13
2159	25	25
2160	25	23
2161	25	9
2162	25	12
2163	25	19
2164	25	13
2165	25	17
2166	25	29
2167	25	37
2168	25	8
2169	25	22
2170	25	10
2171	25	29
2172	25	24
2173	25	33
2174	25	32
2175	25	16
2176	25	14
2177	25	26
2178	31	9
2179	31	7
2180	31	14
2181	31	34
2182	31	27
2183	31	13
2184	31	35
2185	31	28
2186	31	21
2187	31	17
2188	31	33
2189	31	32
2190	31	18
2191	31	25
2192	31	36
2193	33	28
2194	33	14
2195	33	25
2196	33	13
2197	33	7
2198	33	34
2199	33	19
2200	33	12
2201	33	22
2202	33	9
2203	33	16
2204	33	20
2205	33	18
2206	33	24
2207	33	21
2208	33	26
2209	33	17
2210	33	29
2211	33	29
2212	33	37
2213	33	23
2214	33	10
2215	33	15
2216	33	11
2217	33	35
2218	33	31
2219	33	33
2220	37	21
2221	37	11
2222	37	33
2223	37	8
2224	37	27
2225	37	22
2226	37	34
2227	37	16
2228	37	23
2229	37	29
2230	37	7
2231	37	9
2232	37	25
2233	37	28
2234	37	36
2235	37	17
2236	37	13
2237	37	37
2238	37	20
2239	38	14
2240	38	15
2241	38	25
2242	38	35
2243	38	29
2244	38	22
2245	38	12
2246	38	11
2247	43	8
2248	43	29
2249	43	24
2250	43	10
2251	43	26
2252	43	25
2253	43	33
2254	43	14
2255	43	35
2256	43	31
2257	43	28
2258	43	18
2259	43	9
2260	43	17
2261	43	23
2262	43	34
2263	45	32
2264	45	29
2265	45	12
2266	45	24
2267	45	23
2268	45	7
2269	45	18
2270	45	26
2271	48	35
2272	48	9
2273	48	21
2274	48	22
2275	48	34
2276	48	8
2277	48	15
2278	48	25
2279	48	14
2280	48	10
2281	48	26
2282	48	17
2283	48	37
2284	48	31
2285	48	23
2286	48	32
2287	48	7
2288	48	27
2289	48	16
2290	48	12
2291	52	21
2292	52	16
2293	52	35
2294	52	37
2295	52	10
2296	52	32
2297	52	15
2298	52	26
2299	52	24
2300	52	9
2301	52	23
2302	53	33
2303	53	22
2304	53	26
2305	53	36
2306	53	8
2307	53	17
2308	53	25
2309	53	16
2310	53	12
2311	53	7
2312	53	10
2313	53	34
2314	53	20
2315	53	32
2316	53	15
2317	53	24
2318	53	35
2319	53	11
2320	53	14
2321	53	23
2322	69	35
2323	69	29
2324	69	19
2325	69	7
2326	69	33
\.


--
-- Name: seen_arguments_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('seen_arguments_uid_seq', 2326, true);


--
-- Data for Name: seen_statements; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY seen_statements (uid, statement_uid, user_uid) FROM stdin;
1519	1	8
1520	1	27
1521	1	24
1522	1	20
1523	1	13
1524	1	33
1525	1	17
1526	1	29
1527	1	15
1528	1	21
1529	1	9
1530	1	18
1531	1	23
1532	2	14
1533	2	26
1534	2	15
1535	2	28
1536	2	25
1537	2	36
1538	2	9
1539	2	37
1540	2	16
1541	2	13
1542	2	19
1543	2	17
1544	2	24
1545	2	12
1546	2	23
1547	2	10
1548	2	7
1549	2	8
1550	2	29
1551	2	32
1552	2	21
1553	2	18
1554	2	33
1555	3	29
1556	3	19
1557	3	12
1558	3	35
1559	3	10
1560	3	21
1561	3	11
1562	3	27
1563	3	28
1564	3	29
1565	4	26
1566	4	22
1567	4	8
1568	4	25
1569	4	33
1570	4	24
1571	4	28
1572	4	34
1573	4	35
1574	4	31
1575	4	29
1576	4	36
1577	4	15
1578	4	23
1579	4	7
1580	4	19
1581	4	18
1582	4	16
1583	4	9
1584	4	29
1585	4	10
1586	4	17
1587	4	21
1588	4	12
1589	4	20
1590	4	14
1591	5	7
1592	5	37
1593	5	28
1594	5	29
1595	5	21
1596	5	9
1597	5	33
1598	5	35
1599	5	27
1600	5	13
1601	5	26
1602	5	29
1603	6	33
1604	6	28
1605	6	25
1606	6	9
1607	6	34
1608	6	27
1609	6	11
1610	6	8
1611	6	24
1612	7	31
1613	7	27
1614	7	11
1615	7	16
1616	7	9
1617	7	10
1618	7	13
1619	7	33
1620	7	25
1621	8	31
1622	8	21
1623	8	34
1624	8	29
1625	8	32
1626	8	22
1627	8	10
1628	8	9
1629	8	12
1630	8	8
1631	8	36
1632	8	25
1633	8	17
1634	8	7
1635	8	20
1636	8	15
1637	8	16
1638	8	29
1639	8	26
1640	8	28
1641	8	13
1642	8	27
1643	9	10
1644	9	24
1645	9	31
1646	9	33
1647	9	19
1648	9	20
1649	9	25
1650	9	35
1651	9	9
1652	9	15
1653	9	32
1654	9	27
1655	9	34
1656	9	18
1657	10	7
1658	10	15
1659	10	11
1660	10	33
1661	10	24
1662	10	20
1663	10	29
1664	10	28
1665	10	26
1666	10	22
1667	10	36
1668	10	10
1669	10	14
1670	10	21
1671	10	19
1672	10	25
1673	10	16
1674	10	9
1675	11	10
1676	11	28
1677	11	20
1678	11	29
1679	11	22
1680	11	9
1681	11	24
1682	12	19
1683	12	27
1684	12	28
1685	12	16
1686	12	15
1687	12	18
1688	12	13
1689	12	35
1690	12	21
1691	12	32
1692	12	14
1693	12	23
1694	12	24
1695	12	22
1696	12	10
1697	12	29
1698	12	26
1699	12	17
1700	12	34
1701	12	12
1702	12	36
1703	12	9
1704	12	29
1705	12	8
1706	12	7
1707	13	9
1708	13	23
1709	13	36
1710	13	7
1711	13	19
1712	13	18
1713	13	29
1714	13	21
1715	13	14
1716	13	32
1717	13	27
1718	13	33
1719	14	15
1720	14	10
1721	14	33
1722	14	36
1723	14	14
1724	15	7
1725	15	17
1726	15	35
1727	15	26
1728	15	14
1729	16	22
1730	16	28
1731	16	34
1732	16	20
1733	17	14
1734	17	12
1735	17	35
1736	17	28
1737	17	24
1738	17	25
1739	17	10
1740	17	18
1741	18	31
1742	18	23
1743	18	27
1744	18	29
1745	18	36
1746	18	26
1747	18	13
1748	18	19
1749	18	14
1750	18	9
1751	18	28
1752	18	17
1753	18	29
1754	18	15
1755	18	34
1756	18	20
1757	18	12
1758	18	21
1759	19	15
1760	19	37
1761	19	18
1762	19	21
1763	19	16
1764	19	22
1765	19	9
1766	19	7
1767	19	33
1768	19	20
1769	19	31
1770	19	14
1771	19	34
1772	19	10
1773	19	29
1774	19	28
1775	19	12
1776	19	17
1777	19	24
1778	19	13
1779	19	8
1780	19	32
1781	19	26
1782	19	25
1783	19	29
1784	19	27
1785	19	19
1786	19	36
1787	20	28
1788	20	10
1789	20	21
1790	20	36
1791	20	26
1792	20	19
1793	20	34
1794	20	13
1795	20	15
1796	20	32
1797	20	12
1798	20	27
1799	20	23
1800	20	7
1801	20	29
1802	20	17
1803	20	33
1804	20	29
1805	20	8
1806	20	20
1807	20	9
1808	20	22
1809	20	31
1810	20	14
1811	20	18
1812	20	25
1813	21	22
1814	21	32
1815	21	33
1816	21	36
1817	21	37
1818	21	27
1819	21	17
1820	21	8
1821	21	24
1822	21	18
1823	21	29
1824	21	25
1825	21	15
1826	21	21
1827	21	29
1828	22	20
1829	22	21
1830	22	36
1831	22	27
1832	22	26
1833	22	37
1834	22	34
1835	22	29
1836	22	31
1837	23	33
1838	23	35
1839	23	34
1840	23	37
1841	23	24
1842	23	15
1843	23	23
1844	23	20
1845	23	31
1846	23	27
1847	23	22
1848	23	10
1849	24	19
1850	24	18
1851	24	14
1852	24	32
1853	24	28
1854	24	8
1855	24	26
1856	24	37
1857	24	11
1858	24	15
1859	24	24
1860	24	31
1861	24	7
1862	24	21
1863	24	33
1864	24	12
1865	24	9
1866	24	25
1867	24	13
1868	24	16
1869	24	29
1870	24	20
1871	24	10
1872	24	36
1873	24	22
1874	24	17
1875	24	29
1876	24	23
1877	25	14
1878	25	21
1879	25	19
1880	25	29
1881	25	36
1882	25	31
1883	25	8
1884	25	10
1885	25	32
1886	25	17
1887	25	33
1888	25	26
1889	25	27
1890	25	18
1891	25	11
1892	25	28
1893	25	23
1894	25	16
1895	25	12
1896	25	7
1897	25	13
1898	25	35
1899	25	15
1900	26	35
1901	26	10
1902	26	14
1903	26	23
1904	26	16
1905	26	28
1906	26	7
1907	26	9
1908	26	29
1909	26	34
1910	26	25
1911	26	24
1912	26	37
1913	26	8
1914	26	33
1915	26	22
1916	26	31
1917	26	19
1918	26	12
1919	26	18
1920	26	17
1921	26	26
1922	26	27
1923	26	13
1924	26	29
1925	27	34
1926	27	20
1927	27	15
1928	27	21
1929	27	31
1930	27	25
1931	27	35
1932	27	8
1933	27	36
1934	27	29
1935	27	37
1936	27	18
1937	27	12
1938	27	7
1939	27	17
1940	27	16
1941	27	32
1942	28	31
1943	28	17
1944	28	18
1945	28	15
1946	28	12
1947	28	9
1948	28	25
1949	28	16
1950	28	28
1951	28	23
1952	28	29
1953	28	13
1954	28	26
1955	28	24
1956	28	8
1957	28	27
1958	28	7
1959	28	36
1960	29	8
1961	29	35
1962	29	20
1963	29	15
1964	30	10
1965	30	13
1966	30	14
1967	30	32
1968	30	35
1969	30	19
1970	30	23
1971	30	24
1972	30	29
1973	30	20
1974	30	8
1975	30	34
1976	30	33
1977	30	37
1978	30	16
1979	30	21
1980	30	11
1981	30	12
1982	30	26
1983	30	22
1984	30	27
1985	30	18
1986	30	9
1987	30	31
1988	30	36
1989	30	25
1990	31	36
1991	31	17
1992	31	13
1993	31	18
1994	31	8
1995	31	26
1996	32	26
1997	32	37
1998	32	17
1999	32	20
2000	32	9
2001	32	32
2002	32	36
2003	32	23
2004	32	18
2005	32	21
2006	32	15
2007	32	22
2008	32	13
2009	32	7
2010	32	34
2011	33	19
2012	33	21
2013	33	13
2014	33	29
2015	33	28
2016	33	16
2017	34	9
2018	34	22
2019	34	13
2020	34	16
2021	34	8
2022	34	33
2023	34	32
2024	34	14
2025	34	35
2026	34	26
2027	34	12
2028	34	19
2029	34	34
2030	34	37
2031	34	17
2032	34	10
2033	34	27
2034	34	28
2035	34	21
2036	34	20
2037	34	29
2038	34	31
2039	34	7
2040	34	36
2041	34	25
2042	35	16
2043	35	28
2044	35	31
2045	35	33
2046	35	26
2047	35	9
2048	35	7
2049	35	13
2050	35	10
2051	35	17
2052	35	24
2053	35	27
2054	35	29
2055	35	8
2056	35	11
2057	35	22
2058	35	34
2059	35	25
2060	35	15
2061	35	21
2062	35	23
2063	35	32
2064	35	37
2065	35	35
2066	35	29
2067	35	12
2068	35	18
2069	35	19
2070	35	36
2071	36	28
2072	36	36
2073	36	27
2074	36	13
2075	36	22
2076	36	24
2077	36	25
2078	36	8
2079	36	16
2080	36	26
2081	36	23
2082	36	14
2083	36	34
2084	36	9
2085	36	31
2086	36	12
2087	36	17
2088	36	20
2089	37	15
2090	37	20
2091	37	13
2092	37	11
2093	37	12
2094	37	8
2095	37	27
2096	37	35
2097	37	16
2098	37	29
2099	37	17
2100	37	19
2101	38	11
2102	38	9
2103	38	18
2104	38	33
2105	38	14
2106	38	26
2107	38	16
2108	38	20
2109	38	35
2110	38	31
2111	38	17
2112	38	12
2113	38	34
2114	38	36
2115	38	32
2116	38	7
2117	38	37
2118	38	10
2119	38	28
2120	38	24
2121	38	29
2122	38	13
2123	38	8
2124	38	21
2125	38	22
2126	38	25
2127	38	29
2128	38	19
2129	38	15
2130	39	28
2131	39	9
2132	39	25
2133	39	23
2134	39	19
2135	39	36
2136	39	15
2137	39	26
2138	39	32
2139	39	34
2140	39	16
2141	39	17
2142	39	7
2143	39	14
2144	39	35
2145	39	22
2146	39	20
2147	39	27
2148	40	22
2149	40	11
2150	40	28
2151	40	29
2152	40	33
2153	40	19
2154	40	16
2155	40	12
2156	40	27
2157	40	8
2158	40	36
2159	40	7
2160	40	9
2161	40	10
2162	40	32
2163	40	29
2164	40	35
2165	40	34
2166	40	13
2167	40	37
2168	40	24
2169	41	29
2170	41	22
2171	41	16
2172	41	12
2173	41	23
2174	41	29
2175	41	36
2176	41	24
2177	41	17
2178	41	11
2179	41	13
2180	41	35
2181	41	9
2182	41	15
2183	41	21
2184	41	28
2185	42	20
2186	42	36
2187	42	23
2188	42	8
2189	42	15
2190	42	25
2191	42	12
2192	42	22
2193	42	14
2194	42	21
2195	42	29
2196	42	13
2197	43	22
2198	43	14
2199	43	29
2200	43	37
2201	43	13
2202	43	23
2203	43	16
2204	43	17
2205	43	8
2206	44	16
2207	44	8
2208	44	32
2209	44	34
2210	44	18
2211	44	35
2212	44	10
2213	44	17
2214	44	20
2215	44	13
2216	44	12
2217	44	7
2218	44	27
2219	44	22
2220	44	21
2221	44	25
2222	44	23
2223	44	15
2224	44	36
2225	44	9
2226	44	31
2227	44	26
2228	44	28
2229	45	29
2230	45	37
2231	45	16
2232	45	19
2233	45	13
2234	45	25
2235	45	31
2236	45	27
2237	45	9
2238	45	32
2239	45	33
2240	45	23
2241	45	11
2242	45	26
2243	46	26
2244	46	20
2245	46	7
2246	46	13
2247	46	27
2248	47	27
2249	47	28
2250	47	15
2251	47	18
2252	47	8
2253	47	20
2254	47	10
2255	47	11
2256	47	9
2257	47	14
2258	47	37
2259	47	35
2260	47	26
2261	47	12
2262	47	36
2263	47	16
2264	47	23
2265	47	34
2266	48	18
2267	48	35
2268	48	15
2269	48	12
2270	48	32
2271	48	11
2272	48	25
2273	48	13
2274	48	26
2275	48	8
2276	49	24
2277	49	21
2278	49	7
2279	49	22
2280	49	14
2281	49	17
2282	49	29
2283	49	11
2284	49	37
2285	49	29
2286	49	23
2287	49	8
2288	49	33
2289	49	31
2290	49	18
2291	49	26
2292	49	35
2293	49	15
2294	49	10
2295	49	20
2296	49	36
2297	49	12
2298	49	19
2299	50	7
2300	50	26
2301	50	22
2302	50	10
2303	50	19
2304	50	33
2305	50	20
2306	50	18
2307	50	15
2308	50	8
2309	50	24
2310	50	16
2311	50	36
2312	50	25
2313	50	32
2314	50	35
2315	50	9
2316	50	37
2317	50	12
2318	50	21
2319	50	23
2320	50	28
2321	51	32
2322	51	15
2323	51	16
2324	51	35
2325	51	13
2326	51	31
2327	52	29
2328	52	36
2329	52	31
2330	52	11
2331	52	34
2332	52	22
2333	52	16
2334	52	28
2335	52	9
2336	52	15
2337	53	8
2338	53	11
2339	53	9
2340	53	13
2341	53	21
2342	53	7
2343	53	26
2344	53	17
2345	53	33
2346	53	37
2347	54	26
2348	54	15
2349	54	24
2350	54	12
2351	54	7
2352	54	9
2353	54	29
2354	54	18
2355	55	21
2356	55	12
2357	55	10
2358	55	35
2359	55	31
2360	56	26
2361	56	11
2362	56	21
2363	56	19
2364	56	37
2365	56	33
2366	56	23
2367	56	12
2368	56	22
2369	56	36
2370	56	29
2371	56	28
2372	56	10
2373	56	27
2374	56	34
2375	56	14
2376	56	7
2377	56	17
2378	56	16
2379	56	31
2380	56	25
2381	56	15
2382	56	20
2383	56	8
2384	56	29
2385	56	13
2386	56	35
2387	56	9
2388	57	27
2389	57	20
2390	57	36
2391	57	7
2392	57	32
2393	57	13
2394	57	22
2395	57	16
2396	57	29
2397	57	8
2398	58	12
2399	58	29
2400	58	16
2401	58	20
2402	58	17
2403	58	37
2404	58	27
2405	59	35
2406	59	34
2407	59	33
2408	59	20
2409	59	37
2410	59	29
2411	59	27
2412	59	10
2413	59	28
2414	59	19
2415	59	18
2416	59	17
2417	59	32
2418	59	21
2419	59	13
2420	59	11
2421	59	7
2422	59	29
2423	59	9
2424	59	16
2425	60	7
2426	60	19
2427	60	29
2428	60	18
2429	60	15
2430	60	16
2431	60	10
2432	60	37
2433	60	35
2434	60	11
2435	60	20
2436	60	34
2437	60	23
2438	60	24
2439	60	33
2440	60	9
2441	60	27
2442	60	36
2443	60	8
2444	60	29
2445	60	32
2446	60	12
2447	60	26
2448	61	9
2449	61	8
2450	61	23
2451	61	21
2452	61	28
2453	61	14
2454	61	11
2455	61	19
2456	61	29
2457	61	29
2458	61	25
2459	61	36
2460	61	32
2461	61	37
2462	61	7
2463	61	17
2464	61	20
2465	61	18
2466	62	20
2467	62	28
2468	62	7
2469	62	32
2470	62	27
2471	62	12
2472	62	14
2473	62	23
2474	62	17
2475	62	26
2476	62	10
2477	62	13
2478	62	16
2479	62	11
2480	62	15
2481	63	29
2482	63	17
2483	63	9
2484	63	19
2485	63	20
2486	63	18
2487	63	33
2488	63	31
2489	63	22
2490	64	11
2491	64	18
2492	64	27
2493	64	36
2494	64	23
2495	64	34
2496	64	28
2497	64	37
2498	64	26
2499	64	31
2500	64	35
2501	64	20
2502	64	7
2503	64	24
2504	64	25
2505	64	13
2506	64	21
2507	64	16
2508	65	12
2509	65	11
2510	65	18
2511	65	17
2512	65	20
2513	65	29
2514	65	37
2515	65	33
2516	66	21
2517	66	8
2518	66	13
2519	66	25
2520	66	7
2521	66	9
2522	67	7
2523	67	14
2524	67	9
2525	67	25
2526	68	10
2527	68	15
2528	68	14
2529	68	24
2530	68	31
2531	68	25
2532	68	11
2533	68	29
2534	68	7
2535	68	22
2536	69	23
2537	69	21
2538	69	27
2539	69	18
2540	69	36
2541	69	26
2542	69	37
2543	69	9
2544	69	7
2545	69	14
2546	69	12
2547	69	11
2548	69	33
2549	69	29
2550	69	16
2551	69	35
2552	69	31
2553	69	29
2554	69	34
2555	69	17
2556	69	28
2557	69	19
2558	69	22
2559	69	10
2560	69	15
2561	70	35
2562	70	19
2563	70	21
2564	70	20
2565	70	11
2566	70	14
2567	70	22
2568	71	16
2569	71	14
2570	71	23
2571	71	11
2572	71	7
2573	71	31
2574	71	8
2575	71	21
2576	71	27
2577	71	32
2578	71	22
2579	71	19
2580	71	33
2581	71	25
2582	71	15
2583	71	34
2584	71	29
2585	71	37
2586	71	10
2587	71	35
2588	71	13
2589	71	28
2590	71	26
2591	71	36
2592	71	12
2593	71	29
2594	72	36
2595	72	22
2596	72	35
2597	72	9
2598	72	11
2599	72	19
2600	72	12
2601	72	16
2602	72	23
2603	72	29
2604	72	18
2605	72	24
2606	72	10
2607	72	34
2608	72	28
2609	72	14
2610	72	17
2611	72	27
2612	72	26
2613	72	25
2614	72	31
2615	72	20
2616	72	15
2617	72	13
2618	72	32
2619	72	21
2620	72	8
2621	72	33
2622	72	7
2623	73	37
2624	73	8
2625	73	34
2626	73	24
2627	73	18
2628	73	10
2629	73	15
2630	73	32
2631	73	19
2632	73	28
2633	73	17
2634	73	12
2635	73	9
2636	73	21
2637	73	22
2638	73	29
2639	73	36
2640	73	31
2641	73	7
2642	73	11
2643	73	27
2644	73	35
2645	74	26
2646	74	29
2647	74	19
2648	74	35
2649	74	21
2650	74	7
2651	74	10
2652	74	27
2653	74	13
2654	74	29
2655	74	16
2656	74	8
2657	74	17
2658	74	34
2659	74	37
2660	74	18
2661	74	14
2662	74	15
2663	74	9
2664	74	28
2665	75	37
2666	75	13
2667	75	25
2668	75	8
2669	75	19
2670	75	29
2671	75	12
2672	75	35
2673	76	29
2674	76	10
2675	76	25
2676	76	37
2677	76	19
2678	76	35
2679	76	24
2680	76	7
2681	76	34
2682	76	15
2683	76	31
2684	76	18
2685	76	17
2686	76	9
2687	76	8
2688	76	16
2689	77	29
2690	77	26
2691	77	29
2692	77	9
2693	77	21
2694	77	34
2695	78	35
2696	78	29
2697	78	24
2698	78	16
2699	79	19
2700	79	20
2701	79	8
2702	79	37
2703	79	16
2704	79	12
2705	79	11
2706	79	10
2707	79	29
2708	79	35
2709	79	21
2710	79	24
2711	79	7
2712	79	28
2713	79	27
2714	79	23
2715	79	32
2716	79	25
2717	79	22
2718	79	33
2719	79	15
2720	79	17
2721	79	18
2722	79	29
2723	79	34
2724	79	9
2725	80	27
2726	80	12
2727	80	33
2728	80	18
2729	80	21
2730	80	34
2731	80	19
2732	80	8
2733	80	23
2734	80	26
2735	80	17
2736	80	9
2737	81	16
2738	81	22
2739	81	11
2740	81	24
2741	81	12
2742	81	36
2743	81	35
2744	81	32
2745	81	37
2746	81	21
2747	81	8
2748	81	18
2749	81	25
2750	81	23
2751	81	9
2752	81	29
2753	81	15
2754	81	14
2755	81	27
2756	81	7
2757	81	34
2758	81	33
2759	81	10
2760	82	31
2761	82	20
2762	82	29
2763	82	17
2764	82	18
2765	82	36
2766	82	14
2767	82	32
2768	82	37
2769	82	21
2770	82	33
2771	82	22
2772	82	27
2773	82	8
2774	82	12
2775	82	10
2776	82	11
2777	82	19
2778	82	15
2779	82	25
2780	82	16
2781	82	24
2782	82	26
2783	82	35
2784	82	9
\.


--
-- Name: seen_statements_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('seen_statements_uid_seq', 2784, true);


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
1	Ein Radar überwacht den Abstand, eine Frontkamera erkennt Fahrspuren und andere Verkehrsteilnehmer, und je sechs Ultraschallsensoren vorne und hinten helfen beim Einparken und messen während der Fahrt Distanzen im Zentimeterbereich	localhost:3449	/devcards/index.html	5	68	4	2017-08-17 08:18:19.463757
2	Zunächst einmal unterscheidet sich die Hardware für den Autopiloten nicht oder nur marginal von dem, was selbst für einen VW Polo erhältlich ist	localhost:3449	/	5	68	4	2017-08-17 08:18:19.463757
3	Katzen sind kleine Tiger	http://www.iflscience.com/	plants-and-animals/no-your-cat-isnt-plotting-kill-youbut-it-has-lions-personality/	2	15	2	2017-08-17 08:18:19.463757
4	Katzen sind kleine Tiger	http://www.iflscience.com/	plants-and-animals/no-your-cat-isnt-plotting-kill-youbut-it-has-lions-personality/	2	16	2	2017-08-17 08:18:19.463757
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
1	2	we should get a cat	1	2017-07-28 08:18:20.23062	f
2	3	we should get a dog	1	2017-08-10 08:18:20.230724	f
3	4	we could get both, a cat and a dog	1	2017-08-15 08:18:20.230771	f
4	5	cats are very independent	1	2017-08-14 08:18:20.230811	f
5	6	cats are capricious	1	2017-08-15 08:18:20.230847	f
6	7	dogs can act as watch dogs	1	2017-08-15 08:18:20.230882	f
7	8	you have to take the dog for a walk every day, which is tedious	1	2017-07-29 08:18:20.230917	f
8	9	we have no use for a watch dog	1	2017-08-10 08:18:20.230951	f
9	10	going for a walk with the dog every day is good for social interaction and physical exercise	1	2017-07-29 08:18:20.230985	f
10	11	it would be no problem	1	2017-08-17 08:18:20.231019	f
11	12	a cat and a dog will generally not get along well	1	2017-08-08 08:18:20.231053	f
12	13	we do not have enough money for two pets	1	2017-07-31 08:18:20.231087	f
13	14	a dog costs taxes and will be more expensive than a cat	1	2017-07-28 08:18:20.231121	f
14	15	cats are fluffy	1	2017-07-29 08:18:20.231173	f
15	16	cats are small	1	2017-08-12 08:18:20.23121	f
16	17	fluffy animals losing much hair and I'm allergic to animal hair	1	2017-07-25 08:18:20.231244	f
17	18	you could use a automatic vacuum cleaner	1	2017-08-09 08:18:20.231277	f
18	19	cats ancestors are animals in wildlife, who are hunting alone and not in groups	1	2017-07-31 08:18:20.231311	f
19	20	this is not true for overbred races	1	2017-07-31 08:18:20.231345	f
20	21	this lies in their the natural conditions	1	2017-08-02 08:18:20.231378	f
21	22	the purpose of a pet is to have something to take care of	1	2017-07-27 08:18:20.231411	f
22	23	several cats of friends of mine are real as*holes	1	2017-07-28 08:18:20.231445	f
23	24	the fact, that cats are capricious, is based on the cats race	1	2017-08-17 08:18:20.231479	f
24	25	not every cat is capricious	1	2017-08-01 08:18:20.231513	f
25	26	this is based on the cats race and a little bit on the breeding	1	2017-08-01 08:18:20.231546	f
26	27	next to the taxes you will need equipment like a dog lead, anti-flea-spray, and so on	1	2017-08-08 08:18:20.23158	f
27	28	the equipment for running costs of cats and dogs are nearly the same	1	2017-08-01 08:18:20.231613	f
28	29	this is just a claim without any justification	1	2017-07-30 08:18:20.231646	f
29	30	in Germany you have to pay for your second dog even more taxes!	1	2017-08-16 08:18:20.231679	f
30	31	it is important, that pets are small and fluffy!	1	2017-08-02 08:18:20.231713	f
31	32	cats are little, sweet and innocent cuddle toys	1	2017-07-27 08:18:20.231746	f
32	33	do you have ever seen a sphinx cat or savannah cats?	1	2017-07-27 08:18:20.23178	f
33	34	it is much work to take care of both animals	1	2017-07-25 08:18:20.231813	f
34	35	won't be best friends	1	2017-08-12 08:18:20.231846	f
35	36	the city should reduce the number of street festivals	3	2017-08-09 08:18:20.231879	f
36	37	we should shut down University Park	3	2017-08-05 08:18:20.231912	f
37	38	we should close public swimming pools	1	2017-08-17 08:18:20.231946	f
38	39	reducing the number of street festivals can save up to $50.000 a year	1	2017-08-13 08:18:20.231979	f
39	40	every street festival is funded by large companies	1	2017-07-31 08:18:20.232033	f
40	41	then we will have more money to expand out pedestrian zone	1	2017-08-15 08:18:20.232071	f
41	42	our city will get more attractive for shopping	1	2017-08-17 08:18:20.232105	f
42	43	street festivals attract many people, which will increase the citys income	1	2017-07-29 08:18:20.232138	f
43	44	spending of the city for these festivals are higher than the earnings	1	2017-07-26 08:18:20.232172	f
44	45	money does not solve problems of our society	1	2017-07-24 08:18:20.232205	f
45	46	criminals use University Park to sell drugs	1	2017-08-02 08:18:20.232238	f
46	47	shutting down University Park will save $100.000 a year	1	2017-08-03 08:18:20.232271	f
47	48	we should not give in to criminals	1	2017-08-06 08:18:20.232305	f
48	49	the number of police patrols has been increased recently	1	2017-08-11 08:18:20.232338	f
49	50	this is the only park in our city	1	2017-08-11 08:18:20.232372	f
50	51	there are many parks in neighbouring towns	1	2017-08-17 08:18:20.232406	f
51	52	the city is planing a new park in the upcoming month	3	2017-08-06 08:18:20.232439	f
52	53	parks are very important for our climate	3	2017-08-01 08:18:20.232473	f
53	54	our swimming pools are very old and it would take a major investment to repair them	3	2017-08-14 08:18:20.232506	f
54	55	schools need the swimming pools for their sports lessons	1	2017-07-24 08:18:20.23254	f
55	56	the rate of non-swimmers is too high	1	2017-08-17 08:18:20.232573	f
56	57	the police cannot patrol in the park for 24/7	1	2017-08-17 08:18:20.232606	f
57	58	E-Autos "optimal" für den Stadtverkehr sind	1	2017-07-25 08:18:20.232639	f
58	59	dadurch die Lärmbelästigung in der Stadt sinkt	1	2017-08-01 08:18:20.232672	f
77	77	Straßenfeste viel Lärm verursachen	1	2017-08-06 08:18:20.233306	f
59	60	die Anzahl an Ladestationen in der Stadt nicht ausreichend ist	1	2017-08-05 08:18:20.232706	f
60	61	das Unfallrisiko steigt, da die Autos kaum Geräusche verursachen	1	2017-08-01 08:18:20.232739	f
61	62	die Autos auch zuhause geladen werden können und das pro Tag ausreichen sollte	1	2017-08-07 08:18:20.232772	f
62	63	Elektroautos keine lauten Geräusche beim Anfahren produzieren	1	2017-08-17 08:18:20.232805	f
63	64	Lärmbelästigung kein wirkliches Problem in den Städten ist	1	2017-08-16 08:18:20.232839	f
64	65	nicht jede normale Tankstelle auch Stromtankstellen hat	1	2017-08-08 08:18:20.232872	f
65	66	die Länder und Kommunen den Ausbau nun stark fördern wollen	1	2017-08-04 08:18:20.232905	f
66	67	E-Autos das autonome Fahren vorantreiben	5	2017-08-14 08:18:20.232938	f
67	68	Tesla mutig bestehende Techniken einsetzt und zeigt was sie können	5	2017-07-24 08:18:20.232972	f
68	69	durch rücksichtsvolle Verhaltensanpassungen der wissenschaftlichen Mitarbeitenden der Arbeitsaufwand der Sekretärinnen gesenkt werden könnte	1	2017-07-25 08:18:20.233005	f
69	70	wir Standard-Formulare, wie Urlaubsanträge, selbst faxen können	1	2017-07-28 08:18:20.233039	f
70	71	etliche Abläufe durch ein besseres Zusammenarbeiten optimiert werden können. Dies sollte auch schriftlich als Anleitungen festgehalten werden, damit neue Angestellt einen leichten Einstieg finden	1	2017-08-16 08:18:20.233072	f
71	72	viele Arbeiten auch durch die Mitarbeiter erledigt werden können	1	2017-08-11 08:18:20.233105	f
72	73	"rücksichtsvolle Verhaltensanpassungen" viel zu allgemein gehalten ist	1	2017-08-08 08:18:20.233139	f
73	74	das Faxgerät nicht immer zugänglich ist, wenn die Sekretärinnen nicht anwesend sind	1	2017-08-06 08:18:20.233172	f
74	75	wir keine eigenen Faxgeräte haben und so oder so entweder bei Martin stören müssten oder doch bei Sabine im Büro landen würden	1	2017-08-03 08:18:20.233205	f
75	1	Cats are fucking stupid and bloody fuzzy critters!	1	2017-08-11 08:18:20.233238	f
76	76	Die Anzahl der Straßenfeste sollte reduziert werden	1	2017-08-13 08:18:20.233272	f
78	78	Straßenfeste ein wichtiger Bestandteil unserer Kultur sind	1	2017-08-02 08:18:20.233339	f
79	79	Straßenfeste der Kommune Geld einbringen	1	2017-08-09 08:18:20.233372	f
80	80	die Einnahmen der Kommune durch Straßenfeste nur gering sind	1	2017-08-13 08:18:20.233405	f
81	81	Straßenfeste der Kommune hohe Kosten verursachen durch Polizeieinsätze, Säuberung, etc.	1	2017-08-07 08:18:20.233438	f
82	82	die Innenstadt ohnehin sehr laut ist	1	2017-07-24 08:18:20.233471	f
\.


--
-- Name: textversions_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('textversions_uid_seq', 82, true);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY users (uid, firstname, surname, nickname, public_nickname, email, gender, password, group_uid, last_action, last_login, registered, token, token_timestamp) FROM stdin;
1	anonymous	anonymous	anonymous	anonymous		m	$2a$10$yRuHZQMWGpJ68OTjPAGOm.fOQrzvvT08eqA8FjrqyQ.WqatRplK3u	3	2017-08-17 08:18:20.045038	2017-08-17 08:18:20.045164	2017-08-17 08:18:20.045219		\N
2	Tobias	Krauthoff	Tobias	Tobias	krauthoff@cs.uni-duesseldorf.de	m	$2a$10$9P5biPvyX2xVeMcCLm82tO0XFQhmdMFwgAhPaUkCHoVL1F5kEAjIa	1	2017-08-17 08:18:20.045317	2017-08-17 08:18:20.045368	2017-08-17 08:18:20.045421		\N
3	Christian	Meter	Christian	Christian	meter@cs.uni-duesseldorf.de	m	$2a$10$Ou/pHV1MoZRqvt5U8cV09up0qqbIz70ZjwEeanRkyyfR/rrMHcBfe	1	2017-08-17 08:18:20.045504	2017-08-17 08:18:20.045551	2017-08-17 08:18:20.045596		\N
4	Björn	Ebbinghaus	Björn	Björn	bjoern.ebbinghaus@uni-duesseldorf.de	m	$2a$10$LJFrjOh0FF0ppZpFYMyFweGfFMlFKONPVpNjoLBHxqsxfCVHhumPu	1	2017-08-17 08:18:20.052029	2017-08-17 08:18:20.05216	2017-08-17 08:18:20.052288		\N
5	Teresa	Uebber	Teresa	Teresa	teresa.uebber@uni-duesseldorf.de	f	$2a$10$mBEFTjPgZcqE8ogsU.u5K.0iMYpcS23yc2h1xhZrdCj5te8ziYZAm	1	2017-08-17 08:18:20.052427	2017-08-17 08:18:20.052497	2017-08-17 08:18:20.05256		\N
6	Bob	Bubbles	Bob	Bob	tobias.krauthoff+dbas.usert31@gmail.com	n	$2a$10$3.tF0hi1XeaBVvInd/OlpuEFA4/CeUcoLAHzDSffRdojF94xNheei	1	2017-08-17 08:18:20.052649	2017-08-17 08:18:20.052696	2017-08-17 08:18:20.05274		\N
7	Pascal	Lux	Pascal	Pascal	tobias.krauthoff+dbas.usert00@gmail.com	m	$2a$10$3.tF0hi1XeaBVvInd/OlpuEFA4/CeUcoLAHzDSffRdojF94xNheei	3	2017-08-17 08:18:20.052903	2017-08-17 08:18:20.052954	2017-08-17 08:18:20.052999		\N
8	Kurt	Hecht	Kurt	Kurt	tobias.krauthoff+dbas.usert01@gmail.com	m	$2a$10$3.tF0hi1XeaBVvInd/OlpuEFA4/CeUcoLAHzDSffRdojF94xNheei	3	2017-08-17 08:18:20.053076	2017-08-17 08:18:20.053122	2017-08-17 08:18:20.053166		\N
9	Torben	Hartl	Torben	Torben	tobias.krauthoff+dbas.usert02@gmail.com	m	$2a$10$3.tF0hi1XeaBVvInd/OlpuEFA4/CeUcoLAHzDSffRdojF94xNheei	3	2017-08-17 08:18:20.053241	2017-08-17 08:18:20.053288	2017-08-17 08:18:20.053332		\N
10	Thorsten	Scherer	Thorsten	Thorsten	tobias.krauthoff+dbas.usert03@gmail.com	m	$2a$10$3.tF0hi1XeaBVvInd/OlpuEFA4/CeUcoLAHzDSffRdojF94xNheei	3	2017-08-17 08:18:20.053407	2017-08-17 08:18:20.053453	2017-08-17 08:18:20.053497		\N
11	Friedrich	Schutte	Friedrich	Friedrich	tobias.krauthoff+dbas.usert04@gmail.com	m	$2a$10$3.tF0hi1XeaBVvInd/OlpuEFA4/CeUcoLAHzDSffRdojF94xNheei	3	2017-08-17 08:18:20.053573	2017-08-17 08:18:20.053619	2017-08-17 08:18:20.053663		\N
12	Aayden	Westermann	Aayden	Aayden	tobias.krauthoff+dbas.usert05@gmail.com	m	$2a$10$3.tF0hi1XeaBVvInd/OlpuEFA4/CeUcoLAHzDSffRdojF94xNheei	3	2017-08-17 08:18:20.053737	2017-08-17 08:18:20.053783	2017-08-17 08:18:20.053838		\N
13	Hermann	Grasshoff	Hermann	Hermann	tobias.krauthoff+dbas.usert06@gmail.com	m	$2a$10$3.tF0hi1XeaBVvInd/OlpuEFA4/CeUcoLAHzDSffRdojF94xNheei	3	2017-08-17 08:18:20.05399	2017-08-17 08:18:20.05406	2017-08-17 08:18:20.054133		\N
14	Wolf	Himmler	Wolf	Wolf	tobias.krauthoff+dbas.usert07@gmail.com	m	$2a$10$3.tF0hi1XeaBVvInd/OlpuEFA4/CeUcoLAHzDSffRdojF94xNheei	3	2017-08-17 08:18:20.05424	2017-08-17 08:18:20.05429	2017-08-17 08:18:20.054335		\N
15	Jakob	Winter	Jakob	Jakob	tobias.krauthoff+dbas.usert08@gmail.com	m	$2a$10$3.tF0hi1XeaBVvInd/OlpuEFA4/CeUcoLAHzDSffRdojF94xNheei	3	2017-08-17 08:18:20.054411	2017-08-17 08:18:20.054459	2017-08-17 08:18:20.054503		\N
16	Alwin	Wechter	Alwin	Alwin	tobias.krauthoff+dbas.usert09@gmail.com	m	$2a$10$3.tF0hi1XeaBVvInd/OlpuEFA4/CeUcoLAHzDSffRdojF94xNheei	3	2017-08-17 08:18:20.05458	2017-08-17 08:18:20.054627	2017-08-17 08:18:20.054671		\N
17	Walter	Weisser	Walter	Walter	tobias.krauthoff+dbas.usert10@gmail.com	m	$2a$10$3.tF0hi1XeaBVvInd/OlpuEFA4/CeUcoLAHzDSffRdojF94xNheei	3	2017-08-17 08:18:20.054747	2017-08-17 08:18:20.054794	2017-08-17 08:18:20.054838		\N
18	Volker	Keitel	Volker	Volker	tobias.krauthoff+dbas.usert11@gmail.com	m	$2a$10$3.tF0hi1XeaBVvInd/OlpuEFA4/CeUcoLAHzDSffRdojF94xNheei	3	2017-08-17 08:18:20.054913	2017-08-17 08:18:20.054959	2017-08-17 08:18:20.055003		\N
19	Benedikt	Feuerstein	Benedikt	Benedikt	tobias.krauthoff+dbas.usert12@gmail.com	m	$2a$10$3.tF0hi1XeaBVvInd/OlpuEFA4/CeUcoLAHzDSffRdojF94xNheei	3	2017-08-17 08:18:20.055079	2017-08-17 08:18:20.055125	2017-08-17 08:18:20.055169		\N
20	Engelbert	Gottlieb	Engelbert	Engelbert	tobias.krauthoff+dbas.usert13@gmail.com	m	$2a$10$3.tF0hi1XeaBVvInd/OlpuEFA4/CeUcoLAHzDSffRdojF94xNheei	3	2017-08-17 08:18:20.055246	2017-08-17 08:18:20.055293	2017-08-17 08:18:20.055342		\N
21	Elias	Auerbach	Elias	Elias	tobias.krauthoff+dbas.usert14@gmail.com	m	$2a$10$3.tF0hi1XeaBVvInd/OlpuEFA4/CeUcoLAHzDSffRdojF94xNheei	3	2017-08-17 08:18:20.055419	2017-08-17 08:18:20.055488	2017-08-17 08:18:20.055577		\N
22	Rupert	Wenz	Rupert	Rupert	tobias.krauthoff+dbas.usert15@gmail.com	m	$2a$10$3.tF0hi1XeaBVvInd/OlpuEFA4/CeUcoLAHzDSffRdojF94xNheei	3	2017-08-17 08:18:20.05574	2017-08-17 08:18:20.055834	2017-08-17 08:18:20.055915		\N
23	Marga	Wegscheider	Marga	Marga	tobias.krauthoff+dbas.usert16@gmail.com	f	$2a$10$3.tF0hi1XeaBVvInd/OlpuEFA4/CeUcoLAHzDSffRdojF94xNheei	3	2017-08-17 08:18:20.056071	2017-08-17 08:18:20.056131	2017-08-17 08:18:20.056176		\N
24	Larissa	Clauberg	Larissa	Larissa	tobias.krauthoff+dbas.usert17@gmail.com	f	$2a$10$3.tF0hi1XeaBVvInd/OlpuEFA4/CeUcoLAHzDSffRdojF94xNheei	3	2017-08-17 08:18:20.056261	2017-08-17 08:18:20.056331	2017-08-17 08:18:20.056413		\N
25	Emmi	Rosch	Emmi	Emmi	tobias.krauthoff+dbas.usert18@gmail.com	f	$2a$10$3.tF0hi1XeaBVvInd/OlpuEFA4/CeUcoLAHzDSffRdojF94xNheei	3	2017-08-17 08:18:20.056502	2017-08-17 08:18:20.056549	2017-08-17 08:18:20.056593		\N
26	Konstanze	Krebs	Konstanze	Konstanze	tobias.krauthoff+dbas.usert19@gmail.com	f	$2a$10$3.tF0hi1XeaBVvInd/OlpuEFA4/CeUcoLAHzDSffRdojF94xNheei	3	2017-08-17 08:18:20.056669	2017-08-17 08:18:20.056716	2017-08-17 08:18:20.056759		\N
27	Catrin	Fahnrich	Catrin	Catrin	tobias.krauthoff+dbas.usert20@gmail.com	f	$2a$10$3.tF0hi1XeaBVvInd/OlpuEFA4/CeUcoLAHzDSffRdojF94xNheei	3	2017-08-17 08:18:20.056899	2017-08-17 08:18:20.056949	2017-08-17 08:18:20.056997		\N
28	Antonia	Bartram	Antonia	Antonia	tobias.krauthoff+dbas.usert21@gmail.com	f	$2a$10$3.tF0hi1XeaBVvInd/OlpuEFA4/CeUcoLAHzDSffRdojF94xNheei	3	2017-08-17 08:18:20.057074	2017-08-17 08:18:20.05712	2017-08-17 08:18:20.057164		\N
29	Nora	Kempf	Nora	Nora	tobias.krauthoff+dbas.usert22@gmail.com	f	$2a$10$3.tF0hi1XeaBVvInd/OlpuEFA4/CeUcoLAHzDSffRdojF94xNheei	3	2017-08-17 08:18:20.057242	2017-08-17 08:18:20.057289	2017-08-17 08:18:20.057332		\N
30	Julia	Wetter	Julia	Julia	tobias.krauthoff+dbas.usert23@gmail.com	f	$2a$10$3.tF0hi1XeaBVvInd/OlpuEFA4/CeUcoLAHzDSffRdojF94xNheei	3	2017-08-17 08:18:20.057406	2017-08-17 08:18:20.057452	2017-08-17 08:18:20.0575		\N
31	Jutta	Munch	Jutta	Jutta	tobias.krauthoff+dbas.usert24@gmail.com	f	$2a$10$3.tF0hi1XeaBVvInd/OlpuEFA4/CeUcoLAHzDSffRdojF94xNheei	3	2017-08-17 08:18:20.057574	2017-08-17 08:18:20.05762	2017-08-17 08:18:20.057663		\N
32	Helga	Heilmann	Helga	Helga	tobias.krauthoff+dbas.usert25@gmail.com	f	$2a$10$3.tF0hi1XeaBVvInd/OlpuEFA4/CeUcoLAHzDSffRdojF94xNheei	3	2017-08-17 08:18:20.057736	2017-08-17 08:18:20.057781	2017-08-17 08:18:20.057824		\N
33	Denise	Tietjen	Denise	Denise	tobias.krauthoff+dbas.usert26@gmail.com	f	$2a$10$3.tF0hi1XeaBVvInd/OlpuEFA4/CeUcoLAHzDSffRdojF94xNheei	3	2017-08-17 08:18:20.057939	2017-08-17 08:18:20.057985	2017-08-17 08:18:20.058028		\N
34	Hanne	Beckmann	Hanne	Hanne	tobias.krauthoff+dbas.usert27@gmail.com	f	$2a$10$3.tF0hi1XeaBVvInd/OlpuEFA4/CeUcoLAHzDSffRdojF94xNheei	3	2017-08-17 08:18:20.058107	2017-08-17 08:18:20.058154	2017-08-17 08:18:20.058197		\N
35	Elly	Landauer	Elly	Elly	tobias.krauthoff+dbas.usert28@gmail.com	f	$2a$10$3.tF0hi1XeaBVvInd/OlpuEFA4/CeUcoLAHzDSffRdojF94xNheei	3	2017-08-17 08:18:20.05827	2017-08-17 08:18:20.058315	2017-08-17 08:18:20.058359		\N
36	Sybille	Redlich	Sybille	Sybille	tobias.krauthoff+dbas.usert29@gmail.com	f	$2a$10$3.tF0hi1XeaBVvInd/OlpuEFA4/CeUcoLAHzDSffRdojF94xNheei	3	2017-08-17 08:18:20.058434	2017-08-17 08:18:20.05848	2017-08-17 08:18:20.058523		\N
37	Ingeburg	Fischer	Ingeburg	Ingeburg	tobias.krauthoff+dbas.usert30@gmail.com	f	$2a$10$3.tF0hi1XeaBVvInd/OlpuEFA4/CeUcoLAHzDSffRdojF94xNheei	3	2017-08-17 08:18:20.058596	2017-08-17 08:18:20.058644	2017-08-17 08:18:20.058688		\N
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
-- Name: premisegroup_merged premisegroup_merged_premisegroup_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY premisegroup_merged
    ADD CONSTRAINT premisegroup_merged_premisegroup_uid_fkey FOREIGN KEY (premisegroup_uid) REFERENCES premisegroups(uid);


--
-- Name: premisegroup_merged premisegroup_merged_review_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY premisegroup_merged
    ADD CONSTRAINT premisegroup_merged_review_uid_fkey FOREIGN KEY (review_uid) REFERENCES review_merge(uid);


--
-- Name: premisegroup_splitted premisegroup_splitted_premisegroup_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY premisegroup_splitted
    ADD CONSTRAINT premisegroup_splitted_premisegroup_uid_fkey FOREIGN KEY (premisegroup_uid) REFERENCES premisegroups(uid);


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

