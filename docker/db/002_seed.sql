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
REVOKE ALL ON DATABASE discussion FROM PUBLIC;
REVOKE ALL ON DATABASE discussion FROM postgres;
GRANT ALL ON DATABASE discussion TO postgres;
GRANT CONNECT,TEMPORARY ON DATABASE discussion TO PUBLIC;
GRANT CONNECT ON DATABASE discussion TO read_only_discussion;
CREATE DATABASE news WITH TEMPLATE = template0 OWNER = postgres;
REVOKE ALL ON DATABASE template1 FROM PUBLIC;
REVOKE ALL ON DATABASE template1 FROM postgres;
GRANT ALL ON DATABASE template1 TO postgres;
GRANT CONNECT ON DATABASE template1 TO PUBLIC;


\connect beaker

SET default_transaction_read_only = off;

--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.6
-- Dumped by pg_dump version 9.5.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: beaker; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA beaker;


ALTER SCHEMA beaker OWNER TO postgres;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: beaker; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA beaker FROM PUBLIC;
REVOKE ALL ON SCHEMA beaker FROM postgres;
GRANT ALL ON SCHEMA beaker TO postgres;
GRANT ALL ON SCHEMA beaker TO writer;


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

\connect discussion

SET default_transaction_read_only = off;

--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.6
-- Dumped by pg_dump version 9.5.6

SET statement_timeout = 0;
SET lock_timeout = 0;
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
-- Name: uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY arguments ALTER COLUMN uid SET DEFAULT nextval('arguments_uid_seq'::regclass);


--
-- Name: uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY clicked_arguments ALTER COLUMN uid SET DEFAULT nextval('clicked_arguments_uid_seq'::regclass);


--
-- Name: uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY clicked_statements ALTER COLUMN uid SET DEFAULT nextval('clicked_statements_uid_seq'::regclass);


--
-- Name: uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY groups ALTER COLUMN uid SET DEFAULT nextval('groups_uid_seq'::regclass);


--
-- Name: uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY history ALTER COLUMN uid SET DEFAULT nextval('history_uid_seq'::regclass);


--
-- Name: uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY issues ALTER COLUMN uid SET DEFAULT nextval('issues_uid_seq'::regclass);


--
-- Name: uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY languages ALTER COLUMN uid SET DEFAULT nextval('languages_uid_seq'::regclass);


--
-- Name: uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY last_reviewers_delete ALTER COLUMN uid SET DEFAULT nextval('last_reviewers_delete_uid_seq'::regclass);


--
-- Name: uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY last_reviewers_duplicates ALTER COLUMN uid SET DEFAULT nextval('last_reviewers_duplicates_uid_seq'::regclass);


--
-- Name: uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY last_reviewers_edit ALTER COLUMN uid SET DEFAULT nextval('last_reviewers_edit_uid_seq'::regclass);


--
-- Name: uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY last_reviewers_optimization ALTER COLUMN uid SET DEFAULT nextval('last_reviewers_optimization_uid_seq'::regclass);


--
-- Name: uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY marked_arguments ALTER COLUMN uid SET DEFAULT nextval('marked_arguments_uid_seq'::regclass);


--
-- Name: uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY marked_statements ALTER COLUMN uid SET DEFAULT nextval('marked_statements_uid_seq'::regclass);


--
-- Name: uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY messages ALTER COLUMN uid SET DEFAULT nextval('messages_uid_seq'::regclass);


--
-- Name: uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY premisegroups ALTER COLUMN uid SET DEFAULT nextval('premisegroups_uid_seq'::regclass);


--
-- Name: uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY premises ALTER COLUMN uid SET DEFAULT nextval('premises_uid_seq'::regclass);


--
-- Name: uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY reputation_history ALTER COLUMN uid SET DEFAULT nextval('reputation_history_uid_seq'::regclass);


--
-- Name: uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY reputation_reasons ALTER COLUMN uid SET DEFAULT nextval('reputation_reasons_uid_seq'::regclass);


--
-- Name: uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_canceled ALTER COLUMN uid SET DEFAULT nextval('review_canceled_uid_seq'::regclass);


--
-- Name: uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_delete_reasons ALTER COLUMN uid SET DEFAULT nextval('review_delete_reasons_uid_seq'::regclass);


--
-- Name: uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_deletes ALTER COLUMN uid SET DEFAULT nextval('review_deletes_uid_seq'::regclass);


--
-- Name: uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_duplicates ALTER COLUMN uid SET DEFAULT nextval('review_duplicates_uid_seq'::regclass);


--
-- Name: uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_edit_values ALTER COLUMN uid SET DEFAULT nextval('review_edit_values_uid_seq'::regclass);


--
-- Name: uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_edits ALTER COLUMN uid SET DEFAULT nextval('review_edits_uid_seq'::regclass);


--
-- Name: uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_optimizations ALTER COLUMN uid SET DEFAULT nextval('review_optimizations_uid_seq'::regclass);


--
-- Name: uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY revoked_content ALTER COLUMN uid SET DEFAULT nextval('revoked_content_uid_seq'::regclass);


--
-- Name: uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY revoked_content_history ALTER COLUMN uid SET DEFAULT nextval('revoked_content_history_uid_seq'::regclass);


--
-- Name: uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY revoked_duplicate ALTER COLUMN uid SET DEFAULT nextval('revoked_duplicate_uid_seq'::regclass);


--
-- Name: uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY rss ALTER COLUMN uid SET DEFAULT nextval('rss_uid_seq'::regclass);


--
-- Name: uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY seen_arguments ALTER COLUMN uid SET DEFAULT nextval('seen_arguments_uid_seq'::regclass);


--
-- Name: uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY seen_statements ALTER COLUMN uid SET DEFAULT nextval('seen_statements_uid_seq'::regclass);


--
-- Name: uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY statement_references ALTER COLUMN uid SET DEFAULT nextval('statement_references_uid_seq'::regclass);


--
-- Name: uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY statements ALTER COLUMN uid SET DEFAULT nextval('statements_uid_seq'::regclass);


--
-- Name: uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY textversions ALTER COLUMN uid SET DEFAULT nextval('textversions_uid_seq'::regclass);


--
-- Name: uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY users ALTER COLUMN uid SET DEFAULT nextval('users_uid_seq'::regclass);


--
-- Data for Name: arguments; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY arguments (uid, premisesgroup_uid, conclusion_uid, argument_uid, is_supportive, author_uid, "timestamp", issue_uid, is_disabled) FROM stdin;
1	1	2	\N	f	1	2017-03-15 17:08:24.342327	2	t
2	2	2	\N	t	1	2017-03-15 17:08:24.342327	2	f
3	3	2	\N	f	1	2017-03-15 17:08:24.342327	2	f
4	4	3	\N	t	1	2017-03-15 17:08:24.342327	2	f
5	5	3	\N	f	1	2017-03-15 17:08:24.342327	2	f
8	8	4	\N	t	1	2017-03-15 17:08:24.342327	2	f
10	10	11	\N	f	1	2017-03-15 17:08:24.342327	2	f
11	11	2	\N	t	1	2017-03-15 17:08:24.342327	2	f
12	12	2	\N	t	1	2017-03-15 17:08:24.342327	2	f
15	15	5	\N	t	1	2017-03-15 17:08:24.342327	2	f
16	16	5	\N	f	1	2017-03-15 17:08:24.342327	2	f
17	17	5	\N	t	1	2017-03-15 17:08:24.342327	2	f
19	19	6	\N	t	1	2017-03-15 17:08:24.342327	2	f
20	20	6	\N	f	1	2017-03-15 17:08:24.342327	2	f
21	21	6	\N	f	1	2017-03-15 17:08:24.342327	2	f
23	23	14	\N	f	1	2017-03-15 17:08:24.342327	2	f
24	24	14	\N	t	1	2017-03-15 17:08:24.342327	2	f
26	26	14	\N	t	1	2017-03-15 17:08:24.342327	2	f
27	27	15	\N	t	1	2017-03-15 17:08:24.342327	2	f
28	27	16	\N	t	1	2017-03-15 17:08:24.342327	2	f
29	28	15	\N	t	1	2017-03-15 17:08:24.342327	2	f
30	29	15	\N	f	1	2017-03-15 17:08:24.342327	2	f
32	31	36	\N	t	3	2017-03-15 17:08:24.342327	1	f
34	33	39	\N	t	3	2017-03-15 17:08:24.342327	1	f
35	34	41	\N	t	1	2017-03-15 17:08:24.342327	1	f
36	35	36	\N	f	1	2017-03-15 17:08:24.342327	1	f
39	38	37	\N	t	1	2017-03-15 17:08:24.342327	1	f
40	39	37	\N	t	1	2017-03-15 17:08:24.342327	1	f
41	41	46	\N	f	1	2017-03-15 17:08:24.342327	1	f
42	42	37	\N	f	1	2017-03-15 17:08:24.342327	1	f
44	44	50	\N	f	1	2017-03-15 17:08:24.342327	1	f
46	45	50	\N	t	1	2017-03-15 17:08:24.342327	1	f
47	46	38	\N	t	1	2017-03-15 17:08:24.342327	1	f
49	48	38	\N	f	1	2017-03-15 17:08:24.342327	1	f
50	49	49	\N	f	1	2017-03-15 17:08:24.342327	1	f
51	51	58	\N	f	1	2017-03-15 17:08:24.342327	4	f
54	54	59	\N	t	1	2017-03-15 17:08:24.342327	4	f
55	55	59	\N	f	1	2017-03-15 17:08:24.342327	4	f
56	56	60	\N	t	1	2017-03-15 17:08:24.342327	4	f
57	57	60	\N	f	1	2017-03-15 17:08:24.342327	4	f
58	50	58	\N	t	1	2017-03-15 17:08:24.342327	4	f
59	61	67	\N	t	1	2017-03-15 17:08:24.342327	4	f
60	62	69	\N	t	1	2017-03-15 17:08:24.342327	5	f
61	63	69	\N	t	1	2017-03-15 17:08:24.342327	5	f
62	64	69	\N	f	1	2017-03-15 17:08:24.342327	5	f
63	65	70	\N	f	1	2017-03-15 17:08:24.342327	5	f
64	66	70	\N	f	1	2017-03-15 17:08:24.342327	5	f
6	6	\N	4	f	1	2017-03-15 17:08:24.342327	2	f
7	7	\N	5	f	1	2017-03-15 17:08:24.342327	2	f
9	9	\N	8	f	1	2017-03-15 17:08:24.342327	2	f
13	13	\N	12	f	1	2017-03-15 17:08:24.342327	2	f
14	14	\N	13	f	1	2017-03-15 17:08:24.342327	2	f
18	18	\N	2	f	1	2017-03-15 17:08:24.342327	2	f
22	22	\N	3	f	1	2017-03-15 17:08:24.342327	2	f
25	25	\N	11	f	1	2017-03-15 17:08:24.342327	2	f
31	30	\N	15	f	1	2017-03-15 17:08:24.342327	2	f
33	32	\N	32	f	3	2017-03-15 17:08:24.342327	1	f
37	36	\N	36	f	1	2017-03-15 17:08:24.342327	1	f
38	37	\N	36	f	1	2017-03-15 17:08:24.342327	1	f
43	43	\N	42	f	1	2017-03-15 17:08:24.342327	1	f
45	40	\N	39	f	1	2017-03-15 17:08:24.342327	1	f
48	47	\N	47	f	1	2017-03-15 17:08:24.342327	1	f
52	52	\N	58	f	1	2017-03-15 17:08:24.342327	4	f
53	53	\N	51	f	1	2017-03-15 17:08:24.342327	4	f
\.


--
-- Name: arguments_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('arguments_uid_seq', 64, true);


--
-- Data for Name: clicked_arguments; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY clicked_arguments (uid, argument_uid, author_uid, "timestamp", is_up_vote, is_valid) FROM stdin;
1	53	32	2017-02-24 17:08:28.606637	t	t
2	53	30	2017-02-25 17:08:28.606811	t	t
3	53	30	2017-02-23 17:08:28.606919	t	t
4	53	26	2017-02-26 17:08:28.607014	t	t
5	53	15	2017-02-27 17:08:28.607104	f	t
6	53	24	2017-02-28 17:08:28.60719	f	t
7	53	37	2017-03-05 17:08:28.607273	f	t
8	53	35	2017-03-13 17:08:28.607356	f	t
9	53	26	2017-02-19 17:08:28.607437	f	t
10	53	29	2017-02-24 17:08:28.607514	f	t
11	53	19	2017-03-04 17:08:28.60759	f	t
12	53	8	2017-03-07 17:08:28.607666	f	t
13	53	27	2017-03-04 17:08:28.607741	f	t
14	53	10	2017-02-28 17:08:28.607816	f	t
\.


--
-- Name: clicked_arguments_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('clicked_arguments_uid_seq', 14, true);


--
-- Data for Name: clicked_statements; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY clicked_statements (uid, statement_uid, author_uid, "timestamp", is_up_vote, is_valid) FROM stdin;
1	75	33	2017-02-21 17:08:28.588181	t	t
2	75	17	2017-02-20 17:08:28.588368	t	t
3	75	11	2017-03-13 17:08:28.58847	t	t
4	75	33	2017-03-02 17:08:28.588558	t	t
5	75	19	2017-03-08 17:08:28.588642	t	t
6	75	26	2017-02-28 17:08:28.588722	t	t
7	75	25	2017-03-11 17:08:28.588798	t	t
8	75	30	2017-02-24 17:08:28.588873	t	t
9	75	9	2017-02-22 17:08:28.588948	t	t
10	75	22	2017-03-04 17:08:28.589022	f	t
11	75	24	2017-02-28 17:08:28.589094	f	t
12	75	9	2017-03-01 17:08:28.589219	f	t
13	75	21	2017-03-05 17:08:28.589298	f	t
14	75	9	2017-02-27 17:08:28.589371	f	t
15	75	8	2017-02-25 17:08:28.589445	f	t
16	75	10	2017-03-04 17:08:28.58952	f	t
17	75	8	2017-02-18 17:08:28.589592	f	t
18	75	23	2017-03-06 17:08:28.589666	f	t
19	75	15	2017-02-26 17:08:28.58974	f	t
20	75	35	2017-03-04 17:08:28.589813	f	t
\.


--
-- Name: clicked_statements_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('clicked_statements_uid_seq', 20, true);


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

COPY issues (uid, title, info, long_info, date, author_uid, lang_uid, is_disabled) FROM stdin;
1	Town has to cut spending 	Our town needs to cut spending. Please discuss ideas how this should be done.		2017-03-15 17:08:24.289974	2	1	f
2	Cat or Dog	Your family argues about whether to buy a cat or dog as pet. Now your opinion matters!		2017-03-15 17:08:24.289974	2	1	f
3	Make the world better	How can we make this world a better place?		2017-03-15 17:08:24.289974	2	1	f
4	Elektroautos	Elektroautos - Die Autos der Zukunft? Bitte diskutieren Sie dazu.		2017-03-15 17:08:24.289974	2	2	f
5	Unterstützung der Sekretariate	Unsere Sekretariate in der Informatik sind arbeitsmäßig stark überlastet. Bitte diskutieren Sie Möglichkeiten um dies zu verbessern.		2017-03-15 17:08:24.289974	2	2	f
6	Verbesserung des Informatik-Studiengangs	Wie können der Informatik-Studiengang verbessert und die Probleme, die durch die große Anzahl der Studierenden entstanden sind, gelöst werden?	Die Anzahl der Studierenden in der Informatik hat sich in den letzten Jahren stark erhöht. Dadurch treten zahlreiche Probleme auf, wie z.B. Raumknappheit, überfüllte Lehrveranstaltungen und ein Mangel an Plätzen zum Lernen. Wir möchten Sie gerne dazu einladen, gemeinsam mit den Dozierenden der Informatik über Lösungsmöglichkeiten zu diskutieren: Wie können der Studiengang verbessert und die Probleme, die durch die große Anzahl der Studierenden entstanden sind, gelöst werden?	2017-03-15 17:08:24.289974	2	2	t
\.


--
-- Name: issues_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('issues_uid_seq', 6, true);


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
1	15	1	t	2017-03-15 17:08:24.404075
2	17	1	f	2017-03-15 17:08:24.404075
3	18	1	t	2017-03-15 17:08:24.404075
4	23	1	t	2017-03-15 17:08:24.404075
5	24	1	t	2017-03-15 17:08:24.404075
6	21	2	f	2017-03-15 17:08:24.404075
7	22	2	t	2017-03-15 17:08:24.404075
8	19	2	f	2017-03-15 17:08:24.404075
9	35	2	t	2017-03-15 17:08:24.404075
10	25	2	f	2017-03-15 17:08:24.404075
11	26	2	f	2017-03-15 17:08:24.404075
12	27	2	f	2017-03-15 17:08:24.404075
13	28	3	f	2017-03-15 17:08:24.404075
14	29	3	f	2017-03-15 17:08:24.404075
15	34	3	f	2017-03-15 17:08:24.404075
16	20	8	t	2017-03-15 17:08:24.404075
17	36	8	t	2017-03-15 17:08:24.404075
18	37	8	t	2017-03-15 17:08:24.404075
\.


--
-- Name: last_reviewers_delete_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('last_reviewers_delete_uid_seq', 18, true);


--
-- Data for Name: last_reviewers_duplicates; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY last_reviewers_duplicates (uid, reviewer_uid, review_uid, is_okay, "timestamp") FROM stdin;
1	13	1	t	2017-03-15 17:08:24.407874
2	14	2	t	2017-03-15 17:08:24.407874
3	15	2	t	2017-03-15 17:08:24.407874
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
-- Data for Name: last_reviewers_optimization; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY last_reviewers_optimization (uid, reviewer_uid, review_uid, is_okay, "timestamp") FROM stdin;
1	30	1	t	2017-03-15 17:08:24.416218
2	32	1	t	2017-03-15 17:08:24.416218
3	33	1	t	2017-03-15 17:08:24.416218
4	13	2	f	2017-03-15 17:08:24.416218
5	14	2	f	2017-03-15 17:08:24.416218
6	16	2	f	2017-03-15 17:08:24.416218
\.


--
-- Name: last_reviewers_optimization_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('last_reviewers_optimization_uid_seq', 6, true);


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
\.


--
-- Name: premisegroups_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('premisegroups_uid_seq', 66, true);


--
-- Data for Name: premises; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY premises (uid, premisesgroup_uid, statement_uid, is_negated, author_uid, "timestamp", issue_uid, is_disabled) FROM stdin;
1	1	1	f	1	2017-03-15 17:08:24.336455	2	t
2	2	5	f	1	2017-03-15 17:08:24.336455	2	f
3	3	6	f	1	2017-03-15 17:08:24.336455	2	f
4	4	7	f	1	2017-03-15 17:08:24.336455	2	f
5	5	8	f	1	2017-03-15 17:08:24.336455	2	f
6	6	9	f	1	2017-03-15 17:08:24.336455	2	f
7	7	10	f	1	2017-03-15 17:08:24.336455	2	f
8	8	11	f	1	2017-03-15 17:08:24.336455	2	f
9	9	12	f	1	2017-03-15 17:08:24.336455	2	f
10	10	13	f	1	2017-03-15 17:08:24.336455	2	f
11	11	14	f	1	2017-03-15 17:08:24.336455	2	f
12	12	15	f	1	2017-03-15 17:08:24.336455	2	f
13	12	16	f	1	2017-03-15 17:08:24.336455	2	f
14	13	17	f	1	2017-03-15 17:08:24.336455	2	f
15	14	18	f	1	2017-03-15 17:08:24.336455	2	f
16	15	19	f	1	2017-03-15 17:08:24.336455	2	f
17	16	20	f	1	2017-03-15 17:08:24.336455	2	f
18	17	21	f	1	2017-03-15 17:08:24.336455	2	f
19	18	22	f	1	2017-03-15 17:08:24.336455	2	f
20	19	23	f	1	2017-03-15 17:08:24.336455	2	f
21	20	24	f	1	2017-03-15 17:08:24.336455	2	f
22	21	25	f	1	2017-03-15 17:08:24.336455	2	f
23	22	26	f	1	2017-03-15 17:08:24.336455	2	f
24	23	27	f	1	2017-03-15 17:08:24.336455	2	f
25	24	28	f	1	2017-03-15 17:08:24.336455	2	f
26	25	29	f	1	2017-03-15 17:08:24.336455	2	f
27	26	30	f	1	2017-03-15 17:08:24.336455	2	f
28	27	31	f	1	2017-03-15 17:08:24.336455	2	f
29	28	32	f	1	2017-03-15 17:08:24.336455	2	f
30	29	33	f	1	2017-03-15 17:08:24.336455	2	f
31	30	34	f	1	2017-03-15 17:08:24.336455	2	f
32	9	35	f	1	2017-03-15 17:08:24.336455	2	f
33	31	39	f	1	2017-03-15 17:08:24.336455	1	f
34	32	40	f	1	2017-03-15 17:08:24.336455	1	f
35	33	41	f	1	2017-03-15 17:08:24.336455	1	f
36	34	42	f	1	2017-03-15 17:08:24.336455	1	f
37	35	43	f	1	2017-03-15 17:08:24.336455	1	f
38	36	44	f	1	2017-03-15 17:08:24.336455	1	f
39	37	45	f	1	2017-03-15 17:08:24.336455	1	f
40	38	46	f	1	2017-03-15 17:08:24.336455	1	f
41	39	47	f	1	2017-03-15 17:08:24.336455	1	f
42	40	48	f	1	2017-03-15 17:08:24.336455	1	f
43	41	49	f	1	2017-03-15 17:08:24.336455	1	f
44	42	50	f	1	2017-03-15 17:08:24.336455	1	f
45	43	51	f	1	2017-03-15 17:08:24.336455	1	f
46	44	52	f	1	2017-03-15 17:08:24.336455	1	f
47	45	53	f	1	2017-03-15 17:08:24.336455	1	f
48	46	54	f	1	2017-03-15 17:08:24.336455	1	f
49	47	55	f	1	2017-03-15 17:08:24.336455	1	f
50	48	56	f	1	2017-03-15 17:08:24.336455	1	f
51	49	57	f	1	2017-03-15 17:08:24.336455	1	f
52	52	61	f	1	2017-03-15 17:08:24.336455	4	f
53	53	62	f	1	2017-03-15 17:08:24.336455	4	f
54	54	63	f	1	2017-03-15 17:08:24.336455	4	f
55	55	64	f	1	2017-03-15 17:08:24.336455	4	f
56	56	65	f	1	2017-03-15 17:08:24.336455	4	f
57	57	66	f	1	2017-03-15 17:08:24.336455	4	f
58	50	59	f	1	2017-03-15 17:08:24.336455	4	f
59	51	60	f	1	2017-03-15 17:08:24.336455	4	f
60	61	68	f	5	2017-03-15 17:08:24.336455	4	f
61	62	71	f	1	2017-03-15 17:08:24.336455	5	f
62	63	72	f	1	2017-03-15 17:08:24.336455	5	f
63	64	73	f	1	2017-03-15 17:08:24.336455	5	f
64	65	74	f	1	2017-03-15 17:08:24.336455	5	f
65	66	75	f	1	2017-03-15 17:08:24.336455	5	f
\.


--
-- Name: premises_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('premises_uid_seq', 65, true);


--
-- Data for Name: reputation_history; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY reputation_history (uid, reputator_uid, reputation_uid, "timestamp") FROM stdin;
1	24	1	2017-03-13 17:08:28.845221
2	24	2	2017-03-14 17:08:28.845221
3	24	3	2017-03-15 17:08:28.845221
4	26	1	2017-03-13 17:08:28.845221
5	26	2	2017-03-14 17:08:28.845221
6	26	3	2017-03-15 17:08:28.845221
7	23	1	2017-03-13 17:08:28.845221
8	23	2	2017-03-14 17:08:28.845221
9	23	3	2017-03-15 17:08:28.845221
10	35	1	2017-03-13 17:08:28.845221
11	35	2	2017-03-14 17:08:28.845221
12	35	3	2017-03-15 17:08:28.845221
13	2	1	2017-03-13 17:08:28.845221
14	2	2	2017-03-14 17:08:28.845221
15	2	3	2017-03-15 17:08:28.845221
16	2	8	2017-03-15 17:08:28.845221
17	4	3	2017-03-13 17:08:28.845221
18	4	4	2017-03-13 17:08:28.845221
19	4	5	2017-03-14 17:08:28.845221
20	4	6	2017-03-14 17:08:28.845221
21	4	9	2017-03-15 17:08:28.845221
22	4	8	2017-03-15 17:08:28.845221
23	3	4	2017-03-13 17:08:28.845221
24	3	5	2017-03-13 17:08:28.845221
25	3	6	2017-03-14 17:08:28.845221
26	3	9	2017-03-14 17:08:28.845221
27	3	7	2017-03-15 17:08:28.845221
28	3	10	2017-03-15 17:08:28.845221
29	3	8	2017-03-15 17:08:28.845221
30	3	11	2017-03-15 17:08:28.845221
31	3	12	2017-03-15 17:08:28.845221
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

COPY review_canceled (uid, author_uid, review_edit_uid, review_delete_uid, review_optimization_uid, review_duplicate_uid, was_ongoing, "timestamp") FROM stdin;
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
1	19	12	\N	2017-03-15 17:08:24.374452	t	1	f
2	20	29	\N	2017-03-15 17:08:24.374452	t	2	f
3	21	\N	8	2017-03-15 17:08:24.374452	t	2	f
4	22	\N	29	2017-03-15 17:08:24.374452	f	2	f
5	23	\N	19	2017-03-15 17:08:24.374452	f	1	f
6	24	\N	25	2017-03-15 17:08:24.374452	f	2	f
7	25	6	\N	2017-03-15 17:08:24.374452	f	2	f
8	26	30	\N	2017-03-15 17:08:24.374452	f	2	f
9	27	16	\N	2017-03-15 17:08:24.374452	f	1	f
10	28	1	\N	2017-03-15 17:08:24.374452	t	1	f
\.


--
-- Name: review_deletes_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('review_deletes_uid_seq', 10, true);


--
-- Data for Name: review_duplicates; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY review_duplicates (uid, detector_uid, duplicate_statement_uid, original_statement_uid, "timestamp", is_executed, is_revoked) FROM stdin;
1	29	6	1	2017-03-15 17:08:24.397375	f	f
2	30	4	1	2017-03-15 17:08:24.397375	t	f
3	30	22	7	2017-03-15 17:08:24.397375	f	f
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
1	4	\N	2	2017-03-15 17:08:24.380276	f	f
\.


--
-- Name: review_edits_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('review_edits_uid_seq', 1, true);


--
-- Data for Name: review_optimizations; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY review_optimizations (uid, detector_uid, argument_uid, statement_uid, "timestamp", is_executed, is_revoked) FROM stdin;
1	13	27	\N	2017-03-15 17:08:24.391768	t	f
2	14	\N	29	2017-03-15 17:08:24.391768	t	f
3	15	\N	12	2017-03-15 17:08:24.391768	f	f
4	17	8	\N	2017-03-15 17:08:24.391768	f	f
5	18	25	\N	2017-03-15 17:08:24.391768	f	f
6	16	\N	29	2017-03-15 17:08:24.391768	f	f
\.


--
-- Name: review_optimizations_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('review_optimizations_uid_seq', 6, true);


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
65	1	12
66	1	30
67	1	38
68	1	35
69	1	37
70	1	20
71	1	36
72	1	21
73	1	29
74	1	30
75	1	28
76	1	33
77	1	11
78	1	18
79	1	19
80	1	25
81	1	32
82	1	15
83	1	26
84	2	23
85	2	12
86	2	30
87	2	36
88	2	11
89	2	29
90	2	30
91	2	28
92	2	8
93	2	38
94	2	27
95	2	9
96	2	24
97	2	17
98	2	21
99	2	13
100	2	35
101	3	26
102	3	27
103	3	14
104	3	37
105	3	16
106	3	23
107	3	11
108	3	33
109	3	17
110	3	9
111	3	18
112	4	26
113	4	38
114	4	14
115	4	17
116	4	25
117	4	11
118	4	18
119	4	30
120	4	34
121	4	20
122	4	10
123	4	32
124	4	27
125	4	16
126	4	24
127	4	37
128	4	13
129	5	8
130	5	36
131	5	32
132	5	30
133	5	13
134	5	34
135	5	22
136	5	27
137	5	10
138	5	9
139	5	15
140	5	11
141	5	29
142	5	19
143	5	35
144	5	12
145	5	38
146	5	18
147	8	10
148	8	22
149	8	27
150	8	15
151	8	14
152	8	38
153	8	18
154	8	19
155	8	13
156	8	35
157	8	21
158	8	30
159	8	8
160	8	26
161	8	25
162	8	9
163	8	17
164	8	12
165	8	11
166	8	36
167	8	24
168	8	20
169	8	33
170	8	28
171	8	32
172	8	29
173	10	11
174	10	23
175	10	21
176	10	30
177	11	25
178	11	30
179	11	16
180	11	32
181	11	22
182	11	26
183	11	13
184	11	18
185	11	12
186	11	9
187	11	10
188	11	36
189	11	38
190	11	23
191	11	24
192	11	20
193	11	15
194	11	35
195	11	17
196	11	8
197	11	34
198	11	33
199	11	37
200	11	30
201	11	29
202	11	11
203	12	18
204	12	15
205	12	38
206	12	26
207	12	25
208	12	23
209	12	30
210	12	37
211	12	20
212	12	34
213	12	36
214	12	27
215	12	12
216	12	16
217	12	30
218	12	13
219	12	14
220	12	32
221	12	11
222	12	22
223	12	21
224	12	24
225	12	17
226	12	8
227	12	9
228	12	19
229	12	29
230	12	33
231	15	30
232	15	23
233	15	10
234	15	16
235	15	18
236	15	15
237	15	38
238	15	13
239	15	12
240	15	30
241	15	9
242	15	14
243	15	28
244	15	22
245	15	17
246	15	33
247	15	35
248	16	22
249	16	9
250	16	12
251	16	16
252	16	25
253	17	14
254	17	12
255	17	23
256	17	13
257	17	19
258	17	29
259	17	20
260	17	21
261	17	9
262	17	10
263	17	11
264	19	10
265	19	11
266	19	12
267	19	19
268	19	33
269	19	36
270	19	22
271	19	34
272	19	30
273	19	30
274	19	25
275	19	37
276	19	18
277	19	27
278	19	29
279	19	16
280	19	15
281	19	32
282	19	35
283	19	14
284	19	17
285	20	21
286	20	12
287	20	10
288	20	9
289	20	20
290	20	27
291	20	19
292	20	38
293	20	22
294	21	14
295	21	29
296	21	15
297	21	11
298	21	19
299	21	30
300	21	9
301	21	36
302	21	27
303	21	13
304	21	37
305	21	26
306	21	32
307	21	38
308	21	20
309	21	18
310	21	16
311	21	30
312	21	21
313	23	15
314	23	21
315	23	11
316	23	33
317	23	9
318	24	21
319	24	35
320	24	32
321	24	28
322	24	36
323	24	29
324	24	23
325	24	34
326	26	29
327	26	33
328	26	14
329	26	30
330	26	37
331	26	23
332	26	26
333	26	28
334	26	15
335	27	8
336	27	24
337	27	15
338	27	37
339	27	33
340	27	27
341	27	16
342	27	34
343	27	26
344	27	38
345	27	17
346	27	29
347	27	12
348	28	24
349	28	9
350	28	30
351	28	8
352	28	30
353	28	12
354	28	33
355	28	17
356	28	32
357	28	21
358	28	37
359	28	28
360	28	19
361	28	34
362	28	22
363	28	13
364	28	16
365	28	38
366	28	27
367	28	23
368	28	35
369	29	22
370	29	12
371	29	30
372	29	26
373	29	28
374	30	10
375	30	12
376	30	22
377	30	17
378	30	14
379	32	37
380	32	25
381	32	23
382	32	35
383	32	10
384	32	14
385	32	18
386	32	32
387	32	28
388	32	33
389	32	19
390	32	8
391	32	34
392	32	21
393	32	20
394	32	38
395	34	12
396	34	36
397	34	19
398	34	18
399	34	13
400	34	9
401	34	25
402	34	27
403	34	11
404	34	35
405	34	8
406	34	22
407	34	23
408	34	30
409	34	21
410	34	37
411	34	28
412	34	26
413	34	34
414	34	38
415	34	14
416	34	30
417	34	24
418	34	29
419	34	15
420	34	10
421	34	32
422	34	16
423	35	28
424	35	21
425	35	9
426	35	37
427	35	18
428	35	17
429	35	26
430	35	8
431	35	24
432	35	20
433	35	13
434	35	25
435	35	23
436	35	22
437	35	15
438	35	38
439	35	27
440	35	11
441	35	14
442	35	16
443	35	34
444	35	30
445	35	30
446	35	36
447	35	33
448	35	29
449	35	32
450	36	32
451	36	13
452	36	21
453	36	34
454	36	9
455	39	26
456	39	14
457	39	8
458	39	16
459	39	10
460	39	27
461	39	34
462	39	29
463	39	15
464	39	19
465	39	20
466	39	12
467	39	32
468	39	23
469	39	17
470	39	30
471	39	30
472	40	33
473	40	9
474	40	35
475	40	14
476	40	32
477	40	22
478	40	17
479	40	15
480	40	19
481	40	25
482	40	37
483	40	18
484	40	10
485	40	8
486	40	23
487	40	34
488	40	36
489	40	38
490	40	26
491	40	11
492	40	13
493	40	30
494	40	21
495	40	24
496	40	20
497	40	30
498	40	16
499	41	24
500	41	22
501	41	33
502	41	23
503	41	16
504	41	11
505	41	34
506	41	37
507	41	17
508	41	27
509	41	10
510	41	13
511	41	15
512	41	32
513	41	29
514	41	30
515	41	36
516	41	19
517	41	14
518	41	30
519	41	8
520	41	38
521	41	35
522	41	20
523	41	26
524	41	18
525	42	22
526	42	30
527	42	34
528	42	36
529	42	25
530	42	17
531	44	23
532	44	26
533	44	27
534	44	17
535	44	25
536	44	12
537	44	18
538	44	20
539	44	34
540	44	22
541	44	33
542	44	29
543	44	36
544	44	30
545	44	24
546	44	10
547	44	32
548	44	15
549	44	28
550	44	13
551	46	37
552	46	28
553	46	14
554	46	29
555	46	30
556	46	10
557	46	12
558	46	38
559	46	33
560	46	34
561	46	17
562	46	27
563	46	26
564	46	16
565	46	35
566	46	36
567	46	11
568	46	30
569	46	32
570	46	20
571	46	19
572	46	8
573	46	22
574	46	18
575	46	9
576	47	14
577	47	15
578	47	38
579	47	26
580	49	32
581	49	19
582	49	16
583	49	12
584	49	22
585	49	30
586	49	23
587	49	13
588	49	34
589	50	23
590	50	28
591	50	20
592	50	37
593	50	11
594	50	15
595	50	32
596	50	16
597	50	9
598	50	30
599	50	10
600	50	29
601	50	8
602	50	36
603	50	24
604	50	14
605	50	22
606	50	30
607	50	18
608	50	35
609	51	15
610	51	11
611	51	18
612	51	24
613	51	27
614	51	29
615	51	13
616	51	36
617	51	32
618	51	37
619	51	16
620	51	33
621	51	26
622	51	34
623	51	10
624	51	20
625	51	9
626	51	8
627	51	22
628	54	34
629	54	19
630	54	16
631	54	30
632	54	13
633	54	25
634	54	23
635	54	9
636	54	26
637	54	14
638	54	18
639	54	20
640	54	29
641	54	33
642	54	15
643	54	11
644	54	12
645	55	27
646	55	8
647	55	12
648	55	33
649	55	24
650	55	35
651	55	18
652	55	29
653	55	10
654	55	32
655	55	30
656	56	12
657	56	25
658	56	22
659	56	38
660	56	8
661	56	30
662	56	35
663	56	29
664	56	34
665	56	18
666	56	15
667	56	21
668	56	20
669	56	24
670	56	13
671	56	37
672	56	10
673	56	9
674	56	16
675	57	8
676	57	32
677	57	30
678	57	10
679	57	25
680	57	13
681	57	23
682	57	12
683	57	34
684	57	20
685	57	17
686	57	28
687	57	36
688	57	35
689	58	30
690	58	19
691	58	35
692	58	28
693	58	8
694	58	22
695	58	30
696	59	13
697	59	27
698	59	8
699	59	32
700	59	9
701	59	34
702	59	25
703	59	23
704	59	20
705	59	18
706	59	12
707	59	26
708	59	15
709	59	37
710	59	22
711	59	24
712	60	26
713	60	37
714	60	17
715	60	35
716	60	12
717	60	34
718	60	8
719	60	19
720	60	23
721	60	32
722	60	22
723	60	29
724	60	15
725	60	33
726	61	25
727	61	20
728	61	9
729	61	21
730	61	27
731	61	14
732	61	30
733	61	17
734	61	23
735	61	30
736	61	34
737	61	32
738	61	13
739	61	19
740	61	18
741	61	28
742	61	15
743	61	26
744	62	27
745	62	13
746	62	19
747	62	10
748	62	23
749	62	14
750	62	30
751	62	9
752	62	38
753	62	26
754	62	22
755	62	30
756	62	24
757	62	18
758	62	21
759	62	8
760	62	33
761	62	32
762	62	25
763	62	20
764	62	28
765	62	29
766	63	21
767	63	14
768	63	28
769	63	19
770	63	34
771	63	32
772	63	27
773	64	32
774	64	35
775	64	23
776	64	10
777	64	34
778	64	29
779	64	30
780	64	33
781	64	21
782	64	12
783	64	28
784	64	11
785	64	30
786	64	18
787	64	19
788	64	27
789	64	22
790	64	38
791	64	25
792	64	16
793	64	36
794	64	14
795	64	8
796	64	13
797	64	20
798	64	15
799	64	17
800	64	24
801	6	13
802	6	11
803	6	27
804	6	35
805	6	36
806	6	29
807	6	14
808	6	17
809	6	38
810	6	19
811	6	20
812	6	22
813	6	8
814	6	30
815	6	21
816	6	15
817	6	18
818	6	30
819	6	10
820	6	28
821	6	25
822	6	9
823	6	16
824	6	32
825	6	37
826	6	34
827	7	25
828	7	20
829	7	32
830	7	9
831	7	29
832	7	30
833	7	15
834	7	33
835	7	18
836	7	11
837	7	21
838	7	14
839	7	34
840	7	30
841	7	26
842	7	13
843	7	17
844	7	16
845	7	19
846	7	24
847	7	35
848	7	37
849	7	28
850	7	23
851	7	10
852	7	38
853	7	22
854	7	8
855	7	27
856	9	8
857	9	24
858	9	9
859	9	20
860	9	37
861	9	29
862	9	38
863	9	35
864	9	10
865	9	25
866	9	17
867	13	25
868	13	8
869	13	33
870	13	26
871	13	35
872	13	14
873	13	24
874	13	27
875	14	8
876	14	28
877	14	9
878	14	35
879	14	18
880	14	24
881	14	15
882	14	16
883	14	37
884	14	34
885	18	27
886	18	35
887	18	28
888	18	14
889	18	29
890	18	15
891	18	17
892	18	22
893	18	20
894	18	10
895	18	8
896	22	17
897	22	37
898	22	25
899	22	38
900	22	14
901	22	29
902	22	23
903	22	30
904	22	34
905	22	21
906	22	27
907	22	11
908	22	10
909	22	35
910	22	19
911	22	12
912	22	9
913	22	22
914	22	30
915	22	18
916	22	20
917	22	33
918	22	13
919	22	15
920	25	18
921	25	30
922	25	21
923	25	32
924	25	10
925	25	20
926	25	14
927	25	27
928	25	37
929	25	22
930	25	33
931	25	17
932	25	30
933	25	25
934	25	12
935	25	28
936	25	16
937	25	38
938	25	15
939	25	34
940	25	24
941	25	19
942	25	11
943	25	13
944	25	29
945	25	9
946	25	23
947	31	16
948	31	36
949	31	14
950	31	24
951	31	20
952	31	38
953	31	11
954	31	28
955	31	18
956	31	8
957	31	30
958	31	23
959	31	15
960	31	21
961	31	29
962	31	10
963	31	22
964	31	37
965	31	32
966	31	26
967	31	13
968	33	10
969	33	21
970	33	38
971	33	36
972	33	11
973	37	33
974	37	21
975	37	29
976	37	13
977	37	28
978	38	28
979	38	25
980	38	15
981	38	33
982	38	9
983	43	13
984	43	34
985	43	28
986	43	29
987	43	25
988	43	14
989	43	38
990	43	17
991	43	8
992	43	30
993	43	37
994	43	9
995	43	15
996	43	22
997	43	36
998	43	11
999	43	24
1000	43	23
1001	43	30
1002	43	10
1003	43	26
1004	43	21
1005	43	27
1006	43	19
1007	43	32
1008	43	35
1009	43	16
1010	43	20
1011	43	12
1012	45	24
1013	45	33
1014	45	37
1015	45	12
1016	45	29
1017	45	25
1018	48	30
1019	48	8
1020	48	10
1021	48	9
1022	48	36
1023	48	24
1024	48	15
1025	48	34
1026	48	16
1027	48	13
1028	48	26
1029	48	23
1030	48	11
1031	48	28
1032	48	17
1033	48	19
1034	48	33
1035	52	36
1036	52	30
1037	52	34
1038	52	13
1039	52	28
1040	52	11
1041	52	18
1042	52	19
1043	52	10
1044	52	17
1045	52	35
1046	52	8
1047	52	12
1048	52	24
1049	52	23
1050	52	27
1051	52	37
1052	52	16
1053	53	35
1054	53	38
1055	53	27
1056	53	18
1057	53	15
1058	53	8
1059	53	25
1060	53	12
1061	53	23
1062	53	32
1063	53	9
1064	53	34
\.


--
-- Name: seen_arguments_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('seen_arguments_uid_seq', 1064, true);


--
-- Data for Name: seen_statements; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY seen_statements (uid, statement_uid, user_uid) FROM stdin;
76	1	12
77	1	28
78	1	33
79	1	27
80	1	17
81	1	19
82	1	23
83	1	18
84	1	10
85	1	11
86	1	9
87	1	37
88	1	30
89	1	25
90	1	13
91	1	16
92	1	24
93	1	20
94	1	29
95	2	21
96	2	11
97	2	34
98	2	14
99	2	18
100	2	30
101	2	25
102	2	12
103	2	8
104	2	38
105	2	26
106	2	19
107	2	24
108	3	10
109	3	30
110	3	23
111	3	26
112	3	12
113	3	18
114	3	15
115	3	24
116	3	14
117	3	9
118	3	38
119	3	33
120	3	25
121	3	13
122	3	32
123	3	22
124	3	19
125	3	8
126	3	27
127	3	30
128	3	21
129	3	35
130	3	17
131	3	37
132	3	29
133	3	36
134	3	28
135	4	32
136	4	21
137	4	33
138	4	12
139	4	37
140	4	16
141	4	14
142	4	9
143	4	38
144	4	11
145	4	23
146	4	26
147	4	30
148	4	18
149	4	30
150	4	15
151	4	29
152	4	35
153	4	24
154	4	22
155	4	27
156	4	13
157	4	17
158	4	19
159	4	10
160	4	25
161	4	34
162	4	28
163	4	8
164	5	11
165	5	30
166	5	20
167	5	18
168	5	9
169	5	37
170	5	36
171	5	35
172	5	30
173	5	28
174	6	38
175	6	21
176	6	25
177	6	27
178	6	9
179	6	28
180	6	14
181	6	11
182	6	36
183	6	32
184	6	17
185	6	33
186	6	24
187	6	26
188	6	18
189	6	30
190	6	16
191	6	10
192	6	30
193	6	35
194	6	20
195	6	13
196	6	15
197	6	23
198	6	8
199	6	19
200	6	12
201	6	29
202	6	22
203	7	20
204	7	19
205	7	18
206	7	12
207	7	37
208	7	33
209	7	9
210	7	17
211	7	32
212	7	8
213	7	22
214	7	30
215	7	36
216	7	14
217	7	13
218	7	29
219	7	10
220	7	25
221	7	30
222	7	11
223	7	27
224	8	19
225	8	20
226	8	22
227	8	16
228	8	26
229	8	34
230	8	14
231	8	13
232	8	30
233	8	18
234	8	29
235	8	38
236	8	12
237	8	30
238	8	10
239	8	33
240	8	17
241	8	28
242	8	9
243	8	27
244	8	37
245	8	8
246	8	36
247	8	35
248	9	24
249	9	16
250	9	19
251	9	9
252	9	25
253	9	38
254	9	28
255	9	14
256	9	11
257	9	10
258	9	13
259	9	33
260	9	37
261	9	18
262	9	21
263	9	29
264	9	23
265	9	36
266	9	34
267	9	22
268	9	8
269	9	35
270	9	27
271	9	30
272	9	12
273	9	32
274	9	15
275	10	23
276	10	32
277	10	25
278	10	13
279	10	37
280	10	11
281	10	21
282	10	30
283	10	14
284	10	12
285	10	19
286	10	27
287	10	34
288	10	9
289	10	35
290	10	8
291	10	22
292	10	10
293	10	38
294	10	26
295	10	20
296	10	29
297	10	33
298	10	16
299	10	30
300	10	15
301	10	28
302	10	18
303	11	26
304	11	38
305	11	32
306	11	11
307	11	27
308	11	20
309	11	34
310	11	28
311	11	30
312	11	17
313	11	15
314	11	10
315	12	15
316	12	9
317	12	8
318	12	28
319	13	18
320	13	30
321	13	33
322	13	13
323	13	12
324	13	15
325	13	28
326	13	30
327	13	29
328	13	37
329	13	21
330	13	24
331	13	10
332	13	34
333	14	19
334	14	29
335	14	17
336	14	9
337	14	37
338	14	30
339	14	36
340	14	23
341	14	27
342	14	21
343	14	13
344	14	26
345	14	11
346	14	16
347	14	20
348	14	35
349	14	38
350	14	30
351	14	33
352	14	24
353	14	12
354	15	8
355	15	16
356	15	27
357	15	34
358	15	37
359	15	33
360	15	30
361	16	23
362	16	35
363	16	17
364	16	20
365	16	27
366	16	13
367	16	37
368	16	30
369	16	30
370	16	29
371	16	24
372	16	9
373	16	21
374	16	10
375	16	18
376	16	26
377	16	32
378	17	19
379	17	28
380	17	24
381	17	13
382	17	8
383	17	27
384	17	29
385	17	30
386	17	30
387	17	16
388	17	26
389	18	21
390	18	26
391	18	38
392	18	36
393	18	35
394	18	27
395	18	17
396	18	16
397	18	30
398	18	20
399	18	9
400	18	10
401	18	18
402	18	19
403	18	30
404	18	23
405	18	13
406	19	23
407	19	32
408	19	18
409	19	13
410	19	14
411	19	27
412	19	8
413	19	21
414	19	35
415	19	26
416	19	25
417	19	30
418	19	20
419	19	36
420	19	30
421	19	29
422	19	24
423	19	19
424	19	34
425	19	10
426	19	12
427	19	33
428	19	38
429	20	36
430	20	21
431	20	16
432	20	9
433	20	30
434	20	34
435	20	29
436	20	10
437	20	38
438	20	19
439	20	11
440	20	32
441	20	17
442	20	26
443	20	27
444	20	8
445	20	12
446	20	20
447	20	18
448	20	23
449	20	30
450	20	37
451	20	33
452	20	13
453	21	13
454	21	22
455	21	37
456	21	30
457	21	18
458	21	29
459	21	36
460	21	19
461	21	23
462	21	10
463	21	21
464	21	12
465	21	14
466	21	16
467	21	35
468	21	9
469	21	32
470	21	34
471	21	8
472	21	28
473	21	11
474	21	20
475	21	17
476	21	24
477	21	38
478	21	26
479	21	15
480	21	30
481	21	27
482	22	17
483	22	34
484	22	35
485	22	14
486	22	8
487	22	36
488	22	37
489	22	32
490	22	25
491	22	18
492	22	30
493	22	10
494	22	9
495	22	38
496	23	13
497	23	16
498	23	18
499	23	19
500	23	27
501	23	33
502	23	30
503	23	28
504	23	29
505	23	30
506	23	20
507	23	12
508	23	37
509	23	9
510	23	26
511	23	35
512	23	22
513	23	21
514	23	24
515	23	36
516	23	14
517	23	23
518	23	17
519	23	32
520	23	15
521	23	8
522	23	25
523	23	10
524	24	38
525	24	12
526	24	30
527	24	14
528	24	11
529	24	33
530	24	9
531	24	21
532	24	25
533	24	13
534	24	29
535	24	27
536	24	15
537	24	17
538	24	23
539	24	28
540	24	30
541	24	20
542	24	16
543	24	8
544	24	32
545	24	24
546	24	18
547	24	35
548	24	26
549	25	26
550	25	34
551	25	16
552	25	25
553	25	27
554	25	29
555	25	30
556	25	23
557	25	33
558	25	38
559	25	14
560	25	36
561	25	15
562	25	20
563	25	9
564	25	30
565	25	8
566	25	21
567	25	19
568	25	28
569	25	35
570	25	32
571	25	37
572	25	22
573	25	17
574	26	33
575	26	25
576	26	14
577	26	36
578	26	27
579	26	32
580	26	35
581	26	38
582	26	20
583	26	34
584	26	24
585	26	37
586	26	10
587	26	15
588	26	16
589	26	8
590	26	13
591	26	12
592	26	9
593	26	26
594	26	30
595	26	22
596	27	22
597	27	34
598	27	37
599	27	21
600	27	35
601	27	27
602	27	26
603	27	15
604	27	20
605	27	33
606	27	30
607	27	19
608	27	9
609	27	12
610	27	29
611	27	17
612	27	8
613	27	25
614	27	28
615	27	32
616	27	38
617	27	11
618	27	13
619	28	33
620	28	34
621	28	30
622	28	11
623	28	20
624	28	24
625	28	15
626	28	29
627	28	14
628	28	12
629	28	37
630	28	16
631	28	26
632	28	30
633	28	18
634	28	25
635	28	23
636	28	19
637	28	27
638	28	13
639	28	10
640	29	10
641	29	30
642	29	34
643	29	26
644	29	25
645	29	21
646	29	32
647	29	24
648	29	18
649	29	28
650	29	13
651	30	9
652	30	33
653	30	18
654	30	17
655	30	24
656	30	37
657	30	14
658	30	23
659	30	35
660	30	32
661	30	26
662	30	38
663	30	36
664	30	30
665	30	13
666	30	30
667	30	15
668	30	11
669	30	21
670	30	19
671	30	34
672	30	8
673	30	27
674	30	10
675	31	21
676	31	34
677	31	9
678	31	25
679	31	10
680	31	29
681	31	8
682	31	30
683	31	13
684	31	20
685	31	24
686	31	28
687	31	32
688	31	18
689	31	36
690	31	16
691	31	22
692	31	26
693	31	27
694	32	30
695	32	32
696	32	30
697	32	11
698	32	28
699	32	16
700	32	27
701	32	14
702	32	9
703	32	10
704	32	21
705	32	8
706	32	29
707	32	18
708	32	35
709	32	34
710	32	33
711	32	13
712	33	32
713	33	12
714	33	19
715	33	36
716	33	11
717	33	15
718	33	34
719	33	38
720	33	10
721	33	18
722	33	13
723	33	24
724	33	27
725	33	16
726	33	26
727	34	38
728	34	37
729	34	28
730	34	30
731	34	30
732	34	32
733	34	24
734	35	30
735	35	17
736	35	16
737	35	20
738	35	18
739	35	24
740	35	28
741	35	35
742	35	19
743	36	24
744	36	28
745	36	21
746	36	38
747	36	9
748	36	8
749	37	36
750	37	24
751	37	14
752	37	20
753	37	30
754	37	13
755	37	29
756	37	25
757	37	22
758	37	12
759	37	19
760	37	37
761	37	38
762	37	34
763	37	18
764	37	16
765	37	27
766	37	21
767	37	8
768	37	9
769	37	30
770	38	17
771	38	30
772	38	37
773	38	27
774	38	38
775	38	30
776	38	13
777	38	22
778	38	32
779	38	24
780	38	28
781	38	10
782	38	34
783	38	19
784	38	12
785	38	33
786	38	9
787	39	22
788	39	16
789	39	34
790	39	13
791	39	38
792	39	8
793	39	10
794	39	32
795	39	29
796	39	27
797	39	23
798	39	15
799	39	26
800	39	9
801	39	33
802	39	24
803	39	28
804	39	35
805	39	37
806	39	36
807	39	21
808	39	19
809	39	14
810	39	30
811	39	17
812	39	20
813	39	11
814	39	25
815	39	18
816	40	10
817	40	27
818	40	18
819	40	20
820	40	19
821	40	25
822	40	21
823	40	34
824	40	29
825	40	8
826	40	22
827	40	35
828	40	26
829	40	32
830	40	9
831	40	30
832	40	28
833	40	16
834	40	38
835	40	24
836	40	37
837	41	30
838	41	16
839	41	17
840	41	33
841	41	35
842	41	25
843	41	30
844	41	26
845	41	23
846	41	32
847	41	11
848	41	8
849	41	10
850	41	28
851	41	19
852	41	36
853	41	24
854	41	14
855	41	37
856	41	12
857	41	18
858	41	34
859	41	27
860	41	29
861	41	22
862	41	15
863	41	13
864	41	38
865	42	35
866	42	17
867	42	22
868	42	28
869	42	29
870	42	34
871	42	30
872	42	38
873	42	20
874	42	14
875	42	10
876	42	18
877	42	8
878	42	25
879	42	36
880	42	37
881	43	11
882	43	12
883	43	32
884	43	14
885	43	23
886	43	37
887	43	15
888	43	35
889	43	18
890	43	27
891	43	20
892	43	10
893	43	26
894	43	19
895	43	36
896	43	17
897	43	33
898	43	25
899	44	18
900	44	23
901	44	14
902	44	16
903	44	17
904	45	8
905	45	23
906	45	35
907	45	27
908	45	18
909	45	17
910	45	14
911	45	34
912	45	32
913	45	19
914	45	20
915	45	24
916	45	36
917	45	9
918	46	8
919	46	22
920	46	36
921	46	23
922	46	17
923	46	21
924	46	20
925	46	38
926	46	28
927	46	25
928	46	9
929	46	10
930	46	30
931	46	27
932	46	37
933	46	34
934	46	30
935	46	12
936	46	16
937	46	15
938	46	35
939	46	32
940	46	13
941	47	20
942	47	19
943	47	12
944	47	11
945	47	15
946	47	23
947	47	22
948	47	35
949	47	30
950	47	18
951	47	24
952	47	28
953	47	16
954	47	27
955	47	33
956	47	8
957	47	26
958	48	38
959	48	16
960	48	13
961	48	9
962	48	32
963	48	17
964	48	35
965	48	24
966	48	22
967	48	12
968	48	19
969	48	21
970	48	30
971	48	25
972	48	8
973	48	14
974	48	27
975	48	18
976	48	10
977	48	28
978	48	15
979	48	11
980	48	37
981	48	20
982	48	33
983	49	15
984	49	33
985	49	24
986	49	14
987	49	26
988	49	21
989	49	38
990	49	18
991	49	35
992	49	30
993	50	25
994	50	24
995	50	14
996	50	21
997	50	19
998	50	33
999	50	11
1000	50	36
1001	50	30
1002	50	22
1003	50	23
1004	50	27
1005	50	16
1006	50	15
1007	50	13
1008	50	30
1009	51	27
1010	51	14
1011	51	30
1012	51	9
1013	51	23
1014	51	25
1015	51	11
1016	51	26
1017	51	37
1018	52	18
1019	52	30
1020	52	23
1021	52	27
1022	52	17
1023	52	30
1024	52	33
1025	52	11
1026	52	38
1027	52	36
1028	52	21
1029	52	14
1030	52	9
1031	52	13
1032	52	26
1033	52	12
1034	52	29
1035	52	8
1036	52	20
1037	52	28
1038	52	19
1039	52	16
1040	52	15
1041	52	35
1042	52	22
1043	53	12
1044	53	8
1045	53	13
1046	53	26
1047	53	22
1048	53	9
1049	53	18
1050	53	20
1051	53	24
1052	54	34
1053	54	15
1054	54	36
1055	54	27
1056	54	13
1057	54	24
1058	54	11
1059	54	25
1060	54	20
1061	54	38
1062	54	37
1063	54	14
1064	54	8
1065	54	28
1066	54	32
1067	54	26
1068	54	35
1069	54	30
1070	54	23
1071	54	19
1072	54	16
1073	54	30
1074	54	10
1075	55	28
1076	55	37
1077	55	22
1078	55	36
1079	55	8
1080	55	20
1081	55	11
1082	55	9
1083	55	27
1084	55	32
1085	56	27
1086	56	19
1087	56	13
1088	56	34
1089	56	30
1090	56	14
1091	57	36
1092	57	8
1093	57	25
1094	57	37
1095	57	13
1096	57	26
1097	57	34
1098	57	30
1099	57	23
1100	58	29
1101	58	26
1102	58	12
1103	58	15
1104	58	19
1105	58	17
1106	58	37
1107	58	8
1108	58	9
1109	58	36
1110	58	32
1111	58	35
1112	58	25
1113	58	30
1114	58	27
1115	58	34
1116	58	18
1117	58	28
1118	58	11
1119	58	16
1120	58	38
1121	58	33
1122	58	22
1123	59	22
1124	59	28
1125	59	35
1126	59	36
1127	59	10
1128	59	25
1129	59	16
1130	59	29
1131	59	9
1132	59	26
1133	59	8
1134	59	27
1135	59	20
1136	59	11
1137	59	32
1138	59	23
1139	59	30
1140	59	37
1141	59	33
1142	59	24
1143	59	14
1144	60	8
1145	60	34
1146	60	9
1147	60	38
1148	60	23
1149	60	26
1150	60	19
1151	60	30
1152	60	25
1153	61	37
1154	61	25
1155	61	30
1156	61	13
1157	61	19
1158	61	29
1159	62	18
1160	62	13
1161	62	33
1162	62	35
1163	62	29
1164	62	14
1165	62	23
1166	62	24
1167	62	32
1168	62	20
1169	62	19
1170	62	12
1171	62	10
1172	63	13
1173	63	36
1174	63	25
1175	63	17
1176	63	11
1177	63	33
1178	63	28
1179	63	16
1180	63	34
1181	63	30
1182	63	23
1183	63	27
1184	63	22
1185	63	32
1186	63	35
1187	63	10
1188	63	14
1189	64	30
1190	64	27
1191	64	11
1192	64	30
1193	65	24
1194	65	23
1195	65	36
1196	65	34
1197	65	8
1198	65	9
1199	65	32
1200	65	15
1201	65	13
1202	65	10
1203	65	14
1204	65	33
1205	65	26
1206	65	38
1207	65	11
1208	65	27
1209	66	17
1210	66	37
1211	66	20
1212	66	16
1213	66	12
1214	66	27
1215	66	11
1216	66	25
1217	66	8
1218	66	24
1219	66	18
1220	66	29
1221	66	30
1222	66	9
1223	66	28
1224	66	35
1225	66	23
1226	67	30
1227	67	36
1228	67	30
1229	67	19
1230	67	13
1231	67	21
1232	67	9
1233	67	35
1234	67	37
1235	68	27
1236	68	28
1237	68	30
1238	68	25
1239	68	18
1240	68	10
1241	68	33
1242	68	35
1243	68	17
1244	68	24
1245	68	32
1246	68	22
1247	68	26
1248	68	29
1249	68	9
1250	68	15
1251	68	37
1252	68	21
1253	68	14
1254	68	16
1255	68	19
1256	69	11
1257	69	30
1258	69	21
1259	69	12
1260	69	29
1261	69	23
1262	69	20
1263	69	16
1264	69	38
1265	69	32
1266	69	19
1267	69	14
1268	69	27
1269	69	26
1270	69	22
1271	70	14
1272	70	16
1273	70	34
1274	70	30
1275	70	19
1276	70	18
1277	70	15
1278	70	20
1279	70	11
1280	70	32
1281	71	20
1282	71	36
1283	71	24
1284	71	38
1285	71	33
1286	72	17
1287	72	26
1288	72	30
1289	72	34
1290	72	9
1291	72	11
1292	72	32
1293	72	33
1294	72	38
1295	72	37
1296	72	29
1297	72	36
1298	72	14
1299	72	16
1300	72	35
1301	72	24
1302	72	18
1303	72	20
1304	72	23
1305	72	22
1306	72	25
1307	72	15
1308	72	19
1309	72	13
1310	72	30
1311	73	23
1312	73	9
1313	73	25
1314	73	22
1315	73	11
1316	73	21
1317	73	27
1318	73	13
1319	73	10
1320	73	16
1321	74	20
1322	74	25
1323	74	28
1324	74	8
1325	74	32
1326	74	23
1327	74	26
1328	74	21
1329	74	34
1330	74	10
1331	74	37
1332	75	22
1333	75	30
1334	75	23
1335	75	24
1336	75	12
1337	75	35
1338	75	13
1339	75	11
1340	75	21
1341	75	33
1342	75	19
1343	75	28
1344	75	10
1345	75	38
1346	75	30
1347	75	15
1348	75	34
1349	75	16
1350	75	17
1351	75	9
1352	75	27
1353	75	14
1354	75	26
1355	75	25
\.


--
-- Name: seen_statements_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('seen_statements_uid_seq', 1355, true);


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
38	f	t	t	1	2	f
\.


--
-- Data for Name: statement_references; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY statement_references (uid, reference, host, path, author_uid, statement_uid, issue_uid, created) FROM stdin;
1	Ein Radar überwacht den Abstand, eine Frontkamera erkennt Fahrspuren und andere Verkehrsteilnehmer, und je sechs Ultraschallsensoren vorne und hinten helfen beim Einparken und messen während der Fahrt Distanzen im Zentimeterbereich	localhost:3449	/devcards/index.html	5	68	4	2017-03-15 17:08:24.31987
2	Zunächst einmal unterscheidet sich die Hardware für den Autopiloten nicht oder nur marginal von dem, was selbst für einen VW Polo erhältlich ist	localhost:3449	/	5	68	4	2017-03-15 17:08:24.31987
3	Katzen sind kleine Tiger	http://www.iflscience.com/	plants-and-animals/no-your-cat-isnt-plotting-kill-youbut-it-has-lions-personality/	2	15	2	2017-03-15 17:08:24.31987
4	Katzen sind kleine Tiger	http://www.iflscience.com/	plants-and-animals/no-your-cat-isnt-plotting-kill-youbut-it-has-lions-personality/	2	16	2	2017-03-15 17:08:24.31987
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
\.


--
-- Name: statements_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('statements_uid_seq', 75, true);


--
-- Data for Name: textversions; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY textversions (uid, statement_uid, content, author_uid, "timestamp", is_disabled) FROM stdin;
1	2	we should get a cat	1	2017-03-02 17:08:26.560535	f
2	3	we should get a dog	1	2017-03-11 17:08:26.560675	f
3	4	we could get both, a cat and a dog	1	2017-02-24 17:08:26.560743	f
4	5	cats are very independent	1	2017-03-02 17:08:26.560797	f
5	6	cats are capricious	1	2017-03-12 17:08:26.560847	f
6	7	dogs can act as watch dogs	1	2017-02-18 17:08:26.560894	f
7	8	you have to take the dog for a walk every day, which is tedious	1	2017-02-26 17:08:26.560941	f
8	9	we have no use for a watch dog	1	2017-03-10 17:08:26.560987	f
9	10	going for a walk with the dog every day is good for social interaction and physical exercise	1	2017-02-22 17:08:26.561032	f
10	11	it would be no problem	1	2017-02-24 17:08:26.561076	f
11	12	a cat and a dog will generally not get along well	1	2017-02-18 17:08:26.561121	f
12	13	we do not have enough money for two pets	1	2017-02-22 17:08:26.561201	f
13	14	a dog costs taxes and will be more expensive than a cat	1	2017-02-18 17:08:26.561249	f
14	15	cats are fluffy	1	2017-03-15 17:08:26.561293	f
15	16	cats are small	1	2017-03-09 17:08:26.561338	f
16	17	fluffy animals losing much hair and I'm allergic to animal hair	1	2017-03-02 17:08:26.561384	f
17	18	you could use a automatic vacuum cleaner	1	2017-02-18 17:08:26.561429	f
18	19	cats ancestors are animals in wildlife, who are hunting alone and not in groups	1	2017-03-04 17:08:26.561473	f
19	20	this is not true for overbred races	1	2017-03-05 17:08:26.561517	f
20	21	this lies in their the natural conditions	1	2017-03-13 17:08:26.561561	f
21	22	the purpose of a pet is to have something to take care of	1	2017-03-12 17:08:26.561605	f
22	23	several cats of friends of mine are real as*holes	1	2017-02-23 17:08:26.561647	f
23	24	the fact, that cats are capricious, is based on the cats race	1	2017-03-03 17:08:26.561691	f
24	25	not every cat is capricious	1	2017-03-15 17:08:26.561734	f
25	26	this is based on the cats race and a little bit on the breeding	1	2017-02-25 17:08:26.561777	f
26	27	next to the taxes you will need equipment like a dog lead, anti-flea-spray, and so on	1	2017-03-11 17:08:26.56182	f
27	28	the equipment for running costs of cats and dogs are nearly the same	1	2017-03-08 17:08:26.561863	f
28	29	this is just a claim without any justification	1	2017-02-22 17:08:26.561908	f
29	30	in Germany you have to pay for your second dog even more taxes!	1	2017-02-18 17:08:26.561952	f
30	31	it is important, that pets are small and fluffy!	1	2017-02-20 17:08:26.561996	f
31	32	cats are little, sweet and innocent cuddle toys	1	2017-02-27 17:08:26.562039	f
32	33	do you have ever seen a sphinx cat or savannah cats?	1	2017-03-02 17:08:26.562082	f
33	34	it is much work to take care of both animals	1	2017-03-10 17:08:26.562126	f
34	35	won't be best friends	1	2017-02-26 17:08:26.562169	f
35	36	the city should reduce the number of street festivals	3	2017-02-28 17:08:26.562213	f
36	37	we should shut down University Park	3	2017-03-13 17:08:26.562257	f
37	38	we should close public swimming pools	1	2017-03-07 17:08:26.562299	f
38	39	reducing the number of street festivals can save up to $50.000 a year	1	2017-02-19 17:08:26.562343	f
39	40	every street festival is funded by large companies	1	2017-02-24 17:08:26.562386	f
40	41	then we will have more money to expand out pedestrian zone	1	2017-03-07 17:08:26.562429	f
41	42	our city will get more attractive for shopping	1	2017-03-06 17:08:26.562472	f
42	43	street festivals attract many people, which will increase the citys income	1	2017-02-19 17:08:26.562515	f
43	44	spending of the city for these festivals are higher than the earnings	1	2017-03-04 17:08:26.562557	f
44	45	money does not solve problems of our society	1	2017-03-06 17:08:26.5626	f
45	46	criminals use University Park to sell drugs	1	2017-03-08 17:08:26.562644	f
46	47	shutting down University Park will save $100.000 a year	1	2017-03-06 17:08:26.562688	f
47	48	we should not give in to criminals	1	2017-02-28 17:08:26.562731	f
48	49	the number of police patrols has been increased recently	1	2017-03-04 17:08:26.562775	f
49	50	this is the only park in our city	1	2017-02-20 17:08:26.562819	f
50	51	there are many parks in neighbouring towns	1	2017-03-05 17:08:26.562863	f
51	52	the city is planing a new park in the upcoming month	3	2017-02-22 17:08:26.562907	f
52	53	parks are very important for our climate	3	2017-02-21 17:08:26.562952	f
53	54	our swimming pools are very old and it would take a major investment to repair them	3	2017-02-20 17:08:26.562996	f
54	55	schools need the swimming pools for their sports lessons	1	2017-03-13 17:08:26.563041	f
55	56	the rate of non-swimmers is too high	1	2017-02-26 17:08:26.563084	f
56	57	the police cannot patrol in the park for 24/7	1	2017-03-06 17:08:26.563128	f
57	58	E-Autos "optimal" für den Stadtverkehr sind	1	2017-03-12 17:08:26.563172	f
58	59	dadurch die Lärmbelästigung in der Stadt sinkt	1	2017-03-10 17:08:26.563215	f
59	60	die Anzahl an Ladestationen in der Stadt nicht ausreichend ist	1	2017-03-11 17:08:26.563258	f
60	61	das Unfallrisiko steigt, da die Autos kaum Geräusche verursachen	1	2017-03-13 17:08:26.563301	f
61	62	die Autos auch zuhause geladen werden können und das pro Tag ausreichen sollte	1	2017-02-20 17:08:26.563345	f
62	63	Elektroautos keine lauten Geräusche beim Anfahren produzieren	1	2017-03-05 17:08:26.563388	f
63	64	Lärmbelästigung kein wirkliches Problem in den Städten ist	1	2017-02-22 17:08:26.563432	f
64	65	nicht jede normale Tankstelle auch Stromtankstellen hat	1	2017-02-27 17:08:26.563475	f
65	66	die Länder und Kommunen den Ausbau nun stark fördern wollen	1	2017-03-02 17:08:26.563519	f
66	67	E-Autos das autonome Fahren vorantreiben	5	2017-02-23 17:08:26.563562	f
67	68	Tesla mutig bestehende Techniken einsetzt und zeigt was sie können	5	2017-03-11 17:08:26.563605	f
68	69	durch rücksichtsvolle Verhaltensanpassungen der wissenschaftlichen Mitarbeitenden der Arbeitsaufwand der Sekretärinnen gesenkt werden könnte	1	2017-02-25 17:08:26.563648	f
69	70	wir Standard-Formulare, wie Urlaubsanträge, selbst faxen können	1	2017-03-08 17:08:26.563691	f
74	75	wir keine eigenen Faxgeräte haben und so oder so entweder bei Martin stören müssten oder doch bei Sabine im Büro landen würden	1	2017-03-13 17:08:26.563905	f
70	71	etliche Abläufe durch ein besseres Zusammenarbeiten optimiert werden können. Dies sollte auch schriftlich als Anleitungen festgehalten werden, damit neue Angestellt einen leichten Einstieg finden	1	2017-03-07 17:08:26.563734	f
71	72	viele Arbeiten auch durch die Mitarbeiter erledigt werden können	1	2017-03-14 17:08:26.563777	f
72	73	"rücksichtsvolle Verhaltensanpassungen" viel zu allgemein gehalten ist	1	2017-02-26 17:08:26.56382	f
73	74	das Faxgerät nicht immer zugänglich ist, wenn die Sekretärinnen nicht anwesend sind	1	2017-02-21 17:08:26.563863	f
75	1	Cats are fucking stupid and bloody fuzzy critters!	1	2017-03-10 17:08:26.563948	f
\.


--
-- Name: textversions_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('textversions_uid_seq', 75, true);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY users (uid, firstname, surname, nickname, public_nickname, email, gender, password, group_uid, last_action, last_login, registered, token, token_timestamp) FROM stdin;
1	anonymous	anonymous	anonymous	anonymous		m	$2a$10$p7Xwpa1Z1p83T/.gdbaD6eNBS/7.ha9FEk5G654zB2i0Ca9jnXYv.	3	2017-03-15 17:08:24.304299	2017-03-15 17:08:24.304473	2017-03-15 17:08:24.304621		\N
2	admin	admin	admin	admin	dbas.hhu@gmail.com	m	$2a$10$OUgpmtJ2mjLezfgMLBdZ8egic399ONRTHqSJ.2sYgoZIxx0QzEMAW	1	2017-03-15 17:08:24.304299	2017-03-15 17:08:24.304473	2017-03-15 17:08:24.304621		\N
3	Tobias	Krauthoff	Tobias	Tobias	krauthoff@cs.uni-duesseldorf.de	m	$2a$10$9P5biPvyX2xVeMcCLm82tO0XFQhmdMFwgAhPaUkCHoVL1F5kEAjIa	1	2017-03-15 17:08:24.304299	2017-03-15 17:08:24.304473	2017-03-15 17:08:24.304621		\N
4	Christian	Meter	Christian	Christian	meter@cs.uni-duesseldorf.de	m	$2a$10$Ou/pHV1MoZRqvt5U8cV09up0qqbIz70ZjwEeanRkyyfR/rrMHcBfe	1	2017-03-15 17:08:24.304299	2017-03-15 17:08:24.304473	2017-03-15 17:08:24.304621		\N
5	Björn	Ebbinghaus	Björn	Björn	bjoern.ebbinghaus@uni-duesseldorf.de	m	$2a$10$X4f.ZQXG2KHVcG3Qb2QlzOuY7OvfT8IuZKHYXqUfbzM/dDdDIieqK	1	2017-03-15 17:08:24.304299	2017-03-15 17:08:24.304473	2017-03-15 17:08:24.304621		\N
6	Teresa	Uebber	Teresa	Teresa	teresa.uebber@uni-duesseldorf.de	f	$2a$10$.307sXLjtryWMZUSW3IgnOct9ryyK4uyyc08Y8cuCJWEB8IHoAYle	1	2017-03-15 17:08:24.304299	2017-03-15 17:08:24.304473	2017-03-15 17:08:24.304621		\N
7	Bob	Bubbles	Bob	Bob	tobias.krauthoff+dbas.usert31@gmail.com	n	$2a$10$dfbfF3sNzsDRsAZoMDzR5et75H6BlRbJR9.eUYibhZir4F4zHUAQO	1	2017-03-15 17:08:24.304299	2017-03-15 17:08:24.304473	2017-03-15 17:08:24.304621		\N
8	Pascal	Lux	Pascal	Pascal	tobias.krauthoff+dbas.usert00@gmail.com	m	$2a$10$dfbfF3sNzsDRsAZoMDzR5et75H6BlRbJR9.eUYibhZir4F4zHUAQO	3	2017-03-15 17:08:24.304299	2017-03-15 17:08:24.304473	2017-03-15 17:08:24.304621		\N
9	Kurt	Hecht	Kurt	Kurt	tobias.krauthoff+dbas.usert01@gmail.com	m	$2a$10$dfbfF3sNzsDRsAZoMDzR5et75H6BlRbJR9.eUYibhZir4F4zHUAQO	3	2017-03-15 17:08:24.304299	2017-03-15 17:08:24.304473	2017-03-15 17:08:24.304621		\N
10	Torben	Hartl	Torben	Torben	tobias.krauthoff+dbas.usert02@gmail.com	m	$2a$10$dfbfF3sNzsDRsAZoMDzR5et75H6BlRbJR9.eUYibhZir4F4zHUAQO	3	2017-03-15 17:08:24.304299	2017-03-15 17:08:24.304473	2017-03-15 17:08:24.304621		\N
11	Thorsten	Scherer	Thorsten	Thorsten	tobias.krauthoff+dbas.usert03@gmail.com	m	$2a$10$dfbfF3sNzsDRsAZoMDzR5et75H6BlRbJR9.eUYibhZir4F4zHUAQO	3	2017-03-15 17:08:24.304299	2017-03-15 17:08:24.304473	2017-03-15 17:08:24.304621		\N
12	Friedrich	Schutte	Friedrich	Friedrich	tobias.krauthoff+dbas.usert04@gmail.com	m	$2a$10$dfbfF3sNzsDRsAZoMDzR5et75H6BlRbJR9.eUYibhZir4F4zHUAQO	3	2017-03-15 17:08:24.304299	2017-03-15 17:08:24.304473	2017-03-15 17:08:24.304621		\N
13	Aayden	Westermann	Aayden	Aayden	tobias.krauthoff+dbas.usert05@gmail.com	m	$2a$10$dfbfF3sNzsDRsAZoMDzR5et75H6BlRbJR9.eUYibhZir4F4zHUAQO	3	2017-03-15 17:08:24.304299	2017-03-15 17:08:24.304473	2017-03-15 17:08:24.304621		\N
14	Hermann	Grasshoff	Hermann	Hermann	tobias.krauthoff+dbas.usert06@gmail.com	m	$2a$10$dfbfF3sNzsDRsAZoMDzR5et75H6BlRbJR9.eUYibhZir4F4zHUAQO	3	2017-03-15 17:08:24.304299	2017-03-15 17:08:24.304473	2017-03-15 17:08:24.304621		\N
15	Wolf	Himmler	Wolf	Wolf	tobias.krauthoff+dbas.usert07@gmail.com	m	$2a$10$dfbfF3sNzsDRsAZoMDzR5et75H6BlRbJR9.eUYibhZir4F4zHUAQO	3	2017-03-15 17:08:24.304299	2017-03-15 17:08:24.304473	2017-03-15 17:08:24.304621		\N
16	Jakob	Winter	Jakob	Jakob	tobias.krauthoff+dbas.usert08@gmail.com	m	$2a$10$dfbfF3sNzsDRsAZoMDzR5et75H6BlRbJR9.eUYibhZir4F4zHUAQO	3	2017-03-15 17:08:24.304299	2017-03-15 17:08:24.304473	2017-03-15 17:08:24.304621		\N
17	Alwin	Wechter	Alwin	Alwin	tobias.krauthoff+dbas.usert09@gmail.com	m	$2a$10$dfbfF3sNzsDRsAZoMDzR5et75H6BlRbJR9.eUYibhZir4F4zHUAQO	3	2017-03-15 17:08:24.304299	2017-03-15 17:08:24.304473	2017-03-15 17:08:24.304621		\N
18	Walter	Weisser	Walter	Walter	tobias.krauthoff+dbas.usert10@gmail.com	m	$2a$10$dfbfF3sNzsDRsAZoMDzR5et75H6BlRbJR9.eUYibhZir4F4zHUAQO	3	2017-03-15 17:08:24.304299	2017-03-15 17:08:24.304473	2017-03-15 17:08:24.304621		\N
19	Volker	Keitel	Volker	Volker	tobias.krauthoff+dbas.usert11@gmail.com	m	$2a$10$dfbfF3sNzsDRsAZoMDzR5et75H6BlRbJR9.eUYibhZir4F4zHUAQO	3	2017-03-15 17:08:24.304299	2017-03-15 17:08:24.304473	2017-03-15 17:08:24.304621		\N
20	Benedikt	Feuerstein	Benedikt	Benedikt	tobias.krauthoff+dbas.usert12@gmail.com	m	$2a$10$dfbfF3sNzsDRsAZoMDzR5et75H6BlRbJR9.eUYibhZir4F4zHUAQO	3	2017-03-15 17:08:24.304299	2017-03-15 17:08:24.304473	2017-03-15 17:08:24.304621		\N
21	Engelbert	Gottlieb	Engelbert	Engelbert	tobias.krauthoff+dbas.usert13@gmail.com	m	$2a$10$dfbfF3sNzsDRsAZoMDzR5et75H6BlRbJR9.eUYibhZir4F4zHUAQO	3	2017-03-15 17:08:24.304299	2017-03-15 17:08:24.304473	2017-03-15 17:08:24.304621		\N
22	Elias	Auerbach	Elias	Elias	tobias.krauthoff+dbas.usert14@gmail.com	m	$2a$10$dfbfF3sNzsDRsAZoMDzR5et75H6BlRbJR9.eUYibhZir4F4zHUAQO	3	2017-03-15 17:08:24.304299	2017-03-15 17:08:24.304473	2017-03-15 17:08:24.304621		\N
23	Rupert	Wenz	Rupert	Rupert	tobias.krauthoff+dbas.usert15@gmail.com	m	$2a$10$dfbfF3sNzsDRsAZoMDzR5et75H6BlRbJR9.eUYibhZir4F4zHUAQO	3	2017-03-15 17:08:24.304299	2017-03-15 17:08:24.304473	2017-03-15 17:08:24.304621		\N
24	Marga	Wegscheider	Marga	Marga	tobias.krauthoff+dbas.usert16@gmail.com	f	$2a$10$dfbfF3sNzsDRsAZoMDzR5et75H6BlRbJR9.eUYibhZir4F4zHUAQO	3	2017-03-15 17:08:24.304299	2017-03-15 17:08:24.304473	2017-03-15 17:08:24.304621		\N
25	Larissa	Clauberg	Larissa	Larissa	tobias.krauthoff+dbas.usert17@gmail.com	f	$2a$10$dfbfF3sNzsDRsAZoMDzR5et75H6BlRbJR9.eUYibhZir4F4zHUAQO	3	2017-03-15 17:08:24.304299	2017-03-15 17:08:24.304473	2017-03-15 17:08:24.304621		\N
26	Emmi	Rosch	Emmi	Emmi	tobias.krauthoff+dbas.usert18@gmail.com	f	$2a$10$dfbfF3sNzsDRsAZoMDzR5et75H6BlRbJR9.eUYibhZir4F4zHUAQO	3	2017-03-15 17:08:24.304299	2017-03-15 17:08:24.304473	2017-03-15 17:08:24.304621		\N
27	Konstanze	Krebs	Konstanze	Konstanze	tobias.krauthoff+dbas.usert19@gmail.com	f	$2a$10$dfbfF3sNzsDRsAZoMDzR5et75H6BlRbJR9.eUYibhZir4F4zHUAQO	3	2017-03-15 17:08:24.304299	2017-03-15 17:08:24.304473	2017-03-15 17:08:24.304621		\N
28	Catrin	Fahnrich	Catrin	Catrin	tobias.krauthoff+dbas.usert20@gmail.com	f	$2a$10$dfbfF3sNzsDRsAZoMDzR5et75H6BlRbJR9.eUYibhZir4F4zHUAQO	3	2017-03-15 17:08:24.304299	2017-03-15 17:08:24.304473	2017-03-15 17:08:24.304621		\N
29	Antonia	Bartram	Antonia	Antonia	tobias.krauthoff+dbas.usert21@gmail.com	f	$2a$10$dfbfF3sNzsDRsAZoMDzR5et75H6BlRbJR9.eUYibhZir4F4zHUAQO	3	2017-03-15 17:08:24.304299	2017-03-15 17:08:24.304473	2017-03-15 17:08:24.304621		\N
30	Nora	Kempf	Nora	Nora	tobias.krauthoff+dbas.usert22@gmail.com	f	$2a$10$dfbfF3sNzsDRsAZoMDzR5et75H6BlRbJR9.eUYibhZir4F4zHUAQO	3	2017-03-15 17:08:24.304299	2017-03-15 17:08:24.304473	2017-03-15 17:08:24.304621		\N
31	Julia	Wetter	Julia	Julia	tobias.krauthoff+dbas.usert23@gmail.com	f	$2a$10$dfbfF3sNzsDRsAZoMDzR5et75H6BlRbJR9.eUYibhZir4F4zHUAQO	3	2017-03-15 17:08:24.304299	2017-03-15 17:08:24.304473	2017-03-15 17:08:24.304621		\N
32	Jutta	Munch	Jutta	Jutta	tobias.krauthoff+dbas.usert24@gmail.com	f	$2a$10$dfbfF3sNzsDRsAZoMDzR5et75H6BlRbJR9.eUYibhZir4F4zHUAQO	3	2017-03-15 17:08:24.304299	2017-03-15 17:08:24.304473	2017-03-15 17:08:24.304621		\N
33	Helga	Heilmann	Helga	Helga	tobias.krauthoff+dbas.usert25@gmail.com	f	$2a$10$dfbfF3sNzsDRsAZoMDzR5et75H6BlRbJR9.eUYibhZir4F4zHUAQO	3	2017-03-15 17:08:24.304299	2017-03-15 17:08:24.304473	2017-03-15 17:08:24.304621		\N
34	Denise	Tietjen	Denise	Denise	tobias.krauthoff+dbas.usert26@gmail.com	f	$2a$10$dfbfF3sNzsDRsAZoMDzR5et75H6BlRbJR9.eUYibhZir4F4zHUAQO	3	2017-03-15 17:08:24.304299	2017-03-15 17:08:24.304473	2017-03-15 17:08:24.304621		\N
35	Hanne	Beckmann	Hanne	Hanne	tobias.krauthoff+dbas.usert27@gmail.com	f	$2a$10$dfbfF3sNzsDRsAZoMDzR5et75H6BlRbJR9.eUYibhZir4F4zHUAQO	3	2017-03-15 17:08:24.304299	2017-03-15 17:08:24.304473	2017-03-15 17:08:24.304621		\N
36	Elly	Landauer	Elly	Elly	tobias.krauthoff+dbas.usert28@gmail.com	f	$2a$10$dfbfF3sNzsDRsAZoMDzR5et75H6BlRbJR9.eUYibhZir4F4zHUAQO	3	2017-03-15 17:08:24.304299	2017-03-15 17:08:24.304473	2017-03-15 17:08:24.304621		\N
37	Sybille	Redlich	Sybille	Sybille	tobias.krauthoff+dbas.usert29@gmail.com	f	$2a$10$dfbfF3sNzsDRsAZoMDzR5et75H6BlRbJR9.eUYibhZir4F4zHUAQO	3	2017-03-15 17:08:24.304299	2017-03-15 17:08:24.304473	2017-03-15 17:08:24.304621		\N
38	Ingeburg	Fischer	Ingeburg	Ingeburg	tobias.krauthoff+dbas.usert30@gmail.com	f	$2a$10$dfbfF3sNzsDRsAZoMDzR5et75H6BlRbJR9.eUYibhZir4F4zHUAQO	3	2017-03-15 17:08:24.304299	2017-03-15 17:08:24.304473	2017-03-15 17:08:24.304621		\N
\.


--
-- Name: users_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('users_uid_seq', 38, true);


--
-- Name: arguments_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY arguments
    ADD CONSTRAINT arguments_pkey PRIMARY KEY (uid);


--
-- Name: clicked_arguments_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY clicked_arguments
    ADD CONSTRAINT clicked_arguments_pkey PRIMARY KEY (uid);


--
-- Name: clicked_statements_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY clicked_statements
    ADD CONSTRAINT clicked_statements_pkey PRIMARY KEY (uid);


--
-- Name: groups_name_key; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY groups
    ADD CONSTRAINT groups_name_key UNIQUE (name);


--
-- Name: groups_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY groups
    ADD CONSTRAINT groups_pkey PRIMARY KEY (uid);


--
-- Name: history_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY history
    ADD CONSTRAINT history_pkey PRIMARY KEY (uid);


--
-- Name: issues_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY issues
    ADD CONSTRAINT issues_pkey PRIMARY KEY (uid);


--
-- Name: languages_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY languages
    ADD CONSTRAINT languages_pkey PRIMARY KEY (uid);


--
-- Name: languages_ui_locales_key; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY languages
    ADD CONSTRAINT languages_ui_locales_key UNIQUE (ui_locales);


--
-- Name: last_reviewers_delete_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY last_reviewers_delete
    ADD CONSTRAINT last_reviewers_delete_pkey PRIMARY KEY (uid);


--
-- Name: last_reviewers_duplicates_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY last_reviewers_duplicates
    ADD CONSTRAINT last_reviewers_duplicates_pkey PRIMARY KEY (uid);


--
-- Name: last_reviewers_edit_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY last_reviewers_edit
    ADD CONSTRAINT last_reviewers_edit_pkey PRIMARY KEY (uid);


--
-- Name: last_reviewers_optimization_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY last_reviewers_optimization
    ADD CONSTRAINT last_reviewers_optimization_pkey PRIMARY KEY (uid);


--
-- Name: marked_arguments_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY marked_arguments
    ADD CONSTRAINT marked_arguments_pkey PRIMARY KEY (uid);


--
-- Name: marked_statements_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY marked_statements
    ADD CONSTRAINT marked_statements_pkey PRIMARY KEY (uid);


--
-- Name: messages_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY messages
    ADD CONSTRAINT messages_pkey PRIMARY KEY (uid);


--
-- Name: optimization_review_locks_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY optimization_review_locks
    ADD CONSTRAINT optimization_review_locks_pkey PRIMARY KEY (author_uid);


--
-- Name: premisegroups_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY premisegroups
    ADD CONSTRAINT premisegroups_pkey PRIMARY KEY (uid);


--
-- Name: premises_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY premises
    ADD CONSTRAINT premises_pkey PRIMARY KEY (uid);


--
-- Name: reputation_history_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY reputation_history
    ADD CONSTRAINT reputation_history_pkey PRIMARY KEY (uid);


--
-- Name: reputation_reasons_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY reputation_reasons
    ADD CONSTRAINT reputation_reasons_pkey PRIMARY KEY (uid);


--
-- Name: reputation_reasons_reason_key; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY reputation_reasons
    ADD CONSTRAINT reputation_reasons_reason_key UNIQUE (reason);


--
-- Name: review_canceled_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_canceled
    ADD CONSTRAINT review_canceled_pkey PRIMARY KEY (uid);


--
-- Name: review_delete_reasons_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_delete_reasons
    ADD CONSTRAINT review_delete_reasons_pkey PRIMARY KEY (uid);


--
-- Name: review_delete_reasons_reason_key; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_delete_reasons
    ADD CONSTRAINT review_delete_reasons_reason_key UNIQUE (reason);


--
-- Name: review_deletes_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_deletes
    ADD CONSTRAINT review_deletes_pkey PRIMARY KEY (uid);


--
-- Name: review_duplicates_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_duplicates
    ADD CONSTRAINT review_duplicates_pkey PRIMARY KEY (uid);


--
-- Name: review_edit_values_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_edit_values
    ADD CONSTRAINT review_edit_values_pkey PRIMARY KEY (uid);


--
-- Name: review_edits_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_edits
    ADD CONSTRAINT review_edits_pkey PRIMARY KEY (uid);


--
-- Name: review_optimizations_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_optimizations
    ADD CONSTRAINT review_optimizations_pkey PRIMARY KEY (uid);


--
-- Name: revoked_content_history_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY revoked_content_history
    ADD CONSTRAINT revoked_content_history_pkey PRIMARY KEY (uid);


--
-- Name: revoked_content_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY revoked_content
    ADD CONSTRAINT revoked_content_pkey PRIMARY KEY (uid);


--
-- Name: revoked_duplicate_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY revoked_duplicate
    ADD CONSTRAINT revoked_duplicate_pkey PRIMARY KEY (uid);


--
-- Name: rss_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY rss
    ADD CONSTRAINT rss_pkey PRIMARY KEY (uid);


--
-- Name: seen_arguments_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY seen_arguments
    ADD CONSTRAINT seen_arguments_pkey PRIMARY KEY (uid);


--
-- Name: seen_statements_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY seen_statements
    ADD CONSTRAINT seen_statements_pkey PRIMARY KEY (uid);


--
-- Name: settings_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY settings
    ADD CONSTRAINT settings_pkey PRIMARY KEY (author_uid);


--
-- Name: statement_references_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY statement_references
    ADD CONSTRAINT statement_references_pkey PRIMARY KEY (uid);


--
-- Name: statements_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY statements
    ADD CONSTRAINT statements_pkey PRIMARY KEY (uid);


--
-- Name: textversions_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY textversions
    ADD CONSTRAINT textversions_pkey PRIMARY KEY (uid);


--
-- Name: users_nickname_key; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_nickname_key UNIQUE (nickname);


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (uid);


--
-- Name: arguments_argument_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY arguments
    ADD CONSTRAINT arguments_argument_uid_fkey FOREIGN KEY (argument_uid) REFERENCES arguments(uid);


--
-- Name: arguments_author_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY arguments
    ADD CONSTRAINT arguments_author_uid_fkey FOREIGN KEY (author_uid) REFERENCES users(uid);


--
-- Name: arguments_conclusion_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY arguments
    ADD CONSTRAINT arguments_conclusion_uid_fkey FOREIGN KEY (conclusion_uid) REFERENCES statements(uid);


--
-- Name: arguments_issue_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY arguments
    ADD CONSTRAINT arguments_issue_uid_fkey FOREIGN KEY (issue_uid) REFERENCES issues(uid);


--
-- Name: arguments_premisesgroup_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY arguments
    ADD CONSTRAINT arguments_premisesgroup_uid_fkey FOREIGN KEY (premisesgroup_uid) REFERENCES premisegroups(uid);


--
-- Name: clicked_arguments_argument_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY clicked_arguments
    ADD CONSTRAINT clicked_arguments_argument_uid_fkey FOREIGN KEY (argument_uid) REFERENCES arguments(uid);


--
-- Name: clicked_arguments_author_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY clicked_arguments
    ADD CONSTRAINT clicked_arguments_author_uid_fkey FOREIGN KEY (author_uid) REFERENCES users(uid);


--
-- Name: clicked_statements_author_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY clicked_statements
    ADD CONSTRAINT clicked_statements_author_uid_fkey FOREIGN KEY (author_uid) REFERENCES users(uid);


--
-- Name: clicked_statements_statement_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY clicked_statements
    ADD CONSTRAINT clicked_statements_statement_uid_fkey FOREIGN KEY (statement_uid) REFERENCES statements(uid);


--
-- Name: history_author_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY history
    ADD CONSTRAINT history_author_uid_fkey FOREIGN KEY (author_uid) REFERENCES users(uid);


--
-- Name: issues_author_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY issues
    ADD CONSTRAINT issues_author_uid_fkey FOREIGN KEY (author_uid) REFERENCES users(uid);


--
-- Name: issues_lang_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY issues
    ADD CONSTRAINT issues_lang_uid_fkey FOREIGN KEY (lang_uid) REFERENCES languages(uid);


--
-- Name: last_reviewers_delete_review_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY last_reviewers_delete
    ADD CONSTRAINT last_reviewers_delete_review_uid_fkey FOREIGN KEY (review_uid) REFERENCES review_deletes(uid);


--
-- Name: last_reviewers_delete_reviewer_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY last_reviewers_delete
    ADD CONSTRAINT last_reviewers_delete_reviewer_uid_fkey FOREIGN KEY (reviewer_uid) REFERENCES users(uid);


--
-- Name: last_reviewers_duplicates_review_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY last_reviewers_duplicates
    ADD CONSTRAINT last_reviewers_duplicates_review_uid_fkey FOREIGN KEY (review_uid) REFERENCES review_duplicates(uid);


--
-- Name: last_reviewers_duplicates_reviewer_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY last_reviewers_duplicates
    ADD CONSTRAINT last_reviewers_duplicates_reviewer_uid_fkey FOREIGN KEY (reviewer_uid) REFERENCES users(uid);


--
-- Name: last_reviewers_edit_review_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY last_reviewers_edit
    ADD CONSTRAINT last_reviewers_edit_review_uid_fkey FOREIGN KEY (review_uid) REFERENCES review_edits(uid);


--
-- Name: last_reviewers_edit_reviewer_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY last_reviewers_edit
    ADD CONSTRAINT last_reviewers_edit_reviewer_uid_fkey FOREIGN KEY (reviewer_uid) REFERENCES users(uid);


--
-- Name: last_reviewers_optimization_review_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY last_reviewers_optimization
    ADD CONSTRAINT last_reviewers_optimization_review_uid_fkey FOREIGN KEY (review_uid) REFERENCES review_optimizations(uid);


--
-- Name: last_reviewers_optimization_reviewer_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY last_reviewers_optimization
    ADD CONSTRAINT last_reviewers_optimization_reviewer_uid_fkey FOREIGN KEY (reviewer_uid) REFERENCES users(uid);


--
-- Name: marked_arguments_argument_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY marked_arguments
    ADD CONSTRAINT marked_arguments_argument_uid_fkey FOREIGN KEY (argument_uid) REFERENCES arguments(uid);


--
-- Name: marked_arguments_author_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY marked_arguments
    ADD CONSTRAINT marked_arguments_author_uid_fkey FOREIGN KEY (author_uid) REFERENCES users(uid);


--
-- Name: marked_statements_author_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY marked_statements
    ADD CONSTRAINT marked_statements_author_uid_fkey FOREIGN KEY (author_uid) REFERENCES users(uid);


--
-- Name: marked_statements_statement_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY marked_statements
    ADD CONSTRAINT marked_statements_statement_uid_fkey FOREIGN KEY (statement_uid) REFERENCES statements(uid);


--
-- Name: messages_from_author_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY messages
    ADD CONSTRAINT messages_from_author_uid_fkey FOREIGN KEY (from_author_uid) REFERENCES users(uid);


--
-- Name: messages_to_author_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY messages
    ADD CONSTRAINT messages_to_author_uid_fkey FOREIGN KEY (to_author_uid) REFERENCES users(uid);


--
-- Name: optimization_review_locks_author_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY optimization_review_locks
    ADD CONSTRAINT optimization_review_locks_author_uid_fkey FOREIGN KEY (author_uid) REFERENCES users(uid);


--
-- Name: optimization_review_locks_review_optimization_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY optimization_review_locks
    ADD CONSTRAINT optimization_review_locks_review_optimization_uid_fkey FOREIGN KEY (review_optimization_uid) REFERENCES review_optimizations(uid);


--
-- Name: premisegroups_author_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY premisegroups
    ADD CONSTRAINT premisegroups_author_uid_fkey FOREIGN KEY (author_uid) REFERENCES users(uid);


--
-- Name: premises_author_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY premises
    ADD CONSTRAINT premises_author_uid_fkey FOREIGN KEY (author_uid) REFERENCES users(uid);


--
-- Name: premises_issue_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY premises
    ADD CONSTRAINT premises_issue_uid_fkey FOREIGN KEY (issue_uid) REFERENCES issues(uid);


--
-- Name: premises_premisesgroup_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY premises
    ADD CONSTRAINT premises_premisesgroup_uid_fkey FOREIGN KEY (premisesgroup_uid) REFERENCES premisegroups(uid);


--
-- Name: premises_statement_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY premises
    ADD CONSTRAINT premises_statement_uid_fkey FOREIGN KEY (statement_uid) REFERENCES statements(uid);


--
-- Name: reputation_history_reputation_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY reputation_history
    ADD CONSTRAINT reputation_history_reputation_uid_fkey FOREIGN KEY (reputation_uid) REFERENCES reputation_reasons(uid);


--
-- Name: reputation_history_reputator_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY reputation_history
    ADD CONSTRAINT reputation_history_reputator_uid_fkey FOREIGN KEY (reputator_uid) REFERENCES users(uid);


--
-- Name: review_canceled_author_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_canceled
    ADD CONSTRAINT review_canceled_author_uid_fkey FOREIGN KEY (author_uid) REFERENCES users(uid);


--
-- Name: review_canceled_review_delete_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_canceled
    ADD CONSTRAINT review_canceled_review_delete_uid_fkey FOREIGN KEY (review_delete_uid) REFERENCES review_deletes(uid);


--
-- Name: review_canceled_review_duplicate_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_canceled
    ADD CONSTRAINT review_canceled_review_duplicate_uid_fkey FOREIGN KEY (review_duplicate_uid) REFERENCES review_duplicates(uid);


--
-- Name: review_canceled_review_edit_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_canceled
    ADD CONSTRAINT review_canceled_review_edit_uid_fkey FOREIGN KEY (review_edit_uid) REFERENCES review_edits(uid);


--
-- Name: review_canceled_review_optimization_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_canceled
    ADD CONSTRAINT review_canceled_review_optimization_uid_fkey FOREIGN KEY (review_optimization_uid) REFERENCES review_optimizations(uid);


--
-- Name: review_deletes_argument_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_deletes
    ADD CONSTRAINT review_deletes_argument_uid_fkey FOREIGN KEY (argument_uid) REFERENCES arguments(uid);


--
-- Name: review_deletes_detector_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_deletes
    ADD CONSTRAINT review_deletes_detector_uid_fkey FOREIGN KEY (detector_uid) REFERENCES users(uid);


--
-- Name: review_deletes_reason_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_deletes
    ADD CONSTRAINT review_deletes_reason_uid_fkey FOREIGN KEY (reason_uid) REFERENCES review_delete_reasons(uid);


--
-- Name: review_deletes_statement_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_deletes
    ADD CONSTRAINT review_deletes_statement_uid_fkey FOREIGN KEY (statement_uid) REFERENCES statements(uid);


--
-- Name: review_duplicates_detector_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_duplicates
    ADD CONSTRAINT review_duplicates_detector_uid_fkey FOREIGN KEY (detector_uid) REFERENCES users(uid);


--
-- Name: review_duplicates_duplicate_statement_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_duplicates
    ADD CONSTRAINT review_duplicates_duplicate_statement_uid_fkey FOREIGN KEY (duplicate_statement_uid) REFERENCES statements(uid);


--
-- Name: review_duplicates_original_statement_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_duplicates
    ADD CONSTRAINT review_duplicates_original_statement_uid_fkey FOREIGN KEY (original_statement_uid) REFERENCES statements(uid);


--
-- Name: review_edit_values_review_edit_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_edit_values
    ADD CONSTRAINT review_edit_values_review_edit_uid_fkey FOREIGN KEY (review_edit_uid) REFERENCES review_edits(uid);


--
-- Name: review_edit_values_statement_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_edit_values
    ADD CONSTRAINT review_edit_values_statement_uid_fkey FOREIGN KEY (statement_uid) REFERENCES statements(uid);


--
-- Name: review_edits_argument_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_edits
    ADD CONSTRAINT review_edits_argument_uid_fkey FOREIGN KEY (argument_uid) REFERENCES arguments(uid);


--
-- Name: review_edits_detector_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_edits
    ADD CONSTRAINT review_edits_detector_uid_fkey FOREIGN KEY (detector_uid) REFERENCES users(uid);


--
-- Name: review_edits_statement_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_edits
    ADD CONSTRAINT review_edits_statement_uid_fkey FOREIGN KEY (statement_uid) REFERENCES statements(uid);


--
-- Name: review_optimizations_argument_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_optimizations
    ADD CONSTRAINT review_optimizations_argument_uid_fkey FOREIGN KEY (argument_uid) REFERENCES arguments(uid);


--
-- Name: review_optimizations_detector_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_optimizations
    ADD CONSTRAINT review_optimizations_detector_uid_fkey FOREIGN KEY (detector_uid) REFERENCES users(uid);


--
-- Name: review_optimizations_statement_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_optimizations
    ADD CONSTRAINT review_optimizations_statement_uid_fkey FOREIGN KEY (statement_uid) REFERENCES statements(uid);


--
-- Name: revoked_content_argument_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY revoked_content
    ADD CONSTRAINT revoked_content_argument_uid_fkey FOREIGN KEY (argument_uid) REFERENCES arguments(uid);


--
-- Name: revoked_content_author_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY revoked_content
    ADD CONSTRAINT revoked_content_author_uid_fkey FOREIGN KEY (author_uid) REFERENCES users(uid);


--
-- Name: revoked_content_history_argument_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY revoked_content_history
    ADD CONSTRAINT revoked_content_history_argument_uid_fkey FOREIGN KEY (argument_uid) REFERENCES arguments(uid);


--
-- Name: revoked_content_history_new_author_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY revoked_content_history
    ADD CONSTRAINT revoked_content_history_new_author_uid_fkey FOREIGN KEY (new_author_uid) REFERENCES users(uid);


--
-- Name: revoked_content_history_old_author_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY revoked_content_history
    ADD CONSTRAINT revoked_content_history_old_author_uid_fkey FOREIGN KEY (old_author_uid) REFERENCES users(uid);


--
-- Name: revoked_content_history_textversion_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY revoked_content_history
    ADD CONSTRAINT revoked_content_history_textversion_uid_fkey FOREIGN KEY (textversion_uid) REFERENCES textversions(uid);


--
-- Name: revoked_content_statement_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY revoked_content
    ADD CONSTRAINT revoked_content_statement_uid_fkey FOREIGN KEY (statement_uid) REFERENCES statements(uid);


--
-- Name: revoked_duplicate_argument_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY revoked_duplicate
    ADD CONSTRAINT revoked_duplicate_argument_uid_fkey FOREIGN KEY (argument_uid) REFERENCES arguments(uid);


--
-- Name: revoked_duplicate_premise_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY revoked_duplicate
    ADD CONSTRAINT revoked_duplicate_premise_uid_fkey FOREIGN KEY (premise_uid) REFERENCES premises(uid);


--
-- Name: revoked_duplicate_review_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY revoked_duplicate
    ADD CONSTRAINT revoked_duplicate_review_uid_fkey FOREIGN KEY (review_uid) REFERENCES review_duplicates(uid);


--
-- Name: revoked_duplicate_statement_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY revoked_duplicate
    ADD CONSTRAINT revoked_duplicate_statement_uid_fkey FOREIGN KEY (statement_uid) REFERENCES statements(uid);


--
-- Name: rss_author_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY rss
    ADD CONSTRAINT rss_author_uid_fkey FOREIGN KEY (author_uid) REFERENCES users(uid);


--
-- Name: rss_issue_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY rss
    ADD CONSTRAINT rss_issue_uid_fkey FOREIGN KEY (issue_uid) REFERENCES issues(uid);


--
-- Name: seen_arguments_argument_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY seen_arguments
    ADD CONSTRAINT seen_arguments_argument_uid_fkey FOREIGN KEY (argument_uid) REFERENCES arguments(uid);


--
-- Name: seen_arguments_user_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY seen_arguments
    ADD CONSTRAINT seen_arguments_user_uid_fkey FOREIGN KEY (user_uid) REFERENCES users(uid);


--
-- Name: seen_statements_statement_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY seen_statements
    ADD CONSTRAINT seen_statements_statement_uid_fkey FOREIGN KEY (statement_uid) REFERENCES statements(uid);


--
-- Name: seen_statements_user_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY seen_statements
    ADD CONSTRAINT seen_statements_user_uid_fkey FOREIGN KEY (user_uid) REFERENCES users(uid);


--
-- Name: settings_author_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY settings
    ADD CONSTRAINT settings_author_uid_fkey FOREIGN KEY (author_uid) REFERENCES users(uid);


--
-- Name: settings_lang_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY settings
    ADD CONSTRAINT settings_lang_uid_fkey FOREIGN KEY (lang_uid) REFERENCES languages(uid);


--
-- Name: settings_last_topic_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY settings
    ADD CONSTRAINT settings_last_topic_uid_fkey FOREIGN KEY (last_topic_uid) REFERENCES issues(uid);


--
-- Name: statement_references_author_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY statement_references
    ADD CONSTRAINT statement_references_author_uid_fkey FOREIGN KEY (author_uid) REFERENCES users(uid);


--
-- Name: statement_references_issue_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY statement_references
    ADD CONSTRAINT statement_references_issue_uid_fkey FOREIGN KEY (issue_uid) REFERENCES issues(uid);


--
-- Name: statement_references_statement_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY statement_references
    ADD CONSTRAINT statement_references_statement_uid_fkey FOREIGN KEY (statement_uid) REFERENCES statements(uid);


--
-- Name: statements_issue_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY statements
    ADD CONSTRAINT statements_issue_uid_fkey FOREIGN KEY (issue_uid) REFERENCES issues(uid);


--
-- Name: statements_textversion_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY statements
    ADD CONSTRAINT statements_textversion_uid_fkey FOREIGN KEY (textversion_uid) REFERENCES textversions(uid);


--
-- Name: textversions_author_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY textversions
    ADD CONSTRAINT textversions_author_uid_fkey FOREIGN KEY (author_uid) REFERENCES users(uid);


--
-- Name: textversions_statement_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY textversions
    ADD CONSTRAINT textversions_statement_uid_fkey FOREIGN KEY (statement_uid) REFERENCES statements(uid);


--
-- Name: users_group_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_group_uid_fkey FOREIGN KEY (group_uid) REFERENCES groups(uid);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

\connect news

SET default_transaction_read_only = off;

--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.6
-- Dumped by pg_dump version 9.5.6

SET statement_timeout = 0;
SET lock_timeout = 0;
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
-- Name: uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY news ALTER COLUMN uid SET DEFAULT nextval('news_uid_seq'::regclass);


--
-- Data for Name: news; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY news (uid, title, author, date, news) FROM stdin;
1	Docker	Tobias Krauthoff	2017-02-09 00:00:00	The last weeks we have spend to make D-BAS more stable, writing some analyzers as well as dockerize everything. The complete project can be found on https://github.com/hhucn/dbas soon.
2	Experiment	Tobias Krauthoff	2017-02-09 00:00:00	Last week we finished our second experiment at our professorial chair. In short we are very happy with the results and with the first, bigger argumentation map created by inexperienced participants! Now we will fix a few smaller things and looking forward to out first field test!
3	Final version and Captachs	Tobias Krauthoff	2017-01-21 00:00:00	Today we submitted a journal paper about D-BAS and its implementation at Springers CSCW.
4	Final version and Captachs	Tobias Krauthoff	2017-01-03 00:00:00	We have a delayed christmas present for you. D-BAS reached it's first final version including reCAPTCHAS and several minor fixes!
5	Work goes on	Tobias Krauthoff	2016-11-29 00:00:00	After the positive feedback at COMMA16, we decided to do a first field tests with D-BAS at our university. Therefore we are working on current issues, so that we will releasing v1.0. soon.
6	COMMA16	Tobias Krauthoff	2016-09-14 00:00:00	Based on the hard work of the last month, we are attending the 6th International Conference on Computational Models of Argument (COMMA16) in Potsdam. There we are going to show the first demo of D-BAS and present the paper of Krauthoff T., Betz G., Baurmann M. & Mauve, M. (2016) "Dialog-Based Online Argumentation". Looking forward to see you!
7	Review Process	Tobias Krauthoff	2016-09-06 00:00:00	Our first version of the review-module is now online. Every confronting argument can be flagged regarding a specific reason now. Theses flagged argument will be reviewed by other participants, who have enough reputation. Have a look at the review-section!
8	Review Process	Tobias Krauthoff	2016-08-11 00:00:00	I regret that i have neglected the news section, but this is in your interest. In the meantime we are working on an graph view for our argumentation model, a review section for statements and we are improving the ways how we act with each kind of user input. Stay tuned!
9	Sidebar	Tobias Krauthoff	2016-07-05 00:00:00	Today we released a new text-based sidebar for a better experience. Have fun!
10	COMMA16	Tobias Krauthoff	2016-06-24 00:00:00	We are happy to announce, that our paper for the COMMA16 was accepted. In the meantime many little improvements as well as first user tests were done.
11	Development is going on	Tobias Krauthoff	2016-04-05 00:00:00	Recently we improved some features, which will be released in future. Firstly there will be an island view for every argument, where the participants can see every premise for current reactions. Secondly the opinion barometer is still under development. For a more recent update, have a look at our imprint.
12	History Management	Tobias Krauthoff	2016-04-26 00:00:00	We have changed D-BAS' history management. Now you can bookmark any link in any discussion and your history will always be with you!
13	COMMA16	Tobias Krauthoff	2016-04-05 00:00:00	After much work, testing and debugging, we now have version of D-BAS, which will be submitted  to <a href="http://www.ling.uni-potsdam.de/comma2016" target="_blank">COMMA 2016</a>.
14	Speech Bubble System	Tobias Krauthoff	2016-03-02 00:00:00	After one week of testing, we released a new minor version of D-BAS. Instead of the text presentation,we will use chat-like style :) Come on and try it! Additionally anonymous users will have a history now!
15	Notification System	Tobias Krauthoff	2016-02-16 00:00:00	Yesterday we have develope a minimal notification system. This system could send information to every author, if one of their statement was edited. More features are coming soon!
16	Premisegroups	Tobias Krauthoff	2016-02-09 00:00:00	Now we have a mechanism for unclear statements. For example the user enters "I want something because A and B". The we do not know, whether A and B must hold at the same time, or if she wants something when A or B holds. Therefore the system requests feedback.
17	Voting Model	Tobias Krauthoff	2016-01-05 00:00:00	Currently we are improving out model of voting for arguments as well as statements. Therefore we are working together with our colleagues from the theoretical computer science... because D-BAS data structure can be formalized to be compatible with frameworks of Dung.
18	API	Tobias Krauthoff	2016-01-29 00:00:00	Now D-BAS has an API. Just replace the "discuss"-tag in your url with api to get your current steps raw data.
19	Refactoring	Tobias Krauthoff	2016-01-27 00:00:00	D-BAS refactored the last two weeks. During this time, a lot of JavaScript was removed. Therefore D-BAS uses Chameleon with TAL in the Pyramid-Framework. So D-BAS will be more stable and faster. The next period all functions will be tested and recovered.
20	Island View and Pictures	Tobias Krauthoff	2016-01-06 00:00:00	D-BAS will be more personal and results driven. Therefore the new release has profile pictures for everyone. They are powered by gravatar and are based on a md5-hash of the users email. Next to this a new view was published - the island view. Do not be shy and try it in discussions ;-) Last improvement just collects the attacks and supports for arguments...this is needed for our next big thing :) Stay tuned!
21	Happy new Year	Tobias Krauthoff	2016-01-01 00:00:00	Frohes Neues Jahr ... Bonne Annee ... Happy New Year ... Feliz Ano Nuevo ... Feliz Ano Novo
22	Piwik	Tobias Krauthoff	2015-12-08 00:00:00	Today Piwik was installed. It will help to improve the services of D-BAS!
23	Logic improvements	Tobias Krauthoff	2015-12-01 00:00:00	Every week we try to improve the look and feel of the discussions navigation. Sometimes just a few words are edited, but on other day the logic itself gets an update. So keep on testing :)
24	Breadcrumbs	Tobias Krauthoff	2015-11-24 00:00:00	Now we have a breadcrumbs with shortcuts for every step in our discussion. This feature will be im improved soon!
25	Improved Bootstrapping	Tobias Krauthoff	2015-11-16 00:00:00	Bootstraping is one of the main challenges in discussion. Therefore we have a two-step process for this task!
26	Design Update	Tobias Krauthoff	2015-11-11 00:00:00	Today we released a new material-oriented design. Enjoy it!
27	Stable release	Tobias Krauthoff	2015-11-10 00:00:00	After two weeks of debugging, a first and stable version is online. Now we can start with the interesting things!
28	Different topics	Tobias Krauthoff	2015-10-15 00:00:00	Since today we can switch between different topics :) Unfortunately this feature is not really tested ;-)
29	First steps	Tobias Krauthoff	2014-12-01 00:00:00	I've started with with my PhD.
30	Start	Tobias Krauthoff	2015-04-14 00:00:00	I've started with the Prototype.
31	First mockup	Tobias Krauthoff	2015-05-01 00:00:00	The webpage has now a contact, login and register site.
32	Page is growing	Tobias Krauthoff	2015-05-05 00:00:00	The contact page is now working as well as the password-request option.
33	First set of tests	Tobias Krauthoff	2015-05-06 00:00:00	Finished first set of unit- and integration tests for the database and frontend.
34	System will be build up	Tobias Krauthoff	2015-05-01 00:00:00	Currently I am working a lot at the system. This work includes:<br><ul><li>frontend-design with CSS and jQuery</li><li>backend-development with pything</li><li>development of unit- and integration tests</li><li>a database scheme</li><li>validating and deserializing data with <a href="http://docs.pylonsproject.org/projects/colander/en/latest/">Colander</a></li><li>translating string with <a href="http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/i18n.html#localization-deployment-settings">internationalization</a></li></ul>
35	Workshop in Karlsruhe	Tobias Krauthoff	2015-05-07 00:00:00	The working group 'functionality' will drive to Karlsruhe for a workshop with Jun.-Prof. Dr. Betz as well as with C. Voigt until 08.05.2015. Our main topics will be the measurement of quality of discussions and the design of online-participation. I think, this will be very interesting!
36	About the Workshop in Karlsruhe	Tobias Krauthoff	2015-05-09 00:00:00	The workshop was very interesting. We have had very interesting talks and got much great feedback vom Jun.-Prof. Dr. Betz and Mr. Voigt. A repetition will be planed for the middle of july.
37	Settings	Tobias Krauthoff	2015-05-10 00:00:00	New part of the website is finished: a settings page for every user.
38	I18N + L10N	Tobias Krauthoff	2015-05-12 00:00:00	D-BAS, now with internationalization and translation.
39	No I18N + L10N	Tobias Krauthoff	2015-05-18 00:00:00	Interationalization and localization is much more difficult than described by pyramid. This has something todo with Chameleon 2, Lingua and Babel, so this feature has to wait.
40	New logic for inserting	Tobias Krauthoff	2015-10-14 00:00:00	Logic for inserting statements was redone. Every time, where the user can add information via a text area, only the area is visible, which is logically correct. Therefore the decisions are based on argumentation theory.
41	JS Starts	Tobias Krauthoff	2015-05-18 00:00:00	Today started the funny part about the dialog based part, embedded in the content page.
42	Tests and JS	Tobias Krauthoff	2015-05-26 00:00:00	Front-end tests with Splinter are now finished. They are great and easy to manage. Additionally I'am working on JS, so we can navigate in a static graph. Next to this, the I18N is waiting...
43	Sharing	Tobias Krauthoff	2015-05-27 00:00:00	Every news can now be shared via FB, G+, Twitter and Mail. Not very important, but in some kind it is...
44	Admin Interface	Tobias Krauthoff	2015-05-29 00:00:00	Everything is growing, we have now a little admin interface and a navigation for the discussion is finished, but this is very basic and simple
45	Workshop	Tobias Krauthoff	2015-05-27 00:00:00	Today: A new workshop at the O.A.S.E. :)
46	Simple Navigation ready	Tobias Krauthoff	2015-06-09 00:00:00	First beta of D-BAS navigation is now ready. Within this kind the user will be permanently confronted with arguments, which have a attack relation to the current selected argument/position. For an justification the user can select out of all arguments, which have a attack relation to the 'attacking' argument. Unfortunately the support-relation are currently useless except for the justification for the position at start.
47	Simple Navigation was improved	Tobias Krauthoff	2015-06-19 00:00:00	Because the first kind of navigation was finished recently, D-BAS is now dynamically. That means, that each user can add positions and arguments on his own.<br><i>Open issues</i> are i18n, a framework for JS-tests as well as the content of the popups.
48	Edit/Changelog	Tobias Krauthoff	2015-06-24 00:00:00	Now, each user can edit positions and arguments. All changes will be saved and can be watched. Future work is the chance to edit the relations between positions.
49	Session Management / CSRF	Tobias Krauthoff	2015-06-25 00:00:00	D-BAS is no able to manage a session as well as it has protection against CSRF.
50	Design & Research	Tobias Krauthoff	2015-07-13 00:00:00	D-BAS is still under construction. Meanwhile the index page was recreated and we are improving our algorithm for the guided view mode. Next to this we are inventing a bunch of metrics for measuring the quality of discussion in several software programs.
51	i18n	Tobias Krauthoff	2015-07-22 00:00:00	Still working on i18n-problems of chameleon templates due to lingua. If this is fixed, i18n of jQuery will happen. Afterwards l10n will take place.
52	i18n/l10n	Tobias Krauthoff	2015-07-28 00:00:00	Internationalization is now working :)
53	Long time, no see!	Tobias Krauthoff	2015-08-31 00:00:00	In the mean time we have developed a new, better, more logically data structure. Additionally the navigation was refreshed.
54	New URL-Schemes	Tobias Krauthoff	2015-09-01 00:00:00	Now D-BAS has unique urls for the discussion, therefore these urls can be shared.
55	Vacation done	Tobias Krauthoff	2015-09-23 00:00:00	After two and a half weeks of vacation a new feature was done. Hence anonymous users can participate, the discussion is open for all, but committing and editing statements is for registered users only.
56	Anonymous users after vacation	Tobias Krauthoff	2015-09-24 00:00:00	After two and a half week of vacation we have a new feature. The discussion is now available for anonymous users, therefore everyone can participate, but only registered users can make and edit statements.
\.


--
-- Name: news_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('news_uid_seq', 56, true);


--
-- Name: news_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY news
    ADD CONSTRAINT news_pkey PRIMARY KEY (uid);


--
-- Name: news; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA news FROM PUBLIC;
REVOKE ALL ON SCHEMA news FROM postgres;
GRANT ALL ON SCHEMA news TO postgres;
GRANT ALL ON SCHEMA news TO writer;


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

\connect postgres

SET default_transaction_read_only = off;

--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.6
-- Dumped by pg_dump version 9.5.6

SET statement_timeout = 0;
SET lock_timeout = 0;
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


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


SET search_path = public, pg_catalog;

--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: public; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public REVOKE ALL ON TABLES  FROM PUBLIC;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public REVOKE ALL ON TABLES  FROM postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT ALL ON TABLES  TO writer;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT SELECT ON TABLES  TO read_only_discussion;


--
-- PostgreSQL database dump complete
--

\connect template1

SET default_transaction_read_only = off;

--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.6
-- Dumped by pg_dump version 9.5.6

SET statement_timeout = 0;
SET lock_timeout = 0;
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
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database cluster dump complete
--

