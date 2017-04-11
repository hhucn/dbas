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

-- Dumped from database version 9.6.2
-- Dumped by pg_dump version 9.6.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
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

GRANT ALL ON SCHEMA beaker TO writer;


--
-- PostgreSQL database dump complete
--

\connect discussion

SET default_transaction_read_only = off;

--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.2
-- Dumped by pg_dump version 9.6.2

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
-- Name: last_reviewers_optimization uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY last_reviewers_optimization ALTER COLUMN uid SET DEFAULT nextval('last_reviewers_optimization_uid_seq'::regclass);


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
-- Name: review_optimizations uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_optimizations ALTER COLUMN uid SET DEFAULT nextval('review_optimizations_uid_seq'::regclass);


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
15	1	38	2017-03-21 05:39:56.148667	f	t
16	1	19	2017-04-08 05:39:56.148767	f	t
17	1	29	2017-03-17 05:39:56.148805	f	t
18	2	12	2017-03-27 05:39:56.14884	t	t
19	2	22	2017-03-17 05:39:56.14887	t	t
20	2	21	2017-03-31 05:39:56.1489	t	t
21	2	29	2017-04-01 05:39:56.148929	t	t
22	2	26	2017-03-21 05:39:56.148957	t	t
23	2	10	2017-04-03 05:39:56.148986	t	t
24	2	30	2017-04-05 05:39:56.149013	t	t
25	2	26	2017-03-22 05:39:56.14904	f	t
26	2	24	2017-03-30 05:39:56.149067	f	t
27	2	38	2017-03-19 05:39:56.149096	f	t
28	2	21	2017-04-10 05:39:56.149124	f	t
29	2	25	2017-03-19 05:39:56.149153	f	t
30	3	35	2017-04-09 05:39:56.149181	t	t
31	3	15	2017-04-03 05:39:56.149209	t	t
32	3	11	2017-03-30 05:39:56.149237	t	t
33	3	21	2017-04-01 05:39:56.149264	t	t
34	3	18	2017-03-19 05:39:56.149299	t	t
35	3	20	2017-04-09 05:39:56.149344	t	t
36	3	27	2017-03-27 05:39:56.149391	f	t
37	3	16	2017-03-30 05:39:56.149453	f	t
38	3	33	2017-03-25 05:39:56.149501	f	t
39	3	22	2017-03-26 05:39:56.149529	f	t
40	3	38	2017-03-18 05:39:56.149556	f	t
41	3	10	2017-04-06 05:39:56.149584	f	t
42	3	30	2017-03-26 05:39:56.149611	f	t
43	3	12	2017-04-10 05:39:56.149638	f	t
44	3	24	2017-03-31 05:39:56.149665	f	t
45	3	35	2017-04-05 05:39:56.149692	f	t
46	3	13	2017-04-11 05:39:56.14972	f	t
47	3	19	2017-03-21 05:39:56.149748	f	t
48	3	17	2017-03-30 05:39:56.149775	f	t
49	4	38	2017-03-21 05:39:56.149802	t	t
50	4	9	2017-04-05 05:39:56.149829	t	t
51	4	19	2017-03-19 05:39:56.149856	t	t
52	4	26	2017-03-25 05:39:56.149883	t	t
53	4	17	2017-03-27 05:39:56.149911	t	t
54	4	23	2017-03-30 05:39:56.149939	t	t
55	4	24	2017-04-02 05:39:56.149966	t	t
56	4	8	2017-03-28 05:39:56.149992	t	t
57	4	24	2017-04-02 05:39:56.150019	f	t
58	4	17	2017-03-24 05:39:56.150046	f	t
59	4	19	2017-04-07 05:39:56.150072	f	t
60	4	33	2017-04-10 05:39:56.150099	f	t
61	4	20	2017-03-31 05:39:56.150126	f	t
62	4	28	2017-03-30 05:39:56.150153	f	t
63	4	18	2017-03-18 05:39:56.150182	f	t
64	4	26	2017-03-23 05:39:56.150208	f	t
65	4	16	2017-03-19 05:39:56.150235	f	t
66	4	8	2017-04-02 05:39:56.150262	f	t
67	4	21	2017-04-07 05:39:56.150289	f	t
68	4	10	2017-04-09 05:39:56.150316	f	t
69	4	25	2017-04-04 05:39:56.150343	f	t
70	4	14	2017-03-17 05:39:56.150371	f	t
71	4	30	2017-04-11 05:39:56.150398	f	t
72	4	22	2017-04-04 05:39:56.150426	f	t
73	4	13	2017-04-06 05:39:56.150454	f	t
74	4	12	2017-04-03 05:39:56.150508	f	t
75	4	11	2017-04-02 05:39:56.150557	f	t
76	4	27	2017-04-07 05:39:56.150633	f	t
77	4	32	2017-03-17 05:39:56.150685	f	t
78	5	32	2017-04-01 05:39:56.150732	t	t
79	5	19	2017-03-30 05:39:56.150781	t	t
80	5	36	2017-03-25 05:39:56.150842	t	t
81	5	17	2017-03-22 05:39:56.150906	t	t
82	5	8	2017-04-03 05:39:56.150954	t	t
83	5	14	2017-03-29 05:39:56.150998	t	t
84	5	26	2017-04-06 05:39:56.15104	t	t
85	5	21	2017-03-29 05:39:56.151082	t	t
86	5	29	2017-03-27 05:39:56.151126	t	t
87	5	25	2017-04-04 05:39:56.151169	t	t
88	5	15	2017-04-04 05:39:56.151211	t	t
89	5	8	2017-03-19 05:39:56.151258	f	t
90	5	9	2017-04-07 05:39:56.151307	f	t
91	5	18	2017-03-31 05:39:56.151381	f	t
92	5	32	2017-04-01 05:39:56.151441	f	t
93	5	17	2017-03-26 05:39:56.151489	f	t
94	5	27	2017-04-04 05:39:56.151541	f	t
95	5	14	2017-03-25 05:39:56.151591	f	t
96	5	19	2017-03-18 05:39:56.151649	f	t
97	5	11	2017-03-23 05:39:56.151683	f	t
98	5	33	2017-03-26 05:39:56.151732	f	t
99	5	37	2017-03-27 05:39:56.151766	f	t
100	5	29	2017-03-20 05:39:56.151796	f	t
101	5	20	2017-03-20 05:39:56.151825	f	t
102	8	34	2017-04-04 05:39:56.151853	t	t
103	8	8	2017-04-06 05:39:56.151882	t	t
104	8	29	2017-04-05 05:39:56.151912	t	t
105	8	38	2017-03-29 05:39:56.151974	t	t
106	8	24	2017-04-07 05:39:56.152036	t	t
107	8	33	2017-03-29 05:39:56.152076	t	t
108	8	30	2017-03-19 05:39:56.152107	t	t
109	8	27	2017-03-17 05:39:56.152138	t	t
110	8	22	2017-04-04 05:39:56.152167	t	t
111	8	17	2017-03-19 05:39:56.152197	t	t
112	8	21	2017-04-05 05:39:56.152225	t	t
113	8	15	2017-03-27 05:39:56.152272	t	t
114	8	36	2017-03-22 05:39:56.152304	t	t
115	8	9	2017-03-29 05:39:56.152346	t	t
116	8	23	2017-04-10 05:39:56.152379	t	t
117	8	19	2017-03-26 05:39:56.152409	f	t
118	8	36	2017-03-22 05:39:56.152438	f	t
119	8	34	2017-04-08 05:39:56.152477	f	t
120	8	23	2017-03-25 05:39:56.152505	f	t
121	8	8	2017-03-18 05:39:56.152533	f	t
122	8	29	2017-03-27 05:39:56.152561	f	t
123	8	9	2017-04-02 05:39:56.152589	f	t
124	8	21	2017-04-09 05:39:56.152617	f	t
125	8	10	2017-04-09 05:39:56.152645	f	t
126	8	30	2017-04-09 05:39:56.152674	f	t
127	8	11	2017-03-27 05:39:56.152702	f	t
128	8	37	2017-04-02 05:39:56.15273	f	t
129	8	13	2017-04-01 05:39:56.152757	f	t
130	8	24	2017-04-04 05:39:56.152785	f	t
131	8	38	2017-04-01 05:39:56.152813	f	t
132	8	35	2017-03-24 05:39:56.15284	f	t
133	8	20	2017-04-05 05:39:56.152868	f	t
134	8	22	2017-03-20 05:39:56.152896	f	t
135	8	25	2017-04-02 05:39:56.152925	f	t
136	8	14	2017-03-20 05:39:56.152953	f	t
137	8	17	2017-03-23 05:39:56.15298	f	t
138	8	12	2017-03-23 05:39:56.153008	f	t
139	10	25	2017-03-31 05:39:56.153035	t	t
140	10	23	2017-04-02 05:39:56.153064	t	t
141	10	12	2017-03-24 05:39:56.153091	t	t
142	10	30	2017-04-04 05:39:56.153118	t	t
143	10	29	2017-03-31 05:39:56.153145	f	t
144	10	15	2017-03-27 05:39:56.153173	f	t
145	10	33	2017-03-31 05:39:56.1532	f	t
146	10	34	2017-03-17 05:39:56.153227	f	t
147	10	36	2017-04-04 05:39:56.153254	f	t
148	10	27	2017-03-27 05:39:56.153281	f	t
149	10	8	2017-03-17 05:39:56.153308	f	t
150	11	28	2017-03-20 05:39:56.153336	t	t
151	11	16	2017-03-31 05:39:56.153362	t	t
152	11	14	2017-04-11 05:39:56.153389	t	t
153	11	32	2017-03-17 05:39:56.153416	t	t
154	11	22	2017-03-29 05:39:56.153444	t	t
155	11	26	2017-03-30 05:39:56.15347	t	t
156	11	9	2017-04-06 05:39:56.153499	t	t
157	11	15	2017-03-21 05:39:56.153527	t	t
158	11	13	2017-04-09 05:39:56.153554	f	t
159	11	25	2017-03-22 05:39:56.153582	f	t
160	11	22	2017-03-31 05:39:56.153619	f	t
161	11	18	2017-04-03 05:39:56.153649	f	t
162	11	35	2017-03-17 05:39:56.153678	f	t
163	11	12	2017-03-23 05:39:56.153706	f	t
164	11	16	2017-04-09 05:39:56.153734	f	t
165	11	29	2017-03-23 05:39:56.153761	f	t
166	11	26	2017-04-07 05:39:56.153789	f	t
167	12	35	2017-03-31 05:39:56.153818	t	t
168	12	19	2017-03-17 05:39:56.153846	t	t
169	12	21	2017-03-29 05:39:56.153883	t	t
170	12	33	2017-03-19 05:39:56.153911	f	t
171	12	16	2017-04-02 05:39:56.153939	f	t
172	12	38	2017-03-23 05:39:56.153967	f	t
173	12	10	2017-04-02 05:39:56.153995	f	t
174	12	36	2017-03-26 05:39:56.154022	f	t
175	12	25	2017-04-06 05:39:56.154049	f	t
176	12	30	2017-03-27 05:39:56.154077	f	t
177	12	17	2017-04-04 05:39:56.154105	f	t
178	12	35	2017-03-31 05:39:56.154132	f	t
179	12	11	2017-03-26 05:39:56.154171	f	t
180	12	29	2017-03-31 05:39:56.1542	f	t
181	12	27	2017-03-31 05:39:56.154249	f	t
182	12	22	2017-04-06 05:39:56.154277	f	t
183	12	13	2017-03-20 05:39:56.154314	f	t
184	12	28	2017-04-10 05:39:56.154341	f	t
185	12	34	2017-03-30 05:39:56.154369	f	t
186	12	32	2017-03-18 05:39:56.154397	f	t
187	12	20	2017-04-05 05:39:56.154424	f	t
188	12	21	2017-03-28 05:39:56.154452	f	t
189	12	23	2017-04-06 05:39:56.154479	f	t
190	15	37	2017-04-04 05:39:56.154506	t	t
191	16	25	2017-04-05 05:39:56.154533	t	t
192	16	38	2017-03-23 05:39:56.154561	t	t
193	16	26	2017-03-18 05:39:56.154588	t	t
194	16	30	2017-03-25 05:39:56.154616	t	t
195	16	35	2017-03-22 05:39:56.154643	t	t
196	16	17	2017-03-25 05:39:56.154671	t	t
197	16	8	2017-03-18 05:39:56.154698	t	t
198	16	16	2017-03-23 05:39:56.154726	t	t
199	16	18	2017-03-29 05:39:56.154753	t	t
200	16	37	2017-04-04 05:39:56.154781	t	t
201	16	36	2017-04-10 05:39:56.154808	t	t
202	16	20	2017-03-31 05:39:56.154835	t	t
203	16	14	2017-03-19 05:39:56.154861	t	t
204	16	34	2017-03-20 05:39:56.154888	t	t
205	16	12	2017-03-23 05:39:56.154916	t	t
206	16	28	2017-04-10 05:39:56.154943	t	t
207	16	13	2017-03-22 05:39:56.15497	t	t
208	16	21	2017-04-05 05:39:56.154998	t	t
209	16	13	2017-03-28 05:39:56.155025	f	t
210	16	12	2017-03-29 05:39:56.155052	f	t
211	16	21	2017-03-30 05:39:56.15508	f	t
212	16	30	2017-04-10 05:39:56.155107	f	t
213	16	34	2017-04-07 05:39:56.155134	f	t
214	16	11	2017-03-17 05:39:56.155161	f	t
215	16	24	2017-04-05 05:39:56.155189	f	t
216	16	26	2017-04-10 05:39:56.155216	f	t
217	16	37	2017-04-07 05:39:56.155243	f	t
218	16	36	2017-04-08 05:39:56.155271	f	t
219	16	22	2017-04-04 05:39:56.155298	f	t
220	17	33	2017-04-01 05:39:56.155326	t	t
221	17	22	2017-04-02 05:39:56.155395	f	t
222	19	14	2017-03-19 05:39:56.155425	f	t
223	19	21	2017-04-10 05:39:56.155462	f	t
224	20	18	2017-03-19 05:39:56.155501	t	t
225	20	35	2017-03-30 05:39:56.155529	t	t
226	20	21	2017-04-08 05:39:56.155566	t	t
227	20	27	2017-03-24 05:39:56.155593	t	t
228	20	28	2017-03-28 05:39:56.15562	t	t
229	20	29	2017-04-06 05:39:56.155646	t	t
230	20	15	2017-03-26 05:39:56.155674	t	t
231	20	8	2017-03-29 05:39:56.1557	t	t
232	20	34	2017-04-01 05:39:56.155727	t	t
233	20	19	2017-03-22 05:39:56.155755	t	t
234	20	14	2017-04-08 05:39:56.155782	t	t
235	20	30	2017-03-17 05:39:56.155809	t	t
236	20	20	2017-04-04 05:39:56.155837	t	t
237	20	33	2017-04-04 05:39:56.155863	t	t
238	20	17	2017-03-25 05:39:56.15589	t	t
239	20	32	2017-03-17 05:39:56.155917	t	t
240	20	36	2017-03-17 05:39:56.155943	t	t
241	20	30	2017-03-23 05:39:56.15597	f	t
242	20	19	2017-04-08 05:39:56.155997	f	t
243	20	23	2017-03-27 05:39:56.156024	f	t
244	20	18	2017-03-22 05:39:56.156051	f	t
245	20	29	2017-04-04 05:39:56.156078	f	t
246	20	10	2017-03-30 05:39:56.156105	f	t
247	20	17	2017-03-17 05:39:56.156132	f	t
248	20	27	2017-04-07 05:39:56.156159	f	t
249	21	15	2017-04-06 05:39:56.156185	t	t
250	21	16	2017-04-08 05:39:56.156212	t	t
251	21	8	2017-04-09 05:39:56.156239	t	t
252	21	25	2017-03-23 05:39:56.156267	t	t
253	21	18	2017-03-26 05:39:56.156294	t	t
254	21	32	2017-03-28 05:39:56.15632	t	t
255	21	30	2017-03-23 05:39:56.156346	t	t
256	21	38	2017-04-08 05:39:56.156374	t	t
257	21	17	2017-03-26 05:39:56.156401	t	t
258	21	22	2017-03-26 05:39:56.156427	t	t
259	21	19	2017-04-04 05:39:56.156456	t	t
260	21	34	2017-04-07 05:39:56.156483	t	t
261	21	29	2017-03-24 05:39:56.156509	t	t
262	21	25	2017-03-30 05:39:56.156537	f	t
263	21	22	2017-04-05 05:39:56.156564	f	t
264	21	30	2017-03-31 05:39:56.156591	f	t
265	21	28	2017-04-05 05:39:56.156618	f	t
266	21	33	2017-03-25 05:39:56.156645	f	t
267	21	16	2017-04-10 05:39:56.156672	f	t
268	23	29	2017-04-03 05:39:56.156699	t	t
269	23	14	2017-04-10 05:39:56.156725	t	t
270	23	8	2017-04-10 05:39:56.156753	t	t
271	23	15	2017-03-28 05:39:56.156779	t	t
272	23	35	2017-03-19 05:39:56.156835	t	t
273	23	23	2017-03-30 05:39:56.156863	t	t
274	24	30	2017-04-09 05:39:56.15689	t	t
275	24	17	2017-04-02 05:39:56.156917	t	t
276	24	32	2017-03-31 05:39:56.156944	t	t
277	24	11	2017-04-01 05:39:56.156971	t	t
278	24	12	2017-03-22 05:39:56.157009	f	t
279	24	16	2017-03-21 05:39:56.157036	f	t
280	24	19	2017-03-18 05:39:56.157064	f	t
281	24	25	2017-03-19 05:39:56.15709	f	t
282	24	15	2017-03-22 05:39:56.157118	f	t
283	26	20	2017-04-05 05:39:56.157145	t	t
284	27	13	2017-03-30 05:39:56.157173	t	t
285	27	15	2017-04-07 05:39:56.157201	t	t
286	27	9	2017-04-08 05:39:56.157228	t	t
287	27	10	2017-03-17 05:39:56.157256	t	t
288	27	8	2017-03-19 05:39:56.157284	t	t
289	27	38	2017-03-31 05:39:56.157311	t	t
290	27	17	2017-03-25 05:39:56.157337	t	t
291	27	28	2017-03-31 05:39:56.157365	t	t
292	27	30	2017-03-26 05:39:56.157392	f	t
293	27	8	2017-03-17 05:39:56.157419	f	t
294	27	24	2017-04-02 05:39:56.15746	f	t
295	27	27	2017-03-22 05:39:56.157508	f	t
296	27	25	2017-03-31 05:39:56.157538	f	t
297	28	25	2017-03-21 05:39:56.157566	t	t
298	28	24	2017-03-30 05:39:56.157614	t	t
299	28	14	2017-03-31 05:39:56.157662	t	t
300	28	20	2017-03-22 05:39:56.157706	t	t
301	28	35	2017-03-17 05:39:56.157749	t	t
302	28	11	2017-03-31 05:39:56.15779	t	t
303	28	19	2017-04-02 05:39:56.157833	t	t
304	28	12	2017-04-08 05:39:56.157876	t	t
305	28	21	2017-03-28 05:39:56.157919	t	t
306	28	26	2017-04-03 05:39:56.157964	f	t
307	28	12	2017-03-18 05:39:56.158013	f	t
308	28	27	2017-03-28 05:39:56.158063	f	t
309	28	37	2017-04-10 05:39:56.15811	f	t
310	28	19	2017-03-25 05:39:56.158159	f	t
311	28	14	2017-03-26 05:39:56.158209	f	t
312	28	21	2017-03-26 05:39:56.158272	f	t
313	28	38	2017-03-20 05:39:56.158323	f	t
314	28	17	2017-03-26 05:39:56.158364	f	t
315	29	27	2017-03-21 05:39:56.158394	t	t
316	29	25	2017-03-20 05:39:56.158434	t	t
317	30	15	2017-03-18 05:39:56.158462	t	t
318	32	29	2017-03-25 05:39:56.15849	t	t
319	32	9	2017-03-27 05:39:56.158518	t	t
320	32	27	2017-04-10 05:39:56.158547	t	t
321	32	28	2017-04-01 05:39:56.158574	t	t
322	32	35	2017-04-07 05:39:56.158602	t	t
323	32	10	2017-03-17 05:39:56.158639	t	t
324	32	11	2017-03-25 05:39:56.158666	t	t
325	32	12	2017-04-11 05:39:56.158694	t	t
326	32	32	2017-03-21 05:39:56.15872	t	t
327	32	36	2017-04-10 05:39:56.158747	t	t
328	32	24	2017-03-19 05:39:56.158775	f	t
329	32	22	2017-03-19 05:39:56.158802	f	t
330	32	17	2017-04-07 05:39:56.15883	f	t
331	32	32	2017-03-19 05:39:56.158857	f	t
332	32	11	2017-03-24 05:39:56.158884	f	t
333	34	28	2017-03-26 05:39:56.158911	t	t
334	34	22	2017-03-30 05:39:56.158939	t	t
335	34	23	2017-04-05 05:39:56.158965	t	t
336	34	26	2017-03-24 05:39:56.158992	t	t
337	34	13	2017-04-06 05:39:56.159019	t	t
338	34	10	2017-03-21 05:39:56.159045	t	t
339	34	14	2017-04-09 05:39:56.159072	t	t
340	34	29	2017-04-04 05:39:56.159099	t	t
341	34	11	2017-03-28 05:39:56.159125	f	t
342	34	29	2017-03-30 05:39:56.159152	f	t
343	34	32	2017-03-20 05:39:56.15918	f	t
344	34	15	2017-03-31 05:39:56.159206	f	t
345	34	36	2017-03-28 05:39:56.159234	f	t
346	34	17	2017-03-21 05:39:56.159261	f	t
347	34	21	2017-04-06 05:39:56.159288	f	t
348	34	8	2017-04-07 05:39:56.159314	f	t
349	34	27	2017-04-09 05:39:56.159377	f	t
350	34	37	2017-04-04 05:39:56.159425	f	t
351	35	17	2017-03-25 05:39:56.159456	t	t
352	35	16	2017-04-10 05:39:56.159485	t	t
353	35	30	2017-03-25 05:39:56.159512	t	t
354	35	14	2017-03-30 05:39:56.15954	t	t
355	35	9	2017-04-09 05:39:56.159577	t	t
356	35	33	2017-03-20 05:39:56.159604	t	t
357	35	34	2017-04-11 05:39:56.159631	f	t
358	35	22	2017-03-24 05:39:56.159668	f	t
359	35	15	2017-04-11 05:39:56.159696	f	t
360	35	26	2017-04-10 05:39:56.159733	f	t
361	35	17	2017-04-03 05:39:56.159759	f	t
362	35	16	2017-03-23 05:39:56.159786	f	t
363	35	13	2017-03-25 05:39:56.159812	f	t
364	36	34	2017-03-31 05:39:56.159839	t	t
365	36	13	2017-04-10 05:39:56.159865	t	t
366	36	30	2017-04-04 05:39:56.159892	t	t
367	36	22	2017-03-20 05:39:56.159919	t	t
368	36	15	2017-03-22 05:39:56.159945	t	t
369	36	35	2017-04-08 05:39:56.159972	f	t
370	36	36	2017-03-21 05:39:56.159999	f	t
371	36	19	2017-03-31 05:39:56.160026	f	t
372	36	10	2017-03-22 05:39:56.160052	f	t
373	36	17	2017-03-26 05:39:56.160078	f	t
374	36	28	2017-03-20 05:39:56.160104	f	t
375	36	26	2017-04-08 05:39:56.160141	f	t
376	39	29	2017-03-26 05:39:56.160168	t	t
377	39	22	2017-04-07 05:39:56.160196	t	t
378	39	13	2017-03-20 05:39:56.160243	t	t
379	39	16	2017-03-30 05:39:56.16027	t	t
380	39	14	2017-04-08 05:39:56.160307	t	t
381	39	12	2017-03-27 05:39:56.160334	t	t
382	39	12	2017-04-05 05:39:56.16036	f	t
383	39	24	2017-04-05 05:39:56.160386	f	t
384	39	38	2017-03-19 05:39:56.160412	f	t
385	40	9	2017-03-31 05:39:56.160438	t	t
386	40	10	2017-03-19 05:39:56.160465	t	t
387	40	11	2017-04-07 05:39:56.160492	t	t
388	40	30	2017-03-27 05:39:56.160518	t	t
389	40	37	2017-03-19 05:39:56.160544	t	t
390	40	16	2017-03-31 05:39:56.160571	t	t
391	40	28	2017-04-05 05:39:56.160597	t	t
392	40	8	2017-04-06 05:39:56.160623	t	t
393	40	38	2017-04-03 05:39:56.160649	t	t
394	40	26	2017-03-26 05:39:56.160676	t	t
395	40	24	2017-03-28 05:39:56.160702	t	t
396	40	22	2017-04-05 05:39:56.160728	t	t
397	40	36	2017-03-31 05:39:56.160754	t	t
398	40	34	2017-04-05 05:39:56.160782	t	t
399	40	12	2017-03-17 05:39:56.160807	f	t
400	40	28	2017-04-09 05:39:56.160835	f	t
401	40	35	2017-03-27 05:39:56.160861	f	t
402	40	18	2017-04-10 05:39:56.160888	f	t
403	41	14	2017-03-27 05:39:56.160914	t	t
404	41	17	2017-03-26 05:39:56.160942	t	t
405	41	33	2017-04-05 05:39:56.160969	t	t
406	41	11	2017-03-30 05:39:56.160996	t	t
407	42	26	2017-03-24 05:39:56.161023	t	t
408	42	38	2017-03-27 05:39:56.16105	t	t
409	42	10	2017-04-10 05:39:56.161075	t	t
410	42	12	2017-03-17 05:39:56.161103	t	t
411	42	30	2017-03-27 05:39:56.161129	t	t
412	42	35	2017-04-03 05:39:56.161156	t	t
413	42	37	2017-04-08 05:39:56.161182	t	t
414	42	24	2017-03-20 05:39:56.161209	t	t
415	42	14	2017-04-01 05:39:56.161236	t	t
416	42	28	2017-04-11 05:39:56.161262	f	t
417	42	13	2017-03-23 05:39:56.161288	f	t
418	44	37	2017-03-21 05:39:56.161314	t	t
419	44	16	2017-04-03 05:39:56.16134	t	t
420	44	30	2017-04-06 05:39:56.161367	t	t
421	44	32	2017-04-06 05:39:56.161394	t	t
422	44	38	2017-03-23 05:39:56.161423	t	t
423	44	28	2017-03-18 05:39:56.161449	t	t
424	44	17	2017-04-06 05:39:56.161477	t	t
425	44	13	2017-03-18 05:39:56.161503	t	t
426	44	34	2017-04-04 05:39:56.16153	t	t
427	44	29	2017-03-28 05:39:56.161557	t	t
428	44	20	2017-04-02 05:39:56.161584	t	t
429	44	18	2017-03-17 05:39:56.161611	t	t
430	44	10	2017-04-11 05:39:56.161638	t	t
431	44	11	2017-03-25 05:39:56.161665	t	t
432	44	9	2017-03-20 05:39:56.161691	t	t
433	44	23	2017-03-21 05:39:56.161716	t	t
434	44	22	2017-04-07 05:39:56.161743	t	t
435	44	24	2017-03-28 05:39:56.161769	t	t
436	44	29	2017-03-23 05:39:56.161796	f	t
437	44	10	2017-04-05 05:39:56.161822	f	t
438	44	15	2017-03-21 05:39:56.161848	f	t
439	44	32	2017-03-18 05:39:56.161874	f	t
440	44	18	2017-03-26 05:39:56.161901	f	t
441	44	35	2017-04-11 05:39:56.161928	f	t
442	44	8	2017-03-19 05:39:56.161954	f	t
443	44	17	2017-03-27 05:39:56.16198	f	t
444	46	27	2017-03-21 05:39:56.162006	t	t
445	46	16	2017-04-01 05:39:56.162032	t	t
446	46	30	2017-03-22 05:39:56.162059	t	t
447	46	9	2017-03-25 05:39:56.162085	t	t
448	46	18	2017-04-10 05:39:56.162111	t	t
449	46	25	2017-04-06 05:39:56.162137	t	t
450	46	11	2017-03-30 05:39:56.162163	t	t
451	46	38	2017-03-27 05:39:56.162189	t	t
452	46	19	2017-03-24 05:39:56.162215	t	t
453	46	28	2017-03-27 05:39:56.162241	t	t
454	46	32	2017-03-24 05:39:56.162268	t	t
455	46	22	2017-03-22 05:39:56.162293	t	t
456	46	14	2017-04-05 05:39:56.16232	t	t
457	46	20	2017-04-06 05:39:56.162346	t	t
458	46	35	2017-04-09 05:39:56.162373	t	t
459	46	13	2017-04-06 05:39:56.162399	t	t
460	46	33	2017-03-18 05:39:56.162426	f	t
461	46	27	2017-04-11 05:39:56.162453	f	t
462	46	38	2017-03-20 05:39:56.162478	f	t
463	46	9	2017-04-08 05:39:56.162505	f	t
464	46	29	2017-04-08 05:39:56.162531	f	t
465	46	30	2017-04-11 05:39:56.162557	f	t
466	46	37	2017-03-31 05:39:56.162583	f	t
467	47	15	2017-04-02 05:39:56.162609	t	t
468	47	8	2017-04-03 05:39:56.162637	t	t
469	47	18	2017-04-07 05:39:56.162663	t	t
470	47	20	2017-03-29 05:39:56.162689	t	t
471	47	17	2017-04-10 05:39:56.162715	f	t
472	49	13	2017-04-05 05:39:56.162742	f	t
473	49	28	2017-04-10 05:39:56.162768	f	t
474	49	11	2017-04-05 05:39:56.162794	f	t
475	49	12	2017-03-23 05:39:56.162831	f	t
476	49	30	2017-03-22 05:39:56.162859	f	t
477	50	36	2017-03-20 05:39:56.162886	t	t
478	50	8	2017-04-04 05:39:56.162913	t	t
479	50	12	2017-03-19 05:39:56.16294	t	t
480	50	22	2017-03-28 05:39:56.162968	t	t
481	50	30	2017-04-04 05:39:56.162995	t	t
482	50	11	2017-03-19 05:39:56.163032	t	t
483	50	15	2017-04-01 05:39:56.163059	t	t
484	50	26	2017-03-28 05:39:56.163086	t	t
485	50	13	2017-04-01 05:39:56.163113	t	t
486	50	28	2017-03-26 05:39:56.16314	t	t
487	50	27	2017-03-28 05:39:56.163167	t	t
488	50	24	2017-03-29 05:39:56.163194	t	t
489	50	33	2017-03-24 05:39:56.163221	t	t
490	50	21	2017-03-22 05:39:56.163247	t	t
491	50	16	2017-03-18 05:39:56.163274	f	t
492	50	21	2017-03-23 05:39:56.1633	f	t
493	50	8	2017-04-02 05:39:56.163328	f	t
494	50	37	2017-03-25 05:39:56.163381	f	t
495	50	9	2017-04-02 05:39:56.16341	f	t
496	51	9	2017-04-03 05:39:56.163447	t	t
497	51	8	2017-03-17 05:39:56.163473	t	t
498	51	27	2017-03-22 05:39:56.163501	t	t
499	51	25	2017-03-25 05:39:56.163528	t	t
500	51	28	2017-03-22 05:39:56.163555	t	t
501	51	20	2017-04-02 05:39:56.163581	t	t
502	51	35	2017-03-19 05:39:56.163607	t	t
503	51	20	2017-03-17 05:39:56.163633	f	t
504	51	34	2017-03-23 05:39:56.16366	f	t
505	54	38	2017-04-03 05:39:56.163847	t	t
506	54	26	2017-04-10 05:39:56.163877	t	t
507	54	30	2017-03-18 05:39:56.163905	t	t
508	54	21	2017-03-24 05:39:56.163932	t	t
509	54	12	2017-04-11 05:39:56.16396	t	t
510	54	11	2017-03-23 05:39:56.163987	t	t
511	54	28	2017-04-06 05:39:56.164014	t	t
512	54	27	2017-03-29 05:39:56.164039	t	t
513	54	20	2017-03-21 05:39:56.164066	f	t
514	54	30	2017-03-25 05:39:56.164092	f	t
515	54	24	2017-04-07 05:39:56.164119	f	t
516	55	9	2017-03-24 05:39:56.164145	t	t
517	55	32	2017-03-17 05:39:56.164173	t	t
518	55	22	2017-04-11 05:39:56.1642	t	t
519	55	30	2017-03-21 05:39:56.164226	t	t
520	55	33	2017-03-28 05:39:56.164253	t	t
521	55	26	2017-04-08 05:39:56.164279	t	t
522	55	18	2017-04-10 05:39:56.164306	f	t
523	55	27	2017-03-26 05:39:56.164333	f	t
524	55	33	2017-03-18 05:39:56.164359	f	t
525	56	17	2017-04-04 05:39:56.164385	t	t
526	56	24	2017-03-24 05:39:56.164412	t	t
527	56	20	2017-04-07 05:39:56.164438	t	t
528	56	30	2017-03-31 05:39:56.164464	t	t
529	56	22	2017-03-27 05:39:56.164491	f	t
530	56	28	2017-04-05 05:39:56.164518	f	t
531	56	15	2017-03-27 05:39:56.164555	f	t
532	56	13	2017-03-18 05:39:56.164583	f	t
533	57	20	2017-04-09 05:39:56.16461	t	t
534	57	30	2017-03-17 05:39:56.164639	t	t
535	57	30	2017-04-01 05:39:56.164666	t	t
536	57	18	2017-04-08 05:39:56.164694	t	t
537	57	35	2017-03-23 05:39:56.164732	f	t
538	57	30	2017-04-09 05:39:56.16477	f	t
539	57	36	2017-04-11 05:39:56.164798	f	t
540	57	38	2017-04-01 05:39:56.164827	f	t
541	57	11	2017-03-19 05:39:56.164865	f	t
542	58	28	2017-04-01 05:39:56.164892	t	t
543	58	33	2017-03-22 05:39:56.164919	f	t
544	58	26	2017-04-03 05:39:56.164946	f	t
545	58	35	2017-03-17 05:39:56.164973	f	t
546	59	9	2017-03-17 05:39:56.165001	t	t
547	59	16	2017-04-09 05:39:56.165027	t	t
548	59	37	2017-03-19 05:39:56.165053	t	t
549	59	13	2017-03-29 05:39:56.165079	t	t
550	59	20	2017-04-08 05:39:56.165106	t	t
551	59	28	2017-04-02 05:39:56.165133	f	t
552	59	15	2017-03-28 05:39:56.16516	f	t
553	59	27	2017-04-08 05:39:56.165187	f	t
554	59	34	2017-04-07 05:39:56.165213	f	t
555	59	33	2017-03-18 05:39:56.16524	f	t
556	59	20	2017-04-03 05:39:56.165266	f	t
557	59	36	2017-04-11 05:39:56.165293	f	t
558	59	22	2017-04-05 05:39:56.16532	f	t
559	59	30	2017-03-19 05:39:56.165346	f	t
560	59	12	2017-03-29 05:39:56.165374	f	t
561	59	18	2017-03-19 05:39:56.165401	f	t
562	59	26	2017-04-09 05:39:56.165428	f	t
563	59	13	2017-03-31 05:39:56.165455	f	t
564	59	19	2017-03-17 05:39:56.165482	f	t
565	59	35	2017-04-07 05:39:56.165509	f	t
566	60	30	2017-03-17 05:39:56.165535	t	t
567	60	28	2017-03-28 05:39:56.165562	t	t
568	60	14	2017-03-31 05:39:56.16559	t	t
569	60	22	2017-03-30 05:39:56.165617	t	t
570	60	30	2017-04-08 05:39:56.165643	t	t
571	60	35	2017-03-22 05:39:56.16567	t	t
572	60	29	2017-03-21 05:39:56.165697	t	t
573	60	32	2017-03-24 05:39:56.165725	t	t
574	60	24	2017-03-18 05:39:56.165751	t	t
575	60	12	2017-04-07 05:39:56.165778	t	t
576	60	16	2017-03-23 05:39:56.165806	t	t
577	60	18	2017-04-11 05:39:56.165833	t	t
578	60	18	2017-03-29 05:39:56.16586	f	t
579	60	36	2017-03-27 05:39:56.165887	f	t
580	60	34	2017-03-18 05:39:56.165914	f	t
581	60	20	2017-04-11 05:39:56.165941	f	t
582	60	15	2017-04-02 05:39:56.165967	f	t
583	60	24	2017-03-23 05:39:56.165994	f	t
584	60	12	2017-03-18 05:39:56.166021	f	t
585	61	37	2017-03-18 05:39:56.166058	t	t
586	61	12	2017-04-02 05:39:56.166085	t	t
587	61	17	2017-04-06 05:39:56.166112	t	t
588	62	35	2017-03-25 05:39:56.166141	t	t
589	62	17	2017-04-05 05:39:56.166168	t	t
590	62	21	2017-03-17 05:39:56.166204	t	t
591	62	20	2017-04-03 05:39:56.166231	t	t
592	62	34	2017-03-17 05:39:56.166257	t	t
593	62	30	2017-04-05 05:39:56.166283	t	t
594	62	16	2017-04-05 05:39:56.16631	t	t
595	62	11	2017-04-03 05:39:56.166336	t	t
596	62	8	2017-03-31 05:39:56.166362	t	t
597	62	37	2017-03-17 05:39:56.166389	t	t
598	62	10	2017-04-01 05:39:56.166416	t	t
599	62	22	2017-03-20 05:39:56.166443	t	t
600	62	27	2017-03-21 05:39:56.166471	t	t
601	62	19	2017-04-06 05:39:56.166497	t	t
602	62	30	2017-03-31 05:39:56.166524	t	t
603	62	38	2017-03-19 05:39:56.16655	t	t
604	62	15	2017-04-05 05:39:56.166577	t	t
605	62	17	2017-03-27 05:39:56.166604	f	t
606	62	34	2017-04-10 05:39:56.166631	f	t
607	62	29	2017-04-07 05:39:56.166657	f	t
608	62	25	2017-04-04 05:39:56.166684	f	t
609	62	21	2017-04-01 05:39:56.166711	f	t
610	62	33	2017-04-06 05:39:56.166738	f	t
611	62	9	2017-03-26 05:39:56.166764	f	t
612	62	23	2017-04-07 05:39:56.166791	f	t
613	62	15	2017-03-25 05:39:56.166817	f	t
614	62	37	2017-04-06 05:39:56.166844	f	t
615	62	16	2017-03-19 05:39:56.16687	f	t
616	62	26	2017-03-17 05:39:56.166898	f	t
617	63	38	2017-03-30 05:39:56.166925	f	t
618	64	30	2017-03-31 05:39:56.166951	t	t
619	64	12	2017-04-10 05:39:56.166978	t	t
620	64	28	2017-04-10 05:39:56.167005	t	t
621	64	35	2017-04-11 05:39:56.167032	f	t
622	64	19	2017-04-07 05:39:56.167058	f	t
623	64	13	2017-03-26 05:39:56.167085	f	t
624	64	16	2017-04-01 05:39:56.167111	f	t
625	6	18	2017-04-03 05:39:56.167137	t	t
626	6	36	2017-04-01 05:39:56.167163	f	t
627	6	35	2017-04-09 05:39:56.16719	f	t
628	6	37	2017-03-27 05:39:56.167216	f	t
629	6	30	2017-03-22 05:39:56.167242	f	t
630	6	9	2017-03-29 05:39:56.167268	f	t
631	6	23	2017-04-07 05:39:56.167294	f	t
632	6	28	2017-04-10 05:39:56.167321	f	t
633	6	8	2017-04-11 05:39:56.167371	f	t
634	6	25	2017-03-19 05:39:56.167412	f	t
635	7	19	2017-03-20 05:39:56.167463	t	t
636	7	30	2017-04-03 05:39:56.167517	t	t
637	7	13	2017-04-08 05:39:56.167582	t	t
638	7	8	2017-03-31 05:39:56.167615	t	t
639	7	17	2017-03-27 05:39:56.167643	t	t
640	7	9	2017-03-31 05:39:56.167671	t	t
641	7	27	2017-04-05 05:39:56.167698	t	t
642	7	15	2017-04-03 05:39:56.167725	t	t
643	7	23	2017-03-26 05:39:56.167751	t	t
644	7	25	2017-04-09 05:39:56.167778	t	t
645	7	34	2017-04-02 05:39:56.167805	t	t
646	7	38	2017-03-21 05:39:56.167831	t	t
647	7	24	2017-03-28 05:39:56.167858	t	t
648	7	34	2017-04-01 05:39:56.167885	f	t
649	7	17	2017-03-20 05:39:56.167912	f	t
650	7	30	2017-03-20 05:39:56.167939	f	t
651	7	29	2017-03-31 05:39:56.167966	f	t
652	7	13	2017-03-25 05:39:56.167994	f	t
653	7	35	2017-03-19 05:39:56.16802	f	t
654	7	24	2017-04-08 05:39:56.168047	f	t
655	7	32	2017-03-30 05:39:56.168074	f	t
656	7	36	2017-03-21 05:39:56.1681	f	t
657	7	28	2017-03-18 05:39:56.168127	f	t
658	7	15	2017-04-10 05:39:56.168154	f	t
659	7	14	2017-03-27 05:39:56.16818	f	t
660	7	11	2017-04-10 05:39:56.168207	f	t
661	7	21	2017-04-07 05:39:56.168234	f	t
662	7	10	2017-03-24 05:39:56.16826	f	t
663	7	8	2017-03-30 05:39:56.168288	f	t
664	7	25	2017-03-30 05:39:56.168315	f	t
665	9	26	2017-04-11 05:39:56.168341	t	t
666	9	8	2017-03-21 05:39:56.168368	t	t
667	9	33	2017-03-28 05:39:56.168395	t	t
668	9	27	2017-04-03 05:39:56.168422	t	t
669	9	28	2017-03-18 05:39:56.168448	t	t
670	9	23	2017-04-06 05:39:56.168475	t	t
671	9	22	2017-03-20 05:39:56.168502	t	t
672	9	34	2017-04-11 05:39:56.168528	t	t
673	9	38	2017-04-09 05:39:56.168555	t	t
674	9	21	2017-04-05 05:39:56.168582	t	t
675	9	30	2017-04-11 05:39:56.168608	t	t
676	9	10	2017-04-08 05:39:56.168634	t	t
677	9	19	2017-04-02 05:39:56.168661	f	t
678	9	26	2017-04-05 05:39:56.168688	f	t
679	9	14	2017-03-19 05:39:56.168715	f	t
680	13	22	2017-03-24 05:39:56.168741	t	t
681	13	23	2017-03-22 05:39:56.168768	t	t
682	13	18	2017-04-04 05:39:56.168796	t	t
683	13	28	2017-03-19 05:39:56.168823	t	t
684	13	35	2017-03-24 05:39:56.16885	t	t
685	13	19	2017-03-19 05:39:56.168877	t	t
686	13	9	2017-04-02 05:39:56.168904	t	t
687	13	27	2017-04-01 05:39:56.16893	t	t
688	13	24	2017-03-17 05:39:56.168957	t	t
689	13	14	2017-04-11 05:39:56.168984	f	t
690	13	10	2017-04-03 05:39:56.16901	f	t
691	13	28	2017-03-31 05:39:56.169036	f	t
692	13	13	2017-03-29 05:39:56.169062	f	t
693	13	30	2017-04-09 05:39:56.169088	f	t
694	13	15	2017-04-09 05:39:56.169114	f	t
695	13	26	2017-04-11 05:39:56.169142	f	t
696	13	35	2017-03-31 05:39:56.169168	f	t
697	13	12	2017-03-20 05:39:56.169195	f	t
698	13	18	2017-03-25 05:39:56.169221	f	t
699	13	16	2017-03-20 05:39:56.169247	f	t
700	13	38	2017-04-04 05:39:56.169274	f	t
701	13	19	2017-03-20 05:39:56.169301	f	t
702	13	30	2017-03-20 05:39:56.169328	f	t
703	13	36	2017-03-23 05:39:56.169356	f	t
704	13	29	2017-03-30 05:39:56.169383	f	t
705	13	24	2017-03-20 05:39:56.16941	f	t
706	13	11	2017-03-31 05:39:56.169437	f	t
707	14	10	2017-04-03 05:39:56.169464	t	t
708	14	35	2017-04-10 05:39:56.16949	t	t
709	14	27	2017-03-26 05:39:56.169517	t	t
710	14	22	2017-03-31 05:39:56.169544	t	t
711	14	21	2017-04-09 05:39:56.169571	t	t
712	14	37	2017-04-06 05:39:56.16961	t	t
713	14	23	2017-04-02 05:39:56.169638	f	t
714	14	13	2017-03-25 05:39:56.169674	f	t
715	14	10	2017-04-11 05:39:56.169701	f	t
716	14	26	2017-04-11 05:39:56.169728	f	t
717	14	16	2017-03-31 05:39:56.169755	f	t
718	18	30	2017-04-07 05:39:56.169783	t	t
719	18	13	2017-03-28 05:39:56.16981	t	t
720	18	19	2017-03-31 05:39:56.169836	f	t
721	18	38	2017-03-23 05:39:56.169863	f	t
722	18	22	2017-03-21 05:39:56.16989	f	t
723	18	30	2017-04-06 05:39:56.169916	f	t
724	18	25	2017-04-07 05:39:56.169943	f	t
725	18	28	2017-04-08 05:39:56.169971	f	t
726	18	27	2017-03-30 05:39:56.169998	f	t
727	18	36	2017-03-18 05:39:56.170024	f	t
728	18	24	2017-04-08 05:39:56.170051	f	t
729	18	17	2017-03-27 05:39:56.170078	f	t
730	18	34	2017-03-20 05:39:56.170106	f	t
731	18	20	2017-03-27 05:39:56.170132	f	t
732	22	24	2017-03-24 05:39:56.17016	t	t
733	22	12	2017-03-18 05:39:56.170187	t	t
734	22	35	2017-03-17 05:39:56.170215	t	t
735	22	14	2017-03-18 05:39:56.170242	t	t
736	22	36	2017-03-19 05:39:56.170268	t	t
737	22	33	2017-03-23 05:39:56.170294	t	t
738	22	32	2017-03-24 05:39:56.170321	t	t
739	22	29	2017-03-27 05:39:56.170348	t	t
740	22	19	2017-04-02 05:39:56.170375	t	t
741	22	15	2017-03-23 05:39:56.170402	t	t
742	22	30	2017-03-26 05:39:56.210566	t	t
743	22	13	2017-03-29 05:39:56.210617	f	t
744	25	33	2017-03-24 05:39:56.210651	t	t
745	25	24	2017-04-07 05:39:56.210682	t	t
746	25	37	2017-03-28 05:39:56.210711	t	t
747	25	8	2017-03-22 05:39:56.21074	t	t
748	25	9	2017-04-02 05:39:56.210769	t	t
749	25	13	2017-03-27 05:39:56.210798	t	t
750	25	11	2017-03-31 05:39:56.210826	t	t
751	25	29	2017-04-07 05:39:56.210854	t	t
752	25	20	2017-03-31 05:39:56.210881	t	t
753	25	36	2017-04-08 05:39:56.210909	f	t
754	25	22	2017-03-18 05:39:56.210938	f	t
755	25	11	2017-03-30 05:39:56.210966	f	t
756	25	18	2017-04-05 05:39:56.210994	f	t
757	25	33	2017-04-11 05:39:56.21102	f	t
758	25	30	2017-04-01 05:39:56.211047	f	t
759	25	38	2017-03-25 05:39:56.211074	f	t
760	25	35	2017-03-23 05:39:56.211101	f	t
761	25	23	2017-04-08 05:39:56.211129	f	t
762	25	28	2017-03-30 05:39:56.211157	f	t
763	25	24	2017-04-10 05:39:56.211184	f	t
764	31	11	2017-03-18 05:39:56.211211	f	t
765	31	17	2017-04-11 05:39:56.211239	f	t
766	31	24	2017-04-05 05:39:56.211266	f	t
767	31	18	2017-03-20 05:39:56.211292	f	t
768	31	32	2017-03-18 05:39:56.211345	f	t
769	31	16	2017-04-01 05:39:56.211385	f	t
770	33	35	2017-03-27 05:39:56.211424	t	t
771	33	9	2017-04-06 05:39:56.211463	t	t
772	33	11	2017-03-20 05:39:56.211492	t	t
773	33	38	2017-03-27 05:39:56.211529	t	t
774	37	37	2017-03-28 05:39:56.211555	t	t
775	37	25	2017-03-24 05:39:56.211582	t	t
776	37	38	2017-03-26 05:39:56.211608	t	t
777	37	21	2017-04-09 05:39:56.211635	t	t
778	37	14	2017-03-23 05:39:56.211661	f	t
779	37	8	2017-03-25 05:39:56.211688	f	t
780	37	21	2017-03-19 05:39:56.211714	f	t
781	37	20	2017-03-18 05:39:56.211741	f	t
782	37	33	2017-03-26 05:39:56.211768	f	t
783	37	32	2017-03-27 05:39:56.211794	f	t
784	37	22	2017-04-07 05:39:56.21182	f	t
785	37	12	2017-03-25 05:39:56.211847	f	t
786	37	34	2017-03-29 05:39:56.211874	f	t
787	37	30	2017-03-21 05:39:56.2119	f	t
788	37	9	2017-03-25 05:39:56.211926	f	t
789	37	37	2017-03-17 05:39:56.211953	f	t
790	37	16	2017-04-04 05:39:56.211979	f	t
791	37	25	2017-04-07 05:39:56.212005	f	t
792	37	23	2017-03-28 05:39:56.212031	f	t
793	37	11	2017-03-28 05:39:56.212058	f	t
794	37	29	2017-04-10 05:39:56.212084	f	t
795	37	36	2017-04-02 05:39:56.212111	f	t
796	37	30	2017-03-27 05:39:56.212137	f	t
797	37	28	2017-03-25 05:39:56.212164	f	t
798	38	16	2017-04-09 05:39:56.21219	f	t
799	38	17	2017-04-04 05:39:56.212217	f	t
800	38	28	2017-04-04 05:39:56.212243	f	t
801	38	9	2017-03-23 05:39:56.212269	f	t
802	38	22	2017-03-17 05:39:56.212296	f	t
803	38	36	2017-03-31 05:39:56.212322	f	t
804	38	26	2017-04-08 05:39:56.212348	f	t
805	38	35	2017-04-03 05:39:56.212386	f	t
806	38	20	2017-03-20 05:39:56.212413	f	t
807	38	14	2017-03-22 05:39:56.212449	f	t
808	38	38	2017-03-20 05:39:56.212475	f	t
809	43	28	2017-03-27 05:39:56.212501	t	t
810	43	33	2017-03-21 05:39:56.212528	t	t
811	43	26	2017-03-30 05:39:56.212554	t	t
812	43	19	2017-03-27 05:39:56.21258	t	t
813	43	8	2017-03-23 05:39:56.212606	t	t
814	43	36	2017-03-17 05:39:56.212632	t	t
815	43	20	2017-03-31 05:39:56.212658	t	t
816	43	22	2017-03-25 05:39:56.212685	t	t
817	43	9	2017-03-17 05:39:56.212711	t	t
818	43	24	2017-03-24 05:39:56.212737	f	t
819	43	20	2017-04-06 05:39:56.212764	f	t
820	43	27	2017-03-25 05:39:56.21279	f	t
821	43	37	2017-03-23 05:39:56.212816	f	t
822	43	17	2017-04-05 05:39:56.212842	f	t
823	43	23	2017-03-30 05:39:56.212869	f	t
824	43	14	2017-03-18 05:39:56.212895	f	t
825	43	36	2017-03-21 05:39:56.212921	f	t
826	43	21	2017-03-18 05:39:56.212958	f	t
827	43	10	2017-03-19 05:39:56.212986	f	t
828	43	35	2017-03-25 05:39:56.213013	f	t
829	43	32	2017-04-08 05:39:56.213041	f	t
830	43	25	2017-03-27 05:39:56.213068	f	t
831	43	13	2017-04-04 05:39:56.213105	f	t
832	43	9	2017-03-23 05:39:56.213132	f	t
833	43	8	2017-03-22 05:39:56.213159	f	t
834	43	18	2017-04-07 05:39:56.213185	f	t
835	43	11	2017-03-25 05:39:56.213211	f	t
836	43	12	2017-03-30 05:39:56.213238	f	t
837	43	29	2017-04-10 05:39:56.213264	f	t
838	43	30	2017-03-28 05:39:56.21329	f	t
839	43	30	2017-03-29 05:39:56.213316	f	t
840	45	33	2017-03-25 05:39:56.213342	t	t
841	45	30	2017-04-04 05:39:56.213368	t	t
842	45	11	2017-03-29 05:39:56.213394	t	t
843	45	34	2017-03-23 05:39:56.213421	t	t
844	45	20	2017-03-18 05:39:56.213447	t	t
845	45	38	2017-04-05 05:39:56.213473	t	t
846	45	26	2017-03-26 05:39:56.213499	t	t
847	45	30	2017-04-10 05:39:56.213525	t	t
848	45	13	2017-04-07 05:39:56.213551	t	t
849	45	37	2017-03-29 05:39:56.213577	t	t
850	45	19	2017-03-18 05:39:56.213604	t	t
851	45	22	2017-04-06 05:39:56.213631	f	t
852	45	29	2017-03-17 05:39:56.213657	f	t
853	45	17	2017-04-05 05:39:56.213684	f	t
854	45	20	2017-03-27 05:39:56.213711	f	t
855	45	10	2017-03-28 05:39:56.213738	f	t
856	45	38	2017-03-20 05:39:56.213765	f	t
857	45	24	2017-03-24 05:39:56.213792	f	t
858	45	27	2017-04-03 05:39:56.213818	f	t
859	45	30	2017-03-28 05:39:56.213844	f	t
860	45	16	2017-03-18 05:39:56.213871	f	t
861	45	26	2017-03-17 05:39:56.213897	f	t
862	45	18	2017-04-01 05:39:56.213923	f	t
863	45	25	2017-03-22 05:39:56.213951	f	t
864	48	21	2017-03-28 05:39:56.213977	t	t
865	48	27	2017-03-25 05:39:56.214004	t	t
866	48	35	2017-03-17 05:39:56.214031	t	t
867	48	30	2017-03-24 05:39:56.214058	t	t
868	48	37	2017-03-26 05:39:56.214085	t	t
869	52	8	2017-03-17 05:39:56.214112	t	t
870	52	34	2017-03-30 05:39:56.214139	t	t
871	52	33	2017-03-28 05:39:56.214165	t	t
872	52	35	2017-04-02 05:39:56.214193	t	t
873	52	36	2017-03-19 05:39:56.21422	t	t
874	52	21	2017-03-21 05:39:56.214246	f	t
875	52	12	2017-03-24 05:39:56.214273	f	t
876	52	11	2017-04-11 05:39:56.214299	f	t
877	52	23	2017-04-07 05:39:56.214326	f	t
878	52	29	2017-03-19 05:39:56.214353	f	t
879	52	26	2017-03-20 05:39:56.21438	f	t
880	52	25	2017-03-20 05:39:56.214406	f	t
881	52	33	2017-04-06 05:39:56.214433	f	t
882	52	15	2017-04-06 05:39:56.21446	f	t
883	52	22	2017-04-05 05:39:56.214487	f	t
884	53	33	2017-03-20 05:39:56.214514	f	t
885	53	23	2017-03-19 05:39:56.214541	f	t
886	53	25	2017-04-04 05:39:56.214568	f	t
887	53	22	2017-03-21 05:39:56.214595	f	t
888	53	32	2017-03-24 05:39:56.214621	f	t
889	53	38	2017-03-26 05:39:56.214649	f	t
890	53	30	2017-03-22 05:39:56.214687	f	t
891	53	9	2017-04-06 05:39:56.214714	f	t
892	53	34	2017-04-08 05:39:56.214742	f	t
893	53	12	2017-03-31 05:39:56.21477	f	t
\.


--
-- Name: clicked_arguments_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('clicked_arguments_uid_seq', 893, true);


--
-- Data for Name: clicked_statements; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY clicked_statements (uid, statement_uid, author_uid, "timestamp", is_up_vote, is_valid) FROM stdin;
21	1	8	2017-04-09 05:39:55.934279	t	t
22	1	13	2017-04-11 05:39:55.934391	f	t
23	2	33	2017-03-22 05:39:55.93443	t	t
24	2	10	2017-03-21 05:39:55.934463	t	t
25	2	37	2017-04-11 05:39:55.934494	t	t
26	2	27	2017-03-27 05:39:55.934524	t	t
27	2	33	2017-03-28 05:39:55.934552	t	t
28	2	8	2017-03-31 05:39:55.934581	t	t
29	2	23	2017-03-19 05:39:55.93461	t	t
30	2	21	2017-04-05 05:39:55.934639	t	t
31	3	29	2017-03-24 05:39:55.934668	f	t
32	3	28	2017-03-20 05:39:55.934696	f	t
33	3	13	2017-04-10 05:39:55.934723	f	t
34	4	18	2017-04-09 05:39:55.934751	t	t
35	4	32	2017-03-18 05:39:55.934779	t	t
36	4	17	2017-03-27 05:39:55.934807	t	t
37	4	13	2017-03-27 05:39:55.934835	f	t
38	4	30	2017-04-07 05:39:55.934864	f	t
39	4	28	2017-03-29 05:39:55.934892	f	t
40	4	17	2017-04-11 05:39:55.93492	f	t
41	4	9	2017-03-30 05:39:55.934948	f	t
42	4	27	2017-04-07 05:39:55.934976	f	t
43	4	37	2017-04-10 05:39:55.935004	f	t
44	4	28	2017-03-30 05:39:55.935032	f	t
45	4	14	2017-04-03 05:39:55.93506	f	t
46	4	16	2017-04-02 05:39:55.935087	f	t
47	5	11	2017-03-19 05:39:55.935115	t	t
48	5	10	2017-03-31 05:39:55.935143	t	t
49	5	24	2017-03-29 05:39:55.93517	t	t
50	5	25	2017-03-21 05:39:55.935197	t	t
51	5	21	2017-03-29 05:39:55.935225	t	t
52	5	30	2017-04-08 05:39:55.935253	t	t
53	5	33	2017-03-17 05:39:55.935281	t	t
54	5	25	2017-04-04 05:39:55.935308	t	t
55	5	9	2017-04-05 05:39:55.935343	t	t
56	5	10	2017-04-08 05:39:55.935372	t	t
57	5	8	2017-03-24 05:39:55.935401	f	t
58	5	12	2017-03-20 05:39:55.935429	f	t
59	5	20	2017-04-09 05:39:55.935457	f	t
60	5	30	2017-03-22 05:39:55.935484	f	t
61	5	22	2017-03-29 05:39:55.935511	f	t
62	5	36	2017-04-05 05:39:55.935538	f	t
63	5	26	2017-03-24 05:39:55.935566	f	t
64	5	9	2017-03-22 05:39:55.935593	f	t
65	5	17	2017-04-10 05:39:55.935619	f	t
66	5	10	2017-04-05 05:39:55.935646	f	t
67	5	23	2017-03-23 05:39:55.935673	f	t
68	5	30	2017-04-10 05:39:55.9357	f	t
69	5	32	2017-04-06 05:39:55.935727	f	t
70	5	22	2017-04-05 05:39:55.935753	f	t
71	5	35	2017-04-05 05:39:55.93578	f	t
72	5	25	2017-03-28 05:39:55.935818	f	t
73	6	24	2017-03-28 05:39:55.935847	t	t
74	6	18	2017-03-24 05:39:55.935876	t	t
75	6	15	2017-03-26 05:39:55.935906	t	t
76	6	35	2017-04-05 05:39:55.935936	t	t
77	6	21	2017-03-26 05:39:55.935965	t	t
78	6	14	2017-04-07 05:39:55.935996	t	t
79	6	10	2017-04-05 05:39:55.936026	t	t
80	6	27	2017-03-30 05:39:55.936055	t	t
81	6	9	2017-03-23 05:39:55.936085	t	t
82	6	21	2017-03-20 05:39:55.936114	f	t
83	6	8	2017-03-28 05:39:55.936144	f	t
84	6	25	2017-03-26 05:39:55.936174	f	t
85	6	12	2017-03-28 05:39:55.936205	f	t
86	6	23	2017-03-23 05:39:55.936235	f	t
87	6	20	2017-03-27 05:39:55.936265	f	t
88	6	21	2017-03-22 05:39:55.936296	f	t
89	7	8	2017-03-29 05:39:55.936325	t	t
90	7	27	2017-04-08 05:39:55.936356	t	t
91	7	21	2017-04-08 05:39:55.936386	t	t
92	7	29	2017-03-27 05:39:55.936417	t	t
93	7	29	2017-04-07 05:39:55.936447	t	t
94	7	15	2017-03-24 05:39:55.936476	t	t
95	7	19	2017-04-02 05:39:55.936506	t	t
96	7	36	2017-03-19 05:39:55.936535	t	t
97	7	34	2017-04-06 05:39:55.936565	t	t
98	7	8	2017-04-04 05:39:55.936595	t	t
99	7	9	2017-04-07 05:39:55.936624	t	t
100	7	34	2017-04-03 05:39:55.936653	t	t
101	7	13	2017-03-25 05:39:55.936683	t	t
102	7	27	2017-03-22 05:39:55.936712	t	t
103	7	33	2017-03-25 05:39:55.936741	t	t
104	7	30	2017-04-10 05:39:55.93677	f	t
105	7	25	2017-03-20 05:39:55.936808	f	t
106	7	9	2017-03-24 05:39:55.936835	f	t
107	7	30	2017-03-20 05:39:55.936862	f	t
108	7	26	2017-03-26 05:39:55.936888	f	t
109	7	13	2017-03-27 05:39:55.936915	f	t
110	7	38	2017-03-28 05:39:55.936942	f	t
111	7	32	2017-04-09 05:39:55.936969	f	t
112	7	14	2017-03-22 05:39:55.936995	f	t
113	7	36	2017-03-30 05:39:55.937022	f	t
114	7	8	2017-04-09 05:39:55.937049	f	t
115	7	16	2017-03-27 05:39:55.937076	f	t
116	7	15	2017-03-21 05:39:55.937102	f	t
117	7	20	2017-03-25 05:39:55.937129	f	t
118	7	30	2017-03-19 05:39:55.937155	f	t
119	8	36	2017-04-02 05:39:55.937182	t	t
120	8	18	2017-03-31 05:39:55.937209	t	t
121	8	12	2017-03-19 05:39:55.937236	t	t
122	8	17	2017-03-31 05:39:55.937263	t	t
123	8	22	2017-03-19 05:39:55.937291	t	t
124	8	20	2017-03-18 05:39:55.937319	t	t
125	8	12	2017-03-17 05:39:55.937346	t	t
126	8	13	2017-03-21 05:39:55.937373	t	t
127	8	25	2017-04-04 05:39:55.937401	t	t
128	8	26	2017-03-23 05:39:55.93744	t	t
129	8	25	2017-04-09 05:39:55.937489	f	t
130	8	8	2017-04-09 05:39:55.937531	f	t
131	8	37	2017-03-28 05:39:55.93756	f	t
132	8	10	2017-04-10 05:39:55.937587	f	t
133	8	29	2017-03-25 05:39:55.937614	f	t
134	8	17	2017-03-27 05:39:55.937642	f	t
135	8	33	2017-03-25 05:39:55.937669	f	t
136	8	20	2017-03-29 05:39:55.937696	f	t
137	8	30	2017-04-07 05:39:55.937723	f	t
138	9	9	2017-03-23 05:39:55.937751	t	t
139	9	18	2017-04-11 05:39:55.937779	t	t
140	9	25	2017-04-02 05:39:55.937806	t	t
141	9	9	2017-04-11 05:39:55.937833	t	t
142	9	33	2017-03-25 05:39:55.93786	t	t
143	9	12	2017-03-17 05:39:55.937887	t	t
144	9	16	2017-04-02 05:39:55.937915	t	t
145	9	28	2017-03-20 05:39:55.937942	t	t
146	9	36	2017-04-05 05:39:55.937969	f	t
147	9	18	2017-03-23 05:39:55.937996	f	t
148	9	15	2017-04-05 05:39:55.938023	f	t
149	9	37	2017-04-07 05:39:55.93805	f	t
150	9	18	2017-04-08 05:39:55.938077	f	t
151	9	19	2017-03-30 05:39:55.938104	f	t
152	9	33	2017-04-11 05:39:55.938132	f	t
153	10	13	2017-04-02 05:39:55.938159	t	t
154	10	26	2017-04-03 05:39:55.938186	t	t
155	10	9	2017-03-17 05:39:55.938213	t	t
156	10	37	2017-03-26 05:39:55.93824	t	t
157	10	19	2017-03-25 05:39:55.938268	t	t
158	10	37	2017-04-03 05:39:55.938295	t	t
159	10	25	2017-04-11 05:39:55.938322	t	t
160	10	35	2017-04-01 05:39:55.938349	t	t
161	10	29	2017-03-29 05:39:55.938376	t	t
162	10	19	2017-03-22 05:39:55.938403	t	t
163	10	10	2017-03-29 05:39:55.93843	t	t
164	10	29	2017-04-02 05:39:55.938457	t	t
165	10	22	2017-03-29 05:39:55.938483	t	t
166	10	36	2017-04-06 05:39:55.93851	t	t
167	10	27	2017-04-07 05:39:55.938537	t	t
168	10	28	2017-04-06 05:39:55.938564	t	t
169	10	9	2017-04-01 05:39:55.938591	t	t
170	10	9	2017-03-20 05:39:55.938618	t	t
171	10	10	2017-04-03 05:39:55.938644	t	t
172	10	38	2017-04-11 05:39:55.938671	t	t
173	10	32	2017-04-02 05:39:55.938698	t	t
174	10	37	2017-03-28 05:39:55.938725	f	t
175	10	10	2017-04-02 05:39:55.938752	f	t
176	10	23	2017-03-18 05:39:55.938778	f	t
177	10	13	2017-03-23 05:39:55.938805	f	t
178	10	34	2017-04-06 05:39:55.938833	f	t
179	10	26	2017-03-19 05:39:55.938861	f	t
180	10	12	2017-04-05 05:39:55.938887	f	t
181	10	23	2017-03-17 05:39:55.938914	f	t
182	10	22	2017-03-29 05:39:55.938942	f	t
183	10	30	2017-03-30 05:39:55.938968	f	t
184	10	37	2017-03-26 05:39:55.938995	f	t
185	10	17	2017-04-09 05:39:55.939022	f	t
186	10	35	2017-03-30 05:39:55.939049	f	t
187	10	13	2017-04-09 05:39:55.939076	f	t
188	10	23	2017-04-11 05:39:55.939104	f	t
189	10	32	2017-03-19 05:39:55.939147	f	t
190	10	23	2017-03-31 05:39:55.939196	f	t
191	10	30	2017-03-31 05:39:55.939227	f	t
192	10	17	2017-03-30 05:39:55.939256	f	t
193	10	20	2017-03-21 05:39:55.939283	f	t
194	10	26	2017-03-29 05:39:55.93931	f	t
195	10	38	2017-03-22 05:39:55.939345	f	t
196	10	13	2017-04-07 05:39:55.939374	f	t
197	10	22	2017-03-26 05:39:55.939403	f	t
198	10	15	2017-04-04 05:39:55.939431	f	t
199	10	26	2017-04-10 05:39:55.939459	f	t
200	10	37	2017-04-09 05:39:55.939487	f	t
201	11	30	2017-04-03 05:39:55.939514	t	t
202	11	26	2017-03-28 05:39:55.939542	t	t
203	12	19	2017-04-07 05:39:55.93957	t	t
204	12	22	2017-03-28 05:39:55.939597	f	t
205	12	16	2017-03-31 05:39:55.939623	f	t
206	12	18	2017-03-19 05:39:55.939651	f	t
207	12	9	2017-04-03 05:39:55.939678	f	t
208	12	20	2017-03-27 05:39:55.939706	f	t
209	12	29	2017-04-09 05:39:55.939733	f	t
210	12	20	2017-04-10 05:39:55.939762	f	t
211	13	14	2017-03-27 05:39:55.939789	t	t
212	13	9	2017-03-17 05:39:55.939817	t	t
213	13	35	2017-04-08 05:39:55.939845	t	t
214	13	37	2017-03-17 05:39:55.939873	t	t
215	13	22	2017-03-29 05:39:55.9399	t	t
216	13	34	2017-03-24 05:39:55.939927	t	t
217	13	23	2017-03-30 05:39:55.939956	t	t
218	13	8	2017-04-08 05:39:55.939984	t	t
219	13	25	2017-03-19 05:39:55.940012	t	t
220	13	29	2017-03-24 05:39:55.940039	f	t
221	13	10	2017-03-30 05:39:55.940066	f	t
222	13	19	2017-03-30 05:39:55.940094	f	t
223	13	23	2017-03-28 05:39:55.940121	f	t
224	13	38	2017-03-19 05:39:55.940148	f	t
225	13	30	2017-03-25 05:39:55.940175	f	t
226	13	30	2017-03-22 05:39:55.940202	f	t
227	13	17	2017-04-04 05:39:55.940229	f	t
228	13	19	2017-04-04 05:39:55.940257	f	t
229	13	11	2017-03-22 05:39:55.940284	f	t
230	14	36	2017-04-09 05:39:55.940311	t	t
231	14	34	2017-03-24 05:39:55.94035	t	t
232	14	37	2017-04-09 05:39:55.940398	t	t
233	14	30	2017-04-02 05:39:55.940445	t	t
234	14	22	2017-03-30 05:39:55.940477	t	t
235	15	26	2017-03-18 05:39:55.940505	f	t
236	15	30	2017-04-03 05:39:55.940533	f	t
237	15	32	2017-03-25 05:39:55.940564	f	t
238	16	17	2017-03-18 05:39:55.940615	t	t
239	16	30	2017-03-24 05:39:55.940658	t	t
240	16	13	2017-03-18 05:39:55.940688	t	t
241	16	30	2017-04-08 05:39:55.940717	t	t
242	16	30	2017-04-06 05:39:55.940746	t	t
243	16	15	2017-03-31 05:39:55.940774	t	t
244	16	22	2017-04-07 05:39:55.940801	t	t
245	16	24	2017-04-02 05:39:55.940837	t	t
246	16	29	2017-03-18 05:39:55.940864	t	t
247	16	9	2017-04-08 05:39:55.940891	t	t
248	16	10	2017-03-18 05:39:55.940918	t	t
249	16	18	2017-03-21 05:39:55.940944	t	t
250	16	26	2017-03-24 05:39:55.940971	t	t
251	16	13	2017-04-04 05:39:55.940997	t	t
252	16	28	2017-03-20 05:39:55.941024	f	t
253	16	26	2017-03-25 05:39:55.94105	f	t
254	16	8	2017-04-05 05:39:55.941077	f	t
255	16	38	2017-03-31 05:39:55.941103	f	t
256	17	18	2017-04-07 05:39:55.94113	t	t
257	17	15	2017-03-27 05:39:55.941157	t	t
258	17	34	2017-03-28 05:39:55.941183	t	t
259	17	35	2017-04-05 05:39:55.94121	t	t
260	17	11	2017-04-09 05:39:55.941236	t	t
261	17	33	2017-03-23 05:39:55.941262	t	t
262	17	28	2017-04-07 05:39:55.941288	t	t
263	17	8	2017-04-06 05:39:55.941314	f	t
264	17	11	2017-04-03 05:39:55.941341	f	t
265	18	30	2017-03-20 05:39:55.941367	t	t
266	18	35	2017-04-02 05:39:55.941394	f	t
267	18	18	2017-04-02 05:39:55.94142	f	t
268	18	34	2017-03-30 05:39:55.941447	f	t
269	18	30	2017-04-06 05:39:55.941474	f	t
270	18	38	2017-04-11 05:39:55.94152	f	t
271	18	28	2017-04-09 05:39:55.941547	f	t
272	18	12	2017-04-09 05:39:55.941574	f	t
273	19	21	2017-03-17 05:39:55.9416	t	t
274	19	24	2017-04-03 05:39:55.941627	t	t
275	19	17	2017-03-22 05:39:55.941653	t	t
276	19	17	2017-04-05 05:39:55.941679	t	t
277	19	20	2017-03-28 05:39:55.941706	t	t
278	19	20	2017-03-28 05:39:55.941732	t	t
279	19	36	2017-03-21 05:39:55.941759	t	t
280	19	11	2017-03-31 05:39:55.941785	t	t
281	19	16	2017-03-31 05:39:55.941812	f	t
282	19	9	2017-04-04 05:39:55.941838	f	t
283	19	30	2017-03-20 05:39:55.941864	f	t
284	20	23	2017-03-23 05:39:55.94189	t	t
285	20	36	2017-04-09 05:39:55.941917	t	t
286	20	12	2017-04-03 05:39:55.941943	t	t
287	20	33	2017-04-10 05:39:55.941969	t	t
288	20	37	2017-03-24 05:39:55.941995	t	t
289	20	16	2017-04-10 05:39:55.942021	t	t
290	20	13	2017-04-08 05:39:55.942048	t	t
291	20	32	2017-03-17 05:39:55.942074	t	t
292	20	21	2017-03-24 05:39:55.942101	t	t
293	20	12	2017-04-09 05:39:55.942127	t	t
294	20	8	2017-03-29 05:39:55.942153	t	t
295	20	26	2017-03-19 05:39:55.94218	t	t
296	20	28	2017-03-25 05:39:55.942206	t	t
297	20	36	2017-04-07 05:39:55.942233	t	t
298	20	19	2017-04-08 05:39:55.942259	t	t
299	20	10	2017-03-23 05:39:55.942286	f	t
300	20	23	2017-03-18 05:39:55.942312	f	t
301	20	24	2017-04-11 05:39:55.942338	f	t
302	20	17	2017-04-02 05:39:55.942364	f	t
303	20	22	2017-03-18 05:39:55.942391	f	t
304	20	15	2017-03-25 05:39:55.942418	f	t
305	20	22	2017-04-01 05:39:55.942445	f	t
306	20	29	2017-04-01 05:39:55.942471	f	t
307	20	30	2017-04-04 05:39:55.942497	f	t
308	20	37	2017-04-07 05:39:55.942524	f	t
309	21	34	2017-04-07 05:39:55.942549	t	t
310	21	30	2017-03-26 05:39:55.942575	t	t
311	21	25	2017-04-07 05:39:55.942601	t	t
312	21	13	2017-03-25 05:39:55.942627	f	t
313	21	17	2017-03-19 05:39:55.942653	f	t
314	21	16	2017-04-09 05:39:55.942679	f	t
315	22	27	2017-03-25 05:39:55.942706	f	t
316	22	16	2017-04-09 05:39:55.942732	f	t
317	22	10	2017-03-19 05:39:55.942758	f	t
318	23	30	2017-03-27 05:39:55.942784	f	t
319	23	19	2017-03-29 05:39:55.94281	f	t
320	24	9	2017-04-07 05:39:55.942836	t	t
321	24	37	2017-03-30 05:39:55.942862	t	t
322	24	35	2017-04-02 05:39:55.942888	t	t
323	24	18	2017-03-23 05:39:55.942914	t	t
324	24	13	2017-04-10 05:39:55.94294	t	t
325	24	35	2017-03-25 05:39:55.942966	t	t
326	24	22	2017-04-06 05:39:55.942992	t	t
327	24	29	2017-03-29 05:39:55.943018	t	t
328	24	15	2017-03-21 05:39:55.943044	t	t
329	24	38	2017-04-09 05:39:55.943071	t	t
330	24	10	2017-03-21 05:39:55.943097	t	t
331	24	11	2017-04-09 05:39:55.943123	t	t
332	24	18	2017-03-23 05:39:55.943149	f	t
333	24	16	2017-03-31 05:39:55.943175	f	t
334	25	8	2017-03-23 05:39:55.943201	f	t
335	25	8	2017-03-18 05:39:55.943227	f	t
336	25	19	2017-03-17 05:39:55.943253	f	t
337	25	18	2017-04-09 05:39:55.943278	f	t
338	26	24	2017-03-31 05:39:55.943305	t	t
339	26	10	2017-04-10 05:39:55.943351	t	t
340	26	21	2017-03-20 05:39:55.943382	t	t
341	26	30	2017-04-06 05:39:55.943419	t	t
342	26	8	2017-03-24 05:39:55.943446	t	t
343	26	32	2017-03-25 05:39:55.943473	t	t
344	26	11	2017-04-07 05:39:55.9435	t	t
345	26	27	2017-03-29 05:39:55.943525	f	t
346	26	30	2017-03-30 05:39:55.943552	f	t
347	26	16	2017-04-05 05:39:55.943578	f	t
348	27	12	2017-03-18 05:39:55.943605	t	t
349	27	10	2017-03-25 05:39:55.943631	t	t
350	27	11	2017-03-18 05:39:55.943657	t	t
351	27	26	2017-03-29 05:39:55.943683	t	t
352	27	24	2017-03-29 05:39:55.943709	t	t
353	27	30	2017-03-30 05:39:55.943735	t	t
354	27	27	2017-03-20 05:39:55.943761	f	t
355	27	13	2017-04-08 05:39:55.943788	f	t
356	27	33	2017-03-31 05:39:55.943814	f	t
357	27	12	2017-03-24 05:39:55.943851	f	t
358	27	11	2017-04-02 05:39:55.943878	f	t
359	28	30	2017-03-21 05:39:55.943904	t	t
360	28	8	2017-03-24 05:39:55.943931	t	t
361	28	14	2017-03-17 05:39:55.943959	t	t
362	28	21	2017-03-28 05:39:55.943986	t	t
363	28	37	2017-04-06 05:39:55.944014	t	t
364	28	38	2017-03-19 05:39:55.944041	t	t
365	28	35	2017-04-03 05:39:55.944068	t	t
366	28	16	2017-04-09 05:39:55.944096	t	t
367	28	38	2017-03-20 05:39:55.944123	t	t
368	28	9	2017-03-18 05:39:55.94415	t	t
369	28	37	2017-03-23 05:39:55.944178	t	t
370	28	26	2017-03-23 05:39:55.944206	t	t
371	28	11	2017-03-28 05:39:55.944233	t	t
372	28	38	2017-03-29 05:39:55.94426	f	t
373	28	30	2017-03-25 05:39:55.944287	f	t
374	28	24	2017-04-10 05:39:55.944313	f	t
375	28	18	2017-03-18 05:39:55.944341	f	t
376	28	35	2017-04-01 05:39:55.944368	f	t
377	28	17	2017-04-11 05:39:55.944395	f	t
378	28	15	2017-03-22 05:39:55.944422	f	t
379	28	18	2017-04-08 05:39:55.944449	f	t
380	28	34	2017-03-22 05:39:55.944477	f	t
381	28	14	2017-04-05 05:39:55.944504	f	t
382	28	14	2017-03-29 05:39:55.944531	f	t
383	28	34	2017-04-03 05:39:55.944558	f	t
384	28	28	2017-03-23 05:39:55.944585	f	t
385	28	26	2017-03-21 05:39:55.944611	f	t
386	28	30	2017-03-24 05:39:55.944638	f	t
387	29	9	2017-04-03 05:39:55.944665	t	t
388	29	36	2017-03-31 05:39:55.944692	t	t
389	29	10	2017-03-29 05:39:55.944719	t	t
390	29	32	2017-03-29 05:39:55.944746	t	t
391	29	14	2017-04-08 05:39:55.944773	t	t
392	29	28	2017-03-18 05:39:55.9448	t	t
393	29	18	2017-04-01 05:39:55.944835	f	t
394	29	26	2017-03-22 05:39:55.944862	f	t
395	29	35	2017-04-05 05:39:55.944889	f	t
396	29	9	2017-04-01 05:39:55.944915	f	t
397	29	30	2017-03-28 05:39:55.944941	f	t
398	29	18	2017-03-20 05:39:55.944967	f	t
399	29	17	2017-04-07 05:39:55.944994	f	t
400	29	15	2017-03-25 05:39:55.94502	f	t
401	29	17	2017-04-01 05:39:55.945046	f	t
402	29	23	2017-03-23 05:39:55.945072	f	t
403	29	10	2017-03-25 05:39:55.945098	f	t
404	29	27	2017-04-10 05:39:55.945125	f	t
405	30	24	2017-03-22 05:39:55.945151	t	t
406	30	17	2017-04-05 05:39:55.945178	t	t
407	30	25	2017-03-20 05:39:55.945205	f	t
408	30	19	2017-04-07 05:39:55.945231	f	t
409	30	27	2017-03-20 05:39:55.945257	f	t
410	30	18	2017-03-28 05:39:55.945283	f	t
411	30	34	2017-03-23 05:39:55.945309	f	t
412	31	26	2017-03-23 05:39:55.945336	t	t
413	31	32	2017-04-06 05:39:55.945362	t	t
414	31	25	2017-04-03 05:39:55.945388	f	t
415	31	30	2017-03-27 05:39:55.945414	f	t
416	31	22	2017-04-06 05:39:55.94544	f	t
417	31	29	2017-03-17 05:39:55.945467	f	t
418	32	9	2017-03-20 05:39:55.945493	t	t
419	32	20	2017-04-09 05:39:55.945519	f	t
420	32	23	2017-03-28 05:39:55.945545	f	t
421	32	30	2017-03-27 05:39:55.945572	f	t
422	32	33	2017-04-05 05:39:55.945598	f	t
423	32	24	2017-04-06 05:39:55.945636	f	t
424	32	36	2017-03-25 05:39:55.945663	f	t
425	32	16	2017-04-01 05:39:55.94569	f	t
426	32	33	2017-03-30 05:39:55.945717	f	t
427	33	27	2017-03-17 05:39:55.945744	t	t
428	33	13	2017-04-11 05:39:55.94578	t	t
429	33	10	2017-03-18 05:39:55.945806	t	t
430	33	32	2017-04-01 05:39:55.945833	t	t
431	33	30	2017-03-24 05:39:55.945869	t	t
432	33	37	2017-03-24 05:39:55.945896	f	t
433	34	26	2017-03-20 05:39:55.945923	f	t
434	34	15	2017-03-27 05:39:55.945951	f	t
435	35	9	2017-03-29 05:39:55.945978	t	t
436	35	11	2017-03-21 05:39:55.946006	t	t
437	36	11	2017-03-22 05:39:55.946033	t	t
438	36	22	2017-04-10 05:39:55.94606	f	t
439	36	18	2017-03-30 05:39:55.946087	f	t
440	36	26	2017-04-03 05:39:55.946114	f	t
441	36	32	2017-04-07 05:39:55.946141	f	t
442	36	36	2017-03-26 05:39:55.946169	f	t
443	37	16	2017-03-26 05:39:55.946196	t	t
444	37	10	2017-04-09 05:39:55.946223	f	t
445	37	17	2017-04-02 05:39:55.94625	f	t
446	37	34	2017-03-20 05:39:55.946277	f	t
447	37	22	2017-03-21 05:39:55.946304	f	t
448	37	8	2017-03-24 05:39:55.946331	f	t
449	37	24	2017-03-28 05:39:55.946357	f	t
450	37	10	2017-04-09 05:39:55.946384	f	t
451	37	14	2017-03-20 05:39:55.94641	f	t
452	38	30	2017-03-27 05:39:55.946436	t	t
453	38	21	2017-03-19 05:39:55.946463	t	t
454	38	15	2017-03-25 05:39:55.94649	f	t
455	38	33	2017-04-03 05:39:55.946516	f	t
456	39	37	2017-03-20 05:39:55.946543	t	t
457	39	22	2017-04-06 05:39:55.946569	t	t
458	39	20	2017-03-19 05:39:55.946596	t	t
459	39	28	2017-03-17 05:39:55.946623	t	t
460	39	23	2017-04-05 05:39:55.94665	t	t
461	39	34	2017-04-04 05:39:55.946677	t	t
462	39	27	2017-04-11 05:39:55.946703	t	t
463	39	15	2017-04-11 05:39:55.946729	t	t
464	39	10	2017-04-03 05:39:55.946755	t	t
465	39	15	2017-03-17 05:39:55.946782	t	t
466	39	30	2017-04-01 05:39:55.94681	t	t
467	39	11	2017-03-28 05:39:55.946836	f	t
468	39	27	2017-03-30 05:39:55.946863	f	t
469	40	28	2017-03-29 05:39:55.946891	t	t
470	40	25	2017-04-06 05:39:55.946918	t	t
471	40	37	2017-03-17 05:39:55.946946	f	t
472	40	10	2017-03-20 05:39:55.946973	f	t
473	40	20	2017-04-08 05:39:55.947	f	t
474	40	36	2017-04-11 05:39:55.947027	f	t
475	40	17	2017-03-29 05:39:55.947055	f	t
476	40	38	2017-03-31 05:39:55.947083	f	t
477	40	9	2017-04-03 05:39:55.947109	f	t
478	40	15	2017-03-25 05:39:55.947136	f	t
479	40	26	2017-03-17 05:39:55.947163	f	t
480	40	35	2017-04-06 05:39:55.947191	f	t
481	40	8	2017-04-10 05:39:55.947218	f	t
482	41	11	2017-03-26 05:39:55.947245	t	t
483	41	37	2017-04-10 05:39:55.947272	t	t
484	41	23	2017-04-04 05:39:55.9473	t	t
485	41	30	2017-04-07 05:39:55.947328	t	t
486	41	12	2017-03-23 05:39:55.947362	t	t
487	41	30	2017-03-19 05:39:55.94739	t	t
488	41	27	2017-04-04 05:39:55.947417	t	t
489	41	12	2017-04-03 05:39:55.947444	t	t
490	41	33	2017-03-18 05:39:55.947472	t	t
491	41	18	2017-03-29 05:39:55.947499	t	t
492	41	10	2017-04-02 05:39:55.947526	f	t
493	41	8	2017-04-01 05:39:55.947553	f	t
494	41	15	2017-03-28 05:39:55.947581	f	t
495	41	21	2017-03-24 05:39:55.947608	f	t
496	41	13	2017-04-11 05:39:55.947635	f	t
497	41	17	2017-04-02 05:39:55.947662	f	t
498	41	10	2017-04-08 05:39:55.947689	f	t
499	41	29	2017-04-02 05:39:55.947716	f	t
500	41	24	2017-03-22 05:39:55.947744	f	t
501	41	23	2017-04-04 05:39:55.947771	f	t
502	41	34	2017-04-11 05:39:55.947799	f	t
503	41	17	2017-04-08 05:39:55.947847	f	t
504	41	23	2017-03-25 05:39:55.947876	f	t
505	41	15	2017-03-27 05:39:55.947903	f	t
506	41	27	2017-04-10 05:39:55.94793	f	t
507	41	11	2017-03-23 05:39:55.947958	f	t
508	42	37	2017-03-31 05:39:55.947985	t	t
509	42	28	2017-04-03 05:39:55.948012	t	t
510	42	30	2017-03-29 05:39:55.948039	t	t
511	42	38	2017-03-26 05:39:55.948067	t	t
512	42	15	2017-03-29 05:39:55.948094	t	t
513	42	37	2017-04-07 05:39:55.948121	t	t
514	42	12	2017-03-25 05:39:55.948162	t	t
515	42	12	2017-03-27 05:39:55.94822	t	t
516	42	11	2017-04-03 05:39:55.948279	t	t
517	42	20	2017-04-05 05:39:55.948312	t	t
518	42	34	2017-03-22 05:39:55.948351	t	t
519	42	33	2017-04-01 05:39:55.948378	t	t
520	42	32	2017-04-02 05:39:55.948406	f	t
521	42	11	2017-04-07 05:39:55.948433	f	t
522	42	21	2017-03-18 05:39:55.948461	f	t
523	42	23	2017-03-18 05:39:55.948488	f	t
524	42	16	2017-03-20 05:39:55.948515	f	t
525	42	34	2017-03-22 05:39:55.948543	f	t
526	42	30	2017-03-26 05:39:55.948569	f	t
527	42	9	2017-03-26 05:39:55.948597	f	t
528	42	29	2017-04-03 05:39:55.948625	f	t
529	42	17	2017-03-31 05:39:55.948652	f	t
530	42	36	2017-03-22 05:39:55.94868	f	t
531	42	37	2017-03-24 05:39:55.948707	f	t
532	42	16	2017-03-19 05:39:55.948733	f	t
533	42	14	2017-04-06 05:39:55.948761	f	t
534	42	36	2017-04-09 05:39:55.948788	f	t
535	42	30	2017-04-10 05:39:55.948815	f	t
536	43	21	2017-04-11 05:39:55.948842	t	t
537	43	15	2017-03-19 05:39:55.948868	t	t
538	43	9	2017-04-04 05:39:55.948895	t	t
539	43	33	2017-03-22 05:39:55.948922	t	t
540	43	29	2017-04-07 05:39:55.948949	f	t
541	43	11	2017-03-26 05:39:55.948976	f	t
542	44	38	2017-03-30 05:39:55.949002	t	t
543	44	37	2017-03-24 05:39:55.949029	t	t
544	44	9	2017-04-07 05:39:55.949055	t	t
545	44	29	2017-04-10 05:39:55.949082	t	t
546	44	19	2017-03-21 05:39:55.949108	t	t
547	44	13	2017-04-09 05:39:55.949135	t	t
548	44	32	2017-03-23 05:39:55.949161	t	t
549	44	14	2017-03-23 05:39:55.949188	t	t
550	44	25	2017-04-07 05:39:55.949215	t	t
551	44	10	2017-03-22 05:39:55.949242	f	t
552	44	36	2017-03-18 05:39:55.949267	f	t
553	45	24	2017-03-17 05:39:55.949294	t	t
554	45	15	2017-04-01 05:39:55.949321	t	t
555	45	11	2017-03-30 05:39:55.949347	t	t
556	45	16	2017-03-18 05:39:55.949375	t	t
557	45	16	2017-04-03 05:39:55.949418	t	t
558	45	13	2017-04-09 05:39:55.949469	t	t
559	45	19	2017-04-04 05:39:55.949507	t	t
560	45	18	2017-04-10 05:39:55.94956	t	t
561	45	9	2017-04-05 05:39:55.949626	t	t
562	45	21	2017-03-26 05:39:55.949666	f	t
563	45	17	2017-04-04 05:39:55.949695	f	t
564	45	32	2017-03-31 05:39:55.94973	f	t
565	45	19	2017-03-18 05:39:55.94976	f	t
566	45	22	2017-03-25 05:39:55.949789	f	t
567	46	18	2017-04-01 05:39:55.949816	f	t
568	46	34	2017-03-29 05:39:55.949846	f	t
569	46	36	2017-03-25 05:39:55.949899	f	t
570	46	15	2017-04-11 05:39:55.949947	f	t
571	46	32	2017-03-19 05:39:55.949977	f	t
572	46	18	2017-03-30 05:39:55.950006	f	t
573	46	11	2017-03-25 05:39:55.950034	f	t
574	47	21	2017-03-23 05:39:55.950063	f	t
575	47	8	2017-03-20 05:39:55.95009	f	t
576	48	35	2017-04-01 05:39:55.950118	t	t
577	48	8	2017-03-22 05:39:55.950146	t	t
578	48	32	2017-04-01 05:39:55.950175	t	t
579	48	18	2017-03-27 05:39:55.950203	t	t
580	48	30	2017-04-07 05:39:55.95023	t	t
581	48	36	2017-03-21 05:39:55.950258	t	t
582	48	13	2017-04-05 05:39:55.950286	t	t
583	48	16	2017-03-22 05:39:55.950314	t	t
584	48	34	2017-04-06 05:39:55.950342	t	t
585	48	34	2017-04-01 05:39:55.95037	t	t
586	48	13	2017-04-05 05:39:55.950398	t	t
587	48	34	2017-03-27 05:39:55.950426	t	t
588	48	37	2017-03-31 05:39:55.950454	t	t
589	48	38	2017-03-30 05:39:55.950482	t	t
590	48	9	2017-03-18 05:39:55.95052	t	t
591	48	24	2017-03-18 05:39:55.950566	t	t
592	48	17	2017-04-05 05:39:55.950596	t	t
593	48	16	2017-04-01 05:39:55.950624	f	t
594	48	38	2017-04-01 05:39:55.950653	f	t
595	48	27	2017-04-08 05:39:55.950681	f	t
596	48	27	2017-04-05 05:39:55.950709	f	t
597	48	29	2017-04-02 05:39:55.950737	f	t
598	48	13	2017-03-26 05:39:55.950765	f	t
599	48	9	2017-03-29 05:39:55.950793	f	t
600	48	16	2017-03-17 05:39:55.950821	f	t
601	48	27	2017-04-07 05:39:55.950848	f	t
602	48	17	2017-04-04 05:39:55.950876	f	t
603	48	30	2017-04-05 05:39:55.950903	f	t
604	48	15	2017-03-31 05:39:55.950931	f	t
605	48	22	2017-04-06 05:39:55.950958	f	t
606	48	8	2017-03-28 05:39:55.950985	f	t
607	48	30	2017-04-10 05:39:55.951013	f	t
608	48	25	2017-03-18 05:39:55.951041	f	t
609	49	23	2017-03-18 05:39:55.951068	f	t
610	49	21	2017-04-03 05:39:55.951095	f	t
611	49	33	2017-03-28 05:39:55.951122	f	t
612	49	15	2017-03-25 05:39:55.95115	f	t
613	49	20	2017-04-03 05:39:55.951177	f	t
614	50	38	2017-03-25 05:39:55.951204	t	t
615	50	18	2017-03-19 05:39:55.951232	f	t
616	50	19	2017-04-07 05:39:55.951259	f	t
617	50	17	2017-03-28 05:39:55.951286	f	t
618	50	32	2017-04-05 05:39:55.951313	f	t
619	50	16	2017-03-21 05:39:55.951351	f	t
620	50	12	2017-04-11 05:39:55.95138	f	t
621	50	19	2017-04-08 05:39:55.951408	f	t
622	51	24	2017-04-01 05:39:55.951436	t	t
623	51	21	2017-04-04 05:39:55.951463	t	t
624	51	10	2017-03-29 05:39:55.951491	t	t
625	51	15	2017-04-07 05:39:55.951518	t	t
626	51	18	2017-03-21 05:39:55.951546	t	t
627	51	21	2017-03-27 05:39:55.951574	t	t
628	51	23	2017-04-03 05:39:55.951602	t	t
629	51	37	2017-04-08 05:39:55.95163	t	t
630	51	20	2017-04-08 05:39:55.951657	t	t
631	51	10	2017-04-07 05:39:55.951684	t	t
632	51	35	2017-04-05 05:39:55.951712	t	t
633	51	16	2017-04-06 05:39:55.951739	t	t
634	51	11	2017-04-07 05:39:55.951767	t	t
635	51	11	2017-03-26 05:39:55.951794	t	t
636	51	30	2017-03-30 05:39:55.951821	t	t
637	51	23	2017-04-10 05:39:55.95186	f	t
638	51	18	2017-04-05 05:39:55.951893	f	t
639	51	37	2017-03-22 05:39:55.951925	f	t
640	51	34	2017-04-11 05:39:55.951959	f	t
641	51	28	2017-03-18 05:39:55.951991	f	t
642	51	12	2017-03-26 05:39:55.952025	f	t
643	51	22	2017-04-03 05:39:55.952058	f	t
644	51	26	2017-04-09 05:39:55.952092	f	t
645	51	8	2017-04-03 05:39:55.952126	f	t
646	51	25	2017-04-10 05:39:55.95216	f	t
647	51	14	2017-04-08 05:39:55.952193	f	t
648	51	28	2017-04-08 05:39:55.952226	f	t
649	51	11	2017-03-30 05:39:55.95226	f	t
650	51	34	2017-03-22 05:39:55.952293	f	t
651	51	30	2017-04-08 05:39:55.952326	f	t
652	51	24	2017-03-30 05:39:55.95236	f	t
653	51	36	2017-04-06 05:39:55.952394	f	t
654	51	22	2017-03-21 05:39:55.952428	f	t
655	51	22	2017-04-05 05:39:55.95246	f	t
656	52	8	2017-03-26 05:39:55.952494	f	t
657	52	36	2017-04-02 05:39:55.952528	f	t
658	52	8	2017-03-25 05:39:55.952561	f	t
659	52	24	2017-03-24 05:39:55.952596	f	t
660	52	15	2017-03-17 05:39:55.95263	f	t
661	52	30	2017-03-20 05:39:55.952663	f	t
662	52	23	2017-03-28 05:39:55.952696	f	t
663	53	25	2017-03-22 05:39:55.952729	t	t
664	53	11	2017-04-09 05:39:55.952763	t	t
665	53	34	2017-03-18 05:39:55.952796	t	t
666	53	34	2017-03-27 05:39:55.952839	t	t
667	53	33	2017-04-09 05:39:55.952867	t	t
668	53	15	2017-04-05 05:39:55.952894	t	t
669	53	10	2017-04-09 05:39:55.952921	t	t
670	53	29	2017-04-06 05:39:55.952949	t	t
671	53	38	2017-03-27 05:39:55.952976	t	t
672	53	17	2017-04-11 05:39:55.953004	t	t
673	53	27	2017-03-23 05:39:55.953031	t	t
674	53	18	2017-03-31 05:39:55.953058	t	t
675	53	27	2017-03-24 05:39:55.953086	t	t
676	53	16	2017-04-09 05:39:55.953114	t	t
677	53	34	2017-03-20 05:39:55.953141	t	t
678	53	22	2017-03-23 05:39:55.953169	t	t
679	53	25	2017-03-23 05:39:55.953196	t	t
680	53	14	2017-03-20 05:39:55.953223	t	t
681	53	8	2017-04-11 05:39:55.953251	t	t
682	53	8	2017-03-26 05:39:55.953278	t	t
683	53	15	2017-03-22 05:39:55.953305	f	t
684	53	14	2017-03-18 05:39:55.953332	f	t
685	53	26	2017-03-29 05:39:55.95336	f	t
686	53	29	2017-04-08 05:39:55.953388	f	t
687	53	38	2017-03-18 05:39:55.953415	f	t
688	53	30	2017-04-11 05:39:55.953442	f	t
689	53	29	2017-03-23 05:39:55.953469	f	t
690	53	38	2017-03-29 05:39:55.953497	f	t
691	53	28	2017-03-31 05:39:55.953524	f	t
692	53	38	2017-04-01 05:39:55.953552	f	t
693	54	17	2017-04-11 05:39:55.95358	t	t
694	54	18	2017-04-07 05:39:55.953607	t	t
695	54	16	2017-03-18 05:39:55.953635	t	t
696	54	18	2017-03-25 05:39:55.953662	t	t
697	54	15	2017-03-26 05:39:55.953689	f	t
698	54	25	2017-03-20 05:39:55.953717	f	t
699	54	26	2017-03-29 05:39:55.953744	f	t
700	55	23	2017-04-06 05:39:55.953772	t	t
701	55	16	2017-03-19 05:39:55.9538	t	t
702	55	25	2017-04-10 05:39:55.95385	t	t
703	55	25	2017-03-26 05:39:55.953895	t	t
704	55	22	2017-04-08 05:39:55.953925	t	t
705	55	17	2017-04-09 05:39:55.953953	t	t
706	55	29	2017-03-30 05:39:55.953982	t	t
707	55	22	2017-03-26 05:39:55.954009	f	t
708	55	29	2017-04-08 05:39:55.954037	f	t
709	55	14	2017-03-22 05:39:55.954064	f	t
710	55	25	2017-03-27 05:39:55.954093	f	t
711	55	8	2017-03-22 05:39:55.95412	f	t
712	55	20	2017-03-26 05:39:55.954147	f	t
713	55	17	2017-04-07 05:39:55.954175	f	t
714	56	29	2017-04-03 05:39:55.954204	t	t
715	56	28	2017-04-10 05:39:55.954232	t	t
716	56	25	2017-03-28 05:39:55.95426	t	t
717	56	17	2017-03-18 05:39:55.954288	t	t
718	56	34	2017-03-24 05:39:55.954316	t	t
719	56	29	2017-04-11 05:39:55.954343	t	t
720	56	37	2017-03-28 05:39:55.954371	t	t
721	56	12	2017-04-01 05:39:55.954398	t	t
722	56	9	2017-03-25 05:39:55.954427	t	t
723	56	22	2017-03-28 05:39:55.954456	f	t
724	56	19	2017-03-21 05:39:55.954484	f	t
725	56	19	2017-03-19 05:39:55.954511	f	t
726	56	18	2017-04-08 05:39:55.954539	f	t
727	56	30	2017-03-25 05:39:55.954566	f	t
728	56	19	2017-04-05 05:39:55.954594	f	t
729	56	11	2017-03-30 05:39:55.954622	f	t
730	56	33	2017-04-10 05:39:55.954649	f	t
731	56	38	2017-03-22 05:39:55.954676	f	t
732	56	20	2017-03-29 05:39:55.954704	f	t
733	56	37	2017-03-20 05:39:55.954732	f	t
734	56	32	2017-03-26 05:39:55.95476	f	t
735	56	24	2017-04-04 05:39:55.954788	f	t
736	56	36	2017-03-21 05:39:55.954834	f	t
737	57	11	2017-04-02 05:39:55.954862	t	t
738	57	30	2017-04-06 05:39:55.95489	t	t
739	57	34	2017-03-18 05:39:55.954918	t	t
740	57	19	2017-03-21 05:39:55.954946	t	t
741	57	19	2017-03-19 05:39:55.954973	t	t
742	57	18	2017-03-20 05:39:55.955001	t	t
743	57	29	2017-04-07 05:39:55.955028	t	t
744	57	21	2017-03-26 05:39:55.955056	t	t
745	57	23	2017-03-22 05:39:55.955084	t	t
746	57	33	2017-04-11 05:39:55.955112	t	t
747	57	25	2017-03-24 05:39:55.955139	f	t
748	57	28	2017-03-18 05:39:55.955167	f	t
749	57	10	2017-04-02 05:39:55.955196	f	t
750	57	35	2017-03-17 05:39:55.955224	f	t
751	57	9	2017-03-27 05:39:55.955252	f	t
752	57	33	2017-03-22 05:39:55.95528	f	t
753	57	11	2017-04-05 05:39:55.955307	f	t
754	58	22	2017-03-17 05:39:55.955342	t	t
755	58	18	2017-04-07 05:39:55.955371	t	t
756	58	29	2017-04-01 05:39:55.955399	t	t
757	58	20	2017-04-03 05:39:55.955427	t	t
758	58	21	2017-03-23 05:39:55.955455	t	t
759	58	18	2017-04-11 05:39:55.955483	t	t
760	58	20	2017-03-23 05:39:55.95551	t	t
761	58	26	2017-03-17 05:39:55.955538	t	t
762	58	16	2017-03-24 05:39:55.955566	t	t
763	58	10	2017-03-23 05:39:55.955594	t	t
764	58	9	2017-04-02 05:39:55.955622	f	t
765	58	17	2017-04-04 05:39:55.955649	f	t
766	58	18	2017-03-27 05:39:55.955678	f	t
767	58	11	2017-03-22 05:39:55.955706	f	t
768	58	27	2017-03-17 05:39:55.955733	f	t
769	58	17	2017-03-24 05:39:55.955761	f	t
770	58	16	2017-04-03 05:39:55.955789	f	t
771	58	30	2017-04-06 05:39:55.955817	f	t
772	58	16	2017-03-17 05:39:55.955845	f	t
773	58	22	2017-03-19 05:39:55.955873	f	t
774	58	16	2017-04-07 05:39:55.955901	f	t
775	58	23	2017-03-29 05:39:55.955929	f	t
776	58	16	2017-03-23 05:39:55.955956	f	t
777	58	35	2017-03-19 05:39:55.955984	f	t
778	58	16	2017-04-11 05:39:55.956013	f	t
779	59	8	2017-03-18 05:39:55.95604	t	t
780	59	11	2017-03-29 05:39:55.956068	t	t
781	59	19	2017-03-21 05:39:55.956095	t	t
782	59	17	2017-03-20 05:39:55.956123	t	t
783	59	14	2017-04-07 05:39:55.95615	t	t
784	59	34	2017-03-18 05:39:55.956178	f	t
785	59	12	2017-03-21 05:39:55.956207	f	t
786	59	13	2017-03-20 05:39:55.956235	f	t
787	59	25	2017-04-10 05:39:55.956263	f	t
788	60	32	2017-04-02 05:39:55.956291	t	t
789	60	28	2017-03-20 05:39:55.956319	t	t
790	60	19	2017-03-20 05:39:55.956348	t	t
791	60	8	2017-03-20 05:39:55.956375	t	t
792	60	37	2017-03-18 05:39:55.956403	t	t
793	60	9	2017-04-06 05:39:55.956431	t	t
794	60	16	2017-04-04 05:39:55.956458	t	t
795	60	28	2017-04-08 05:39:55.956485	f	t
796	60	17	2017-04-08 05:39:55.956512	f	t
797	60	24	2017-03-22 05:39:55.95654	f	t
798	60	25	2017-04-08 05:39:55.956567	f	t
799	60	19	2017-03-20 05:39:55.956595	f	t
800	60	17	2017-04-09 05:39:55.956623	f	t
801	60	33	2017-04-08 05:39:55.95665	f	t
802	60	21	2017-04-10 05:39:55.956677	f	t
803	60	17	2017-03-25 05:39:55.956705	f	t
804	60	26	2017-04-06 05:39:55.956732	f	t
805	61	30	2017-04-06 05:39:55.956759	t	t
806	61	15	2017-04-04 05:39:55.956787	t	t
807	61	28	2017-03-18 05:39:55.956814	t	t
808	61	13	2017-03-21 05:39:55.956843	t	t
809	61	19	2017-04-06 05:39:55.95687	t	t
810	61	18	2017-04-03 05:39:55.956898	t	t
811	61	36	2017-04-05 05:39:55.956925	f	t
812	62	17	2017-03-26 05:39:55.956952	t	t
813	62	37	2017-03-26 05:39:55.956979	t	t
814	62	22	2017-03-29 05:39:55.957008	t	t
815	62	13	2017-03-22 05:39:55.957035	t	t
816	62	29	2017-03-17 05:39:55.957063	t	t
817	62	28	2017-03-21 05:39:55.95709	f	t
818	62	20	2017-03-24 05:39:55.957118	f	t
819	62	23	2017-04-09 05:39:55.957146	f	t
820	62	29	2017-03-19 05:39:55.957174	f	t
821	62	12	2017-03-29 05:39:55.957201	f	t
822	62	29	2017-04-05 05:39:55.957228	f	t
823	62	27	2017-04-03 05:39:55.957256	f	t
824	62	8	2017-03-25 05:39:55.957283	f	t
825	63	10	2017-03-26 05:39:55.95731	t	t
826	63	27	2017-03-22 05:39:55.957338	t	t
827	63	8	2017-04-01 05:39:55.957365	t	t
828	63	10	2017-04-05 05:39:55.957393	t	t
829	63	24	2017-04-09 05:39:55.95742	t	t
830	63	12	2017-03-28 05:39:55.957447	t	t
831	63	33	2017-04-10 05:39:55.957474	t	t
832	63	27	2017-03-29 05:39:55.957502	t	t
833	63	8	2017-03-20 05:39:55.957529	t	t
834	63	8	2017-04-06 05:39:55.957557	t	t
835	63	23	2017-03-27 05:39:55.957584	t	t
836	63	21	2017-03-26 05:39:55.957611	f	t
837	63	20	2017-04-10 05:39:55.957638	f	t
838	63	10	2017-04-05 05:39:55.957665	f	t
839	63	20	2017-04-06 05:39:55.957692	f	t
840	63	24	2017-03-17 05:39:55.957719	f	t
841	63	8	2017-04-10 05:39:55.957746	f	t
842	63	11	2017-04-11 05:39:55.957775	f	t
843	63	34	2017-03-25 05:39:55.957803	f	t
844	63	23	2017-03-29 05:39:55.95783	f	t
845	64	22	2017-03-26 05:39:55.957858	t	t
846	64	36	2017-03-27 05:39:55.957885	t	t
847	64	8	2017-03-17 05:39:55.957913	t	t
848	65	32	2017-04-03 05:39:55.95794	t	t
849	65	24	2017-03-24 05:39:55.957968	t	t
850	65	28	2017-03-27 05:39:55.957996	t	t
851	65	29	2017-03-30 05:39:55.958024	t	t
852	65	21	2017-03-24 05:39:55.958051	t	t
853	65	29	2017-04-11 05:39:55.958078	t	t
854	65	38	2017-04-07 05:39:55.958104	t	t
855	65	27	2017-04-06 05:39:55.958131	t	t
856	65	10	2017-03-20 05:39:55.958159	t	t
857	65	29	2017-03-21 05:39:55.958186	t	t
858	65	18	2017-04-05 05:39:55.958213	f	t
859	65	19	2017-04-09 05:39:55.95824	f	t
860	65	12	2017-03-24 05:39:55.958268	f	t
861	65	36	2017-04-06 05:39:55.958295	f	t
862	65	14	2017-03-22 05:39:55.958322	f	t
863	65	25	2017-04-03 05:39:55.95835	f	t
864	65	21	2017-03-23 05:39:55.958377	f	t
865	65	18	2017-03-30 05:39:55.958404	f	t
866	65	33	2017-03-22 05:39:55.958432	f	t
867	65	22	2017-04-05 05:39:55.958459	f	t
868	66	17	2017-04-08 05:39:55.958487	t	t
869	66	33	2017-04-08 05:39:55.958515	f	t
870	66	30	2017-03-26 05:39:55.958543	f	t
871	66	9	2017-04-08 05:39:55.95857	f	t
872	66	8	2017-03-18 05:39:55.958598	f	t
873	66	20	2017-04-06 05:39:55.958625	f	t
874	66	21	2017-04-02 05:39:55.958652	f	t
875	66	19	2017-03-22 05:39:55.958679	f	t
876	66	13	2017-04-06 05:39:55.958708	f	t
877	66	11	2017-03-24 05:39:55.958735	f	t
878	66	16	2017-03-22 05:39:55.958762	f	t
879	66	15	2017-03-26 05:39:55.958789	f	t
880	66	13	2017-03-21 05:39:55.958816	f	t
881	66	11	2017-04-04 05:39:55.958845	f	t
882	66	11	2017-03-24 05:39:55.958872	f	t
883	66	38	2017-04-02 05:39:55.9589	f	t
884	66	14	2017-04-08 05:39:55.958928	f	t
885	66	27	2017-03-19 05:39:55.958957	f	t
886	66	22	2017-04-03 05:39:55.958984	f	t
887	66	17	2017-03-27 05:39:55.959012	f	t
888	66	22	2017-03-28 05:39:55.959039	f	t
889	67	38	2017-03-31 05:39:55.959066	t	t
890	67	13	2017-03-21 05:39:55.959094	t	t
891	67	28	2017-04-01 05:39:55.959122	t	t
892	67	36	2017-03-24 05:39:55.959148	t	t
893	67	11	2017-03-30 05:39:55.959176	t	t
894	67	30	2017-03-19 05:39:55.959203	t	t
895	67	20	2017-03-26 05:39:55.95923	t	t
896	67	27	2017-03-31 05:39:55.959257	t	t
897	67	15	2017-04-06 05:39:55.959285	t	t
898	67	28	2017-03-17 05:39:55.959313	f	t
899	67	18	2017-03-23 05:39:55.959349	f	t
900	67	36	2017-04-10 05:39:55.959378	f	t
901	67	17	2017-04-06 05:39:55.959405	f	t
902	67	11	2017-03-30 05:39:55.959433	f	t
903	67	29	2017-03-22 05:39:55.95946	f	t
904	68	36	2017-03-26 05:39:55.959488	t	t
905	68	36	2017-03-22 05:39:55.959515	t	t
906	68	27	2017-03-28 05:39:55.959543	t	t
907	68	37	2017-04-08 05:39:55.959571	t	t
908	68	32	2017-03-19 05:39:55.959598	t	t
909	68	35	2017-03-18 05:39:55.959626	t	t
910	68	14	2017-04-03 05:39:55.959655	t	t
911	68	30	2017-03-29 05:39:55.959683	f	t
912	68	26	2017-04-05 05:39:55.95971	f	t
913	68	30	2017-04-11 05:39:55.959738	f	t
914	68	9	2017-03-24 05:39:55.959765	f	t
915	68	30	2017-04-09 05:39:55.959792	f	t
916	69	26	2017-04-01 05:39:55.95982	t	t
917	69	35	2017-03-23 05:39:55.959848	t	t
918	69	10	2017-03-18 05:39:55.959888	t	t
919	69	20	2017-04-10 05:39:55.959918	f	t
920	70	9	2017-04-05 05:39:55.959949	t	t
921	70	36	2017-04-06 05:39:55.959979	t	t
922	70	34	2017-03-24 05:39:55.96001	t	t
923	70	36	2017-03-19 05:39:55.96004	f	t
924	70	30	2017-04-06 05:39:55.96007	f	t
925	71	36	2017-03-27 05:39:55.960101	t	t
926	71	35	2017-03-26 05:39:55.960132	t	t
927	71	25	2017-03-31 05:39:55.960162	t	t
928	71	15	2017-03-19 05:39:55.960193	t	t
929	71	11	2017-04-02 05:39:55.960223	t	t
930	71	29	2017-03-30 05:39:55.960253	t	t
931	71	37	2017-03-26 05:39:55.960283	f	t
932	71	14	2017-04-11 05:39:55.960313	f	t
933	71	17	2017-04-06 05:39:55.960343	f	t
934	71	26	2017-04-07 05:39:55.960373	f	t
935	71	19	2017-03-24 05:39:55.960402	f	t
936	71	16	2017-03-24 05:39:55.960433	f	t
937	71	22	2017-03-26 05:39:55.960463	f	t
938	71	23	2017-04-02 05:39:55.960493	f	t
939	71	25	2017-03-19 05:39:55.960523	f	t
940	71	34	2017-03-17 05:39:55.960553	f	t
941	72	14	2017-04-03 05:39:55.960584	f	t
942	72	19	2017-04-03 05:39:55.960615	f	t
943	73	26	2017-03-26 05:39:55.960645	t	t
944	73	32	2017-04-08 05:39:55.960676	t	t
945	73	14	2017-04-08 05:39:55.960706	t	t
946	73	16	2017-04-11 05:39:55.960737	f	t
947	73	25	2017-03-24 05:39:55.960766	f	t
948	73	10	2017-03-23 05:39:55.960797	f	t
949	73	20	2017-03-31 05:39:55.960827	f	t
950	73	30	2017-03-26 05:39:55.960857	f	t
951	73	37	2017-03-20 05:39:55.960894	f	t
952	74	12	2017-03-24 05:39:55.960922	t	t
953	74	25	2017-04-07 05:39:55.96095	t	t
954	74	23	2017-04-05 05:39:55.960978	t	t
955	74	38	2017-03-30 05:39:55.961005	f	t
956	74	23	2017-04-04 05:39:55.961033	f	t
957	75	19	2017-03-20 05:39:55.96106	t	t
958	75	10	2017-04-01 05:39:55.961088	t	t
959	75	26	2017-03-28 05:39:55.961116	t	t
960	75	14	2017-03-18 05:39:55.961143	f	t
961	75	25	2017-04-03 05:39:55.96117	f	t
962	75	22	2017-03-24 05:39:55.961198	f	t
963	75	26	2017-04-10 05:39:55.961225	f	t
\.


--
-- Name: clicked_statements_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('clicked_statements_uid_seq', 963, true);


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
1	3	/discuss/elektroautos	2017-04-11 05:39:55.903016
\.


--
-- Name: history_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('history_uid_seq', 1, true);


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
19	15	11	t	2017-04-11 05:39:54.063376
20	17	11	f	2017-04-11 05:39:54.063376
21	18	11	t	2017-04-11 05:39:54.063376
22	23	11	t	2017-04-11 05:39:54.063376
23	24	11	t	2017-04-11 05:39:54.063376
24	21	12	f	2017-04-11 05:39:54.063376
25	22	12	t	2017-04-11 05:39:54.063376
26	19	12	f	2017-04-11 05:39:54.063376
27	35	12	t	2017-04-11 05:39:54.063376
28	25	12	f	2017-04-11 05:39:54.063376
29	26	12	f	2017-04-11 05:39:54.063376
30	27	12	f	2017-04-11 05:39:54.063376
31	28	13	f	2017-04-11 05:39:54.063376
32	29	13	f	2017-04-11 05:39:54.063376
33	34	13	f	2017-04-11 05:39:54.063376
34	20	18	t	2017-04-11 05:39:54.063376
35	36	18	t	2017-04-11 05:39:54.063376
36	37	18	t	2017-04-11 05:39:54.063376
\.


--
-- Name: last_reviewers_delete_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('last_reviewers_delete_uid_seq', 36, true);


--
-- Data for Name: last_reviewers_duplicates; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY last_reviewers_duplicates (uid, reviewer_uid, review_uid, is_okay, "timestamp") FROM stdin;
1	13	1	t	2017-03-15 17:08:24.407874
2	14	2	t	2017-03-15 17:08:24.407874
3	15	2	t	2017-03-15 17:08:24.407874
4	13	4	t	2017-04-11 05:39:54.065259
5	14	5	t	2017-04-11 05:39:54.065259
6	15	5	t	2017-04-11 05:39:54.065259
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
-- Data for Name: last_reviewers_optimization; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY last_reviewers_optimization (uid, reviewer_uid, review_uid, is_okay, "timestamp") FROM stdin;
1	30	1	t	2017-03-15 17:08:24.416218
2	32	1	t	2017-03-15 17:08:24.416218
3	33	1	t	2017-03-15 17:08:24.416218
4	13	2	f	2017-03-15 17:08:24.416218
5	14	2	f	2017-03-15 17:08:24.416218
6	16	2	f	2017-03-15 17:08:24.416218
7	30	7	t	2017-04-11 05:39:54.069244
8	32	7	t	2017-04-11 05:39:54.069244
9	33	7	t	2017-04-11 05:39:54.069244
10	13	8	f	2017-04-11 05:39:54.069244
11	14	8	f	2017-04-11 05:39:54.069244
12	16	8	f	2017-04-11 05:39:54.069244
\.


--
-- Name: last_reviewers_optimization_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('last_reviewers_optimization_uid_seq', 12, true);


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
32	24	1	2017-04-09 05:39:56.454939
33	24	2	2017-04-10 05:39:56.454939
34	24	3	2017-04-11 05:39:56.454939
35	26	1	2017-04-09 05:39:56.454939
36	26	2	2017-04-10 05:39:56.454939
37	26	3	2017-04-11 05:39:56.454939
38	23	1	2017-04-09 05:39:56.454939
39	23	2	2017-04-10 05:39:56.454939
40	23	3	2017-04-11 05:39:56.454939
41	35	1	2017-04-09 05:39:56.454939
42	35	2	2017-04-10 05:39:56.454939
43	35	3	2017-04-11 05:39:56.454939
44	2	1	2017-04-09 05:39:56.454939
45	2	2	2017-04-10 05:39:56.454939
46	2	3	2017-04-11 05:39:56.454939
47	2	8	2017-04-11 05:39:56.454939
48	4	3	2017-04-09 05:39:56.454939
49	4	4	2017-04-09 05:39:56.454939
50	4	5	2017-04-10 05:39:56.454939
51	4	6	2017-04-10 05:39:56.454939
52	4	9	2017-04-11 05:39:56.454939
53	4	8	2017-04-11 05:39:56.454939
54	3	4	2017-04-09 05:39:56.454939
55	3	5	2017-04-09 05:39:56.454939
56	3	6	2017-04-10 05:39:56.454939
57	3	9	2017-04-10 05:39:56.454939
58	3	7	2017-04-11 05:39:56.454939
59	3	10	2017-04-11 05:39:56.454939
60	3	8	2017-04-11 05:39:56.454939
61	3	11	2017-04-11 05:39:56.454939
62	3	12	2017-04-11 05:39:56.454939
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
11	19	20	\N	2017-04-11 05:39:54.050437	t	2	f
12	20	23	\N	2017-04-11 05:39:54.050437	t	1	f
13	21	\N	28	2017-04-11 05:39:54.050437	t	1	f
14	22	\N	23	2017-04-11 05:39:54.050437	f	1	f
15	23	\N	6	2017-04-11 05:39:54.050437	f	1	f
16	24	\N	23	2017-04-11 05:39:54.050437	f	1	f
17	25	23	\N	2017-04-11 05:39:54.050437	f	1	f
18	26	17	\N	2017-04-11 05:39:54.050437	f	2	f
19	27	17	\N	2017-04-11 05:39:54.050437	f	2	f
20	28	1	\N	2017-04-11 05:39:54.050437	t	1	f
\.


--
-- Name: review_deletes_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('review_deletes_uid_seq', 20, true);


--
-- Data for Name: review_duplicates; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY review_duplicates (uid, detector_uid, duplicate_statement_uid, original_statement_uid, "timestamp", is_executed, is_revoked) FROM stdin;
1	29	6	1	2017-03-15 17:08:24.397375	f	f
2	30	4	1	2017-03-15 17:08:24.397375	t	f
3	30	22	7	2017-03-15 17:08:24.397375	f	f
4	29	6	1	2017-04-11 05:39:54.060174	f	f
5	30	4	1	2017-04-11 05:39:54.060174	t	f
6	30	22	7	2017-04-11 05:39:54.060174	f	f
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
1	4	\N	2	2017-03-15 17:08:24.380276	f	f
2	4	\N	2	2017-04-11 05:39:54.053278	f	f
\.


--
-- Name: review_edits_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('review_edits_uid_seq', 2, true);


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
7	13	9	\N	2017-04-11 05:39:54.057669	t	f
8	14	\N	15	2017-04-11 05:39:54.057669	t	f
9	15	\N	14	2017-04-11 05:39:54.057669	f	f
10	17	13	\N	2017-04-11 05:39:54.057669	f	f
11	18	20	\N	2017-04-11 05:39:54.057669	f	f
12	16	\N	12	2017-04-11 05:39:54.057669	f	f
\.


--
-- Name: review_optimizations_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('review_optimizations_uid_seq', 12, true);


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
1065	1	30
1066	1	26
1067	1	30
1068	1	10
1069	1	8
1070	1	27
1071	1	25
1072	1	16
1073	1	28
1074	1	11
1075	1	38
1076	1	22
1077	1	35
1078	1	17
1079	1	12
1080	1	36
1081	2	32
1082	2	30
1083	2	16
1084	2	26
1085	2	29
1086	2	21
1087	2	35
1088	2	12
1089	2	22
1090	2	37
1091	2	18
1092	2	30
1093	2	20
1094	2	9
1095	2	24
1096	2	23
1097	2	14
1098	2	19
1099	2	36
1100	2	15
1101	2	11
1102	2	34
1103	3	38
1104	3	24
1105	3	17
1106	3	12
1107	3	14
1108	3	36
1109	3	16
1110	3	18
1111	3	35
1112	3	9
1113	3	23
1114	3	19
1115	3	37
1116	3	15
1117	3	22
1118	3	28
1119	3	8
1120	3	25
1121	3	32
1122	3	29
1123	3	26
1124	3	30
1125	3	11
1126	3	34
1127	3	20
1128	3	30
1129	4	13
1130	4	25
1131	4	37
1132	4	28
1133	4	36
1134	4	15
1135	4	9
1136	4	16
1137	4	27
1138	4	23
1139	4	10
1140	4	8
1141	4	22
1142	4	11
1143	4	12
1144	4	14
1145	4	26
1146	4	20
1147	4	35
1148	4	17
1149	4	30
1150	4	32
1151	4	24
1152	4	19
1153	4	29
1154	4	33
1155	5	33
1156	5	8
1157	5	27
1158	5	34
1159	5	29
1160	5	38
1161	5	35
1162	5	28
1163	5	15
1164	5	22
1165	5	26
1166	5	36
1167	5	37
1168	5	13
1169	5	32
1170	5	14
1171	5	10
1172	8	10
1173	8	35
1174	8	27
1175	8	16
1176	8	19
1177	8	22
1178	8	24
1179	8	8
1180	8	28
1181	8	12
1182	8	36
1183	8	20
1184	8	21
1185	8	18
1186	8	30
1187	8	34
1188	8	29
1189	8	23
1190	8	14
1191	8	25
1192	8	9
1193	8	30
1194	8	15
1195	8	13
1196	8	26
1197	8	37
1198	8	11
1199	8	17
1200	8	33
1201	10	10
1202	10	19
1203	10	8
1204	10	30
1205	10	22
1206	10	21
1207	10	17
1208	10	29
1209	10	11
1210	10	32
1211	10	35
1212	10	36
1213	10	30
1214	10	26
1215	10	27
1216	10	15
1217	10	37
1218	11	32
1219	11	11
1220	11	15
1221	11	27
1222	11	36
1223	11	16
1224	11	17
1225	11	20
1226	11	19
1227	11	12
1228	11	35
1229	11	30
1230	11	10
1231	11	24
1232	11	33
1233	11	25
1234	11	22
1235	12	12
1236	12	17
1237	12	30
1238	12	37
1239	12	9
1240	12	36
1241	12	23
1242	12	28
1243	12	19
1244	12	20
1245	12	11
1246	12	30
1247	12	38
1248	12	25
1249	12	29
1250	12	26
1251	12	27
1252	12	34
1253	12	14
1254	12	13
1255	12	21
1256	12	10
1257	12	8
1258	15	17
1259	15	9
1260	15	16
1261	15	28
1262	15	30
1263	16	34
1264	16	12
1265	16	8
1266	16	15
1267	16	36
1268	16	14
1269	16	22
1270	16	26
1271	16	37
1272	16	30
1273	16	11
1274	16	33
1275	16	19
1276	16	9
1277	16	27
1278	16	32
1279	16	29
1280	16	10
1281	16	24
1282	16	25
1283	16	21
1284	17	13
1285	17	20
1286	17	12
1287	17	24
1288	17	33
1289	19	25
1290	19	14
1291	19	32
1292	19	33
1293	19	28
1294	20	32
1295	20	34
1296	20	38
1297	20	12
1298	20	18
1299	20	25
1300	20	22
1301	20	9
1302	20	33
1303	20	23
1304	20	37
1305	20	11
1306	20	10
1307	20	29
1308	20	14
1309	20	26
1310	20	30
1311	20	36
1312	20	28
1313	21	12
1314	21	27
1315	21	34
1316	21	10
1317	21	19
1318	21	36
1319	21	16
1320	21	17
1321	21	30
1322	21	28
1323	21	15
1324	21	32
1325	21	30
1326	21	29
1327	21	22
1328	21	26
1329	21	23
1330	21	20
1331	21	11
1332	21	18
1333	21	21
1334	21	25
1335	21	24
1336	21	14
1337	21	35
1338	23	8
1339	23	27
1340	23	30
1341	23	20
1342	23	36
1343	23	15
1344	23	14
1345	23	32
1346	23	28
1347	23	11
1348	23	25
1349	23	29
1350	23	23
1351	23	18
1352	23	19
1353	23	37
1354	23	26
1355	23	9
1356	23	16
1357	24	15
1358	24	27
1359	24	29
1360	24	18
1361	24	32
1362	24	14
1363	24	11
1364	24	25
1365	26	19
1366	26	33
1367	26	18
1368	26	30
1369	27	9
1370	27	16
1371	27	22
1372	27	18
1373	27	15
1374	27	37
1375	27	34
1376	27	25
1377	27	11
1378	27	30
1379	28	11
1380	28	34
1381	28	8
1382	28	33
1383	28	26
1384	28	35
1385	28	22
1386	28	24
1387	28	38
1388	28	13
1389	28	21
1390	29	32
1391	29	19
1392	29	26
1393	29	25
1394	29	21
1395	30	15
1396	30	32
1397	30	30
1398	30	34
1399	32	15
1400	32	25
1401	32	35
1402	32	24
1403	32	30
1404	32	9
1405	32	12
1406	32	18
1407	32	28
1408	32	36
1409	32	13
1410	32	11
1411	32	20
1412	32	19
1413	32	10
1414	32	33
1415	34	10
1416	34	26
1417	34	35
1418	34	11
1419	34	16
1420	34	34
1421	34	14
1422	34	18
1423	34	22
1424	34	37
1425	34	21
1426	34	25
1427	34	12
1428	34	30
1429	34	23
1430	35	11
1431	35	22
1432	35	12
1433	35	15
1434	35	29
1435	35	30
1436	35	9
1437	35	27
1438	35	23
1439	35	37
1440	35	16
1441	35	34
1442	35	33
1443	35	28
1444	35	38
1445	35	30
1446	35	32
1447	35	8
1448	36	21
1449	36	36
1450	36	33
1451	36	37
1452	36	30
1453	36	26
1454	36	14
1455	36	18
1456	36	10
1457	36	15
1458	36	38
1459	36	28
1460	36	27
1461	36	35
1462	36	34
1463	36	22
1464	36	24
1465	36	20
1466	36	32
1467	36	19
1468	39	9
1469	39	20
1470	39	38
1471	39	36
1472	39	10
1473	39	22
1474	39	32
1475	39	14
1476	39	26
1477	39	16
1478	39	21
1479	39	27
1480	39	25
1481	39	8
1482	39	35
1483	39	29
1484	39	30
1485	39	28
1486	39	12
1487	39	19
1488	39	23
1489	40	19
1490	40	30
1491	40	35
1492	40	23
1493	40	26
1494	40	11
1495	40	22
1496	40	14
1497	40	24
1498	40	25
1499	40	15
1500	40	30
1501	40	18
1502	40	13
1503	40	29
1504	40	10
1505	40	17
1506	40	37
1507	40	33
1508	40	32
1509	41	11
1510	41	34
1511	41	18
1512	41	9
1513	41	30
1514	41	13
1515	41	20
1516	41	37
1517	41	10
1518	41	12
1519	41	27
1520	42	28
1521	42	34
1522	42	27
1523	42	24
1524	42	15
1525	42	12
1526	42	35
1527	42	36
1528	42	20
1529	42	18
1530	42	22
1531	42	26
1532	42	30
1533	42	9
1534	42	25
1535	42	38
1536	42	30
1537	42	14
1538	42	17
1539	42	33
1540	42	29
1541	44	29
1542	44	34
1543	44	26
1544	44	27
1545	44	15
1546	44	18
1547	44	19
1548	44	38
1549	44	10
1550	44	37
1551	44	25
1552	44	30
1553	44	17
1554	44	8
1555	44	30
1556	44	21
1557	44	9
1558	44	11
1559	44	33
1560	44	12
1561	44	22
1562	44	35
1563	44	32
1564	46	38
1565	46	33
1566	46	30
1567	46	13
1568	46	29
1569	46	30
1570	46	34
1571	46	27
1572	46	32
1573	46	19
1574	46	17
1575	46	15
1576	46	28
1577	46	18
1578	46	9
1579	46	36
1580	46	21
1581	46	37
1582	47	18
1583	47	11
1584	47	10
1585	47	17
1586	47	8
1587	47	29
1588	47	25
1589	47	16
1590	47	19
1591	47	9
1592	47	22
1593	47	20
1594	49	19
1595	49	33
1596	49	36
1597	49	25
1598	49	15
1599	49	32
1600	49	9
1601	49	30
1602	49	18
1603	49	16
1604	49	17
1605	49	22
1606	49	20
1607	49	21
1608	49	14
1609	49	34
1610	49	24
1611	49	27
1612	50	14
1613	50	24
1614	50	11
1615	50	9
1616	50	33
1617	50	22
1618	50	10
1619	50	30
1620	50	19
1621	50	36
1622	50	18
1623	50	16
1624	50	28
1625	50	25
1626	50	37
1627	50	13
1628	50	26
1629	50	23
1630	50	34
1631	50	32
1632	50	38
1633	50	20
1634	50	30
1635	50	15
1636	50	29
1637	50	8
1638	51	26
1639	51	10
1640	51	29
1641	51	25
1642	51	22
1643	51	12
1644	51	36
1645	51	27
1646	51	33
1647	51	35
1648	51	21
1649	51	28
1650	51	15
1651	51	38
1652	51	32
1653	51	13
1654	51	24
1655	51	37
1656	54	15
1657	54	18
1658	54	33
1659	54	21
1660	54	30
1661	54	24
1662	54	37
1663	54	16
1664	54	13
1665	54	14
1666	54	34
1667	54	36
1668	54	38
1669	54	8
1670	55	22
1671	55	23
1672	55	34
1673	55	37
1674	55	24
1675	55	28
1676	55	20
1677	55	16
1678	55	35
1679	56	37
1680	56	22
1681	56	32
1682	56	34
1683	56	12
1684	56	18
1685	57	30
1686	57	24
1687	57	12
1688	57	30
1689	57	38
1690	57	25
1691	57	20
1692	58	10
1693	58	36
1694	58	11
1695	58	27
1696	58	24
1697	58	30
1698	58	26
1699	58	30
1700	58	32
1701	58	21
1702	58	17
1703	59	28
1704	59	11
1705	59	35
1706	59	25
1707	59	29
1708	59	21
1709	59	18
1710	59	27
1711	59	37
1712	59	13
1713	59	14
1714	59	34
1715	59	19
1716	59	32
1717	59	23
1718	59	15
1719	59	8
1720	59	36
1721	59	30
1722	59	12
1723	59	24
1724	59	17
1725	59	20
1726	59	38
1727	59	16
1728	60	16
1729	60	35
1730	60	28
1731	60	10
1732	60	23
1733	60	22
1734	60	12
1735	60	15
1736	60	11
1737	60	19
1738	60	30
1739	60	29
1740	60	36
1741	60	32
1742	60	33
1743	60	34
1744	61	8
1745	61	19
1746	61	32
1747	61	27
1748	61	20
1749	62	28
1750	62	22
1751	62	16
1752	62	17
1753	62	26
1754	62	19
1755	62	15
1756	62	33
1757	62	21
1758	62	11
1759	62	37
1760	62	34
1761	62	27
1762	62	12
1763	62	35
1764	62	25
1765	62	32
1766	62	20
1767	62	24
1768	63	14
1769	63	9
1770	63	32
1771	63	17
1772	63	37
1773	63	16
1774	63	21
1775	63	34
1776	63	25
1777	63	29
1778	64	30
1779	64	22
1780	64	8
1781	64	25
1782	64	16
1783	64	26
1784	64	38
1785	64	18
1786	64	30
1787	64	15
1788	64	14
1789	64	21
1790	64	13
1791	64	36
1792	64	34
1793	64	19
1794	64	33
1795	64	28
1796	64	12
1797	64	17
1798	6	19
1799	6	32
1800	6	18
1801	6	24
1802	6	14
1803	6	29
1804	6	35
1805	6	34
1806	6	30
1807	6	8
1808	6	20
1809	6	17
1810	6	37
1811	6	23
1812	6	27
1813	6	25
1814	6	22
1815	6	12
1816	6	10
1817	6	11
1818	6	26
1819	6	38
1820	6	9
1821	6	16
1822	6	21
1823	6	15
1824	7	32
1825	7	18
1826	7	21
1827	7	38
1828	7	25
1829	7	8
1830	7	24
1831	7	22
1832	7	27
1833	7	30
1834	7	12
1835	7	11
1836	7	33
1837	7	16
1838	7	23
1839	7	14
1840	7	36
1841	7	26
1842	7	30
1843	7	13
1844	7	19
1845	7	17
1846	7	34
1847	9	23
1848	9	19
1849	9	33
1850	9	28
1851	9	24
1852	9	14
1853	9	12
1854	9	34
1855	9	26
1856	9	20
1857	9	10
1858	9	17
1859	9	22
1860	9	27
1861	9	30
1862	9	11
1863	9	15
1864	9	16
1865	9	37
1866	9	13
1867	9	38
1868	9	30
1869	13	11
1870	13	23
1871	13	37
1872	13	25
1873	13	32
1874	13	24
1875	13	30
1876	13	38
1877	13	12
1878	13	20
1879	13	13
1880	13	10
1881	13	15
1882	13	21
1883	13	22
1884	13	17
1885	13	33
1886	13	14
1887	13	26
1888	13	28
1889	13	8
1890	13	19
1891	13	16
1892	13	30
1893	13	18
1894	13	36
1895	14	15
1896	14	20
1897	14	32
1898	14	14
1899	14	28
1900	14	9
1901	14	30
1902	14	11
1903	14	38
1904	14	13
1905	14	33
1906	14	17
1907	14	22
1908	14	35
1909	14	34
1910	14	26
1911	18	17
1912	18	25
1913	18	19
1914	18	18
1915	18	16
1916	18	14
1917	18	30
1918	18	26
1919	18	15
1920	18	8
1921	18	32
1922	18	34
1923	18	11
1924	18	27
1925	18	33
1926	18	24
1927	18	20
1928	18	10
1929	18	35
1930	18	13
1931	18	23
1932	18	28
1933	18	21
1934	18	30
1935	18	36
1936	22	30
1937	22	18
1938	22	16
1939	22	25
1940	22	22
1941	22	30
1942	22	35
1943	22	17
1944	22	9
1945	22	26
1946	22	37
1947	22	38
1948	22	19
1949	22	15
1950	22	13
1951	22	32
1952	25	38
1953	25	12
1954	25	28
1955	25	35
1956	25	36
1957	25	17
1958	25	26
1959	25	8
1960	25	27
1961	25	21
1962	25	10
1963	25	14
1964	25	25
1965	25	9
1966	25	34
1967	25	22
1968	25	18
1969	25	30
1970	25	29
1971	25	24
1972	25	19
1973	25	15
1974	25	33
1975	25	32
1976	25	37
1977	25	30
1978	25	23
1979	25	11
1980	25	13
1981	31	22
1982	31	30
1983	31	32
1984	31	38
1985	31	23
1986	31	21
1987	31	29
1988	31	9
1989	31	15
1990	31	26
1991	31	8
1992	33	24
1993	33	18
1994	33	32
1995	33	29
1996	33	25
1997	33	30
1998	33	35
1999	33	17
2000	33	20
2001	33	23
2002	33	36
2003	33	15
2004	37	33
2005	37	28
2006	37	8
2007	37	13
2008	37	19
2009	37	18
2010	37	20
2011	37	38
2012	37	24
2013	37	36
2014	37	29
2015	37	12
2016	37	27
2017	37	16
2018	37	10
2019	37	15
2020	37	37
2021	37	32
2022	37	30
2023	37	25
2024	37	23
2025	37	30
2026	37	17
2027	38	38
2028	38	30
2029	38	23
2030	38	34
2031	38	30
2032	38	10
2033	38	13
2034	38	21
2035	38	18
2036	38	16
2037	38	35
2038	38	9
2039	38	36
2040	38	29
2041	38	33
2042	38	26
2043	38	20
2044	38	11
2045	38	37
2046	38	32
2047	38	27
2048	38	24
2049	38	22
2050	43	38
2051	43	34
2052	43	37
2053	43	8
2054	43	9
2055	43	22
2056	43	35
2057	43	30
2058	43	13
2059	43	27
2060	43	11
2061	43	17
2062	43	14
2063	43	25
2064	43	33
2065	43	19
2066	43	16
2067	43	23
2068	43	32
2069	43	12
2070	43	30
2071	43	18
2072	43	10
2073	43	26
2074	43	24
2075	43	15
2076	43	28
2077	43	36
2078	45	25
2079	45	19
2080	45	37
2081	45	14
2082	45	17
2083	45	20
2084	45	8
2085	45	24
2086	45	28
2087	45	23
2088	45	29
2089	45	11
2090	45	18
2091	45	22
2092	45	13
2093	45	30
2094	45	32
2095	48	32
2096	48	21
2097	48	17
2098	48	18
2099	48	28
2100	48	15
2101	48	24
2102	48	22
2103	48	13
2104	48	23
2105	52	16
2106	52	38
2107	52	10
2108	52	18
2109	52	32
2110	52	23
2111	52	21
2112	52	30
2113	52	27
2114	52	9
2115	52	15
2116	52	28
2117	52	26
2118	52	34
2119	52	8
2120	52	12
2121	52	24
2122	52	20
2123	52	25
2124	52	33
2125	52	17
2126	52	35
2127	52	19
2128	53	33
2129	53	34
2130	53	30
2131	53	27
2132	53	22
2133	53	17
2134	53	9
2135	53	32
2136	53	13
2137	53	8
2138	53	10
2139	53	26
2140	53	29
2141	53	11
2142	53	36
\.


--
-- Name: seen_arguments_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('seen_arguments_uid_seq', 2142, true);


--
-- Data for Name: seen_statements; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY seen_statements (uid, statement_uid, user_uid) FROM stdin;
1356	1	13
1357	1	20
1358	1	24
1359	1	27
1360	1	18
1361	1	26
1362	2	35
1363	2	15
1364	2	30
1365	2	19
1366	2	8
1367	2	33
1368	2	20
1369	2	11
1370	2	30
1371	2	25
1372	2	26
1373	2	22
1374	2	13
1375	2	18
1376	2	38
1377	2	12
1378	2	36
1379	2	37
1380	2	23
1381	2	29
1382	2	34
1383	2	16
1384	2	21
1385	2	32
1386	2	28
1387	2	9
1388	2	24
1389	2	14
1390	3	14
1391	3	21
1392	3	9
1393	3	10
1394	3	37
1395	3	36
1396	4	38
1397	4	24
1398	4	23
1399	4	21
1400	4	11
1401	4	14
1402	4	37
1403	4	35
1404	4	10
1405	4	28
1406	4	12
1407	4	27
1408	4	29
1409	5	13
1410	5	25
1411	5	9
1412	5	32
1413	5	21
1414	5	16
1415	5	30
1416	5	8
1417	5	22
1418	5	38
1419	5	29
1420	5	12
1421	5	33
1422	5	10
1423	5	24
1424	5	15
1425	5	26
1426	5	23
1427	5	19
1428	5	36
1429	5	20
1430	6	13
1431	6	14
1432	6	17
1433	6	28
1434	6	35
1435	6	21
1436	6	8
1437	6	16
1438	6	30
1439	6	37
1440	6	29
1441	6	32
1442	6	38
1443	6	12
1444	6	34
1445	6	36
1446	6	26
1447	6	23
1448	6	25
1449	6	30
1450	7	34
1451	7	23
1452	7	17
1453	7	9
1454	7	21
1455	7	35
1456	7	30
1457	7	18
1458	7	8
1459	7	11
1460	7	20
1461	7	13
1462	7	33
1463	7	30
1464	7	27
1465	7	29
1466	7	36
1467	7	32
1468	7	14
1469	8	18
1470	8	19
1471	8	30
1472	8	26
1473	8	8
1474	8	25
1475	8	24
1476	8	21
1477	8	11
1478	8	22
1479	8	30
1480	8	20
1481	8	14
1482	8	15
1483	9	33
1484	9	34
1485	9	21
1486	9	17
1487	9	23
1488	9	25
1489	9	11
1490	9	10
1491	9	15
1492	9	8
1493	9	38
1494	9	16
1495	9	18
1496	9	35
1497	9	32
1498	9	36
1499	9	13
1500	9	30
1501	9	30
1502	10	36
1503	10	33
1504	10	20
1505	10	22
1506	10	12
1507	10	30
1508	10	30
1509	10	13
1510	10	28
1511	10	37
1512	10	10
1513	10	9
1514	10	32
1515	10	21
1516	10	17
1517	10	26
1518	10	24
1519	10	23
1520	10	29
1521	10	16
1522	10	35
1523	10	38
1524	10	8
1525	10	18
1526	10	34
1527	10	14
1528	10	15
1529	10	27
1530	10	19
1531	11	12
1532	11	15
1533	11	24
1534	11	37
1535	11	21
1536	12	36
1537	12	25
1538	12	23
1539	12	27
1540	12	28
1541	12	30
1542	12	26
1543	12	11
1544	12	22
1545	12	9
1546	12	24
1547	12	8
1548	12	18
1549	12	21
1550	12	15
1551	12	12
1552	12	14
1553	12	29
1554	13	35
1555	13	28
1556	13	18
1557	13	11
1558	13	26
1559	13	25
1560	13	33
1561	13	10
1562	13	23
1563	13	16
1564	13	8
1565	13	9
1566	14	30
1567	14	15
1568	14	30
1569	14	25
1570	14	28
1571	14	38
1572	14	17
1573	14	29
1574	14	27
1575	14	19
1576	15	35
1577	15	30
1578	15	10
1579	15	25
1580	15	23
1581	15	36
1582	15	14
1583	15	22
1584	16	15
1585	16	13
1586	16	28
1587	16	12
1588	16	10
1589	16	18
1590	16	37
1591	16	34
1592	16	32
1593	16	9
1594	16	22
1595	16	17
1596	16	33
1597	16	27
1598	16	19
1599	16	26
1600	17	10
1601	17	27
1602	17	11
1603	17	37
1604	17	14
1605	17	8
1606	17	30
1607	17	33
1608	17	20
1609	17	29
1610	17	16
1611	17	34
1612	17	25
1613	17	19
1614	17	17
1615	17	36
1616	17	12
1617	17	15
1618	17	22
1619	17	21
1620	17	18
1621	18	11
1622	18	30
1623	18	16
1624	18	18
1625	18	20
1626	18	12
1627	18	29
1628	18	26
1629	18	38
1630	18	30
1631	18	28
1632	18	15
1633	18	17
1634	19	23
1635	19	24
1636	19	33
1637	19	9
1638	19	28
1639	19	38
1640	19	32
1641	19	15
1642	19	30
1643	19	22
1644	19	29
1645	19	13
1646	19	8
1647	20	26
1648	20	11
1649	20	8
1650	20	20
1651	20	14
1652	20	34
1653	20	37
1654	20	28
1655	20	18
1656	20	21
1657	20	25
1658	20	30
1659	20	9
1660	20	36
1661	20	30
1662	20	24
1663	20	17
1664	20	27
1665	21	13
1666	21	26
1667	21	28
1668	21	29
1669	21	24
1670	21	15
1671	21	30
1672	21	23
1673	21	18
1674	21	8
1675	21	20
1676	21	10
1677	22	38
1678	22	29
1679	22	28
1680	22	22
1681	22	25
1682	23	20
1683	23	30
1684	23	28
1685	23	15
1686	24	22
1687	24	24
1688	24	26
1689	24	30
1690	24	30
1691	24	36
1692	24	23
1693	24	34
1694	24	38
1695	24	11
1696	24	37
1697	24	14
1698	24	21
1699	24	8
1700	24	9
1701	24	29
1702	24	33
1703	24	25
1704	24	12
1705	24	35
1706	24	17
1707	24	13
1708	24	16
1709	24	20
1710	24	27
1711	24	32
1712	25	38
1713	25	23
1714	25	22
1715	25	12
1716	25	20
1717	25	30
1718	25	19
1719	26	36
1720	26	29
1721	26	17
1722	26	15
1723	26	26
1724	26	12
1725	26	19
1726	26	28
1727	26	34
1728	27	15
1729	27	35
1730	27	36
1731	27	19
1732	27	17
1733	27	14
1734	27	18
1735	27	37
1736	27	30
1737	27	23
1738	27	32
1739	27	24
1740	27	21
1741	27	38
1742	27	20
1743	27	33
1744	27	26
1745	27	13
1746	27	12
1747	27	9
1748	27	22
1749	27	30
1750	27	28
1751	27	11
1752	27	25
1753	27	10
1754	27	34
1755	27	16
1756	27	8
1757	28	23
1758	28	32
1759	28	10
1760	28	24
1761	28	13
1762	28	38
1763	28	28
1764	28	27
1765	28	8
1766	28	33
1767	28	18
1768	28	9
1769	28	36
1770	28	30
1771	28	35
1772	28	16
1773	28	29
1774	28	17
1775	29	29
1776	29	21
1777	29	9
1778	29	22
1779	29	8
1780	29	11
1781	29	35
1782	29	23
1783	29	12
1784	29	19
1785	29	38
1786	29	30
1787	29	18
1788	29	20
1789	29	10
1790	29	37
1791	29	16
1792	29	14
1793	29	15
1794	29	26
1795	30	9
1796	30	27
1797	30	28
1798	30	38
1799	30	37
1800	30	10
1801	30	22
1802	30	21
1803	30	16
1804	30	36
1805	30	14
1806	30	30
1807	30	30
1808	31	35
1809	31	30
1810	31	29
1811	31	26
1812	31	16
1813	31	9
1814	31	24
1815	31	36
1816	32	22
1817	32	19
1818	32	36
1819	32	20
1820	32	21
1821	32	34
1822	32	35
1823	32	26
1824	32	27
1825	32	23
1826	32	16
1827	32	10
1828	32	18
1829	32	17
1830	32	28
1831	33	34
1832	33	29
1833	33	24
1834	33	18
1835	33	32
1836	33	8
1837	33	15
1838	33	23
1839	33	30
1840	33	17
1841	33	20
1842	34	30
1843	34	15
1844	34	20
1845	34	38
1846	35	33
1847	35	36
1848	35	27
1849	35	37
1850	35	23
1851	35	28
1852	35	30
1853	35	15
1854	35	34
1855	35	10
1856	36	14
1857	36	22
1858	36	30
1859	36	29
1860	36	13
1861	36	20
1862	36	33
1863	36	37
1864	36	8
1865	36	24
1866	36	18
1867	36	19
1868	36	9
1869	36	26
1870	36	36
1871	36	23
1872	36	11
1873	36	38
1874	36	21
1875	37	19
1876	37	23
1877	37	36
1878	37	35
1879	37	26
1880	37	14
1881	37	37
1882	37	11
1883	37	12
1884	37	22
1885	37	30
1886	37	8
1887	37	25
1888	37	13
1889	37	27
1890	37	34
1891	37	16
1892	37	10
1893	37	20
1894	37	18
1895	37	28
1896	37	15
1897	38	17
1898	38	19
1899	38	10
1900	38	20
1901	38	38
1902	38	32
1903	39	29
1904	39	20
1905	39	27
1906	39	18
1907	39	13
1908	39	10
1909	39	23
1910	39	37
1911	39	11
1912	39	36
1913	39	19
1914	39	30
1915	39	30
1916	39	24
1917	39	22
1918	40	26
1919	40	10
1920	40	37
1921	40	28
1922	40	22
1923	40	33
1924	40	27
1925	40	21
1926	40	36
1927	40	34
1928	40	30
1929	40	32
1930	40	35
1931	40	25
1932	40	11
1933	40	18
1934	41	34
1935	41	24
1936	41	12
1937	41	9
1938	41	10
1939	41	14
1940	41	16
1941	41	11
1942	41	23
1943	41	27
1944	41	38
1945	41	37
1946	41	30
1947	41	18
1948	41	28
1949	41	8
1950	41	29
1951	41	26
1952	42	36
1953	42	13
1954	42	25
1955	42	11
1956	42	34
1957	42	35
1958	42	30
1959	42	8
1960	42	28
1961	42	18
1962	42	19
1963	42	10
1964	42	21
1965	42	20
1966	42	23
1967	42	33
1968	42	24
1969	42	37
1970	43	26
1971	43	28
1972	43	37
1973	43	35
1974	43	9
1975	43	30
1976	44	20
1977	44	13
1978	44	38
1979	44	12
1980	44	34
1981	44	32
1982	44	21
1983	44	29
1984	44	17
1985	44	30
1986	44	23
1987	44	11
1988	44	35
1989	44	14
1990	45	23
1991	45	32
1992	45	11
1993	45	24
1994	45	21
1995	45	10
1996	45	22
1997	45	19
1998	45	8
1999	45	25
2000	45	38
2001	45	18
2002	45	35
2003	45	34
2004	45	37
2005	46	35
2006	46	19
2007	46	15
2008	46	24
2009	46	27
2010	46	36
2011	46	8
2012	46	14
2013	46	30
2014	46	30
2015	46	26
2016	46	18
2017	46	17
2018	46	38
2019	46	22
2020	46	21
2021	46	33
2022	46	29
2023	46	10
2024	46	25
2025	46	13
2026	46	16
2027	46	12
2028	47	11
2029	47	26
2030	47	36
2031	47	8
2032	47	18
2033	47	38
2034	47	12
2035	48	35
2036	48	32
2037	48	30
2038	48	26
2039	48	9
2040	48	24
2041	48	19
2042	48	21
2043	48	13
2044	48	22
2045	48	37
2046	48	18
2047	48	10
2048	48	12
2049	48	30
2050	48	8
2051	48	28
2052	48	38
2053	48	29
2054	49	30
2055	49	29
2056	49	10
2057	49	18
2058	49	32
2059	49	33
2060	49	38
2061	49	22
2062	49	36
2063	49	37
2064	49	15
2065	49	24
2066	49	16
2067	49	11
2068	49	35
2069	49	30
2070	49	17
2071	49	21
2072	49	12
2073	50	28
2074	50	15
2075	50	23
2076	50	20
2077	50	36
2078	50	35
2079	50	17
2080	50	37
2081	50	8
2082	50	10
2083	50	38
2084	50	33
2085	50	9
2086	50	18
2087	50	16
2088	50	14
2089	50	34
2090	50	26
2091	50	27
2092	51	33
2093	51	19
2094	51	25
2095	51	37
2096	51	36
2097	51	10
2098	51	35
2099	51	9
2100	51	14
2101	51	26
2102	51	24
2103	51	21
2104	51	13
2105	51	22
2106	51	28
2107	51	17
2108	51	29
2109	51	23
2110	51	27
2111	51	20
2112	51	18
2113	51	16
2114	51	38
2115	51	32
2116	51	8
2117	51	30
2118	52	8
2119	52	13
2120	52	15
2121	52	10
2122	52	14
2123	52	34
2124	52	33
2125	52	27
2126	52	24
2127	52	9
2128	52	32
2129	52	17
2130	53	25
2131	53	35
2132	53	32
2133	53	26
2134	53	14
2135	53	28
2136	53	29
2137	53	19
2138	53	33
2139	53	15
2140	53	13
2141	53	30
2142	53	37
2143	53	27
2144	53	24
2145	53	20
2146	53	10
2147	53	36
2148	53	21
2149	53	34
2150	53	16
2151	53	22
2152	53	9
2153	53	11
2154	53	18
2155	53	12
2156	53	23
2157	53	30
2158	53	38
2159	54	25
2160	54	26
2161	54	28
2162	54	18
2163	54	11
2164	54	9
2165	55	15
2166	55	26
2167	55	23
2168	55	29
2169	55	22
2170	55	33
2171	55	14
2172	55	36
2173	55	10
2174	55	30
2175	55	18
2176	56	8
2177	56	15
2178	56	32
2179	56	19
2180	56	29
2181	56	11
2182	56	17
2183	56	25
2184	56	21
2185	56	13
2186	56	10
2187	56	37
2188	56	33
2189	56	16
2190	56	30
2191	56	36
2192	56	23
2193	56	20
2194	56	12
2195	56	27
2196	56	14
2197	56	34
2198	56	24
2199	56	38
2200	56	22
2201	56	26
2202	56	9
2203	56	18
2204	57	10
2205	57	36
2206	57	30
2207	57	9
2208	57	26
2209	57	21
2210	57	8
2211	57	29
2212	57	30
2213	57	28
2214	57	15
2215	57	16
2216	57	17
2217	57	23
2218	57	20
2219	57	19
2220	57	34
2221	57	27
2222	57	35
2223	57	32
2224	57	13
2225	57	37
2226	58	32
2227	58	28
2228	58	16
2229	58	26
2230	58	10
2231	58	24
2232	58	18
2233	58	37
2234	58	25
2235	58	33
2236	58	8
2237	58	35
2238	58	30
2239	58	19
2240	58	9
2241	58	11
2242	58	22
2243	58	30
2244	58	13
2245	58	36
2246	58	38
2247	58	21
2248	58	15
2249	58	27
2250	58	34
2251	58	29
2252	58	20
2253	59	24
2254	59	23
2255	59	15
2256	59	32
2257	59	37
2258	59	38
2259	59	19
2260	59	22
2261	59	36
2262	59	34
2263	59	33
2264	59	11
2265	60	23
2266	60	37
2267	60	8
2268	60	14
2269	60	30
2270	60	17
2271	60	10
2272	60	38
2273	60	13
2274	60	18
2275	60	16
2276	60	26
2277	60	19
2278	60	25
2279	61	17
2280	61	9
2281	61	25
2282	61	37
2283	61	27
2284	61	33
2285	61	16
2286	61	15
2287	61	38
2288	61	8
2289	62	22
2290	62	35
2291	62	15
2292	62	16
2293	62	33
2294	62	24
2295	62	29
2296	62	19
2297	62	11
2298	62	34
2299	62	30
2300	62	26
2301	63	22
2302	63	8
2303	63	30
2304	63	19
2305	63	35
2306	63	18
2307	63	10
2308	63	27
2309	63	24
2310	63	30
2311	63	9
2312	63	13
2313	63	34
2314	63	38
2315	63	20
2316	63	26
2317	63	36
2318	64	26
2319	64	13
2320	64	36
2321	64	23
2322	64	30
2323	64	14
2324	65	11
2325	65	29
2326	65	24
2327	65	19
2328	65	30
2329	65	10
2330	65	23
2331	65	27
2332	65	36
2333	65	33
2334	65	37
2335	65	30
2336	65	28
2337	65	9
2338	65	13
2339	65	38
2340	66	27
2341	66	21
2342	66	35
2343	66	14
2344	66	28
2345	66	33
2346	66	12
2347	66	19
2348	66	22
2349	66	25
2350	66	30
2351	66	10
2352	66	16
2353	66	15
2354	66	9
2355	66	34
2356	66	11
2357	66	18
2358	66	30
2359	66	32
2360	66	8
2361	66	20
2362	66	26
2363	66	13
2364	66	24
2365	66	29
2366	66	23
2367	66	17
2368	67	37
2369	67	25
2370	67	33
2371	67	18
2372	67	20
2373	67	15
2374	67	11
2375	67	8
2376	67	35
2377	67	32
2378	67	23
2379	67	30
2380	67	17
2381	67	9
2382	67	21
2383	67	36
2384	67	10
2385	67	12
2386	67	24
2387	67	19
2388	67	34
2389	67	16
2390	67	30
2391	67	38
2392	67	22
2393	67	29
2394	68	25
2395	68	16
2396	68	32
2397	68	28
2398	68	26
2399	68	29
2400	68	13
2401	68	11
2402	68	36
2403	68	17
2404	68	24
2405	68	35
2406	68	37
2407	68	19
2408	68	27
2409	69	27
2410	69	25
2411	69	12
2412	69	24
2413	69	16
2414	69	32
2415	69	29
2416	69	37
2417	69	23
2418	70	30
2419	70	36
2420	70	13
2421	70	8
2422	70	27
2423	71	30
2424	71	32
2425	71	15
2426	71	25
2427	71	12
2428	71	34
2429	71	16
2430	71	20
2431	71	26
2432	71	36
2433	71	27
2434	71	9
2435	71	10
2436	71	18
2437	71	8
2438	71	23
2439	71	38
2440	71	11
2441	71	37
2442	71	24
2443	71	17
2444	71	35
2445	71	14
2446	71	33
2447	71	19
2448	71	29
2449	71	21
2450	71	22
2451	72	22
2452	72	35
2453	72	14
2454	72	28
2455	72	26
2456	72	20
2457	72	32
2458	72	23
2459	73	22
2460	73	33
2461	73	30
2462	73	37
2463	73	12
2464	73	9
2465	73	20
2466	73	13
2467	73	19
2468	73	16
2469	73	11
2470	73	35
2471	74	23
2472	74	25
2473	74	12
2474	74	14
2475	74	28
2476	74	10
2477	74	19
2478	74	26
2479	74	13
2480	74	18
2481	75	13
2482	75	20
2483	75	22
2484	75	37
2485	75	12
2486	75	29
2487	58	3
2488	67	3
\.


--
-- Name: seen_statements_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('seen_statements_uid_seq', 2488, true);


--
-- Data for Name: settings; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY settings (author_uid, should_send_mails, should_send_notifications, should_show_public_nickname, last_topic_uid, lang_uid, keep_logged_in) FROM stdin;
1	f	t	t	1	2	f
2	f	t	t	1	2	f
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
3	f	t	t	4	2	f
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
3	Tobias	Krauthoff	Tobias	Tobias	krauthoff@cs.uni-duesseldorf.de	m	$2a$10$9P5biPvyX2xVeMcCLm82tO0XFQhmdMFwgAhPaUkCHoVL1F5kEAjIa	1	2017-04-11 05:40:05.082513	2017-03-15 17:08:24.304473	2017-03-15 17:08:24.304621		\N
\.


--
-- Name: users_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('users_uid_seq', 38, true);


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
-- Name: last_reviewers_optimization last_reviewers_optimization_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY last_reviewers_optimization
    ADD CONSTRAINT last_reviewers_optimization_pkey PRIMARY KEY (uid);


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
-- Name: review_optimizations review_optimizations_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_optimizations
    ADD CONSTRAINT review_optimizations_pkey PRIMARY KEY (uid);


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
-- Name: review_canceled review_canceled_review_optimization_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY review_canceled
    ADD CONSTRAINT review_canceled_review_optimization_uid_fkey FOREIGN KEY (review_optimization_uid) REFERENCES review_optimizations(uid);


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
-- PostgreSQL database dump complete
--

\connect news

SET default_transaction_read_only = off;

--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.2
-- Dumped by pg_dump version 9.6.2

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

-- Dumped from database version 9.6.2
-- Dumped by pg_dump version 9.6.2

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
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT SELECT ON TABLES  TO read_only_discussion;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT ALL ON TABLES  TO writer;


--
-- PostgreSQL database dump complete
--

\connect template1

SET default_transaction_read_only = off;

--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.2
-- Dumped by pg_dump version 9.6.2

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

