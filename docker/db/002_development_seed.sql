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
-- Name: statement_replacements_by_premisegroup_split; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE statement_replacements_by_premisegroup_split (
    uid integer NOT NULL,
    review_uid integer,
    old_statement_uid integer,
    new_statement_uid integer,
    "timestamp" timestamp without time zone
);


ALTER TABLE statement_replacements_by_premisegroup_split OWNER TO dbas;

--
-- Name: statement_replacements_by_premisegroup_split_uid_seq; Type: SEQUENCE; Schema: public; Owner: dbas
--

CREATE SEQUENCE statement_replacements_by_premisegroup_split_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE statement_replacements_by_premisegroup_split_uid_seq OWNER TO dbas;

--
-- Name: statement_replacements_by_premisegroup_split_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbas
--

ALTER SEQUENCE statement_replacements_by_premisegroup_split_uid_seq OWNED BY statement_replacements_by_premisegroup_split.uid;


--
-- Name: statement_replacements_by_premisegroups_merge; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE statement_replacements_by_premisegroups_merge (
    uid integer NOT NULL,
    review_uid integer,
    old_statement_uid integer,
    new_statement_uid integer,
    "timestamp" timestamp without time zone
);


ALTER TABLE statement_replacements_by_premisegroups_merge OWNER TO dbas;

--
-- Name: statement_replacements_by_premisegroups_merge_uid_seq; Type: SEQUENCE; Schema: public; Owner: dbas
--

CREATE SEQUENCE statement_replacements_by_premisegroups_merge_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE statement_replacements_by_premisegroups_merge_uid_seq OWNER TO dbas;

--
-- Name: statement_replacements_by_premisegroups_merge_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbas
--

ALTER SEQUENCE statement_replacements_by_premisegroups_merge_uid_seq OWNED BY statement_replacements_by_premisegroups_merge.uid;


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
-- Name: statement_replacements_by_premisegroup_split uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY statement_replacements_by_premisegroup_split ALTER COLUMN uid SET DEFAULT nextval('statement_replacements_by_premisegroup_split_uid_seq'::regclass);


--
-- Name: statement_replacements_by_premisegroups_merge uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY statement_replacements_by_premisegroups_merge ALTER COLUMN uid SET DEFAULT nextval('statement_replacements_by_premisegroups_merge_uid_seq'::regclass);


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
1	1	2	\N	f	1	2017-08-17 13:52:06.058107	2	t
2	2	2	\N	t	1	2017-08-17 13:52:06.058223	2	f
3	3	2	\N	f	1	2017-08-17 13:52:06.058311	2	f
4	4	3	\N	t	1	2017-08-17 13:52:06.058395	2	f
5	5	3	\N	f	1	2017-08-17 13:52:06.058476	2	f
8	8	4	\N	t	1	2017-08-17 13:52:06.058721	2	f
10	10	11	\N	f	1	2017-08-17 13:52:06.058883	2	f
11	11	2	\N	t	1	2017-08-17 13:52:06.058963	2	f
12	12	2	\N	t	1	2017-08-17 13:52:06.059045	2	f
15	15	5	\N	t	1	2017-08-17 13:52:06.059286	2	f
16	16	5	\N	f	1	2017-08-17 13:52:06.059366	2	f
17	17	5	\N	t	1	2017-08-17 13:52:06.059445	2	f
19	19	6	\N	t	1	2017-08-17 13:52:06.059605	2	f
20	20	6	\N	f	1	2017-08-17 13:52:06.059684	2	f
21	21	6	\N	f	1	2017-08-17 13:52:06.059771	2	f
23	23	14	\N	f	1	2017-08-17 13:52:06.059992	2	f
24	24	14	\N	t	1	2017-08-17 13:52:06.060074	2	f
26	26	14	\N	t	1	2017-08-17 13:52:06.060235	2	f
27	27	15	\N	t	1	2017-08-17 13:52:06.060317	2	f
28	27	16	\N	t	1	2017-08-17 13:52:06.0604	2	f
29	28	15	\N	t	1	2017-08-17 13:52:06.060483	2	f
30	29	15	\N	f	1	2017-08-17 13:52:06.060565	2	f
32	31	36	\N	t	3	2017-08-17 13:52:06.060726	1	f
34	33	39	\N	t	3	2017-08-17 13:52:06.060884	1	f
35	34	41	\N	t	1	2017-08-17 13:52:06.060964	1	f
36	35	36	\N	f	1	2017-08-17 13:52:06.061044	1	f
39	38	37	\N	t	1	2017-08-17 13:52:06.061295	1	f
40	39	37	\N	t	1	2017-08-17 13:52:06.061372	1	f
41	41	46	\N	f	1	2017-08-17 13:52:06.06145	1	f
42	42	37	\N	f	1	2017-08-17 13:52:06.0616	1	f
44	44	50	\N	f	1	2017-08-17 13:52:06.061752	1	f
46	45	50	\N	t	1	2017-08-17 13:52:06.061826	1	f
47	46	38	\N	t	1	2017-08-17 13:52:06.06191	1	f
49	48	38	\N	f	1	2017-08-17 13:52:06.062077	1	f
50	49	49	\N	f	1	2017-08-17 13:52:06.062154	1	f
51	51	58	\N	f	1	2017-08-17 13:52:06.062307	4	f
54	54	59	\N	t	1	2017-08-17 13:52:06.062533	4	f
55	55	59	\N	f	1	2017-08-17 13:52:06.062607	4	f
56	56	60	\N	t	1	2017-08-17 13:52:06.062683	4	f
57	57	60	\N	f	1	2017-08-17 13:52:06.06276	4	f
58	50	58	\N	t	1	2017-08-17 13:52:06.062232	4	f
59	61	67	\N	t	1	2017-08-17 13:52:06.062836	4	f
60	62	69	\N	t	1	2017-08-17 13:52:06.062912	5	f
61	63	69	\N	t	1	2017-08-17 13:52:06.062996	5	f
62	64	69	\N	f	1	2017-08-17 13:52:06.063078	5	f
63	65	70	\N	f	1	2017-08-17 13:52:06.063157	5	f
64	66	70	\N	f	1	2017-08-17 13:52:06.063235	5	f
65	67	76	\N	t	1	2017-08-17 13:52:06.063312	7	f
66	68	76	\N	f	1	2017-08-17 13:52:06.063391	7	f
67	69	76	\N	f	1	2017-08-17 13:52:06.063471	7	f
68	70	79	\N	f	1	2017-08-17 13:52:06.063548	7	f
6	6	\N	4	f	1	2017-08-17 13:52:06.058556	2	f
7	7	\N	5	f	1	2017-08-17 13:52:06.058639	2	f
9	9	\N	8	f	1	2017-08-17 13:52:06.058801	2	f
13	13	\N	12	f	1	2017-08-17 13:52:06.059127	2	f
14	14	\N	13	f	1	2017-08-17 13:52:06.059207	2	f
18	18	\N	2	f	1	2017-08-17 13:52:06.059525	2	f
22	22	\N	3	f	1	2017-08-17 13:52:06.059851	2	f
25	25	\N	11	f	1	2017-08-17 13:52:06.060153	2	f
31	30	\N	15	f	1	2017-08-17 13:52:06.060646	2	f
33	32	\N	32	f	3	2017-08-17 13:52:06.060805	1	f
37	36	\N	36	f	1	2017-08-17 13:52:06.061123	1	f
38	37	\N	36	f	1	2017-08-17 13:52:06.06122	1	f
43	43	\N	42	f	1	2017-08-17 13:52:06.061676	1	f
45	40	\N	39	f	1	2017-08-17 13:52:06.061525	1	f
48	47	\N	47	f	1	2017-08-17 13:52:06.061986	1	f
52	52	\N	58	f	1	2017-08-17 13:52:06.062383	4	f
53	53	\N	51	f	1	2017-08-17 13:52:06.062458	4	f
69	71	\N	65	f	1	2017-08-17 13:52:06.063625	7	f
\.


--
-- Name: arguments_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('arguments_uid_seq', 69, true);


--
-- Data for Name: clicked_arguments; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY clicked_arguments (uid, argument_uid, author_uid, "timestamp", is_up_vote, is_valid) FROM stdin;
1054	1	14	2017-08-03 13:52:14.010178	t	t
1055	1	31	2017-08-17 13:52:14.010356	t	t
1056	1	35	2017-08-04 13:52:14.010435	t	t
1057	1	18	2017-08-07 13:52:14.010508	t	t
1058	1	13	2017-08-13 13:52:14.010579	t	t
1059	1	34	2017-08-01 13:52:14.010648	t	t
1060	1	28	2017-08-01 13:52:14.010715	t	t
1061	1	16	2017-08-09 13:52:14.010782	f	t
1062	1	11	2017-07-28 13:52:14.010849	f	t
1063	1	29	2017-08-09 13:52:14.010914	f	t
1064	1	29	2017-08-16 13:52:14.010981	f	t
1065	2	23	2017-08-11 13:52:14.011049	t	t
1066	2	17	2017-08-11 13:52:14.011117	t	t
1067	2	18	2017-08-02 13:52:14.011183	t	t
1068	2	10	2017-08-11 13:52:14.011251	t	t
1069	2	11	2017-08-14 13:52:14.011319	t	t
1070	2	33	2017-08-05 13:52:14.011387	t	t
1071	2	34	2017-08-01 13:52:14.011453	t	t
1072	2	36	2017-08-17 13:52:14.011521	f	t
1073	2	28	2017-07-29 13:52:14.011588	f	t
1074	2	32	2017-08-09 13:52:14.011654	f	t
1075	2	29	2017-07-31 13:52:14.011721	f	t
1076	3	8	2017-07-30 13:52:14.011788	t	t
1077	3	9	2017-08-17 13:52:14.011854	t	t
1078	3	29	2017-08-03 13:52:14.01192	t	t
1079	3	28	2017-07-28 13:52:14.011987	t	t
1080	3	34	2017-08-04 13:52:14.012053	t	t
1081	3	7	2017-07-31 13:52:14.012117	t	t
1082	3	14	2017-08-04 13:52:14.012182	f	t
1083	3	28	2017-08-09 13:52:14.012249	f	t
1084	3	37	2017-07-24 13:52:14.012317	f	t
1085	3	29	2017-08-11 13:52:14.012385	f	t
1086	3	17	2017-08-09 13:52:14.012452	f	t
1087	3	20	2017-08-08 13:52:14.012518	f	t
1088	3	33	2017-08-09 13:52:14.012585	f	t
1089	4	37	2017-08-05 13:52:14.012652	t	t
1090	4	35	2017-07-31 13:52:14.012718	t	t
1091	4	19	2017-08-13 13:52:14.012785	t	t
1092	4	36	2017-08-06 13:52:14.012853	t	t
1093	4	13	2017-08-12 13:52:14.012921	t	t
1094	4	20	2017-08-11 13:52:14.012987	t	t
1095	4	9	2017-08-14 13:52:14.013054	t	t
1096	4	15	2017-07-30 13:52:14.013121	t	t
1097	4	18	2017-07-28 13:52:14.013188	t	t
1098	4	25	2017-07-27 13:52:14.013254	t	t
1099	4	27	2017-08-08 13:52:14.01332	t	t
1100	4	7	2017-07-25 13:52:14.013386	t	t
1101	4	15	2017-07-23 13:52:14.013453	f	t
1102	4	37	2017-08-13 13:52:14.013518	f	t
1103	4	21	2017-08-02 13:52:14.013584	f	t
1104	5	29	2017-08-13 13:52:14.01365	t	t
1105	5	10	2017-08-02 13:52:14.013716	t	t
1106	5	34	2017-08-04 13:52:14.013781	t	t
1107	5	14	2017-08-16 13:52:14.013856	t	t
1108	5	31	2017-08-02 13:52:14.01393	t	t
1109	5	25	2017-08-10 13:52:14.013998	t	t
1110	5	33	2017-08-10 13:52:14.014066	f	t
1111	5	27	2017-07-27 13:52:14.014133	f	t
1112	5	19	2017-08-01 13:52:14.0142	f	t
1113	5	29	2017-08-07 13:52:14.014266	f	t
1114	5	17	2017-08-05 13:52:14.014334	f	t
1115	5	11	2017-08-12 13:52:14.014401	f	t
1116	5	21	2017-08-10 13:52:14.014469	f	t
1117	5	15	2017-08-16 13:52:14.014536	f	t
1118	5	20	2017-07-30 13:52:14.014603	f	t
1119	8	9	2017-08-07 13:52:14.01467	t	t
1120	8	22	2017-08-15 13:52:14.014737	t	t
1121	8	29	2017-07-31 13:52:14.014803	t	t
1122	8	19	2017-08-07 13:52:14.014869	t	t
1123	8	16	2017-08-11 13:52:14.014936	t	t
1124	8	7	2017-08-05 13:52:14.015003	t	t
1125	8	25	2017-08-10 13:52:14.015069	t	t
1126	8	17	2017-07-29 13:52:14.015136	t	t
1127	8	20	2017-08-17 13:52:14.015203	t	t
1128	8	33	2017-08-08 13:52:14.01527	t	t
1129	8	14	2017-08-11 13:52:14.015337	t	t
1130	8	37	2017-07-28 13:52:14.015405	t	t
1131	8	28	2017-08-01 13:52:14.015472	f	t
1132	8	9	2017-08-15 13:52:14.015539	f	t
1133	8	14	2017-08-15 13:52:14.015606	f	t
1134	8	23	2017-07-25 13:52:14.015672	f	t
1135	8	8	2017-07-29 13:52:14.015738	f	t
1136	8	15	2017-08-05 13:52:14.015805	f	t
1137	8	20	2017-08-01 13:52:14.015872	f	t
1138	8	24	2017-08-03 13:52:14.015936	f	t
1139	8	11	2017-08-14 13:52:14.016002	f	t
1140	8	21	2017-07-30 13:52:14.016069	f	t
1141	10	7	2017-08-02 13:52:14.016136	t	t
1142	10	34	2017-08-10 13:52:14.016204	t	t
1143	10	31	2017-08-16 13:52:14.016269	t	t
1144	10	28	2017-08-15 13:52:14.016337	t	t
1145	10	22	2017-08-04 13:52:14.016404	t	t
1146	10	10	2017-08-01 13:52:14.016472	t	t
1147	10	15	2017-08-02 13:52:14.016539	t	t
1148	10	13	2017-08-03 13:52:14.016607	t	t
1149	10	36	2017-08-03 13:52:14.016674	t	t
1150	10	18	2017-07-31 13:52:14.01674	t	t
1151	10	29	2017-08-04 13:52:14.016806	t	t
1152	10	17	2017-07-27 13:52:14.016872	t	t
1153	10	9	2017-08-06 13:52:14.016949	t	t
1154	10	33	2017-08-17 13:52:14.017017	t	t
1155	10	35	2017-08-04 13:52:14.017086	t	t
1156	10	23	2017-08-02 13:52:14.017155	t	t
1157	10	14	2017-08-08 13:52:14.017225	t	t
1158	10	32	2017-07-23 13:52:14.017294	f	t
1159	10	24	2017-07-28 13:52:14.017363	f	t
1160	11	35	2017-08-01 13:52:14.017433	t	t
1161	11	26	2017-08-05 13:52:14.017503	t	t
1162	11	19	2017-08-10 13:52:14.017572	t	t
1163	11	29	2017-07-29 13:52:14.017641	t	t
1164	11	36	2017-07-27 13:52:14.017711	t	t
1165	11	7	2017-07-23 13:52:14.01778	t	t
1166	11	31	2017-08-01 13:52:14.017856	t	t
1167	11	14	2017-08-17 13:52:14.017937	t	t
1168	11	20	2017-08-04 13:52:14.018004	t	t
1169	11	29	2017-07-26 13:52:14.018072	t	t
1170	11	24	2017-07-23 13:52:14.018137	t	t
1171	11	9	2017-07-28 13:52:14.018205	t	t
1172	11	12	2017-07-31 13:52:14.018271	t	t
1173	11	10	2017-08-07 13:52:14.018338	t	t
1174	11	20	2017-08-03 13:52:14.018404	f	t
1175	11	21	2017-08-12 13:52:14.018471	f	t
1176	11	23	2017-08-09 13:52:14.018539	f	t
1177	11	9	2017-08-09 13:52:14.018605	f	t
1178	11	25	2017-08-05 13:52:14.018672	f	t
1179	11	34	2017-08-16 13:52:14.01874	f	t
1180	11	32	2017-08-01 13:52:14.018808	f	t
1181	12	32	2017-08-08 13:52:14.018874	t	t
1182	12	16	2017-08-08 13:52:14.018941	t	t
1183	15	26	2017-08-09 13:52:14.019007	t	t
1184	15	10	2017-08-06 13:52:14.019073	t	t
1185	15	28	2017-08-15 13:52:14.01914	t	t
1186	15	31	2017-08-04 13:52:14.019206	f	t
1187	15	13	2017-08-16 13:52:14.019272	f	t
1188	15	18	2017-08-08 13:52:14.019339	f	t
1189	15	16	2017-08-03 13:52:14.019407	f	t
1190	15	23	2017-07-31 13:52:14.019474	f	t
1191	15	32	2017-08-06 13:52:14.019541	f	t
1192	15	22	2017-08-05 13:52:14.019607	f	t
1193	16	16	2017-07-31 13:52:14.019673	t	t
1194	16	22	2017-08-03 13:52:14.01974	t	t
1195	16	20	2017-08-06 13:52:14.019806	t	t
1196	16	29	2017-07-31 13:52:14.019872	t	t
1197	16	18	2017-07-29 13:52:14.019939	t	t
1198	16	27	2017-08-13 13:52:14.020006	t	t
1199	16	21	2017-07-30 13:52:14.020073	t	t
1200	16	24	2017-08-10 13:52:14.02014	t	t
1201	16	32	2017-07-25 13:52:14.020207	t	t
1202	16	25	2017-08-05 13:52:14.020274	t	t
1203	16	9	2017-08-01 13:52:14.020339	t	t
1204	16	37	2017-07-26 13:52:14.020404	t	t
1205	16	7	2017-07-26 13:52:14.020471	t	t
1206	16	29	2017-07-26 13:52:14.020537	t	t
1207	16	37	2017-07-28 13:52:14.020603	f	t
1208	16	22	2017-08-03 13:52:14.020668	f	t
1209	16	34	2017-08-06 13:52:14.020734	f	t
1210	16	25	2017-08-17 13:52:14.020794	f	t
1211	16	12	2017-08-10 13:52:14.020859	f	t
1212	17	11	2017-08-09 13:52:14.020925	t	t
1213	17	29	2017-08-04 13:52:14.02099	t	t
1214	17	24	2017-08-02 13:52:14.021055	t	t
1215	17	12	2017-08-11 13:52:14.021119	t	t
1216	17	10	2017-07-24 13:52:14.021184	t	t
1217	17	14	2017-07-29 13:52:14.021251	t	t
1218	17	34	2017-08-04 13:52:14.021317	t	t
1219	17	37	2017-08-04 13:52:14.021375	t	t
1220	17	13	2017-07-31 13:52:14.021437	t	t
1221	17	23	2017-07-26 13:52:14.021501	t	t
1222	17	22	2017-07-31 13:52:14.021564	t	t
1223	17	25	2017-08-07 13:52:14.021626	t	t
1224	17	33	2017-08-04 13:52:14.021684	t	t
1225	17	21	2017-08-08 13:52:14.021741	t	t
1226	17	29	2017-08-11 13:52:14.021804	f	t
1227	17	20	2017-08-12 13:52:14.021882	f	t
1228	17	9	2017-07-25 13:52:14.021951	f	t
1229	17	35	2017-08-07 13:52:14.022019	f	t
1230	17	15	2017-07-30 13:52:14.022086	f	t
1231	17	33	2017-08-03 13:52:14.022154	f	t
1232	17	17	2017-07-24 13:52:14.02222	f	t
1233	17	8	2017-08-11 13:52:14.022287	f	t
1234	17	22	2017-07-31 13:52:14.022354	f	t
1235	19	22	2017-08-06 13:52:14.02242	t	t
1236	19	21	2017-08-04 13:52:14.022486	t	t
1237	19	10	2017-08-02 13:52:14.022553	t	t
1238	19	28	2017-07-28 13:52:14.022619	t	t
1239	19	17	2017-08-02 13:52:14.022687	t	t
1240	19	34	2017-07-29 13:52:14.022753	t	t
1241	19	27	2017-07-30 13:52:14.02282	t	t
1242	19	29	2017-08-07 13:52:14.022887	t	t
1243	19	12	2017-08-12 13:52:14.022953	t	t
1244	19	35	2017-07-25 13:52:14.023019	t	t
1245	19	25	2017-08-07 13:52:14.023082	t	t
1246	19	32	2017-08-17 13:52:14.023146	t	t
1247	19	36	2017-08-14 13:52:14.02321	t	t
1248	19	16	2017-08-09 13:52:14.023275	t	t
1249	19	8	2017-07-23 13:52:14.023339	t	t
1250	19	19	2017-08-07 13:52:14.023402	t	t
1251	19	15	2017-08-15 13:52:14.023462	t	t
1252	19	14	2017-07-29 13:52:14.023523	t	t
1253	19	20	2017-08-16 13:52:14.023586	t	t
1254	19	26	2017-08-10 13:52:14.023649	t	t
1255	19	29	2017-07-24 13:52:14.023712	t	t
1256	19	7	2017-07-30 13:52:14.023774	t	t
1257	19	23	2017-08-12 13:52:14.023835	t	t
1258	19	33	2017-08-13 13:52:14.023895	f	t
1259	19	20	2017-08-06 13:52:14.023956	f	t
1260	19	26	2017-07-25 13:52:14.024023	f	t
1261	19	29	2017-07-25 13:52:14.024091	f	t
1262	19	17	2017-08-09 13:52:14.024158	f	t
1263	19	27	2017-08-13 13:52:14.024225	f	t
1264	19	12	2017-07-23 13:52:14.024292	f	t
1265	19	37	2017-08-05 13:52:14.024357	f	t
1266	19	32	2017-08-03 13:52:14.024423	f	t
1267	19	35	2017-07-26 13:52:14.02449	f	t
1268	19	36	2017-07-25 13:52:14.024557	f	t
1269	19	21	2017-07-31 13:52:14.024624	f	t
1270	19	7	2017-08-02 13:52:14.024692	f	t
1271	19	10	2017-08-17 13:52:14.024759	f	t
1272	19	25	2017-07-23 13:52:14.024826	f	t
1273	19	34	2017-08-04 13:52:14.024893	f	t
1274	19	16	2017-07-27 13:52:14.02496	f	t
1275	19	13	2017-08-08 13:52:14.025028	f	t
1276	19	24	2017-07-31 13:52:14.025095	f	t
1277	19	15	2017-07-23 13:52:14.025162	f	t
1278	20	28	2017-08-14 13:52:14.025229	t	t
1279	20	36	2017-08-12 13:52:14.025297	t	t
1280	21	13	2017-07-29 13:52:14.025364	t	t
1281	21	33	2017-07-24 13:52:14.02543	t	t
1282	21	32	2017-07-31 13:52:14.025497	t	t
1283	21	28	2017-08-04 13:52:14.025563	t	t
1284	21	9	2017-08-16 13:52:14.02563	t	t
1285	21	27	2017-07-31 13:52:14.025696	t	t
1286	21	31	2017-08-02 13:52:14.025764	t	t
1287	21	29	2017-08-02 13:52:14.025832	t	t
1288	21	15	2017-08-14 13:52:14.025941	f	t
1289	23	16	2017-08-07 13:52:14.026011	t	t
1290	23	18	2017-08-10 13:52:14.026079	t	t
1291	23	29	2017-08-05 13:52:14.026145	t	t
1292	23	14	2017-08-17 13:52:14.026209	t	t
1293	23	21	2017-08-15 13:52:14.026274	t	t
1294	23	11	2017-08-10 13:52:14.026339	t	t
1295	23	16	2017-08-01 13:52:14.026401	f	t
1296	23	20	2017-08-06 13:52:14.026464	f	t
1297	23	24	2017-08-17 13:52:14.026529	f	t
1298	23	33	2017-08-03 13:52:14.026593	f	t
1299	24	10	2017-07-27 13:52:14.026658	t	t
1300	24	36	2017-07-27 13:52:14.026721	t	t
1301	24	22	2017-08-13 13:52:14.026781	t	t
1302	24	15	2017-07-26 13:52:14.026844	t	t
1303	24	35	2017-08-08 13:52:14.026912	t	t
1304	24	21	2017-08-16 13:52:14.026978	t	t
1305	24	17	2017-08-03 13:52:14.027045	t	t
1306	24	37	2017-07-30 13:52:14.027112	t	t
1307	24	25	2017-08-01 13:52:14.027179	t	t
1308	24	20	2017-08-15 13:52:14.027244	t	t
1309	24	26	2017-08-17 13:52:14.02731	t	t
1310	24	7	2017-08-01 13:52:14.027376	t	t
1311	24	32	2017-07-24 13:52:14.027491	t	t
1312	24	9	2017-08-12 13:52:14.02756	t	t
1313	24	28	2017-07-28 13:52:14.027629	t	t
1314	24	8	2017-07-28 13:52:14.027697	t	t
1315	24	31	2017-07-29 13:52:14.027765	t	t
1316	24	29	2017-08-10 13:52:14.027832	t	t
1317	24	23	2017-07-28 13:52:14.0279	t	t
1318	24	14	2017-07-29 13:52:14.027967	t	t
1319	24	19	2017-08-12 13:52:14.028035	t	t
1320	24	25	2017-08-07 13:52:14.028102	f	t
1321	24	7	2017-08-06 13:52:14.02817	f	t
1322	24	8	2017-08-04 13:52:14.028237	f	t
1323	24	12	2017-07-26 13:52:14.028302	f	t
1324	24	15	2017-07-26 13:52:14.028369	f	t
1325	24	26	2017-08-03 13:52:14.028436	f	t
1326	24	34	2017-08-04 13:52:14.028503	f	t
1327	24	29	2017-08-03 13:52:14.02857	f	t
1328	24	28	2017-08-17 13:52:14.028638	f	t
1329	24	14	2017-08-04 13:52:14.028705	f	t
1330	24	10	2017-08-05 13:52:14.028772	f	t
1331	24	36	2017-08-05 13:52:14.028838	f	t
1332	24	33	2017-08-08 13:52:14.028905	f	t
1333	24	19	2017-08-17 13:52:14.028969	f	t
1334	24	16	2017-08-06 13:52:14.029035	f	t
1335	24	35	2017-08-16 13:52:14.0291	f	t
1336	24	24	2017-07-29 13:52:14.029167	f	t
1337	24	37	2017-08-02 13:52:14.029234	f	t
1338	24	17	2017-07-29 13:52:14.0293	f	t
1339	24	29	2017-08-02 13:52:14.029364	f	t
1340	24	27	2017-07-31 13:52:14.02943	f	t
1341	26	8	2017-07-30 13:52:14.029497	t	t
1342	26	34	2017-08-02 13:52:14.029563	t	t
1343	26	32	2017-07-25 13:52:14.029627	t	t
1344	26	29	2017-07-31 13:52:14.029693	t	t
1345	26	9	2017-08-11 13:52:14.02976	t	t
1346	26	29	2017-08-15 13:52:14.029827	t	t
1347	26	7	2017-08-11 13:52:14.029905	t	t
1348	26	10	2017-08-11 13:52:14.029979	t	t
1349	26	7	2017-08-15 13:52:14.030047	f	t
1350	26	19	2017-08-03 13:52:14.030113	f	t
1351	26	31	2017-07-23 13:52:14.030177	f	t
1352	26	13	2017-08-11 13:52:14.030247	f	t
1353	26	34	2017-08-09 13:52:14.030316	f	t
1354	26	12	2017-07-31 13:52:14.030385	f	t
1355	26	16	2017-08-14 13:52:14.030453	f	t
1356	26	26	2017-08-13 13:52:14.030524	f	t
1357	27	14	2017-07-24 13:52:14.030593	t	t
1358	27	35	2017-08-13 13:52:14.030664	t	t
1359	27	12	2017-08-17 13:52:14.030734	t	t
1360	27	12	2017-08-05 13:52:14.030802	f	t
1361	27	19	2017-07-30 13:52:14.030871	f	t
1362	27	18	2017-08-07 13:52:14.030949	f	t
1363	28	34	2017-08-02 13:52:14.031016	t	t
1364	28	21	2017-08-12 13:52:14.031083	t	t
1365	28	26	2017-08-10 13:52:14.03115	t	t
1366	28	25	2017-08-17 13:52:14.031217	t	t
1367	28	28	2017-07-27 13:52:14.031283	t	t
1368	28	29	2017-08-04 13:52:14.03135	t	t
1369	28	19	2017-07-29 13:52:14.031414	t	t
1370	28	31	2017-08-15 13:52:14.031476	t	t
1371	28	12	2017-08-05 13:52:14.03154	f	t
1372	28	27	2017-08-03 13:52:14.031604	f	t
1373	28	17	2017-08-13 13:52:14.031667	f	t
1374	28	23	2017-08-16 13:52:14.031731	f	t
1375	28	16	2017-08-11 13:52:14.031794	f	t
1376	28	34	2017-07-27 13:52:14.031859	f	t
1377	28	25	2017-08-16 13:52:14.031922	f	t
1378	28	31	2017-08-08 13:52:14.031986	f	t
1379	28	20	2017-08-04 13:52:14.032047	f	t
1380	28	11	2017-08-13 13:52:14.03211	f	t
1381	29	19	2017-07-23 13:52:14.032177	t	t
1382	29	18	2017-08-02 13:52:14.032243	t	t
1383	29	26	2017-08-15 13:52:14.03231	t	t
1384	29	22	2017-07-27 13:52:14.032376	t	t
1385	29	16	2017-08-16 13:52:14.032442	t	t
1386	29	12	2017-08-10 13:52:14.03251	t	t
1387	29	15	2017-07-25 13:52:14.032577	t	t
1388	29	32	2017-07-27 13:52:14.032645	t	t
1389	29	27	2017-08-07 13:52:14.032711	t	t
1390	29	8	2017-08-13 13:52:14.032778	t	t
1391	29	9	2017-08-12 13:52:14.032846	t	t
1392	29	20	2017-08-07 13:52:14.032914	t	t
1393	29	11	2017-07-31 13:52:14.032981	t	t
1394	29	10	2017-08-03 13:52:14.033048	t	t
1395	29	23	2017-08-02 13:52:14.033115	t	t
1396	29	31	2017-07-25 13:52:14.033181	t	t
1397	29	8	2017-08-01 13:52:14.033248	f	t
1398	29	28	2017-08-05 13:52:14.033314	f	t
1399	30	20	2017-08-02 13:52:14.033378	t	t
1400	30	36	2017-08-13 13:52:14.033443	t	t
1401	30	12	2017-08-05 13:52:14.033509	t	t
1402	30	18	2017-07-24 13:52:14.033574	t	t
1403	30	22	2017-07-26 13:52:14.033639	t	t
1404	30	10	2017-07-24 13:52:14.033705	t	t
1405	30	29	2017-08-08 13:52:14.033768	t	t
1406	30	26	2017-07-27 13:52:14.033833	t	t
1407	30	9	2017-07-27 13:52:14.033908	t	t
1408	30	33	2017-07-30 13:52:14.033974	t	t
1409	30	35	2017-08-17 13:52:14.034042	t	t
1410	30	14	2017-07-23 13:52:14.034108	f	t
1411	30	27	2017-07-27 13:52:14.034173	f	t
1412	30	24	2017-07-30 13:52:14.034238	f	t
1413	30	36	2017-08-09 13:52:14.034302	f	t
1414	30	17	2017-07-24 13:52:14.03437	f	t
1415	30	15	2017-07-28 13:52:14.034439	f	t
1416	30	7	2017-08-02 13:52:14.034502	f	t
1417	30	16	2017-08-03 13:52:14.034565	f	t
1418	30	8	2017-07-28 13:52:14.03463	f	t
1419	30	26	2017-08-04 13:52:14.034694	f	t
1420	30	21	2017-07-29 13:52:14.034754	f	t
1421	30	31	2017-08-09 13:52:14.034819	f	t
1422	30	23	2017-07-27 13:52:14.034886	f	t
1423	30	29	2017-08-13 13:52:14.034953	f	t
1424	30	35	2017-07-31 13:52:14.035021	f	t
1425	30	9	2017-07-25 13:52:14.035089	f	t
1426	30	10	2017-07-24 13:52:14.035156	f	t
1427	30	37	2017-07-23 13:52:14.035224	f	t
1428	30	13	2017-08-17 13:52:14.03529	f	t
1429	30	12	2017-08-07 13:52:14.035358	f	t
1430	30	22	2017-08-07 13:52:14.035424	f	t
1431	32	12	2017-08-15 13:52:14.035492	t	t
1432	32	32	2017-08-01 13:52:14.03556	t	t
1433	32	36	2017-07-30 13:52:14.035626	f	t
1434	32	31	2017-08-17 13:52:14.035693	f	t
1435	32	33	2017-07-24 13:52:14.035761	f	t
1436	32	35	2017-08-09 13:52:14.035827	f	t
1437	32	19	2017-08-14 13:52:14.035894	f	t
1438	32	26	2017-08-07 13:52:14.03596	f	t
1439	34	19	2017-08-13 13:52:14.036027	t	t
1440	34	27	2017-08-02 13:52:14.036093	t	t
1441	34	37	2017-07-23 13:52:14.036158	t	t
1442	34	17	2017-08-12 13:52:14.036223	t	t
1443	34	23	2017-08-05 13:52:14.036286	t	t
1444	34	25	2017-07-25 13:52:14.036351	t	t
1445	34	29	2017-08-04 13:52:14.036414	t	t
1446	34	10	2017-08-02 13:52:14.036478	t	t
1447	34	15	2017-07-27 13:52:14.036541	t	t
1448	34	33	2017-08-04 13:52:14.036605	f	t
1449	34	36	2017-08-15 13:52:14.03667	f	t
1450	34	29	2017-08-10 13:52:14.036733	f	t
1451	34	21	2017-08-15 13:52:14.036797	f	t
1452	34	37	2017-08-13 13:52:14.036858	f	t
1453	34	13	2017-08-16 13:52:14.036919	f	t
1454	34	29	2017-08-12 13:52:14.036982	f	t
1455	34	28	2017-08-01 13:52:14.037049	f	t
1456	34	18	2017-08-11 13:52:14.037116	f	t
1457	34	23	2017-08-02 13:52:14.037183	f	t
1458	34	19	2017-08-05 13:52:14.037251	f	t
1459	34	9	2017-08-07 13:52:14.037316	f	t
1460	34	7	2017-07-26 13:52:14.037383	f	t
1461	35	19	2017-08-13 13:52:14.037449	t	t
1462	35	28	2017-08-15 13:52:14.037517	t	t
1463	35	36	2017-08-12 13:52:14.037583	t	t
1464	35	26	2017-07-25 13:52:14.037649	t	t
1465	35	29	2017-08-06 13:52:14.037717	f	t
1466	35	14	2017-08-11 13:52:14.037784	f	t
1467	35	28	2017-07-25 13:52:14.037857	f	t
1468	36	35	2017-07-27 13:52:14.037929	t	t
1469	36	24	2017-07-27 13:52:14.037997	t	t
1470	36	32	2017-07-27 13:52:14.038063	t	t
1471	36	17	2017-07-26 13:52:14.038129	t	t
1472	36	19	2017-08-14 13:52:14.038194	t	t
1473	36	10	2017-08-10 13:52:14.03826	f	t
1474	36	33	2017-07-25 13:52:14.038327	f	t
1475	36	15	2017-07-24 13:52:14.038393	f	t
1476	36	25	2017-08-14 13:52:14.038458	f	t
1477	36	13	2017-07-28 13:52:14.038525	f	t
1478	39	29	2017-07-26 13:52:14.03859	t	t
1479	39	15	2017-08-12 13:52:14.038657	t	t
1480	39	34	2017-08-09 13:52:14.038723	t	t
1481	40	20	2017-08-13 13:52:14.038788	t	t
1482	40	12	2017-07-30 13:52:14.038854	t	t
1483	40	13	2017-08-03 13:52:14.038919	f	t
1484	40	19	2017-08-10 13:52:14.038986	f	t
1485	40	15	2017-08-10 13:52:14.039054	f	t
1486	41	36	2017-07-29 13:52:14.039117	t	t
1487	41	24	2017-08-08 13:52:14.039182	t	t
1488	41	10	2017-08-09 13:52:14.039247	t	t
1489	41	8	2017-07-25 13:52:14.039309	t	t
1490	41	15	2017-08-15 13:52:14.03937	t	t
1491	41	36	2017-07-23 13:52:14.039437	f	t
1492	41	15	2017-08-01 13:52:14.039504	f	t
1493	41	37	2017-08-06 13:52:14.03957	f	t
1494	41	11	2017-07-30 13:52:14.039637	f	t
1495	41	26	2017-07-23 13:52:14.039703	f	t
1496	41	12	2017-08-14 13:52:14.03977	f	t
1497	41	10	2017-08-12 13:52:14.039838	f	t
1498	41	16	2017-08-07 13:52:14.039907	f	t
1499	41	32	2017-08-15 13:52:14.039976	f	t
1500	41	8	2017-07-28 13:52:14.040043	f	t
1501	42	31	2017-08-17 13:52:14.04011	t	t
1502	42	25	2017-08-09 13:52:14.040178	t	t
1503	42	16	2017-08-06 13:52:14.040246	t	t
1504	42	34	2017-08-16 13:52:14.040315	t	t
1505	42	29	2017-08-16 13:52:14.040383	t	t
1506	42	36	2017-08-15 13:52:14.04045	t	t
1507	42	33	2017-08-06 13:52:14.040517	t	t
1508	42	21	2017-07-31 13:52:14.040582	t	t
1509	42	20	2017-08-04 13:52:14.040647	t	t
1510	42	12	2017-07-24 13:52:14.040711	t	t
1511	42	18	2017-08-02 13:52:14.040777	t	t
1512	42	10	2017-08-15 13:52:14.040841	t	t
1513	42	29	2017-07-26 13:52:14.040904	t	t
1514	42	22	2017-08-04 13:52:14.040978	f	t
1515	42	17	2017-08-03 13:52:14.041044	f	t
1516	42	10	2017-08-09 13:52:14.04111	f	t
1517	42	29	2017-08-11 13:52:14.041176	f	t
1518	42	13	2017-08-04 13:52:14.04124	f	t
1519	42	8	2017-08-13 13:52:14.041303	f	t
1520	42	33	2017-07-24 13:52:14.041368	f	t
1521	42	9	2017-07-25 13:52:14.041435	f	t
1522	42	24	2017-08-04 13:52:14.041505	f	t
1523	42	26	2017-08-16 13:52:14.041574	f	t
1524	42	35	2017-07-31 13:52:14.041644	f	t
1525	42	32	2017-08-08 13:52:14.041713	f	t
1526	42	21	2017-08-11 13:52:14.041782	f	t
1527	42	34	2017-08-14 13:52:14.041857	f	t
1528	44	35	2017-07-29 13:52:14.041929	t	t
1529	44	9	2017-07-30 13:52:14.042007	t	t
1530	44	7	2017-08-12 13:52:14.042075	t	t
1531	44	12	2017-08-03 13:52:14.042143	t	t
1532	44	31	2017-07-23 13:52:14.042211	t	t
1533	44	19	2017-08-17 13:52:14.042278	t	t
1534	44	24	2017-08-10 13:52:14.042345	t	t
1535	44	33	2017-07-23 13:52:14.042414	t	t
1536	44	14	2017-08-13 13:52:14.042482	t	t
1537	44	34	2017-08-02 13:52:14.042549	t	t
1538	44	26	2017-07-31 13:52:14.042616	t	t
1539	44	13	2017-07-25 13:52:14.042681	t	t
1540	44	37	2017-08-12 13:52:14.042747	t	t
1541	44	16	2017-07-27 13:52:14.042813	t	t
1542	44	21	2017-08-09 13:52:14.042878	t	t
1543	44	29	2017-07-24 13:52:14.042944	f	t
1544	44	22	2017-07-31 13:52:14.043047	f	t
1545	44	7	2017-07-29 13:52:14.043113	f	t
1546	44	35	2017-08-05 13:52:14.04318	f	t
1547	44	16	2017-08-02 13:52:14.043245	f	t
1548	44	31	2017-08-11 13:52:14.043311	f	t
1549	44	14	2017-08-10 13:52:14.043378	f	t
1550	44	25	2017-07-29 13:52:14.043442	f	t
1551	46	13	2017-07-30 13:52:14.043507	t	t
1552	46	14	2017-08-04 13:52:14.043573	t	t
1553	46	22	2017-08-10 13:52:14.043639	t	t
1554	46	7	2017-07-24 13:52:14.043707	t	t
1555	46	17	2017-08-14 13:52:14.043772	t	t
1556	46	26	2017-08-15 13:52:14.043835	t	t
1557	46	34	2017-07-26 13:52:14.0439	t	t
1558	46	11	2017-08-05 13:52:14.043966	t	t
1559	46	13	2017-08-02 13:52:14.044027	f	t
1560	46	17	2017-07-30 13:52:14.044088	f	t
1561	46	7	2017-07-31 13:52:14.044155	f	t
1562	46	14	2017-07-26 13:52:14.044222	f	t
1563	46	26	2017-08-15 13:52:14.044289	f	t
1564	46	9	2017-08-03 13:52:14.044356	f	t
1565	46	21	2017-07-28 13:52:14.044423	f	t
1566	46	22	2017-07-31 13:52:14.04449	f	t
1567	46	16	2017-08-03 13:52:14.044558	f	t
1568	47	8	2017-07-28 13:52:14.044625	t	t
1569	47	24	2017-07-25 13:52:14.044693	t	t
1570	47	28	2017-07-31 13:52:14.04476	t	t
1571	47	16	2017-07-30 13:52:14.044828	t	t
1572	47	33	2017-08-06 13:52:14.044896	t	t
1573	47	27	2017-08-13 13:52:14.044963	t	t
1574	47	12	2017-07-27 13:52:14.04503	f	t
1575	49	18	2017-07-23 13:52:14.045097	t	t
1576	49	16	2017-08-13 13:52:14.045163	t	t
1577	49	28	2017-08-11 13:52:14.045231	t	t
1578	49	19	2017-08-16 13:52:14.045298	t	t
1579	49	33	2017-08-04 13:52:14.045364	t	t
1580	49	29	2017-07-24 13:52:14.045431	t	t
1581	49	8	2017-07-27 13:52:14.045495	t	t
1582	49	37	2017-07-27 13:52:14.04556	t	t
1583	49	24	2017-07-31 13:52:14.045623	t	t
1584	49	31	2017-08-08 13:52:14.045687	t	t
1585	49	17	2017-07-27 13:52:14.04575	t	t
1586	49	10	2017-07-24 13:52:14.045815	t	t
1587	49	25	2017-08-01 13:52:14.045885	t	t
1588	49	15	2017-08-06 13:52:14.045948	t	t
1589	49	13	2017-08-10 13:52:14.046013	t	t
1590	49	22	2017-07-29 13:52:14.046076	t	t
1591	49	7	2017-08-14 13:52:14.046141	f	t
1592	49	22	2017-07-30 13:52:14.046203	f	t
1593	50	13	2017-08-09 13:52:14.046264	t	t
1594	50	37	2017-08-03 13:52:14.046327	t	t
1595	50	26	2017-08-06 13:52:14.046391	t	t
1596	50	36	2017-07-24 13:52:14.046458	t	t
1597	50	32	2017-07-24 13:52:14.046526	f	t
1598	50	25	2017-08-08 13:52:14.046593	f	t
1599	51	14	2017-08-11 13:52:14.046659	t	t
1600	51	29	2017-07-28 13:52:14.046726	t	t
1601	51	31	2017-08-15 13:52:14.046793	t	t
1602	51	37	2017-08-07 13:52:14.046859	t	t
1603	51	7	2017-07-28 13:52:14.046926	t	t
1604	51	29	2017-08-17 13:52:14.046993	t	t
1605	51	20	2017-07-23 13:52:14.04706	t	t
1606	51	34	2017-08-06 13:52:14.047128	t	t
1607	51	9	2017-08-13 13:52:14.047194	t	t
1608	51	26	2017-07-23 13:52:14.047261	t	t
1609	51	17	2017-07-27 13:52:14.047329	f	t
1610	51	7	2017-08-14 13:52:14.047394	f	t
1611	51	25	2017-08-06 13:52:14.04746	f	t
1612	51	14	2017-08-11 13:52:14.047525	f	t
1613	51	12	2017-08-08 13:52:14.047592	f	t
1614	51	24	2017-08-13 13:52:14.047657	f	t
1615	51	15	2017-07-30 13:52:14.047723	f	t
1616	51	21	2017-07-31 13:52:14.047789	f	t
1617	51	20	2017-07-31 13:52:14.047855	f	t
1618	51	26	2017-08-01 13:52:14.047921	f	t
1619	51	9	2017-08-07 13:52:14.047987	f	t
1620	51	18	2017-07-30 13:52:14.048052	f	t
1621	51	36	2017-08-01 13:52:14.048116	f	t
1622	51	11	2017-08-10 13:52:14.048182	f	t
1623	51	23	2017-08-09 13:52:14.048249	f	t
1624	51	27	2017-07-26 13:52:14.048316	f	t
1625	51	19	2017-08-16 13:52:14.048378	f	t
1626	51	8	2017-08-12 13:52:14.048443	f	t
1627	51	32	2017-07-27 13:52:14.04851	f	t
1628	51	13	2017-07-24 13:52:14.048572	f	t
1629	51	29	2017-07-26 13:52:14.048638	f	t
1630	54	14	2017-08-09 13:52:14.048705	t	t
1631	54	18	2017-08-10 13:52:14.048772	t	t
1632	54	13	2017-08-03 13:52:14.048838	t	t
1633	54	9	2017-08-15 13:52:14.048906	t	t
1634	54	15	2017-07-25 13:52:14.048973	t	t
1635	54	37	2017-08-05 13:52:14.04904	t	t
1636	54	7	2017-08-01 13:52:14.049107	f	t
1637	54	19	2017-08-10 13:52:14.049173	f	t
1638	54	20	2017-08-05 13:52:14.04924	f	t
1639	54	13	2017-07-28 13:52:14.049307	f	t
1640	54	17	2017-08-11 13:52:14.049374	f	t
1641	54	21	2017-07-29 13:52:14.049441	f	t
1642	55	7	2017-08-01 13:52:14.049507	t	t
1643	55	34	2017-08-05 13:52:14.049575	t	t
1644	55	36	2017-08-04 13:52:14.04964	t	t
1645	55	31	2017-07-29 13:52:14.049704	t	t
1646	55	18	2017-08-06 13:52:14.049768	t	t
1647	55	13	2017-08-16 13:52:14.049833	t	t
1648	55	31	2017-07-23 13:52:14.049907	f	t
1649	55	9	2017-08-09 13:52:14.049973	f	t
1650	55	8	2017-08-06 13:52:14.050038	f	t
1651	55	24	2017-08-10 13:52:14.050103	f	t
1652	55	13	2017-08-14 13:52:14.050167	f	t
1653	55	32	2017-07-30 13:52:14.05023	f	t
1654	55	18	2017-07-25 13:52:14.050294	f	t
1655	55	20	2017-08-06 13:52:14.050356	f	t
1656	55	19	2017-08-02 13:52:14.050424	f	t
1657	55	11	2017-07-27 13:52:14.050493	f	t
1658	55	37	2017-08-15 13:52:14.05056	f	t
1659	56	37	2017-08-14 13:52:14.050627	t	t
1660	56	17	2017-08-17 13:52:14.050694	t	t
1661	56	35	2017-07-31 13:52:14.050761	t	t
1662	56	28	2017-08-08 13:52:14.050828	t	t
1663	56	29	2017-08-17 13:52:14.050895	t	t
1664	56	11	2017-08-06 13:52:14.050962	t	t
1665	56	13	2017-08-04 13:52:14.05103	t	t
1666	56	36	2017-08-09 13:52:14.051098	t	t
1667	56	28	2017-07-24 13:52:14.051165	f	t
1668	56	32	2017-08-09 13:52:14.051232	f	t
1669	56	13	2017-07-31 13:52:14.051299	f	t
1670	57	22	2017-08-10 13:52:14.051366	t	t
1671	57	21	2017-08-17 13:52:14.051431	t	t
1672	57	16	2017-07-24 13:52:14.051496	t	t
1673	57	27	2017-07-29 13:52:14.051561	t	t
1674	57	19	2017-07-28 13:52:14.051626	t	t
1675	57	34	2017-08-09 13:52:14.051692	f	t
1676	57	25	2017-07-29 13:52:14.051758	f	t
1677	57	37	2017-07-23 13:52:14.051821	f	t
1678	57	8	2017-07-29 13:52:14.051888	f	t
1679	57	32	2017-07-30 13:52:14.051952	f	t
1680	58	27	2017-08-06 13:52:14.052018	t	t
1681	58	12	2017-08-06 13:52:14.052084	t	t
1682	58	36	2017-08-10 13:52:14.05215	t	t
1683	58	33	2017-07-27 13:52:14.052215	f	t
1684	58	7	2017-08-07 13:52:14.052281	f	t
1685	58	37	2017-08-06 13:52:14.052348	f	t
1686	59	10	2017-08-12 13:52:14.052415	t	t
1687	59	24	2017-08-01 13:52:14.052479	t	t
1688	59	22	2017-08-01 13:52:14.052545	t	t
1689	59	14	2017-07-25 13:52:14.052609	f	t
1690	59	27	2017-08-07 13:52:14.052673	f	t
1691	59	31	2017-08-14 13:52:14.052735	f	t
1692	59	13	2017-07-27 13:52:14.052803	f	t
1693	59	20	2017-08-09 13:52:14.05287	f	t
1694	59	11	2017-07-23 13:52:14.052938	f	t
1695	59	23	2017-08-07 13:52:14.053007	f	t
1696	59	34	2017-08-17 13:52:14.053074	f	t
1697	59	12	2017-08-14 13:52:14.053142	f	t
1698	59	24	2017-08-16 13:52:14.053209	f	t
1699	59	18	2017-07-26 13:52:14.053276	f	t
1700	60	10	2017-08-04 13:52:14.053344	t	t
1701	60	14	2017-08-10 13:52:14.053412	t	t
1702	60	21	2017-07-28 13:52:14.053478	f	t
1703	61	19	2017-07-28 13:52:14.053546	t	t
1704	61	29	2017-08-17 13:52:14.053612	t	t
1705	61	20	2017-08-15 13:52:14.053679	t	t
1706	61	11	2017-08-03 13:52:14.053746	t	t
1707	61	16	2017-08-08 13:52:14.053813	t	t
1708	61	7	2017-08-06 13:52:14.053889	t	t
1709	61	28	2017-07-30 13:52:14.053955	t	t
1710	61	35	2017-08-14 13:52:14.05403	t	t
1711	61	36	2017-07-29 13:52:14.054096	f	t
1712	61	28	2017-08-07 13:52:14.054163	f	t
1713	61	24	2017-08-12 13:52:14.054229	f	t
1714	62	36	2017-07-25 13:52:14.054295	t	t
1715	62	10	2017-08-16 13:52:14.054361	t	t
1716	62	37	2017-07-27 13:52:14.054428	t	t
1717	62	21	2017-07-31 13:52:14.054495	t	t
1718	62	19	2017-08-10 13:52:14.054561	t	t
1719	62	20	2017-08-11 13:52:14.054625	t	t
1720	62	17	2017-08-09 13:52:14.054689	t	t
1721	62	24	2017-08-08 13:52:14.054754	t	t
1722	62	19	2017-08-12 13:52:14.054822	f	t
1723	62	21	2017-08-03 13:52:14.054891	f	t
1724	62	25	2017-08-10 13:52:14.05496	f	t
1725	62	23	2017-08-13 13:52:14.055036	f	t
1726	62	32	2017-07-30 13:52:14.055103	f	t
1727	62	26	2017-08-01 13:52:14.055169	f	t
1728	62	36	2017-08-07 13:52:14.055235	f	t
1729	62	16	2017-07-27 13:52:14.055301	f	t
1730	63	25	2017-08-12 13:52:14.055368	t	t
1731	63	27	2017-07-29 13:52:14.055436	t	t
1732	63	36	2017-08-11 13:52:14.055503	t	t
1733	63	24	2017-07-24 13:52:14.05557	t	t
1734	63	16	2017-08-13 13:52:14.055637	t	t
1735	63	21	2017-07-26 13:52:14.055704	t	t
1736	63	15	2017-08-03 13:52:14.055771	t	t
1737	63	31	2017-07-27 13:52:14.055837	t	t
1738	63	12	2017-08-04 13:52:14.055901	t	t
1739	63	9	2017-07-26 13:52:14.055967	t	t
1740	63	7	2017-07-31 13:52:14.056034	t	t
1741	63	26	2017-07-23 13:52:14.056099	t	t
1742	63	17	2017-08-12 13:52:14.056164	t	t
1743	63	19	2017-08-04 13:52:14.056231	t	t
1744	63	25	2017-08-15 13:52:14.056295	f	t
1745	63	10	2017-08-01 13:52:14.056363	f	t
1746	63	19	2017-08-17 13:52:14.056428	f	t
1747	63	21	2017-08-11 13:52:14.056493	f	t
1748	63	15	2017-08-13 13:52:14.056559	f	t
1749	63	18	2017-07-29 13:52:14.056625	f	t
1750	63	22	2017-07-23 13:52:14.056692	f	t
1751	63	29	2017-07-30 13:52:14.056756	f	t
1752	63	35	2017-08-11 13:52:14.056821	f	t
1753	63	11	2017-08-02 13:52:14.056886	f	t
1754	63	8	2017-07-29 13:52:14.056949	f	t
1755	63	34	2017-07-29 13:52:14.057011	f	t
1756	63	17	2017-08-03 13:52:14.057076	f	t
1757	63	29	2017-08-01 13:52:14.057143	f	t
1758	63	27	2017-08-05 13:52:14.057209	f	t
1759	63	36	2017-08-06 13:52:14.057274	f	t
1760	63	26	2017-08-04 13:52:14.057341	f	t
1761	63	28	2017-07-24 13:52:14.057408	f	t
1762	64	27	2017-08-05 13:52:14.057474	t	t
1763	64	15	2017-08-16 13:52:14.05754	t	t
1764	64	34	2017-08-16 13:52:14.057607	t	t
1765	64	7	2017-07-30 13:52:14.057675	f	t
1766	64	26	2017-08-01 13:52:14.057743	f	t
1767	64	24	2017-08-15 13:52:14.057812	f	t
1768	64	15	2017-08-17 13:52:14.057914	f	t
1769	64	16	2017-08-07 13:52:14.057984	f	t
1770	64	13	2017-08-11 13:52:14.058051	f	t
1771	64	8	2017-07-27 13:52:14.058116	f	t
1772	64	37	2017-08-08 13:52:14.05818	f	t
1773	64	14	2017-08-16 13:52:14.058245	f	t
1774	65	7	2017-08-12 13:52:14.05831	t	t
1775	65	33	2017-08-14 13:52:14.058373	f	t
1776	65	17	2017-08-06 13:52:14.058437	f	t
1777	65	11	2017-07-23 13:52:14.058541	f	t
1778	65	27	2017-07-27 13:52:14.058607	f	t
1779	65	16	2017-07-26 13:52:14.05867	f	t
1780	65	15	2017-08-16 13:52:14.058733	f	t
1781	66	15	2017-07-27 13:52:14.058799	t	t
1782	66	7	2017-08-14 13:52:14.058867	t	t
1783	66	34	2017-08-01 13:52:14.058935	t	t
1784	66	9	2017-07-29 13:52:14.059002	t	t
1785	66	28	2017-07-25 13:52:14.059068	t	t
1786	66	25	2017-08-08 13:52:14.059135	t	t
1787	66	37	2017-08-02 13:52:14.059203	t	t
1788	66	23	2017-08-13 13:52:14.05927	t	t
1789	66	10	2017-07-23 13:52:14.059337	t	t
1790	66	29	2017-08-08 13:52:14.059403	t	t
1791	66	12	2017-08-07 13:52:14.059471	t	t
1792	66	33	2017-07-27 13:52:14.059539	t	t
1793	66	21	2017-07-26 13:52:14.059606	t	t
1794	66	36	2017-08-01 13:52:14.059673	f	t
1795	66	28	2017-08-08 13:52:14.059738	f	t
1796	66	7	2017-08-13 13:52:14.059805	f	t
1797	66	19	2017-07-30 13:52:14.059871	f	t
1798	67	22	2017-08-01 13:52:14.059936	t	t
1799	67	18	2017-08-06 13:52:14.060002	t	t
1800	67	21	2017-08-01 13:52:14.060068	t	t
1801	67	12	2017-07-28 13:52:14.060134	t	t
1802	67	19	2017-08-05 13:52:14.060198	t	t
1803	67	28	2017-08-11 13:52:14.060264	t	t
1804	67	7	2017-08-15 13:52:14.060329	f	t
1805	67	12	2017-08-04 13:52:14.060395	f	t
1806	67	35	2017-08-16 13:52:14.060461	f	t
1807	67	25	2017-08-15 13:52:14.060526	f	t
1808	67	24	2017-07-28 13:52:14.060591	f	t
1809	68	32	2017-08-07 13:52:14.060656	t	t
1810	68	29	2017-08-11 13:52:14.060723	t	t
1811	68	31	2017-08-17 13:52:14.06079	t	t
1812	68	16	2017-08-05 13:52:14.060853	t	t
1813	68	12	2017-08-15 13:52:14.060917	f	t
1814	68	14	2017-07-25 13:52:14.060982	f	t
1815	68	17	2017-07-23 13:52:14.061046	f	t
1816	68	24	2017-08-05 13:52:14.061107	f	t
1817	68	36	2017-08-15 13:52:14.061172	f	t
1818	68	29	2017-08-09 13:52:14.061239	f	t
1819	68	16	2017-07-27 13:52:14.061306	f	t
1820	68	33	2017-08-08 13:52:14.061372	f	t
1821	68	31	2017-08-02 13:52:14.061439	f	t
1822	6	16	2017-07-25 13:52:14.061506	t	t
1823	6	35	2017-08-01 13:52:14.061572	t	t
1824	6	37	2017-08-02 13:52:14.061639	t	t
1825	6	9	2017-07-31 13:52:14.061706	t	t
1826	6	36	2017-07-25 13:52:14.061773	t	t
1827	6	34	2017-07-30 13:52:14.06184	t	t
1828	6	18	2017-08-06 13:52:14.061916	t	t
1829	6	15	2017-07-30 13:52:14.061983	t	t
1830	6	12	2017-08-01 13:52:14.06205	t	t
1831	6	22	2017-08-09 13:52:14.062119	t	t
1832	6	17	2017-08-17 13:52:14.062186	t	t
1833	6	36	2017-08-08 13:52:14.062253	f	t
1834	6	35	2017-08-14 13:52:14.06232	f	t
1835	7	17	2017-08-01 13:52:14.062385	t	t
1836	7	15	2017-08-12 13:52:14.062449	t	t
1837	9	11	2017-08-10 13:52:14.062514	t	t
1838	9	28	2017-07-28 13:52:14.062578	t	t
1839	9	17	2017-07-25 13:52:14.062642	t	t
1840	9	37	2017-08-11 13:52:14.062705	t	t
1841	9	37	2017-07-29 13:52:14.062767	f	t
1842	9	14	2017-07-27 13:52:14.062832	f	t
1843	9	13	2017-07-26 13:52:14.062895	f	t
1844	9	28	2017-08-11 13:52:14.062959	f	t
1845	9	12	2017-08-01 13:52:14.063021	f	t
1846	13	14	2017-07-29 13:52:14.063082	t	t
1847	13	15	2017-08-02 13:52:14.063147	t	t
1848	13	25	2017-08-01 13:52:14.063213	t	t
1849	13	21	2017-08-05 13:52:14.06328	t	t
1850	13	11	2017-08-07 13:52:14.063348	t	t
1851	13	37	2017-07-30 13:52:14.063414	t	t
1852	13	31	2017-08-06 13:52:14.063482	t	t
1853	13	26	2017-07-23 13:52:14.063548	t	t
1854	13	20	2017-07-28 13:52:14.063614	t	t
1855	13	9	2017-07-27 13:52:14.063682	t	t
1856	13	28	2017-08-09 13:52:14.063749	t	t
1857	13	33	2017-08-10 13:52:14.063815	t	t
1858	13	17	2017-07-23 13:52:14.063881	t	t
1859	13	34	2017-07-31 13:52:14.063948	t	t
1860	13	35	2017-07-31 13:52:14.064014	t	t
1861	13	13	2017-08-16 13:52:14.064081	t	t
1862	13	7	2017-07-23 13:52:14.064148	f	t
1863	13	34	2017-07-30 13:52:14.064213	f	t
1864	13	15	2017-08-11 13:52:14.064279	f	t
1865	13	25	2017-08-07 13:52:14.064344	f	t
1866	13	36	2017-08-05 13:52:14.06441	f	t
1867	13	10	2017-08-10 13:52:14.064476	f	t
1868	13	16	2017-08-08 13:52:14.064542	f	t
1869	13	24	2017-08-09 13:52:14.064607	f	t
1870	13	29	2017-07-23 13:52:14.064672	f	t
1871	13	26	2017-08-11 13:52:14.064739	f	t
1872	14	17	2017-08-13 13:52:14.064804	t	t
1873	14	27	2017-08-03 13:52:14.064871	t	t
1874	14	8	2017-08-10 13:52:14.064936	t	t
1875	14	31	2017-07-28 13:52:14.065004	t	t
1876	14	31	2017-08-17 13:52:14.065071	f	t
1877	14	10	2017-07-31 13:52:14.065136	f	t
1878	14	9	2017-08-02 13:52:14.065199	f	t
1879	14	26	2017-08-05 13:52:14.065264	f	t
1880	14	24	2017-08-09 13:52:14.065329	f	t
1881	18	14	2017-08-01 13:52:14.065391	f	t
1882	18	21	2017-08-14 13:52:14.065457	f	t
1883	18	27	2017-07-24 13:52:14.065525	f	t
1884	18	13	2017-07-24 13:52:14.065592	f	t
1885	18	20	2017-08-09 13:52:14.065661	f	t
1886	22	19	2017-08-15 13:52:14.06573	t	t
1887	22	12	2017-08-13 13:52:14.065798	t	t
1888	22	29	2017-08-10 13:52:14.065872	f	t
1889	22	35	2017-07-30 13:52:14.065941	f	t
1890	22	23	2017-07-24 13:52:14.066009	f	t
1891	22	22	2017-08-15 13:52:14.066077	f	t
1892	22	25	2017-08-12 13:52:14.066145	f	t
1893	22	18	2017-08-05 13:52:14.066213	f	t
1894	22	34	2017-07-23 13:52:14.066279	f	t
1895	25	13	2017-08-08 13:52:14.066347	t	t
1896	25	19	2017-08-07 13:52:14.066413	t	t
1897	25	33	2017-08-16 13:52:14.066478	t	t
1898	25	36	2017-07-31 13:52:14.066543	t	t
1899	25	36	2017-08-17 13:52:14.066607	f	t
1900	25	29	2017-07-26 13:52:14.066671	f	t
1901	31	18	2017-07-26 13:52:14.066735	t	t
1902	31	17	2017-07-28 13:52:14.066799	f	t
1903	31	26	2017-07-30 13:52:14.066863	f	t
1904	31	32	2017-07-28 13:52:14.066927	f	t
1905	31	34	2017-08-02 13:52:14.066992	f	t
1906	31	28	2017-07-23 13:52:14.067054	f	t
1907	31	9	2017-08-06 13:52:14.067118	f	t
1908	31	35	2017-08-08 13:52:14.067182	f	t
1909	33	21	2017-08-13 13:52:14.06725	f	t
1910	33	16	2017-08-03 13:52:14.067318	f	t
1911	33	15	2017-08-07 13:52:14.067386	f	t
1912	33	12	2017-07-31 13:52:14.067452	f	t
1913	37	29	2017-08-13 13:52:14.06752	f	t
1914	37	37	2017-08-04 13:52:14.067587	f	t
1915	37	11	2017-07-30 13:52:14.067656	f	t
1916	38	18	2017-07-27 13:52:14.067722	t	t
1917	38	14	2017-08-15 13:52:14.067789	t	t
1918	38	10	2017-08-17 13:52:14.067856	t	t
1919	43	36	2017-08-04 13:52:14.067923	t	t
1920	43	12	2017-07-27 13:52:14.067992	t	t
1921	43	17	2017-08-01 13:52:14.06807	f	t
1922	43	27	2017-07-29 13:52:14.068139	f	t
1923	45	27	2017-07-29 13:52:14.068209	t	t
1924	45	28	2017-08-08 13:52:14.068277	t	t
1925	45	26	2017-08-17 13:52:14.068344	t	t
1926	45	33	2017-08-12 13:52:14.068411	t	t
1927	45	29	2017-07-26 13:52:14.06848	t	t
1928	45	7	2017-07-24 13:52:14.068549	t	t
1929	45	29	2017-08-17 13:52:14.068617	t	t
1930	45	31	2017-07-29 13:52:14.068684	t	t
1931	45	34	2017-08-06 13:52:14.068752	t	t
1932	45	17	2017-08-08 13:52:14.068821	t	t
1933	45	36	2017-08-15 13:52:14.068888	t	t
1934	45	11	2017-07-30 13:52:14.068956	t	t
1935	45	37	2017-07-28 13:52:14.069031	t	t
1936	45	22	2017-08-05 13:52:14.069096	t	t
1937	45	25	2017-08-03 13:52:14.069163	t	t
1938	45	33	2017-08-05 13:52:14.069229	f	t
1939	45	17	2017-08-07 13:52:14.069293	f	t
1940	48	9	2017-08-13 13:52:14.069357	t	t
1941	48	37	2017-08-02 13:52:14.069423	t	t
1942	48	24	2017-08-01 13:52:14.069487	t	t
1943	48	16	2017-07-29 13:52:14.069549	t	t
1944	48	13	2017-08-01 13:52:14.069614	t	t
1945	48	27	2017-07-28 13:52:14.069682	t	t
1946	48	14	2017-08-01 13:52:14.06975	t	t
1947	48	23	2017-08-08 13:52:14.069818	t	t
1948	48	25	2017-08-07 13:52:14.069894	f	t
1949	48	26	2017-08-13 13:52:14.069963	f	t
1950	48	12	2017-07-23 13:52:14.07003	f	t
1951	48	29	2017-07-26 13:52:14.070099	f	t
1952	48	20	2017-07-30 13:52:14.070166	f	t
1953	52	9	2017-08-09 13:52:14.070233	t	t
1954	52	11	2017-07-25 13:52:14.0703	t	t
1955	52	15	2017-08-07 13:52:14.070367	t	t
1956	52	35	2017-08-06 13:52:14.070434	t	t
1957	52	22	2017-08-11 13:52:14.070501	t	t
1958	52	14	2017-08-10 13:52:14.070568	t	t
1959	52	37	2017-07-28 13:52:14.070635	f	t
1960	52	31	2017-07-23 13:52:14.070701	f	t
1961	52	32	2017-08-16 13:52:14.070768	f	t
1962	53	14	2017-08-03 13:52:14.070833	t	t
1963	69	25	2017-08-07 13:52:14.070896	t	t
1964	69	29	2017-07-30 13:52:14.070959	t	t
1965	69	9	2017-08-14 13:52:14.071024	t	t
1966	69	31	2017-08-14 13:52:14.071089	t	t
1967	69	27	2017-08-14 13:52:14.071151	t	t
1968	69	13	2017-08-17 13:52:14.071215	t	t
1969	69	35	2017-08-11 13:52:14.071279	t	t
1970	69	29	2017-08-02 13:52:14.071343	t	t
1971	69	16	2017-08-08 13:52:14.071408	t	t
1972	69	34	2017-08-17 13:52:14.07147	t	t
1973	69	22	2017-08-07 13:52:14.071531	t	t
1974	69	32	2017-07-26 13:52:14.071595	t	t
1975	69	37	2017-07-26 13:52:14.071663	t	t
1976	69	17	2017-07-23 13:52:14.071729	t	t
1977	69	34	2017-08-06 13:52:14.071797	f	t
1978	69	29	2017-08-03 13:52:14.071862	f	t
1979	69	33	2017-08-03 13:52:14.071928	f	t
1980	69	13	2017-08-15 13:52:14.071995	f	t
1981	69	8	2017-08-07 13:52:14.072062	f	t
1982	69	17	2017-07-28 13:52:14.072129	f	t
1983	69	27	2017-07-28 13:52:14.072195	f	t
1984	69	15	2017-08-03 13:52:14.072261	f	t
1985	69	7	2017-08-07 13:52:14.072328	f	t
1986	69	26	2017-08-09 13:52:14.072396	f	t
1987	69	21	2017-08-01 13:52:14.072463	f	t
1988	69	16	2017-08-15 13:52:14.072529	f	t
1989	69	22	2017-07-28 13:52:14.072596	f	t
1990	69	18	2017-08-14 13:52:14.07266	f	t
1991	69	37	2017-07-30 13:52:14.072727	f	t
1992	69	35	2017-08-14 13:52:14.072793	f	t
\.


--
-- Name: clicked_arguments_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('clicked_arguments_uid_seq', 1992, true);


--
-- Data for Name: clicked_statements; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY clicked_statements (uid, statement_uid, author_uid, "timestamp", is_up_vote, is_valid) FROM stdin;
1095	1	14	2017-07-23 13:52:13.444222	t	t
1096	1	23	2017-08-05 13:52:13.44442	f	t
1097	1	32	2017-08-02 13:52:13.444501	f	t
1098	2	31	2017-07-23 13:52:13.444577	t	t
1099	2	22	2017-07-28 13:52:13.444649	f	t
1100	2	26	2017-08-04 13:52:13.444718	f	t
1101	2	33	2017-08-11 13:52:13.444787	f	t
1102	2	10	2017-08-02 13:52:13.444855	f	t
1103	2	16	2017-08-03 13:52:13.444924	f	t
1104	2	35	2017-08-02 13:52:13.444993	f	t
1105	2	14	2017-07-23 13:52:13.445061	f	t
1106	2	29	2017-07-24 13:52:13.445128	f	t
1107	2	11	2017-08-13 13:52:13.445197	f	t
1108	2	19	2017-08-16 13:52:13.445266	f	t
1109	2	33	2017-07-29 13:52:13.445334	f	t
1110	2	33	2017-07-31 13:52:13.445402	f	t
1111	2	20	2017-07-30 13:52:13.445469	f	t
1112	2	14	2017-07-27 13:52:13.445537	f	t
1113	3	36	2017-08-01 13:52:13.445604	t	t
1114	3	24	2017-08-03 13:52:13.44567	t	t
1115	3	16	2017-08-04 13:52:13.445737	t	t
1116	3	23	2017-08-11 13:52:13.445804	t	t
1117	3	9	2017-07-28 13:52:13.445881	t	t
1118	3	18	2017-08-05 13:52:13.44595	f	t
1119	3	14	2017-08-17 13:52:13.446017	f	t
1120	3	34	2017-08-09 13:52:13.446084	f	t
1121	4	9	2017-08-02 13:52:13.446151	t	t
1122	4	23	2017-08-05 13:52:13.446219	t	t
1123	4	29	2017-08-09 13:52:13.446285	t	t
1124	4	11	2017-08-15 13:52:13.446352	t	t
1125	4	24	2017-08-07 13:52:13.446419	t	t
1126	4	25	2017-07-26 13:52:13.446486	t	t
1127	4	23	2017-08-13 13:52:13.446553	t	t
1128	4	26	2017-07-26 13:52:13.44662	t	t
1129	4	19	2017-08-06 13:52:13.446686	t	t
1130	4	35	2017-08-11 13:52:13.446753	t	t
1131	4	21	2017-08-14 13:52:13.446818	t	t
1132	4	35	2017-07-28 13:52:13.446882	f	t
1133	4	11	2017-08-03 13:52:13.446946	f	t
1134	4	25	2017-07-27 13:52:13.447011	f	t
1135	4	10	2017-08-15 13:52:13.447076	f	t
1136	4	32	2017-08-06 13:52:13.447141	f	t
1137	4	10	2017-08-09 13:52:13.447206	f	t
1138	4	36	2017-08-10 13:52:13.447273	f	t
1139	4	12	2017-08-09 13:52:13.447339	f	t
1140	4	25	2017-07-29 13:52:13.447407	f	t
1141	4	33	2017-08-14 13:52:13.447473	f	t
1142	4	17	2017-08-15 13:52:13.44754	f	t
1143	4	31	2017-07-31 13:52:13.447607	f	t
1144	4	15	2017-08-02 13:52:13.447674	f	t
1145	4	24	2017-08-03 13:52:13.447739	f	t
1146	4	29	2017-08-12 13:52:13.447805	f	t
1147	4	22	2017-08-15 13:52:13.447872	f	t
1148	4	29	2017-08-07 13:52:13.447939	f	t
1149	4	32	2017-08-06 13:52:13.448005	f	t
1150	5	33	2017-08-04 13:52:13.448071	t	t
1151	5	14	2017-08-08 13:52:13.44814	t	t
1152	5	25	2017-08-11 13:52:13.448207	t	t
1153	5	10	2017-07-31 13:52:13.448274	t	t
1154	5	29	2017-08-16 13:52:13.448341	t	t
1155	5	10	2017-08-05 13:52:13.448408	t	t
1156	5	20	2017-07-31 13:52:13.448475	t	t
1157	5	20	2017-07-24 13:52:13.448542	t	t
1158	5	11	2017-07-23 13:52:13.448608	t	t
1159	5	29	2017-08-10 13:52:13.448673	t	t
1160	5	15	2017-08-10 13:52:13.448738	t	t
1161	5	21	2017-08-04 13:52:13.448803	t	t
1162	5	20	2017-08-05 13:52:13.448869	t	t
1163	5	31	2017-08-13 13:52:13.448933	t	t
1164	5	15	2017-08-14 13:52:13.448999	t	t
1165	5	10	2017-08-17 13:52:13.449066	t	t
1166	5	23	2017-08-04 13:52:13.449133	t	t
1167	5	24	2017-08-15 13:52:13.4492	f	t
1168	5	19	2017-08-06 13:52:13.449267	f	t
1169	5	35	2017-07-23 13:52:13.449334	f	t
1170	5	26	2017-07-27 13:52:13.449402	f	t
1171	5	34	2017-07-31 13:52:13.449468	f	t
1172	5	19	2017-08-12 13:52:13.449533	f	t
1173	5	14	2017-08-07 13:52:13.449598	f	t
1174	5	19	2017-07-26 13:52:13.449663	f	t
1175	5	24	2017-08-14 13:52:13.449728	f	t
1176	5	28	2017-07-26 13:52:13.449793	f	t
1177	5	8	2017-07-29 13:52:13.449864	f	t
1178	6	26	2017-07-26 13:52:13.449933	t	t
1179	6	31	2017-08-06 13:52:13.450001	t	t
1180	6	8	2017-08-01 13:52:13.450068	t	t
1181	6	11	2017-07-31 13:52:13.450136	t	t
1182	6	7	2017-08-10 13:52:13.450202	t	t
1183	6	33	2017-07-31 13:52:13.450268	t	t
1184	6	36	2017-08-01 13:52:13.450334	t	t
1185	6	28	2017-08-12 13:52:13.450394	t	t
1186	6	34	2017-08-03 13:52:13.450452	f	t
1187	6	27	2017-08-11 13:52:13.45051	f	t
1188	6	8	2017-07-29 13:52:13.450567	f	t
1189	6	24	2017-08-06 13:52:13.450623	f	t
1190	6	34	2017-07-27 13:52:13.450679	f	t
1191	6	36	2017-08-14 13:52:13.450741	f	t
1192	6	21	2017-08-17 13:52:13.450803	f	t
1193	6	33	2017-08-02 13:52:13.45086	f	t
1194	6	8	2017-08-15 13:52:13.450917	f	t
1195	6	7	2017-08-14 13:52:13.450974	f	t
1196	6	24	2017-07-24 13:52:13.451031	f	t
1197	6	9	2017-08-15 13:52:13.451088	f	t
1198	6	14	2017-08-12 13:52:13.451147	f	t
1199	6	35	2017-08-11 13:52:13.451207	f	t
1200	7	18	2017-08-11 13:52:13.45127	t	t
1201	7	10	2017-08-09 13:52:13.451332	t	t
1202	7	14	2017-08-05 13:52:13.451398	f	t
1203	7	31	2017-08-04 13:52:13.451462	f	t
1204	7	10	2017-08-03 13:52:13.451528	f	t
1205	7	9	2017-07-24 13:52:13.451593	f	t
1206	7	31	2017-08-05 13:52:13.451658	f	t
1207	7	34	2017-08-06 13:52:13.451724	f	t
1208	7	14	2017-08-06 13:52:13.45179	f	t
1209	7	31	2017-08-02 13:52:13.451856	f	t
1210	7	37	2017-08-10 13:52:13.45192	f	t
1211	7	22	2017-08-14 13:52:13.451986	f	t
1212	7	31	2017-07-31 13:52:13.452052	f	t
1213	8	9	2017-08-01 13:52:13.452117	f	t
1214	8	22	2017-08-01 13:52:13.452182	f	t
1215	8	35	2017-07-30 13:52:13.452248	f	t
1216	9	21	2017-08-05 13:52:13.452314	t	t
1217	9	28	2017-08-10 13:52:13.452378	t	t
1218	9	16	2017-07-31 13:52:13.452442	t	t
1219	9	20	2017-08-15 13:52:13.452507	t	t
1220	9	22	2017-08-11 13:52:13.452572	t	t
1221	9	10	2017-08-15 13:52:13.452638	t	t
1222	9	21	2017-08-06 13:52:13.452704	t	t
1223	9	22	2017-07-26 13:52:13.452769	t	t
1224	9	7	2017-08-12 13:52:13.452834	t	t
1225	9	18	2017-08-14 13:52:13.452899	t	t
1226	9	12	2017-08-09 13:52:13.452964	t	t
1227	9	20	2017-08-07 13:52:13.45303	t	t
1228	9	26	2017-07-26 13:52:13.453095	t	t
1229	9	20	2017-07-24 13:52:13.453161	t	t
1230	9	36	2017-07-24 13:52:13.453227	t	t
1231	9	29	2017-07-23 13:52:13.453292	f	t
1232	9	15	2017-07-25 13:52:13.453356	f	t
1233	9	14	2017-07-30 13:52:13.453421	f	t
1234	9	20	2017-07-24 13:52:13.453485	f	t
1235	9	20	2017-08-15 13:52:13.453551	f	t
1236	9	29	2017-08-08 13:52:13.453617	f	t
1237	9	9	2017-08-17 13:52:13.453682	f	t
1238	9	37	2017-08-17 13:52:13.453746	f	t
1239	9	29	2017-07-29 13:52:13.453811	f	t
1240	9	27	2017-08-17 13:52:13.453885	f	t
1241	9	20	2017-08-07 13:52:13.453951	f	t
1242	9	16	2017-08-17 13:52:13.454017	f	t
1243	9	19	2017-08-08 13:52:13.454082	f	t
1244	9	22	2017-08-06 13:52:13.454146	f	t
1245	9	28	2017-07-28 13:52:13.454213	f	t
1246	9	7	2017-08-14 13:52:13.454281	f	t
1247	9	19	2017-08-12 13:52:13.454349	f	t
1248	10	21	2017-07-30 13:52:13.454416	t	t
1249	10	22	2017-08-09 13:52:13.454481	t	t
1250	10	35	2017-08-07 13:52:13.454547	t	t
1251	10	11	2017-08-10 13:52:13.454615	t	t
1252	10	17	2017-08-04 13:52:13.454682	t	t
1253	10	37	2017-08-04 13:52:13.454749	t	t
1254	10	9	2017-08-06 13:52:13.454816	t	t
1255	10	28	2017-07-30 13:52:13.454883	t	t
1256	10	29	2017-08-04 13:52:13.45495	t	t
1257	10	12	2017-08-02 13:52:13.455016	f	t
1258	10	25	2017-08-09 13:52:13.455083	f	t
1259	10	25	2017-07-26 13:52:13.45515	f	t
1260	11	22	2017-07-24 13:52:13.455218	t	t
1261	11	10	2017-08-05 13:52:13.455286	f	t
1262	11	9	2017-07-31 13:52:13.455353	f	t
1263	11	21	2017-08-10 13:52:13.45542	f	t
1264	11	13	2017-08-05 13:52:13.455487	f	t
1265	11	23	2017-08-06 13:52:13.455553	f	t
1266	11	25	2017-08-13 13:52:13.455619	f	t
1267	11	22	2017-08-03 13:52:13.455685	f	t
1268	11	23	2017-07-27 13:52:13.455751	f	t
1269	12	16	2017-08-04 13:52:13.455817	t	t
1270	12	28	2017-08-08 13:52:13.455885	t	t
1271	12	16	2017-07-26 13:52:13.455952	t	t
1272	12	24	2017-07-31 13:52:13.456019	t	t
1273	12	28	2017-08-04 13:52:13.456086	t	t
1274	12	13	2017-08-16 13:52:13.456151	t	t
1275	12	12	2017-08-10 13:52:13.456218	f	t
1276	12	27	2017-08-17 13:52:13.456284	f	t
1277	13	23	2017-08-17 13:52:13.45635	t	t
1278	13	7	2017-08-15 13:52:13.456415	t	t
1279	13	33	2017-08-03 13:52:13.456483	f	t
1280	13	12	2017-08-15 13:52:13.456549	f	t
1281	13	22	2017-07-23 13:52:13.456615	f	t
1282	14	33	2017-07-31 13:52:13.456682	t	t
1283	14	11	2017-08-08 13:52:13.456749	t	t
1284	14	35	2017-08-06 13:52:13.456816	t	t
1285	15	13	2017-08-05 13:52:13.456882	f	t
1286	16	33	2017-07-24 13:52:13.456949	t	t
1287	16	21	2017-07-29 13:52:13.457016	t	t
1288	16	31	2017-08-05 13:52:13.457082	t	t
1289	16	15	2017-07-29 13:52:13.457149	t	t
1290	16	15	2017-08-11 13:52:13.457215	t	t
1291	16	12	2017-07-31 13:52:13.457281	t	t
1292	16	20	2017-08-14 13:52:13.457347	t	t
1293	16	33	2017-07-30 13:52:13.457414	t	t
1294	16	19	2017-08-16 13:52:13.457481	t	t
1295	16	33	2017-07-26 13:52:13.457549	t	t
1296	16	13	2017-08-02 13:52:13.457616	t	t
1297	16	24	2017-07-28 13:52:13.457682	t	t
1298	16	33	2017-08-01 13:52:13.45775	t	t
1299	16	11	2017-08-13 13:52:13.457816	t	t
1300	16	35	2017-07-23 13:52:13.457892	t	t
1301	16	14	2017-08-04 13:52:13.45796	f	t
1302	16	16	2017-08-01 13:52:13.458027	f	t
1303	17	27	2017-08-01 13:52:13.458093	t	t
1304	17	24	2017-07-27 13:52:13.45816	t	t
1305	17	32	2017-08-01 13:52:13.458229	t	t
1306	17	20	2017-08-08 13:52:13.458295	t	t
1307	17	25	2017-08-10 13:52:13.458363	t	t
1308	17	28	2017-08-04 13:52:13.45843	t	t
1309	17	23	2017-08-14 13:52:13.458497	f	t
1310	17	18	2017-08-17 13:52:13.458564	f	t
1311	17	32	2017-07-30 13:52:13.45863	f	t
1312	17	26	2017-07-31 13:52:13.458697	f	t
1313	17	25	2017-07-24 13:52:13.458764	f	t
1314	17	36	2017-08-17 13:52:13.458831	f	t
1315	18	37	2017-08-08 13:52:13.458898	t	t
1316	18	36	2017-08-08 13:52:13.458965	f	t
1317	18	24	2017-08-06 13:52:13.459031	f	t
1318	18	28	2017-08-15 13:52:13.459097	f	t
1319	18	36	2017-07-31 13:52:13.459164	f	t
1320	18	23	2017-08-07 13:52:13.459232	f	t
1321	18	18	2017-08-05 13:52:13.459298	f	t
1322	18	31	2017-07-27 13:52:13.459366	f	t
1323	18	28	2017-08-09 13:52:13.459432	f	t
1324	19	16	2017-07-23 13:52:13.4595	t	t
1325	19	13	2017-08-01 13:52:13.459567	f	t
1326	19	22	2017-08-10 13:52:13.459633	f	t
1327	20	11	2017-08-02 13:52:13.459699	t	t
1328	20	22	2017-07-27 13:52:13.459766	t	t
1329	20	13	2017-07-26 13:52:13.459832	t	t
1330	20	28	2017-08-06 13:52:13.459899	t	t
1331	20	33	2017-07-24 13:52:13.459967	t	t
1332	20	13	2017-07-30 13:52:13.460033	t	t
1333	20	13	2017-08-03 13:52:13.4601	t	t
1334	20	23	2017-08-17 13:52:13.460167	t	t
1335	20	14	2017-07-26 13:52:13.460232	t	t
1336	20	25	2017-08-17 13:52:13.460299	t	t
1337	20	29	2017-08-16 13:52:13.460366	t	t
1338	20	17	2017-07-30 13:52:13.460434	t	t
1339	20	18	2017-08-03 13:52:13.460503	t	t
1340	20	31	2017-08-07 13:52:13.460571	t	t
1341	20	26	2017-08-08 13:52:13.460638	t	t
1342	20	34	2017-08-16 13:52:13.460705	t	t
1343	20	24	2017-08-08 13:52:13.460772	t	t
1344	20	37	2017-08-09 13:52:13.460882	f	t
1345	20	24	2017-07-30 13:52:13.460949	f	t
1346	20	18	2017-07-23 13:52:13.461013	f	t
1347	20	37	2017-08-17 13:52:13.461079	f	t
1348	20	16	2017-07-25 13:52:13.461146	f	t
1349	20	10	2017-08-11 13:52:13.461211	f	t
1350	20	9	2017-08-14 13:52:13.461276	f	t
1351	20	12	2017-07-28 13:52:13.461341	f	t
1352	20	9	2017-08-05 13:52:13.461406	f	t
1353	20	17	2017-08-13 13:52:13.461473	f	t
1354	20	24	2017-08-11 13:52:13.46154	f	t
1355	20	33	2017-08-12 13:52:13.461608	f	t
1356	20	28	2017-08-04 13:52:13.461675	f	t
1357	20	31	2017-08-05 13:52:13.461741	f	t
1358	20	13	2017-08-16 13:52:13.461807	f	t
1359	20	9	2017-08-08 13:52:13.461889	f	t
1360	20	25	2017-08-14 13:52:13.461958	f	t
1361	20	13	2017-08-10 13:52:13.462025	f	t
1362	20	20	2017-07-30 13:52:13.462093	f	t
1363	20	26	2017-08-14 13:52:13.46216	f	t
1364	20	19	2017-07-26 13:52:13.462227	f	t
1365	20	25	2017-07-27 13:52:13.462293	f	t
1366	21	25	2017-08-14 13:52:13.46236	t	t
1367	21	24	2017-07-27 13:52:13.462429	t	t
1368	21	18	2017-07-23 13:52:13.462497	f	t
1369	21	33	2017-08-02 13:52:13.462566	f	t
1370	21	16	2017-08-17 13:52:13.462633	f	t
1371	21	10	2017-08-16 13:52:13.4627	f	t
1372	21	35	2017-08-04 13:52:13.462769	f	t
1373	22	11	2017-08-06 13:52:13.462835	t	t
1374	22	10	2017-08-02 13:52:13.462903	t	t
1375	22	31	2017-08-17 13:52:13.462971	f	t
1376	22	13	2017-08-08 13:52:13.463038	f	t
1377	22	14	2017-08-01 13:52:13.463106	f	t
1378	22	36	2017-08-04 13:52:13.463172	f	t
1379	22	17	2017-08-12 13:52:13.463239	f	t
1380	22	31	2017-08-06 13:52:13.463306	f	t
1381	22	19	2017-08-13 13:52:13.463374	f	t
1382	22	29	2017-08-15 13:52:13.463441	f	t
1383	22	29	2017-08-07 13:52:13.463509	f	t
1384	22	29	2017-08-11 13:52:13.463576	f	t
1385	22	22	2017-08-11 13:52:13.463642	f	t
1386	22	29	2017-08-11 13:52:13.463708	f	t
1387	22	29	2017-07-27 13:52:13.463772	f	t
1388	22	10	2017-07-23 13:52:13.46383	f	t
1389	22	9	2017-08-15 13:52:13.46389	f	t
1390	22	20	2017-08-17 13:52:13.463949	f	t
1391	22	25	2017-07-23 13:52:13.464009	f	t
1392	24	36	2017-08-11 13:52:13.464072	f	t
1393	24	31	2017-07-31 13:52:13.464136	f	t
1394	24	26	2017-08-16 13:52:13.4642	f	t
1395	24	31	2017-07-29 13:52:13.464265	f	t
1396	25	34	2017-08-05 13:52:13.46433	t	t
1397	25	37	2017-08-03 13:52:13.464396	t	t
1398	25	16	2017-07-25 13:52:13.464462	t	t
1399	25	8	2017-08-15 13:52:13.464528	t	t
1400	25	7	2017-08-01 13:52:13.464596	f	t
1401	25	20	2017-07-29 13:52:13.464663	f	t
1402	25	37	2017-08-06 13:52:13.464729	f	t
1403	25	29	2017-07-29 13:52:13.464796	f	t
1404	25	29	2017-08-08 13:52:13.464862	f	t
1405	26	18	2017-08-04 13:52:13.464931	f	t
1406	26	7	2017-08-02 13:52:13.464998	f	t
1407	26	35	2017-08-09 13:52:13.465067	f	t
1408	26	37	2017-08-07 13:52:13.465134	f	t
1409	26	29	2017-07-26 13:52:13.465201	f	t
1410	26	21	2017-07-31 13:52:13.465268	f	t
1411	26	18	2017-08-02 13:52:13.465334	f	t
1412	26	35	2017-07-28 13:52:13.465403	f	t
1413	26	29	2017-07-29 13:52:13.46547	f	t
1414	26	21	2017-08-11 13:52:13.465537	f	t
1415	27	33	2017-07-26 13:52:13.465604	t	t
1416	27	11	2017-08-11 13:52:13.465672	t	t
1417	27	18	2017-07-28 13:52:13.465738	f	t
1418	28	7	2017-07-27 13:52:13.465806	t	t
1419	28	20	2017-08-10 13:52:13.465884	t	t
1420	28	18	2017-07-27 13:52:13.465952	t	t
1421	28	34	2017-08-06 13:52:13.466019	t	t
1422	28	13	2017-07-29 13:52:13.466085	t	t
1423	28	26	2017-08-12 13:52:13.466152	f	t
1424	28	17	2017-08-10 13:52:13.466218	f	t
1425	28	22	2017-07-28 13:52:13.466284	f	t
1426	29	7	2017-07-24 13:52:13.466351	t	t
1427	29	32	2017-08-10 13:52:13.466419	t	t
1428	29	25	2017-08-08 13:52:13.466486	t	t
1429	29	29	2017-07-28 13:52:13.466553	t	t
1430	29	22	2017-07-28 13:52:13.46662	t	t
1431	29	24	2017-08-08 13:52:13.466687	t	t
1432	29	8	2017-08-03 13:52:13.466753	t	t
1433	29	26	2017-07-26 13:52:13.466819	t	t
1434	29	26	2017-08-10 13:52:13.466886	t	t
1435	29	19	2017-08-04 13:52:13.466953	t	t
1436	29	11	2017-07-28 13:52:13.46702	t	t
1437	29	37	2017-08-11 13:52:13.467087	t	t
1438	29	32	2017-07-25 13:52:13.467152	t	t
1439	29	19	2017-08-14 13:52:13.467218	t	t
1440	29	8	2017-08-14 13:52:13.467285	t	t
1441	29	14	2017-08-01 13:52:13.467351	t	t
1442	29	25	2017-08-13 13:52:13.467417	t	t
1443	29	32	2017-07-30 13:52:13.467484	t	t
1444	29	35	2017-08-04 13:52:13.467552	t	t
1445	29	8	2017-07-29 13:52:13.46762	t	t
1446	29	19	2017-08-16 13:52:13.467687	t	t
1447	29	19	2017-08-17 13:52:13.467753	t	t
1448	29	26	2017-07-25 13:52:13.46782	t	t
1449	29	14	2017-07-27 13:52:13.467887	t	t
1450	29	29	2017-08-17 13:52:13.467954	t	t
1451	29	8	2017-08-16 13:52:13.46802	f	t
1452	29	17	2017-08-11 13:52:13.468087	f	t
1453	29	7	2017-08-07 13:52:13.468154	f	t
1454	29	10	2017-08-10 13:52:13.468221	f	t
1455	29	17	2017-08-10 13:52:13.468287	f	t
1456	29	22	2017-08-06 13:52:13.468354	f	t
1457	29	22	2017-08-04 13:52:13.46842	f	t
1458	29	33	2017-08-01 13:52:13.468486	f	t
1459	29	7	2017-08-09 13:52:13.468553	f	t
1460	29	20	2017-08-12 13:52:13.468619	f	t
1461	29	32	2017-07-29 13:52:13.468686	f	t
1462	29	8	2017-08-17 13:52:13.468753	f	t
1463	29	24	2017-07-24 13:52:13.46882	f	t
1464	29	31	2017-07-28 13:52:13.468886	f	t
1465	29	10	2017-07-26 13:52:13.468952	f	t
1466	29	33	2017-07-31 13:52:13.469019	f	t
1467	29	12	2017-08-03 13:52:13.469087	f	t
1468	29	34	2017-07-29 13:52:13.469153	f	t
1469	29	11	2017-08-14 13:52:13.469219	f	t
1470	29	29	2017-08-04 13:52:13.469288	f	t
1471	29	24	2017-07-25 13:52:13.469354	f	t
1472	29	32	2017-07-31 13:52:13.46942	f	t
1473	29	10	2017-08-09 13:52:13.469487	f	t
1474	29	26	2017-08-16 13:52:13.469552	f	t
1475	29	11	2017-07-26 13:52:13.46962	f	t
1476	30	10	2017-08-03 13:52:13.469689	t	t
1477	30	28	2017-07-28 13:52:13.469756	t	t
1478	30	8	2017-08-13 13:52:13.469822	t	t
1479	30	11	2017-08-14 13:52:13.469898	t	t
1480	30	28	2017-08-14 13:52:13.469966	t	t
1481	30	20	2017-08-07 13:52:13.470033	t	t
1482	30	25	2017-08-12 13:52:13.470101	t	t
1483	30	29	2017-08-08 13:52:13.470168	t	t
1484	30	21	2017-08-05 13:52:13.470235	t	t
1485	30	34	2017-08-09 13:52:13.470301	t	t
1486	30	28	2017-08-08 13:52:13.470366	t	t
1487	30	19	2017-08-14 13:52:13.470432	f	t
1488	31	19	2017-08-01 13:52:13.470499	t	t
1489	31	22	2017-08-01 13:52:13.470566	t	t
1490	31	33	2017-07-23 13:52:13.470632	t	t
1491	31	15	2017-08-10 13:52:13.470698	t	t
1492	31	36	2017-07-23 13:52:13.470764	t	t
1493	31	26	2017-07-31 13:52:13.470831	t	t
1494	31	10	2017-08-09 13:52:13.470897	t	t
1495	31	33	2017-07-31 13:52:13.470962	t	t
1496	31	27	2017-08-11 13:52:13.471029	t	t
1497	31	26	2017-07-30 13:52:13.471096	f	t
1498	31	35	2017-08-11 13:52:13.471163	f	t
1499	31	37	2017-08-13 13:52:13.471229	f	t
1500	31	12	2017-07-30 13:52:13.471296	f	t
1501	31	9	2017-08-07 13:52:13.471363	f	t
1502	31	10	2017-07-29 13:52:13.471431	f	t
1503	31	29	2017-08-03 13:52:13.471496	f	t
1504	31	9	2017-08-02 13:52:13.471563	f	t
1505	31	17	2017-08-06 13:52:13.47163	f	t
1506	31	23	2017-07-25 13:52:13.471696	f	t
1507	31	12	2017-07-30 13:52:13.471763	f	t
1508	31	36	2017-07-31 13:52:13.47183	f	t
1509	31	13	2017-07-29 13:52:13.471897	f	t
1510	31	23	2017-07-23 13:52:13.471963	f	t
1511	31	33	2017-08-05 13:52:13.47203	f	t
1512	32	19	2017-08-12 13:52:13.472097	t	t
1513	32	7	2017-08-03 13:52:13.472165	t	t
1514	32	27	2017-07-28 13:52:13.472232	t	t
1515	32	21	2017-07-28 13:52:13.472299	t	t
1516	32	18	2017-07-23 13:52:13.472365	t	t
1517	32	15	2017-08-15 13:52:13.472432	t	t
1518	32	36	2017-08-10 13:52:13.472498	t	t
1519	32	27	2017-07-29 13:52:13.472564	t	t
1520	32	11	2017-08-15 13:52:13.472631	f	t
1521	32	31	2017-08-05 13:52:13.472699	f	t
1522	32	11	2017-07-26 13:52:13.472765	f	t
1523	32	20	2017-07-27 13:52:13.472833	f	t
1524	32	32	2017-08-03 13:52:13.472899	f	t
1525	32	27	2017-07-24 13:52:13.472967	f	t
1526	33	21	2017-08-09 13:52:13.473034	t	t
1527	33	29	2017-08-13 13:52:13.473101	t	t
1528	33	18	2017-08-17 13:52:13.473167	t	t
1529	33	7	2017-07-23 13:52:13.473234	t	t
1530	33	33	2017-08-06 13:52:13.473301	t	t
1531	33	24	2017-08-06 13:52:13.473367	t	t
1532	33	29	2017-08-01 13:52:13.473434	t	t
1533	33	37	2017-08-17 13:52:13.4735	t	t
1534	33	15	2017-07-25 13:52:13.473567	t	t
1535	33	33	2017-08-08 13:52:13.473632	t	t
1536	33	28	2017-08-02 13:52:13.473697	t	t
1537	33	19	2017-08-14 13:52:13.473763	t	t
1538	33	28	2017-07-24 13:52:13.473831	t	t
1539	33	36	2017-08-10 13:52:13.473907	t	t
1540	33	28	2017-07-31 13:52:13.473974	t	t
1541	33	35	2017-08-03 13:52:13.474042	t	t
1542	33	11	2017-08-15 13:52:13.474109	t	t
1543	33	35	2017-07-30 13:52:13.474177	t	t
1544	33	25	2017-07-26 13:52:13.474245	f	t
1545	33	15	2017-08-02 13:52:13.474311	f	t
1546	33	35	2017-07-23 13:52:13.474377	f	t
1547	33	21	2017-08-16 13:52:13.474444	f	t
1548	33	16	2017-07-30 13:52:13.474511	f	t
1549	33	21	2017-08-01 13:52:13.474578	f	t
1550	33	9	2017-08-08 13:52:13.474645	f	t
1551	33	29	2017-08-11 13:52:13.474712	f	t
1552	33	18	2017-08-04 13:52:13.47478	f	t
1553	33	29	2017-08-04 13:52:13.474847	f	t
1554	33	23	2017-08-08 13:52:13.474913	f	t
1555	33	35	2017-08-13 13:52:13.47498	f	t
1556	33	29	2017-07-26 13:52:13.475047	f	t
1557	33	23	2017-07-31 13:52:13.475113	f	t
1558	33	13	2017-07-31 13:52:13.47518	f	t
1559	33	33	2017-08-06 13:52:13.475247	f	t
1560	33	23	2017-07-23 13:52:13.475313	f	t
1561	33	22	2017-07-26 13:52:13.475379	f	t
1562	33	28	2017-08-04 13:52:13.475446	f	t
1563	33	22	2017-08-08 13:52:13.475513	f	t
1564	33	17	2017-08-16 13:52:13.475579	f	t
1565	33	32	2017-07-28 13:52:13.475644	f	t
1566	33	34	2017-07-27 13:52:13.475708	f	t
1567	33	11	2017-07-26 13:52:13.475773	f	t
1568	33	10	2017-08-11 13:52:13.475837	f	t
1569	34	18	2017-08-02 13:52:13.475902	t	t
1570	34	12	2017-08-03 13:52:13.475966	t	t
1571	34	7	2017-08-09 13:52:13.476029	f	t
1572	34	24	2017-07-26 13:52:13.476094	f	t
1573	34	37	2017-08-11 13:52:13.476157	f	t
1574	35	18	2017-07-25 13:52:13.476222	t	t
1575	35	25	2017-07-23 13:52:13.476288	t	t
1576	35	25	2017-08-05 13:52:13.476354	t	t
1577	35	15	2017-07-24 13:52:13.476454	f	t
1578	35	11	2017-07-29 13:52:13.476521	f	t
1579	36	13	2017-07-29 13:52:13.476588	t	t
1580	36	12	2017-08-13 13:52:13.476655	t	t
1581	36	12	2017-07-30 13:52:13.476723	f	t
1582	36	27	2017-07-26 13:52:13.476791	f	t
1583	36	36	2017-07-28 13:52:13.476859	f	t
1584	37	29	2017-08-03 13:52:13.476927	t	t
1585	37	23	2017-07-28 13:52:13.476994	t	t
1586	37	9	2017-08-09 13:52:13.477061	t	t
1587	37	15	2017-07-25 13:52:13.477127	t	t
1588	37	9	2017-07-24 13:52:13.477194	t	t
1589	37	29	2017-07-27 13:52:13.47726	t	t
1590	37	12	2017-08-04 13:52:13.477327	t	t
1591	37	7	2017-08-17 13:52:13.477393	f	t
1592	37	37	2017-07-25 13:52:13.47746	f	t
1593	37	37	2017-08-02 13:52:13.477527	f	t
1594	37	12	2017-08-13 13:52:13.477593	f	t
1595	37	11	2017-08-01 13:52:13.477659	f	t
1596	37	8	2017-08-04 13:52:13.477725	f	t
1597	37	12	2017-08-08 13:52:13.477791	f	t
1598	37	16	2017-08-02 13:52:13.477862	f	t
1599	37	8	2017-07-29 13:52:13.47793	f	t
1600	37	28	2017-07-28 13:52:13.477995	f	t
1601	37	28	2017-08-15 13:52:13.478062	f	t
1602	37	18	2017-08-02 13:52:13.478128	f	t
1603	37	26	2017-07-25 13:52:13.478196	f	t
1604	37	20	2017-07-29 13:52:13.478262	f	t
1605	37	21	2017-07-29 13:52:13.478328	f	t
1606	37	36	2017-08-09 13:52:13.478396	f	t
1607	38	29	2017-08-16 13:52:13.478463	t	t
1608	38	29	2017-08-16 13:52:13.478531	t	t
1609	38	31	2017-08-14 13:52:13.478598	t	t
1610	38	37	2017-08-17 13:52:13.478664	t	t
1611	38	25	2017-08-17 13:52:13.47873	t	t
1612	38	25	2017-08-04 13:52:13.478795	t	t
1613	38	10	2017-08-10 13:52:13.478862	t	t
1614	38	25	2017-08-12 13:52:13.478929	t	t
1615	38	27	2017-08-03 13:52:13.478995	t	t
1616	38	22	2017-07-31 13:52:13.479063	t	t
1617	38	21	2017-07-24 13:52:13.479131	t	t
1618	38	10	2017-08-03 13:52:13.479198	t	t
1619	38	29	2017-08-13 13:52:13.479266	t	t
1620	38	10	2017-08-07 13:52:13.479336	t	t
1621	38	29	2017-07-27 13:52:13.479402	t	t
1622	38	28	2017-08-11 13:52:13.479468	t	t
1623	38	16	2017-08-08 13:52:13.479535	t	t
1624	38	15	2017-08-12 13:52:13.479601	t	t
1625	38	18	2017-08-15 13:52:13.479669	t	t
1626	38	19	2017-08-03 13:52:13.479735	t	t
1627	38	13	2017-07-30 13:52:13.479802	t	t
1628	38	18	2017-08-14 13:52:13.479868	t	t
1629	38	19	2017-07-24 13:52:13.479934	t	t
1630	38	8	2017-08-10 13:52:13.48	t	t
1631	38	7	2017-08-01 13:52:13.480067	t	t
1632	38	35	2017-08-12 13:52:13.480133	t	t
1633	38	32	2017-08-12 13:52:13.480199	f	t
1634	38	23	2017-08-10 13:52:13.480267	f	t
1635	38	12	2017-07-31 13:52:13.480335	f	t
1636	38	31	2017-07-24 13:52:13.480402	f	t
1637	38	34	2017-07-24 13:52:13.48047	f	t
1638	38	37	2017-07-31 13:52:13.480536	f	t
1639	38	29	2017-08-13 13:52:13.480602	f	t
1640	38	34	2017-08-12 13:52:13.480677	f	t
1641	38	27	2017-08-14 13:52:13.480745	f	t
1642	38	18	2017-08-14 13:52:13.480814	f	t
1643	38	20	2017-08-14 13:52:13.480882	f	t
1644	38	22	2017-08-08 13:52:13.480951	f	t
1645	38	28	2017-08-14 13:52:13.481021	f	t
1646	38	14	2017-08-10 13:52:13.481089	f	t
1647	38	24	2017-07-30 13:52:13.481158	f	t
1648	38	18	2017-07-25 13:52:13.481228	f	t
1649	38	27	2017-07-28 13:52:13.481297	f	t
1650	39	20	2017-07-23 13:52:13.481365	t	t
1651	39	11	2017-07-27 13:52:13.481433	t	t
1652	39	24	2017-07-30 13:52:13.4815	t	t
1653	39	13	2017-08-03 13:52:13.481566	f	t
1654	39	36	2017-08-07 13:52:13.481634	f	t
1655	39	36	2017-08-06 13:52:13.48171	f	t
1656	40	19	2017-07-24 13:52:13.481778	t	t
1657	40	11	2017-07-31 13:52:13.481853	t	t
1658	40	36	2017-07-29 13:52:13.481923	t	t
1659	40	25	2017-07-31 13:52:13.481991	t	t
1660	40	32	2017-08-02 13:52:13.482058	t	t
1661	40	15	2017-08-05 13:52:13.482125	t	t
1662	40	8	2017-08-14 13:52:13.482192	t	t
1663	40	34	2017-08-17 13:52:13.48226	t	t
1664	40	12	2017-08-05 13:52:13.482327	t	t
1665	40	34	2017-07-27 13:52:13.482395	t	t
1666	40	27	2017-08-05 13:52:13.482463	t	t
1667	40	22	2017-08-10 13:52:13.48253	t	t
1668	40	33	2017-08-15 13:52:13.482597	t	t
1669	40	10	2017-08-14 13:52:13.482665	t	t
1670	40	24	2017-07-25 13:52:13.482732	t	t
1671	40	28	2017-08-07 13:52:13.482798	t	t
1672	40	19	2017-08-06 13:52:13.482866	t	t
1673	40	31	2017-07-25 13:52:13.482932	t	t
1674	40	9	2017-08-10 13:52:13.482999	t	t
1675	40	33	2017-08-06 13:52:13.483066	t	t
1676	40	7	2017-07-29 13:52:13.483133	t	t
1677	40	29	2017-08-04 13:52:13.4832	t	t
1678	40	17	2017-07-26 13:52:13.483264	f	t
1679	40	25	2017-08-04 13:52:13.483329	f	t
1680	40	16	2017-08-06 13:52:13.483393	f	t
1681	40	13	2017-07-30 13:52:13.483457	f	t
1682	40	19	2017-07-24 13:52:13.483522	f	t
1683	40	11	2017-07-24 13:52:13.483585	f	t
1684	40	17	2017-07-27 13:52:13.483649	f	t
1685	40	28	2017-08-11 13:52:13.483712	f	t
1686	40	34	2017-07-29 13:52:13.483775	f	t
1687	40	21	2017-07-23 13:52:13.483837	f	t
1688	40	33	2017-07-30 13:52:13.483902	f	t
1689	40	36	2017-08-05 13:52:13.483969	f	t
1690	40	25	2017-07-23 13:52:13.484035	f	t
1691	41	28	2017-08-09 13:52:13.484101	t	t
1692	42	9	2017-08-08 13:52:13.48421	t	t
1693	42	33	2017-07-31 13:52:13.484281	t	t
1694	42	27	2017-08-07 13:52:13.484348	t	t
1695	42	27	2017-08-14 13:52:13.484414	t	t
1696	42	18	2017-08-08 13:52:13.484482	t	t
1697	42	31	2017-07-28 13:52:13.484549	t	t
1698	42	12	2017-08-15 13:52:13.484616	t	t
1699	42	14	2017-07-26 13:52:13.484683	t	t
1700	42	10	2017-07-23 13:52:13.48475	t	t
1701	42	27	2017-07-25 13:52:13.484816	t	t
1702	42	33	2017-07-26 13:52:13.484882	t	t
1703	42	31	2017-07-30 13:52:13.484949	t	t
1704	42	9	2017-08-13 13:52:13.485017	t	t
1705	42	17	2017-08-02 13:52:13.485085	t	t
1706	42	14	2017-08-11 13:52:13.485151	t	t
1707	42	7	2017-08-15 13:52:13.485217	f	t
1708	42	16	2017-08-09 13:52:13.485284	f	t
1709	42	32	2017-08-11 13:52:13.48535	f	t
1710	42	9	2017-08-05 13:52:13.48542	f	t
1711	42	29	2017-07-26 13:52:13.485486	f	t
1712	42	27	2017-08-17 13:52:13.48555	f	t
1713	42	23	2017-07-30 13:52:13.485615	f	t
1714	43	29	2017-08-09 13:52:13.48568	f	t
1715	43	32	2017-08-11 13:52:13.485748	f	t
1716	44	19	2017-08-15 13:52:13.485814	t	t
1717	44	22	2017-07-29 13:52:13.485894	t	t
1718	44	9	2017-08-01 13:52:13.485962	f	t
1719	44	15	2017-07-26 13:52:13.486029	f	t
1720	44	20	2017-08-03 13:52:13.486096	f	t
1721	44	33	2017-08-01 13:52:13.486164	f	t
1722	44	19	2017-08-14 13:52:13.486231	f	t
1723	44	9	2017-08-16 13:52:13.4863	f	t
1724	44	19	2017-07-28 13:52:13.486366	f	t
1725	45	7	2017-07-31 13:52:13.486434	t	t
1726	45	35	2017-08-02 13:52:13.4865	f	t
1727	45	24	2017-07-28 13:52:13.486568	f	t
1728	45	37	2017-08-16 13:52:13.486641	f	t
1729	46	18	2017-07-29 13:52:13.486716	t	t
1730	46	16	2017-07-29 13:52:13.486781	t	t
1731	46	35	2017-08-12 13:52:13.48685	t	t
1732	46	35	2017-08-16 13:52:13.486917	t	t
1733	46	7	2017-07-28 13:52:13.486981	t	t
1734	46	36	2017-08-04 13:52:13.487045	t	t
1735	46	32	2017-07-23 13:52:13.48711	t	t
1736	46	29	2017-08-07 13:52:13.487175	t	t
1737	46	8	2017-08-06 13:52:13.487239	t	t
1738	46	20	2017-08-11 13:52:13.487302	t	t
1739	46	20	2017-08-14 13:52:13.487365	t	t
1740	46	15	2017-08-12 13:52:13.487428	t	t
1741	46	11	2017-08-15 13:52:13.487491	t	t
1742	46	29	2017-08-05 13:52:13.487554	f	t
1743	46	35	2017-08-01 13:52:13.487616	f	t
1744	46	15	2017-07-25 13:52:13.487688	f	t
1745	47	8	2017-08-17 13:52:13.487755	t	t
1746	47	12	2017-08-14 13:52:13.487822	t	t
1747	47	35	2017-07-28 13:52:13.487889	t	t
1748	47	37	2017-07-23 13:52:13.48796	t	t
1749	47	29	2017-08-12 13:52:13.488028	t	t
1750	47	26	2017-08-08 13:52:13.488095	t	t
1751	47	15	2017-08-12 13:52:13.488161	t	t
1752	47	11	2017-08-05 13:52:13.488228	f	t
1753	47	19	2017-08-16 13:52:13.488295	f	t
1754	47	8	2017-08-05 13:52:13.488361	f	t
1755	48	29	2017-07-31 13:52:13.488427	f	t
1756	48	9	2017-07-30 13:52:13.488495	f	t
1757	48	32	2017-07-31 13:52:13.488562	f	t
1758	48	12	2017-08-15 13:52:13.48863	f	t
1759	48	7	2017-07-26 13:52:13.488696	f	t
1760	48	37	2017-08-11 13:52:13.488763	f	t
1761	48	13	2017-07-27 13:52:13.48883	f	t
1762	48	16	2017-08-14 13:52:13.488895	f	t
1763	48	17	2017-07-28 13:52:13.488962	f	t
1764	48	36	2017-07-24 13:52:13.489035	f	t
1765	48	20	2017-08-04 13:52:13.489104	f	t
1766	48	33	2017-07-27 13:52:13.48917	f	t
1767	48	28	2017-08-14 13:52:13.489237	f	t
1768	48	12	2017-08-01 13:52:13.489305	f	t
1769	48	15	2017-08-17 13:52:13.489372	f	t
1770	48	21	2017-07-25 13:52:13.48944	f	t
1771	48	23	2017-07-25 13:52:13.489506	f	t
1772	49	36	2017-07-27 13:52:13.489573	f	t
1773	49	35	2017-07-27 13:52:13.489641	f	t
1774	49	31	2017-07-28 13:52:13.489708	f	t
1775	49	36	2017-08-08 13:52:13.489775	f	t
1776	49	12	2017-08-02 13:52:13.489842	f	t
1777	49	37	2017-07-27 13:52:13.489922	f	t
1778	49	11	2017-07-27 13:52:13.489989	f	t
1779	49	9	2017-08-17 13:52:13.490056	f	t
1780	49	31	2017-07-29 13:52:13.490124	f	t
1781	49	29	2017-08-08 13:52:13.490191	f	t
1782	49	12	2017-07-29 13:52:13.490258	f	t
1783	50	11	2017-08-05 13:52:13.490326	t	t
1784	50	14	2017-08-04 13:52:13.490394	t	t
1785	50	11	2017-07-26 13:52:13.49046	t	t
1786	50	25	2017-08-15 13:52:13.490527	t	t
1787	50	17	2017-08-13 13:52:13.490599	t	t
1788	50	25	2017-08-05 13:52:13.490668	t	t
1789	50	18	2017-08-09 13:52:13.490735	t	t
1790	50	21	2017-07-31 13:52:13.490802	t	t
1791	50	22	2017-07-26 13:52:13.490868	t	t
1792	50	26	2017-08-06 13:52:13.490934	t	t
1793	50	16	2017-07-23 13:52:13.491	t	t
1794	50	19	2017-07-28 13:52:13.491066	t	t
1795	50	16	2017-08-14 13:52:13.491133	t	t
1796	50	35	2017-08-15 13:52:13.491198	t	t
1797	50	17	2017-07-29 13:52:13.491266	t	t
1798	50	8	2017-08-08 13:52:13.491331	t	t
1799	50	32	2017-08-10 13:52:13.491395	t	t
1800	50	18	2017-07-27 13:52:13.491464	t	t
1801	50	7	2017-07-31 13:52:13.491527	t	t
1802	50	19	2017-07-31 13:52:13.491592	t	t
1803	50	32	2017-08-15 13:52:13.491656	t	t
1804	50	20	2017-08-08 13:52:13.491721	t	t
1805	50	35	2017-08-12 13:52:13.491785	f	t
1806	50	34	2017-07-26 13:52:13.491849	f	t
1807	50	23	2017-08-08 13:52:13.491913	f	t
1808	50	37	2017-07-27 13:52:13.491978	f	t
1809	50	20	2017-07-27 13:52:13.492045	f	t
1810	50	31	2017-08-02 13:52:13.492146	f	t
1811	50	31	2017-07-31 13:52:13.49222	f	t
1812	50	34	2017-07-23 13:52:13.492287	f	t
1813	50	25	2017-07-29 13:52:13.492353	f	t
1814	50	8	2017-08-17 13:52:13.492423	f	t
1815	50	29	2017-08-01 13:52:13.49249	f	t
1816	51	20	2017-07-31 13:52:13.492558	t	t
1817	51	17	2017-08-13 13:52:13.492624	t	t
1818	51	18	2017-08-13 13:52:13.492692	t	t
1819	51	15	2017-07-24 13:52:13.49276	t	t
1820	51	17	2017-07-23 13:52:13.492827	t	t
1821	51	22	2017-08-01 13:52:13.492893	t	t
1822	51	28	2017-08-08 13:52:13.49296	t	t
1823	51	13	2017-07-29 13:52:13.493027	t	t
1824	51	12	2017-08-15 13:52:13.493093	t	t
1825	51	12	2017-07-25 13:52:13.493161	t	t
1826	51	8	2017-07-25 13:52:13.493228	t	t
1827	51	22	2017-08-02 13:52:13.493295	t	t
1828	51	18	2017-08-02 13:52:13.493361	t	t
1829	51	36	2017-08-05 13:52:13.493426	f	t
1830	51	36	2017-07-30 13:52:13.493491	f	t
1831	51	35	2017-07-30 13:52:13.493558	f	t
1832	51	18	2017-08-10 13:52:13.493628	f	t
1833	51	36	2017-07-31 13:52:13.493696	f	t
1834	51	22	2017-08-11 13:52:13.493763	f	t
1835	51	24	2017-07-24 13:52:13.49383	f	t
1836	51	13	2017-07-28 13:52:13.493909	f	t
1837	52	33	2017-08-03 13:52:13.493978	t	t
1838	52	9	2017-08-07 13:52:13.494047	t	t
1839	52	35	2017-07-25 13:52:13.494114	t	t
1840	52	26	2017-08-14 13:52:13.494181	t	t
1841	52	16	2017-08-15 13:52:13.494249	t	t
1842	52	34	2017-07-23 13:52:13.494316	t	t
1843	52	29	2017-08-04 13:52:13.494387	f	t
1844	52	11	2017-08-15 13:52:13.494455	f	t
1845	53	21	2017-07-27 13:52:13.494523	t	t
1846	53	32	2017-08-12 13:52:13.494591	t	t
1847	53	29	2017-08-12 13:52:13.494656	t	t
1848	53	36	2017-07-26 13:52:13.494723	t	t
1849	53	35	2017-07-28 13:52:13.494792	t	t
1850	53	24	2017-07-24 13:52:13.494858	f	t
1851	53	16	2017-07-31 13:52:13.494925	f	t
1852	53	21	2017-08-10 13:52:13.494991	f	t
1853	53	7	2017-08-05 13:52:13.495059	f	t
1854	53	36	2017-07-26 13:52:13.495127	f	t
1855	53	28	2017-07-31 13:52:13.495193	f	t
1856	53	36	2017-08-10 13:52:13.49526	f	t
1857	53	23	2017-08-09 13:52:13.495327	f	t
1858	53	18	2017-08-11 13:52:13.495394	f	t
1859	54	29	2017-08-08 13:52:13.495461	t	t
1860	54	10	2017-08-11 13:52:13.495528	t	t
1861	54	19	2017-08-16 13:52:13.495596	f	t
1862	54	7	2017-08-03 13:52:13.495664	f	t
1863	55	26	2017-08-01 13:52:13.49573	t	t
1864	55	11	2017-08-03 13:52:13.495796	t	t
1865	55	33	2017-08-16 13:52:13.495862	t	t
1866	55	20	2017-08-02 13:52:13.495931	t	t
1867	55	11	2017-07-31 13:52:13.495997	t	t
1868	55	17	2017-08-07 13:52:13.496061	t	t
1869	55	9	2017-07-28 13:52:13.496124	t	t
1870	55	31	2017-08-17 13:52:13.496188	t	t
1871	55	24	2017-07-26 13:52:13.496253	t	t
1872	55	28	2017-08-16 13:52:13.496321	t	t
1873	55	14	2017-07-29 13:52:13.496387	t	t
1874	55	15	2017-08-04 13:52:13.496451	t	t
1875	55	18	2017-07-28 13:52:13.496516	t	t
1876	55	18	2017-08-14 13:52:13.496578	f	t
1877	55	14	2017-08-16 13:52:13.496642	f	t
1878	55	29	2017-08-01 13:52:13.496708	f	t
1879	55	27	2017-08-11 13:52:13.496775	f	t
1880	55	10	2017-07-29 13:52:13.496844	f	t
1881	55	31	2017-08-17 13:52:13.496901	f	t
1882	55	31	2017-08-02 13:52:13.496959	f	t
1883	55	22	2017-08-04 13:52:13.497028	f	t
1884	55	25	2017-08-15 13:52:13.497094	f	t
1885	55	8	2017-08-08 13:52:13.497162	f	t
1886	55	10	2017-08-01 13:52:13.497229	f	t
1887	55	22	2017-07-27 13:52:13.497295	f	t
1888	55	34	2017-08-04 13:52:13.497362	f	t
1889	55	8	2017-08-10 13:52:13.497429	f	t
1890	56	18	2017-08-12 13:52:13.497495	t	t
1891	56	7	2017-08-13 13:52:13.497563	t	t
1892	56	23	2017-08-04 13:52:13.497629	t	t
1893	56	14	2017-07-24 13:52:13.497695	t	t
1894	56	29	2017-08-17 13:52:13.497763	f	t
1895	57	29	2017-08-07 13:52:13.49783	t	t
1896	57	15	2017-07-31 13:52:13.497908	f	t
1897	57	34	2017-07-26 13:52:13.497976	f	t
1898	57	34	2017-07-30 13:52:13.498042	f	t
1899	58	13	2017-07-29 13:52:13.498115	t	t
1900	58	21	2017-08-05 13:52:13.498185	t	t
1901	58	10	2017-08-15 13:52:13.498252	t	t
1902	58	11	2017-08-16 13:52:13.498318	t	t
1903	58	13	2017-07-30 13:52:13.498386	t	t
1904	58	21	2017-08-11 13:52:13.498454	t	t
1905	58	31	2017-07-23 13:52:13.49852	t	t
1906	58	27	2017-07-31 13:52:13.498588	t	t
1907	58	9	2017-08-03 13:52:13.498656	f	t
1908	58	18	2017-08-10 13:52:13.498727	f	t
1909	58	33	2017-08-11 13:52:13.498793	f	t
1910	59	24	2017-07-31 13:52:13.498861	f	t
1911	59	36	2017-07-26 13:52:13.498928	f	t
1912	59	32	2017-08-05 13:52:13.498999	f	t
1913	59	29	2017-08-13 13:52:13.499067	f	t
1914	59	11	2017-08-17 13:52:13.499135	f	t
1915	59	19	2017-07-29 13:52:13.499201	f	t
1916	59	13	2017-08-11 13:52:13.499273	f	t
1917	59	31	2017-08-03 13:52:13.499341	f	t
1918	59	36	2017-08-12 13:52:13.499408	f	t
1919	59	23	2017-08-02 13:52:13.499475	f	t
1920	60	11	2017-07-31 13:52:13.499541	t	t
1921	60	24	2017-07-23 13:52:13.499607	t	t
1922	60	35	2017-07-28 13:52:13.499674	t	t
1923	60	20	2017-07-24 13:52:13.499739	t	t
1924	60	23	2017-08-17 13:52:13.499807	t	t
1925	60	29	2017-07-24 13:52:13.499874	t	t
1926	60	34	2017-08-11 13:52:13.499942	t	t
1927	60	19	2017-08-07 13:52:13.500009	t	t
1928	60	29	2017-07-24 13:52:13.500075	t	t
1929	60	24	2017-08-01 13:52:13.500143	t	t
1930	60	26	2017-08-13 13:52:13.50021	t	t
1931	60	24	2017-08-06 13:52:13.500279	f	t
1932	60	22	2017-07-23 13:52:13.500345	f	t
1933	60	12	2017-07-30 13:52:13.500412	f	t
1934	60	11	2017-08-03 13:52:13.500479	f	t
1935	60	14	2017-07-24 13:52:13.500546	f	t
1936	60	9	2017-08-17 13:52:13.500611	f	t
1937	61	11	2017-08-10 13:52:13.500678	t	t
1938	61	32	2017-07-30 13:52:13.500745	t	t
1939	61	29	2017-08-17 13:52:13.500811	t	t
1940	61	33	2017-08-01 13:52:13.500875	f	t
1941	61	21	2017-08-02 13:52:13.500939	f	t
1942	61	7	2017-07-28 13:52:13.501003	f	t
1943	61	33	2017-08-11 13:52:13.501067	f	t
1944	61	10	2017-08-14 13:52:13.501138	f	t
1945	62	26	2017-08-01 13:52:13.501203	t	t
1946	62	14	2017-07-30 13:52:13.501269	t	t
1947	62	15	2017-07-26 13:52:13.501332	f	t
1948	62	32	2017-08-02 13:52:13.501397	f	t
1949	62	29	2017-07-26 13:52:13.501459	f	t
1950	62	16	2017-07-24 13:52:13.501523	f	t
1951	63	32	2017-07-30 13:52:13.501589	t	t
1952	63	28	2017-08-03 13:52:13.501657	t	t
1953	63	35	2017-07-24 13:52:13.501724	t	t
1954	63	13	2017-07-31 13:52:13.501792	t	t
1955	63	31	2017-07-24 13:52:13.501869	t	t
1956	63	11	2017-07-24 13:52:13.501938	t	t
1957	63	29	2017-07-30 13:52:13.502005	t	t
1958	63	16	2017-08-02 13:52:13.502073	t	t
1959	63	34	2017-08-11 13:52:13.50214	f	t
1960	63	13	2017-08-03 13:52:13.502208	f	t
1961	64	32	2017-07-28 13:52:13.502274	t	t
1962	64	17	2017-08-13 13:52:13.502341	t	t
1963	64	18	2017-07-23 13:52:13.502407	t	t
1964	64	11	2017-08-11 13:52:13.502473	t	t
1965	64	21	2017-07-29 13:52:13.50254	t	t
1966	64	10	2017-07-28 13:52:13.502606	t	t
1967	64	14	2017-08-05 13:52:13.502672	f	t
1968	64	29	2017-08-08 13:52:13.502741	f	t
1969	65	19	2017-07-31 13:52:13.502807	t	t
1970	65	20	2017-08-13 13:52:13.502873	t	t
1971	65	10	2017-08-03 13:52:13.50294	t	t
1972	65	29	2017-08-05 13:52:13.503006	t	t
1973	65	19	2017-07-29 13:52:13.503071	t	t
1974	65	12	2017-07-25 13:52:13.503137	t	t
1975	65	16	2017-07-27 13:52:13.503205	t	t
1976	65	21	2017-08-17 13:52:13.503271	t	t
1977	65	34	2017-08-17 13:52:13.503338	t	t
1978	65	13	2017-08-14 13:52:13.503405	t	t
1979	65	21	2017-08-09 13:52:13.503473	t	t
1980	65	34	2017-08-01 13:52:13.503547	t	t
1981	65	19	2017-08-12 13:52:13.503616	t	t
1982	65	31	2017-07-23 13:52:13.503684	t	t
1983	65	15	2017-07-31 13:52:13.503752	t	t
1984	65	12	2017-07-30 13:52:13.503819	t	t
1985	65	17	2017-08-07 13:52:13.503886	t	t
1986	65	35	2017-07-29 13:52:13.503949	t	t
1987	65	37	2017-08-01 13:52:13.504007	t	t
1988	65	23	2017-07-30 13:52:13.504064	t	t
1989	65	28	2017-08-02 13:52:13.50412	t	t
1990	65	21	2017-07-29 13:52:13.504177	t	t
1991	65	11	2017-07-30 13:52:13.504233	t	t
1992	65	20	2017-08-04 13:52:13.504291	f	t
1993	65	31	2017-08-14 13:52:13.504351	f	t
1994	65	28	2017-08-01 13:52:13.504413	f	t
1995	65	36	2017-08-12 13:52:13.504474	f	t
1996	65	23	2017-08-05 13:52:13.504531	f	t
1997	65	27	2017-07-30 13:52:13.504588	f	t
1998	65	16	2017-08-10 13:52:13.504646	f	t
1999	65	25	2017-08-13 13:52:13.504704	f	t
2000	65	24	2017-08-01 13:52:13.50477	f	t
2001	65	33	2017-08-13 13:52:13.50483	f	t
2002	65	20	2017-08-11 13:52:13.504889	f	t
2003	65	13	2017-07-23 13:52:13.504951	f	t
2004	65	32	2017-08-08 13:52:13.505014	f	t
2005	65	36	2017-08-06 13:52:13.505079	f	t
2006	66	20	2017-08-11 13:52:13.505147	t	t
2007	66	20	2017-07-29 13:52:13.505213	t	t
2008	66	17	2017-08-10 13:52:13.505277	t	t
2009	66	13	2017-08-11 13:52:13.505344	t	t
2010	66	17	2017-07-26 13:52:13.50541	f	t
2011	67	26	2017-08-11 13:52:13.50548	t	t
2012	67	14	2017-08-15 13:52:13.505548	t	t
2013	67	32	2017-07-27 13:52:13.505618	t	t
2014	67	25	2017-08-04 13:52:13.505685	t	t
2015	67	19	2017-07-25 13:52:13.505751	t	t
2016	67	26	2017-07-24 13:52:13.505821	t	t
2017	67	17	2017-08-10 13:52:13.505898	t	t
2018	67	8	2017-08-10 13:52:13.505967	t	t
2019	67	22	2017-07-24 13:52:13.506034	t	t
2020	67	22	2017-08-08 13:52:13.506099	t	t
2021	67	20	2017-08-16 13:52:13.506167	f	t
2022	67	24	2017-08-08 13:52:13.506234	f	t
2023	67	22	2017-07-29 13:52:13.506301	f	t
2024	67	9	2017-08-04 13:52:13.506367	f	t
2025	67	11	2017-08-12 13:52:13.506432	f	t
2026	67	28	2017-07-31 13:52:13.5065	f	t
2027	67	20	2017-08-09 13:52:13.506565	f	t
2028	67	24	2017-07-30 13:52:13.506631	f	t
2029	67	28	2017-08-12 13:52:13.506697	f	t
2030	67	18	2017-08-08 13:52:13.506763	f	t
2031	67	17	2017-08-01 13:52:13.506829	f	t
2032	67	18	2017-08-01 13:52:13.506895	f	t
2033	67	7	2017-08-06 13:52:13.50696	f	t
2034	67	27	2017-08-11 13:52:13.507026	f	t
2035	67	16	2017-08-15 13:52:13.507092	f	t
2036	68	20	2017-07-24 13:52:13.507158	f	t
2037	69	24	2017-07-24 13:52:13.507222	t	t
2038	69	15	2017-08-15 13:52:13.507288	t	t
2039	69	19	2017-07-31 13:52:13.507354	t	t
2040	69	19	2017-08-09 13:52:13.507419	t	t
2041	69	19	2017-08-14 13:52:13.507485	t	t
2042	69	7	2017-07-23 13:52:13.507549	f	t
2043	69	32	2017-08-15 13:52:13.507645	f	t
2044	69	36	2017-08-06 13:52:13.507713	f	t
2045	69	32	2017-08-12 13:52:13.507791	f	t
2046	69	26	2017-07-26 13:52:13.507859	f	t
2047	69	7	2017-07-29 13:52:13.507925	f	t
2048	69	15	2017-08-02 13:52:13.507992	f	t
2049	69	29	2017-07-27 13:52:13.50806	f	t
2050	69	10	2017-08-12 13:52:13.508127	f	t
2051	69	23	2017-07-23 13:52:13.508193	f	t
2052	69	37	2017-08-05 13:52:13.50826	f	t
2053	69	29	2017-07-31 13:52:13.508323	f	t
2054	69	14	2017-08-06 13:52:13.508384	f	t
2055	69	15	2017-08-13 13:52:13.50845	f	t
2056	70	35	2017-08-13 13:52:13.508518	t	t
2057	70	20	2017-08-02 13:52:13.508581	t	t
2058	70	26	2017-08-17 13:52:13.508645	t	t
2059	70	18	2017-07-23 13:52:13.508708	t	t
2060	70	8	2017-07-24 13:52:13.50878	t	t
2061	70	26	2017-08-01 13:52:13.508841	t	t
2062	70	32	2017-08-01 13:52:13.508904	t	t
2063	70	37	2017-07-31 13:52:13.508964	t	t
2064	70	17	2017-08-10 13:52:13.50902	f	t
2065	70	32	2017-08-16 13:52:13.509074	f	t
2066	70	14	2017-07-27 13:52:13.509131	f	t
2067	70	27	2017-08-05 13:52:13.509191	f	t
2068	70	25	2017-07-31 13:52:13.509252	f	t
2069	70	33	2017-08-05 13:52:13.509309	f	t
2070	70	28	2017-07-27 13:52:13.509362	f	t
2071	70	21	2017-08-05 13:52:13.509416	f	t
2072	70	8	2017-08-10 13:52:13.509468	f	t
2073	70	31	2017-08-03 13:52:13.509519	f	t
2074	70	15	2017-08-15 13:52:13.509579	f	t
2075	70	16	2017-07-25 13:52:13.50964	f	t
2076	70	33	2017-08-08 13:52:13.509704	f	t
2077	70	27	2017-08-13 13:52:13.509764	f	t
2078	70	19	2017-08-14 13:52:13.509822	f	t
2079	70	20	2017-07-27 13:52:13.509893	f	t
2080	71	7	2017-07-27 13:52:13.509956	t	t
2081	71	13	2017-07-23 13:52:13.510016	t	t
2082	71	28	2017-07-28 13:52:13.510075	t	t
2083	71	12	2017-08-10 13:52:13.510137	t	t
2084	71	26	2017-08-10 13:52:13.510203	t	t
2085	71	9	2017-08-02 13:52:13.510262	t	t
2086	71	31	2017-08-04 13:52:13.51032	t	t
2087	71	7	2017-08-10 13:52:13.510379	t	t
2088	71	8	2017-08-16 13:52:13.510445	t	t
2089	71	24	2017-08-14 13:52:13.510504	t	t
2090	71	18	2017-08-03 13:52:13.510564	t	t
2091	71	17	2017-08-06 13:52:13.510626	t	t
2092	71	20	2017-07-23 13:52:13.510686	t	t
2093	71	37	2017-07-26 13:52:13.510744	t	t
2094	71	15	2017-07-24 13:52:13.510806	t	t
2095	71	18	2017-08-07 13:52:13.51086	t	t
2096	71	12	2017-07-28 13:52:13.510915	f	t
2097	71	25	2017-08-04 13:52:13.510976	f	t
2098	71	19	2017-08-13 13:52:13.511042	f	t
2099	71	23	2017-08-11 13:52:13.511107	f	t
2100	71	35	2017-08-06 13:52:13.511173	f	t
2101	71	34	2017-07-25 13:52:13.511239	f	t
2102	71	13	2017-08-10 13:52:13.511308	f	t
2103	71	27	2017-08-14 13:52:13.511374	f	t
2104	71	34	2017-08-14 13:52:13.511442	f	t
2105	71	22	2017-08-04 13:52:13.511509	f	t
2106	71	37	2017-07-24 13:52:13.511576	f	t
2107	71	18	2017-08-12 13:52:13.511644	f	t
2108	71	23	2017-08-06 13:52:13.51171	f	t
2109	71	12	2017-08-01 13:52:13.511776	f	t
2110	71	20	2017-08-07 13:52:13.511843	f	t
2111	72	11	2017-08-06 13:52:13.511909	f	t
2112	72	16	2017-08-17 13:52:13.511976	f	t
2113	72	21	2017-08-07 13:52:13.512043	f	t
2114	73	36	2017-07-30 13:52:13.512115	t	t
2115	73	29	2017-08-12 13:52:13.512182	t	t
2116	73	11	2017-08-13 13:52:13.512249	t	t
2117	73	20	2017-08-12 13:52:13.512317	t	t
2118	73	7	2017-08-11 13:52:13.512384	t	t
2119	73	36	2017-08-02 13:52:13.512451	t	t
2120	73	13	2017-08-15 13:52:13.512517	t	t
2121	73	34	2017-07-28 13:52:13.512585	t	t
2122	73	11	2017-08-14 13:52:13.512652	t	t
2123	73	10	2017-08-17 13:52:13.512723	t	t
2124	73	23	2017-08-09 13:52:13.512794	f	t
2125	73	14	2017-08-06 13:52:13.512861	f	t
2126	73	17	2017-07-26 13:52:13.51293	f	t
2127	73	36	2017-07-28 13:52:13.512997	f	t
2128	73	23	2017-07-23 13:52:13.513062	f	t
2129	73	31	2017-08-08 13:52:13.513128	f	t
2130	73	27	2017-07-28 13:52:13.513194	f	t
2131	73	36	2017-08-04 13:52:13.513261	f	t
2132	73	29	2017-08-15 13:52:13.513327	f	t
2133	74	32	2017-07-30 13:52:13.513396	t	t
2134	74	16	2017-08-10 13:52:13.513463	t	t
2135	74	10	2017-08-12 13:52:13.513528	t	t
2136	74	27	2017-07-27 13:52:13.513594	t	t
2137	74	27	2017-08-12 13:52:13.51366	t	t
2138	74	20	2017-08-15 13:52:13.513725	t	t
2139	74	33	2017-08-13 13:52:13.513801	t	t
2140	74	36	2017-08-14 13:52:13.51388	t	t
2141	74	19	2017-07-26 13:52:13.513951	t	t
2142	74	31	2017-08-02 13:52:13.514022	t	t
2143	74	20	2017-08-03 13:52:13.514091	t	t
2144	74	24	2017-07-31 13:52:13.514159	t	t
2145	74	18	2017-07-30 13:52:13.51423	t	t
2146	74	34	2017-08-13 13:52:13.514298	t	t
2147	74	21	2017-08-08 13:52:13.514366	t	t
2148	74	10	2017-08-11 13:52:13.514437	t	t
2149	74	28	2017-08-03 13:52:13.514506	f	t
2150	74	25	2017-08-13 13:52:13.514579	f	t
2151	74	36	2017-07-31 13:52:13.514648	f	t
2152	74	20	2017-08-10 13:52:13.514717	f	t
2153	75	37	2017-08-03 13:52:13.514793	t	t
2154	75	24	2017-07-27 13:52:13.514859	t	t
2155	75	26	2017-08-01 13:52:13.514926	t	t
2156	75	12	2017-08-08 13:52:13.514994	t	t
2157	75	17	2017-07-30 13:52:13.515061	t	t
2158	75	19	2017-08-15 13:52:13.515128	t	t
2159	75	8	2017-07-28 13:52:13.515195	t	t
2160	75	31	2017-08-09 13:52:13.515267	f	t
2161	75	31	2017-07-30 13:52:13.515335	f	t
2162	75	16	2017-07-31 13:52:13.515401	f	t
2163	75	37	2017-08-10 13:52:13.515469	f	t
2164	75	14	2017-08-13 13:52:13.515536	f	t
2165	75	37	2017-08-06 13:52:13.515603	f	t
2166	75	23	2017-08-07 13:52:13.515671	f	t
2167	75	29	2017-08-10 13:52:13.515739	f	t
2168	75	28	2017-08-11 13:52:13.515809	f	t
2169	75	28	2017-08-13 13:52:13.515877	f	t
2170	75	24	2017-07-29 13:52:13.515945	f	t
2171	75	11	2017-08-01 13:52:13.516013	f	t
2172	75	10	2017-07-25 13:52:13.51608	f	t
2173	75	17	2017-08-05 13:52:13.516144	f	t
2174	75	7	2017-08-11 13:52:13.516211	f	t
2175	75	36	2017-08-08 13:52:13.516275	f	t
2176	75	32	2017-08-01 13:52:13.516337	f	t
2177	76	29	2017-08-03 13:52:13.516402	t	t
2178	76	17	2017-07-28 13:52:13.516465	t	t
2179	76	20	2017-07-30 13:52:13.516533	t	t
2180	76	15	2017-08-17 13:52:13.516601	t	t
2181	76	21	2017-08-14 13:52:13.516666	t	t
2182	76	11	2017-07-28 13:52:13.516731	f	t
2183	76	16	2017-08-15 13:52:13.516798	f	t
2184	76	20	2017-08-17 13:52:13.516865	f	t
2185	76	10	2017-08-13 13:52:13.51693	f	t
2186	76	35	2017-08-07 13:52:13.516996	f	t
2187	76	37	2017-07-24 13:52:13.517062	f	t
2188	76	24	2017-08-04 13:52:13.517127	f	t
2189	76	16	2017-08-11 13:52:13.517191	f	t
2190	76	9	2017-08-17 13:52:13.517258	f	t
2191	76	16	2017-07-26 13:52:13.517325	f	t
2192	76	16	2017-08-15 13:52:13.517392	f	t
2193	76	36	2017-08-14 13:52:13.51746	f	t
2194	77	29	2017-08-07 13:52:13.517526	t	t
2195	77	11	2017-07-28 13:52:13.517594	t	t
2196	77	7	2017-08-07 13:52:13.517664	f	t
2197	77	16	2017-08-15 13:52:13.517732	f	t
2198	77	25	2017-08-09 13:52:13.517802	f	t
2199	78	26	2017-07-30 13:52:13.517876	t	t
2200	78	24	2017-08-09 13:52:13.517945	t	t
2201	78	33	2017-08-05 13:52:13.518013	t	t
2202	78	21	2017-07-26 13:52:13.51808	t	t
2203	78	36	2017-07-26 13:52:13.518148	f	t
2204	78	18	2017-07-24 13:52:13.518214	f	t
2205	78	34	2017-08-16 13:52:13.518283	f	t
2206	78	27	2017-08-14 13:52:13.51835	f	t
2207	78	33	2017-08-07 13:52:13.518417	f	t
2208	79	36	2017-08-09 13:52:13.518484	t	t
2209	79	28	2017-07-29 13:52:13.518551	t	t
2210	79	34	2017-08-11 13:52:13.518619	f	t
2211	79	26	2017-08-15 13:52:13.518686	f	t
2212	79	29	2017-07-31 13:52:13.518754	f	t
2213	80	18	2017-08-13 13:52:13.518822	t	t
2214	80	15	2017-08-04 13:52:13.518891	t	t
2215	80	28	2017-08-07 13:52:13.518962	t	t
2216	80	21	2017-08-14 13:52:13.519029	t	t
2217	80	11	2017-07-23 13:52:13.519097	t	t
2218	80	22	2017-07-30 13:52:13.519164	t	t
2219	80	10	2017-08-14 13:52:13.519232	t	t
2220	80	33	2017-08-09 13:52:13.519299	t	t
2221	80	23	2017-08-06 13:52:13.519366	t	t
2222	80	22	2017-08-14 13:52:13.519439	t	t
2223	80	10	2017-08-10 13:52:13.519507	t	t
2224	80	26	2017-07-25 13:52:13.519576	t	t
2225	80	16	2017-08-05 13:52:13.519642	t	t
2226	80	35	2017-08-16 13:52:13.519709	f	t
2227	80	18	2017-08-09 13:52:13.519776	f	t
2228	80	24	2017-08-05 13:52:13.519842	f	t
2229	80	37	2017-08-12 13:52:13.519909	f	t
2230	80	34	2017-07-31 13:52:13.519975	f	t
2231	80	8	2017-08-08 13:52:13.520042	f	t
2232	80	11	2017-08-02 13:52:13.520112	f	t
2233	80	37	2017-08-08 13:52:13.520179	f	t
2234	80	33	2017-08-04 13:52:13.520246	f	t
2235	80	18	2017-08-11 13:52:13.520316	f	t
2236	80	31	2017-07-29 13:52:13.520384	f	t
2237	80	27	2017-08-12 13:52:13.520451	f	t
2238	80	33	2017-08-01 13:52:13.520519	f	t
2239	80	7	2017-08-16 13:52:13.520586	f	t
2240	80	25	2017-08-14 13:52:13.520654	f	t
2241	81	23	2017-07-31 13:52:13.520722	f	t
2242	81	16	2017-08-16 13:52:13.520789	f	t
2243	81	29	2017-08-14 13:52:13.520856	f	t
2244	81	27	2017-08-10 13:52:13.520923	f	t
2245	81	17	2017-08-01 13:52:13.520992	f	t
2246	82	11	2017-07-23 13:52:13.521062	t	t
2247	82	33	2017-07-31 13:52:13.52113	t	t
2248	82	24	2017-07-31 13:52:13.521197	f	t
2249	82	14	2017-08-11 13:52:13.521263	f	t
\.


--
-- Name: clicked_statements_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('clicked_statements_uid_seq', 2249, true);


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
1	Town has to cut spending 	town-has-to-cut-spending	Our town needs to cut spending. Please discuss ideas how this should be done.		2017-08-17 13:52:05.781325	2	1	t
2	Cat or Dog	cat-or-dog	Your family argues about whether to buy a cat or dog as pet. Now your opinion matters!		2017-08-17 13:52:05.781493	2	1	f
3	Make the world better	make-the-world-better	How can we make this world a better place?		2017-08-17 13:52:05.781635	2	1	f
4	Elektroautos	elektroautos	Elektroautos - Die Autos der Zukunft? Bitte diskutieren Sie dazu.		2017-08-17 13:52:05.781763	2	2	f
5	Unterstützung der Sekretariate	unterstutzung-der-sekretariate	Unsere Sekretariate in der Informatik sind arbeitsmäßig stark überlastet. Bitte diskutieren Sie Möglichkeiten um dies zu verbessern.		2017-08-17 13:52:05.782601	2	2	f
6	Verbesserung des Informatik-Studiengangs	verbesserung-des-informatik-studiengangs	Wie können der Informatik-Studiengang verbessert und die Probleme, die durch die große Anzahl der Studierenden entstanden sind, gelöst werden?	Die Anzahl der Studierenden in der Informatik hat sich in den letzten Jahren stark erhöht. Dadurch treten zahlreiche Probleme auf, wie z.B. Raumknappheit, überfüllte Lehrveranstaltungen und ein Mangel an Plätzen zum Lernen. Wir möchten Sie gerne dazu einladen, gemeinsam mit den Dozierenden der Informatik über Lösungsmöglichkeiten zu diskutieren: Wie können der Studiengang verbessert und die Probleme, die durch die große Anzahl der Studierenden entstanden sind, gelöst werden?	2017-08-17 13:52:05.782736	2	2	t
7	Bürgerbeteiligung in der Kommune	burgerbeteiligung-in-der-kommune	Es werden Vorschläge zur Verbesserung des Zusammenlebens in unserer Kommune gesammelt.		2017-08-17 13:52:05.782867	2	2	f
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
1	14	1	t	2017-08-17 13:52:08.806492
2	16	1	f	2017-08-17 13:52:08.80656
3	17	1	t	2017-08-17 13:52:08.806624
4	22	1	t	2017-08-17 13:52:08.806688
5	23	1	t	2017-08-17 13:52:08.806751
6	20	2	f	2017-08-17 13:52:08.806815
7	21	2	t	2017-08-17 13:52:08.80688
8	18	2	f	2017-08-17 13:52:08.806945
9	34	2	t	2017-08-17 13:52:08.807009
10	24	2	f	2017-08-17 13:52:08.807073
11	25	2	f	2017-08-17 13:52:08.807138
12	26	2	f	2017-08-17 13:52:08.807201
13	27	3	f	2017-08-17 13:52:08.807264
14	28	3	f	2017-08-17 13:52:08.807327
15	33	3	f	2017-08-17 13:52:08.80739
16	19	8	t	2017-08-17 13:52:08.807454
17	35	8	t	2017-08-17 13:52:08.807517
18	36	8	t	2017-08-17 13:52:08.80758
\.


--
-- Name: last_reviewers_delete_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('last_reviewers_delete_uid_seq', 18, true);


--
-- Data for Name: last_reviewers_duplicates; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY last_reviewers_duplicates (uid, reviewer_uid, review_uid, is_okay, "timestamp") FROM stdin;
1	12	1	t	2017-08-17 13:52:08.807657
2	13	2	t	2017-08-17 13:52:08.807725
3	14	2	t	2017-08-17 13:52:08.807789
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
1	29	1	t	2017-08-17 13:52:08.806026
2	31	1	t	2017-08-17 13:52:08.806129
3	32	1	t	2017-08-17 13:52:08.8062
4	12	2	f	2017-08-17 13:52:08.806266
5	13	2	f	2017-08-17 13:52:08.80633
6	15	2	f	2017-08-17 13:52:08.806394
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
1	1	1	f	1	2017-08-17 13:52:06.014052	2	t
2	2	5	f	1	2017-08-17 13:52:06.014206	2	f
3	3	6	f	1	2017-08-17 13:52:06.014298	2	f
4	4	7	f	1	2017-08-17 13:52:06.014385	2	f
5	5	8	f	1	2017-08-17 13:52:06.014471	2	f
6	6	9	f	1	2017-08-17 13:52:06.014563	2	f
7	7	10	f	1	2017-08-17 13:52:06.014644	2	f
8	8	11	f	1	2017-08-17 13:52:06.014725	2	f
9	9	12	f	1	2017-08-17 13:52:06.014807	2	f
10	10	13	f	1	2017-08-17 13:52:06.014889	2	f
11	11	14	f	1	2017-08-17 13:52:06.014969	2	f
12	12	15	f	1	2017-08-17 13:52:06.01505	2	f
13	12	16	f	1	2017-08-17 13:52:06.015131	2	f
14	13	17	f	1	2017-08-17 13:52:06.015212	2	f
15	14	18	f	1	2017-08-17 13:52:06.015292	2	f
16	15	19	f	1	2017-08-17 13:52:06.015373	2	f
17	16	20	f	1	2017-08-17 13:52:06.015454	2	f
18	17	21	f	1	2017-08-17 13:52:06.015537	2	f
19	18	22	f	1	2017-08-17 13:52:06.015618	2	f
20	19	23	f	1	2017-08-17 13:52:06.015698	2	f
21	20	24	f	1	2017-08-17 13:52:06.015778	2	f
22	21	25	f	1	2017-08-17 13:52:06.015858	2	f
23	22	26	f	1	2017-08-17 13:52:06.015938	2	f
24	23	27	f	1	2017-08-17 13:52:06.016018	2	f
25	24	28	f	1	2017-08-17 13:52:06.016098	2	f
26	25	29	f	1	2017-08-17 13:52:06.016178	2	f
27	26	30	f	1	2017-08-17 13:52:06.016258	2	f
28	27	31	f	1	2017-08-17 13:52:06.016338	2	f
29	28	32	f	1	2017-08-17 13:52:06.016419	2	f
30	29	33	f	1	2017-08-17 13:52:06.016498	2	f
31	30	34	f	1	2017-08-17 13:52:06.016578	2	f
32	9	35	f	1	2017-08-17 13:52:06.016658	2	f
33	31	39	f	1	2017-08-17 13:52:06.016738	1	f
34	32	40	f	1	2017-08-17 13:52:06.016817	1	f
35	33	41	f	1	2017-08-17 13:52:06.016897	1	f
36	34	42	f	1	2017-08-17 13:52:06.016978	1	f
37	35	43	f	1	2017-08-17 13:52:06.017059	1	f
38	36	44	f	1	2017-08-17 13:52:06.017139	1	f
39	37	45	f	1	2017-08-17 13:52:06.017224	1	f
40	38	46	f	1	2017-08-17 13:52:06.017306	1	f
41	39	47	f	1	2017-08-17 13:52:06.017386	1	f
42	40	48	f	1	2017-08-17 13:52:06.017466	1	f
43	41	49	f	1	2017-08-17 13:52:06.017547	1	f
44	42	50	f	1	2017-08-17 13:52:06.017627	1	f
45	43	51	f	1	2017-08-17 13:52:06.01771	1	f
46	44	52	f	1	2017-08-17 13:52:06.017791	1	f
47	45	53	f	1	2017-08-17 13:52:06.01788	1	f
48	46	54	f	1	2017-08-17 13:52:06.017965	1	f
49	47	55	f	1	2017-08-17 13:52:06.018047	1	f
50	48	56	f	1	2017-08-17 13:52:06.018128	1	f
51	49	57	f	1	2017-08-17 13:52:06.018209	1	f
52	52	61	f	1	2017-08-17 13:52:06.018456	4	f
53	53	62	f	1	2017-08-17 13:52:06.01854	4	f
54	54	63	f	1	2017-08-17 13:52:06.018623	4	f
55	55	64	f	1	2017-08-17 13:52:06.018763	4	f
56	56	65	f	1	2017-08-17 13:52:06.018848	4	f
57	57	66	f	1	2017-08-17 13:52:06.018929	4	f
58	50	59	f	1	2017-08-17 13:52:06.018292	4	f
59	51	60	f	1	2017-08-17 13:52:06.018374	4	f
60	61	68	f	5	2017-08-17 13:52:06.019009	4	f
61	62	71	f	1	2017-08-17 13:52:06.019092	5	f
62	63	72	f	1	2017-08-17 13:52:06.019174	5	f
63	64	73	f	1	2017-08-17 13:52:06.019257	5	f
64	65	74	f	1	2017-08-17 13:52:06.019338	5	f
65	66	75	f	1	2017-08-17 13:52:06.019425	5	f
66	67	77	f	1	2017-08-17 13:52:06.019507	7	f
67	68	78	f	1	2017-08-17 13:52:06.019587	7	f
68	69	79	f	1	2017-08-17 13:52:06.019668	7	f
69	70	80	f	1	2017-08-17 13:52:06.019752	7	f
70	70	81	f	1	2017-08-17 13:52:06.019833	7	f
71	71	82	f	1	2017-08-17 13:52:06.019913	7	f
\.


--
-- Name: premises_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('premises_uid_seq', 71, true);


--
-- Data for Name: reputation_history; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY reputation_history (uid, reputator_uid, reputation_uid, "timestamp") FROM stdin;
1	23	1	2017-08-15 13:52:08.832297
2	23	2	2017-08-16 13:52:08.832297
3	23	3	2017-08-17 13:52:08.832297
4	25	1	2017-08-15 13:52:08.832297
5	25	2	2017-08-16 13:52:08.832297
6	25	3	2017-08-17 13:52:08.832297
7	22	1	2017-08-15 13:52:08.832297
8	22	2	2017-08-16 13:52:08.832297
9	22	3	2017-08-17 13:52:08.832297
10	34	1	2017-08-15 13:52:08.832297
11	34	2	2017-08-16 13:52:08.832297
12	34	3	2017-08-17 13:52:08.832297
13	3	1	2017-08-15 13:52:08.832297
14	3	2	2017-08-16 13:52:08.832297
15	3	3	2017-08-17 13:52:08.832297
16	3	8	2017-08-17 13:52:08.832297
17	3	3	2017-08-15 13:52:08.832297
18	3	4	2017-08-15 13:52:08.832297
19	3	5	2017-08-16 13:52:08.832297
20	3	6	2017-08-16 13:52:08.832297
21	3	9	2017-08-17 13:52:08.832297
22	3	8	2017-08-17 13:52:08.832297
23	2	4	2017-08-15 13:52:08.832297
24	2	5	2017-08-15 13:52:08.832297
25	2	6	2017-08-16 13:52:08.832297
26	2	9	2017-08-16 13:52:08.832297
27	2	7	2017-08-17 13:52:08.832297
28	2	10	2017-08-17 13:52:08.832297
29	2	8	2017-08-17 13:52:08.832297
30	2	11	2017-08-17 13:52:08.832297
31	2	12	2017-08-17 13:52:08.832297
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
1	18	23	\N	2017-08-17 13:52:08.783996	t	1	f
2	19	7	\N	2017-08-17 13:52:08.784076	t	1	f
3	20	\N	19	2017-08-17 13:52:08.784152	t	2	f
4	21	\N	28	2017-08-17 13:52:08.784227	f	1	f
5	22	\N	11	2017-08-17 13:52:08.784303	f	1	f
6	23	\N	21	2017-08-17 13:52:08.784377	f	1	f
7	24	9	\N	2017-08-17 13:52:08.784452	f	2	f
8	25	6	\N	2017-08-17 13:52:08.784547	f	1	f
9	26	12	\N	2017-08-17 13:52:08.784622	f	1	f
10	27	1	\N	2017-08-17 13:52:08.784697	t	1	f
\.


--
-- Name: review_deletes_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('review_deletes_uid_seq', 10, true);


--
-- Data for Name: review_duplicates; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY review_duplicates (uid, detector_uid, duplicate_statement_uid, original_statement_uid, "timestamp", is_executed, is_revoked) FROM stdin;
1	28	6	1	2017-08-17 13:52:08.784777	f	f
2	29	4	1	2017-08-17 13:52:08.784851	t	f
3	29	22	7	2017-08-17 13:52:08.784919	f	f
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
1	3	\N	2	2017-08-17 13:52:08.845763	f	f
\.


--
-- Name: review_edits_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('review_edits_uid_seq', 1, true);


--
-- Data for Name: review_merge; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY review_merge (uid, detector_uid, premisesgroup_uid, "timestamp", is_executed, is_revoked) FROM stdin;
1	31	1	2017-08-17 13:52:08.784995	f	f
2	32	5	2017-08-17 13:52:08.785066	f	f
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
2	1	sadipscing elitr, sed diam nonumy eirmod (value02)
\.


--
-- Name: review_merge_values_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('review_merge_values_uid_seq', 2, true);


--
-- Data for Name: review_optimizations; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY review_optimizations (uid, detector_uid, argument_uid, statement_uid, "timestamp", is_executed, is_revoked) FROM stdin;
1	12	29	\N	2017-08-17 13:52:08.783426	t	f
2	13	\N	25	2017-08-17 13:52:08.783554	t	f
3	14	\N	8	2017-08-17 13:52:08.783644	f	f
4	16	13	\N	2017-08-17 13:52:08.783824	f	f
5	17	7	\N	2017-08-17 13:52:08.783897	f	f
6	15	\N	22	2017-08-17 13:52:08.783729	f	f
\.


--
-- Name: review_optimizations_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('review_optimizations_uid_seq', 6, true);


--
-- Data for Name: review_split; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY review_split (uid, detector_uid, premisesgroup_uid, "timestamp", is_executed, is_revoked) FROM stdin;
1	33	10	2017-08-17 13:52:08.785141	f	f
2	34	12	2017-08-17 13:52:08.785211	f	f
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
1208	1	17
1209	1	32
1210	1	18
1211	1	15
1212	1	24
1213	1	23
1214	1	27
1215	1	26
1216	1	21
1217	1	7
1218	1	9
1219	2	25
1220	2	31
1221	2	32
1222	2	9
1223	2	26
1224	2	12
1225	2	21
1226	2	7
1227	2	37
1228	2	33
1229	2	35
1230	2	8
1231	2	10
1232	2	19
1233	2	29
1234	2	28
1235	3	23
1236	3	19
1237	3	33
1238	3	11
1239	3	22
1240	3	14
1241	3	24
1242	3	20
1243	3	25
1244	3	28
1245	4	23
1246	4	12
1247	4	9
1248	4	17
1249	4	36
1250	4	33
1251	4	26
1252	4	29
1253	4	37
1254	4	29
1255	4	16
1256	4	21
1257	4	34
1258	4	28
1259	4	25
1260	4	7
1261	4	27
1262	4	20
1263	4	31
1264	4	11
1265	5	35
1266	5	26
1267	5	32
1268	5	14
1269	5	27
1270	5	15
1271	5	29
1272	5	22
1273	5	37
1274	5	19
1275	5	10
1276	5	24
1277	5	18
1278	5	28
1279	5	16
1280	5	12
1281	8	20
1282	8	9
1283	8	37
1284	8	14
1285	8	11
1286	8	29
1287	8	13
1288	8	7
1289	8	21
1290	8	32
1291	8	18
1292	8	23
1293	8	31
1294	8	22
1295	8	33
1296	8	24
1297	8	25
1298	8	36
1299	8	27
1300	8	19
1301	8	12
1302	8	8
1303	8	34
1304	8	10
1305	8	28
1306	8	29
1307	8	26
1308	8	35
1309	10	13
1310	10	23
1311	10	31
1312	10	32
1313	10	17
1314	10	15
1315	10	11
1316	10	22
1317	10	8
1318	10	27
1319	10	25
1320	10	37
1321	10	20
1322	10	29
1323	10	28
1324	10	33
1325	10	21
1326	10	36
1327	10	34
1328	10	24
1329	10	19
1330	10	35
1331	10	26
1332	10	9
1333	10	16
1334	10	12
1335	11	20
1336	11	7
1337	11	22
1338	11	29
1339	11	32
1340	11	17
1341	11	27
1342	11	34
1343	11	16
1344	11	33
1345	11	28
1346	11	29
1347	11	23
1348	11	13
1349	11	18
1350	11	24
1351	11	15
1352	11	31
1353	11	37
1354	11	21
1355	11	25
1356	11	26
1357	11	12
1358	11	9
1359	11	11
1360	11	14
1361	11	19
1362	11	10
1363	12	14
1364	12	37
1365	12	23
1366	12	18
1367	12	21
1368	15	17
1369	15	36
1370	15	35
1371	15	32
1372	15	29
1373	15	22
1374	15	19
1375	15	21
1376	15	13
1377	16	20
1378	16	28
1379	16	24
1380	16	16
1381	16	12
1382	16	27
1383	16	18
1384	16	33
1385	16	26
1386	16	29
1387	16	21
1388	16	10
1389	16	13
1390	16	11
1391	16	14
1392	16	7
1393	17	9
1394	17	29
1395	17	8
1396	17	34
1397	17	18
1398	17	17
1399	17	31
1400	17	24
1401	17	20
1402	17	23
1403	17	35
1404	17	29
1405	17	37
1406	17	27
1407	17	19
1408	17	16
1409	19	12
1410	19	36
1411	19	28
1412	19	10
1413	19	19
1414	19	9
1415	19	33
1416	19	32
1417	19	15
1418	19	23
1419	19	29
1420	19	17
1421	19	8
1422	19	21
1423	19	14
1424	19	25
1425	19	22
1426	19	24
1427	19	13
1428	19	11
1429	19	18
1430	19	27
1431	19	31
1432	19	26
1433	19	20
1434	19	34
1435	19	7
1436	19	35
1437	20	7
1438	20	11
1439	20	20
1440	20	18
1441	20	10
1442	20	35
1443	21	33
1444	21	23
1445	21	11
1446	21	17
1447	21	28
1448	21	34
1449	21	12
1450	21	36
1451	21	31
1452	21	16
1453	21	26
1454	21	21
1455	21	8
1456	21	32
1457	21	29
1458	21	25
1459	21	22
1460	21	10
1461	23	26
1462	23	31
1463	23	18
1464	23	25
1465	23	21
1466	23	13
1467	23	23
1468	23	8
1469	23	35
1470	23	7
1471	23	17
1472	23	19
1473	23	34
1474	23	24
1475	23	14
1476	23	32
1477	23	12
1478	23	33
1479	23	11
1480	23	29
1481	23	27
1482	23	9
1483	23	37
1484	23	22
1485	23	15
1486	24	14
1487	24	34
1488	24	24
1489	24	21
1490	24	15
1491	24	36
1492	24	11
1493	24	29
1494	24	10
1495	24	32
1496	24	18
1497	24	37
1498	24	17
1499	24	23
1500	24	25
1501	24	16
1502	24	12
1503	24	29
1504	24	31
1505	24	35
1506	24	33
1507	24	19
1508	24	27
1509	24	22
1510	24	9
1511	24	8
1512	26	27
1513	26	8
1514	26	22
1515	26	33
1516	26	34
1517	26	23
1518	26	31
1519	26	35
1520	26	9
1521	26	29
1522	26	24
1523	27	14
1524	27	34
1525	27	37
1526	27	20
1527	27	32
1528	28	20
1529	28	21
1530	28	32
1531	28	24
1532	28	26
1533	28	23
1534	28	9
1535	28	7
1536	28	18
1537	28	27
1538	28	15
1539	28	29
1540	28	34
1541	28	22
1542	28	25
1543	28	33
1544	28	31
1545	28	19
1546	28	13
1547	28	8
1548	28	37
1549	28	12
1550	28	35
1551	28	36
1552	29	24
1553	29	13
1554	29	32
1555	29	9
1556	29	15
1557	29	18
1558	29	12
1559	29	16
1560	29	36
1561	29	29
1562	29	22
1563	29	19
1564	29	23
1565	29	20
1566	29	27
1567	29	34
1568	29	8
1569	29	31
1570	29	17
1571	29	21
1572	29	10
1573	29	29
1574	29	35
1575	29	28
1576	29	25
1577	29	26
1578	30	32
1579	30	13
1580	30	16
1581	30	7
1582	30	29
1583	30	21
1584	30	27
1585	30	15
1586	30	10
1587	30	23
1588	30	11
1589	30	29
1590	30	24
1591	30	22
1592	30	33
1593	30	37
1594	30	12
1595	30	14
1596	30	9
1597	30	18
1598	30	19
1599	30	25
1600	30	8
1601	30	17
1602	30	31
1603	30	36
1604	30	28
1605	32	15
1606	32	19
1607	32	21
1608	32	29
1609	32	23
1610	32	20
1611	32	29
1612	32	36
1613	32	33
1614	32	24
1615	32	25
1616	32	10
1617	32	7
1618	32	32
1619	32	34
1620	34	23
1621	34	25
1622	34	15
1623	34	19
1624	34	26
1625	34	9
1626	34	37
1627	34	22
1628	34	29
1629	34	21
1630	34	20
1631	34	31
1632	34	33
1633	34	8
1634	34	17
1635	34	16
1636	34	36
1637	34	32
1638	34	7
1639	34	34
1640	35	15
1641	35	12
1642	35	35
1643	35	23
1644	35	36
1645	35	26
1646	35	21
1647	35	22
1648	36	7
1649	36	21
1650	36	26
1651	36	17
1652	36	37
1653	36	18
1654	36	31
1655	36	15
1656	36	11
1657	39	18
1658	39	13
1659	39	12
1660	39	24
1661	39	29
1662	39	11
1663	40	7
1664	40	28
1665	40	11
1666	40	27
1667	40	20
1668	40	12
1669	40	17
1670	41	15
1671	41	12
1672	41	24
1673	41	36
1674	41	22
1675	41	9
1676	41	7
1677	41	37
1678	41	8
1679	41	32
1680	41	14
1681	41	29
1682	42	27
1683	42	33
1684	42	15
1685	42	35
1686	42	29
1687	42	19
1688	42	7
1689	42	29
1690	42	32
1691	42	34
1692	42	26
1693	42	14
1694	42	18
1695	42	13
1696	42	12
1697	42	21
1698	42	16
1699	42	8
1700	42	31
1701	42	24
1702	42	11
1703	42	25
1704	42	28
1705	42	22
1706	42	37
1707	42	9
1708	42	36
1709	44	29
1710	44	13
1711	44	8
1712	44	31
1713	44	17
1714	44	33
1715	44	14
1716	44	24
1717	44	37
1718	44	35
1719	44	32
1720	44	28
1721	44	18
1722	44	20
1723	44	10
1724	44	19
1725	44	36
1726	44	29
1727	44	11
1728	44	21
1729	44	25
1730	44	26
1731	46	24
1732	46	11
1733	46	32
1734	46	23
1735	46	14
1736	46	37
1737	46	21
1738	46	35
1739	46	29
1740	46	7
1741	46	31
1742	46	26
1743	46	22
1744	46	19
1745	46	8
1746	46	15
1747	46	18
1748	46	12
1749	47	9
1750	47	20
1751	47	33
1752	47	17
1753	47	37
1754	47	28
1755	47	19
1756	47	8
1757	47	31
1758	47	15
1759	47	13
1760	47	22
1761	47	26
1762	47	34
1763	47	11
1764	47	21
1765	47	12
1766	47	16
1767	47	23
1768	47	29
1769	47	7
1770	47	32
1771	47	24
1772	47	27
1773	47	29
1774	47	18
1775	47	14
1776	49	33
1777	49	16
1778	49	7
1779	49	25
1780	49	24
1781	49	20
1782	49	26
1783	49	36
1784	49	27
1785	49	13
1786	49	15
1787	49	14
1788	49	34
1789	49	10
1790	49	31
1791	49	21
1792	49	9
1793	49	19
1794	49	12
1795	49	22
1796	49	32
1797	49	37
1798	49	29
1799	50	31
1800	50	16
1801	50	34
1802	50	24
1803	50	25
1804	50	28
1805	50	33
1806	50	12
1807	50	27
1808	50	32
1809	50	29
1810	50	14
1811	50	19
1812	50	20
1813	50	37
1814	50	35
1815	51	37
1816	51	9
1817	51	28
1818	51	35
1819	51	24
1820	51	23
1821	51	21
1822	51	29
1823	51	20
1824	51	36
1825	51	12
1826	51	25
1827	51	10
1828	51	15
1829	51	31
1830	51	7
1831	51	18
1832	51	22
1833	51	16
1834	51	33
1835	51	13
1836	51	34
1837	51	32
1838	51	27
1839	51	26
1840	51	14
1841	51	19
1842	51	11
1843	51	17
1844	54	35
1845	54	27
1846	54	37
1847	54	31
1848	54	29
1849	54	32
1850	54	24
1851	54	29
1852	54	15
1853	54	22
1854	54	28
1855	54	12
1856	54	9
1857	55	31
1858	55	11
1859	55	34
1860	55	8
1861	55	33
1862	55	17
1863	55	25
1864	55	14
1865	55	18
1866	55	19
1867	55	24
1868	55	21
1869	55	22
1870	55	23
1871	56	17
1872	56	12
1873	56	24
1874	56	7
1875	56	29
1876	56	18
1877	56	27
1878	56	8
1879	56	15
1880	56	28
1881	56	29
1882	56	35
1883	56	14
1884	56	11
1885	56	13
1886	56	31
1887	56	37
1888	56	10
1889	56	23
1890	56	32
1891	56	9
1892	56	33
1893	56	21
1894	56	16
1895	56	20
1896	56	26
1897	56	25
1898	57	20
1899	57	27
1900	57	35
1901	57	22
1902	57	37
1903	57	10
1904	57	25
1905	57	8
1906	58	19
1907	58	10
1908	58	21
1909	58	37
1910	58	17
1911	58	15
1912	58	20
1913	58	29
1914	58	24
1915	59	25
1916	59	26
1917	59	31
1918	59	22
1919	59	19
1920	59	8
1921	59	20
1922	59	16
1923	59	9
1924	59	24
1925	59	35
1926	59	7
1927	59	21
1928	59	28
1929	59	29
1930	60	29
1931	60	10
1932	60	27
1933	60	17
1934	60	8
1935	60	24
1936	60	16
1937	60	32
1938	60	35
1939	60	20
1940	60	29
1941	60	23
1942	60	28
1943	60	7
1944	60	21
1945	60	9
1946	60	31
1947	60	12
1948	60	36
1949	60	11
1950	60	13
1951	60	33
1952	60	18
1953	60	26
1954	60	37
1955	60	14
1956	60	19
1957	61	32
1958	61	11
1959	61	18
1960	61	10
1961	61	24
1962	61	23
1963	61	16
1964	61	12
1965	61	22
1966	61	19
1967	61	25
1968	61	33
1969	62	33
1970	62	23
1971	62	12
1972	62	14
1973	62	16
1974	62	27
1975	62	18
1976	62	26
1977	62	19
1978	62	9
1979	62	34
1980	62	11
1981	62	17
1982	62	15
1983	62	37
1984	62	13
1985	63	12
1986	63	9
1987	63	16
1988	63	37
1989	63	18
1990	63	27
1991	63	31
1992	63	22
1993	63	7
1994	63	13
1995	63	29
1996	63	10
1997	63	23
1998	63	34
1999	63	32
2000	63	14
2001	63	17
2002	63	21
2003	63	24
2004	63	29
2005	63	15
2006	63	35
2007	64	7
2008	64	19
2009	64	13
2010	64	15
2011	64	11
2012	64	35
2013	64	25
2014	64	26
2015	64	12
2016	64	24
2017	64	18
2018	64	28
2019	64	20
2020	64	8
2021	64	16
2022	64	17
2023	64	21
2024	65	18
2025	65	17
2026	65	29
2027	65	8
2028	65	33
2029	65	15
2030	65	12
2031	65	23
2032	66	28
2033	66	24
2034	66	35
2035	66	23
2036	66	25
2037	66	9
2038	66	7
2039	66	31
2040	66	26
2041	66	29
2042	66	13
2043	66	20
2044	66	11
2045	66	36
2046	66	15
2047	66	32
2048	66	8
2049	66	14
2050	66	29
2051	66	18
2052	66	21
2053	66	34
2054	66	16
2055	66	12
2056	67	18
2057	67	37
2058	67	27
2059	67	35
2060	67	32
2061	67	15
2062	67	26
2063	67	11
2064	67	20
2065	67	34
2066	67	9
2067	67	10
2068	67	16
2069	67	12
2070	67	14
2071	67	23
2072	67	33
2073	68	37
2074	68	21
2075	68	15
2076	68	10
2077	68	29
2078	68	8
2079	68	33
2080	68	32
2081	68	7
2082	68	31
2083	68	29
2084	68	25
2085	68	13
2086	68	12
2087	68	36
2088	68	11
2089	68	34
2090	6	34
2091	6	29
2092	6	24
2093	6	27
2094	6	25
2095	6	11
2096	6	12
2097	6	36
2098	6	26
2099	6	8
2100	6	20
2101	6	35
2102	6	33
2103	6	31
2104	6	32
2105	6	28
2106	6	29
2107	6	16
2108	7	37
2109	7	14
2110	7	21
2111	7	28
2112	7	13
2113	7	8
2114	9	22
2115	9	26
2116	9	27
2117	9	37
2118	9	13
2119	9	31
2120	9	8
2121	9	29
2122	13	18
2123	13	32
2124	13	21
2125	13	9
2126	13	7
2127	13	11
2128	13	26
2129	13	27
2130	13	22
2131	13	17
2132	13	33
2133	13	37
2134	13	34
2135	13	25
2136	13	16
2137	13	36
2138	13	29
2139	13	14
2140	14	34
2141	14	22
2142	14	26
2143	14	14
2144	14	32
2145	14	35
2146	14	36
2147	18	37
2148	18	7
2149	18	26
2150	18	27
2151	18	20
2152	18	28
2153	18	36
2154	18	10
2155	18	29
2156	18	8
2157	18	13
2158	18	24
2159	18	15
2160	18	31
2161	18	17
2162	18	29
2163	18	23
2164	18	9
2165	18	34
2166	22	14
2167	22	28
2168	22	11
2169	22	15
2170	22	29
2171	22	33
2172	22	22
2173	22	25
2174	22	34
2175	22	9
2176	22	29
2177	22	23
2178	22	37
2179	22	17
2180	22	24
2181	22	27
2182	22	26
2183	25	36
2184	25	32
2185	25	26
2186	25	13
2187	25	37
2188	25	35
2189	25	10
2190	25	19
2191	31	13
2192	31	27
2193	31	34
2194	31	18
2195	31	37
2196	31	28
2197	31	24
2198	31	36
2199	31	26
2200	31	32
2201	31	19
2202	31	29
2203	31	10
2204	31	23
2205	31	21
2206	31	31
2207	31	35
2208	31	15
2209	31	20
2210	33	12
2211	33	17
2212	33	11
2213	33	31
2214	33	29
2215	33	13
2216	33	24
2217	33	8
2218	33	19
2219	33	26
2220	33	28
2221	33	27
2222	33	21
2223	33	23
2224	37	29
2225	37	28
2226	37	36
2227	37	29
2228	37	33
2229	37	18
2230	38	33
2231	38	18
2232	38	23
2233	38	17
2234	38	8
2235	38	20
2236	43	34
2237	43	27
2238	43	13
2239	43	19
2240	43	33
2241	43	9
2242	43	23
2243	43	17
2244	43	16
2245	43	10
2246	43	29
2247	43	29
2248	43	14
2249	45	13
2250	45	24
2251	45	29
2252	45	28
2253	45	22
2254	45	25
2255	45	27
2256	45	32
2257	45	7
2258	45	12
2259	45	35
2260	45	16
2261	45	20
2262	45	9
2263	45	14
2264	45	11
2265	45	31
2266	45	26
2267	48	8
2268	48	21
2269	48	36
2270	48	24
2271	48	16
2272	48	35
2273	48	28
2274	48	11
2275	48	20
2276	48	17
2277	48	9
2278	48	31
2279	48	37
2280	48	19
2281	48	10
2282	48	32
2283	48	18
2284	48	12
2285	48	25
2286	48	14
2287	48	15
2288	48	22
2289	48	34
2290	48	26
2291	52	23
2292	52	14
2293	52	24
2294	52	27
2295	52	20
2296	52	15
2297	52	7
2298	52	32
2299	52	13
2300	52	29
2301	52	10
2302	52	22
2303	52	21
2304	52	36
2305	52	31
2306	52	37
2307	52	28
2308	52	19
2309	52	26
2310	52	34
2311	53	13
2312	53	8
2313	53	16
2314	53	21
2315	53	26
2316	53	20
2317	53	28
2318	69	19
2319	69	26
2320	69	29
2321	69	23
2322	69	17
2323	69	14
2324	69	16
2325	69	12
2326	69	11
2327	69	33
2328	69	10
2329	69	9
2330	69	29
2331	69	7
2332	69	24
2333	69	36
2334	69	28
2335	69	32
2336	69	27
2337	69	35
2338	69	25
2339	69	37
2340	69	22
2341	69	18
2342	69	15
2343	69	8
2344	69	13
2345	69	31
\.


--
-- Name: seen_arguments_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('seen_arguments_uid_seq', 2345, true);


--
-- Data for Name: seen_statements; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY seen_statements (uid, statement_uid, user_uid) FROM stdin;
1395	1	23
1396	1	14
1397	1	35
1398	1	15
1399	1	22
1400	1	33
1401	1	29
1402	1	26
1403	1	18
1404	1	25
1405	1	16
1406	2	14
1407	2	19
1408	2	9
1409	2	33
1410	2	28
1411	2	18
1412	2	8
1413	2	35
1414	2	25
1415	2	23
1416	2	16
1417	2	20
1418	2	27
1419	2	36
1420	2	11
1421	2	15
1422	2	21
1423	2	13
1424	2	29
1425	2	24
1426	2	32
1427	2	26
1428	3	32
1429	3	23
1430	3	27
1431	3	20
1432	3	29
1433	3	11
1434	3	28
1435	3	37
1436	3	36
1437	3	9
1438	3	24
1439	3	16
1440	3	19
1441	3	7
1442	3	10
1443	3	29
1444	3	17
1445	3	12
1446	3	34
1447	3	14
1448	3	26
1449	3	18
1450	3	31
1451	3	22
1452	3	25
1453	3	21
1454	4	21
1455	4	18
1456	4	29
1457	4	19
1458	4	22
1459	4	25
1460	4	28
1461	4	34
1462	4	23
1463	4	15
1464	4	16
1465	4	14
1466	4	35
1467	4	10
1468	4	26
1469	4	20
1470	4	32
1471	4	27
1472	4	31
1473	4	17
1474	4	33
1475	4	7
1476	4	12
1477	4	9
1478	5	29
1479	5	24
1480	5	28
1481	5	37
1482	5	7
1483	5	15
1484	5	27
1485	5	11
1486	5	12
1487	5	22
1488	5	34
1489	5	16
1490	5	17
1491	5	26
1492	5	23
1493	5	19
1494	5	29
1495	5	21
1496	5	9
1497	5	33
1498	5	14
1499	5	25
1500	5	35
1501	5	32
1502	6	22
1503	6	21
1504	6	17
1505	6	31
1506	6	36
1507	6	28
1508	6	29
1509	6	15
1510	6	12
1511	6	10
1512	6	13
1513	6	14
1514	6	11
1515	6	35
1516	6	16
1517	6	32
1518	6	18
1519	7	19
1520	7	13
1521	7	16
1522	7	23
1523	7	7
1524	7	29
1525	7	24
1526	7	33
1527	7	12
1528	7	9
1529	7	31
1530	7	27
1531	7	29
1532	8	13
1533	8	33
1534	8	29
1535	8	15
1536	8	11
1537	8	21
1538	8	9
1539	8	25
1540	8	23
1541	9	24
1542	9	23
1543	9	18
1544	9	34
1545	9	31
1546	9	27
1547	9	22
1548	9	19
1549	9	28
1550	9	9
1551	9	11
1552	9	10
1553	9	32
1554	9	17
1555	9	13
1556	9	36
1557	9	37
1558	9	12
1559	9	15
1560	9	33
1561	9	29
1562	10	31
1563	10	26
1564	10	13
1565	10	15
1566	10	25
1567	10	27
1568	10	18
1569	10	36
1570	10	16
1571	10	8
1572	10	35
1573	10	20
1574	10	11
1575	10	29
1576	10	24
1577	10	17
1578	10	29
1579	10	9
1580	10	32
1581	11	8
1582	11	15
1583	11	35
1584	11	18
1585	11	29
1586	11	11
1587	11	32
1588	11	7
1589	11	21
1590	11	36
1591	11	33
1592	11	17
1593	11	9
1594	11	13
1595	11	27
1596	11	25
1597	11	37
1598	11	22
1599	11	24
1600	11	16
1601	12	24
1602	12	11
1603	12	20
1604	12	10
1605	12	18
1606	12	36
1607	12	9
1608	12	16
1609	12	28
1610	12	27
1611	12	13
1612	12	37
1613	12	23
1614	12	34
1615	12	12
1616	12	14
1617	12	29
1618	12	31
1619	12	17
1620	12	21
1621	13	17
1622	13	27
1623	13	29
1624	13	21
1625	13	20
1626	13	36
1627	14	9
1628	14	13
1629	14	21
1630	14	16
1631	14	8
1632	14	10
1633	14	25
1634	14	29
1635	15	26
1636	15	10
1637	15	29
1638	15	20
1639	15	18
1640	15	28
1641	16	31
1642	16	23
1643	16	29
1644	16	29
1645	16	20
1646	16	13
1647	16	18
1648	16	24
1649	16	17
1650	16	15
1651	16	36
1652	16	33
1653	16	14
1654	16	10
1655	16	28
1656	16	12
1657	16	32
1658	17	19
1659	17	15
1660	17	34
1661	17	14
1662	17	8
1663	17	22
1664	17	32
1665	17	29
1666	17	37
1667	18	14
1668	18	36
1669	18	34
1670	18	8
1671	18	13
1672	18	29
1673	18	22
1674	18	19
1675	18	33
1676	18	29
1677	19	16
1678	19	37
1679	19	33
1680	19	7
1681	20	14
1682	20	32
1683	20	20
1684	20	16
1685	20	28
1686	20	17
1687	20	10
1688	20	35
1689	20	33
1690	20	24
1691	20	29
1692	20	8
1693	20	19
1694	20	29
1695	20	11
1696	20	27
1697	20	18
1698	20	26
1699	20	34
1700	20	22
1701	20	15
1702	20	23
1703	20	25
1704	20	9
1705	21	28
1706	21	8
1707	21	37
1708	21	31
1709	21	17
1710	21	13
1711	21	35
1712	22	18
1713	22	16
1714	22	7
1715	22	31
1716	22	8
1717	22	21
1718	22	25
1719	22	32
1720	22	17
1721	22	14
1722	22	20
1723	22	36
1724	22	19
1725	22	33
1726	22	24
1727	22	35
1728	22	10
1729	22	37
1730	22	22
1731	23	18
1732	23	26
1733	23	24
1734	23	25
1735	23	15
1736	23	34
1737	24	11
1738	24	29
1739	24	9
1740	24	17
1741	24	23
1742	24	28
1743	25	37
1744	25	19
1745	25	24
1746	25	27
1747	25	34
1748	25	29
1749	25	25
1750	25	21
1751	25	12
1752	25	35
1753	25	10
1754	26	31
1755	26	29
1756	26	18
1757	26	36
1758	26	9
1759	26	14
1760	26	22
1761	26	12
1762	26	21
1763	26	11
1764	26	7
1765	26	32
1766	26	20
1767	27	21
1768	27	29
1769	27	31
1770	27	29
1771	27	10
1772	27	11
1773	27	35
1774	27	14
1775	28	18
1776	28	29
1777	28	13
1778	28	35
1779	28	23
1780	28	10
1781	28	31
1782	28	27
1783	28	19
1784	28	34
1785	28	33
1786	28	16
1787	28	15
1788	28	21
1789	28	32
1790	28	22
1791	28	7
1792	28	24
1793	28	36
1794	28	14
1795	28	11
1796	28	29
1797	28	8
1798	28	20
1799	28	37
1800	28	12
1801	28	17
1802	28	28
1803	28	25
1804	29	8
1805	29	37
1806	29	33
1807	29	34
1808	29	19
1809	29	36
1810	29	20
1811	29	29
1812	29	15
1813	29	32
1814	29	10
1815	29	14
1816	29	11
1817	29	27
1818	29	29
1819	29	12
1820	29	16
1821	29	24
1822	29	21
1823	29	13
1824	29	28
1825	29	22
1826	29	25
1827	29	7
1828	29	17
1829	29	23
1830	29	35
1831	29	18
1832	30	27
1833	30	29
1834	30	8
1835	30	37
1836	30	12
1837	30	26
1838	30	7
1839	30	22
1840	30	25
1841	30	36
1842	30	32
1843	30	14
1844	30	28
1845	30	9
1846	31	28
1847	31	13
1848	31	37
1849	31	15
1850	31	33
1851	31	7
1852	31	32
1853	31	29
1854	31	12
1855	31	8
1856	31	34
1857	31	31
1858	31	19
1859	31	9
1860	31	26
1861	31	16
1862	31	11
1863	31	17
1864	32	29
1865	32	36
1866	32	17
1867	32	37
1868	32	20
1869	32	29
1870	32	35
1871	32	31
1872	32	24
1873	32	7
1874	32	21
1875	33	34
1876	33	37
1877	33	29
1878	33	9
1879	33	19
1880	33	10
1881	33	21
1882	33	33
1883	33	11
1884	33	32
1885	33	15
1886	33	16
1887	33	31
1888	33	27
1889	33	25
1890	33	26
1891	33	18
1892	33	28
1893	33	13
1894	33	12
1895	33	36
1896	33	35
1897	33	8
1898	33	23
1899	33	24
1900	33	17
1901	33	7
1902	33	20
1903	34	26
1904	34	24
1905	34	36
1906	34	13
1907	34	35
1908	34	8
1909	34	22
1910	34	7
1911	34	34
1912	34	25
1913	34	16
1914	34	37
1915	34	32
1916	34	10
1917	34	29
1918	34	29
1919	35	21
1920	35	18
1921	35	17
1922	35	19
1923	35	11
1924	35	28
1925	35	14
1926	36	31
1927	36	35
1928	36	26
1929	36	11
1930	36	34
1931	36	23
1932	36	20
1933	36	13
1934	36	28
1935	36	9
1936	36	18
1937	36	25
1938	37	16
1939	37	28
1940	37	23
1941	37	18
1942	37	22
1943	37	8
1944	37	19
1945	37	29
1946	37	20
1947	37	27
1948	37	9
1949	37	24
1950	37	12
1951	37	29
1952	37	36
1953	37	32
1954	37	7
1955	37	17
1956	37	11
1957	37	15
1958	37	14
1959	38	33
1960	38	27
1961	38	32
1962	38	28
1963	38	29
1964	38	16
1965	38	17
1966	38	8
1967	38	25
1968	38	18
1969	38	22
1970	38	19
1971	38	37
1972	38	26
1973	38	7
1974	38	34
1975	38	36
1976	38	31
1977	38	14
1978	38	21
1979	38	35
1980	38	13
1981	38	29
1982	38	23
1983	38	10
1984	38	9
1985	38	15
1986	38	20
1987	38	11
1988	39	18
1989	39	34
1990	39	17
1991	39	25
1992	39	27
1993	39	37
1994	39	33
1995	39	14
1996	39	16
1997	39	31
1998	39	29
1999	39	12
2000	39	11
2001	40	16
2002	40	11
2003	40	13
2004	40	27
2005	40	35
2006	40	20
2007	40	33
2008	40	28
2009	40	9
2010	40	12
2011	40	25
2012	40	36
2013	40	10
2014	40	29
2015	40	24
2016	40	7
2017	40	34
2018	40	31
2019	40	22
2020	40	14
2021	40	17
2022	40	29
2023	40	37
2024	40	26
2025	40	15
2026	40	23
2027	41	29
2028	41	33
2029	41	11
2030	41	27
2031	42	31
2032	42	19
2033	42	25
2034	42	34
2035	42	33
2036	42	16
2037	42	17
2038	42	24
2039	42	28
2040	42	20
2041	42	36
2042	42	15
2043	42	11
2044	42	13
2045	42	7
2046	42	9
2047	42	27
2048	42	23
2049	43	27
2050	43	14
2051	43	15
2052	43	11
2053	44	23
2054	44	33
2055	44	34
2056	44	36
2057	44	20
2058	44	28
2059	44	24
2060	44	29
2061	44	32
2062	44	18
2063	44	35
2064	44	16
2065	44	7
2066	44	9
2067	44	17
2068	44	19
2069	44	8
2070	44	26
2071	44	31
2072	44	11
2073	44	10
2074	44	37
2075	44	22
2076	44	29
2077	44	21
2078	44	13
2079	44	25
2080	45	36
2081	45	34
2082	45	31
2083	45	29
2084	45	22
2085	46	17
2086	46	29
2087	46	33
2088	46	14
2089	46	35
2090	46	8
2091	46	32
2092	46	15
2093	46	36
2094	46	28
2095	46	16
2096	46	22
2097	46	11
2098	46	34
2099	46	37
2100	46	24
2101	47	36
2102	47	35
2103	47	31
2104	47	21
2105	47	22
2106	47	13
2107	47	32
2108	47	25
2109	47	26
2110	48	31
2111	48	25
2112	48	28
2113	48	12
2114	48	14
2115	48	24
2116	48	17
2117	48	10
2118	48	29
2119	48	37
2120	48	21
2121	48	9
2122	48	29
2123	48	35
2124	48	33
2125	48	36
2126	48	27
2127	48	16
2128	48	18
2129	48	26
2130	48	23
2131	49	26
2132	49	8
2133	49	31
2134	49	20
2135	49	10
2136	49	25
2137	49	18
2138	49	23
2139	49	12
2140	49	29
2141	49	37
2142	49	11
2143	49	36
2144	49	14
2145	49	17
2146	49	33
2147	49	34
2148	49	21
2149	49	28
2150	49	24
2151	50	29
2152	50	24
2153	50	20
2154	50	34
2155	50	36
2156	50	29
2157	50	31
2158	50	17
2159	50	11
2160	50	22
2161	50	37
2162	50	18
2163	50	32
2164	50	26
2165	50	21
2166	50	19
2167	50	13
2168	50	9
2169	50	10
2170	50	27
2171	50	12
2172	50	16
2173	50	28
2174	50	8
2175	50	35
2176	50	7
2177	50	15
2178	51	36
2179	51	28
2180	51	33
2181	51	24
2182	51	11
2183	51	37
2184	51	13
2185	51	17
2186	51	32
2187	51	29
2188	51	22
2189	51	26
2190	51	31
2191	51	34
2192	51	19
2193	51	25
2194	52	20
2195	52	16
2196	52	27
2197	52	34
2198	52	24
2199	52	33
2200	52	18
2201	52	12
2202	53	20
2203	53	13
2204	53	24
2205	53	37
2206	53	28
2207	53	15
2208	53	25
2209	53	8
2210	53	32
2211	53	11
2212	53	9
2213	53	29
2214	53	10
2215	54	7
2216	54	29
2217	54	11
2218	54	9
2219	54	35
2220	54	28
2221	54	36
2222	54	21
2223	54	26
2224	54	12
2225	54	24
2226	54	32
2227	54	13
2228	54	8
2229	54	15
2230	54	14
2231	54	25
2232	54	22
2233	54	18
2234	54	29
2235	54	10
2236	54	37
2237	54	27
2238	54	16
2239	54	17
2240	54	31
2241	54	20
2242	54	23
2243	55	24
2244	55	17
2245	55	16
2246	55	8
2247	55	15
2248	55	7
2249	55	31
2250	55	19
2251	55	12
2252	55	21
2253	55	20
2254	55	35
2255	55	26
2256	55	32
2257	55	10
2258	55	27
2259	55	13
2260	55	11
2261	55	37
2262	55	25
2263	55	14
2264	55	34
2265	55	9
2266	55	33
2267	55	36
2268	55	23
2269	55	22
2270	55	29
2271	56	16
2272	56	31
2273	56	27
2274	56	23
2275	56	28
2276	56	12
2277	57	35
2278	57	29
2279	57	29
2280	57	18
2281	57	21
2282	57	19
2283	58	27
2284	58	7
2285	58	31
2286	58	35
2287	58	29
2288	58	34
2289	58	11
2290	58	24
2291	58	22
2292	58	18
2293	58	10
2294	59	31
2295	59	22
2296	59	14
2297	59	11
2298	59	29
2299	59	21
2300	59	16
2301	59	18
2302	59	37
2303	59	35
2304	59	13
2305	59	26
2306	59	20
2307	59	28
2308	59	27
2309	59	25
2310	59	24
2311	59	12
2312	59	8
2313	59	7
2314	59	23
2315	59	9
2316	59	33
2317	59	15
2318	59	29
2319	59	19
2320	59	32
2321	60	34
2322	60	18
2323	60	11
2324	60	33
2325	60	31
2326	60	17
2327	60	10
2328	60	27
2329	60	37
2330	60	22
2331	60	23
2332	60	29
2333	60	13
2334	61	20
2335	61	13
2336	61	31
2337	61	16
2338	61	36
2339	61	28
2340	61	25
2341	61	37
2342	61	29
2343	62	21
2344	62	27
2345	62	36
2346	62	14
2347	62	34
2348	62	25
2349	62	23
2350	62	12
2351	62	17
2352	62	8
2353	62	7
2354	62	33
2355	62	26
2356	62	31
2357	63	13
2358	63	26
2359	63	17
2360	63	29
2361	63	29
2362	63	24
2363	63	11
2364	63	33
2365	63	37
2366	63	31
2367	63	15
2368	63	34
2369	63	18
2370	64	37
2371	64	14
2372	64	24
2373	64	26
2374	64	22
2375	64	9
2376	64	25
2377	64	11
2378	64	32
2379	64	28
2380	64	34
2381	64	29
2382	64	8
2383	64	13
2384	64	18
2385	64	29
2386	64	15
2387	64	21
2388	65	24
2389	65	22
2390	65	36
2391	65	10
2392	65	33
2393	65	28
2394	65	23
2395	65	15
2396	65	25
2397	65	29
2398	65	34
2399	65	26
2400	65	9
2401	65	12
2402	65	29
2403	65	35
2404	65	8
2405	65	17
2406	65	13
2407	65	21
2408	65	7
2409	65	16
2410	65	14
2411	65	27
2412	65	18
2413	66	7
2414	66	20
2415	66	14
2416	66	12
2417	66	34
2418	66	9
2419	66	22
2420	66	35
2421	66	32
2422	66	29
2423	66	24
2424	66	10
2425	66	17
2426	66	18
2427	66	28
2428	66	15
2429	66	11
2430	66	37
2431	66	23
2432	66	27
2433	66	21
2434	66	26
2435	66	31
2436	66	33
2437	66	19
2438	66	13
2439	66	29
2440	66	16
2441	67	26
2442	67	29
2443	67	28
2444	67	29
2445	67	15
2446	67	14
2447	67	24
2448	67	17
2449	67	11
2450	67	32
2451	67	27
2452	67	18
2453	67	33
2454	67	9
2455	67	25
2456	67	37
2457	67	21
2458	67	7
2459	68	16
2460	68	22
2461	68	28
2462	68	9
2463	68	15
2464	69	31
2465	69	10
2466	69	18
2467	69	7
2468	69	25
2469	69	20
2470	69	14
2471	69	33
2472	69	9
2473	69	29
2474	69	13
2475	69	24
2476	69	26
2477	69	35
2478	69	11
2479	69	23
2480	69	28
2481	69	8
2482	69	22
2483	69	29
2484	69	12
2485	69	36
2486	69	16
2487	70	18
2488	70	33
2489	70	37
2490	70	25
2491	70	20
2492	70	15
2493	70	29
2494	70	31
2495	70	16
2496	70	7
2497	70	8
2498	70	32
2499	70	21
2500	70	12
2501	70	11
2502	70	27
2503	70	28
2504	70	14
2505	70	13
2506	70	22
2507	70	34
2508	70	35
2509	70	9
2510	70	24
2511	71	17
2512	71	19
2513	71	34
2514	71	7
2515	71	33
2516	71	26
2517	71	8
2518	71	12
2519	71	21
2520	71	31
2521	71	25
2522	71	29
2523	71	16
2524	71	28
2525	71	22
2526	71	14
2527	71	18
2528	71	10
2529	71	24
2530	71	20
2531	71	11
2532	71	36
2533	71	27
2534	71	9
2535	71	32
2536	72	24
2537	72	34
2538	72	12
2539	72	10
2540	72	8
2541	72	23
2542	72	16
2543	72	35
2544	73	29
2545	73	35
2546	73	13
2547	73	19
2548	73	36
2549	73	8
2550	73	32
2551	73	17
2552	73	15
2553	73	10
2554	73	29
2555	73	28
2556	73	18
2557	73	33
2558	74	17
2559	74	16
2560	74	32
2561	74	14
2562	74	27
2563	74	11
2564	74	10
2565	74	13
2566	74	36
2567	74	12
2568	74	8
2569	74	28
2570	74	21
2571	74	37
2572	74	35
2573	74	26
2574	74	34
2575	74	19
2576	74	18
2577	74	24
2578	74	23
2579	74	25
2580	74	20
2581	75	14
2582	75	7
2583	75	10
2584	75	37
2585	75	18
2586	75	13
2587	75	34
2588	75	32
2589	75	28
2590	75	27
2591	75	20
2592	75	17
2593	75	29
2594	75	21
2595	75	33
2596	75	22
2597	75	35
2598	75	36
2599	75	15
2600	76	13
2601	76	26
2602	76	33
2603	76	15
2604	76	19
2605	76	22
2606	76	21
2607	76	34
2608	76	24
2609	76	7
2610	76	36
2611	76	20
2612	76	10
2613	76	8
2614	76	31
2615	76	29
2616	76	25
2617	76	18
2618	76	32
2619	76	16
2620	76	35
2621	76	17
2622	76	27
2623	76	37
2624	77	37
2625	77	27
2626	77	26
2627	77	31
2628	77	36
2629	77	17
2630	77	33
2631	77	18
2632	77	19
2633	77	29
2634	77	23
2635	77	32
2636	78	28
2637	78	16
2638	78	33
2639	78	20
2640	78	32
2641	78	17
2642	78	29
2643	78	37
2644	78	11
2645	78	18
2646	78	7
2647	78	13
2648	78	34
2649	79	10
2650	79	36
2651	79	34
2652	79	28
2653	79	33
2654	79	31
2655	79	27
2656	79	20
2657	79	29
2658	79	7
2659	79	16
2660	79	29
2661	79	24
2662	79	15
2663	79	35
2664	79	11
2665	79	25
2666	79	9
2667	79	8
2668	80	31
2669	80	32
2670	80	34
2671	80	9
2672	80	29
2673	80	12
2674	80	21
2675	80	18
2676	80	29
2677	80	14
2678	80	22
2679	80	24
2680	80	33
2681	80	27
2682	80	13
2683	80	11
2684	80	23
2685	80	37
2686	80	16
2687	80	35
2688	80	25
2689	80	19
2690	80	26
2691	80	10
2692	80	15
2693	80	17
2694	80	7
2695	80	8
2696	80	36
2697	81	14
2698	81	35
2699	81	34
2700	81	31
2701	81	32
2702	81	7
2703	81	28
2704	81	33
2705	81	15
2706	81	18
2707	82	16
2708	82	23
2709	82	22
2710	82	19
2711	82	24
2712	82	36
2713	82	12
\.


--
-- Name: seen_statements_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('seen_statements_uid_seq', 2713, true);


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
1	Ein Radar überwacht den Abstand, eine Frontkamera erkennt Fahrspuren und andere Verkehrsteilnehmer, und je sechs Ultraschallsensoren vorne und hinten helfen beim Einparken und messen während der Fahrt Distanzen im Zentimeterbereich	localhost:3449	/devcards/index.html	5	68	4	2017-08-17 13:52:05.150878
2	Zunächst einmal unterscheidet sich die Hardware für den Autopiloten nicht oder nur marginal von dem, was selbst für einen VW Polo erhältlich ist	localhost:3449	/	5	68	4	2017-08-17 13:52:05.150878
3	Katzen sind kleine Tiger	http://www.iflscience.com/	plants-and-animals/no-your-cat-isnt-plotting-kill-youbut-it-has-lions-personality/	2	15	2	2017-08-17 13:52:05.150878
4	Katzen sind kleine Tiger	http://www.iflscience.com/	plants-and-animals/no-your-cat-isnt-plotting-kill-youbut-it-has-lions-personality/	2	16	2	2017-08-17 13:52:05.150878
\.


--
-- Name: statement_references_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('statement_references_uid_seq', 4, true);


--
-- Data for Name: statement_replacements_by_premisegroup_split; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY statement_replacements_by_premisegroup_split (uid, review_uid, old_statement_uid, new_statement_uid, "timestamp") FROM stdin;
\.


--
-- Name: statement_replacements_by_premisegroup_split_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('statement_replacements_by_premisegroup_split_uid_seq', 1, false);


--
-- Data for Name: statement_replacements_by_premisegroups_merge; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY statement_replacements_by_premisegroups_merge (uid, review_uid, old_statement_uid, new_statement_uid, "timestamp") FROM stdin;
\.


--
-- Name: statement_replacements_by_premisegroups_merge_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('statement_replacements_by_premisegroups_merge_uid_seq', 1, false);


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
1	2	we should get a cat	1	2017-08-13 13:52:05.923438	f
2	3	we should get a dog	1	2017-08-07 13:52:05.923562	f
3	4	we could get both, a cat and a dog	1	2017-08-12 13:52:05.923618	f
4	5	cats are very independent	1	2017-08-14 13:52:05.923664	f
5	6	cats are capricious	1	2017-07-30 13:52:05.923707	f
6	7	dogs can act as watch dogs	1	2017-08-03 13:52:05.923749	f
7	8	you have to take the dog for a walk every day, which is tedious	1	2017-08-16 13:52:05.923789	f
8	9	we have no use for a watch dog	1	2017-08-05 13:52:05.923829	f
9	10	going for a walk with the dog every day is good for social interaction and physical exercise	1	2017-08-08 13:52:05.923869	f
10	11	it would be no problem	1	2017-08-02 13:52:05.923908	f
11	12	a cat and a dog will generally not get along well	1	2017-08-17 13:52:05.923947	f
12	13	we do not have enough money for two pets	1	2017-08-09 13:52:05.923985	f
13	14	a dog costs taxes and will be more expensive than a cat	1	2017-07-24 13:52:05.924025	f
14	15	cats are fluffy	1	2017-08-15 13:52:05.924064	f
15	16	cats are small	1	2017-08-13 13:52:05.924111	f
16	17	fluffy animals losing much hair and I'm allergic to animal hair	1	2017-07-26 13:52:05.924151	f
17	18	you could use a automatic vacuum cleaner	1	2017-07-25 13:52:05.924191	f
18	19	cats ancestors are animals in wildlife, who are hunting alone and not in groups	1	2017-08-03 13:52:05.92423	f
19	20	this is not true for overbred races	1	2017-07-24 13:52:05.924269	f
20	21	this lies in their the natural conditions	1	2017-08-16 13:52:05.924309	f
21	22	the purpose of a pet is to have something to take care of	1	2017-08-12 13:52:05.924349	f
22	23	several cats of friends of mine are real as*holes	1	2017-07-27 13:52:05.924387	f
23	24	the fact, that cats are capricious, is based on the cats race	1	2017-07-30 13:52:05.924426	f
24	25	not every cat is capricious	1	2017-08-03 13:52:05.924465	f
25	26	this is based on the cats race and a little bit on the breeding	1	2017-07-30 13:52:05.924504	f
26	27	next to the taxes you will need equipment like a dog lead, anti-flea-spray, and so on	1	2017-07-23 13:52:05.924543	f
27	28	the equipment for running costs of cats and dogs are nearly the same	1	2017-07-29 13:52:05.924582	f
28	29	this is just a claim without any justification	1	2017-08-14 13:52:05.924621	f
29	30	in Germany you have to pay for your second dog even more taxes!	1	2017-07-28 13:52:05.924661	f
30	31	it is important, that pets are small and fluffy!	1	2017-08-07 13:52:05.9247	f
31	32	cats are little, sweet and innocent cuddle toys	1	2017-08-09 13:52:05.924739	f
32	33	do you have ever seen a sphinx cat or savannah cats?	1	2017-08-16 13:52:05.924778	f
33	34	it is much work to take care of both animals	1	2017-07-24 13:52:05.924817	f
34	35	won't be best friends	1	2017-08-07 13:52:05.924856	f
35	36	the city should reduce the number of street festivals	3	2017-08-12 13:52:05.924895	f
36	37	we should shut down University Park	3	2017-08-03 13:52:05.924934	f
37	38	we should close public swimming pools	1	2017-07-27 13:52:05.924973	f
38	39	reducing the number of street festivals can save up to $50.000 a year	1	2017-08-02 13:52:05.925011	f
39	40	every street festival is funded by large companies	1	2017-07-25 13:52:05.925049	f
40	41	then we will have more money to expand out pedestrian zone	1	2017-07-27 13:52:05.925088	f
41	42	our city will get more attractive for shopping	1	2017-08-08 13:52:05.925125	f
42	43	street festivals attract many people, which will increase the citys income	1	2017-08-03 13:52:05.925164	f
43	44	spending of the city for these festivals are higher than the earnings	1	2017-08-10 13:52:05.925202	f
44	45	money does not solve problems of our society	1	2017-08-16 13:52:05.92524	f
45	46	criminals use University Park to sell drugs	1	2017-07-24 13:52:05.925279	f
46	47	shutting down University Park will save $100.000 a year	1	2017-08-02 13:52:05.925317	f
47	48	we should not give in to criminals	1	2017-07-24 13:52:05.925356	f
48	49	the number of police patrols has been increased recently	1	2017-08-09 13:52:05.925394	f
49	50	this is the only park in our city	1	2017-08-15 13:52:05.925433	f
50	51	there are many parks in neighbouring towns	1	2017-08-16 13:52:05.925471	f
51	52	the city is planing a new park in the upcoming month	3	2017-08-10 13:52:05.925509	f
52	53	parks are very important for our climate	3	2017-07-30 13:52:05.925548	f
53	54	our swimming pools are very old and it would take a major investment to repair them	3	2017-07-25 13:52:05.925587	f
54	55	schools need the swimming pools for their sports lessons	1	2017-07-30 13:52:05.925626	f
55	56	the rate of non-swimmers is too high	1	2017-08-16 13:52:05.925664	f
56	57	the police cannot patrol in the park for 24/7	1	2017-07-28 13:52:05.925703	f
57	58	E-Autos "optimal" für den Stadtverkehr sind	1	2017-07-27 13:52:05.925742	f
58	59	dadurch die Lärmbelästigung in der Stadt sinkt	1	2017-08-12 13:52:05.925781	f
77	77	Straßenfeste viel Lärm verursachen	1	2017-08-08 13:52:05.926473	f
59	60	die Anzahl an Ladestationen in der Stadt nicht ausreichend ist	1	2017-08-07 13:52:05.92582	f
60	61	das Unfallrisiko steigt, da die Autos kaum Geräusche verursachen	1	2017-07-31 13:52:05.925893	f
61	62	die Autos auch zuhause geladen werden können und das pro Tag ausreichen sollte	1	2017-08-02 13:52:05.92593	f
62	63	Elektroautos keine lauten Geräusche beim Anfahren produzieren	1	2017-07-30 13:52:05.925965	f
63	64	Lärmbelästigung kein wirkliches Problem in den Städten ist	1	2017-07-30 13:52:05.925999	f
64	65	nicht jede normale Tankstelle auch Stromtankstellen hat	1	2017-07-23 13:52:05.926033	f
65	66	die Länder und Kommunen den Ausbau nun stark fördern wollen	1	2017-07-24 13:52:05.926068	f
66	67	E-Autos das autonome Fahren vorantreiben	5	2017-08-12 13:52:05.926102	f
67	68	Tesla mutig bestehende Techniken einsetzt und zeigt was sie können	5	2017-08-03 13:52:05.926136	f
68	69	durch rücksichtsvolle Verhaltensanpassungen der wissenschaftlichen Mitarbeitenden der Arbeitsaufwand der Sekretärinnen gesenkt werden könnte	1	2017-08-10 13:52:05.92617	f
69	70	wir Standard-Formulare, wie Urlaubsanträge, selbst faxen können	1	2017-08-13 13:52:05.926203	f
70	71	etliche Abläufe durch ein besseres Zusammenarbeiten optimiert werden können. Dies sollte auch schriftlich als Anleitungen festgehalten werden, damit neue Angestellt einen leichten Einstieg finden	1	2017-08-05 13:52:05.926237	f
71	72	viele Arbeiten auch durch die Mitarbeiter erledigt werden können	1	2017-08-04 13:52:05.92627	f
72	73	"rücksichtsvolle Verhaltensanpassungen" viel zu allgemein gehalten ist	1	2017-08-13 13:52:05.926304	f
73	74	das Faxgerät nicht immer zugänglich ist, wenn die Sekretärinnen nicht anwesend sind	1	2017-08-04 13:52:05.926337	f
74	75	wir keine eigenen Faxgeräte haben und so oder so entweder bei Martin stören müssten oder doch bei Sabine im Büro landen würden	1	2017-07-25 13:52:05.926371	f
75	1	Cats are fucking stupid and bloody fuzzy critters!	1	2017-08-12 13:52:05.926406	f
76	76	Die Anzahl der Straßenfeste sollte reduziert werden	1	2017-07-28 13:52:05.926439	f
78	78	Straßenfeste ein wichtiger Bestandteil unserer Kultur sind	1	2017-08-11 13:52:05.926506	f
79	79	Straßenfeste der Kommune Geld einbringen	1	2017-08-05 13:52:05.92654	f
80	80	die Einnahmen der Kommune durch Straßenfeste nur gering sind	1	2017-08-03 13:52:05.926573	f
81	81	Straßenfeste der Kommune hohe Kosten verursachen durch Polizeieinsätze, Säuberung, etc.	1	2017-07-23 13:52:05.926606	f
82	82	die Innenstadt ohnehin sehr laut ist	1	2017-08-13 13:52:05.92664	f
\.


--
-- Name: textversions_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('textversions_uid_seq', 82, true);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY users (uid, firstname, surname, nickname, public_nickname, email, gender, password, group_uid, last_action, last_login, registered, token, token_timestamp) FROM stdin;
1	anonymous	anonymous	anonymous	anonymous		m	$2a$10$SFsXaPkYUuJrXDVa4Wlx.u2UWyq9FJhO2Lf.buCcg9MayHWxchz2i	3	2017-08-17 13:52:05.743397	2017-08-17 13:52:05.743516	2017-08-17 13:52:05.743567		\N
2	Tobias	Krauthoff	Tobias	Tobias	krauthoff@cs.uni-duesseldorf.de	m	$2a$10$9P5biPvyX2xVeMcCLm82tO0XFQhmdMFwgAhPaUkCHoVL1F5kEAjIa	1	2017-08-17 13:52:05.743656	2017-08-17 13:52:05.743706	2017-08-17 13:52:05.743751		\N
3	Christian	Meter	Christian	Christian	meter@cs.uni-duesseldorf.de	m	$2a$10$Ou/pHV1MoZRqvt5U8cV09up0qqbIz70ZjwEeanRkyyfR/rrMHcBfe	1	2017-08-17 13:52:05.743831	2017-08-17 13:52:05.743878	2017-08-17 13:52:05.743923		\N
4	Björn	Ebbinghaus	Björn	Björn	bjoern.ebbinghaus@uni-duesseldorf.de	m	$2a$10$uHmicxwdEdR5dygTpyCXxetQiq2vGizNgUOuvBuGUr2RV9KZS.td2	1	2017-08-17 13:52:05.74886	2017-08-17 13:52:05.748953	2017-08-17 13:52:05.74902		\N
5	Teresa	Uebber	Teresa	Teresa	teresa.uebber@uni-duesseldorf.de	f	$2a$10$nBmo8URUPI4L5u69klSPjOt/vyneb9vSR95dIbYcxsM.8Uuo5QEEm	1	2017-08-17 13:52:05.749135	2017-08-17 13:52:05.749201	2017-08-17 13:52:05.749263		\N
6	Bob	Bubbles	Bob	Bob	tobias.krauthoff+dbas.usert31@gmail.com	n	$2a$10$6yF/8oSBagIDYUMpCXA3JOXHvEcYe4DvNkXJs8xGLsyPVUEUtdjiy	1	2017-08-17 13:52:05.749372	2017-08-17 13:52:05.749437	2017-08-17 13:52:05.749499		\N
7	Pascal	Lux	Pascal	Pascal	tobias.krauthoff+dbas.usert00@gmail.com	m	$2a$10$6yF/8oSBagIDYUMpCXA3JOXHvEcYe4DvNkXJs8xGLsyPVUEUtdjiy	3	2017-08-17 13:52:05.749684	2017-08-17 13:52:05.749743	2017-08-17 13:52:05.749795		\N
8	Kurt	Hecht	Kurt	Kurt	tobias.krauthoff+dbas.usert01@gmail.com	m	$2a$10$6yF/8oSBagIDYUMpCXA3JOXHvEcYe4DvNkXJs8xGLsyPVUEUtdjiy	3	2017-08-17 13:52:05.749906	2017-08-17 13:52:05.749962	2017-08-17 13:52:05.750013		\N
9	Torben	Hartl	Torben	Torben	tobias.krauthoff+dbas.usert02@gmail.com	m	$2a$10$6yF/8oSBagIDYUMpCXA3JOXHvEcYe4DvNkXJs8xGLsyPVUEUtdjiy	3	2017-08-17 13:52:05.750101	2017-08-17 13:52:05.750154	2017-08-17 13:52:05.750204		\N
10	Thorsten	Scherer	Thorsten	Thorsten	tobias.krauthoff+dbas.usert03@gmail.com	m	$2a$10$6yF/8oSBagIDYUMpCXA3JOXHvEcYe4DvNkXJs8xGLsyPVUEUtdjiy	3	2017-08-17 13:52:05.750291	2017-08-17 13:52:05.750343	2017-08-17 13:52:05.750395		\N
11	Friedrich	Schutte	Friedrich	Friedrich	tobias.krauthoff+dbas.usert04@gmail.com	m	$2a$10$6yF/8oSBagIDYUMpCXA3JOXHvEcYe4DvNkXJs8xGLsyPVUEUtdjiy	3	2017-08-17 13:52:05.750482	2017-08-17 13:52:05.750534	2017-08-17 13:52:05.750591		\N
12	Aayden	Westermann	Aayden	Aayden	tobias.krauthoff+dbas.usert05@gmail.com	m	$2a$10$6yF/8oSBagIDYUMpCXA3JOXHvEcYe4DvNkXJs8xGLsyPVUEUtdjiy	3	2017-08-17 13:52:05.75071	2017-08-17 13:52:05.750776	2017-08-17 13:52:05.750825		\N
13	Hermann	Grasshoff	Hermann	Hermann	tobias.krauthoff+dbas.usert06@gmail.com	m	$2a$10$6yF/8oSBagIDYUMpCXA3JOXHvEcYe4DvNkXJs8xGLsyPVUEUtdjiy	3	2017-08-17 13:52:05.750917	2017-08-17 13:52:05.750965	2017-08-17 13:52:05.751009		\N
14	Wolf	Himmler	Wolf	Wolf	tobias.krauthoff+dbas.usert07@gmail.com	m	$2a$10$6yF/8oSBagIDYUMpCXA3JOXHvEcYe4DvNkXJs8xGLsyPVUEUtdjiy	3	2017-08-17 13:52:05.751086	2017-08-17 13:52:05.751132	2017-08-17 13:52:05.751176		\N
15	Jakob	Winter	Jakob	Jakob	tobias.krauthoff+dbas.usert08@gmail.com	m	$2a$10$6yF/8oSBagIDYUMpCXA3JOXHvEcYe4DvNkXJs8xGLsyPVUEUtdjiy	3	2017-08-17 13:52:05.751253	2017-08-17 13:52:05.751299	2017-08-17 13:52:05.751344		\N
16	Alwin	Wechter	Alwin	Alwin	tobias.krauthoff+dbas.usert09@gmail.com	m	$2a$10$6yF/8oSBagIDYUMpCXA3JOXHvEcYe4DvNkXJs8xGLsyPVUEUtdjiy	3	2017-08-17 13:52:05.75142	2017-08-17 13:52:05.751466	2017-08-17 13:52:05.75151		\N
17	Walter	Weisser	Walter	Walter	tobias.krauthoff+dbas.usert10@gmail.com	m	$2a$10$6yF/8oSBagIDYUMpCXA3JOXHvEcYe4DvNkXJs8xGLsyPVUEUtdjiy	3	2017-08-17 13:52:05.751587	2017-08-17 13:52:05.751632	2017-08-17 13:52:05.751677		\N
18	Volker	Keitel	Volker	Volker	tobias.krauthoff+dbas.usert11@gmail.com	m	$2a$10$6yF/8oSBagIDYUMpCXA3JOXHvEcYe4DvNkXJs8xGLsyPVUEUtdjiy	3	2017-08-17 13:52:05.751753	2017-08-17 13:52:05.751799	2017-08-17 13:52:05.751844		\N
19	Benedikt	Feuerstein	Benedikt	Benedikt	tobias.krauthoff+dbas.usert12@gmail.com	m	$2a$10$6yF/8oSBagIDYUMpCXA3JOXHvEcYe4DvNkXJs8xGLsyPVUEUtdjiy	3	2017-08-17 13:52:05.75192	2017-08-17 13:52:05.751966	2017-08-17 13:52:05.752018		\N
20	Engelbert	Gottlieb	Engelbert	Engelbert	tobias.krauthoff+dbas.usert13@gmail.com	m	$2a$10$6yF/8oSBagIDYUMpCXA3JOXHvEcYe4DvNkXJs8xGLsyPVUEUtdjiy	3	2017-08-17 13:52:05.752104	2017-08-17 13:52:05.752153	2017-08-17 13:52:05.752198		\N
21	Elias	Auerbach	Elias	Elias	tobias.krauthoff+dbas.usert14@gmail.com	m	$2a$10$6yF/8oSBagIDYUMpCXA3JOXHvEcYe4DvNkXJs8xGLsyPVUEUtdjiy	3	2017-08-17 13:52:05.752314	2017-08-17 13:52:05.752364	2017-08-17 13:52:05.75241		\N
22	Rupert	Wenz	Rupert	Rupert	tobias.krauthoff+dbas.usert15@gmail.com	m	$2a$10$6yF/8oSBagIDYUMpCXA3JOXHvEcYe4DvNkXJs8xGLsyPVUEUtdjiy	3	2017-08-17 13:52:05.752489	2017-08-17 13:52:05.752538	2017-08-17 13:52:05.752583		\N
23	Marga	Wegscheider	Marga	Marga	tobias.krauthoff+dbas.usert16@gmail.com	f	$2a$10$6yF/8oSBagIDYUMpCXA3JOXHvEcYe4DvNkXJs8xGLsyPVUEUtdjiy	3	2017-08-17 13:52:05.752661	2017-08-17 13:52:05.752708	2017-08-17 13:52:05.752753		\N
24	Larissa	Clauberg	Larissa	Larissa	tobias.krauthoff+dbas.usert17@gmail.com	f	$2a$10$6yF/8oSBagIDYUMpCXA3JOXHvEcYe4DvNkXJs8xGLsyPVUEUtdjiy	3	2017-08-17 13:52:05.752831	2017-08-17 13:52:05.752878	2017-08-17 13:52:05.752922		\N
25	Emmi	Rosch	Emmi	Emmi	tobias.krauthoff+dbas.usert18@gmail.com	f	$2a$10$6yF/8oSBagIDYUMpCXA3JOXHvEcYe4DvNkXJs8xGLsyPVUEUtdjiy	3	2017-08-17 13:52:05.752999	2017-08-17 13:52:05.753045	2017-08-17 13:52:05.753089		\N
26	Konstanze	Krebs	Konstanze	Konstanze	tobias.krauthoff+dbas.usert19@gmail.com	f	$2a$10$6yF/8oSBagIDYUMpCXA3JOXHvEcYe4DvNkXJs8xGLsyPVUEUtdjiy	3	2017-08-17 13:52:05.753165	2017-08-17 13:52:05.753214	2017-08-17 13:52:05.753259		\N
27	Catrin	Fahnrich	Catrin	Catrin	tobias.krauthoff+dbas.usert20@gmail.com	f	$2a$10$6yF/8oSBagIDYUMpCXA3JOXHvEcYe4DvNkXJs8xGLsyPVUEUtdjiy	3	2017-08-17 13:52:05.753337	2017-08-17 13:52:05.753384	2017-08-17 13:52:05.753428		\N
28	Antonia	Bartram	Antonia	Antonia	tobias.krauthoff+dbas.usert21@gmail.com	f	$2a$10$6yF/8oSBagIDYUMpCXA3JOXHvEcYe4DvNkXJs8xGLsyPVUEUtdjiy	3	2017-08-17 13:52:05.753504	2017-08-17 13:52:05.75355	2017-08-17 13:52:05.753601		\N
29	Nora	Kempf	Nora	Nora	tobias.krauthoff+dbas.usert22@gmail.com	f	$2a$10$6yF/8oSBagIDYUMpCXA3JOXHvEcYe4DvNkXJs8xGLsyPVUEUtdjiy	3	2017-08-17 13:52:05.753678	2017-08-17 13:52:05.753725	2017-08-17 13:52:05.753769		\N
30	Julia	Wetter	Julia	Julia	tobias.krauthoff+dbas.usert23@gmail.com	f	$2a$10$6yF/8oSBagIDYUMpCXA3JOXHvEcYe4DvNkXJs8xGLsyPVUEUtdjiy	3	2017-08-17 13:52:05.753862	2017-08-17 13:52:05.753932	2017-08-17 13:52:05.753982		\N
31	Jutta	Munch	Jutta	Jutta	tobias.krauthoff+dbas.usert24@gmail.com	f	$2a$10$6yF/8oSBagIDYUMpCXA3JOXHvEcYe4DvNkXJs8xGLsyPVUEUtdjiy	3	2017-08-17 13:52:05.754066	2017-08-17 13:52:05.754116	2017-08-17 13:52:05.754163		\N
32	Helga	Heilmann	Helga	Helga	tobias.krauthoff+dbas.usert25@gmail.com	f	$2a$10$6yF/8oSBagIDYUMpCXA3JOXHvEcYe4DvNkXJs8xGLsyPVUEUtdjiy	3	2017-08-17 13:52:05.754244	2017-08-17 13:52:05.754293	2017-08-17 13:52:05.75434		\N
33	Denise	Tietjen	Denise	Denise	tobias.krauthoff+dbas.usert26@gmail.com	f	$2a$10$6yF/8oSBagIDYUMpCXA3JOXHvEcYe4DvNkXJs8xGLsyPVUEUtdjiy	3	2017-08-17 13:52:05.754424	2017-08-17 13:52:05.754474	2017-08-17 13:52:05.754522		\N
34	Hanne	Beckmann	Hanne	Hanne	tobias.krauthoff+dbas.usert27@gmail.com	f	$2a$10$6yF/8oSBagIDYUMpCXA3JOXHvEcYe4DvNkXJs8xGLsyPVUEUtdjiy	3	2017-08-17 13:52:05.754605	2017-08-17 13:52:05.754655	2017-08-17 13:52:05.754702		\N
35	Elly	Landauer	Elly	Elly	tobias.krauthoff+dbas.usert28@gmail.com	f	$2a$10$6yF/8oSBagIDYUMpCXA3JOXHvEcYe4DvNkXJs8xGLsyPVUEUtdjiy	3	2017-08-17 13:52:05.754785	2017-08-17 13:52:05.754835	2017-08-17 13:52:05.754882		\N
36	Sybille	Redlich	Sybille	Sybille	tobias.krauthoff+dbas.usert29@gmail.com	f	$2a$10$6yF/8oSBagIDYUMpCXA3JOXHvEcYe4DvNkXJs8xGLsyPVUEUtdjiy	3	2017-08-17 13:52:05.754967	2017-08-17 13:52:05.755014	2017-08-17 13:52:05.755058		\N
37	Ingeburg	Fischer	Ingeburg	Ingeburg	tobias.krauthoff+dbas.usert30@gmail.com	f	$2a$10$6yF/8oSBagIDYUMpCXA3JOXHvEcYe4DvNkXJs8xGLsyPVUEUtdjiy	3	2017-08-17 13:52:05.755136	2017-08-17 13:52:05.755183	2017-08-17 13:52:05.755232		\N
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
-- Name: statement_replacements_by_premisegroup_split statement_replacements_by_premisegroup_split_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY statement_replacements_by_premisegroup_split
    ADD CONSTRAINT statement_replacements_by_premisegroup_split_pkey PRIMARY KEY (uid);


--
-- Name: statement_replacements_by_premisegroups_merge statement_replacements_by_premisegroups_merge_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY statement_replacements_by_premisegroups_merge
    ADD CONSTRAINT statement_replacements_by_premisegroups_merge_pkey PRIMARY KEY (uid);


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
-- Name: statement_replacements_by_premisegroup_split statement_replacements_by_premisegroup_s_new_statement_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY statement_replacements_by_premisegroup_split
    ADD CONSTRAINT statement_replacements_by_premisegroup_s_new_statement_uid_fkey FOREIGN KEY (new_statement_uid) REFERENCES statements(uid);


--
-- Name: statement_replacements_by_premisegroup_split statement_replacements_by_premisegroup_s_old_statement_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY statement_replacements_by_premisegroup_split
    ADD CONSTRAINT statement_replacements_by_premisegroup_s_old_statement_uid_fkey FOREIGN KEY (old_statement_uid) REFERENCES statements(uid);


--
-- Name: statement_replacements_by_premisegroup_split statement_replacements_by_premisegroup_split_review_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY statement_replacements_by_premisegroup_split
    ADD CONSTRAINT statement_replacements_by_premisegroup_split_review_uid_fkey FOREIGN KEY (review_uid) REFERENCES review_split(uid);


--
-- Name: statement_replacements_by_premisegroups_merge statement_replacements_by_premisegroups__new_statement_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY statement_replacements_by_premisegroups_merge
    ADD CONSTRAINT statement_replacements_by_premisegroups__new_statement_uid_fkey FOREIGN KEY (new_statement_uid) REFERENCES statements(uid);


--
-- Name: statement_replacements_by_premisegroups_merge statement_replacements_by_premisegroups__old_statement_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY statement_replacements_by_premisegroups_merge
    ADD CONSTRAINT statement_replacements_by_premisegroups__old_statement_uid_fkey FOREIGN KEY (old_statement_uid) REFERENCES statements(uid);


--
-- Name: statement_replacements_by_premisegroups_merge statement_replacements_by_premisegroups_merge_review_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY statement_replacements_by_premisegroups_merge
    ADD CONSTRAINT statement_replacements_by_premisegroups_merge_review_uid_fkey FOREIGN KEY (review_uid) REFERENCES review_split(uid);


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
-- Name: statement_replacements_by_premisegroup_split; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE statement_replacements_by_premisegroup_split TO read_only_discussion;


--
-- Name: statement_replacements_by_premisegroups_merge; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE statement_replacements_by_premisegroups_merge TO read_only_discussion;


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

