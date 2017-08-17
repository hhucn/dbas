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
1	1	2	\N	f	1	2017-08-17 13:44:19.697804	2	t
2	2	2	\N	t	1	2017-08-17 13:44:19.697982	2	f
3	3	2	\N	f	1	2017-08-17 13:44:19.698091	2	f
4	4	3	\N	t	1	2017-08-17 13:44:19.698194	2	f
5	5	3	\N	f	1	2017-08-17 13:44:19.698295	2	f
8	8	4	\N	t	1	2017-08-17 13:44:19.698592	2	f
10	10	11	\N	f	1	2017-08-17 13:44:19.698798	2	f
11	11	2	\N	t	1	2017-08-17 13:44:19.698897	2	f
12	12	2	\N	t	1	2017-08-17 13:44:19.698996	2	f
15	15	5	\N	t	1	2017-08-17 13:44:19.699291	2	f
16	16	5	\N	f	1	2017-08-17 13:44:19.699393	2	f
17	17	5	\N	t	1	2017-08-17 13:44:19.699492	2	f
19	19	6	\N	t	1	2017-08-17 13:44:19.699695	2	f
20	20	6	\N	f	1	2017-08-17 13:44:19.699793	2	f
21	21	6	\N	f	1	2017-08-17 13:44:19.699891	2	f
23	23	14	\N	f	1	2017-08-17 13:44:19.700158	2	f
24	24	14	\N	t	1	2017-08-17 13:44:19.700256	2	f
26	26	14	\N	t	1	2017-08-17 13:44:19.700459	2	f
27	27	15	\N	t	1	2017-08-17 13:44:19.70056	2	f
28	27	16	\N	t	1	2017-08-17 13:44:19.700659	2	f
29	28	15	\N	t	1	2017-08-17 13:44:19.700759	2	f
30	29	15	\N	f	1	2017-08-17 13:44:19.700857	2	f
32	31	36	\N	t	3	2017-08-17 13:44:19.701055	1	f
34	33	39	\N	t	3	2017-08-17 13:44:19.701247	1	f
35	34	41	\N	t	1	2017-08-17 13:44:19.701345	1	f
36	35	36	\N	f	1	2017-08-17 13:44:19.701443	1	f
39	38	37	\N	t	1	2017-08-17 13:44:19.701824	1	f
40	39	37	\N	t	1	2017-08-17 13:44:19.701939	1	f
41	41	46	\N	f	1	2017-08-17 13:44:19.702039	1	f
42	42	37	\N	f	1	2017-08-17 13:44:19.702235	1	f
44	44	50	\N	f	1	2017-08-17 13:44:19.70245	1	f
46	45	50	\N	t	1	2017-08-17 13:44:19.702549	1	f
47	46	38	\N	t	1	2017-08-17 13:44:19.702647	1	f
49	48	38	\N	f	1	2017-08-17 13:44:19.702844	1	f
50	49	49	\N	f	1	2017-08-17 13:44:19.702944	1	f
51	51	58	\N	f	1	2017-08-17 13:44:19.703144	4	f
54	54	59	\N	t	1	2017-08-17 13:44:19.703441	4	f
55	55	59	\N	f	1	2017-08-17 13:44:19.703539	4	f
56	56	60	\N	t	1	2017-08-17 13:44:19.703637	4	f
57	57	60	\N	f	1	2017-08-17 13:44:19.703739	4	f
58	50	58	\N	t	1	2017-08-17 13:44:19.703046	4	f
59	61	67	\N	t	1	2017-08-17 13:44:19.703843	4	f
60	62	69	\N	t	1	2017-08-17 13:44:19.703942	5	f
61	63	69	\N	t	1	2017-08-17 13:44:19.70404	5	f
62	64	69	\N	f	1	2017-08-17 13:44:19.704145	5	f
63	65	70	\N	f	1	2017-08-17 13:44:19.704246	5	f
64	66	70	\N	f	1	2017-08-17 13:44:19.704344	5	f
65	67	76	\N	t	1	2017-08-17 13:44:19.704442	7	f
66	68	76	\N	f	1	2017-08-17 13:44:19.704542	7	f
67	69	76	\N	f	1	2017-08-17 13:44:19.70464	7	f
68	70	79	\N	f	1	2017-08-17 13:44:19.704738	7	f
6	6	\N	4	f	1	2017-08-17 13:44:19.698394	2	f
7	7	\N	5	f	1	2017-08-17 13:44:19.698492	2	f
9	9	\N	8	f	1	2017-08-17 13:44:19.698697	2	f
13	13	\N	12	f	1	2017-08-17 13:44:19.699093	2	f
14	14	\N	13	f	1	2017-08-17 13:44:19.699191	2	f
18	18	\N	2	f	1	2017-08-17 13:44:19.699596	2	f
22	22	\N	3	f	1	2017-08-17 13:44:19.700057	2	f
25	25	\N	11	f	1	2017-08-17 13:44:19.700353	2	f
31	30	\N	15	f	1	2017-08-17 13:44:19.700957	2	f
33	32	\N	32	f	3	2017-08-17 13:44:19.70115	1	f
37	36	\N	36	f	1	2017-08-17 13:44:19.70154	1	f
38	37	\N	36	f	1	2017-08-17 13:44:19.701676	1	f
43	43	\N	42	f	1	2017-08-17 13:44:19.702349	1	f
45	40	\N	39	f	1	2017-08-17 13:44:19.702136	1	f
48	47	\N	47	f	1	2017-08-17 13:44:19.702744	1	f
52	52	\N	58	f	1	2017-08-17 13:44:19.703244	4	f
53	53	\N	51	f	1	2017-08-17 13:44:19.703342	4	f
69	71	\N	65	f	1	2017-08-17 13:44:19.704835	7	f
\.


--
-- Name: arguments_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('arguments_uid_seq', 69, true);


--
-- Data for Name: clicked_arguments; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY clicked_arguments (uid, argument_uid, author_uid, "timestamp", is_up_vote, is_valid) FROM stdin;
882	1	27	2017-08-07 13:44:27.872647	t	t
883	1	21	2017-08-11 13:44:27.87276	t	t
884	1	28	2017-08-03 13:44:27.872809	t	t
885	2	36	2017-08-01 13:44:27.872847	t	t
886	3	24	2017-08-17 13:44:27.872882	t	t
887	3	27	2017-08-04 13:44:27.872917	t	t
888	3	21	2017-08-10 13:44:27.872951	t	t
889	3	16	2017-07-25 13:44:27.872983	t	t
890	3	20	2017-08-11 13:44:27.873014	f	t
891	4	11	2017-08-08 13:44:27.873045	t	t
892	4	29	2017-08-09 13:44:27.873076	t	t
893	4	31	2017-07-24 13:44:27.873107	t	t
894	4	14	2017-07-29 13:44:27.873138	t	t
895	4	15	2017-08-14 13:44:27.873168	f	t
896	4	29	2017-07-23 13:44:27.8732	f	t
897	5	18	2017-07-28 13:44:27.873231	t	t
898	5	9	2017-08-05 13:44:27.873261	t	t
899	5	36	2017-07-28 13:44:27.873291	t	t
900	5	10	2017-07-30 13:44:27.873321	f	t
901	5	19	2017-08-07 13:44:27.873351	f	t
902	5	28	2017-07-30 13:44:27.873381	f	t
903	5	12	2017-08-07 13:44:27.873411	f	t
904	5	17	2017-07-25 13:44:27.873441	f	t
905	5	8	2017-07-28 13:44:27.873471	f	t
906	5	9	2017-08-02 13:44:27.873501	f	t
907	5	26	2017-08-08 13:44:27.87353	f	t
908	5	23	2017-07-31 13:44:27.87356	f	t
909	5	15	2017-08-01 13:44:27.873589	f	t
910	8	32	2017-08-15 13:44:27.873619	t	t
911	8	21	2017-07-31 13:44:27.87365	t	t
912	8	18	2017-08-12 13:44:27.87368	t	t
913	8	15	2017-07-27 13:44:27.87371	t	t
914	8	33	2017-08-02 13:44:27.873739	t	t
915	8	29	2017-08-04 13:44:27.873769	t	t
916	8	23	2017-08-13 13:44:27.873799	t	t
917	8	35	2017-08-09 13:44:27.87383	t	t
918	8	25	2017-08-04 13:44:27.873868	t	t
919	10	23	2017-08-06 13:44:27.873899	t	t
920	10	37	2017-08-12 13:44:27.873929	t	t
921	10	33	2017-08-01 13:44:27.873959	t	t
922	10	32	2017-08-04 13:44:27.873989	t	t
923	10	10	2017-08-03 13:44:27.874018	t	t
924	10	34	2017-08-17 13:44:27.874047	t	t
925	10	22	2017-07-23 13:44:27.874076	f	t
926	10	25	2017-08-10 13:44:27.874105	f	t
927	11	9	2017-08-04 13:44:27.874134	t	t
928	11	26	2017-08-06 13:44:27.874163	t	t
929	11	7	2017-07-31 13:44:27.874193	t	t
930	11	37	2017-08-17 13:44:27.874222	t	t
931	11	8	2017-07-26 13:44:27.874252	t	t
932	11	19	2017-08-15 13:44:27.874281	t	t
933	11	16	2017-07-31 13:44:27.874311	t	t
934	11	29	2017-07-28 13:44:27.874341	t	t
935	11	36	2017-08-15 13:44:27.874371	t	t
936	11	20	2017-07-28 13:44:27.874402	t	t
937	11	28	2017-07-27 13:44:27.874432	t	t
938	11	12	2017-08-05 13:44:27.874461	t	t
939	11	11	2017-08-17 13:44:27.87449	t	t
940	11	13	2017-08-09 13:44:27.87452	t	t
941	11	15	2017-08-14 13:44:27.874549	t	t
942	11	21	2017-08-10 13:44:27.874579	t	t
943	11	23	2017-07-26 13:44:27.874609	t	t
944	11	26	2017-07-26 13:44:27.874638	f	t
945	11	18	2017-08-02 13:44:27.874667	f	t
946	11	34	2017-08-09 13:44:27.874696	f	t
947	12	18	2017-07-23 13:44:27.874725	t	t
948	12	14	2017-08-13 13:44:27.874754	t	t
949	12	24	2017-07-27 13:44:27.874784	t	t
950	12	13	2017-08-16 13:44:27.874813	t	t
951	12	10	2017-08-12 13:44:27.874843	t	t
952	12	27	2017-08-05 13:44:27.874873	t	t
953	12	31	2017-08-05 13:44:27.874904	t	t
954	12	12	2017-08-02 13:44:27.874933	t	t
955	12	25	2017-08-04 13:44:27.874962	t	t
956	12	23	2017-07-25 13:44:27.874991	t	t
957	12	20	2017-08-13 13:44:27.87502	t	t
958	12	9	2017-08-14 13:44:27.875049	t	t
959	12	19	2017-08-11 13:44:27.875079	t	t
960	12	35	2017-08-13 13:44:27.875108	t	t
961	12	32	2017-07-29 13:44:27.875138	t	t
962	12	34	2017-08-07 13:44:27.875167	t	t
963	12	29	2017-07-27 13:44:27.875197	t	t
964	12	24	2017-08-10 13:44:27.875226	f	t
965	12	36	2017-08-07 13:44:27.875255	f	t
966	12	20	2017-07-26 13:44:27.875284	f	t
967	12	37	2017-07-25 13:44:27.875313	f	t
968	12	21	2017-08-07 13:44:27.875342	f	t
969	12	22	2017-07-26 13:44:27.875372	f	t
970	12	14	2017-08-17 13:44:27.875401	f	t
971	12	26	2017-08-10 13:44:27.875432	f	t
972	12	13	2017-08-13 13:44:27.875461	f	t
973	12	29	2017-08-16 13:44:27.87549	f	t
974	12	11	2017-08-04 13:44:27.875519	f	t
975	12	10	2017-08-09 13:44:27.875549	f	t
976	12	7	2017-08-15 13:44:27.875577	f	t
977	12	16	2017-08-02 13:44:27.875607	f	t
978	12	29	2017-07-29 13:44:27.875636	f	t
979	15	29	2017-08-01 13:44:27.875666	t	t
980	15	10	2017-08-01 13:44:27.875695	t	t
981	15	23	2017-08-11 13:44:27.875724	t	t
982	15	14	2017-07-26 13:44:27.875753	f	t
983	15	21	2017-07-24 13:44:27.875782	f	t
984	15	37	2017-07-30 13:44:27.875811	f	t
985	16	10	2017-08-08 13:44:27.87584	f	t
986	16	12	2017-08-02 13:44:27.875869	f	t
987	16	34	2017-08-11 13:44:27.875899	f	t
988	16	7	2017-08-16 13:44:27.875928	f	t
989	17	29	2017-07-23 13:44:27.875957	t	t
990	17	13	2017-07-23 13:44:27.875987	t	t
991	17	14	2017-08-15 13:44:27.876017	t	t
992	17	26	2017-07-24 13:44:27.876046	t	t
993	17	10	2017-07-25 13:44:27.876075	f	t
994	17	33	2017-08-09 13:44:27.876104	f	t
995	17	31	2017-07-24 13:44:27.876133	f	t
996	17	28	2017-08-07 13:44:27.876163	f	t
997	17	27	2017-07-26 13:44:27.876192	f	t
998	19	12	2017-08-09 13:44:27.876221	t	t
999	19	12	2017-08-09 13:44:27.87625	f	t
1000	19	26	2017-07-24 13:44:27.876279	f	t
1001	19	32	2017-08-11 13:44:27.876308	f	t
1002	20	33	2017-08-16 13:44:27.876337	t	t
1003	20	11	2017-07-31 13:44:27.876366	t	t
1004	20	8	2017-07-27 13:44:27.876395	t	t
1005	20	10	2017-08-09 13:44:27.876424	t	t
1006	20	9	2017-07-24 13:44:27.876453	t	t
1007	20	35	2017-07-29 13:44:27.876482	t	t
1008	20	29	2017-08-05 13:44:27.876511	t	t
1009	20	12	2017-07-30 13:44:27.87654	t	t
1010	20	17	2017-08-03 13:44:27.876569	t	t
1011	20	29	2017-08-06 13:44:27.876598	t	t
1012	20	36	2017-08-15 13:44:27.876627	t	t
1013	20	21	2017-07-30 13:44:27.876656	t	t
1014	20	14	2017-07-30 13:44:27.876685	t	t
1015	20	18	2017-08-12 13:44:27.876714	t	t
1016	20	26	2017-08-04 13:44:27.876754	t	t
1017	20	32	2017-08-15 13:44:27.876784	t	t
1018	20	15	2017-07-31 13:44:27.876814	t	t
1019	20	31	2017-08-08 13:44:27.876844	t	t
1020	20	22	2017-07-31 13:44:27.876874	t	t
1021	20	8	2017-07-24 13:44:27.876904	f	t
1022	20	37	2017-08-08 13:44:27.876934	f	t
1023	20	29	2017-08-11 13:44:27.876964	f	t
1024	20	14	2017-07-29 13:44:27.877014	f	t
1025	20	12	2017-08-03 13:44:27.877044	f	t
1026	20	7	2017-07-29 13:44:27.877073	f	t
1027	20	28	2017-07-23 13:44:27.877104	f	t
1028	20	34	2017-08-01 13:44:27.877143	f	t
1029	20	16	2017-07-31 13:44:27.877172	f	t
1030	20	20	2017-08-11 13:44:27.877201	f	t
1031	20	27	2017-08-06 13:44:27.87723	f	t
1032	20	17	2017-08-09 13:44:27.877259	f	t
1033	20	15	2017-08-07 13:44:27.877288	f	t
1034	20	22	2017-08-09 13:44:27.877317	f	t
1035	20	25	2017-08-02 13:44:27.877346	f	t
1036	20	32	2017-08-02 13:44:27.877375	f	t
1037	20	11	2017-08-13 13:44:27.877405	f	t
1038	20	21	2017-08-07 13:44:27.877434	f	t
1039	20	36	2017-08-17 13:44:27.877463	f	t
1040	20	18	2017-08-11 13:44:27.877493	f	t
1041	20	33	2017-07-23 13:44:27.877522	f	t
1042	20	19	2017-08-07 13:44:27.877553	f	t
1043	20	29	2017-08-17 13:44:27.877582	f	t
1044	20	10	2017-07-24 13:44:27.877612	f	t
1045	20	13	2017-08-16 13:44:27.877641	f	t
1046	20	35	2017-07-25 13:44:27.87767	f	t
1047	21	19	2017-08-17 13:44:27.877699	f	t
1048	21	37	2017-07-26 13:44:27.877729	f	t
1049	21	15	2017-08-03 13:44:27.877758	f	t
1050	21	16	2017-07-27 13:44:27.877787	f	t
1051	23	27	2017-07-23 13:44:27.877817	t	t
1052	23	16	2017-07-26 13:44:27.87785	t	t
1053	23	26	2017-08-15 13:44:27.877882	t	t
1054	23	20	2017-07-28 13:44:27.877912	t	t
1055	23	8	2017-08-04 13:44:27.877942	f	t
1056	23	16	2017-07-28 13:44:27.877971	f	t
1057	23	36	2017-08-07 13:44:27.878001	f	t
1058	23	31	2017-08-09 13:44:27.87803	f	t
1059	23	29	2017-08-07 13:44:27.87806	f	t
1060	23	27	2017-07-25 13:44:27.878089	f	t
1061	23	20	2017-08-10 13:44:27.878119	f	t
1062	23	17	2017-08-03 13:44:27.878148	f	t
1063	24	26	2017-08-03 13:44:27.878177	t	t
1064	24	36	2017-08-02 13:44:27.878206	t	t
1065	24	7	2017-08-02 13:44:27.878235	t	t
1066	24	14	2017-08-01 13:44:27.878264	t	t
1067	24	23	2017-08-06 13:44:27.878292	t	t
1068	24	24	2017-08-07 13:44:27.878322	t	t
1069	24	21	2017-07-28 13:44:27.878351	t	t
1070	24	13	2017-08-03 13:44:27.87838	t	t
1071	24	19	2017-08-14 13:44:27.878409	t	t
1072	27	29	2017-08-11 13:44:27.878439	t	t
1073	27	34	2017-08-15 13:44:27.878468	t	t
1074	27	10	2017-07-24 13:44:27.878498	t	t
1075	27	28	2017-08-03 13:44:27.878527	t	t
1076	27	31	2017-07-26 13:44:27.878555	t	t
1077	27	20	2017-07-31 13:44:27.878585	t	t
1078	27	13	2017-08-07 13:44:27.878614	t	t
1079	27	36	2017-08-14 13:44:27.878642	t	t
1080	27	21	2017-07-23 13:44:27.878672	t	t
1081	27	27	2017-07-24 13:44:27.878701	t	t
1082	27	23	2017-08-12 13:44:27.87873	t	t
1083	27	16	2017-08-07 13:44:27.878785	t	t
1084	27	11	2017-08-10 13:44:27.878815	t	t
1085	27	7	2017-08-04 13:44:27.878845	t	t
1086	27	19	2017-08-02 13:44:27.878873	t	t
1087	27	34	2017-08-08 13:44:27.878902	f	t
1088	27	11	2017-08-03 13:44:27.878931	f	t
1089	27	29	2017-07-31 13:44:27.878971	f	t
1090	27	37	2017-08-16 13:44:27.87901	f	t
1091	27	28	2017-08-15 13:44:27.87904	f	t
1092	27	33	2017-08-10 13:44:27.879069	f	t
1093	27	15	2017-08-16 13:44:27.879097	f	t
1094	27	8	2017-08-12 13:44:27.879127	f	t
1095	27	7	2017-08-08 13:44:27.879156	f	t
1096	27	12	2017-07-27 13:44:27.879185	f	t
1097	27	22	2017-08-10 13:44:27.879214	f	t
1098	27	35	2017-08-15 13:44:27.879243	f	t
1099	27	20	2017-07-25 13:44:27.879273	f	t
1100	27	23	2017-07-25 13:44:27.879302	f	t
1101	27	18	2017-07-23 13:44:27.879331	f	t
1102	27	24	2017-08-10 13:44:27.87936	f	t
1103	27	14	2017-07-23 13:44:27.879389	f	t
1104	27	31	2017-08-11 13:44:27.879418	f	t
1105	28	32	2017-08-05 13:44:27.879447	t	t
1106	28	27	2017-08-16 13:44:27.879475	t	t
1107	28	37	2017-07-25 13:44:27.879505	t	t
1108	28	34	2017-07-27 13:44:27.879535	t	t
1109	28	11	2017-08-14 13:44:27.879564	t	t
1110	28	15	2017-07-24 13:44:27.879594	t	t
1111	28	36	2017-07-30 13:44:27.879622	t	t
1112	28	22	2017-07-26 13:44:27.879651	t	t
1113	28	12	2017-07-30 13:44:27.879681	t	t
1114	28	25	2017-08-07 13:44:27.87971	t	t
1115	28	24	2017-07-27 13:44:27.879739	t	t
1116	28	10	2017-08-08 13:44:27.879778	f	t
1117	29	29	2017-08-08 13:44:27.879808	t	t
1118	29	36	2017-07-31 13:44:27.879848	t	t
1119	29	31	2017-08-16 13:44:27.879877	t	t
1120	29	20	2017-08-04 13:44:27.879907	t	t
1121	29	19	2017-07-26 13:44:27.879937	t	t
1122	29	11	2017-08-07 13:44:27.879966	t	t
1123	29	7	2017-07-29 13:44:27.879995	t	t
1124	29	13	2017-08-08 13:44:27.880024	t	t
1125	29	22	2017-08-07 13:44:27.880054	t	t
1126	29	16	2017-08-10 13:44:27.880084	t	t
1127	29	15	2017-07-29 13:44:27.880113	f	t
1128	29	31	2017-08-12 13:44:27.880143	f	t
1129	29	25	2017-08-09 13:44:27.880172	f	t
1130	29	35	2017-08-02 13:44:27.880202	f	t
1131	29	20	2017-08-17 13:44:27.880231	f	t
1132	29	21	2017-08-03 13:44:27.88028	f	t
1133	29	12	2017-08-16 13:44:27.880309	f	t
1134	29	29	2017-07-27 13:44:27.880351	f	t
1135	29	18	2017-08-17 13:44:27.880381	f	t
1136	29	22	2017-08-07 13:44:27.880432	f	t
1137	29	10	2017-08-12 13:44:27.880463	f	t
1138	30	36	2017-08-09 13:44:27.880493	t	t
1139	30	22	2017-08-12 13:44:27.880559	t	t
1140	30	16	2017-08-11 13:44:27.88059	t	t
1141	30	20	2017-07-23 13:44:27.88062	f	t
1142	30	24	2017-08-05 13:44:27.880672	f	t
1143	30	27	2017-08-07 13:44:27.880702	f	t
1144	30	9	2017-07-24 13:44:27.880731	f	t
1145	30	12	2017-08-09 13:44:27.880761	f	t
1146	30	16	2017-08-12 13:44:27.88079	f	t
1147	30	7	2017-07-27 13:44:27.88082	f	t
1148	30	19	2017-08-06 13:44:27.880861	f	t
1149	30	21	2017-07-24 13:44:27.880912	f	t
1150	30	28	2017-08-13 13:44:27.880952	f	t
1151	32	27	2017-08-14 13:44:27.880992	t	t
1152	32	29	2017-08-10 13:44:27.881032	t	t
1153	32	11	2017-07-25 13:44:27.881061	t	t
1154	32	18	2017-08-04 13:44:27.881091	t	t
1155	32	7	2017-07-25 13:44:27.881121	t	t
1156	32	10	2017-08-11 13:44:27.88115	f	t
1157	32	22	2017-08-15 13:44:27.88118	f	t
1158	32	13	2017-08-05 13:44:27.88122	f	t
1159	32	25	2017-07-27 13:44:27.881251	f	t
1160	32	16	2017-08-17 13:44:27.881282	f	t
1161	32	24	2017-08-10 13:44:27.881315	f	t
1162	32	34	2017-08-09 13:44:27.881356	f	t
1163	34	21	2017-07-24 13:44:27.881385	t	t
1164	34	12	2017-08-04 13:44:27.881416	t	t
1165	34	27	2017-08-04 13:44:27.881447	t	t
1166	34	17	2017-07-25 13:44:27.881479	t	t
1167	34	35	2017-08-13 13:44:27.881521	f	t
1168	34	27	2017-08-01 13:44:27.881572	f	t
1169	34	29	2017-07-27 13:44:27.881603	f	t
1170	34	24	2017-07-31 13:44:27.881634	f	t
1171	34	32	2017-07-28 13:44:27.881675	f	t
1172	35	9	2017-07-24 13:44:27.881723	t	t
1173	35	12	2017-07-27 13:44:27.881809	t	t
1174	35	26	2017-07-28 13:44:27.881859	t	t
1175	35	16	2017-08-05 13:44:27.881892	t	t
1176	35	22	2017-07-31 13:44:27.881923	t	t
1177	35	35	2017-08-07 13:44:27.881953	t	t
1178	35	23	2017-07-27 13:44:27.881983	t	t
1179	35	37	2017-07-30 13:44:27.882013	t	t
1180	35	36	2017-08-02 13:44:27.882043	t	t
1181	35	15	2017-08-10 13:44:27.882073	t	t
1182	35	11	2017-08-01 13:44:27.882103	t	t
1183	35	35	2017-07-23 13:44:27.882131	f	t
1184	35	7	2017-07-27 13:44:27.88216	f	t
1185	35	31	2017-08-07 13:44:27.88219	f	t
1186	35	34	2017-08-08 13:44:27.88222	f	t
1187	35	24	2017-08-03 13:44:27.88226	f	t
1188	35	29	2017-07-25 13:44:27.882309	f	t
1189	35	25	2017-07-26 13:44:27.88237	f	t
1190	35	11	2017-08-14 13:44:27.882417	f	t
1191	36	7	2017-07-29 13:44:27.882469	t	t
1192	36	14	2017-08-16 13:44:27.882524	t	t
1193	36	12	2017-07-25 13:44:27.882579	t	t
1194	36	29	2017-08-08 13:44:27.882632	t	t
1195	36	31	2017-07-25 13:44:27.882685	t	t
1196	36	24	2017-08-14 13:44:27.88277	t	t
1197	36	29	2017-07-30 13:44:27.882851	t	t
1198	36	23	2017-07-26 13:44:27.882912	t	t
1199	36	27	2017-08-06 13:44:27.882963	t	t
1200	36	21	2017-08-03 13:44:27.88302	t	t
1201	36	10	2017-08-08 13:44:27.883054	t	t
1202	36	15	2017-07-31 13:44:27.883085	f	t
1203	36	36	2017-08-08 13:44:27.883117	f	t
1204	36	34	2017-08-02 13:44:27.883147	f	t
1205	36	27	2017-08-01 13:44:27.883177	f	t
1206	36	10	2017-07-29 13:44:27.883207	f	t
1207	39	27	2017-07-29 13:44:27.883237	t	t
1208	39	28	2017-07-24 13:44:27.883267	t	t
1209	39	14	2017-08-08 13:44:27.883298	f	t
1210	40	18	2017-07-25 13:44:27.883329	t	t
1211	40	26	2017-08-12 13:44:27.883372	t	t
1212	40	24	2017-08-04 13:44:27.883405	t	t
1213	40	32	2017-08-10 13:44:27.883435	t	t
1214	40	22	2017-08-08 13:44:27.88347	t	t
1215	40	7	2017-07-27 13:44:27.883528	t	t
1216	40	14	2017-08-02 13:44:27.883576	t	t
1217	40	16	2017-08-01 13:44:27.883625	t	t
1218	40	29	2017-08-11 13:44:27.883671	t	t
1219	40	35	2017-08-13 13:44:27.883719	t	t
1220	40	28	2017-08-12 13:44:27.883766	t	t
1221	40	31	2017-07-23 13:44:27.883825	t	t
1222	40	12	2017-08-06 13:44:27.883896	t	t
1223	40	37	2017-07-26 13:44:27.88398	t	t
1224	40	21	2017-08-13 13:44:27.884033	t	t
1225	40	36	2017-08-10 13:44:27.884083	f	t
1226	40	29	2017-08-07 13:44:27.884138	f	t
1227	40	10	2017-08-13 13:44:27.884192	f	t
1228	40	14	2017-08-05 13:44:27.884242	f	t
1229	40	7	2017-08-17 13:44:27.884292	f	t
1230	40	32	2017-08-02 13:44:27.884372	f	t
1231	40	20	2017-08-15 13:44:27.884424	f	t
1232	40	12	2017-08-01 13:44:27.884484	f	t
1233	40	15	2017-08-15 13:44:27.884543	f	t
1234	40	31	2017-08-12 13:44:27.884598	f	t
1235	40	22	2017-08-16 13:44:27.884651	f	t
1236	40	27	2017-07-26 13:44:27.884706	f	t
1237	40	33	2017-08-08 13:44:27.884767	f	t
1238	40	17	2017-08-16 13:44:27.88483	f	t
1239	40	9	2017-08-10 13:44:27.884902	f	t
1240	40	29	2017-08-06 13:44:27.884961	f	t
1241	41	13	2017-08-12 13:44:27.885027	t	t
1242	41	9	2017-08-01 13:44:27.885088	t	t
1243	41	11	2017-08-11 13:44:27.885149	t	t
1244	41	22	2017-08-09 13:44:27.885206	t	t
1245	41	19	2017-08-12 13:44:27.885263	t	t
1246	41	12	2017-07-25 13:44:27.885323	t	t
1247	41	28	2017-08-17 13:44:27.885385	t	t
1248	41	26	2017-08-10 13:44:27.885446	t	t
1249	41	18	2017-08-12 13:44:27.88551	t	t
1250	41	37	2017-08-13 13:44:27.885571	t	t
1251	41	15	2017-08-03 13:44:27.885631	t	t
1252	41	10	2017-08-10 13:44:27.885685	t	t
1253	41	24	2017-08-11 13:44:27.885765	t	t
1254	41	23	2017-08-01 13:44:27.885827	t	t
1255	41	14	2017-08-11 13:44:27.885913	t	t
1256	41	32	2017-07-25 13:44:27.88595	f	t
1257	41	33	2017-08-08 13:44:27.885986	f	t
1258	41	19	2017-07-29 13:44:27.886018	f	t
1259	41	29	2017-07-27 13:44:27.88605	f	t
1260	41	10	2017-08-07 13:44:27.886081	f	t
1261	41	14	2017-07-30 13:44:27.886114	f	t
1262	41	17	2017-07-29 13:44:27.886146	f	t
1263	42	15	2017-08-15 13:44:27.886177	t	t
1264	42	14	2017-08-04 13:44:27.886211	t	t
1265	42	31	2017-08-11 13:44:27.886246	f	t
1266	42	10	2017-08-03 13:44:27.886279	f	t
1267	42	12	2017-08-04 13:44:27.88631	f	t
1268	42	11	2017-07-28 13:44:27.886342	f	t
1269	42	16	2017-08-17 13:44:27.886374	f	t
1270	44	31	2017-07-31 13:44:27.886408	t	t
1271	44	28	2017-08-06 13:44:27.886439	t	t
1272	44	29	2017-08-15 13:44:27.886485	f	t
1273	44	17	2017-07-30 13:44:27.886517	f	t
1274	44	14	2017-07-25 13:44:27.886547	f	t
1275	46	33	2017-07-31 13:44:27.886578	t	t
1276	46	35	2017-08-12 13:44:27.886609	t	t
1277	46	27	2017-07-24 13:44:27.88664	t	t
1278	46	36	2017-08-04 13:44:27.88667	t	t
1279	46	24	2017-08-16 13:44:27.8867	t	t
1280	46	13	2017-08-13 13:44:27.886763	f	t
1281	46	7	2017-08-02 13:44:27.886813	f	t
1282	46	18	2017-08-03 13:44:27.886842	f	t
1283	46	34	2017-08-14 13:44:27.886871	f	t
1284	46	19	2017-07-28 13:44:27.8869	f	t
1285	46	20	2017-08-03 13:44:27.886929	f	t
1286	46	17	2017-07-25 13:44:27.886958	f	t
1287	46	25	2017-08-01 13:44:27.886987	f	t
1288	46	14	2017-08-12 13:44:27.887016	f	t
1289	47	26	2017-08-03 13:44:27.887046	t	t
1290	47	31	2017-07-25 13:44:27.887076	f	t
1291	47	23	2017-07-31 13:44:27.887106	f	t
1292	47	19	2017-08-15 13:44:27.887136	f	t
1293	47	24	2017-08-08 13:44:27.887165	f	t
1294	47	22	2017-07-31 13:44:27.887195	f	t
1295	47	11	2017-08-06 13:44:27.887224	f	t
1296	47	25	2017-07-26 13:44:27.887253	f	t
1297	47	36	2017-07-31 13:44:27.887282	f	t
1298	47	9	2017-08-09 13:44:27.88731	f	t
1299	47	13	2017-08-15 13:44:27.887339	f	t
1300	47	16	2017-07-26 13:44:27.887369	f	t
1301	47	15	2017-08-13 13:44:27.887397	f	t
1302	49	16	2017-07-26 13:44:27.887426	t	t
1303	49	31	2017-08-14 13:44:27.887456	t	t
1304	49	21	2017-08-03 13:44:27.887485	t	t
1305	49	26	2017-08-11 13:44:27.887513	t	t
1306	49	13	2017-08-10 13:44:27.887542	t	t
1307	49	27	2017-07-23 13:44:27.887572	t	t
1308	49	36	2017-08-10 13:44:27.887601	t	t
1309	49	22	2017-08-07 13:44:27.887631	f	t
1310	49	31	2017-08-10 13:44:27.88766	f	t
1311	49	17	2017-07-24 13:44:27.887688	f	t
1312	49	12	2017-07-25 13:44:27.887717	f	t
1313	49	29	2017-08-14 13:44:27.887746	f	t
1314	49	19	2017-08-02 13:44:27.887775	f	t
1315	49	7	2017-08-02 13:44:27.887805	f	t
1316	50	32	2017-08-12 13:44:27.887834	t	t
1317	50	35	2017-07-30 13:44:27.887863	t	t
1318	50	25	2017-08-08 13:44:27.887892	t	t
1319	50	20	2017-08-06 13:44:27.88792	t	t
1320	50	19	2017-07-28 13:44:27.887948	t	t
1321	50	15	2017-08-10 13:44:27.887977	t	t
1322	50	9	2017-07-28 13:44:27.888006	f	t
1323	50	17	2017-08-06 13:44:27.888035	f	t
1324	50	15	2017-07-31 13:44:27.888064	f	t
1325	50	24	2017-08-12 13:44:27.888093	f	t
1326	50	29	2017-08-17 13:44:27.888121	f	t
1327	50	29	2017-08-08 13:44:27.888151	f	t
1328	51	26	2017-07-31 13:44:27.888179	f	t
1329	51	18	2017-07-27 13:44:27.888209	f	t
1330	51	19	2017-08-09 13:44:27.888238	f	t
1331	51	7	2017-08-09 13:44:27.888267	f	t
1332	51	23	2017-07-26 13:44:27.888296	f	t
1333	51	15	2017-08-16 13:44:27.888325	f	t
1334	51	31	2017-08-02 13:44:27.888354	f	t
1335	51	16	2017-08-05 13:44:27.888383	f	t
1336	51	24	2017-08-15 13:44:27.888412	f	t
1337	51	11	2017-08-12 13:44:27.888441	f	t
1338	51	36	2017-08-09 13:44:27.888471	f	t
1339	51	25	2017-08-09 13:44:27.8885	f	t
1340	51	35	2017-08-17 13:44:27.888528	f	t
1341	51	32	2017-08-12 13:44:27.888557	f	t
1342	55	14	2017-08-06 13:44:27.888586	t	t
1343	55	8	2017-08-06 13:44:27.888615	t	t
1344	55	9	2017-07-24 13:44:27.888645	t	t
1345	55	17	2017-08-16 13:44:27.888674	t	t
1346	55	13	2017-07-23 13:44:27.888703	t	t
1347	55	23	2017-07-29 13:44:27.888732	f	t
1348	55	17	2017-07-23 13:44:27.888761	f	t
1349	55	9	2017-08-02 13:44:27.88879	f	t
1350	56	20	2017-08-05 13:44:27.888819	t	t
1351	56	22	2017-08-05 13:44:27.888848	t	t
1352	56	18	2017-08-16 13:44:27.888876	t	t
1353	56	24	2017-08-02 13:44:27.888906	t	t
1354	56	7	2017-08-05 13:44:27.888946	t	t
1355	56	26	2017-08-15 13:44:27.888997	t	t
1356	56	34	2017-08-13 13:44:27.889036	t	t
1357	56	15	2017-07-30 13:44:27.889065	t	t
1358	56	8	2017-08-14 13:44:27.889094	t	t
1359	56	14	2017-08-05 13:44:27.889123	t	t
1360	56	29	2017-07-23 13:44:27.889152	t	t
1361	56	19	2017-07-23 13:44:27.889181	t	t
1362	56	37	2017-08-06 13:44:27.88921	t	t
1363	56	10	2017-08-14 13:44:27.889239	t	t
1364	56	28	2017-08-07 13:44:27.889268	t	t
1365	56	12	2017-08-11 13:44:27.889298	f	t
1366	56	10	2017-08-11 13:44:27.889328	f	t
1367	58	25	2017-08-08 13:44:27.889357	t	t
1368	59	25	2017-08-13 13:44:27.889385	t	t
1369	59	29	2017-07-27 13:44:27.889414	f	t
1370	59	35	2017-07-23 13:44:27.889443	f	t
1371	59	14	2017-08-13 13:44:27.889472	f	t
1372	59	8	2017-08-15 13:44:27.889531	f	t
1373	59	16	2017-07-25 13:44:27.889561	f	t
1374	59	32	2017-07-25 13:44:27.889591	f	t
1375	59	9	2017-07-24 13:44:27.88962	f	t
1376	59	27	2017-08-02 13:44:27.889649	f	t
1377	59	10	2017-07-30 13:44:27.889678	f	t
1378	59	24	2017-08-14 13:44:27.889708	f	t
1379	60	31	2017-08-16 13:44:27.889738	t	t
1380	60	12	2017-08-08 13:44:27.889768	t	t
1381	60	24	2017-08-09 13:44:27.889798	t	t
1382	60	16	2017-07-29 13:44:27.889828	t	t
1383	60	18	2017-08-09 13:44:27.889877	t	t
1384	61	20	2017-08-08 13:44:27.889917	t	t
1385	61	36	2017-07-26 13:44:27.889947	t	t
1386	61	15	2017-08-09 13:44:27.889977	t	t
1387	61	24	2017-08-17 13:44:27.890006	t	t
1388	61	29	2017-08-11 13:44:27.890036	t	t
1389	61	9	2017-08-12 13:44:27.890065	t	t
1390	61	32	2017-08-05 13:44:27.890095	t	t
1391	61	13	2017-07-26 13:44:27.890123	t	t
1392	61	31	2017-07-31 13:44:27.890152	t	t
1393	61	37	2017-08-02 13:44:27.890181	t	t
1394	61	28	2017-07-31 13:44:27.89021	t	t
1395	61	14	2017-08-01 13:44:27.890239	t	t
1396	61	29	2017-08-03 13:44:27.890268	t	t
1397	61	22	2017-08-07 13:44:27.890297	t	t
1398	61	18	2017-07-24 13:44:27.890326	t	t
1399	61	8	2017-07-26 13:44:27.890354	t	t
1400	61	27	2017-08-02 13:44:27.890383	t	t
1401	61	16	2017-08-16 13:44:27.890412	f	t
1402	61	7	2017-08-01 13:44:27.890441	f	t
1403	61	27	2017-08-04 13:44:27.890471	f	t
1404	61	25	2017-08-04 13:44:27.890499	f	t
1405	61	11	2017-08-12 13:44:27.890529	f	t
1406	61	19	2017-08-08 13:44:27.890558	f	t
1407	61	28	2017-08-04 13:44:27.890587	f	t
1408	61	20	2017-08-14 13:44:27.890616	f	t
1409	61	24	2017-07-23 13:44:27.890645	f	t
1410	61	33	2017-08-01 13:44:27.890674	f	t
1411	61	36	2017-07-28 13:44:27.890702	f	t
1412	61	32	2017-08-05 13:44:27.890731	f	t
1413	61	17	2017-08-12 13:44:27.890769	f	t
1414	61	15	2017-08-12 13:44:27.890799	f	t
1415	61	23	2017-07-23 13:44:27.890829	f	t
1416	61	22	2017-07-25 13:44:27.890859	f	t
1417	61	10	2017-07-30 13:44:27.890889	f	t
1418	61	35	2017-07-23 13:44:27.890919	f	t
1419	62	7	2017-07-28 13:44:27.890948	t	t
1420	62	17	2017-07-26 13:44:27.890979	f	t
1421	62	13	2017-08-01 13:44:27.891009	f	t
1422	63	27	2017-08-10 13:44:27.891039	t	t
1423	63	19	2017-07-24 13:44:27.891069	t	t
1424	63	35	2017-08-05 13:44:27.891098	t	t
1425	63	37	2017-07-26 13:44:27.891128	t	t
1426	63	10	2017-07-27 13:44:27.891158	t	t
1427	63	26	2017-07-24 13:44:27.891187	t	t
1428	63	16	2017-07-24 13:44:27.891217	t	t
1429	64	32	2017-08-10 13:44:27.891246	t	t
1430	64	12	2017-08-06 13:44:27.891276	t	t
1431	64	16	2017-08-06 13:44:27.891305	t	t
1432	64	20	2017-07-26 13:44:27.891335	t	t
1433	64	21	2017-07-31 13:44:27.891364	t	t
1434	64	26	2017-08-01 13:44:27.891393	t	t
1435	64	34	2017-08-09 13:44:27.891422	t	t
1436	64	24	2017-08-04 13:44:27.891452	t	t
1437	64	18	2017-08-16 13:44:27.891481	t	t
1438	64	17	2017-08-04 13:44:27.891511	f	t
1439	64	25	2017-08-15 13:44:27.891541	f	t
1440	64	18	2017-08-10 13:44:27.891571	f	t
1441	64	12	2017-08-02 13:44:27.891601	f	t
1442	64	29	2017-07-27 13:44:27.89163	f	t
1443	64	32	2017-08-01 13:44:27.89166	f	t
1444	64	27	2017-07-31 13:44:27.891689	f	t
1445	64	34	2017-08-12 13:44:27.891719	f	t
1446	64	31	2017-07-25 13:44:27.891749	f	t
1447	65	29	2017-08-13 13:44:27.891779	t	t
1448	65	7	2017-08-03 13:44:27.891809	t	t
1449	65	19	2017-08-09 13:44:27.891838	t	t
1450	65	34	2017-07-26 13:44:27.891868	t	t
1451	65	13	2017-08-13 13:44:27.891898	f	t
1452	65	17	2017-07-24 13:44:27.891927	f	t
1453	65	20	2017-08-03 13:44:27.891957	f	t
1454	65	9	2017-07-24 13:44:27.891987	f	t
1455	65	15	2017-07-31 13:44:27.892016	f	t
1456	65	14	2017-07-28 13:44:27.892047	f	t
1457	65	35	2017-08-15 13:44:27.892077	f	t
1458	66	31	2017-08-07 13:44:27.892107	t	t
1459	66	24	2017-07-28 13:44:27.892137	t	t
1460	66	25	2017-08-08 13:44:27.892167	t	t
1461	66	36	2017-08-11 13:44:27.892196	t	t
1462	66	15	2017-07-25 13:44:27.892226	t	t
1463	66	26	2017-08-13 13:44:27.892255	t	t
1464	66	17	2017-08-07 13:44:27.892285	t	t
1465	66	28	2017-07-25 13:44:27.892314	t	t
1466	66	12	2017-08-11 13:44:27.892344	f	t
1467	66	9	2017-08-05 13:44:27.892374	f	t
1468	66	33	2017-08-10 13:44:27.892403	f	t
1469	67	36	2017-07-30 13:44:27.892432	t	t
1470	67	31	2017-08-03 13:44:27.892462	t	t
1471	67	27	2017-08-13 13:44:27.892491	t	t
1472	67	32	2017-08-09 13:44:27.892521	t	t
1473	67	35	2017-07-31 13:44:27.892551	t	t
1474	67	9	2017-07-24 13:44:27.89258	t	t
1475	67	8	2017-08-17 13:44:27.89261	t	t
1476	67	24	2017-08-05 13:44:27.89264	t	t
1477	67	23	2017-08-02 13:44:27.892669	t	t
1478	67	28	2017-08-06 13:44:27.892699	t	t
1479	67	7	2017-07-25 13:44:27.892729	t	t
1480	67	11	2017-08-13 13:44:27.892759	t	t
1481	67	18	2017-08-16 13:44:27.892789	t	t
1482	67	13	2017-08-16 13:44:27.89282	t	t
1483	67	33	2017-08-13 13:44:27.89285	t	t
1484	67	12	2017-08-02 13:44:27.89288	t	t
1485	67	29	2017-07-24 13:44:27.892909	t	t
1486	67	15	2017-08-10 13:44:27.892939	t	t
1487	67	29	2017-08-15 13:44:27.89297	t	t
1488	67	34	2017-08-13 13:44:27.893	t	t
1489	67	35	2017-08-06 13:44:27.893052	f	t
1490	67	13	2017-08-13 13:44:27.893119	f	t
1491	67	26	2017-08-15 13:44:27.893205	f	t
1492	67	32	2017-08-15 13:44:27.893261	f	t
1493	67	12	2017-08-14 13:44:27.893294	f	t
1494	67	23	2017-08-13 13:44:27.893325	f	t
1495	67	10	2017-08-04 13:44:27.893356	f	t
1496	67	14	2017-08-16 13:44:27.893388	f	t
1497	67	34	2017-07-28 13:44:27.893418	f	t
1498	67	16	2017-07-26 13:44:27.893449	f	t
1499	67	37	2017-07-27 13:44:27.893479	f	t
1500	67	15	2017-08-07 13:44:27.893509	f	t
1501	67	18	2017-07-30 13:44:27.893539	f	t
1502	67	22	2017-07-29 13:44:27.893569	f	t
1503	67	11	2017-08-06 13:44:27.893599	f	t
1504	67	20	2017-08-02 13:44:27.893629	f	t
1505	67	33	2017-08-16 13:44:27.893659	f	t
1506	67	19	2017-08-09 13:44:27.893688	f	t
1507	67	24	2017-08-07 13:44:27.893718	f	t
1508	68	21	2017-08-07 13:44:27.893749	t	t
1509	68	23	2017-07-29 13:44:27.893778	f	t
1510	68	15	2017-08-11 13:44:27.893808	f	t
1511	6	29	2017-08-09 13:44:27.893838	t	t
1512	6	7	2017-07-27 13:44:27.893876	t	t
1513	6	35	2017-07-25 13:44:27.893907	t	t
1514	6	12	2017-07-23 13:44:27.893937	t	t
1515	6	15	2017-08-13 13:44:27.893967	t	t
1516	6	22	2017-07-24 13:44:27.893998	t	t
1517	6	8	2017-07-28 13:44:27.894028	f	t
1518	6	33	2017-07-31 13:44:27.894059	f	t
1519	6	13	2017-08-15 13:44:27.894088	f	t
1520	6	35	2017-08-15 13:44:27.894119	f	t
1521	6	15	2017-08-09 13:44:27.894149	f	t
1522	6	31	2017-08-13 13:44:27.894179	f	t
1523	6	18	2017-07-28 13:44:27.894208	f	t
1524	6	20	2017-08-14 13:44:27.894238	f	t
1525	6	22	2017-07-24 13:44:27.894268	f	t
1526	6	36	2017-07-26 13:44:27.89432	f	t
1527	7	31	2017-08-16 13:44:27.894363	t	t
1528	7	37	2017-07-23 13:44:27.894415	t	t
1529	7	27	2017-08-13 13:44:27.894445	f	t
1530	7	32	2017-08-05 13:44:27.894476	f	t
1531	7	35	2017-08-03 13:44:27.894516	f	t
1532	7	12	2017-08-01 13:44:27.894577	f	t
1533	7	15	2017-08-11 13:44:27.894607	f	t
1534	9	18	2017-08-17 13:44:27.894637	t	t
1535	9	32	2017-07-27 13:44:27.894667	t	t
1536	9	8	2017-07-31 13:44:27.894697	t	t
1537	9	35	2017-07-24 13:44:27.894726	t	t
1538	9	14	2017-08-13 13:44:27.894756	t	t
1539	9	36	2017-08-10 13:44:27.894786	t	t
1540	9	34	2017-08-08 13:44:27.894816	t	t
1541	9	9	2017-07-25 13:44:27.894846	t	t
1542	9	16	2017-08-09 13:44:27.894876	t	t
1543	9	22	2017-07-26 13:44:27.894905	t	t
1544	9	15	2017-08-08 13:44:27.894936	t	t
1545	9	29	2017-08-01 13:44:27.894966	t	t
1546	9	13	2017-07-27 13:44:27.894995	t	t
1547	9	11	2017-07-28 13:44:27.895025	t	t
1548	9	15	2017-08-12 13:44:27.895054	f	t
1549	9	25	2017-08-10 13:44:27.895084	f	t
1550	9	18	2017-07-28 13:44:27.895114	f	t
1551	9	34	2017-07-29 13:44:27.895144	f	t
1552	9	32	2017-08-14 13:44:27.895173	f	t
1553	9	23	2017-07-25 13:44:27.895205	f	t
1554	13	27	2017-08-15 13:44:27.895234	f	t
1555	13	14	2017-07-29 13:44:27.895265	f	t
1556	13	34	2017-08-14 13:44:27.895294	f	t
1557	13	33	2017-08-02 13:44:27.895324	f	t
1558	13	25	2017-08-08 13:44:27.895353	f	t
1559	13	35	2017-07-30 13:44:27.895383	f	t
1560	13	29	2017-08-02 13:44:27.895413	f	t
1561	13	20	2017-07-29 13:44:27.895443	f	t
1562	13	10	2017-08-14 13:44:27.895473	f	t
1563	13	36	2017-07-29 13:44:27.895503	f	t
1564	14	31	2017-07-31 13:44:27.895532	f	t
1565	14	22	2017-07-30 13:44:27.895562	f	t
1566	14	8	2017-08-07 13:44:27.895591	f	t
1567	14	34	2017-07-31 13:44:27.895621	f	t
1568	14	26	2017-07-27 13:44:27.895651	f	t
1569	14	25	2017-07-29 13:44:27.895682	f	t
1570	14	18	2017-08-03 13:44:27.895712	f	t
1571	14	37	2017-08-05 13:44:27.895742	f	t
1572	14	35	2017-07-26 13:44:27.895772	f	t
1573	18	8	2017-07-29 13:44:27.895801	t	t
1574	18	24	2017-07-27 13:44:27.895831	t	t
1575	18	22	2017-08-16 13:44:27.89586	t	t
1576	18	7	2017-08-06 13:44:27.89589	t	t
1577	18	25	2017-07-26 13:44:27.89592	t	t
1578	18	13	2017-08-03 13:44:27.895949	t	t
1579	18	15	2017-08-06 13:44:27.895978	t	t
1580	18	35	2017-07-29 13:44:27.896008	t	t
1581	18	37	2017-07-26 13:44:27.896037	t	t
1582	18	12	2017-08-04 13:44:27.896067	t	t
1583	18	11	2017-07-29 13:44:27.896096	t	t
1584	18	26	2017-07-27 13:44:27.896126	t	t
1585	18	23	2017-08-06 13:44:27.896156	t	t
1586	18	29	2017-08-15 13:44:27.896186	t	t
1587	18	18	2017-08-10 13:44:27.896216	t	t
1588	18	36	2017-07-24 13:44:27.896246	t	t
1589	18	14	2017-08-15 13:44:27.896276	t	t
1590	18	20	2017-08-05 13:44:27.896305	t	t
1591	18	32	2017-08-10 13:44:27.896336	t	t
1592	18	31	2017-08-01 13:44:27.896376	t	t
1593	18	28	2017-08-09 13:44:27.896408	t	t
1594	18	9	2017-07-23 13:44:27.896438	t	t
1595	18	19	2017-08-06 13:44:27.896469	t	t
1596	18	21	2017-08-02 13:44:27.896498	t	t
1597	18	25	2017-07-24 13:44:27.896529	f	t
1598	18	11	2017-08-10 13:44:27.896558	f	t
1599	18	15	2017-07-31 13:44:27.896588	f	t
1600	18	16	2017-08-09 13:44:27.896617	f	t
1601	18	20	2017-08-02 13:44:27.896647	f	t
1602	18	17	2017-07-25 13:44:27.896676	f	t
1603	18	29	2017-07-28 13:44:27.896706	f	t
1604	18	7	2017-08-09 13:44:27.896735	f	t
1605	18	35	2017-07-31 13:44:27.896786	f	t
1606	22	7	2017-07-25 13:44:27.896817	f	t
1607	22	21	2017-07-27 13:44:27.896847	f	t
1608	22	35	2017-08-11 13:44:27.896878	f	t
1609	22	22	2017-07-30 13:44:27.896908	f	t
1610	22	29	2017-07-31 13:44:27.896938	f	t
1611	22	19	2017-07-27 13:44:27.896967	f	t
1612	22	24	2017-08-01 13:44:27.896996	f	t
1613	22	18	2017-08-10 13:44:27.897026	f	t
1614	22	9	2017-08-15 13:44:27.897056	f	t
1615	22	36	2017-07-27 13:44:27.897086	f	t
1616	22	12	2017-08-03 13:44:27.897116	f	t
1617	22	29	2017-08-02 13:44:27.897146	f	t
1618	22	33	2017-07-31 13:44:27.897176	f	t
1619	22	27	2017-07-25 13:44:27.897206	f	t
1620	22	37	2017-07-23 13:44:27.897236	f	t
1621	22	15	2017-08-11 13:44:27.897266	f	t
1622	22	28	2017-08-02 13:44:27.897296	f	t
1623	22	10	2017-07-31 13:44:27.897326	f	t
1624	22	8	2017-08-13 13:44:27.897356	f	t
1625	22	20	2017-08-13 13:44:27.897387	f	t
1626	22	13	2017-07-30 13:44:27.897417	f	t
1627	22	23	2017-08-09 13:44:27.897448	f	t
1628	22	11	2017-08-06 13:44:27.897478	f	t
1629	22	25	2017-08-05 13:44:27.897508	f	t
1630	22	31	2017-07-30 13:44:27.897538	f	t
1631	22	32	2017-08-06 13:44:27.897567	f	t
1632	22	26	2017-08-10 13:44:27.897598	f	t
1633	25	28	2017-08-13 13:44:27.897628	t	t
1634	25	20	2017-08-15 13:44:27.897659	t	t
1635	25	33	2017-07-29 13:44:27.89769	t	t
1636	25	9	2017-08-02 13:44:27.897721	t	t
1637	25	20	2017-07-30 13:44:27.897751	f	t
1638	25	18	2017-07-24 13:44:27.897782	f	t
1639	25	22	2017-08-12 13:44:27.897811	f	t
1640	31	25	2017-08-01 13:44:27.897842	t	t
1641	31	21	2017-08-02 13:44:27.897879	f	t
1642	33	12	2017-08-01 13:44:27.897909	t	t
1643	33	29	2017-07-30 13:44:27.897939	t	t
1644	33	24	2017-08-07 13:44:27.897969	t	t
1645	33	26	2017-07-28 13:44:27.897999	f	t
1646	33	25	2017-08-10 13:44:27.898029	f	t
1647	33	36	2017-07-30 13:44:27.898058	f	t
1648	33	37	2017-08-15 13:44:27.898089	f	t
1649	33	20	2017-07-29 13:44:27.898118	f	t
1650	33	19	2017-08-04 13:44:27.898148	f	t
1651	33	27	2017-08-02 13:44:27.898177	f	t
1652	33	29	2017-07-28 13:44:27.898207	f	t
1653	33	28	2017-08-08 13:44:27.898237	f	t
1654	37	37	2017-07-26 13:44:27.898267	t	t
1655	37	29	2017-08-08 13:44:27.898296	t	t
1656	37	29	2017-08-07 13:44:27.898326	t	t
1657	37	36	2017-07-23 13:44:27.898355	t	t
1658	37	8	2017-08-15 13:44:27.898384	t	t
1659	37	7	2017-07-23 13:44:27.898414	t	t
1660	37	13	2017-08-09 13:44:27.898443	t	t
1661	37	20	2017-07-30 13:44:27.898484	f	t
1662	37	29	2017-07-23 13:44:27.898514	f	t
1663	37	14	2017-08-08 13:44:27.898565	f	t
1664	37	25	2017-07-24 13:44:27.898596	f	t
1665	37	35	2017-08-05 13:44:27.898627	f	t
1666	37	18	2017-08-15 13:44:27.898667	f	t
1667	37	12	2017-07-24 13:44:27.898698	f	t
1668	37	37	2017-07-26 13:44:27.898727	f	t
1669	38	23	2017-08-07 13:44:27.898757	t	t
1670	38	33	2017-08-15 13:44:27.898786	t	t
1671	38	20	2017-07-24 13:44:27.898816	f	t
1672	38	22	2017-08-02 13:44:27.898845	f	t
1673	38	14	2017-08-06 13:44:27.898875	f	t
1674	43	32	2017-08-04 13:44:27.898904	t	t
1675	43	9	2017-08-04 13:44:27.898934	t	t
1676	43	29	2017-08-07 13:44:27.898975	t	t
1677	43	18	2017-08-09 13:44:27.899015	f	t
1678	43	25	2017-08-16 13:44:27.899046	f	t
1679	43	11	2017-08-09 13:44:27.899076	f	t
1680	45	33	2017-08-08 13:44:27.899106	t	t
1681	45	12	2017-07-30 13:44:27.899137	t	t
1682	45	28	2017-08-14 13:44:27.899167	t	t
1683	45	37	2017-08-08 13:44:27.899197	t	t
1684	45	13	2017-08-11 13:44:27.899227	t	t
1685	45	9	2017-08-04 13:44:27.899257	t	t
1686	45	29	2017-07-25 13:44:27.899286	t	t
1687	45	7	2017-07-25 13:44:27.899316	t	t
1688	45	31	2017-08-05 13:44:27.899346	t	t
1689	45	36	2017-08-08 13:44:27.899376	f	t
1690	45	15	2017-08-01 13:44:27.899405	f	t
1691	45	31	2017-08-12 13:44:27.899435	f	t
1692	45	29	2017-08-08 13:44:27.899465	f	t
1693	45	37	2017-08-04 13:44:27.899495	f	t
1694	45	13	2017-08-11 13:44:27.899525	f	t
1695	45	20	2017-08-02 13:44:27.899554	f	t
1696	45	17	2017-08-01 13:44:27.899584	f	t
1697	45	16	2017-07-26 13:44:27.899614	f	t
1698	45	25	2017-08-10 13:44:27.899643	f	t
1699	45	18	2017-08-14 13:44:27.899672	f	t
1700	45	32	2017-07-23 13:44:27.899703	f	t
1701	48	36	2017-08-17 13:44:27.899733	t	t
1702	48	9	2017-07-25 13:44:27.899763	t	t
1703	48	8	2017-08-05 13:44:27.899792	t	t
1704	48	22	2017-07-31 13:44:27.899821	t	t
1705	48	24	2017-07-25 13:44:27.89985	t	t
1706	48	10	2017-08-01 13:44:27.899879	t	t
1707	48	34	2017-08-10 13:44:27.899909	t	t
1708	48	29	2017-07-26 13:44:27.899939	t	t
1709	48	27	2017-08-02 13:44:27.899968	f	t
1710	48	28	2017-08-10 13:44:27.899998	f	t
1711	48	34	2017-08-12 13:44:27.900028	f	t
1712	48	23	2017-08-10 13:44:27.900059	f	t
1713	48	12	2017-07-26 13:44:27.900089	f	t
1714	48	32	2017-08-01 13:44:27.900118	f	t
1715	48	17	2017-07-31 13:44:27.900147	f	t
1716	48	19	2017-08-01 13:44:27.900177	f	t
1717	48	9	2017-08-04 13:44:27.900206	f	t
1718	52	23	2017-08-09 13:44:27.900236	t	t
1719	52	17	2017-07-26 13:44:27.900265	t	t
1720	52	31	2017-07-24 13:44:27.900295	t	t
1721	52	13	2017-08-01 13:44:27.900324	t	t
1722	52	12	2017-07-25 13:44:27.900354	t	t
1723	52	8	2017-08-16 13:44:27.900384	t	t
1724	52	24	2017-08-04 13:44:27.900421	t	t
1725	52	19	2017-08-12 13:44:27.900457	t	t
1726	52	37	2017-07-24 13:44:27.900488	t	t
1727	52	15	2017-08-01 13:44:27.900519	t	t
1728	52	37	2017-08-12 13:44:27.900549	f	t
1729	52	19	2017-08-01 13:44:27.900579	f	t
1730	52	18	2017-08-03 13:44:27.900609	f	t
1731	52	15	2017-08-02 13:44:27.900639	f	t
1732	52	11	2017-08-01 13:44:27.900669	f	t
1733	52	31	2017-08-05 13:44:27.900698	f	t
1734	52	17	2017-08-12 13:44:27.900728	f	t
1735	52	9	2017-08-16 13:44:27.900759	f	t
1736	52	27	2017-07-24 13:44:27.900789	f	t
1737	52	8	2017-07-28 13:44:27.90082	f	t
1738	53	25	2017-08-06 13:44:27.900858	t	t
1739	53	29	2017-08-16 13:44:27.900887	t	t
1740	53	11	2017-08-08 13:44:27.900916	t	t
1741	53	28	2017-08-04 13:44:27.900945	t	t
1742	53	24	2017-08-15 13:44:27.900975	t	t
1743	53	13	2017-07-23 13:44:27.901005	t	t
1744	53	19	2017-08-12 13:44:27.901034	t	t
1745	53	17	2017-08-12 13:44:27.901065	t	t
1746	53	23	2017-07-30 13:44:27.901094	f	t
1747	53	13	2017-07-26 13:44:27.901123	f	t
1748	53	15	2017-08-14 13:44:27.901151	f	t
1749	53	20	2017-07-30 13:44:27.90118	f	t
1750	53	37	2017-08-16 13:44:27.901209	f	t
1751	53	18	2017-08-02 13:44:27.901238	f	t
1752	53	11	2017-07-25 13:44:27.901267	f	t
1753	69	18	2017-08-01 13:44:27.901295	t	t
1754	69	34	2017-07-24 13:44:27.901324	t	t
1755	69	35	2017-07-27 13:44:27.901353	t	t
1756	69	11	2017-08-10 13:44:27.901382	t	t
1757	69	20	2017-07-25 13:44:27.901411	t	t
1758	69	37	2017-08-15 13:44:27.90145	t	t
1759	69	31	2017-08-16 13:44:27.90148	t	t
1760	69	21	2017-08-17 13:44:27.901519	t	t
1761	69	25	2017-08-11 13:44:27.901548	t	t
1762	69	14	2017-08-17 13:44:27.901578	t	t
1763	69	13	2017-07-25 13:44:27.901607	f	t
1764	69	7	2017-08-14 13:44:27.901635	f	t
\.


--
-- Name: clicked_arguments_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('clicked_arguments_uid_seq', 1764, true);


--
-- Data for Name: clicked_statements; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY clicked_statements (uid, statement_uid, author_uid, "timestamp", is_up_vote, is_valid) FROM stdin;
1236	1	10	2017-08-11 13:44:27.602946	t	t
1237	1	26	2017-08-06 13:44:27.603081	t	t
1238	1	21	2017-08-17 13:44:27.603142	t	t
1239	1	19	2017-07-31 13:44:27.603178	t	t
1240	1	8	2017-08-09 13:44:27.60321	t	t
1241	1	35	2017-07-25 13:44:27.603242	t	t
1242	1	26	2017-07-31 13:44:27.603274	t	t
1243	1	32	2017-07-27 13:44:27.603305	t	t
1244	1	28	2017-08-05 13:44:27.603336	t	t
1245	1	22	2017-08-07 13:44:27.603366	t	t
1246	1	13	2017-08-17 13:44:27.603396	t	t
1247	1	9	2017-08-03 13:44:27.603427	t	t
1248	1	12	2017-08-06 13:44:27.603467	t	t
1249	1	34	2017-07-26 13:44:27.603519	t	t
1250	1	29	2017-08-16 13:44:27.603575	t	t
1251	1	25	2017-07-29 13:44:27.603616	t	t
1252	1	10	2017-08-01 13:44:27.603646	t	t
1253	1	15	2017-08-13 13:44:27.603687	t	t
1254	1	17	2017-08-01 13:44:27.603748	t	t
1255	1	27	2017-07-23 13:44:27.603798	t	t
1256	1	36	2017-08-07 13:44:27.603828	t	t
1257	1	34	2017-08-11 13:44:27.603857	f	t
1258	2	31	2017-08-15 13:44:27.603886	t	t
1259	2	33	2017-07-25 13:44:27.603916	t	t
1260	2	29	2017-07-28 13:44:27.603946	t	t
1261	2	15	2017-07-28 13:44:27.603977	t	t
1262	2	35	2017-08-08 13:44:27.604006	t	t
1263	2	26	2017-07-23 13:44:27.604035	t	t
1264	2	20	2017-08-15 13:44:27.604065	f	t
1265	2	32	2017-08-03 13:44:27.604094	f	t
1266	2	13	2017-08-14 13:44:27.604123	f	t
1267	2	25	2017-08-02 13:44:27.604152	f	t
1268	2	9	2017-07-25 13:44:27.604182	f	t
1269	2	10	2017-08-02 13:44:27.604211	f	t
1270	2	12	2017-08-14 13:44:27.604241	f	t
1271	2	24	2017-08-13 13:44:27.604271	f	t
1272	2	27	2017-08-16 13:44:27.6043	f	t
1273	2	25	2017-08-17 13:44:27.604331	f	t
1274	2	31	2017-08-15 13:44:27.604361	f	t
1275	2	22	2017-07-29 13:44:27.604391	f	t
1276	4	10	2017-08-07 13:44:27.604421	t	t
1277	4	27	2017-08-16 13:44:27.604451	t	t
1278	5	35	2017-07-31 13:44:27.604481	f	t
1279	5	26	2017-08-15 13:44:27.604511	f	t
1280	5	8	2017-08-12 13:44:27.60454	f	t
1281	6	11	2017-08-11 13:44:27.60457	t	t
1282	6	11	2017-08-15 13:44:27.6046	t	t
1283	6	9	2017-08-17 13:44:27.60463	t	t
1284	6	34	2017-08-06 13:44:27.60466	t	t
1285	6	32	2017-08-13 13:44:27.604701	f	t
1286	7	28	2017-07-28 13:44:27.604761	t	t
1287	7	23	2017-07-23 13:44:27.604791	t	t
1288	7	21	2017-07-24 13:44:27.60482	t	t
1289	7	12	2017-08-03 13:44:27.60485	t	t
1290	7	36	2017-07-29 13:44:27.60488	t	t
1291	7	24	2017-08-14 13:44:27.60491	t	t
1292	7	14	2017-08-05 13:44:27.60494	t	t
1293	7	34	2017-08-15 13:44:27.604969	t	t
1294	7	8	2017-08-06 13:44:27.605	t	t
1295	7	16	2017-07-24 13:44:27.605029	t	t
1296	7	29	2017-07-31 13:44:27.605059	t	t
1297	7	25	2017-07-28 13:44:27.605089	f	t
1298	7	16	2017-08-17 13:44:27.605119	f	t
1299	7	32	2017-08-08 13:44:27.605149	f	t
1300	7	25	2017-08-04 13:44:27.605179	f	t
1301	7	12	2017-08-14 13:44:27.605209	f	t
1302	7	29	2017-07-29 13:44:27.605239	f	t
1303	7	13	2017-07-29 13:44:27.605268	f	t
1304	7	17	2017-08-07 13:44:27.605297	f	t
1305	7	31	2017-07-29 13:44:27.605327	f	t
1306	7	23	2017-08-08 13:44:27.605389	f	t
1307	7	26	2017-07-24 13:44:27.605421	f	t
1308	7	12	2017-07-26 13:44:27.605485	f	t
1309	8	24	2017-08-05 13:44:27.605538	t	t
1310	8	37	2017-08-06 13:44:27.605568	t	t
1311	8	37	2017-08-11 13:44:27.605599	t	t
1312	8	24	2017-07-27 13:44:27.605629	t	t
1313	8	27	2017-08-04 13:44:27.605659	t	t
1314	8	13	2017-07-30 13:44:27.605688	t	t
1315	8	16	2017-08-06 13:44:27.605717	t	t
1316	8	25	2017-07-31 13:44:27.605747	t	t
1317	8	16	2017-08-05 13:44:27.605779	t	t
1318	8	27	2017-08-06 13:44:27.605809	t	t
1319	8	24	2017-08-03 13:44:27.605838	t	t
1320	8	9	2017-08-15 13:44:27.605913	t	t
1321	8	18	2017-08-11 13:44:27.605952	t	t
1322	8	14	2017-08-13 13:44:27.605985	t	t
1323	8	8	2017-07-29 13:44:27.606028	t	t
1324	8	14	2017-08-13 13:44:27.606059	f	t
1325	8	29	2017-08-14 13:44:27.606089	f	t
1326	8	10	2017-08-12 13:44:27.606119	f	t
1327	8	22	2017-07-23 13:44:27.606149	f	t
1328	8	29	2017-08-11 13:44:27.606181	f	t
1329	8	13	2017-07-28 13:44:27.606211	f	t
1330	8	27	2017-08-06 13:44:27.60624	f	t
1331	8	20	2017-07-23 13:44:27.60627	f	t
1332	8	19	2017-07-28 13:44:27.6063	f	t
1333	8	16	2017-07-24 13:44:27.606331	f	t
1334	8	29	2017-07-29 13:44:27.60636	f	t
1335	8	19	2017-08-15 13:44:27.60639	f	t
1336	8	37	2017-08-06 13:44:27.606437	f	t
1337	8	16	2017-08-16 13:44:27.606483	f	t
1338	8	9	2017-07-23 13:44:27.606514	f	t
1339	8	13	2017-08-17 13:44:27.606544	f	t
1340	8	22	2017-08-13 13:44:27.606574	f	t
1341	8	14	2017-07-31 13:44:27.606604	f	t
1342	9	20	2017-08-16 13:44:27.606633	t	t
1343	9	7	2017-08-05 13:44:27.606663	t	t
1344	9	15	2017-08-09 13:44:27.606692	t	t
1345	9	28	2017-07-28 13:44:27.606722	t	t
1346	9	17	2017-08-02 13:44:27.606752	t	t
1347	9	13	2017-08-06 13:44:27.606781	t	t
1348	9	17	2017-07-26 13:44:27.606811	t	t
1349	9	17	2017-08-16 13:44:27.606841	t	t
1350	9	13	2017-08-09 13:44:27.606871	t	t
1351	9	27	2017-07-28 13:44:27.6069	t	t
1352	9	22	2017-07-29 13:44:27.60693	t	t
1353	9	8	2017-08-12 13:44:27.606959	f	t
1354	9	10	2017-07-30 13:44:27.606989	f	t
1355	9	34	2017-07-27 13:44:27.607018	f	t
1356	9	29	2017-08-13 13:44:27.607048	f	t
1357	10	25	2017-08-07 13:44:27.607078	t	t
1358	10	26	2017-08-12 13:44:27.607108	t	t
1359	10	34	2017-07-29 13:44:27.607137	t	t
1360	10	13	2017-08-10 13:44:27.607166	t	t
1361	10	25	2017-08-07 13:44:27.607196	t	t
1362	10	27	2017-08-08 13:44:27.607226	t	t
1363	10	13	2017-08-10 13:44:27.607255	t	t
1364	10	19	2017-08-08 13:44:27.607285	t	t
1365	10	27	2017-07-29 13:44:27.607315	t	t
1366	10	25	2017-08-01 13:44:27.607344	t	t
1367	10	26	2017-08-09 13:44:27.607373	t	t
1368	10	25	2017-07-29 13:44:27.607402	t	t
1369	10	31	2017-08-12 13:44:27.607432	t	t
1370	10	13	2017-07-25 13:44:27.607463	t	t
1371	10	13	2017-07-30 13:44:27.607492	t	t
1372	10	29	2017-07-29 13:44:27.607522	t	t
1373	10	35	2017-07-25 13:44:27.607552	t	t
1374	10	16	2017-08-08 13:44:27.607581	f	t
1375	10	29	2017-08-12 13:44:27.607611	f	t
1376	10	16	2017-07-26 13:44:27.60764	f	t
1377	10	29	2017-08-13 13:44:27.607669	f	t
1378	10	17	2017-08-05 13:44:27.607699	f	t
1379	10	7	2017-07-30 13:44:27.607728	f	t
1380	10	25	2017-08-14 13:44:27.607758	f	t
1381	10	14	2017-08-12 13:44:27.607788	f	t
1382	10	16	2017-08-11 13:44:27.607817	f	t
1383	10	13	2017-08-06 13:44:27.607846	f	t
1384	10	7	2017-08-07 13:44:27.607876	f	t
1385	10	25	2017-07-29 13:44:27.607906	f	t
1386	11	11	2017-07-30 13:44:27.607935	t	t
1387	11	8	2017-07-29 13:44:27.607965	t	t
1388	11	15	2017-07-28 13:44:27.607994	t	t
1389	11	26	2017-08-04 13:44:27.608023	t	t
1390	11	24	2017-08-03 13:44:27.608052	t	t
1391	11	15	2017-07-26 13:44:27.608082	t	t
1392	11	34	2017-07-24 13:44:27.608111	f	t
1393	11	18	2017-08-14 13:44:27.60814	f	t
1394	12	37	2017-08-16 13:44:27.608171	t	t
1395	12	20	2017-07-24 13:44:27.6082	t	t
1396	12	13	2017-08-05 13:44:27.608234	t	t
1397	12	33	2017-08-12 13:44:27.608265	t	t
1398	12	9	2017-08-08 13:44:27.608296	t	t
1399	12	16	2017-07-31 13:44:27.608325	t	t
1400	12	24	2017-08-15 13:44:27.608354	t	t
1401	12	7	2017-07-31 13:44:27.608384	t	t
1402	12	10	2017-08-15 13:44:27.608413	t	t
1403	12	14	2017-07-31 13:44:27.608452	t	t
1404	12	22	2017-08-05 13:44:27.608487	f	t
1405	12	26	2017-08-01 13:44:27.608518	f	t
1406	12	33	2017-07-28 13:44:27.608548	f	t
1407	12	34	2017-08-16 13:44:27.608578	f	t
1408	13	14	2017-07-27 13:44:27.608608	t	t
1409	13	20	2017-07-28 13:44:27.608638	f	t
1410	13	27	2017-08-09 13:44:27.608667	f	t
1411	13	20	2017-07-25 13:44:27.608696	f	t
1412	13	19	2017-08-08 13:44:27.608725	f	t
1413	13	15	2017-07-27 13:44:27.608755	f	t
1414	13	17	2017-08-13 13:44:27.608785	f	t
1415	13	8	2017-08-06 13:44:27.608815	f	t
1416	14	29	2017-08-09 13:44:27.608845	t	t
1417	14	11	2017-08-01 13:44:27.608885	f	t
1418	14	17	2017-08-02 13:44:27.608916	f	t
1419	14	7	2017-08-01 13:44:27.608956	f	t
1420	14	13	2017-08-15 13:44:27.608985	f	t
1421	14	31	2017-07-27 13:44:27.609014	f	t
1422	14	7	2017-08-06 13:44:27.609044	f	t
1423	14	13	2017-07-28 13:44:27.609073	f	t
1424	14	27	2017-08-12 13:44:27.609102	f	t
1425	14	8	2017-08-11 13:44:27.609132	f	t
1426	14	20	2017-07-30 13:44:27.609162	f	t
1427	14	15	2017-08-10 13:44:27.609191	f	t
1428	14	22	2017-08-04 13:44:27.60922	f	t
1429	14	28	2017-08-12 13:44:27.609249	f	t
1430	14	18	2017-08-03 13:44:27.609279	f	t
1431	15	29	2017-08-12 13:44:27.609309	t	t
1432	15	27	2017-08-15 13:44:27.609339	t	t
1433	15	24	2017-08-17 13:44:27.609368	t	t
1434	15	31	2017-07-27 13:44:27.609397	t	t
1435	15	33	2017-08-12 13:44:27.609427	t	t
1436	15	17	2017-08-04 13:44:27.609456	t	t
1437	15	16	2017-07-27 13:44:27.609485	f	t
1438	15	18	2017-08-12 13:44:27.609515	f	t
1439	15	12	2017-08-08 13:44:27.609544	f	t
1440	16	24	2017-07-31 13:44:27.609573	t	t
1441	16	28	2017-07-31 13:44:27.609604	t	t
1442	16	19	2017-08-14 13:44:27.609634	f	t
1443	16	10	2017-08-06 13:44:27.609664	f	t
1444	16	28	2017-08-12 13:44:27.609694	f	t
1445	16	23	2017-08-14 13:44:27.609724	f	t
1446	16	35	2017-07-31 13:44:27.609754	f	t
1447	16	22	2017-08-09 13:44:27.609783	f	t
1448	16	37	2017-08-06 13:44:27.609813	f	t
1449	16	17	2017-08-04 13:44:27.609843	f	t
1450	16	16	2017-08-06 13:44:27.609912	f	t
1451	16	32	2017-07-27 13:44:27.609943	f	t
1452	16	32	2017-07-25 13:44:27.609973	f	t
1453	16	15	2017-08-13 13:44:27.610003	f	t
1454	16	24	2017-07-28 13:44:27.610044	f	t
1455	16	27	2017-07-28 13:44:27.610084	f	t
1456	16	9	2017-07-23 13:44:27.610134	f	t
1457	17	32	2017-07-31 13:44:27.610163	t	t
1458	17	34	2017-08-10 13:44:27.610193	t	t
1459	17	20	2017-08-02 13:44:27.610235	t	t
1460	17	34	2017-08-03 13:44:27.6103	t	t
1461	17	26	2017-08-01 13:44:27.610329	t	t
1462	17	9	2017-08-11 13:44:27.61036	t	t
1463	17	19	2017-08-03 13:44:27.61039	f	t
1464	17	15	2017-08-02 13:44:27.61042	f	t
1465	17	8	2017-08-12 13:44:27.610449	f	t
1466	17	14	2017-08-04 13:44:27.61048	f	t
1467	17	19	2017-08-16 13:44:27.61051	f	t
1468	17	25	2017-08-07 13:44:27.610539	f	t
1469	17	19	2017-07-28 13:44:27.61057	f	t
1470	17	35	2017-08-03 13:44:27.610599	f	t
1471	17	29	2017-07-30 13:44:27.610628	f	t
1472	17	17	2017-07-24 13:44:27.610658	f	t
1473	17	19	2017-07-24 13:44:27.610688	f	t
1474	17	13	2017-07-25 13:44:27.610718	f	t
1475	17	33	2017-08-07 13:44:27.610748	f	t
1476	17	16	2017-08-06 13:44:27.610778	f	t
1477	17	32	2017-07-30 13:44:27.610808	f	t
1478	17	18	2017-07-23 13:44:27.610837	f	t
1479	18	37	2017-08-07 13:44:27.610867	t	t
1480	18	22	2017-08-04 13:44:27.610896	t	t
1481	18	18	2017-08-14 13:44:27.610926	t	t
1482	18	21	2017-07-24 13:44:27.610955	t	t
1483	18	10	2017-07-31 13:44:27.610985	t	t
1484	18	29	2017-08-04 13:44:27.611014	t	t
1485	18	14	2017-08-01 13:44:27.611065	t	t
1486	18	17	2017-08-17 13:44:27.611096	t	t
1487	18	29	2017-08-02 13:44:27.611126	t	t
1488	18	28	2017-08-03 13:44:27.611155	t	t
1489	18	33	2017-07-24 13:44:27.611185	t	t
1490	18	10	2017-08-17 13:44:27.611216	t	t
1491	18	36	2017-07-28 13:44:27.611246	f	t
1492	18	12	2017-08-13 13:44:27.611276	f	t
1493	18	12	2017-08-03 13:44:27.611305	f	t
1494	18	8	2017-08-02 13:44:27.611334	f	t
1495	18	16	2017-08-05 13:44:27.611364	f	t
1496	18	17	2017-07-25 13:44:27.611393	f	t
1497	18	31	2017-08-02 13:44:27.611422	f	t
1498	18	26	2017-07-25 13:44:27.611452	f	t
1499	18	9	2017-07-31 13:44:27.611481	f	t
1500	18	34	2017-07-26 13:44:27.61151	f	t
1501	18	28	2017-07-26 13:44:27.61154	f	t
1502	18	34	2017-07-26 13:44:27.61157	f	t
1503	18	17	2017-07-30 13:44:27.6116	f	t
1504	18	34	2017-08-15 13:44:27.611629	f	t
1505	18	15	2017-08-14 13:44:27.611659	f	t
1506	18	9	2017-07-28 13:44:27.611688	f	t
1507	18	19	2017-07-30 13:44:27.611717	f	t
1508	18	20	2017-07-28 13:44:27.611747	f	t
1509	18	29	2017-07-28 13:44:27.611776	f	t
1510	19	29	2017-08-11 13:44:27.611805	t	t
1511	19	33	2017-08-05 13:44:27.611836	t	t
1512	19	32	2017-07-29 13:44:27.611878	t	t
1513	19	29	2017-08-05 13:44:27.611918	t	t
1514	19	21	2017-08-04 13:44:27.611947	t	t
1515	19	14	2017-07-25 13:44:27.611976	t	t
1516	19	9	2017-07-31 13:44:27.612006	t	t
1517	19	25	2017-08-01 13:44:27.612036	t	t
1518	19	14	2017-08-10 13:44:27.612065	t	t
1519	19	31	2017-07-26 13:44:27.612094	t	t
1520	19	22	2017-08-14 13:44:27.612124	t	t
1521	19	14	2017-07-31 13:44:27.612153	t	t
1522	19	12	2017-07-29 13:44:27.612182	f	t
1523	20	8	2017-08-07 13:44:27.612212	f	t
1524	20	11	2017-07-26 13:44:27.612241	f	t
1525	20	16	2017-08-10 13:44:27.61227	f	t
1526	20	32	2017-08-03 13:44:27.612299	f	t
1527	20	18	2017-07-24 13:44:27.612329	f	t
1528	21	12	2017-08-01 13:44:27.612358	t	t
1529	21	21	2017-08-12 13:44:27.612387	f	t
1530	21	12	2017-08-14 13:44:27.612416	f	t
1531	21	29	2017-07-31 13:44:27.612446	f	t
1532	21	9	2017-08-13 13:44:27.612475	f	t
1533	22	33	2017-07-27 13:44:27.612505	t	t
1534	22	25	2017-08-07 13:44:27.612534	t	t
1535	22	24	2017-08-01 13:44:27.612563	t	t
1536	22	14	2017-08-08 13:44:27.612592	t	t
1537	22	19	2017-08-12 13:44:27.612622	f	t
1538	23	12	2017-08-13 13:44:27.612651	t	t
1539	23	14	2017-07-29 13:44:27.61268	f	t
1540	24	28	2017-08-12 13:44:27.612709	t	t
1541	24	33	2017-07-27 13:44:27.612739	t	t
1542	24	34	2017-08-09 13:44:27.612768	t	t
1543	24	33	2017-07-30 13:44:27.612797	t	t
1544	24	25	2017-08-10 13:44:27.612826	t	t
1545	24	29	2017-07-26 13:44:27.612855	t	t
1546	24	19	2017-08-05 13:44:27.612885	t	t
1547	24	35	2017-08-10 13:44:27.612927	t	t
1548	24	9	2017-08-13 13:44:27.612966	t	t
1549	24	32	2017-07-30 13:44:27.612996	t	t
1550	24	28	2017-08-07 13:44:27.613026	t	t
1551	24	29	2017-08-07 13:44:27.613055	t	t
1552	24	29	2017-08-02 13:44:27.613085	t	t
1553	24	26	2017-07-24 13:44:27.613114	t	t
1554	24	33	2017-08-10 13:44:27.613145	t	t
1555	24	22	2017-08-10 13:44:27.613174	t	t
1556	24	34	2017-08-06 13:44:27.613203	t	t
1557	24	26	2017-07-28 13:44:27.613232	t	t
1558	24	24	2017-08-03 13:44:27.613261	t	t
1559	24	27	2017-07-26 13:44:27.613291	t	t
1560	24	27	2017-08-12 13:44:27.61332	t	t
1561	24	27	2017-08-09 13:44:27.61335	f	t
1562	24	31	2017-08-13 13:44:27.61338	f	t
1563	24	7	2017-07-25 13:44:27.61341	f	t
1564	24	33	2017-08-13 13:44:27.613439	f	t
1565	24	10	2017-08-04 13:44:27.613468	f	t
1566	24	18	2017-08-13 13:44:27.613497	f	t
1567	24	29	2017-07-27 13:44:27.613527	f	t
1568	24	36	2017-08-15 13:44:27.613556	f	t
1569	24	24	2017-07-25 13:44:27.613585	f	t
1570	24	18	2017-07-24 13:44:27.613615	f	t
1571	24	28	2017-08-02 13:44:27.613645	f	t
1572	24	12	2017-08-10 13:44:27.613674	f	t
1573	24	11	2017-08-13 13:44:27.613704	f	t
1574	24	35	2017-07-27 13:44:27.613733	f	t
1575	25	26	2017-07-30 13:44:27.613762	f	t
1576	25	11	2017-07-30 13:44:27.613792	f	t
1577	26	12	2017-08-07 13:44:27.613821	t	t
1578	26	31	2017-07-27 13:44:27.613869	t	t
1579	26	24	2017-08-11 13:44:27.613921	t	t
1580	26	26	2017-07-29 13:44:27.613952	t	t
1581	26	31	2017-08-16 13:44:27.613981	t	t
1582	26	7	2017-08-13 13:44:27.614011	f	t
1583	27	17	2017-07-25 13:44:27.614041	t	t
1584	27	8	2017-08-12 13:44:27.614071	t	t
1585	27	7	2017-08-03 13:44:27.614101	t	t
1586	27	28	2017-07-30 13:44:27.614131	t	t
1587	27	13	2017-07-31 13:44:27.614161	t	t
1588	27	16	2017-08-15 13:44:27.61419	t	t
1589	27	10	2017-07-28 13:44:27.614219	t	t
1590	27	23	2017-08-03 13:44:27.614249	f	t
1591	27	34	2017-07-29 13:44:27.614278	f	t
1592	27	10	2017-08-15 13:44:27.614307	f	t
1593	27	29	2017-08-12 13:44:27.614337	f	t
1594	27	24	2017-08-07 13:44:27.614366	f	t
1595	27	11	2017-07-31 13:44:27.614395	f	t
1596	27	29	2017-07-25 13:44:27.614424	f	t
1597	27	25	2017-08-16 13:44:27.614453	f	t
1598	27	13	2017-08-03 13:44:27.614483	f	t
1599	27	20	2017-07-27 13:44:27.614512	f	t
1600	27	29	2017-08-07 13:44:27.614541	f	t
1601	27	14	2017-08-11 13:44:27.61457	f	t
1602	27	8	2017-07-24 13:44:27.614599	f	t
1603	27	8	2017-08-05 13:44:27.614628	f	t
1604	28	22	2017-08-12 13:44:27.614658	t	t
1605	28	12	2017-08-02 13:44:27.614687	t	t
1606	28	36	2017-07-23 13:44:27.614716	t	t
1607	28	21	2017-08-06 13:44:27.614745	t	t
1608	28	14	2017-08-11 13:44:27.614774	t	t
1609	28	12	2017-08-01 13:44:27.614802	t	t
1610	28	29	2017-08-17 13:44:27.614831	t	t
1611	28	20	2017-07-24 13:44:27.61486	t	t
1612	28	15	2017-07-31 13:44:27.61489	t	t
1613	28	11	2017-07-23 13:44:27.614919	t	t
1614	28	28	2017-08-15 13:44:27.614948	t	t
1615	28	8	2017-08-11 13:44:27.614977	t	t
1616	28	28	2017-07-30 13:44:27.615007	t	t
1617	28	27	2017-07-25 13:44:27.615036	f	t
1618	28	14	2017-08-11 13:44:27.615065	f	t
1619	28	13	2017-08-01 13:44:27.615107	f	t
1620	28	10	2017-08-16 13:44:27.615139	f	t
1621	28	37	2017-08-05 13:44:27.61522	f	t
1622	28	18	2017-08-05 13:44:27.615257	f	t
1623	28	29	2017-08-08 13:44:27.615288	f	t
1624	28	7	2017-08-13 13:44:27.615318	f	t
1625	28	33	2017-08-08 13:44:27.615348	f	t
1626	28	9	2017-08-12 13:44:27.615378	f	t
1627	29	15	2017-08-02 13:44:27.615408	t	t
1628	29	22	2017-07-25 13:44:27.61545	t	t
1629	29	37	2017-08-04 13:44:27.615501	t	t
1630	29	11	2017-07-25 13:44:27.615531	t	t
1631	29	29	2017-08-12 13:44:27.615571	f	t
1632	29	17	2017-08-15 13:44:27.615602	f	t
1633	29	29	2017-07-30 13:44:27.615643	f	t
1634	29	35	2017-08-06 13:44:27.615693	f	t
1635	29	7	2017-08-08 13:44:27.615733	f	t
1636	29	33	2017-07-28 13:44:27.615778	f	t
1637	29	13	2017-08-07 13:44:27.615825	f	t
1638	29	10	2017-08-07 13:44:27.615857	f	t
1639	29	15	2017-08-13 13:44:27.615888	f	t
1640	29	21	2017-07-29 13:44:27.615919	f	t
1641	29	17	2017-07-31 13:44:27.615949	f	t
1642	29	22	2017-07-28 13:44:27.61598	f	t
1643	29	16	2017-08-17 13:44:27.616013	f	t
1644	30	14	2017-07-28 13:44:27.616045	t	t
1645	30	31	2017-07-24 13:44:27.616076	t	t
1646	30	25	2017-08-15 13:44:27.616107	t	t
1647	30	29	2017-08-10 13:44:27.616137	t	t
1648	30	21	2017-08-13 13:44:27.616166	t	t
1649	30	37	2017-08-15 13:44:27.616196	t	t
1650	30	29	2017-08-08 13:44:27.616226	t	t
1651	30	8	2017-08-01 13:44:27.616256	t	t
1652	30	24	2017-08-08 13:44:27.616285	t	t
1653	30	34	2017-07-23 13:44:27.616315	t	t
1654	30	8	2017-08-16 13:44:27.616345	f	t
1655	30	28	2017-08-14 13:44:27.616377	f	t
1656	30	26	2017-07-28 13:44:27.616408	f	t
1657	30	31	2017-08-10 13:44:27.616441	f	t
1658	30	23	2017-07-23 13:44:27.616473	f	t
1659	30	29	2017-07-25 13:44:27.616503	f	t
1660	30	32	2017-08-10 13:44:27.616533	f	t
1661	30	9	2017-08-09 13:44:27.616565	f	t
1662	30	12	2017-08-08 13:44:27.616595	f	t
1663	30	19	2017-08-08 13:44:27.616625	f	t
1664	30	8	2017-08-16 13:44:27.616655	f	t
1665	30	15	2017-08-12 13:44:27.616685	f	t
1666	30	20	2017-07-25 13:44:27.616715	f	t
1667	30	24	2017-07-28 13:44:27.616745	f	t
1668	30	19	2017-07-28 13:44:27.616774	f	t
1669	30	22	2017-08-10 13:44:27.616804	f	t
1670	30	17	2017-08-05 13:44:27.616833	f	t
1671	30	8	2017-08-09 13:44:27.616863	f	t
1672	30	19	2017-08-13 13:44:27.616893	f	t
1673	30	29	2017-07-28 13:44:27.616923	f	t
1674	30	34	2017-07-31 13:44:27.616952	f	t
1675	31	24	2017-07-24 13:44:27.616981	t	t
1676	31	11	2017-08-12 13:44:27.617011	t	t
1677	31	20	2017-08-10 13:44:27.617041	t	t
1678	31	14	2017-07-27 13:44:27.61707	f	t
1679	31	35	2017-08-16 13:44:27.617111	f	t
1680	31	8	2017-08-06 13:44:27.617164	f	t
1681	31	26	2017-08-07 13:44:27.61722	f	t
1682	31	24	2017-08-14 13:44:27.617275	f	t
1683	31	29	2017-07-30 13:44:27.617349	f	t
1684	31	29	2017-07-31 13:44:27.617385	f	t
1685	32	34	2017-08-06 13:44:27.617416	t	t
1686	32	23	2017-08-05 13:44:27.617447	t	t
1687	32	18	2017-08-04 13:44:27.617477	t	t
1688	32	25	2017-07-26 13:44:27.617519	f	t
1689	32	10	2017-07-27 13:44:27.617575	f	t
1690	32	10	2017-08-07 13:44:27.617631	f	t
1691	32	34	2017-07-31 13:44:27.617685	f	t
1692	32	15	2017-07-25 13:44:27.617749	f	t
1693	32	36	2017-08-12 13:44:27.617798	f	t
1694	33	10	2017-07-30 13:44:27.617831	t	t
1695	33	15	2017-08-03 13:44:27.617873	t	t
1696	33	15	2017-08-01 13:44:27.617905	f	t
1697	33	34	2017-07-28 13:44:27.617946	f	t
1698	33	13	2017-08-12 13:44:27.617976	f	t
1699	34	14	2017-07-28 13:44:27.618008	t	t
1700	34	24	2017-08-06 13:44:27.618038	t	t
1701	34	27	2017-08-02 13:44:27.618068	t	t
1702	34	12	2017-08-10 13:44:27.618109	t	t
1703	34	11	2017-07-25 13:44:27.618157	t	t
1704	34	18	2017-08-12 13:44:27.618199	t	t
1705	34	14	2017-07-25 13:44:27.618241	t	t
1706	34	27	2017-08-03 13:44:27.618274	f	t
1707	35	14	2017-08-14 13:44:27.618304	t	t
1708	35	24	2017-08-03 13:44:27.618335	f	t
1709	36	25	2017-08-04 13:44:27.618366	t	t
1710	36	33	2017-08-09 13:44:27.618396	t	t
1711	36	29	2017-07-24 13:44:27.618426	t	t
1712	36	10	2017-07-25 13:44:27.618457	t	t
1713	36	28	2017-08-13 13:44:27.618489	t	t
1714	36	8	2017-07-30 13:44:27.618522	t	t
1715	36	31	2017-08-15 13:44:27.618563	t	t
1716	36	33	2017-07-30 13:44:27.618595	t	t
1717	36	24	2017-08-01 13:44:27.618646	t	t
1718	36	18	2017-08-10 13:44:27.618718	t	t
1719	36	15	2017-08-04 13:44:27.61875	t	t
1720	36	24	2017-08-15 13:44:27.61879	t	t
1721	36	25	2017-07-24 13:44:27.618832	f	t
1722	36	13	2017-08-04 13:44:27.618863	f	t
1723	36	19	2017-07-29 13:44:27.618894	f	t
1724	36	24	2017-08-02 13:44:27.618935	f	t
1725	36	17	2017-07-29 13:44:27.618976	f	t
1726	36	33	2017-08-04 13:44:27.619016	f	t
1727	37	28	2017-08-12 13:44:27.619045	t	t
1728	37	22	2017-08-16 13:44:27.619076	t	t
1729	38	23	2017-08-12 13:44:27.61911	t	t
1730	38	10	2017-08-15 13:44:27.61914	t	t
1731	38	34	2017-08-17 13:44:27.619171	t	t
1732	38	9	2017-07-23 13:44:27.619201	t	t
1733	39	21	2017-08-11 13:44:27.619231	t	t
1734	39	25	2017-07-30 13:44:27.619261	t	t
1735	39	35	2017-08-08 13:44:27.619291	t	t
1736	39	18	2017-08-01 13:44:27.619322	t	t
1737	39	11	2017-07-30 13:44:27.619352	t	t
1738	39	16	2017-07-26 13:44:27.619381	t	t
1739	39	16	2017-08-01 13:44:27.619413	t	t
1740	39	10	2017-08-13 13:44:27.619443	t	t
1741	39	22	2017-08-10 13:44:27.619474	t	t
1742	40	37	2017-07-31 13:44:27.619503	t	t
1743	40	37	2017-08-15 13:44:27.619533	t	t
1744	40	7	2017-08-12 13:44:27.619563	t	t
1745	40	15	2017-07-23 13:44:27.619593	t	t
1746	40	9	2017-07-27 13:44:27.619623	t	t
1747	40	23	2017-08-06 13:44:27.619653	t	t
1748	40	12	2017-08-14 13:44:27.619683	t	t
1749	40	25	2017-07-23 13:44:27.619714	t	t
1750	40	7	2017-08-17 13:44:27.619744	t	t
1751	40	29	2017-07-29 13:44:27.619775	t	t
1752	40	24	2017-08-03 13:44:27.619805	t	t
1753	40	25	2017-08-16 13:44:27.619835	t	t
1754	40	25	2017-07-25 13:44:27.619866	t	t
1755	40	24	2017-08-05 13:44:27.619898	t	t
1756	40	24	2017-08-13 13:44:27.619928	t	t
1757	40	28	2017-08-03 13:44:27.619959	t	t
1758	40	23	2017-08-17 13:44:27.619988	t	t
1759	40	16	2017-08-05 13:44:27.620018	t	t
1760	40	14	2017-08-03 13:44:27.620048	t	t
1761	40	29	2017-08-09 13:44:27.620078	t	t
1762	40	24	2017-07-27 13:44:27.62011	t	t
1763	40	22	2017-08-04 13:44:27.62014	t	t
1764	40	29	2017-07-31 13:44:27.620169	t	t
1765	40	28	2017-08-15 13:44:27.620202	t	t
1766	41	27	2017-08-14 13:44:27.620232	t	t
1767	41	29	2017-08-11 13:44:27.620262	t	t
1768	41	11	2017-07-25 13:44:27.620292	t	t
1769	41	31	2017-07-27 13:44:27.620322	t	t
1770	41	17	2017-07-30 13:44:27.620351	t	t
1771	41	25	2017-07-23 13:44:27.620382	t	t
1772	41	17	2017-08-15 13:44:27.620411	t	t
1773	41	9	2017-08-11 13:44:27.620463	t	t
1774	41	29	2017-08-10 13:44:27.620493	t	t
1775	41	12	2017-08-12 13:44:27.620522	t	t
1776	41	7	2017-08-07 13:44:27.620553	f	t
1777	41	29	2017-07-25 13:44:27.620582	f	t
1778	41	29	2017-08-04 13:44:27.620612	f	t
1779	41	7	2017-08-07 13:44:27.620642	f	t
1780	41	15	2017-08-07 13:44:27.620672	f	t
1781	41	12	2017-08-01 13:44:27.620702	f	t
1782	42	29	2017-08-08 13:44:27.620732	t	t
1783	42	16	2017-08-14 13:44:27.620762	t	t
1784	42	27	2017-08-15 13:44:27.620802	t	t
1785	42	15	2017-08-15 13:44:27.620865	t	t
1786	42	34	2017-08-03 13:44:27.620895	t	t
1787	42	37	2017-08-10 13:44:27.620925	t	t
1788	42	10	2017-07-30 13:44:27.620955	t	t
1789	42	31	2017-08-07 13:44:27.620995	t	t
1790	42	34	2017-08-16 13:44:27.621057	t	t
1791	42	29	2017-08-10 13:44:27.621107	t	t
1792	42	14	2017-08-10 13:44:27.621137	t	t
1793	42	29	2017-08-06 13:44:27.621166	t	t
1794	42	12	2017-07-29 13:44:27.621196	f	t
1795	42	27	2017-08-10 13:44:27.621225	f	t
1796	42	17	2017-07-27 13:44:27.621255	f	t
1797	42	29	2017-08-02 13:44:27.621285	f	t
1798	42	28	2017-08-15 13:44:27.621315	f	t
1799	42	37	2017-08-10 13:44:27.621344	f	t
1800	42	12	2017-08-02 13:44:27.621374	f	t
1801	42	19	2017-08-13 13:44:27.621407	f	t
1802	42	28	2017-08-13 13:44:27.621438	f	t
1803	42	36	2017-08-09 13:44:27.621468	f	t
1804	42	34	2017-07-29 13:44:27.621498	f	t
1805	42	24	2017-07-23 13:44:27.621529	f	t
1806	42	7	2017-08-16 13:44:27.621558	f	t
1807	43	24	2017-08-06 13:44:27.621589	t	t
1808	43	11	2017-08-03 13:44:27.62162	t	t
1809	43	13	2017-08-16 13:44:27.621651	t	t
1810	43	22	2017-08-08 13:44:27.621682	t	t
1811	43	32	2017-07-29 13:44:27.621716	f	t
1812	43	28	2017-08-17 13:44:27.621748	f	t
1813	44	36	2017-07-31 13:44:27.621778	t	t
1814	44	26	2017-08-12 13:44:27.621808	t	t
1815	44	23	2017-08-10 13:44:27.621838	f	t
1816	44	15	2017-08-07 13:44:27.621878	f	t
1817	44	26	2017-08-16 13:44:27.621909	f	t
1818	44	27	2017-08-09 13:44:27.62194	f	t
1819	44	10	2017-08-15 13:44:27.62197	f	t
1820	44	19	2017-08-06 13:44:27.622001	f	t
1821	44	29	2017-08-16 13:44:27.622041	f	t
1822	44	25	2017-08-09 13:44:27.622093	f	t
1823	44	23	2017-08-04 13:44:27.622135	f	t
1824	44	7	2017-08-04 13:44:27.622166	f	t
1825	45	20	2017-08-03 13:44:27.622196	t	t
1826	45	29	2017-08-03 13:44:27.622226	t	t
1827	45	7	2017-07-25 13:44:27.622256	t	t
1828	45	37	2017-07-27 13:44:27.622285	t	t
1829	45	24	2017-07-24 13:44:27.622315	t	t
1830	45	17	2017-08-02 13:44:27.622345	t	t
1831	45	11	2017-07-26 13:44:27.622375	t	t
1832	45	29	2017-08-03 13:44:27.622404	t	t
1833	45	24	2017-08-11 13:44:27.622434	t	t
1834	45	20	2017-08-06 13:44:27.622464	t	t
1835	45	16	2017-08-02 13:44:27.622494	t	t
1836	45	21	2017-08-03 13:44:27.622524	t	t
1837	45	20	2017-08-08 13:44:27.622556	f	t
1838	45	19	2017-08-12 13:44:27.622586	f	t
1839	45	20	2017-08-01 13:44:27.622616	f	t
1840	45	35	2017-07-29 13:44:27.622645	f	t
1841	45	28	2017-08-10 13:44:27.622675	f	t
1842	45	16	2017-08-01 13:44:27.622736	f	t
1843	45	24	2017-07-31 13:44:27.622768	f	t
1844	45	32	2017-08-01 13:44:27.622828	f	t
1845	45	15	2017-07-24 13:44:27.622882	f	t
1846	45	34	2017-07-24 13:44:27.622912	f	t
1847	45	29	2017-07-27 13:44:27.622942	f	t
1848	45	28	2017-08-17 13:44:27.622972	f	t
1849	45	24	2017-08-07 13:44:27.623002	f	t
1850	45	29	2017-08-08 13:44:27.623034	f	t
1851	45	13	2017-08-14 13:44:27.623064	f	t
1852	45	27	2017-08-01 13:44:27.623094	f	t
1853	45	29	2017-08-14 13:44:27.623127	f	t
1854	45	29	2017-07-31 13:44:27.623157	f	t
1855	45	29	2017-08-14 13:44:27.623186	f	t
1856	45	36	2017-07-26 13:44:27.623218	f	t
1857	45	29	2017-08-07 13:44:27.62325	f	t
1858	46	28	2017-08-06 13:44:27.623282	t	t
1859	47	29	2017-07-23 13:44:27.623313	t	t
1860	47	29	2017-08-08 13:44:27.623345	t	t
1861	47	34	2017-08-11 13:44:27.623374	t	t
1862	47	23	2017-07-30 13:44:27.623404	t	t
1863	47	28	2017-07-29 13:44:27.623437	t	t
1864	47	37	2017-08-07 13:44:27.62347	f	t
1865	47	8	2017-07-31 13:44:27.6235	f	t
1866	47	16	2017-08-12 13:44:27.62353	f	t
1867	47	15	2017-08-12 13:44:27.623562	f	t
1868	47	20	2017-07-31 13:44:27.623593	f	t
1869	47	12	2017-08-13 13:44:27.623624	f	t
1870	47	21	2017-08-16 13:44:27.623654	f	t
1871	47	12	2017-08-01 13:44:27.623684	f	t
1872	48	29	2017-08-06 13:44:27.623714	t	t
1873	48	21	2017-08-15 13:44:27.623782	t	t
1874	48	21	2017-07-29 13:44:27.623813	t	t
1875	48	23	2017-07-24 13:44:27.623843	t	t
1876	48	14	2017-07-26 13:44:27.623874	t	t
1877	48	31	2017-07-24 13:44:27.623903	t	t
1878	48	26	2017-07-25 13:44:27.623932	t	t
1879	48	29	2017-08-09 13:44:27.623962	t	t
1880	48	29	2017-07-31 13:44:27.623991	t	t
1881	48	35	2017-08-13 13:44:27.624021	t	t
1882	48	20	2017-08-08 13:44:27.62405	t	t
1883	48	34	2017-07-27 13:44:27.62408	t	t
1884	48	20	2017-08-02 13:44:27.62411	t	t
1885	48	19	2017-08-10 13:44:27.62414	f	t
1886	48	22	2017-07-30 13:44:27.62417	f	t
1887	48	37	2017-08-13 13:44:27.6242	f	t
1888	48	8	2017-08-14 13:44:27.62423	f	t
1889	48	11	2017-08-10 13:44:27.62426	f	t
1890	48	19	2017-08-06 13:44:27.624289	f	t
1891	48	9	2017-08-07 13:44:27.624319	f	t
1892	48	34	2017-08-07 13:44:27.624348	f	t
1893	48	9	2017-08-07 13:44:27.624377	f	t
1894	48	29	2017-08-17 13:44:27.624406	f	t
1895	48	15	2017-08-13 13:44:27.624435	f	t
1896	48	9	2017-07-28 13:44:27.624464	f	t
1897	48	31	2017-07-23 13:44:27.624494	f	t
1898	48	19	2017-08-09 13:44:27.624523	f	t
1899	48	12	2017-08-12 13:44:27.624553	f	t
1900	48	27	2017-08-02 13:44:27.624582	f	t
1901	49	32	2017-08-08 13:44:27.624611	t	t
1902	49	29	2017-08-05 13:44:27.62464	t	t
1903	49	7	2017-07-23 13:44:27.62467	t	t
1904	49	12	2017-08-09 13:44:27.624699	f	t
1905	49	25	2017-08-08 13:44:27.624728	f	t
1906	49	31	2017-07-27 13:44:27.624758	f	t
1907	49	19	2017-07-31 13:44:27.624789	f	t
1908	49	20	2017-08-04 13:44:27.62482	f	t
1909	49	17	2017-08-12 13:44:27.624852	f	t
1910	49	21	2017-08-01 13:44:27.624881	f	t
1911	49	12	2017-08-15 13:44:27.624911	f	t
1912	49	7	2017-08-17 13:44:27.624941	f	t
1913	49	25	2017-07-27 13:44:27.624971	f	t
1914	49	19	2017-08-13 13:44:27.625	f	t
1915	49	18	2017-07-29 13:44:27.62503	f	t
1916	49	25	2017-07-24 13:44:27.62506	f	t
1917	50	26	2017-08-13 13:44:27.625089	t	t
1918	50	15	2017-08-05 13:44:27.625119	t	t
1919	50	10	2017-08-07 13:44:27.625148	t	t
1920	50	12	2017-08-08 13:44:27.625178	t	t
1921	50	36	2017-08-13 13:44:27.625207	t	t
1922	50	37	2017-07-30 13:44:27.625237	t	t
1923	50	26	2017-08-04 13:44:27.625268	t	t
1924	50	34	2017-08-15 13:44:27.625299	t	t
1925	50	20	2017-08-09 13:44:27.625328	t	t
1926	50	33	2017-08-07 13:44:27.625358	t	t
1927	50	29	2017-07-30 13:44:27.625387	f	t
1928	50	15	2017-08-12 13:44:27.625416	f	t
1929	50	29	2017-08-09 13:44:27.625446	f	t
1930	50	18	2017-08-15 13:44:27.625476	f	t
1931	50	27	2017-08-12 13:44:27.625507	f	t
1932	50	25	2017-07-27 13:44:27.625538	f	t
1933	51	8	2017-07-27 13:44:27.625567	t	t
1934	51	32	2017-07-24 13:44:27.625597	t	t
1935	51	37	2017-08-08 13:44:27.625627	t	t
1936	51	14	2017-07-23 13:44:27.625657	t	t
1937	51	8	2017-08-12 13:44:27.625686	t	t
1938	51	22	2017-08-02 13:44:27.625716	t	t
1939	51	26	2017-08-14 13:44:27.625746	t	t
1940	51	14	2017-08-01 13:44:27.625776	t	t
1941	51	19	2017-08-08 13:44:27.625806	t	t
1942	51	11	2017-08-15 13:44:27.625835	t	t
1943	51	26	2017-08-08 13:44:27.625872	t	t
1944	51	14	2017-07-29 13:44:27.625903	t	t
1945	51	20	2017-07-25 13:44:27.625936	t	t
1946	51	33	2017-08-13 13:44:27.625966	t	t
1947	51	33	2017-08-02 13:44:27.625996	t	t
1948	51	18	2017-08-06 13:44:27.626025	t	t
1949	51	28	2017-08-12 13:44:27.626055	t	t
1950	51	27	2017-08-10 13:44:27.626085	t	t
1951	51	34	2017-07-29 13:44:27.626134	t	t
1952	51	21	2017-08-14 13:44:27.626165	t	t
1953	51	24	2017-08-14 13:44:27.626195	t	t
1954	51	10	2017-08-14 13:44:27.626226	f	t
1955	51	29	2017-08-04 13:44:27.626256	f	t
1956	52	32	2017-08-03 13:44:27.626285	f	t
1957	52	33	2017-07-23 13:44:27.626315	f	t
1958	52	12	2017-08-08 13:44:27.626345	f	t
1959	53	7	2017-08-10 13:44:27.626375	t	t
1960	53	31	2017-07-23 13:44:27.626405	t	t
1961	53	18	2017-08-06 13:44:27.626435	t	t
1962	53	7	2017-08-10 13:44:27.626465	f	t
1963	53	14	2017-07-27 13:44:27.626495	f	t
1964	53	28	2017-08-14 13:44:27.626527	f	t
1965	53	36	2017-07-27 13:44:27.626557	f	t
1966	53	21	2017-08-11 13:44:27.626587	f	t
1967	53	37	2017-08-16 13:44:27.626617	f	t
1968	53	11	2017-07-23 13:44:27.626647	f	t
1969	53	35	2017-08-01 13:44:27.626676	f	t
1970	53	12	2017-08-09 13:44:27.626705	f	t
1971	53	19	2017-08-11 13:44:27.626735	f	t
1972	53	16	2017-08-14 13:44:27.626764	f	t
1973	53	28	2017-08-01 13:44:27.626794	f	t
1974	54	29	2017-08-04 13:44:27.626823	t	t
1975	54	26	2017-08-15 13:44:27.626853	f	t
1976	54	29	2017-08-01 13:44:27.626883	f	t
1977	55	35	2017-08-14 13:44:27.626913	f	t
1978	55	27	2017-08-12 13:44:27.626944	f	t
1979	56	15	2017-08-10 13:44:27.626975	t	t
1980	56	18	2017-08-13 13:44:27.627006	t	t
1981	56	35	2017-07-29 13:44:27.627038	t	t
1982	56	23	2017-08-11 13:44:27.627068	t	t
1983	56	36	2017-08-04 13:44:27.627098	t	t
1984	56	21	2017-08-08 13:44:27.627127	t	t
1985	56	33	2017-08-05 13:44:27.627156	t	t
1986	56	34	2017-07-30 13:44:27.627186	f	t
1987	56	18	2017-08-11 13:44:27.627216	f	t
1988	57	18	2017-08-16 13:44:27.627246	t	t
1989	57	18	2017-08-11 13:44:27.627276	t	t
1990	57	26	2017-07-28 13:44:27.627306	t	t
1991	57	34	2017-08-17 13:44:27.627338	t	t
1992	57	14	2017-08-06 13:44:27.627369	t	t
1993	57	10	2017-07-29 13:44:27.627399	t	t
1994	57	18	2017-07-23 13:44:27.627428	t	t
1995	57	23	2017-08-03 13:44:27.627469	t	t
1996	57	31	2017-08-11 13:44:27.62752	t	t
1997	57	34	2017-08-01 13:44:27.62756	f	t
1998	57	12	2017-07-25 13:44:27.627589	f	t
1999	57	35	2017-08-11 13:44:27.627619	f	t
2000	57	10	2017-08-02 13:44:27.627659	f	t
2001	57	23	2017-08-08 13:44:27.627724	f	t
2002	57	10	2017-08-09 13:44:27.627753	f	t
2003	57	8	2017-08-09 13:44:27.627783	f	t
2004	57	20	2017-08-04 13:44:27.627812	f	t
2005	57	13	2017-08-11 13:44:27.627842	f	t
2006	57	23	2017-08-06 13:44:27.627872	f	t
2007	58	18	2017-08-14 13:44:27.627902	f	t
2008	58	16	2017-07-28 13:44:27.627932	f	t
2009	58	17	2017-08-05 13:44:27.627962	f	t
2010	58	9	2017-07-25 13:44:27.627991	f	t
2011	59	34	2017-07-31 13:44:27.628021	t	t
2012	59	17	2017-08-02 13:44:27.628051	t	t
2013	59	9	2017-08-09 13:44:27.62808	t	t
2014	59	19	2017-08-15 13:44:27.62811	t	t
2015	59	28	2017-08-02 13:44:27.62814	f	t
2016	59	13	2017-08-15 13:44:27.62817	f	t
2017	59	17	2017-08-07 13:44:27.628203	f	t
2018	59	35	2017-08-04 13:44:27.628233	f	t
2019	59	15	2017-08-06 13:44:27.628263	f	t
2020	60	37	2017-07-30 13:44:27.628293	t	t
2021	60	19	2017-08-13 13:44:27.628323	t	t
2022	60	23	2017-07-29 13:44:27.628353	t	t
2023	60	8	2017-07-26 13:44:27.628383	t	t
2024	60	22	2017-08-05 13:44:27.628412	t	t
2025	60	8	2017-08-12 13:44:27.628442	t	t
2026	60	10	2017-07-23 13:44:27.628471	t	t
2027	60	8	2017-08-02 13:44:27.6285	t	t
2028	60	31	2017-08-02 13:44:27.628543	t	t
2029	60	17	2017-08-13 13:44:27.628583	t	t
2030	60	13	2017-07-30 13:44:27.628613	f	t
2031	60	15	2017-07-28 13:44:27.628643	f	t
2032	60	28	2017-08-12 13:44:27.628672	f	t
2033	60	14	2017-07-24 13:44:27.628703	f	t
2034	60	29	2017-08-16 13:44:27.628733	f	t
2035	60	18	2017-08-03 13:44:27.628766	f	t
2036	60	17	2017-07-30 13:44:27.628797	f	t
2037	60	29	2017-07-26 13:44:27.628827	f	t
2038	60	25	2017-07-25 13:44:27.628857	f	t
2039	60	37	2017-08-16 13:44:27.628887	f	t
2040	60	16	2017-08-05 13:44:27.628917	f	t
2041	60	17	2017-08-13 13:44:27.628948	f	t
2042	60	8	2017-08-14 13:44:27.628978	f	t
2043	60	29	2017-08-13 13:44:27.629008	f	t
2044	60	18	2017-07-26 13:44:27.629038	f	t
2045	60	16	2017-08-03 13:44:27.629069	f	t
2046	60	14	2017-07-29 13:44:27.629099	f	t
2047	60	21	2017-07-30 13:44:27.629128	f	t
2048	60	25	2017-07-29 13:44:27.629157	f	t
2049	60	7	2017-07-31 13:44:27.629187	f	t
2050	60	13	2017-08-04 13:44:27.629216	f	t
2051	60	33	2017-08-02 13:44:27.629245	f	t
2052	60	29	2017-07-31 13:44:27.629275	f	t
2053	61	26	2017-07-30 13:44:27.629307	t	t
2054	61	16	2017-08-12 13:44:27.629337	f	t
2055	61	33	2017-08-14 13:44:27.629367	f	t
2056	61	9	2017-08-07 13:44:27.629397	f	t
2057	61	29	2017-08-11 13:44:27.629427	f	t
2058	61	21	2017-07-23 13:44:27.629457	f	t
2059	61	13	2017-08-01 13:44:27.629486	f	t
2060	61	17	2017-08-01 13:44:27.629516	f	t
2061	61	15	2017-07-28 13:44:27.629545	f	t
2062	61	12	2017-08-01 13:44:27.629575	f	t
2063	62	37	2017-07-30 13:44:27.629627	t	t
2064	62	37	2017-08-06 13:44:27.629658	t	t
2065	62	36	2017-08-06 13:44:27.629689	t	t
2066	62	28	2017-08-04 13:44:27.62972	t	t
2067	62	37	2017-08-16 13:44:27.62975	t	t
2068	62	9	2017-08-07 13:44:27.629779	t	t
2069	62	24	2017-07-27 13:44:27.629809	f	t
2070	62	12	2017-08-16 13:44:27.629839	f	t
2071	62	11	2017-08-04 13:44:27.629875	f	t
2072	62	27	2017-08-16 13:44:27.629906	f	t
2073	62	21	2017-08-11 13:44:27.629936	f	t
2074	63	25	2017-07-27 13:44:27.629966	t	t
2075	63	22	2017-07-31 13:44:27.629997	t	t
2076	63	32	2017-08-08 13:44:27.630028	t	t
2077	63	20	2017-07-31 13:44:27.630058	t	t
2078	63	7	2017-08-12 13:44:27.630088	t	t
2079	63	19	2017-08-10 13:44:27.630118	t	t
2080	63	28	2017-08-16 13:44:27.630148	t	t
2081	63	13	2017-07-27 13:44:27.630186	f	t
2082	63	31	2017-07-27 13:44:27.630215	f	t
2083	63	12	2017-08-05 13:44:27.630244	f	t
2084	63	7	2017-07-24 13:44:27.630273	f	t
2085	64	14	2017-08-06 13:44:27.630302	t	t
2086	64	29	2017-07-30 13:44:27.630331	t	t
2087	64	31	2017-08-10 13:44:27.63036	t	t
2088	64	14	2017-08-12 13:44:27.630388	t	t
2089	64	36	2017-08-14 13:44:27.63042	t	t
2090	64	23	2017-07-30 13:44:27.63045	t	t
2091	64	20	2017-07-24 13:44:27.630481	t	t
2092	64	21	2017-08-01 13:44:27.630511	t	t
2093	64	27	2017-08-16 13:44:27.63054	t	t
2094	64	31	2017-07-24 13:44:27.630569	f	t
2095	64	15	2017-07-24 13:44:27.630598	f	t
2096	64	19	2017-08-04 13:44:27.630627	f	t
2097	64	11	2017-08-16 13:44:27.630656	f	t
2098	65	18	2017-07-24 13:44:27.630685	t	t
2099	65	19	2017-08-08 13:44:27.630714	f	t
2100	65	23	2017-08-14 13:44:27.630743	f	t
2101	65	34	2017-08-11 13:44:27.630772	f	t
2102	65	25	2017-07-30 13:44:27.630802	f	t
2103	65	28	2017-08-08 13:44:27.630831	f	t
2104	65	20	2017-08-02 13:44:27.630861	f	t
2105	65	11	2017-07-27 13:44:27.630889	f	t
2106	66	17	2017-08-17 13:44:27.630918	t	t
2107	66	29	2017-08-08 13:44:27.630947	t	t
2108	66	31	2017-08-14 13:44:27.630977	t	t
2109	66	31	2017-08-07 13:44:27.631006	t	t
2110	66	13	2017-08-04 13:44:27.631035	t	t
2111	66	23	2017-08-16 13:44:27.631064	t	t
2112	66	35	2017-08-06 13:44:27.631093	t	t
2113	66	23	2017-08-16 13:44:27.631122	t	t
2114	66	13	2017-08-03 13:44:27.631151	f	t
2115	66	19	2017-07-23 13:44:27.631179	f	t
2116	66	13	2017-07-31 13:44:27.631208	f	t
2117	66	12	2017-07-30 13:44:27.631237	f	t
2118	66	9	2017-08-10 13:44:27.631265	f	t
2119	66	31	2017-07-27 13:44:27.631293	f	t
2120	66	15	2017-07-31 13:44:27.631321	f	t
2121	66	12	2017-07-30 13:44:27.63135	f	t
2122	67	20	2017-07-29 13:44:27.631378	t	t
2123	67	22	2017-08-04 13:44:27.631407	f	t
2124	67	29	2017-08-16 13:44:27.631436	f	t
2125	67	32	2017-08-03 13:44:27.631467	f	t
2126	67	20	2017-08-08 13:44:27.631496	f	t
2127	68	8	2017-08-08 13:44:27.631525	t	t
2128	68	28	2017-07-24 13:44:27.631554	t	t
2129	68	8	2017-07-29 13:44:27.631582	t	t
2130	68	15	2017-08-07 13:44:27.631611	t	t
2131	68	10	2017-07-24 13:44:27.63164	t	t
2132	68	23	2017-07-24 13:44:27.631669	t	t
2133	68	13	2017-07-23 13:44:27.631697	t	t
2134	68	25	2017-08-04 13:44:27.631726	t	t
2135	68	28	2017-08-12 13:44:27.631771	t	t
2136	68	28	2017-08-13 13:44:27.631803	t	t
2137	68	16	2017-07-29 13:44:27.631833	t	t
2138	68	36	2017-08-05 13:44:27.631862	t	t
2139	68	11	2017-08-11 13:44:27.631891	t	t
2140	68	22	2017-08-10 13:44:27.63192	f	t
2141	68	33	2017-08-13 13:44:27.631949	f	t
2142	68	35	2017-08-05 13:44:27.631989	f	t
2143	68	18	2017-08-14 13:44:27.632019	f	t
2144	68	31	2017-08-09 13:44:27.632049	f	t
2145	68	22	2017-08-15 13:44:27.63209	f	t
2146	68	31	2017-08-03 13:44:27.632121	f	t
2147	68	9	2017-07-26 13:44:27.632177	f	t
2148	68	14	2017-07-30 13:44:27.632227	f	t
2149	69	18	2017-08-02 13:44:27.632258	t	t
2150	69	17	2017-07-29 13:44:27.632287	t	t
2151	69	9	2017-08-02 13:44:27.632316	t	t
2152	69	37	2017-08-03 13:44:27.632345	f	t
2153	69	14	2017-07-25 13:44:27.632374	f	t
2154	69	12	2017-08-08 13:44:27.632403	f	t
2155	69	33	2017-08-03 13:44:27.632431	f	t
2156	69	27	2017-08-16 13:44:27.63246	f	t
2157	69	11	2017-07-31 13:44:27.63249	f	t
2158	70	32	2017-08-10 13:44:27.632519	f	t
2159	70	9	2017-08-14 13:44:27.63255	f	t
2160	70	19	2017-08-11 13:44:27.632579	f	t
2161	71	11	2017-07-27 13:44:27.632611	t	t
2162	71	27	2017-08-12 13:44:27.632641	t	t
2163	71	32	2017-07-24 13:44:27.63267	t	t
2164	71	29	2017-07-25 13:44:27.632699	t	t
2165	71	35	2017-08-07 13:44:27.632728	t	t
2166	71	20	2017-08-14 13:44:27.632759	t	t
2167	71	11	2017-08-16 13:44:27.632789	t	t
2168	71	34	2017-08-07 13:44:27.632818	f	t
2169	71	22	2017-07-24 13:44:27.632847	f	t
2170	71	11	2017-08-04 13:44:27.632876	f	t
2171	72	15	2017-08-10 13:44:27.632905	t	t
2172	72	33	2017-08-14 13:44:27.632934	t	t
2173	72	37	2017-08-14 13:44:27.632963	t	t
2174	72	32	2017-07-27 13:44:27.632992	t	t
2175	72	36	2017-08-17 13:44:27.633031	t	t
2176	72	23	2017-08-07 13:44:27.63306	t	t
2177	72	32	2017-08-04 13:44:27.633102	t	t
2178	72	13	2017-08-16 13:44:27.633153	t	t
2179	72	11	2017-07-31 13:44:27.633193	t	t
2180	72	15	2017-08-09 13:44:27.633231	t	t
2181	72	28	2017-08-01 13:44:27.633259	t	t
2182	72	27	2017-08-08 13:44:27.633288	t	t
2183	72	29	2017-08-11 13:44:27.633317	t	t
2184	72	33	2017-07-24 13:44:27.633362	t	t
2185	72	29	2017-08-11 13:44:27.633392	t	t
2186	72	36	2017-08-14 13:44:27.633421	t	t
2187	72	29	2017-08-17 13:44:27.63345	t	t
2188	72	34	2017-08-08 13:44:27.633479	t	t
2189	72	23	2017-08-15 13:44:27.633507	t	t
2190	72	11	2017-08-11 13:44:27.633535	t	t
2191	72	18	2017-08-09 13:44:27.633564	t	t
2192	72	29	2017-07-28 13:44:27.633592	t	t
2193	72	31	2017-08-13 13:44:27.633621	t	t
2194	72	12	2017-08-02 13:44:27.633649	t	t
2195	72	19	2017-08-04 13:44:27.633678	t	t
2196	72	33	2017-07-31 13:44:27.633706	f	t
2197	72	19	2017-08-07 13:44:27.633737	f	t
2198	72	25	2017-08-13 13:44:27.633766	f	t
2199	72	37	2017-08-14 13:44:27.633795	f	t
2200	72	16	2017-08-09 13:44:27.633824	f	t
2201	72	20	2017-07-28 13:44:27.633868	f	t
2202	72	14	2017-08-17 13:44:27.6339	f	t
2203	72	17	2017-07-28 13:44:27.633952	f	t
2204	72	35	2017-08-12 13:44:27.633982	f	t
2205	72	33	2017-08-13 13:44:27.634013	f	t
2206	72	8	2017-07-23 13:44:27.634043	f	t
2207	72	14	2017-08-16 13:44:27.634082	f	t
2208	72	19	2017-08-09 13:44:27.634111	f	t
2209	72	11	2017-08-02 13:44:27.63414	f	t
2210	72	21	2017-08-01 13:44:27.634168	f	t
2211	73	29	2017-08-16 13:44:27.634196	t	t
2212	73	21	2017-07-25 13:44:27.634227	t	t
2213	73	20	2017-08-17 13:44:27.634256	t	t
2214	73	29	2017-07-30 13:44:27.634285	t	t
2215	73	31	2017-08-04 13:44:27.634314	t	t
2216	73	8	2017-08-16 13:44:27.634342	t	t
2217	73	22	2017-08-01 13:44:27.634371	t	t
2218	73	14	2017-08-10 13:44:27.634401	t	t
2219	73	31	2017-07-25 13:44:27.63443	t	t
2220	73	27	2017-08-08 13:44:27.634459	t	t
2221	73	35	2017-08-01 13:44:27.634488	t	t
2222	73	27	2017-07-24 13:44:27.634516	f	t
2223	73	15	2017-07-30 13:44:27.634545	f	t
2224	73	21	2017-08-05 13:44:27.634573	f	t
2225	73	12	2017-07-31 13:44:27.634602	f	t
2226	73	27	2017-08-06 13:44:27.634641	f	t
2227	73	12	2017-08-16 13:44:27.634679	f	t
2228	73	27	2017-08-06 13:44:27.634708	f	t
2229	73	34	2017-08-03 13:44:27.634737	f	t
2230	73	29	2017-08-17 13:44:27.634766	f	t
2231	73	24	2017-08-10 13:44:27.634794	f	t
2232	73	18	2017-08-05 13:44:27.634823	f	t
2233	73	31	2017-08-03 13:44:27.634856	f	t
2234	73	16	2017-08-03 13:44:27.634886	f	t
2235	74	24	2017-08-05 13:44:27.634914	t	t
2236	74	32	2017-07-31 13:44:27.634943	t	t
2237	74	10	2017-08-14 13:44:27.634971	t	t
2238	74	33	2017-08-08 13:44:27.635	f	t
2239	74	23	2017-08-14 13:44:27.635029	f	t
2240	74	31	2017-07-25 13:44:27.635058	f	t
2241	74	29	2017-08-15 13:44:27.635087	f	t
2242	74	18	2017-08-10 13:44:27.635117	f	t
2243	74	34	2017-07-25 13:44:27.635148	f	t
2244	75	7	2017-08-06 13:44:27.635178	t	t
2245	75	16	2017-07-25 13:44:27.635206	t	t
2246	75	22	2017-07-23 13:44:27.635235	t	t
2247	75	33	2017-07-28 13:44:27.635264	t	t
2248	75	7	2017-08-10 13:44:27.635294	t	t
2249	75	14	2017-07-24 13:44:27.635323	t	t
2250	75	32	2017-08-09 13:44:27.635351	t	t
2251	75	27	2017-07-29 13:44:27.63538	t	t
2252	75	29	2017-07-27 13:44:27.635408	t	t
2253	75	7	2017-08-12 13:44:27.635437	t	t
2254	75	26	2017-08-11 13:44:27.635467	t	t
2255	75	14	2017-08-05 13:44:27.635495	t	t
2256	75	21	2017-08-15 13:44:27.635523	t	t
2257	75	27	2017-08-03 13:44:27.635552	t	t
2258	75	23	2017-08-17 13:44:27.635581	t	t
2259	75	10	2017-07-31 13:44:27.635611	f	t
2260	75	10	2017-08-16 13:44:27.63564	f	t
2261	75	23	2017-08-03 13:44:27.635669	f	t
2262	75	36	2017-08-02 13:44:27.635698	f	t
2263	75	9	2017-08-13 13:44:27.635726	f	t
2264	75	24	2017-08-10 13:44:27.635755	f	t
2265	75	10	2017-08-04 13:44:27.635784	f	t
2266	75	35	2017-08-11 13:44:27.635813	f	t
2267	75	16	2017-08-13 13:44:27.635844	f	t
2268	76	35	2017-07-30 13:44:27.635873	t	t
2269	76	33	2017-07-27 13:44:27.635905	t	t
2270	76	24	2017-08-01 13:44:27.635934	t	t
2271	76	24	2017-07-25 13:44:27.635963	t	t
2272	77	37	2017-07-25 13:44:27.635992	t	t
2273	77	19	2017-07-27 13:44:27.63602	t	t
2274	77	26	2017-07-28 13:44:27.636049	t	t
2275	77	26	2017-07-31 13:44:27.636078	t	t
2276	77	7	2017-08-01 13:44:27.636107	t	t
2277	77	25	2017-08-01 13:44:27.636135	t	t
2278	77	23	2017-08-05 13:44:27.636163	f	t
2279	77	25	2017-07-25 13:44:27.636192	f	t
2280	77	14	2017-07-29 13:44:27.63622	f	t
2281	77	35	2017-08-03 13:44:27.636249	f	t
2282	77	36	2017-08-12 13:44:27.636278	f	t
2283	77	17	2017-07-30 13:44:27.636307	f	t
2284	77	23	2017-08-17 13:44:27.636335	f	t
2285	77	25	2017-08-16 13:44:27.636364	f	t
2286	77	15	2017-08-09 13:44:27.636393	f	t
2287	77	24	2017-08-17 13:44:27.636422	f	t
2288	77	15	2017-08-11 13:44:27.636451	f	t
2289	77	8	2017-08-14 13:44:27.63648	f	t
2290	77	17	2017-08-02 13:44:27.636509	f	t
2291	77	12	2017-07-24 13:44:27.636539	f	t
2292	77	13	2017-08-17 13:44:27.636568	f	t
2293	77	24	2017-08-13 13:44:27.636597	f	t
2294	78	10	2017-08-06 13:44:27.636626	t	t
2295	78	29	2017-07-27 13:44:27.636655	t	t
2296	78	27	2017-08-01 13:44:27.636683	t	t
2297	78	10	2017-08-13 13:44:27.636712	f	t
2298	78	24	2017-08-05 13:44:27.636741	f	t
2299	78	28	2017-08-02 13:44:27.63677	f	t
2300	79	31	2017-08-14 13:44:27.636799	t	t
2301	79	18	2017-07-25 13:44:27.636828	t	t
2302	79	15	2017-07-23 13:44:27.636856	t	t
2303	79	12	2017-08-04 13:44:27.636885	t	t
2304	79	22	2017-07-29 13:44:27.636914	t	t
2305	79	17	2017-07-23 13:44:27.636945	t	t
2306	79	13	2017-08-10 13:44:27.636974	t	t
2307	79	27	2017-08-11 13:44:27.637003	t	t
2308	79	11	2017-08-15 13:44:27.637031	t	t
2309	79	17	2017-07-26 13:44:27.63706	t	t
2310	79	29	2017-07-25 13:44:27.637088	t	t
2311	79	10	2017-07-23 13:44:27.637116	t	t
2312	79	10	2017-08-09 13:44:27.637145	f	t
2313	79	32	2017-08-16 13:44:27.637173	f	t
2314	79	21	2017-08-15 13:44:27.637202	f	t
2315	79	37	2017-08-02 13:44:27.637233	f	t
2316	79	22	2017-07-28 13:44:27.637263	f	t
2317	79	35	2017-07-26 13:44:27.637292	f	t
2318	79	7	2017-07-29 13:44:27.63732	f	t
2319	80	29	2017-07-25 13:44:27.637349	t	t
2320	80	14	2017-08-10 13:44:27.637377	t	t
2321	80	28	2017-07-30 13:44:27.637406	t	t
2322	80	35	2017-08-16 13:44:27.637434	f	t
2323	80	23	2017-07-25 13:44:27.637463	f	t
2324	80	12	2017-08-08 13:44:27.637491	f	t
2325	80	21	2017-08-03 13:44:27.637521	f	t
2326	80	14	2017-08-15 13:44:27.637549	f	t
2327	80	12	2017-07-23 13:44:27.637581	f	t
2328	80	26	2017-08-11 13:44:27.63761	f	t
2329	80	8	2017-08-11 13:44:27.637639	f	t
2330	80	20	2017-08-06 13:44:27.637668	f	t
2331	80	12	2017-07-26 13:44:27.637697	f	t
2332	80	35	2017-08-01 13:44:27.637728	f	t
2333	81	29	2017-07-29 13:44:27.637757	t	t
2334	81	37	2017-07-26 13:44:27.637786	t	t
2335	81	22	2017-07-29 13:44:27.637815	t	t
2336	81	35	2017-08-14 13:44:27.637844	f	t
2337	81	18	2017-08-15 13:44:27.637878	f	t
2338	81	21	2017-08-14 13:44:27.637908	f	t
2339	81	13	2017-08-15 13:44:27.637937	f	t
2340	81	9	2017-07-23 13:44:27.637967	f	t
2341	81	14	2017-08-13 13:44:27.637998	f	t
2342	81	26	2017-08-01 13:44:27.638028	f	t
2343	81	17	2017-07-24 13:44:27.638056	f	t
\.


--
-- Name: clicked_statements_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('clicked_statements_uid_seq', 2343, true);


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
1	Town has to cut spending 	town-has-to-cut-spending	Our town needs to cut spending. Please discuss ideas how this should be done.		2017-08-17 13:44:19.415855	2	1	t
2	Cat or Dog	cat-or-dog	Your family argues about whether to buy a cat or dog as pet. Now your opinion matters!		2017-08-17 13:44:19.416018	2	1	f
3	Make the world better	make-the-world-better	How can we make this world a better place?		2017-08-17 13:44:19.41615	2	1	f
4	Elektroautos	elektroautos	Elektroautos - Die Autos der Zukunft? Bitte diskutieren Sie dazu.		2017-08-17 13:44:19.416274	2	2	f
5	Unterstützung der Sekretariate	unterstutzung-der-sekretariate	Unsere Sekretariate in der Informatik sind arbeitsmäßig stark überlastet. Bitte diskutieren Sie Möglichkeiten um dies zu verbessern.		2017-08-17 13:44:19.417166	2	2	f
6	Verbesserung des Informatik-Studiengangs	verbesserung-des-informatik-studiengangs	Wie können der Informatik-Studiengang verbessert und die Probleme, die durch die große Anzahl der Studierenden entstanden sind, gelöst werden?	Die Anzahl der Studierenden in der Informatik hat sich in den letzten Jahren stark erhöht. Dadurch treten zahlreiche Probleme auf, wie z.B. Raumknappheit, überfüllte Lehrveranstaltungen und ein Mangel an Plätzen zum Lernen. Wir möchten Sie gerne dazu einladen, gemeinsam mit den Dozierenden der Informatik über Lösungsmöglichkeiten zu diskutieren: Wie können der Studiengang verbessert und die Probleme, die durch die große Anzahl der Studierenden entstanden sind, gelöst werden?	2017-08-17 13:44:19.417312	2	2	t
7	Bürgerbeteiligung in der Kommune	burgerbeteiligung-in-der-kommune	Es werden Vorschläge zur Verbesserung des Zusammenlebens in unserer Kommune gesammelt.		2017-08-17 13:44:19.417458	2	2	f
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
1	14	1	t	2017-08-17 13:44:22.544802
2	16	1	f	2017-08-17 13:44:22.544925
3	17	1	t	2017-08-17 13:44:22.545044
4	22	1	t	2017-08-17 13:44:22.54516
5	23	1	t	2017-08-17 13:44:22.545276
6	20	2	f	2017-08-17 13:44:22.545392
7	21	2	t	2017-08-17 13:44:22.545507
8	18	2	f	2017-08-17 13:44:22.545621
9	34	2	t	2017-08-17 13:44:22.545735
10	24	2	f	2017-08-17 13:44:22.545885
11	25	2	f	2017-08-17 13:44:22.546008
12	26	2	f	2017-08-17 13:44:22.546124
13	27	3	f	2017-08-17 13:44:22.54624
14	28	3	f	2017-08-17 13:44:22.546356
15	33	3	f	2017-08-17 13:44:22.546473
16	19	8	t	2017-08-17 13:44:22.54659
17	35	8	t	2017-08-17 13:44:22.546706
18	36	8	t	2017-08-17 13:44:22.546821
\.


--
-- Name: last_reviewers_delete_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('last_reviewers_delete_uid_seq', 18, true);


--
-- Data for Name: last_reviewers_duplicates; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY last_reviewers_duplicates (uid, reviewer_uid, review_uid, is_okay, "timestamp") FROM stdin;
1	12	1	t	2017-08-17 13:44:22.546965
2	13	2	t	2017-08-17 13:44:22.54709
3	14	2	t	2017-08-17 13:44:22.547211
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
1	29	1	t	2017-08-17 13:44:22.543919
2	31	1	t	2017-08-17 13:44:22.544137
3	32	1	t	2017-08-17 13:44:22.544281
4	12	2	f	2017-08-17 13:44:22.544413
5	13	2	f	2017-08-17 13:44:22.544536
6	15	2	f	2017-08-17 13:44:22.544658
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
1	1	1	f	1	2017-08-17 13:44:19.656029	2	t
2	2	5	f	1	2017-08-17 13:44:19.65617	2	f
3	3	6	f	1	2017-08-17 13:44:19.656251	2	f
4	4	7	f	1	2017-08-17 13:44:19.656328	2	f
5	5	8	f	1	2017-08-17 13:44:19.656404	2	f
6	6	9	f	1	2017-08-17 13:44:19.656478	2	f
7	7	10	f	1	2017-08-17 13:44:19.656561	2	f
8	8	11	f	1	2017-08-17 13:44:19.656634	2	f
9	9	12	f	1	2017-08-17 13:44:19.656706	2	f
10	10	13	f	1	2017-08-17 13:44:19.656777	2	f
11	11	14	f	1	2017-08-17 13:44:19.656849	2	f
12	12	15	f	1	2017-08-17 13:44:19.65692	2	f
13	12	16	f	1	2017-08-17 13:44:19.656991	2	f
14	13	17	f	1	2017-08-17 13:44:19.657064	2	f
15	14	18	f	1	2017-08-17 13:44:19.657136	2	f
16	15	19	f	1	2017-08-17 13:44:19.657208	2	f
17	16	20	f	1	2017-08-17 13:44:19.657279	2	f
18	17	21	f	1	2017-08-17 13:44:19.65735	2	f
19	18	22	f	1	2017-08-17 13:44:19.657421	2	f
20	19	23	f	1	2017-08-17 13:44:19.657492	2	f
21	20	24	f	1	2017-08-17 13:44:19.657564	2	f
22	21	25	f	1	2017-08-17 13:44:19.657637	2	f
23	22	26	f	1	2017-08-17 13:44:19.657709	2	f
24	23	27	f	1	2017-08-17 13:44:19.657781	2	f
25	24	28	f	1	2017-08-17 13:44:19.657865	2	f
26	25	29	f	1	2017-08-17 13:44:19.657941	2	f
27	26	30	f	1	2017-08-17 13:44:19.658013	2	f
28	27	31	f	1	2017-08-17 13:44:19.658085	2	f
29	28	32	f	1	2017-08-17 13:44:19.658157	2	f
30	29	33	f	1	2017-08-17 13:44:19.658228	2	f
31	30	34	f	1	2017-08-17 13:44:19.6583	2	f
32	9	35	f	1	2017-08-17 13:44:19.658371	2	f
33	31	39	f	1	2017-08-17 13:44:19.658442	1	f
34	32	40	f	1	2017-08-17 13:44:19.658514	1	f
35	33	41	f	1	2017-08-17 13:44:19.658586	1	f
36	34	42	f	1	2017-08-17 13:44:19.658657	1	f
37	35	43	f	1	2017-08-17 13:44:19.658729	1	f
38	36	44	f	1	2017-08-17 13:44:19.6588	1	f
39	37	45	f	1	2017-08-17 13:44:19.658872	1	f
40	38	46	f	1	2017-08-17 13:44:19.658944	1	f
41	39	47	f	1	2017-08-17 13:44:19.659015	1	f
42	40	48	f	1	2017-08-17 13:44:19.659086	1	f
43	41	49	f	1	2017-08-17 13:44:19.659157	1	f
44	42	50	f	1	2017-08-17 13:44:19.659228	1	f
45	43	51	f	1	2017-08-17 13:44:19.659299	1	f
46	44	52	f	1	2017-08-17 13:44:19.659372	1	f
47	45	53	f	1	2017-08-17 13:44:19.659443	1	f
48	46	54	f	1	2017-08-17 13:44:19.659514	1	f
49	47	55	f	1	2017-08-17 13:44:19.659585	1	f
50	48	56	f	1	2017-08-17 13:44:19.659657	1	f
51	49	57	f	1	2017-08-17 13:44:19.659727	1	f
52	52	61	f	1	2017-08-17 13:44:19.660028	4	f
53	53	62	f	1	2017-08-17 13:44:19.660102	4	f
54	54	63	f	1	2017-08-17 13:44:19.66023	4	f
55	55	64	f	1	2017-08-17 13:44:19.66031	4	f
56	56	65	f	1	2017-08-17 13:44:19.660383	4	f
57	57	66	f	1	2017-08-17 13:44:19.660455	4	f
58	50	59	f	1	2017-08-17 13:44:19.65981	4	f
59	51	60	f	1	2017-08-17 13:44:19.659926	4	f
60	61	68	f	5	2017-08-17 13:44:19.660526	4	f
61	62	71	f	1	2017-08-17 13:44:19.6606	5	f
62	63	72	f	1	2017-08-17 13:44:19.660672	5	f
63	64	73	f	1	2017-08-17 13:44:19.660743	5	f
64	65	74	f	1	2017-08-17 13:44:19.660816	5	f
65	66	75	f	1	2017-08-17 13:44:19.660888	5	f
66	67	77	f	1	2017-08-17 13:44:19.66096	7	f
67	68	78	f	1	2017-08-17 13:44:19.661035	7	f
68	69	79	f	1	2017-08-17 13:44:19.661108	7	f
69	70	80	f	1	2017-08-17 13:44:19.661182	7	f
70	70	81	f	1	2017-08-17 13:44:19.661255	7	f
71	71	82	f	1	2017-08-17 13:44:19.661327	7	f
\.


--
-- Name: premises_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('premises_uid_seq', 71, true);


--
-- Data for Name: reputation_history; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY reputation_history (uid, reputator_uid, reputation_uid, "timestamp") FROM stdin;
1	23	1	2017-08-15 13:44:22.594373
2	23	2	2017-08-16 13:44:22.594373
3	23	3	2017-08-17 13:44:22.594373
4	25	1	2017-08-15 13:44:22.594373
5	25	2	2017-08-16 13:44:22.594373
6	25	3	2017-08-17 13:44:22.594373
7	22	1	2017-08-15 13:44:22.594373
8	22	2	2017-08-16 13:44:22.594373
9	22	3	2017-08-17 13:44:22.594373
10	34	1	2017-08-15 13:44:22.594373
11	34	2	2017-08-16 13:44:22.594373
12	34	3	2017-08-17 13:44:22.594373
13	3	1	2017-08-15 13:44:22.594373
14	3	2	2017-08-16 13:44:22.594373
15	3	3	2017-08-17 13:44:22.594373
16	3	8	2017-08-17 13:44:22.594373
17	3	3	2017-08-15 13:44:22.594373
18	3	4	2017-08-15 13:44:22.594373
19	3	5	2017-08-16 13:44:22.594373
20	3	6	2017-08-16 13:44:22.594373
21	3	9	2017-08-17 13:44:22.594373
22	3	8	2017-08-17 13:44:22.594373
23	2	4	2017-08-15 13:44:22.594373
24	2	5	2017-08-15 13:44:22.594373
25	2	6	2017-08-16 13:44:22.594373
26	2	9	2017-08-16 13:44:22.594373
27	2	7	2017-08-17 13:44:22.594373
28	2	10	2017-08-17 13:44:22.594373
29	2	8	2017-08-17 13:44:22.594373
30	2	11	2017-08-17 13:44:22.594373
31	2	12	2017-08-17 13:44:22.594373
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
1	18	7	\N	2017-08-17 13:44:22.477856	t	2	f
2	19	22	\N	2017-08-17 13:44:22.478014	t	1	f
3	20	\N	20	2017-08-17 13:44:22.478155	t	2	f
4	21	\N	7	2017-08-17 13:44:22.478291	f	1	f
5	22	\N	13	2017-08-17 13:44:22.478424	f	1	f
6	23	\N	30	2017-08-17 13:44:22.478559	f	1	f
7	24	7	\N	2017-08-17 13:44:22.47869	f	1	f
8	25	29	\N	2017-08-17 13:44:22.478824	f	1	f
9	26	27	\N	2017-08-17 13:44:22.478953	f	2	f
10	27	1	\N	2017-08-17 13:44:22.479085	t	1	f
\.


--
-- Name: review_deletes_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('review_deletes_uid_seq', 10, true);


--
-- Data for Name: review_duplicates; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY review_duplicates (uid, detector_uid, duplicate_statement_uid, original_statement_uid, "timestamp", is_executed, is_revoked) FROM stdin;
1	28	6	1	2017-08-17 13:44:22.479231	f	f
2	29	4	1	2017-08-17 13:44:22.479372	t	f
3	29	22	7	2017-08-17 13:44:22.479495	f	f
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
1	3	\N	2	2017-08-17 13:44:22.62162	f	f
\.


--
-- Name: review_edits_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('review_edits_uid_seq', 1, true);


--
-- Data for Name: review_merge; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY review_merge (uid, detector_uid, premisesgroup_uid, "timestamp", is_executed, is_revoked) FROM stdin;
1	31	1	2017-08-17 13:44:22.479629	f	f
2	32	5	2017-08-17 13:44:22.479748	f	f
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
1	12	8	\N	2017-08-17 13:44:22.476924	t	f
2	13	\N	23	2017-08-17 13:44:22.477135	t	f
3	14	\N	28	2017-08-17 13:44:22.477285	f	f
4	16	7	\N	2017-08-17 13:44:22.477548	f	f
5	17	28	\N	2017-08-17 13:44:22.477682	f	f
6	15	\N	26	2017-08-17 13:44:22.477416	f	f
\.


--
-- Name: review_optimizations_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('review_optimizations_uid_seq', 6, true);


--
-- Data for Name: review_split; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY review_split (uid, detector_uid, premisesgroup_uid, "timestamp", is_executed, is_revoked) FROM stdin;
1	33	10	2017-08-17 13:44:22.479882	f	f
2	34	12	2017-08-17 13:44:22.480008	f	f
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
1108	1	10
1109	1	27
1110	1	15
1111	1	14
1112	1	29
1113	1	32
1114	1	7
1115	2	9
1116	2	17
1117	2	12
1118	2	25
1119	2	28
1120	2	8
1121	2	19
1122	2	23
1123	2	32
1124	2	29
1125	2	22
1126	2	16
1127	2	14
1128	2	26
1129	3	27
1130	3	9
1131	3	24
1132	3	13
1133	3	14
1134	3	23
1135	3	31
1136	3	25
1137	3	33
1138	3	11
1139	3	32
1140	3	35
1141	3	26
1142	3	21
1143	3	36
1144	3	12
1145	3	34
1146	4	29
1147	4	33
1148	4	16
1149	4	20
1150	4	10
1151	4	7
1152	4	8
1153	4	18
1154	4	34
1155	4	13
1156	4	35
1157	4	9
1158	4	32
1159	4	17
1160	4	25
1161	5	19
1162	5	14
1163	5	32
1164	5	13
1165	5	37
1166	5	27
1167	5	28
1168	5	7
1169	5	31
1170	5	15
1171	5	35
1172	5	10
1173	5	25
1174	5	29
1175	5	26
1176	5	12
1177	8	17
1178	8	19
1179	8	21
1180	8	20
1181	8	33
1182	8	28
1183	8	7
1184	8	32
1185	8	12
1186	8	34
1187	8	29
1188	8	29
1189	8	9
1190	10	16
1191	10	35
1192	10	22
1193	10	10
1194	10	23
1195	10	33
1196	10	13
1197	10	29
1198	11	25
1199	11	13
1200	11	9
1201	11	29
1202	11	12
1203	11	15
1204	11	35
1205	11	36
1206	11	29
1207	11	11
1208	11	17
1209	11	34
1210	11	20
1211	11	32
1212	11	18
1213	11	24
1214	11	27
1215	11	22
1216	11	28
1217	11	26
1218	11	33
1219	11	23
1220	11	37
1221	11	31
1222	11	14
1223	11	21
1224	12	21
1225	12	37
1226	12	19
1227	12	29
1228	12	35
1229	12	28
1230	12	33
1231	12	18
1232	12	9
1233	12	36
1234	12	7
1235	12	34
1236	12	11
1237	12	8
1238	12	25
1239	12	17
1240	12	27
1241	12	26
1242	12	16
1243	15	16
1244	15	14
1245	15	19
1246	15	8
1247	15	24
1248	15	37
1249	15	11
1250	16	27
1251	16	9
1252	16	26
1253	16	25
1254	16	29
1255	16	28
1256	16	20
1257	16	23
1258	16	36
1259	17	28
1260	17	37
1261	17	17
1262	17	29
1263	17	23
1264	17	34
1265	17	18
1266	17	35
1267	17	20
1268	19	25
1269	19	36
1270	19	28
1271	19	7
1272	19	18
1273	19	26
1274	19	35
1275	19	22
1276	19	19
1277	19	15
1278	19	9
1279	19	27
1280	19	16
1281	19	23
1282	19	24
1283	19	11
1284	19	33
1285	19	21
1286	19	32
1287	19	29
1288	19	12
1289	19	10
1290	19	31
1291	20	32
1292	20	25
1293	20	7
1294	20	21
1295	20	14
1296	20	29
1297	20	26
1298	20	24
1299	20	17
1300	20	20
1301	20	34
1302	20	29
1303	20	11
1304	20	35
1305	20	36
1306	20	9
1307	20	28
1308	20	33
1309	20	18
1310	20	22
1311	20	27
1312	20	37
1313	20	31
1314	20	16
1315	20	8
1316	20	19
1317	20	13
1318	20	15
1319	20	23
1320	21	32
1321	21	9
1322	21	29
1323	21	14
1324	21	34
1325	21	11
1326	23	19
1327	23	36
1328	23	9
1329	23	26
1330	23	37
1331	23	20
1332	23	28
1333	23	18
1334	23	12
1335	23	29
1336	23	7
1337	23	29
1338	23	25
1339	23	32
1340	23	16
1341	23	34
1342	23	23
1343	24	21
1344	24	35
1345	24	32
1346	24	15
1347	24	37
1348	24	25
1349	24	27
1350	24	34
1351	24	8
1352	24	7
1353	24	13
1354	24	24
1355	24	10
1356	24	29
1357	24	14
1358	24	17
1359	24	26
1360	24	28
1361	24	31
1362	24	19
1363	24	33
1364	24	23
1365	26	24
1366	26	19
1367	26	11
1368	26	13
1369	26	7
1370	26	34
1371	26	22
1372	26	27
1373	26	25
1374	26	17
1375	27	8
1376	27	15
1377	27	29
1378	27	31
1379	27	10
1380	27	11
1381	27	9
1382	27	35
1383	27	34
1384	27	36
1385	27	33
1386	27	12
1387	27	29
1388	27	20
1389	27	14
1390	27	7
1391	27	22
1392	27	28
1393	27	18
1394	27	19
1395	27	24
1396	27	26
1397	27	23
1398	27	27
1399	28	37
1400	28	35
1401	28	20
1402	28	28
1403	28	21
1404	28	29
1405	28	15
1406	28	9
1407	28	36
1408	28	14
1409	28	34
1410	28	11
1411	28	10
1412	28	24
1413	28	26
1414	28	22
1415	29	28
1416	29	24
1417	29	10
1418	29	29
1419	29	19
1420	29	22
1421	29	26
1422	29	16
1423	29	13
1424	29	33
1425	29	36
1426	29	17
1427	29	21
1428	29	23
1429	29	35
1430	29	29
1431	29	25
1432	29	37
1433	29	12
1434	29	15
1435	29	11
1436	29	18
1437	29	34
1438	29	7
1439	29	8
1440	30	19
1441	30	23
1442	30	36
1443	30	22
1444	30	12
1445	30	21
1446	30	15
1447	30	8
1448	30	11
1449	30	24
1450	30	25
1451	30	14
1452	30	37
1453	30	26
1454	32	37
1455	32	33
1456	32	17
1457	32	27
1458	32	20
1459	32	28
1460	32	23
1461	32	15
1462	32	36
1463	32	29
1464	32	22
1465	32	14
1466	32	10
1467	32	11
1468	32	19
1469	32	26
1470	32	12
1471	32	24
1472	34	10
1473	34	18
1474	34	35
1475	34	23
1476	34	9
1477	34	12
1478	34	24
1479	34	37
1480	35	23
1481	35	16
1482	35	15
1483	35	10
1484	35	19
1485	35	22
1486	35	18
1487	35	25
1488	35	32
1489	35	11
1490	35	9
1491	35	33
1492	35	14
1493	36	10
1494	36	11
1495	36	28
1496	36	26
1497	36	9
1498	36	21
1499	36	35
1500	36	34
1501	36	15
1502	36	29
1503	36	7
1504	36	19
1505	36	18
1506	36	25
1507	36	37
1508	36	31
1509	36	8
1510	36	17
1511	36	33
1512	36	12
1513	36	24
1514	39	20
1515	39	21
1516	39	26
1517	39	16
1518	40	27
1519	40	13
1520	40	33
1521	40	31
1522	40	8
1523	40	18
1524	40	10
1525	40	16
1526	40	32
1527	40	14
1528	40	37
1529	40	19
1530	40	15
1531	40	29
1532	40	22
1533	40	11
1534	40	12
1535	40	35
1536	40	34
1537	40	25
1538	40	9
1539	40	26
1540	40	24
1541	40	36
1542	41	8
1543	41	13
1544	41	36
1545	41	19
1546	41	15
1547	41	25
1548	41	31
1549	41	9
1550	41	7
1551	41	22
1552	41	35
1553	41	26
1554	41	37
1555	41	27
1556	41	24
1557	41	12
1558	41	16
1559	41	29
1560	42	12
1561	42	27
1562	42	23
1563	42	14
1564	42	17
1565	42	13
1566	42	25
1567	42	37
1568	42	22
1569	42	11
1570	42	29
1571	42	10
1572	42	20
1573	42	33
1574	42	18
1575	42	34
1576	42	26
1577	42	36
1578	42	24
1579	42	35
1580	42	19
1581	42	32
1582	42	21
1583	42	9
1584	42	31
1585	42	29
1586	42	28
1587	44	16
1588	44	24
1589	44	13
1590	44	12
1591	44	7
1592	44	9
1593	44	15
1594	46	37
1595	46	8
1596	46	34
1597	46	23
1598	46	21
1599	46	28
1600	46	12
1601	46	9
1602	46	22
1603	46	15
1604	46	10
1605	46	31
1606	46	18
1607	46	27
1608	46	14
1609	46	29
1610	46	7
1611	46	25
1612	46	29
1613	46	36
1614	46	33
1615	46	17
1616	46	11
1617	46	19
1618	46	20
1619	46	26
1620	46	35
1621	47	10
1622	47	36
1623	47	34
1624	47	8
1625	47	9
1626	47	24
1627	47	17
1628	47	18
1629	47	33
1630	47	28
1631	47	29
1632	47	14
1633	47	27
1634	47	37
1635	47	16
1636	47	31
1637	47	32
1638	47	19
1639	47	13
1640	47	23
1641	47	12
1642	47	21
1643	47	7
1644	47	29
1645	47	20
1646	47	26
1647	47	22
1648	47	25
1649	47	11
1650	49	11
1651	49	8
1652	49	36
1653	49	19
1654	49	35
1655	49	9
1656	49	31
1657	49	16
1658	49	15
1659	49	12
1660	49	25
1661	49	22
1662	49	37
1663	49	32
1664	49	7
1665	49	28
1666	49	33
1667	49	26
1668	49	18
1669	49	13
1670	49	20
1671	50	23
1672	50	16
1673	50	28
1674	50	19
1675	50	7
1676	50	12
1677	50	31
1678	50	14
1679	50	10
1680	50	34
1681	50	26
1682	50	9
1683	50	27
1684	51	25
1685	51	20
1686	51	27
1687	51	13
1688	51	23
1689	51	19
1690	51	9
1691	51	26
1692	51	35
1693	51	11
1694	51	34
1695	51	21
1696	51	8
1697	51	28
1698	51	31
1699	51	32
1700	54	11
1701	54	29
1702	54	20
1703	54	23
1704	54	13
1705	55	19
1706	55	14
1707	55	35
1708	55	13
1709	55	9
1710	55	28
1711	55	37
1712	55	36
1713	55	23
1714	55	31
1715	55	29
1716	55	16
1717	55	32
1718	55	20
1719	55	27
1720	55	8
1721	55	24
1722	55	22
1723	55	25
1724	55	33
1725	55	11
1726	55	29
1727	55	15
1728	55	34
1729	55	21
1730	55	26
1731	55	7
1732	56	18
1733	56	35
1734	56	36
1735	56	20
1736	56	34
1737	56	7
1738	56	27
1739	56	9
1740	56	8
1741	56	23
1742	56	29
1743	56	33
1744	56	12
1745	56	25
1746	56	22
1747	56	13
1748	56	26
1749	56	32
1750	56	15
1751	56	16
1752	56	21
1753	56	19
1754	56	17
1755	56	28
1756	57	29
1757	57	21
1758	57	23
1759	57	22
1760	57	8
1761	57	14
1762	57	13
1763	57	19
1764	57	35
1765	57	31
1766	57	20
1767	57	7
1768	57	25
1769	57	16
1770	58	20
1771	58	27
1772	58	35
1773	58	34
1774	58	33
1775	58	18
1776	58	31
1777	59	25
1778	59	34
1779	59	7
1780	59	22
1781	59	27
1782	59	24
1783	59	19
1784	59	10
1785	59	12
1786	59	18
1787	59	28
1788	59	8
1789	59	31
1790	59	14
1791	59	9
1792	59	16
1793	60	33
1794	60	21
1795	60	22
1796	60	36
1797	60	16
1798	60	37
1799	60	28
1800	60	10
1801	60	24
1802	60	12
1803	60	18
1804	60	7
1805	60	14
1806	61	18
1807	61	12
1808	61	10
1809	61	29
1810	61	27
1811	61	8
1812	61	15
1813	61	31
1814	61	7
1815	61	28
1816	61	11
1817	61	16
1818	61	33
1819	61	23
1820	61	19
1821	61	26
1822	61	17
1823	61	25
1824	61	37
1825	61	13
1826	61	14
1827	61	35
1828	61	29
1829	61	34
1830	61	20
1831	61	32
1832	61	24
1833	61	9
1834	61	21
1835	62	23
1836	62	32
1837	62	29
1838	62	8
1839	63	28
1840	63	29
1841	63	15
1842	63	19
1843	63	16
1844	63	33
1845	63	24
1846	63	21
1847	63	8
1848	63	7
1849	63	32
1850	63	23
1851	63	14
1852	63	29
1853	63	31
1854	63	18
1855	63	13
1856	63	37
1857	63	34
1858	63	12
1859	63	36
1860	63	27
1861	64	28
1862	64	35
1863	64	14
1864	64	32
1865	64	20
1866	64	24
1867	64	25
1868	64	34
1869	64	21
1870	64	36
1871	64	8
1872	64	11
1873	64	17
1874	64	7
1875	65	26
1876	65	19
1877	65	28
1878	65	16
1879	65	11
1880	65	25
1881	65	15
1882	65	37
1883	65	14
1884	65	12
1885	66	29
1886	66	13
1887	66	29
1888	66	15
1889	66	25
1890	66	26
1891	66	37
1892	66	31
1893	66	33
1894	66	9
1895	66	17
1896	66	23
1897	66	8
1898	66	28
1899	66	19
1900	66	18
1901	66	22
1902	67	22
1903	67	31
1904	67	13
1905	67	29
1906	67	21
1907	67	16
1908	67	24
1909	67	7
1910	67	20
1911	67	25
1912	67	28
1913	67	23
1914	67	17
1915	67	27
1916	67	33
1917	67	8
1918	67	26
1919	67	9
1920	67	35
1921	67	10
1922	67	18
1923	67	14
1924	67	37
1925	68	26
1926	68	21
1927	68	33
1928	68	17
1929	68	16
1930	6	21
1931	6	29
1932	6	31
1933	6	15
1934	6	24
1935	6	27
1936	6	36
1937	6	26
1938	6	10
1939	6	37
1940	6	25
1941	6	34
1942	6	35
1943	6	16
1944	6	29
1945	6	23
1946	6	7
1947	6	13
1948	6	32
1949	6	12
1950	6	19
1951	7	18
1952	7	29
1953	7	32
1954	7	12
1955	7	7
1956	7	31
1957	7	28
1958	7	11
1959	7	23
1960	7	29
1961	7	37
1962	7	27
1963	7	36
1964	9	35
1965	9	24
1966	9	31
1967	9	21
1968	9	13
1969	9	27
1970	9	9
1971	9	16
1972	9	15
1973	9	26
1974	9	19
1975	9	20
1976	9	17
1977	9	29
1978	9	7
1979	9	37
1980	13	21
1981	13	22
1982	13	8
1983	13	15
1984	13	19
1985	13	14
1986	13	7
1987	13	11
1988	13	26
1989	13	12
1990	13	23
1991	13	24
1992	14	9
1993	14	19
1994	14	20
1995	14	35
1996	14	11
1997	14	12
1998	14	15
1999	14	34
2000	14	21
2001	14	37
2002	14	36
2003	14	7
2004	18	12
2005	18	24
2006	18	13
2007	18	21
2008	18	35
2009	18	18
2010	18	9
2011	18	26
2012	18	16
2013	18	32
2014	18	20
2015	18	14
2016	18	27
2017	18	25
2018	18	34
2019	18	10
2020	18	33
2021	18	8
2022	18	19
2023	18	23
2024	18	29
2025	18	28
2026	18	17
2027	18	7
2028	18	22
2029	18	36
2030	18	15
2031	18	37
2032	18	29
2033	22	7
2034	22	19
2035	22	14
2036	22	11
2037	22	28
2038	22	24
2039	22	37
2040	22	26
2041	22	25
2042	22	29
2043	22	33
2044	22	20
2045	22	16
2046	22	34
2047	22	35
2048	22	32
2049	22	10
2050	22	9
2051	22	21
2052	22	36
2053	22	22
2054	22	31
2055	22	12
2056	22	13
2057	22	23
2058	22	17
2059	22	15
2060	22	18
2061	22	29
2062	25	36
2063	25	37
2064	25	12
2065	25	16
2066	25	35
2067	25	11
2068	25	21
2069	25	29
2070	25	34
2071	25	17
2072	25	13
2073	31	29
2074	31	10
2075	31	37
2076	31	18
2077	33	33
2078	33	37
2079	33	35
2080	33	24
2081	33	29
2082	33	25
2083	33	7
2084	33	26
2085	33	18
2086	33	16
2087	33	15
2088	33	13
2089	33	29
2090	37	14
2091	37	23
2092	37	20
2093	37	21
2094	37	31
2095	37	32
2096	37	15
2097	37	33
2098	37	29
2099	37	18
2100	37	25
2101	37	29
2102	37	34
2103	38	13
2104	38	26
2105	38	34
2106	38	18
2107	38	27
2108	43	22
2109	43	10
2110	43	29
2111	43	14
2112	43	34
2113	43	35
2114	43	18
2115	45	21
2116	45	34
2117	45	25
2118	45	18
2119	45	16
2120	45	31
2121	45	36
2122	45	35
2123	45	12
2124	45	20
2125	45	28
2126	45	26
2127	45	33
2128	45	32
2129	45	15
2130	45	19
2131	45	24
2132	45	9
2133	45	37
2134	45	29
2135	45	29
2136	45	7
2137	45	22
2138	45	11
2139	45	27
2140	45	10
2141	45	8
2142	48	11
2143	48	29
2144	48	25
2145	48	7
2146	48	12
2147	48	36
2148	48	31
2149	48	24
2150	48	21
2151	48	32
2152	48	34
2153	48	19
2154	48	35
2155	48	15
2156	48	23
2157	48	10
2158	48	29
2159	48	37
2160	48	26
2161	48	28
2162	52	31
2163	52	10
2164	52	16
2165	52	8
2166	52	24
2167	52	33
2168	52	13
2169	52	22
2170	52	36
2171	52	29
2172	52	32
2173	52	20
2174	52	29
2175	52	18
2176	52	7
2177	52	11
2178	52	15
2179	52	14
2180	52	25
2181	52	27
2182	52	17
2183	52	12
2184	52	35
2185	52	19
2186	52	21
2187	53	24
2188	53	7
2189	53	25
2190	53	19
2191	53	8
2192	53	12
2193	53	27
2194	53	31
2195	53	9
2196	53	36
2197	53	20
2198	53	22
2199	53	37
2200	69	23
2201	69	22
2202	69	36
2203	69	33
2204	69	25
2205	69	35
2206	69	29
2207	69	21
2208	69	15
2209	69	10
2210	69	24
2211	69	27
2212	69	19
2213	69	37
\.


--
-- Name: seen_arguments_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('seen_arguments_uid_seq', 2213, true);


--
-- Data for Name: seen_statements; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY seen_statements (uid, statement_uid, user_uid) FROM stdin;
1521	1	10
1522	1	7
1523	1	37
1524	1	32
1525	1	24
1526	1	29
1527	1	12
1528	1	18
1529	1	26
1530	1	14
1531	1	22
1532	1	21
1533	1	28
1534	1	15
1535	1	9
1536	1	29
1537	1	20
1538	1	35
1539	1	8
1540	1	33
1541	1	27
1542	1	36
1543	1	11
1544	2	14
1545	2	37
1546	2	29
1547	2	28
1548	2	19
1549	2	8
1550	2	27
1551	2	13
1552	2	11
1553	2	25
1554	2	32
1555	2	12
1556	2	18
1557	2	17
1558	2	21
1559	2	35
1560	2	31
1561	2	10
1562	2	29
1563	2	33
1564	2	23
1565	2	20
1566	2	34
1567	2	36
1568	2	9
1569	2	7
1570	3	26
1571	3	29
1572	3	13
1573	3	9
1574	3	8
1575	3	31
1576	3	27
1577	3	34
1578	3	23
1579	3	21
1580	3	19
1581	3	20
1582	3	33
1583	3	24
1584	3	28
1585	3	32
1586	3	36
1587	4	21
1588	4	17
1589	4	11
1590	4	31
1591	5	27
1592	5	21
1593	5	13
1594	5	29
1595	5	31
1596	5	23
1597	5	20
1598	5	17
1599	5	9
1600	6	10
1601	6	22
1602	6	8
1603	6	34
1604	6	19
1605	6	18
1606	6	14
1607	6	29
1608	6	36
1609	6	12
1610	6	29
1611	6	32
1612	6	27
1613	6	25
1614	6	28
1615	6	16
1616	6	31
1617	6	33
1618	6	17
1619	6	11
1620	6	26
1621	6	37
1622	6	21
1623	6	35
1624	7	23
1625	7	13
1626	7	7
1627	7	25
1628	7	36
1629	7	18
1630	7	15
1631	7	14
1632	7	26
1633	7	35
1634	7	29
1635	7	31
1636	7	22
1637	7	21
1638	7	37
1639	7	20
1640	8	14
1641	8	10
1642	8	18
1643	8	22
1644	8	33
1645	8	34
1646	8	37
1647	8	15
1648	8	27
1649	8	23
1650	8	9
1651	8	20
1652	8	35
1653	8	28
1654	8	17
1655	8	32
1656	8	29
1657	8	11
1658	8	21
1659	8	31
1660	8	24
1661	8	16
1662	8	29
1663	9	21
1664	9	29
1665	9	28
1666	9	18
1667	9	26
1668	9	22
1669	9	20
1670	9	7
1671	9	11
1672	9	27
1673	9	37
1674	9	36
1675	9	33
1676	10	36
1677	10	34
1678	10	22
1679	10	11
1680	10	8
1681	10	37
1682	10	26
1683	10	29
1684	10	15
1685	10	24
1686	10	20
1687	10	7
1688	10	10
1689	10	31
1690	10	35
1691	10	27
1692	10	28
1693	10	13
1694	10	14
1695	10	18
1696	10	17
1697	11	22
1698	11	32
1699	11	33
1700	11	19
1701	11	21
1702	11	9
1703	11	15
1704	11	12
1705	11	34
1706	11	36
1707	11	13
1708	11	7
1709	11	14
1710	11	18
1711	11	35
1712	11	25
1713	11	26
1714	11	20
1715	11	17
1716	11	37
1717	11	29
1718	11	11
1719	11	29
1720	12	13
1721	12	29
1722	12	37
1723	12	29
1724	12	20
1725	12	7
1726	12	23
1727	12	8
1728	12	24
1729	12	21
1730	12	27
1731	12	12
1732	12	11
1733	13	27
1734	13	35
1735	13	8
1736	13	11
1737	13	36
1738	13	26
1739	13	13
1740	13	9
1741	13	15
1742	13	32
1743	13	28
1744	13	34
1745	13	17
1746	13	25
1747	13	14
1748	13	19
1749	13	10
1750	13	21
1751	13	16
1752	13	7
1753	13	18
1754	13	37
1755	13	12
1756	13	31
1757	14	28
1758	14	20
1759	14	12
1760	14	35
1761	14	37
1762	14	19
1763	14	15
1764	14	13
1765	14	9
1766	14	33
1767	14	34
1768	14	8
1769	14	17
1770	14	29
1771	14	21
1772	14	7
1773	14	10
1774	14	36
1775	14	16
1776	15	18
1777	15	23
1778	15	31
1779	15	25
1780	15	33
1781	15	15
1782	15	35
1783	15	29
1784	16	14
1785	16	27
1786	16	20
1787	16	13
1788	16	19
1789	16	16
1790	16	37
1791	16	29
1792	16	21
1793	16	17
1794	16	32
1795	16	28
1796	16	9
1797	16	7
1798	16	10
1799	16	11
1800	16	8
1801	16	33
1802	16	22
1803	17	10
1804	17	7
1805	17	17
1806	17	37
1807	17	14
1808	17	33
1809	17	15
1810	17	18
1811	17	19
1812	17	20
1813	17	22
1814	17	31
1815	17	35
1816	17	23
1817	17	25
1818	17	26
1819	17	24
1820	17	21
1821	17	36
1822	17	34
1823	17	9
1824	17	28
1825	18	37
1826	18	17
1827	18	18
1828	18	29
1829	18	28
1830	18	25
1831	18	26
1832	18	21
1833	18	15
1834	18	19
1835	18	36
1836	18	12
1837	18	27
1838	18	33
1839	18	32
1840	18	9
1841	18	13
1842	18	10
1843	18	7
1844	18	24
1845	18	20
1846	18	14
1847	19	12
1848	19	22
1849	19	31
1850	19	20
1851	19	7
1852	19	10
1853	19	25
1854	19	18
1855	19	24
1856	19	16
1857	19	19
1858	19	11
1859	19	33
1860	19	34
1861	19	32
1862	19	8
1863	19	21
1864	19	26
1865	19	27
1866	19	35
1867	19	17
1868	19	13
1869	19	36
1870	19	14
1871	19	29
1872	19	23
1873	19	15
1874	20	35
1875	20	25
1876	20	12
1877	20	10
1878	20	9
1879	20	23
1880	20	16
1881	20	28
1882	21	34
1883	21	15
1884	21	35
1885	21	27
1886	21	23
1887	21	36
1888	22	11
1889	22	28
1890	22	33
1891	22	16
1892	22	8
1893	22	24
1894	23	29
1895	23	22
1896	23	20
1897	23	25
1898	23	13
1899	23	32
1900	23	7
1901	23	21
1902	23	17
1903	23	27
1904	23	37
1905	23	26
1906	23	33
1907	23	9
1908	24	24
1909	24	27
1910	24	15
1911	24	33
1912	24	29
1913	24	7
1914	24	25
1915	24	10
1916	24	29
1917	24	32
1918	24	14
1919	24	28
1920	24	19
1921	24	37
1922	24	35
1923	24	22
1924	24	23
1925	24	8
1926	24	36
1927	24	18
1928	24	11
1929	24	9
1930	24	17
1931	24	13
1932	24	26
1933	24	31
1934	25	7
1935	25	36
1936	25	10
1937	25	34
1938	25	28
1939	25	19
1940	25	37
1941	25	9
1942	26	16
1943	26	19
1944	26	22
1945	26	20
1946	26	27
1947	26	35
1948	26	21
1949	26	29
1950	26	18
1951	26	23
1952	26	37
1953	26	17
1954	26	31
1955	26	11
1956	26	13
1957	26	9
1958	26	32
1959	26	26
1960	26	34
1961	27	20
1962	27	7
1963	27	8
1964	27	37
1965	27	9
1966	27	12
1967	27	22
1968	27	24
1969	27	17
1970	27	33
1971	27	28
1972	27	34
1973	27	32
1974	27	18
1975	27	31
1976	27	14
1977	27	15
1978	27	23
1979	27	36
1980	27	11
1981	27	10
1982	27	27
1983	27	19
1984	28	34
1985	28	24
1986	28	19
1987	28	23
1988	28	9
1989	28	11
1990	28	8
1991	28	10
1992	28	17
1993	28	31
1994	28	12
1995	28	21
1996	28	26
1997	28	20
1998	28	7
1999	28	36
2000	29	25
2001	29	33
2002	29	26
2003	29	13
2004	29	10
2005	29	16
2006	29	22
2007	29	20
2008	29	15
2009	29	29
2010	29	24
2011	29	28
2012	29	17
2013	29	12
2014	29	7
2015	29	8
2016	29	34
2017	29	35
2018	29	36
2019	29	27
2020	29	23
2021	29	29
2022	29	21
2023	30	29
2024	30	16
2025	30	23
2026	30	11
2027	30	34
2028	30	14
2029	30	13
2030	30	18
2031	30	8
2032	30	17
2033	30	33
2034	30	12
2035	30	27
2036	30	19
2037	30	21
2038	30	15
2039	30	32
2040	30	31
2041	30	9
2042	30	22
2043	30	24
2044	30	10
2045	30	28
2046	30	37
2047	30	35
2048	30	7
2049	30	25
2050	31	14
2051	31	37
2052	31	20
2053	31	21
2054	31	24
2055	31	18
2056	31	29
2057	31	8
2058	31	36
2059	31	33
2060	31	23
2061	31	31
2062	31	9
2063	31	28
2064	31	34
2065	31	27
2066	31	17
2067	31	10
2068	31	19
2069	31	15
2070	31	7
2071	31	25
2072	31	16
2073	31	12
2074	31	35
2075	31	13
2076	31	22
2077	31	26
2078	31	11
2079	32	26
2080	32	12
2081	32	24
2082	32	7
2083	32	20
2084	32	31
2085	32	23
2086	32	13
2087	32	19
2088	32	15
2089	32	17
2090	32	22
2091	32	36
2092	33	37
2093	33	36
2094	33	26
2095	33	23
2096	33	31
2097	33	9
2098	33	19
2099	34	29
2100	34	8
2101	34	13
2102	34	20
2103	34	27
2104	34	7
2105	34	34
2106	34	19
2107	34	18
2108	34	28
2109	34	25
2110	34	36
2111	34	15
2112	34	12
2113	34	33
2114	35	13
2115	35	14
2116	35	11
2117	35	23
2118	36	18
2119	36	24
2120	36	35
2121	36	15
2122	36	36
2123	36	27
2124	36	11
2125	36	23
2126	36	25
2127	36	32
2128	36	26
2129	36	10
2130	36	16
2131	36	21
2132	36	19
2133	36	33
2134	36	29
2135	36	22
2136	36	31
2137	36	34
2138	36	13
2139	36	29
2140	36	8
2141	36	7
2142	37	31
2143	37	27
2144	37	24
2145	37	28
2146	37	23
2147	37	12
2148	37	33
2149	37	10
2150	37	14
2151	37	36
2152	37	19
2153	37	26
2154	37	8
2155	37	34
2156	37	35
2157	37	7
2158	37	29
2159	37	29
2160	37	15
2161	37	37
2162	37	13
2163	37	25
2164	37	20
2165	37	22
2166	37	17
2167	38	33
2168	38	8
2169	38	23
2170	38	16
2171	38	18
2172	38	26
2173	38	13
2174	38	29
2175	38	12
2176	38	14
2177	39	36
2178	39	21
2179	39	20
2180	39	19
2181	39	34
2182	39	28
2183	39	27
2184	39	22
2185	39	24
2186	39	15
2187	39	12
2188	39	14
2189	39	35
2190	40	36
2191	40	26
2192	40	29
2193	40	11
2194	40	20
2195	40	8
2196	40	27
2197	40	31
2198	40	19
2199	40	9
2200	40	33
2201	40	35
2202	40	17
2203	40	22
2204	40	12
2205	40	10
2206	40	24
2207	40	29
2208	40	34
2209	40	28
2210	40	23
2211	40	32
2212	40	16
2213	40	21
2214	40	7
2215	40	37
2216	40	18
2217	41	19
2218	41	27
2219	41	21
2220	41	22
2221	41	28
2222	41	34
2223	41	10
2224	41	35
2225	41	8
2226	41	16
2227	41	11
2228	41	33
2229	41	7
2230	41	14
2231	41	23
2232	41	24
2233	41	18
2234	41	26
2235	41	31
2236	41	36
2237	41	25
2238	41	29
2239	41	29
2240	42	24
2241	42	19
2242	42	29
2243	42	20
2244	42	16
2245	42	11
2246	42	15
2247	42	28
2248	42	17
2249	42	37
2250	42	12
2251	42	36
2252	42	8
2253	42	10
2254	42	34
2255	42	23
2256	42	25
2257	42	26
2258	42	7
2259	42	27
2260	42	14
2261	43	25
2262	43	28
2263	43	17
2264	43	16
2265	43	19
2266	43	21
2267	43	34
2268	43	32
2269	43	37
2270	43	15
2271	44	32
2272	44	18
2273	44	37
2274	44	36
2275	44	28
2276	44	12
2277	44	33
2278	44	25
2279	44	16
2280	44	29
2281	44	9
2282	44	11
2283	44	29
2284	45	28
2285	45	29
2286	45	23
2287	45	27
2288	45	26
2289	45	31
2290	45	14
2291	45	19
2292	45	22
2293	45	36
2294	45	20
2295	45	7
2296	45	15
2297	45	24
2298	45	18
2299	45	37
2300	45	16
2301	45	25
2302	45	11
2303	45	13
2304	45	17
2305	45	8
2306	45	34
2307	45	10
2308	46	20
2309	46	31
2310	46	22
2311	46	25
2312	46	19
2313	46	35
2314	46	21
2315	46	16
2316	46	12
2317	46	29
2318	46	33
2319	46	9
2320	46	15
2321	46	23
2322	46	28
2323	46	32
2324	46	8
2325	46	37
2326	46	14
2327	46	26
2328	46	36
2329	46	11
2330	46	7
2331	47	27
2332	47	7
2333	47	19
2334	47	15
2335	47	11
2336	47	14
2337	47	32
2338	47	17
2339	47	18
2340	47	37
2341	47	29
2342	47	16
2343	47	13
2344	47	9
2345	47	35
2346	47	29
2347	47	25
2348	47	12
2349	47	33
2350	47	20
2351	47	31
2352	47	28
2353	48	22
2354	48	29
2355	48	33
2356	48	13
2357	48	19
2358	48	36
2359	48	7
2360	48	26
2361	48	27
2362	48	10
2363	48	11
2364	48	15
2365	48	34
2366	48	25
2367	48	28
2368	48	37
2369	48	18
2370	48	32
2371	49	31
2372	49	19
2373	49	32
2374	49	21
2375	49	22
2376	49	34
2377	49	29
2378	49	10
2379	49	17
2380	49	14
2381	49	12
2382	49	27
2383	49	9
2384	49	13
2385	49	18
2386	50	27
2387	50	14
2388	50	22
2389	50	18
2390	50	17
2391	50	13
2392	50	33
2393	50	37
2394	50	35
2395	50	34
2396	50	8
2397	50	29
2398	50	21
2399	50	36
2400	50	11
2401	50	32
2402	50	10
2403	50	7
2404	50	20
2405	50	15
2406	50	28
2407	50	26
2408	50	24
2409	50	23
2410	50	19
2411	50	31
2412	51	25
2413	51	21
2414	51	34
2415	51	28
2416	51	29
2417	51	17
2418	51	11
2419	51	10
2420	51	36
2421	51	29
2422	51	19
2423	51	27
2424	51	23
2425	51	15
2426	51	12
2427	51	35
2428	51	24
2429	51	31
2430	51	7
2431	51	8
2432	51	16
2433	51	9
2434	51	32
2435	51	20
2436	51	37
2437	52	14
2438	52	35
2439	52	7
2440	52	37
2441	52	24
2442	52	23
2443	52	11
2444	53	9
2445	53	12
2446	53	23
2447	53	21
2448	53	29
2449	53	14
2450	53	18
2451	53	29
2452	53	19
2453	53	26
2454	53	24
2455	53	37
2456	53	36
2457	53	15
2458	53	16
2459	53	35
2460	53	11
2461	53	20
2462	53	7
2463	53	28
2464	53	8
2465	54	37
2466	54	20
2467	54	23
2468	54	33
2469	55	11
2470	55	25
2471	55	24
2472	55	21
2473	55	33
2474	55	31
2475	55	35
2476	55	23
2477	56	32
2478	56	19
2479	56	17
2480	56	29
2481	56	14
2482	56	28
2483	56	31
2484	56	10
2485	56	18
2486	56	26
2487	56	36
2488	56	27
2489	56	16
2490	56	22
2491	56	8
2492	57	21
2493	57	25
2494	57	32
2495	57	17
2496	57	7
2497	57	29
2498	57	9
2499	57	16
2500	57	10
2501	57	12
2502	57	33
2503	57	34
2504	57	20
2505	57	28
2506	57	35
2507	57	27
2508	57	26
2509	57	11
2510	57	13
2511	57	19
2512	57	14
2513	58	31
2514	58	19
2515	58	10
2516	58	18
2517	58	9
2518	58	14
2519	59	10
2520	59	34
2521	59	16
2522	59	21
2523	59	20
2524	59	37
2525	59	36
2526	59	24
2527	59	29
2528	59	19
2529	59	15
2530	59	14
2531	59	28
2532	60	28
2533	60	19
2534	60	16
2535	60	36
2536	60	22
2537	60	31
2538	60	7
2539	60	33
2540	60	24
2541	60	29
2542	60	14
2543	60	35
2544	60	17
2545	60	26
2546	60	10
2547	60	11
2548	60	8
2549	60	12
2550	60	25
2551	60	15
2552	60	18
2553	60	9
2554	60	23
2555	60	37
2556	60	34
2557	61	31
2558	61	29
2559	61	25
2560	61	27
2561	61	13
2562	61	35
2563	61	26
2564	61	34
2565	61	24
2566	61	16
2567	61	20
2568	61	15
2569	62	11
2570	62	36
2571	62	17
2572	62	19
2573	62	34
2574	62	28
2575	62	29
2576	62	25
2577	62	33
2578	63	23
2579	63	35
2580	63	10
2581	63	18
2582	63	29
2583	63	22
2584	63	29
2585	63	32
2586	63	17
2587	63	25
2588	64	11
2589	64	15
2590	64	25
2591	64	10
2592	64	18
2593	64	24
2594	64	23
2595	64	19
2596	64	21
2597	64	36
2598	64	35
2599	64	22
2600	64	31
2601	64	26
2602	65	14
2603	65	33
2604	65	17
2605	65	9
2606	65	7
2607	65	11
2608	65	27
2609	65	31
2610	65	23
2611	65	15
2612	65	22
2613	65	18
2614	65	35
2615	65	29
2616	65	19
2617	65	37
2618	65	12
2619	65	24
2620	65	25
2621	65	8
2622	66	37
2623	66	36
2624	66	20
2625	66	8
2626	66	26
2627	66	24
2628	66	21
2629	66	14
2630	66	25
2631	66	13
2632	66	29
2633	66	15
2634	66	9
2635	67	35
2636	67	24
2637	67	34
2638	67	16
2639	67	29
2640	67	13
2641	67	18
2642	67	27
2643	67	12
2644	67	10
2645	68	33
2646	68	36
2647	68	9
2648	68	29
2649	68	35
2650	68	13
2651	68	27
2652	68	10
2653	68	37
2654	68	11
2655	68	14
2656	68	18
2657	68	19
2658	68	17
2659	68	31
2660	69	23
2661	69	18
2662	69	27
2663	69	22
2664	69	7
2665	69	36
2666	69	33
2667	69	31
2668	69	29
2669	69	20
2670	69	9
2671	69	34
2672	69	17
2673	69	11
2674	70	14
2675	70	8
2676	70	12
2677	70	28
2678	70	33
2679	70	31
2680	70	22
2681	70	25
2682	70	26
2683	71	25
2684	71	19
2685	71	29
2686	71	14
2687	71	17
2688	71	7
2689	71	36
2690	71	26
2691	71	32
2692	71	11
2693	71	13
2694	71	12
2695	71	18
2696	71	16
2697	71	37
2698	71	8
2699	71	15
2700	72	9
2701	72	29
2702	72	34
2703	72	24
2704	72	12
2705	72	21
2706	72	35
2707	72	15
2708	72	14
2709	72	28
2710	72	17
2711	72	37
2712	72	10
2713	72	26
2714	72	23
2715	72	11
2716	72	31
2717	72	22
2718	72	29
2719	72	19
2720	72	16
2721	72	8
2722	72	27
2723	72	36
2724	72	25
2725	72	18
2726	72	33
2727	72	32
2728	72	13
2729	73	10
2730	73	18
2731	73	29
2732	73	9
2733	73	11
2734	73	32
2735	73	23
2736	73	35
2737	73	22
2738	73	36
2739	73	19
2740	73	24
2741	73	16
2742	73	13
2743	73	34
2744	74	12
2745	74	29
2746	74	36
2747	74	32
2748	74	15
2749	74	7
2750	74	25
2751	74	27
2752	74	9
2753	74	10
2754	74	31
2755	74	28
2756	74	23
2757	74	37
2758	74	17
2759	75	33
2760	75	8
2761	75	7
2762	75	11
2763	75	18
2764	75	16
2765	75	19
2766	75	34
2767	75	24
2768	75	35
2769	75	14
2770	75	23
2771	75	25
2772	75	36
2773	75	17
2774	75	9
2775	75	22
2776	75	37
2777	75	21
2778	75	10
2779	75	20
2780	76	18
2781	76	17
2782	76	34
2783	76	7
2784	76	20
2785	76	16
2786	76	36
2787	76	29
2788	76	23
2789	76	9
2790	76	28
2791	76	35
2792	76	29
2793	76	15
2794	76	27
2795	77	7
2796	77	29
2797	77	19
2798	77	20
2799	77	18
2800	77	31
2801	77	34
2802	77	16
2803	77	12
2804	77	37
2805	77	29
2806	77	25
2807	77	27
2808	77	22
2809	77	14
2810	77	11
2811	77	32
2812	77	15
2813	77	9
2814	77	21
2815	77	28
2816	77	36
2817	77	17
2818	77	23
2819	78	34
2820	78	35
2821	78	28
2822	78	16
2823	78	37
2824	78	26
2825	78	24
2826	78	13
2827	79	32
2828	79	35
2829	79	24
2830	79	10
2831	79	9
2832	79	34
2833	79	15
2834	79	37
2835	79	25
2836	79	29
2837	79	17
2838	79	31
2839	79	33
2840	79	8
2841	79	14
2842	79	16
2843	79	23
2844	79	27
2845	79	13
2846	79	11
2847	79	7
2848	79	21
2849	80	20
2850	80	27
2851	80	29
2852	80	29
2853	80	21
2854	80	9
2855	80	31
2856	80	16
2857	80	19
2858	80	37
2859	80	28
2860	80	34
2861	80	35
2862	80	15
2863	80	12
2864	80	14
2865	80	18
2866	80	23
2867	80	13
2868	80	32
2869	80	33
2870	80	22
2871	80	11
2872	80	24
2873	81	16
2874	81	8
2875	81	10
2876	81	17
2877	81	34
2878	81	28
2879	81	37
2880	81	20
2881	81	9
2882	81	14
2883	81	23
2884	81	7
2885	81	26
2886	81	33
2887	81	31
2888	81	27
2889	81	19
2890	81	32
2891	81	29
2892	81	24
2893	81	13
2894	81	18
2895	81	12
2896	82	35
2897	82	18
2898	82	24
2899	82	10
2900	82	31
2901	82	23
2902	82	7
\.


--
-- Name: seen_statements_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('seen_statements_uid_seq', 2902, true);


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
1	Ein Radar überwacht den Abstand, eine Frontkamera erkennt Fahrspuren und andere Verkehrsteilnehmer, und je sechs Ultraschallsensoren vorne und hinten helfen beim Einparken und messen während der Fahrt Distanzen im Zentimeterbereich	localhost:3449	/devcards/index.html	5	68	4	2017-08-17 13:44:18.804201
2	Zunächst einmal unterscheidet sich die Hardware für den Autopiloten nicht oder nur marginal von dem, was selbst für einen VW Polo erhältlich ist	localhost:3449	/	5	68	4	2017-08-17 13:44:18.804201
3	Katzen sind kleine Tiger	http://www.iflscience.com/	plants-and-animals/no-your-cat-isnt-plotting-kill-youbut-it-has-lions-personality/	2	15	2	2017-08-17 13:44:18.804201
4	Katzen sind kleine Tiger	http://www.iflscience.com/	plants-and-animals/no-your-cat-isnt-plotting-kill-youbut-it-has-lions-personality/	2	16	2	2017-08-17 13:44:18.804201
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
1	2	we should get a cat	1	2017-08-02 13:44:19.559255	f
2	3	we should get a dog	1	2017-08-13 13:44:19.559377	f
3	4	we could get both, a cat and a dog	1	2017-08-16 13:44:19.559431	f
4	5	cats are very independent	1	2017-08-06 13:44:19.559477	f
5	6	cats are capricious	1	2017-08-01 13:44:19.55952	f
6	7	dogs can act as watch dogs	1	2017-08-11 13:44:19.559561	f
7	8	you have to take the dog for a walk every day, which is tedious	1	2017-07-25 13:44:19.5596	f
8	9	we have no use for a watch dog	1	2017-07-27 13:44:19.559641	f
9	10	going for a walk with the dog every day is good for social interaction and physical exercise	1	2017-08-14 13:44:19.55968	f
10	11	it would be no problem	1	2017-08-07 13:44:19.55972	f
11	12	a cat and a dog will generally not get along well	1	2017-07-28 13:44:19.559759	f
12	13	we do not have enough money for two pets	1	2017-08-10 13:44:19.559798	f
13	14	a dog costs taxes and will be more expensive than a cat	1	2017-08-12 13:44:19.559837	f
14	15	cats are fluffy	1	2017-08-06 13:44:19.559877	f
15	16	cats are small	1	2017-08-17 13:44:19.559915	f
16	17	fluffy animals losing much hair and I'm allergic to animal hair	1	2017-07-31 13:44:19.559955	f
17	18	you could use a automatic vacuum cleaner	1	2017-08-14 13:44:19.560018	f
18	19	cats ancestors are animals in wildlife, who are hunting alone and not in groups	1	2017-08-13 13:44:19.560074	f
19	20	this is not true for overbred races	1	2017-07-30 13:44:19.560115	f
20	21	this lies in their the natural conditions	1	2017-08-14 13:44:19.560157	f
21	22	the purpose of a pet is to have something to take care of	1	2017-08-08 13:44:19.560196	f
22	23	several cats of friends of mine are real as*holes	1	2017-08-13 13:44:19.560236	f
23	24	the fact, that cats are capricious, is based on the cats race	1	2017-08-01 13:44:19.560276	f
24	25	not every cat is capricious	1	2017-08-14 13:44:19.560315	f
25	26	this is based on the cats race and a little bit on the breeding	1	2017-08-08 13:44:19.56036	f
26	27	next to the taxes you will need equipment like a dog lead, anti-flea-spray, and so on	1	2017-07-28 13:44:19.560401	f
27	28	the equipment for running costs of cats and dogs are nearly the same	1	2017-08-08 13:44:19.56044	f
28	29	this is just a claim without any justification	1	2017-08-14 13:44:19.560479	f
29	30	in Germany you have to pay for your second dog even more taxes!	1	2017-08-13 13:44:19.560518	f
30	31	it is important, that pets are small and fluffy!	1	2017-08-13 13:44:19.560558	f
31	32	cats are little, sweet and innocent cuddle toys	1	2017-08-15 13:44:19.560597	f
32	33	do you have ever seen a sphinx cat or savannah cats?	1	2017-08-11 13:44:19.560637	f
33	34	it is much work to take care of both animals	1	2017-07-28 13:44:19.560676	f
34	35	won't be best friends	1	2017-08-09 13:44:19.560715	f
35	36	the city should reduce the number of street festivals	3	2017-08-10 13:44:19.560754	f
36	37	we should shut down University Park	3	2017-08-13 13:44:19.560793	f
37	38	we should close public swimming pools	1	2017-08-17 13:44:19.560832	f
38	39	reducing the number of street festivals can save up to $50.000 a year	1	2017-08-04 13:44:19.560871	f
39	40	every street festival is funded by large companies	1	2017-07-27 13:44:19.56091	f
40	41	then we will have more money to expand out pedestrian zone	1	2017-07-31 13:44:19.560949	f
41	42	our city will get more attractive for shopping	1	2017-07-26 13:44:19.560988	f
42	43	street festivals attract many people, which will increase the citys income	1	2017-08-14 13:44:19.561026	f
43	44	spending of the city for these festivals are higher than the earnings	1	2017-08-14 13:44:19.561065	f
44	45	money does not solve problems of our society	1	2017-08-14 13:44:19.561104	f
45	46	criminals use University Park to sell drugs	1	2017-08-01 13:44:19.561143	f
46	47	shutting down University Park will save $100.000 a year	1	2017-08-14 13:44:19.561181	f
47	48	we should not give in to criminals	1	2017-08-07 13:44:19.56122	f
48	49	the number of police patrols has been increased recently	1	2017-08-15 13:44:19.561258	f
49	50	this is the only park in our city	1	2017-08-06 13:44:19.561297	f
50	51	there are many parks in neighbouring towns	1	2017-08-11 13:44:19.561335	f
51	52	the city is planing a new park in the upcoming month	3	2017-08-03 13:44:19.561373	f
52	53	parks are very important for our climate	3	2017-07-25 13:44:19.561411	f
53	54	our swimming pools are very old and it would take a major investment to repair them	3	2017-07-28 13:44:19.561449	f
54	55	schools need the swimming pools for their sports lessons	1	2017-08-04 13:44:19.561488	f
55	56	the rate of non-swimmers is too high	1	2017-07-27 13:44:19.561526	f
56	57	the police cannot patrol in the park for 24/7	1	2017-08-11 13:44:19.561566	f
57	58	E-Autos "optimal" für den Stadtverkehr sind	1	2017-07-31 13:44:19.561604	f
58	59	dadurch die Lärmbelästigung in der Stadt sinkt	1	2017-08-01 13:44:19.561643	f
77	77	Straßenfeste viel Lärm verursachen	1	2017-07-24 13:44:19.562404	f
59	60	die Anzahl an Ladestationen in der Stadt nicht ausreichend ist	1	2017-08-02 13:44:19.561682	f
60	61	das Unfallrisiko steigt, da die Autos kaum Geräusche verursachen	1	2017-08-05 13:44:19.56172	f
61	62	die Autos auch zuhause geladen werden können und das pro Tag ausreichen sollte	1	2017-07-24 13:44:19.561758	f
62	63	Elektroautos keine lauten Geräusche beim Anfahren produzieren	1	2017-08-11 13:44:19.561797	f
63	64	Lärmbelästigung kein wirkliches Problem in den Städten ist	1	2017-07-26 13:44:19.561835	f
64	65	nicht jede normale Tankstelle auch Stromtankstellen hat	1	2017-08-15 13:44:19.561896	f
65	66	die Länder und Kommunen den Ausbau nun stark fördern wollen	1	2017-08-08 13:44:19.561938	f
66	67	E-Autos das autonome Fahren vorantreiben	5	2017-07-24 13:44:19.561977	f
67	68	Tesla mutig bestehende Techniken einsetzt und zeigt was sie können	5	2017-08-07 13:44:19.562016	f
68	69	durch rücksichtsvolle Verhaltensanpassungen der wissenschaftlichen Mitarbeitenden der Arbeitsaufwand der Sekretärinnen gesenkt werden könnte	1	2017-08-10 13:44:19.562055	f
69	70	wir Standard-Formulare, wie Urlaubsanträge, selbst faxen können	1	2017-07-27 13:44:19.562093	f
70	71	etliche Abläufe durch ein besseres Zusammenarbeiten optimiert werden können. Dies sollte auch schriftlich als Anleitungen festgehalten werden, damit neue Angestellt einen leichten Einstieg finden	1	2017-07-23 13:44:19.562132	f
71	72	viele Arbeiten auch durch die Mitarbeiter erledigt werden können	1	2017-08-04 13:44:19.562171	f
72	73	"rücksichtsvolle Verhaltensanpassungen" viel zu allgemein gehalten ist	1	2017-08-10 13:44:19.56221	f
73	74	das Faxgerät nicht immer zugänglich ist, wenn die Sekretärinnen nicht anwesend sind	1	2017-08-03 13:44:19.562249	f
74	75	wir keine eigenen Faxgeräte haben und so oder so entweder bei Martin stören müssten oder doch bei Sabine im Büro landen würden	1	2017-08-03 13:44:19.562288	f
75	1	Cats are fucking stupid and bloody fuzzy critters!	1	2017-08-17 13:44:19.562326	f
76	76	Die Anzahl der Straßenfeste sollte reduziert werden	1	2017-08-15 13:44:19.562366	f
78	78	Straßenfeste ein wichtiger Bestandteil unserer Kultur sind	1	2017-08-10 13:44:19.562443	f
79	79	Straßenfeste der Kommune Geld einbringen	1	2017-07-24 13:44:19.562483	f
80	80	die Einnahmen der Kommune durch Straßenfeste nur gering sind	1	2017-07-28 13:44:19.562522	f
81	81	Straßenfeste der Kommune hohe Kosten verursachen durch Polizeieinsätze, Säuberung, etc.	1	2017-08-16 13:44:19.562561	f
82	82	die Innenstadt ohnehin sehr laut ist	1	2017-08-04 13:44:19.562601	f
\.


--
-- Name: textversions_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('textversions_uid_seq', 82, true);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY users (uid, firstname, surname, nickname, public_nickname, email, gender, password, group_uid, last_action, last_login, registered, token, token_timestamp) FROM stdin;
1	anonymous	anonymous	anonymous	anonymous		m	$2a$10$9uW.QLJc0S9JDSdArzvASefAidhND1o9lKNEyEYiBuoJRkmMLiWwy	3	2017-08-17 13:44:19.377933	2017-08-17 13:44:19.378068	2017-08-17 13:44:19.378118		\N
2	Tobias	Krauthoff	Tobias	Tobias	krauthoff@cs.uni-duesseldorf.de	m	$2a$10$9P5biPvyX2xVeMcCLm82tO0XFQhmdMFwgAhPaUkCHoVL1F5kEAjIa	1	2017-08-17 13:44:19.378203	2017-08-17 13:44:19.378251	2017-08-17 13:44:19.378295		\N
3	Christian	Meter	Christian	Christian	meter@cs.uni-duesseldorf.de	m	$2a$10$Ou/pHV1MoZRqvt5U8cV09up0qqbIz70ZjwEeanRkyyfR/rrMHcBfe	1	2017-08-17 13:44:19.378377	2017-08-17 13:44:19.378424	2017-08-17 13:44:19.378468		\N
4	Björn	Ebbinghaus	Björn	Björn	bjoern.ebbinghaus@uni-duesseldorf.de	m	$2a$10$BfuBfUVkJvqzePMoAoAyeODRzFesqM4lb5I9o/6ljLDzcXhusfM0y	1	2017-08-17 13:44:19.383558	2017-08-17 13:44:19.383649	2017-08-17 13:44:19.383714		\N
5	Teresa	Uebber	Teresa	Teresa	teresa.uebber@uni-duesseldorf.de	f	$2a$10$1zkC3TbBMf77YoIj0MPrzuW1zUtt3BeJyitTCyPe1zbPc0WSBIi1i	1	2017-08-17 13:44:19.383824	2017-08-17 13:44:19.383889	2017-08-17 13:44:19.38395		\N
6	Bob	Bubbles	Bob	Bob	tobias.krauthoff+dbas.usert31@gmail.com	n	$2a$10$KCCzZ35EZ8xRGA/ZU3AOJebYKcpnoNzcoPzUNFPTu4S9ibuZQYWka	1	2017-08-17 13:44:19.384055	2017-08-17 13:44:19.38412	2017-08-17 13:44:19.38418		\N
7	Pascal	Lux	Pascal	Pascal	tobias.krauthoff+dbas.usert00@gmail.com	m	$2a$10$KCCzZ35EZ8xRGA/ZU3AOJebYKcpnoNzcoPzUNFPTu4S9ibuZQYWka	3	2017-08-17 13:44:19.384385	2017-08-17 13:44:19.384455	2017-08-17 13:44:19.384515		\N
8	Kurt	Hecht	Kurt	Kurt	tobias.krauthoff+dbas.usert01@gmail.com	m	$2a$10$KCCzZ35EZ8xRGA/ZU3AOJebYKcpnoNzcoPzUNFPTu4S9ibuZQYWka	3	2017-08-17 13:44:19.384589	2017-08-17 13:44:19.384635	2017-08-17 13:44:19.384678		\N
9	Torben	Hartl	Torben	Torben	tobias.krauthoff+dbas.usert02@gmail.com	m	$2a$10$KCCzZ35EZ8xRGA/ZU3AOJebYKcpnoNzcoPzUNFPTu4S9ibuZQYWka	3	2017-08-17 13:44:19.384751	2017-08-17 13:44:19.384796	2017-08-17 13:44:19.384839		\N
10	Thorsten	Scherer	Thorsten	Thorsten	tobias.krauthoff+dbas.usert03@gmail.com	m	$2a$10$KCCzZ35EZ8xRGA/ZU3AOJebYKcpnoNzcoPzUNFPTu4S9ibuZQYWka	3	2017-08-17 13:44:19.384912	2017-08-17 13:44:19.384957	2017-08-17 13:44:19.385		\N
11	Friedrich	Schutte	Friedrich	Friedrich	tobias.krauthoff+dbas.usert04@gmail.com	m	$2a$10$KCCzZ35EZ8xRGA/ZU3AOJebYKcpnoNzcoPzUNFPTu4S9ibuZQYWka	3	2017-08-17 13:44:19.385072	2017-08-17 13:44:19.385118	2017-08-17 13:44:19.385161		\N
12	Aayden	Westermann	Aayden	Aayden	tobias.krauthoff+dbas.usert05@gmail.com	m	$2a$10$KCCzZ35EZ8xRGA/ZU3AOJebYKcpnoNzcoPzUNFPTu4S9ibuZQYWka	3	2017-08-17 13:44:19.385235	2017-08-17 13:44:19.385281	2017-08-17 13:44:19.385324		\N
13	Hermann	Grasshoff	Hermann	Hermann	tobias.krauthoff+dbas.usert06@gmail.com	m	$2a$10$KCCzZ35EZ8xRGA/ZU3AOJebYKcpnoNzcoPzUNFPTu4S9ibuZQYWka	3	2017-08-17 13:44:19.385396	2017-08-17 13:44:19.385441	2017-08-17 13:44:19.385484		\N
14	Wolf	Himmler	Wolf	Wolf	tobias.krauthoff+dbas.usert07@gmail.com	m	$2a$10$KCCzZ35EZ8xRGA/ZU3AOJebYKcpnoNzcoPzUNFPTu4S9ibuZQYWka	3	2017-08-17 13:44:19.385557	2017-08-17 13:44:19.385602	2017-08-17 13:44:19.385655		\N
15	Jakob	Winter	Jakob	Jakob	tobias.krauthoff+dbas.usert08@gmail.com	m	$2a$10$KCCzZ35EZ8xRGA/ZU3AOJebYKcpnoNzcoPzUNFPTu4S9ibuZQYWka	3	2017-08-17 13:44:19.385739	2017-08-17 13:44:19.385783	2017-08-17 13:44:19.385826		\N
16	Alwin	Wechter	Alwin	Alwin	tobias.krauthoff+dbas.usert09@gmail.com	m	$2a$10$KCCzZ35EZ8xRGA/ZU3AOJebYKcpnoNzcoPzUNFPTu4S9ibuZQYWka	3	2017-08-17 13:44:19.385934	2017-08-17 13:44:19.385979	2017-08-17 13:44:19.386022		\N
17	Walter	Weisser	Walter	Walter	tobias.krauthoff+dbas.usert10@gmail.com	m	$2a$10$KCCzZ35EZ8xRGA/ZU3AOJebYKcpnoNzcoPzUNFPTu4S9ibuZQYWka	3	2017-08-17 13:44:19.386095	2017-08-17 13:44:19.38614	2017-08-17 13:44:19.386185		\N
18	Volker	Keitel	Volker	Volker	tobias.krauthoff+dbas.usert11@gmail.com	m	$2a$10$KCCzZ35EZ8xRGA/ZU3AOJebYKcpnoNzcoPzUNFPTu4S9ibuZQYWka	3	2017-08-17 13:44:19.386259	2017-08-17 13:44:19.386304	2017-08-17 13:44:19.38635		\N
19	Benedikt	Feuerstein	Benedikt	Benedikt	tobias.krauthoff+dbas.usert12@gmail.com	m	$2a$10$KCCzZ35EZ8xRGA/ZU3AOJebYKcpnoNzcoPzUNFPTu4S9ibuZQYWka	3	2017-08-17 13:44:19.386423	2017-08-17 13:44:19.386468	2017-08-17 13:44:19.38651		\N
20	Engelbert	Gottlieb	Engelbert	Engelbert	tobias.krauthoff+dbas.usert13@gmail.com	m	$2a$10$KCCzZ35EZ8xRGA/ZU3AOJebYKcpnoNzcoPzUNFPTu4S9ibuZQYWka	3	2017-08-17 13:44:19.386583	2017-08-17 13:44:19.386628	2017-08-17 13:44:19.38667		\N
21	Elias	Auerbach	Elias	Elias	tobias.krauthoff+dbas.usert14@gmail.com	m	$2a$10$KCCzZ35EZ8xRGA/ZU3AOJebYKcpnoNzcoPzUNFPTu4S9ibuZQYWka	3	2017-08-17 13:44:19.386747	2017-08-17 13:44:19.386834	2017-08-17 13:44:19.386878		\N
22	Rupert	Wenz	Rupert	Rupert	tobias.krauthoff+dbas.usert15@gmail.com	m	$2a$10$KCCzZ35EZ8xRGA/ZU3AOJebYKcpnoNzcoPzUNFPTu4S9ibuZQYWka	3	2017-08-17 13:44:19.386954	2017-08-17 13:44:19.387002	2017-08-17 13:44:19.387045		\N
23	Marga	Wegscheider	Marga	Marga	tobias.krauthoff+dbas.usert16@gmail.com	f	$2a$10$KCCzZ35EZ8xRGA/ZU3AOJebYKcpnoNzcoPzUNFPTu4S9ibuZQYWka	3	2017-08-17 13:44:19.387119	2017-08-17 13:44:19.387164	2017-08-17 13:44:19.387207		\N
24	Larissa	Clauberg	Larissa	Larissa	tobias.krauthoff+dbas.usert17@gmail.com	f	$2a$10$KCCzZ35EZ8xRGA/ZU3AOJebYKcpnoNzcoPzUNFPTu4S9ibuZQYWka	3	2017-08-17 13:44:19.38729	2017-08-17 13:44:19.387345	2017-08-17 13:44:19.38739		\N
25	Emmi	Rosch	Emmi	Emmi	tobias.krauthoff+dbas.usert18@gmail.com	f	$2a$10$KCCzZ35EZ8xRGA/ZU3AOJebYKcpnoNzcoPzUNFPTu4S9ibuZQYWka	3	2017-08-17 13:44:19.387463	2017-08-17 13:44:19.387511	2017-08-17 13:44:19.387554		\N
26	Konstanze	Krebs	Konstanze	Konstanze	tobias.krauthoff+dbas.usert19@gmail.com	f	$2a$10$KCCzZ35EZ8xRGA/ZU3AOJebYKcpnoNzcoPzUNFPTu4S9ibuZQYWka	3	2017-08-17 13:44:19.387627	2017-08-17 13:44:19.387674	2017-08-17 13:44:19.387717		\N
27	Catrin	Fahnrich	Catrin	Catrin	tobias.krauthoff+dbas.usert20@gmail.com	f	$2a$10$KCCzZ35EZ8xRGA/ZU3AOJebYKcpnoNzcoPzUNFPTu4S9ibuZQYWka	3	2017-08-17 13:44:19.38779	2017-08-17 13:44:19.387834	2017-08-17 13:44:19.387878		\N
28	Antonia	Bartram	Antonia	Antonia	tobias.krauthoff+dbas.usert21@gmail.com	f	$2a$10$KCCzZ35EZ8xRGA/ZU3AOJebYKcpnoNzcoPzUNFPTu4S9ibuZQYWka	3	2017-08-17 13:44:19.387952	2017-08-17 13:44:19.387997	2017-08-17 13:44:19.388041		\N
29	Nora	Kempf	Nora	Nora	tobias.krauthoff+dbas.usert22@gmail.com	f	$2a$10$KCCzZ35EZ8xRGA/ZU3AOJebYKcpnoNzcoPzUNFPTu4S9ibuZQYWka	3	2017-08-17 13:44:19.388114	2017-08-17 13:44:19.388159	2017-08-17 13:44:19.388201		\N
30	Julia	Wetter	Julia	Julia	tobias.krauthoff+dbas.usert23@gmail.com	f	$2a$10$KCCzZ35EZ8xRGA/ZU3AOJebYKcpnoNzcoPzUNFPTu4S9ibuZQYWka	3	2017-08-17 13:44:19.388273	2017-08-17 13:44:19.388318	2017-08-17 13:44:19.38836		\N
31	Jutta	Munch	Jutta	Jutta	tobias.krauthoff+dbas.usert24@gmail.com	f	$2a$10$KCCzZ35EZ8xRGA/ZU3AOJebYKcpnoNzcoPzUNFPTu4S9ibuZQYWka	3	2017-08-17 13:44:19.388436	2017-08-17 13:44:19.388481	2017-08-17 13:44:19.388523		\N
32	Helga	Heilmann	Helga	Helga	tobias.krauthoff+dbas.usert25@gmail.com	f	$2a$10$KCCzZ35EZ8xRGA/ZU3AOJebYKcpnoNzcoPzUNFPTu4S9ibuZQYWka	3	2017-08-17 13:44:19.388598	2017-08-17 13:44:19.388643	2017-08-17 13:44:19.388685		\N
33	Denise	Tietjen	Denise	Denise	tobias.krauthoff+dbas.usert26@gmail.com	f	$2a$10$KCCzZ35EZ8xRGA/ZU3AOJebYKcpnoNzcoPzUNFPTu4S9ibuZQYWka	3	2017-08-17 13:44:19.388758	2017-08-17 13:44:19.388802	2017-08-17 13:44:19.388845		\N
34	Hanne	Beckmann	Hanne	Hanne	tobias.krauthoff+dbas.usert27@gmail.com	f	$2a$10$KCCzZ35EZ8xRGA/ZU3AOJebYKcpnoNzcoPzUNFPTu4S9ibuZQYWka	3	2017-08-17 13:44:19.388918	2017-08-17 13:44:19.388962	2017-08-17 13:44:19.389007		\N
35	Elly	Landauer	Elly	Elly	tobias.krauthoff+dbas.usert28@gmail.com	f	$2a$10$KCCzZ35EZ8xRGA/ZU3AOJebYKcpnoNzcoPzUNFPTu4S9ibuZQYWka	3	2017-08-17 13:44:19.389081	2017-08-17 13:44:19.389128	2017-08-17 13:44:19.38917		\N
36	Sybille	Redlich	Sybille	Sybille	tobias.krauthoff+dbas.usert29@gmail.com	f	$2a$10$KCCzZ35EZ8xRGA/ZU3AOJebYKcpnoNzcoPzUNFPTu4S9ibuZQYWka	3	2017-08-17 13:44:19.389243	2017-08-17 13:44:19.389288	2017-08-17 13:44:19.38933		\N
37	Ingeburg	Fischer	Ingeburg	Ingeburg	tobias.krauthoff+dbas.usert30@gmail.com	f	$2a$10$KCCzZ35EZ8xRGA/ZU3AOJebYKcpnoNzcoPzUNFPTu4S9ibuZQYWka	3	2017-08-17 13:44:19.389403	2017-08-17 13:44:19.389447	2017-08-17 13:44:19.38949		\N
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

