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
CREATE ROLE read_only_discussion;
ALTER ROLE read_only_discussion WITH NOSUPERUSER INHERIT NOCREATEROLE NOCREATEDB NOLOGIN NOREPLICATION NOBYPASSRLS;
CREATE ROLE writer;
ALTER ROLE writer WITH NOSUPERUSER INHERIT NOCREATEROLE NOCREATEDB NOLOGIN NOREPLICATION NOBYPASSRLS;


--
-- Role memberships
--

GRANT writer TO dbas GRANTED BY postgres;




--
-- Database creation
--

CREATE DATABASE beaker WITH TEMPLATE = template0 OWNER = postgres;
CREATE DATABASE discussion WITH TEMPLATE = template0 OWNER = postgres;
GRANT CONNECT ON DATABASE discussion TO read_only_discussion;
CREATE DATABASE test_discussion WITH TEMPLATE = template0 OWNER = postgres;
GRANT CONNECT ON DATABASE test_discussion TO read_only_discussion;
REVOKE CONNECT,TEMPORARY ON DATABASE template1 FROM PUBLIC;
GRANT CONNECT ON DATABASE template1 TO PUBLIC;


\connect beaker

SET default_transaction_read_only = off;

--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.5
-- Dumped by pg_dump version 9.6.5

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

-- Dumped from database version 9.6.5
-- Dumped by pg_dump version 9.6.5

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

SET search_path = news, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: news; Type: TABLE; Schema: news; Owner: dbas
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
-- Name: news_uid_seq; Type: SEQUENCE; Schema: news; Owner: dbas
--

CREATE SEQUENCE news_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE news_uid_seq OWNER TO dbas;

--
-- Name: news_uid_seq; Type: SEQUENCE OWNED BY; Schema: news; Owner: dbas
--

ALTER SEQUENCE news_uid_seq OWNED BY news.uid;


SET search_path = public, pg_catalog;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE alembic_version OWNER TO dbas;

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
-- Name: arguments_added_by_premisegroups_split; Type: TABLE; Schema: public; Owner: dbas
--

CREATE TABLE arguments_added_by_premisegroups_split (
    uid integer NOT NULL,
    review_uid integer,
    argument_uid integer,
    "timestamp" timestamp without time zone
);


ALTER TABLE arguments_added_by_premisegroups_split OWNER TO dbas;

--
-- Name: arguments_added_by_premisegroups_split_uid_seq; Type: SEQUENCE; Schema: public; Owner: dbas
--

CREATE SEQUENCE arguments_added_by_premisegroups_split_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE arguments_added_by_premisegroups_split_uid_seq OWNER TO dbas;

--
-- Name: arguments_added_by_premisegroups_split_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbas
--

ALTER SEQUENCE arguments_added_by_premisegroups_split_uid_seq OWNED BY arguments_added_by_premisegroups_split.uid;


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


SET search_path = news, pg_catalog;

--
-- Name: news uid; Type: DEFAULT; Schema: news; Owner: dbas
--

ALTER TABLE ONLY news ALTER COLUMN uid SET DEFAULT nextval('news_uid_seq'::regclass);


SET search_path = public, pg_catalog;

--
-- Name: arguments uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY arguments ALTER COLUMN uid SET DEFAULT nextval('arguments_uid_seq'::regclass);


--
-- Name: arguments_added_by_premisegroups_split uid; Type: DEFAULT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY arguments_added_by_premisegroups_split ALTER COLUMN uid SET DEFAULT nextval('arguments_added_by_premisegroups_split_uid_seq'::regclass);


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


SET search_path = news, pg_catalog;

--
-- Data for Name: news; Type: TABLE DATA; Schema: news; Owner: dbas
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
-- Name: news_uid_seq; Type: SEQUENCE SET; Schema: news; Owner: dbas
--

SELECT pg_catalog.setval('news_uid_seq', 60, true);


SET search_path = public, pg_catalog;

--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY alembic_version (version_num) FROM stdin;
2a4bc7c8ff38
\.


--
-- Data for Name: arguments; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY arguments (uid, premisesgroup_uid, conclusion_uid, argument_uid, is_supportive, author_uid, "timestamp", issue_uid, is_disabled) FROM stdin;
1	1	2	\N	f	1	2017-08-19 11:25:09.346412	2	t
2	2	2	\N	t	1	2017-08-19 11:25:09.346515	2	f
3	3	2	\N	f	1	2017-08-19 11:25:09.346596	2	f
4	4	3	\N	t	1	2017-08-19 11:25:09.346673	2	f
5	5	3	\N	f	1	2017-08-19 11:25:09.346748	2	f
8	8	4	\N	t	1	2017-08-19 11:25:09.346966	2	f
10	10	11	\N	f	1	2017-08-19 11:25:09.347116	2	f
11	11	2	\N	t	1	2017-08-19 11:25:09.347189	2	f
12	12	2	\N	t	1	2017-08-19 11:25:09.347261	2	f
15	15	5	\N	t	1	2017-08-19 11:25:09.347476	2	f
16	16	5	\N	f	1	2017-08-19 11:25:09.347548	2	f
17	17	5	\N	t	1	2017-08-19 11:25:09.347621	2	f
19	19	6	\N	t	1	2017-08-19 11:25:09.347767	2	f
20	20	6	\N	f	1	2017-08-19 11:25:09.347839	2	f
21	21	6	\N	f	1	2017-08-19 11:25:09.347911	2	f
23	23	14	\N	f	1	2017-08-19 11:25:09.34811	2	f
24	24	14	\N	t	1	2017-08-19 11:25:09.348183	2	f
26	26	14	\N	t	1	2017-08-19 11:25:09.34833	2	f
27	27	15	\N	t	1	2017-08-19 11:25:09.348403	2	f
28	27	16	\N	t	1	2017-08-19 11:25:09.348475	2	f
29	28	15	\N	t	1	2017-08-19 11:25:09.348547	2	f
30	29	15	\N	f	1	2017-08-19 11:25:09.348629	2	f
32	31	36	\N	t	3	2017-08-19 11:25:09.348773	1	f
34	33	39	\N	t	3	2017-08-19 11:25:09.348917	1	f
35	34	41	\N	t	1	2017-08-19 11:25:09.34899	1	f
36	35	36	\N	f	1	2017-08-19 11:25:09.349062	1	f
39	38	37	\N	t	1	2017-08-19 11:25:09.349279	1	f
40	39	37	\N	t	1	2017-08-19 11:25:09.349351	1	f
41	41	46	\N	f	1	2017-08-19 11:25:09.349426	1	f
42	42	37	\N	f	1	2017-08-19 11:25:09.349569	1	f
44	44	50	\N	f	1	2017-08-19 11:25:09.349715	1	f
46	45	50	\N	t	1	2017-08-19 11:25:09.349788	1	f
47	46	38	\N	t	1	2017-08-19 11:25:09.34986	1	f
49	48	38	\N	f	1	2017-08-19 11:25:09.350003	1	f
50	49	49	\N	f	1	2017-08-19 11:25:09.350077	1	f
51	51	58	\N	f	1	2017-08-19 11:25:09.350293	4	f
54	54	59	\N	t	1	2017-08-19 11:25:09.350519	4	f
55	55	59	\N	f	1	2017-08-19 11:25:09.350593	4	f
56	56	60	\N	t	1	2017-08-19 11:25:09.350665	4	f
57	57	60	\N	f	1	2017-08-19 11:25:09.350738	4	f
58	50	58	\N	t	1	2017-08-19 11:25:09.350163	4	f
59	61	67	\N	t	1	2017-08-19 11:25:09.35081	4	f
60	62	69	\N	t	1	2017-08-19 11:25:09.350884	5	f
61	63	69	\N	t	1	2017-08-19 11:25:09.350956	5	f
62	64	69	\N	f	1	2017-08-19 11:25:09.351028	5	f
63	65	70	\N	f	1	2017-08-19 11:25:09.351103	5	f
64	66	70	\N	f	1	2017-08-19 11:25:09.351176	5	f
65	67	76	\N	t	1	2017-08-19 11:25:09.351249	7	f
66	68	76	\N	f	1	2017-08-19 11:25:09.351321	7	f
67	69	76	\N	f	1	2017-08-19 11:25:09.351392	7	f
68	70	79	\N	f	1	2017-08-19 11:25:09.351464	7	f
6	6	\N	4	f	1	2017-08-19 11:25:09.346821	2	f
7	7	\N	5	f	1	2017-08-19 11:25:09.346893	2	f
9	9	\N	8	f	1	2017-08-19 11:25:09.347038	2	f
13	13	\N	12	f	1	2017-08-19 11:25:09.347333	2	f
14	14	\N	13	f	1	2017-08-19 11:25:09.347404	2	f
18	18	\N	2	f	1	2017-08-19 11:25:09.347692	2	f
22	22	\N	3	f	1	2017-08-19 11:25:09.348036	2	f
25	25	\N	11	f	1	2017-08-19 11:25:09.348255	2	f
31	30	\N	15	f	1	2017-08-19 11:25:09.348701	2	f
33	32	\N	32	f	3	2017-08-19 11:25:09.348844	1	f
37	36	\N	36	f	1	2017-08-19 11:25:09.349135	1	f
38	37	\N	36	f	1	2017-08-19 11:25:09.349207	1	f
43	43	\N	42	f	1	2017-08-19 11:25:09.34964	1	f
45	40	\N	39	f	1	2017-08-19 11:25:09.349498	1	f
48	47	\N	47	f	1	2017-08-19 11:25:09.349931	1	f
52	52	\N	58	f	1	2017-08-19 11:25:09.350373	4	f
53	53	\N	51	f	1	2017-08-19 11:25:09.350445	4	f
69	71	\N	65	f	1	2017-08-19 11:25:09.351537	7	f
\.


--
-- Data for Name: arguments_added_by_premisegroups_split; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY arguments_added_by_premisegroups_split (uid, review_uid, argument_uid, "timestamp") FROM stdin;
\.


--
-- Name: arguments_added_by_premisegroups_split_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('arguments_added_by_premisegroups_split_uid_seq', 1, false);


--
-- Name: arguments_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('arguments_uid_seq', 69, true);


--
-- Data for Name: clicked_arguments; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY clicked_arguments (uid, argument_uid, author_uid, "timestamp", is_up_vote, is_valid) FROM stdin;
861	1	13	2017-08-11 11:25:16.606147	t	t
862	1	8	2017-08-06 11:25:16.606245	f	t
863	2	18	2017-07-31 11:25:16.606285	t	t
864	2	7	2017-07-29 11:25:16.606334	t	t
865	2	35	2017-07-30 11:25:16.606377	t	t
866	2	10	2017-07-25 11:25:16.606407	t	t
867	2	9	2017-08-13 11:25:16.606438	t	t
868	2	32	2017-08-05 11:25:16.606467	t	t
869	2	28	2017-08-03 11:25:16.606496	t	t
870	2	13	2017-07-28 11:25:16.606526	t	t
871	2	26	2017-07-30 11:25:16.606556	t	t
872	2	12	2017-08-19 11:25:16.606585	t	t
873	2	29	2017-07-27 11:25:16.606615	t	t
874	2	16	2017-08-15 11:25:16.606644	t	t
875	2	29	2017-08-18 11:25:16.606674	t	t
876	2	20	2017-07-31 11:25:16.606704	t	t
877	2	23	2017-08-02 11:25:16.606734	t	t
878	2	25	2017-08-07 11:25:16.606764	t	t
879	2	27	2017-08-19 11:25:16.606794	t	t
880	2	15	2017-07-27 11:25:16.606824	t	t
881	2	36	2017-08-06 11:25:16.606853	t	t
882	2	8	2017-07-26 11:25:16.606883	t	t
883	2	31	2017-08-09 11:25:16.606912	t	t
884	2	19	2017-08-11 11:25:16.606941	t	t
885	2	11	2017-07-28 11:25:16.606971	t	t
886	2	37	2017-08-11 11:25:16.607	t	t
887	2	17	2017-08-06 11:25:16.607029	t	t
888	2	32	2017-08-04 11:25:16.607058	f	t
889	2	11	2017-08-10 11:25:16.607087	f	t
890	2	27	2017-07-30 11:25:16.607116	f	t
891	2	8	2017-08-06 11:25:16.607144	f	t
892	2	37	2017-07-31 11:25:16.607173	f	t
893	2	22	2017-08-14 11:25:16.607202	f	t
894	2	29	2017-07-26 11:25:16.607231	f	t
895	2	29	2017-08-07 11:25:16.607259	f	t
896	2	23	2017-08-08 11:25:16.607288	f	t
897	3	12	2017-08-04 11:25:16.607317	t	t
898	3	15	2017-08-18 11:25:16.607347	t	t
899	3	31	2017-07-30 11:25:16.607377	t	t
900	3	22	2017-07-27 11:25:16.607406	t	t
901	3	23	2017-08-11 11:25:16.607435	t	t
902	3	13	2017-08-19 11:25:16.607465	t	t
903	3	16	2017-08-17 11:25:16.607494	t	t
904	3	35	2017-07-28 11:25:16.607524	t	t
905	3	19	2017-08-12 11:25:16.607553	t	t
906	3	34	2017-08-09 11:25:16.607583	t	t
907	3	27	2017-08-05 11:25:16.607612	t	t
908	3	11	2017-07-29 11:25:16.607641	t	t
909	3	7	2017-08-15 11:25:16.60767	f	t
910	3	13	2017-08-04 11:25:16.607699	f	t
911	3	15	2017-08-04 11:25:16.607728	f	t
912	3	34	2017-08-09 11:25:16.607757	f	t
913	4	36	2017-08-02 11:25:16.607786	t	t
914	4	35	2017-07-30 11:25:16.607815	t	t
915	4	24	2017-08-11 11:25:16.607844	t	t
916	4	17	2017-08-04 11:25:16.607873	t	t
917	4	8	2017-07-29 11:25:16.607902	t	t
918	4	15	2017-08-01 11:25:16.607931	t	t
919	4	26	2017-08-13 11:25:16.60796	t	t
920	4	37	2017-08-16 11:25:16.607989	t	t
921	4	16	2017-08-05 11:25:16.608019	t	t
922	4	29	2017-08-07 11:25:16.608048	t	t
923	4	10	2017-07-25 11:25:16.608078	t	t
924	4	34	2017-08-17 11:25:16.608107	t	t
925	4	14	2017-08-11 11:25:16.608136	t	t
926	4	13	2017-08-17 11:25:16.608165	f	t
927	4	37	2017-08-09 11:25:16.608195	f	t
928	4	29	2017-08-02 11:25:16.608224	f	t
929	4	11	2017-08-06 11:25:16.608253	f	t
930	4	14	2017-08-05 11:25:16.608282	f	t
931	5	7	2017-08-15 11:25:16.608311	t	t
932	5	9	2017-08-15 11:25:16.608341	t	t
933	5	31	2017-08-02 11:25:16.60837	t	t
934	5	33	2017-08-19 11:25:16.608399	t	t
935	5	25	2017-08-02 11:25:16.608429	t	t
936	5	17	2017-07-30 11:25:16.608458	t	t
937	5	29	2017-08-14 11:25:16.608487	t	t
938	5	22	2017-08-18 11:25:16.608516	t	t
939	5	26	2017-07-25 11:25:16.608545	t	t
940	5	23	2017-08-14 11:25:16.608575	t	t
941	5	34	2017-07-31 11:25:16.608604	t	t
942	5	10	2017-08-09 11:25:16.608633	f	t
943	5	17	2017-07-28 11:25:16.608663	f	t
944	5	36	2017-08-11 11:25:16.608692	f	t
945	5	12	2017-08-18 11:25:16.608721	f	t
946	5	23	2017-07-30 11:25:16.60875	f	t
947	5	8	2017-07-25 11:25:16.608779	f	t
948	5	28	2017-07-30 11:25:16.608808	f	t
949	5	27	2017-08-06 11:25:16.608838	f	t
950	5	18	2017-08-16 11:25:16.608868	f	t
951	5	21	2017-08-03 11:25:16.608897	f	t
952	8	16	2017-07-28 11:25:16.608964	t	t
953	8	18	2017-07-25 11:25:16.608999	t	t
954	8	9	2017-08-16 11:25:16.60903	t	t
955	8	23	2017-08-19 11:25:16.60906	t	t
956	8	26	2017-07-27 11:25:16.60909	t	t
957	8	29	2017-08-14 11:25:16.60912	t	t
958	8	33	2017-07-31 11:25:16.60915	t	t
959	8	14	2017-07-26 11:25:16.609179	t	t
960	8	37	2017-08-15 11:25:16.609209	t	t
961	8	36	2017-07-29 11:25:16.609238	t	t
962	8	33	2017-08-19 11:25:16.609268	f	t
963	8	19	2017-08-03 11:25:16.609297	f	t
964	8	31	2017-08-06 11:25:16.609327	f	t
965	8	22	2017-07-25 11:25:16.609356	f	t
966	8	37	2017-08-17 11:25:16.609386	f	t
967	8	24	2017-08-16 11:25:16.609415	f	t
968	8	34	2017-08-09 11:25:16.609444	f	t
969	8	12	2017-08-04 11:25:16.609474	f	t
970	8	16	2017-08-04 11:25:16.609503	f	t
971	8	13	2017-08-17 11:25:16.609532	f	t
972	8	17	2017-07-26 11:25:16.609561	f	t
973	10	8	2017-07-26 11:25:16.609591	t	t
974	10	35	2017-08-19 11:25:16.60962	t	t
975	10	14	2017-08-11 11:25:16.60965	t	t
976	10	13	2017-08-11 11:25:16.609679	t	t
977	10	34	2017-08-03 11:25:16.609708	t	t
978	10	7	2017-08-01 11:25:16.609738	t	t
979	10	18	2017-08-03 11:25:16.609767	t	t
980	10	24	2017-08-19 11:25:16.609796	t	t
981	10	12	2017-08-14 11:25:16.609826	t	t
982	10	29	2017-08-05 11:25:16.609855	t	t
983	10	15	2017-08-09 11:25:16.609916	t	t
984	10	23	2017-08-12 11:25:16.609948	t	t
985	11	34	2017-08-02 11:25:16.609978	t	t
986	11	29	2017-07-25 11:25:16.610019	t	t
987	11	10	2017-08-06 11:25:16.610058	t	t
988	11	18	2017-08-02 11:25:16.610087	t	t
989	11	7	2017-08-09 11:25:16.610116	t	t
990	11	37	2017-07-30 11:25:16.610145	t	t
991	11	16	2017-08-09 11:25:16.610174	t	t
992	11	26	2017-08-14 11:25:16.610202	t	t
993	11	11	2017-08-13 11:25:16.610231	t	t
994	11	32	2017-07-26 11:25:16.610259	t	t
995	11	9	2017-08-13 11:25:16.610288	t	t
996	11	31	2017-08-06 11:25:16.61033	t	t
997	11	19	2017-08-19 11:25:16.610371	t	t
998	11	21	2017-08-02 11:25:16.610399	t	t
999	11	17	2017-08-10 11:25:16.610428	t	t
1000	11	36	2017-07-28 11:25:16.610456	t	t
1001	11	24	2017-08-01 11:25:16.610485	t	t
1002	11	13	2017-08-05 11:25:16.610513	f	t
1003	11	34	2017-08-11 11:25:16.610541	f	t
1004	11	22	2017-08-07 11:25:16.61057	f	t
1005	11	26	2017-08-10 11:25:16.610598	f	t
1006	11	17	2017-07-27 11:25:16.610626	f	t
1007	11	27	2017-08-05 11:25:16.610655	f	t
1008	11	16	2017-08-15 11:25:16.610683	f	t
1009	11	7	2017-08-05 11:25:16.610711	f	t
1010	11	20	2017-08-03 11:25:16.610739	f	t
1011	11	24	2017-08-17 11:25:16.610768	f	t
1012	11	25	2017-07-30 11:25:16.610797	f	t
1013	11	19	2017-08-09 11:25:16.610826	f	t
1014	11	35	2017-07-26 11:25:16.610855	f	t
1015	11	14	2017-08-04 11:25:16.610883	f	t
1016	11	37	2017-08-05 11:25:16.610912	f	t
1017	11	32	2017-08-09 11:25:16.610941	f	t
1018	11	28	2017-07-30 11:25:16.610969	f	t
1019	11	8	2017-08-18 11:25:16.610997	f	t
1020	11	12	2017-08-16 11:25:16.611025	f	t
1021	11	31	2017-08-14 11:25:16.611054	f	t
1022	11	36	2017-08-03 11:25:16.611082	f	t
1023	11	33	2017-08-11 11:25:16.61111	f	t
1024	11	11	2017-08-06 11:25:16.611138	f	t
1025	11	15	2017-07-30 11:25:16.611167	f	t
1026	11	10	2017-08-18 11:25:16.611206	f	t
1027	11	9	2017-08-07 11:25:16.611235	f	t
1028	12	24	2017-08-02 11:25:16.611273	t	t
1029	12	29	2017-08-16 11:25:16.611313	t	t
1030	12	14	2017-08-04 11:25:16.611374	t	t
1031	12	19	2017-08-12 11:25:16.611436	t	t
1032	12	16	2017-07-31 11:25:16.611491	t	t
1033	12	9	2017-08-17 11:25:16.61154	t	t
1034	12	34	2017-08-13 11:25:16.611592	t	t
1035	12	37	2017-07-30 11:25:16.611629	t	t
1036	12	25	2017-08-09 11:25:16.611699	t	t
1037	12	11	2017-08-16 11:25:16.611731	f	t
1038	12	8	2017-08-06 11:25:16.611761	f	t
1039	12	24	2017-08-01 11:25:16.611791	f	t
1040	12	22	2017-08-16 11:25:16.611819	f	t
1041	12	29	2017-08-06 11:25:16.611849	f	t
1042	12	9	2017-08-08 11:25:16.611878	f	t
1043	12	36	2017-08-09 11:25:16.611907	f	t
1044	12	34	2017-07-31 11:25:16.611936	f	t
1045	12	17	2017-08-07 11:25:16.611964	f	t
1046	15	37	2017-07-27 11:25:16.611993	t	t
1047	15	34	2017-08-08 11:25:16.612021	t	t
1048	16	31	2017-08-18 11:25:16.61205	t	t
1049	16	9	2017-08-07 11:25:16.612079	t	t
1050	16	14	2017-07-31 11:25:16.612107	t	t
1051	16	18	2017-07-29 11:25:16.612136	t	t
1052	16	13	2017-07-26 11:25:16.612165	t	t
1053	16	29	2017-08-15 11:25:16.612194	t	t
1054	16	24	2017-08-10 11:25:16.612223	t	t
1055	16	17	2017-08-04 11:25:16.612251	f	t
1056	16	36	2017-07-29 11:25:16.61228	f	t
1057	17	23	2017-08-01 11:25:16.612308	t	t
1058	17	21	2017-08-04 11:25:16.612336	t	t
1059	17	36	2017-08-06 11:25:16.612365	t	t
1060	17	22	2017-08-10 11:25:16.612394	t	t
1061	17	29	2017-08-15 11:25:16.612422	t	t
1062	17	11	2017-08-17 11:25:16.612451	t	t
1063	17	14	2017-08-08 11:25:16.61248	t	t
1064	17	15	2017-08-06 11:25:16.612508	t	t
1065	17	37	2017-08-06 11:25:16.612537	t	t
1066	17	12	2017-08-08 11:25:16.612565	t	t
1067	17	19	2017-07-25 11:25:16.612594	t	t
1068	17	17	2017-07-25 11:25:16.612623	t	t
1069	17	10	2017-08-14 11:25:16.612652	t	t
1070	17	24	2017-07-30 11:25:16.612682	t	t
1071	17	28	2017-08-11 11:25:16.612711	t	t
1072	17	16	2017-08-11 11:25:16.61274	t	t
1073	17	25	2017-07-29 11:25:16.612769	t	t
1074	17	20	2017-08-17 11:25:16.612798	t	t
1075	17	8	2017-07-29 11:25:16.612827	t	t
1076	17	29	2017-07-26 11:25:16.612856	t	t
1077	17	35	2017-07-26 11:25:16.612884	t	t
1078	17	27	2017-08-10 11:25:16.612912	t	t
1079	17	34	2017-08-07 11:25:16.612941	t	t
1080	17	32	2017-08-18 11:25:16.61297	t	t
1081	17	9	2017-08-12 11:25:16.612999	t	t
1082	17	31	2017-07-28 11:25:16.613028	t	t
1083	17	29	2017-08-07 11:25:16.613056	f	t
1084	17	13	2017-08-08 11:25:16.613085	f	t
1085	17	16	2017-07-28 11:25:16.613113	f	t
1086	17	21	2017-08-08 11:25:16.613141	f	t
1087	19	7	2017-08-09 11:25:16.61317	t	t
1088	19	11	2017-08-09 11:25:16.6132	f	t
1089	19	35	2017-07-29 11:25:16.613229	f	t
1090	20	21	2017-08-10 11:25:16.613257	t	t
1091	20	36	2017-08-16 11:25:16.613287	t	t
1092	20	14	2017-07-28 11:25:16.613316	t	t
1093	20	11	2017-08-07 11:25:16.613345	t	t
1094	20	22	2017-07-26 11:25:16.613374	t	t
1095	20	34	2017-08-07 11:25:16.613403	t	t
1096	20	25	2017-07-30 11:25:16.613431	t	t
1097	20	13	2017-08-15 11:25:16.61346	t	t
1098	20	23	2017-08-04 11:25:16.613488	t	t
1099	20	9	2017-08-07 11:25:16.613518	t	t
1100	20	7	2017-08-03 11:25:16.613546	t	t
1101	20	20	2017-07-29 11:25:16.613575	t	t
1102	20	29	2017-08-17 11:25:16.613604	t	t
1103	20	17	2017-08-01 11:25:16.613633	t	t
1104	20	29	2017-08-02 11:25:16.613662	t	t
1105	20	35	2017-07-25 11:25:16.613691	t	t
1106	20	19	2017-08-19 11:25:16.61372	t	t
1107	20	28	2017-08-19 11:25:16.613749	t	t
1108	20	7	2017-08-06 11:25:16.613777	f	t
1109	20	22	2017-08-17 11:25:16.613806	f	t
1110	20	12	2017-08-13 11:25:16.613834	f	t
1111	20	32	2017-08-11 11:25:16.613863	f	t
1112	20	11	2017-07-27 11:25:16.613892	f	t
1113	20	29	2017-08-10 11:25:16.613921	f	t
1114	20	31	2017-07-28 11:25:16.613961	f	t
1115	20	34	2017-08-09 11:25:16.614001	f	t
1116	20	36	2017-08-13 11:25:16.614029	f	t
1117	20	20	2017-08-12 11:25:16.614058	f	t
1118	20	37	2017-07-31 11:25:16.614108	f	t
1119	20	14	2017-08-09 11:25:16.614138	f	t
1120	20	10	2017-07-25 11:25:16.614166	f	t
1121	20	26	2017-08-17 11:25:16.614195	f	t
1122	20	16	2017-08-13 11:25:16.614224	f	t
1123	20	27	2017-08-13 11:25:16.614252	f	t
1124	20	33	2017-08-17 11:25:16.61428	f	t
1125	21	13	2017-07-27 11:25:16.614309	f	t
1126	21	12	2017-08-07 11:25:16.614345	f	t
1127	23	8	2017-08-08 11:25:16.614374	f	t
1128	23	28	2017-08-06 11:25:16.614402	f	t
1129	23	34	2017-07-30 11:25:16.614431	f	t
1130	24	8	2017-08-12 11:25:16.614459	f	t
1131	24	17	2017-08-16 11:25:16.614488	f	t
1132	24	31	2017-08-08 11:25:16.614516	f	t
1133	24	13	2017-08-10 11:25:16.614544	f	t
1134	26	16	2017-08-19 11:25:16.614573	t	t
1135	26	17	2017-08-01 11:25:16.614601	t	t
1136	26	31	2017-08-01 11:25:16.614629	f	t
1137	26	16	2017-07-31 11:25:16.614657	f	t
1138	27	31	2017-08-03 11:25:16.614685	t	t
1139	27	23	2017-08-07 11:25:16.614714	t	t
1140	27	12	2017-08-01 11:25:16.614741	t	t
1141	27	14	2017-08-18 11:25:16.61477	t	t
1142	27	19	2017-07-29 11:25:16.614799	t	t
1143	27	20	2017-07-30 11:25:16.614827	f	t
1144	27	9	2017-08-06 11:25:16.614856	f	t
1145	28	29	2017-08-01 11:25:16.614884	t	t
1146	28	18	2017-07-27 11:25:16.614913	t	t
1147	28	37	2017-08-14 11:25:16.614941	t	t
1148	28	35	2017-08-16 11:25:16.61497	f	t
1149	28	26	2017-08-03 11:25:16.614999	f	t
1150	28	14	2017-07-28 11:25:16.615028	f	t
1151	28	27	2017-08-17 11:25:16.615056	f	t
1152	28	29	2017-08-14 11:25:16.615085	f	t
1153	28	19	2017-08-12 11:25:16.615114	f	t
1154	29	13	2017-08-12 11:25:16.615143	t	t
1155	29	7	2017-08-08 11:25:16.615171	t	t
1156	29	34	2017-08-12 11:25:16.6152	t	t
1157	29	21	2017-08-10 11:25:16.615229	t	t
1158	29	15	2017-07-26 11:25:16.615258	t	t
1159	29	28	2017-08-16 11:25:16.615287	t	t
1160	29	29	2017-08-07 11:25:16.615316	t	t
1161	29	10	2017-08-03 11:25:16.615345	t	t
1162	29	25	2017-08-06 11:25:16.615373	f	t
1163	29	28	2017-08-19 11:25:16.615402	f	t
1164	29	20	2017-08-14 11:25:16.61543	f	t
1165	29	8	2017-07-28 11:25:16.615459	f	t
1166	30	25	2017-08-17 11:25:16.615488	t	t
1167	30	35	2017-08-18 11:25:16.615516	t	t
1168	30	17	2017-08-19 11:25:16.615544	t	t
1169	30	21	2017-07-26 11:25:16.615573	t	t
1170	30	29	2017-08-12 11:25:16.615601	t	t
1171	30	33	2017-08-04 11:25:16.61563	t	t
1172	30	32	2017-08-12 11:25:16.615658	t	t
1173	30	19	2017-08-09 11:25:16.615687	t	t
1174	30	37	2017-08-06 11:25:16.615716	t	t
1175	30	25	2017-07-26 11:25:16.615744	f	t
1176	30	19	2017-08-15 11:25:16.615773	f	t
1177	30	7	2017-08-03 11:25:16.615802	f	t
1178	30	23	2017-07-25 11:25:16.61583	f	t
1179	30	27	2017-07-31 11:25:16.615859	f	t
1180	30	20	2017-08-07 11:25:16.615888	f	t
1181	30	16	2017-08-02 11:25:16.615916	f	t
1182	30	29	2017-08-05 11:25:16.615945	f	t
1183	30	35	2017-08-12 11:25:16.615973	f	t
1184	30	12	2017-08-19 11:25:16.616018	f	t
1185	30	26	2017-07-30 11:25:16.616069	f	t
1186	30	22	2017-07-27 11:25:16.616111	f	t
1187	30	31	2017-08-07 11:25:16.616142	f	t
1188	30	10	2017-07-28 11:25:16.616172	f	t
1189	30	21	2017-08-15 11:25:16.616201	f	t
1190	30	15	2017-08-14 11:25:16.61623	f	t
1191	30	33	2017-07-26 11:25:16.616259	f	t
1192	32	36	2017-08-04 11:25:16.616287	f	t
1193	32	17	2017-08-10 11:25:16.616316	f	t
1194	32	19	2017-07-29 11:25:16.616345	f	t
1195	32	16	2017-08-07 11:25:16.616374	f	t
1196	32	11	2017-08-11 11:25:16.616403	f	t
1197	32	8	2017-08-07 11:25:16.616431	f	t
1198	32	31	2017-08-11 11:25:16.61646	f	t
1199	32	18	2017-08-15 11:25:16.61649	f	t
1200	32	33	2017-08-07 11:25:16.616519	f	t
1201	32	28	2017-07-26 11:25:16.616548	f	t
1202	32	14	2017-07-30 11:25:16.616578	f	t
1203	32	7	2017-08-18 11:25:16.616606	f	t
1204	32	21	2017-08-03 11:25:16.616635	f	t
1205	32	23	2017-08-06 11:25:16.616664	f	t
1206	32	25	2017-08-03 11:25:16.616693	f	t
1207	32	12	2017-08-08 11:25:16.616721	f	t
1208	32	15	2017-08-02 11:25:16.61675	f	t
1209	32	13	2017-08-18 11:25:16.616778	f	t
1210	32	29	2017-08-08 11:25:16.616807	f	t
1211	34	10	2017-07-29 11:25:16.616836	f	t
1212	34	25	2017-08-15 11:25:16.616865	f	t
1213	34	26	2017-08-16 11:25:16.616894	f	t
1214	34	9	2017-08-04 11:25:16.616923	f	t
1215	34	27	2017-08-15 11:25:16.616951	f	t
1216	34	22	2017-07-31 11:25:16.616979	f	t
1217	34	16	2017-08-19 11:25:16.617009	f	t
1218	34	33	2017-08-15 11:25:16.617038	f	t
1219	34	34	2017-07-25 11:25:16.617067	f	t
1220	34	31	2017-08-14 11:25:16.617095	f	t
1221	34	32	2017-08-14 11:25:16.617124	f	t
1222	34	21	2017-08-18 11:25:16.617163	f	t
1223	35	23	2017-08-09 11:25:16.617194	t	t
1224	35	27	2017-08-10 11:25:16.617224	t	t
1225	35	22	2017-08-19 11:25:16.617253	t	t
1226	35	37	2017-07-25 11:25:16.617282	t	t
1227	35	18	2017-07-31 11:25:16.617311	t	t
1228	35	20	2017-08-03 11:25:16.617339	t	t
1229	35	34	2017-08-11 11:25:16.617368	f	t
1230	35	17	2017-07-26 11:25:16.617397	f	t
1231	35	29	2017-08-10 11:25:16.617425	f	t
1232	35	19	2017-08-02 11:25:16.617454	f	t
1233	35	9	2017-08-12 11:25:16.617483	f	t
1234	35	29	2017-07-27 11:25:16.617518	f	t
1235	36	23	2017-07-26 11:25:16.617549	t	t
1236	36	8	2017-08-15 11:25:16.617578	t	t
1237	36	28	2017-07-28 11:25:16.617607	t	t
1238	36	19	2017-08-15 11:25:16.617635	t	t
1239	36	17	2017-08-13 11:25:16.617664	t	t
1240	36	29	2017-08-02 11:25:16.617693	t	t
1241	36	11	2017-07-27 11:25:16.617722	t	t
1242	36	31	2017-07-29 11:25:16.617751	f	t
1243	36	21	2017-08-10 11:25:16.617779	f	t
1244	36	11	2017-08-04 11:25:16.617807	f	t
1245	36	19	2017-08-10 11:25:16.617835	f	t
1246	36	18	2017-07-26 11:25:16.617865	f	t
1247	36	35	2017-07-31 11:25:16.617894	f	t
1248	36	29	2017-08-11 11:25:16.617923	f	t
1249	36	15	2017-08-19 11:25:16.617952	f	t
1250	36	8	2017-08-18 11:25:16.617981	f	t
1251	36	32	2017-08-01 11:25:16.618009	f	t
1252	36	17	2017-07-28 11:25:16.618038	f	t
1253	36	29	2017-08-04 11:25:16.618066	f	t
1254	36	24	2017-07-29 11:25:16.618096	f	t
1255	36	37	2017-07-31 11:25:16.618125	f	t
1256	36	7	2017-08-09 11:25:16.618154	f	t
1257	36	14	2017-08-19 11:25:16.618183	f	t
1258	36	23	2017-08-04 11:25:16.618212	f	t
1259	36	13	2017-07-30 11:25:16.61824	f	t
1260	39	16	2017-08-16 11:25:16.618269	t	t
1261	39	9	2017-08-06 11:25:16.618299	t	t
1262	39	15	2017-08-03 11:25:16.618332	t	t
1263	39	24	2017-07-30 11:25:16.618362	t	t
1264	39	12	2017-08-15 11:25:16.618391	t	t
1265	39	35	2017-08-03 11:25:16.618421	t	t
1266	39	36	2017-08-04 11:25:16.61845	t	t
1267	39	7	2017-08-01 11:25:16.618478	t	t
1268	39	29	2017-08-07 11:25:16.618507	t	t
1269	39	14	2017-08-10 11:25:16.618536	t	t
1270	39	17	2017-08-09 11:25:16.618564	t	t
1271	39	23	2017-07-28 11:25:16.618593	t	t
1272	39	29	2017-08-17 11:25:16.618622	t	t
1273	39	10	2017-07-26 11:25:16.618651	t	t
1274	39	28	2017-08-17 11:25:16.618679	t	t
1275	39	20	2017-08-16 11:25:16.618708	t	t
1276	39	23	2017-08-16 11:25:16.618738	f	t
1277	39	36	2017-08-11 11:25:16.618766	f	t
1278	39	24	2017-08-13 11:25:16.618794	f	t
1279	39	19	2017-07-31 11:25:16.618823	f	t
1280	39	37	2017-08-07 11:25:16.618851	f	t
1281	39	22	2017-07-29 11:25:16.61888	f	t
1282	39	17	2017-08-10 11:25:16.618909	f	t
1283	39	29	2017-07-28 11:25:16.618937	f	t
1284	39	21	2017-08-02 11:25:16.618965	f	t
1285	39	9	2017-07-26 11:25:16.618994	f	t
1286	39	16	2017-08-14 11:25:16.619022	f	t
1287	39	34	2017-08-18 11:25:16.619051	f	t
1288	39	29	2017-08-16 11:25:16.61908	f	t
1289	39	7	2017-08-13 11:25:16.619109	f	t
1290	39	33	2017-08-01 11:25:16.619137	f	t
1291	40	32	2017-07-25 11:25:16.619166	t	t
1292	40	11	2017-08-01 11:25:16.619198	t	t
1293	40	23	2017-08-04 11:25:16.619243	t	t
1294	40	18	2017-08-18 11:25:16.619274	t	t
1295	40	27	2017-08-07 11:25:16.619304	t	t
1296	40	35	2017-08-15 11:25:16.619332	t	t
1297	40	28	2017-08-09 11:25:16.619361	f	t
1298	40	13	2017-08-13 11:25:16.619391	f	t
1299	41	22	2017-08-17 11:25:16.61942	t	t
1300	41	13	2017-08-05 11:25:16.619449	t	t
1301	41	12	2017-08-12 11:25:16.619478	t	t
1302	41	36	2017-08-11 11:25:16.619507	t	t
1303	41	37	2017-07-29 11:25:16.619536	t	t
1304	41	19	2017-08-04 11:25:16.619565	t	t
1305	41	16	2017-08-10 11:25:16.619593	t	t
1306	41	10	2017-07-30 11:25:16.619622	t	t
1307	41	25	2017-08-16 11:25:16.619651	t	t
1308	41	24	2017-07-26 11:25:16.61968	t	t
1309	41	34	2017-07-25 11:25:16.619708	t	t
1310	41	20	2017-08-07 11:25:16.619737	t	t
1311	41	27	2017-08-09 11:25:16.619765	t	t
1312	41	32	2017-08-07 11:25:16.619794	t	t
1313	41	7	2017-08-04 11:25:16.619822	t	t
1314	41	11	2017-08-15 11:25:16.619851	t	t
1315	41	14	2017-07-28 11:25:16.619879	t	t
1316	41	35	2017-08-03 11:25:16.619908	t	t
1317	41	28	2017-08-05 11:25:16.619936	t	t
1318	41	21	2017-08-08 11:25:16.619965	t	t
1319	41	26	2017-08-06 11:25:16.619993	t	t
1320	41	18	2017-08-14 11:25:16.620022	t	t
1321	41	29	2017-08-02 11:25:16.620051	t	t
1322	41	15	2017-08-09 11:25:16.62008	t	t
1323	41	16	2017-08-09 11:25:16.620108	f	t
1324	41	10	2017-08-07 11:25:16.620136	f	t
1325	41	33	2017-08-10 11:25:16.620164	f	t
1326	41	18	2017-08-11 11:25:16.620193	f	t
1327	41	14	2017-07-25 11:25:16.620222	f	t
1328	41	7	2017-08-18 11:25:16.620251	f	t
1329	41	17	2017-08-03 11:25:16.62028	f	t
1330	41	25	2017-08-02 11:25:16.620309	f	t
1331	41	12	2017-08-17 11:25:16.620337	f	t
1332	41	24	2017-07-30 11:25:16.620366	f	t
1333	41	11	2017-08-07 11:25:16.620395	f	t
1334	41	35	2017-08-05 11:25:16.620424	f	t
1335	41	28	2017-07-31 11:25:16.620452	f	t
1336	41	15	2017-08-01 11:25:16.620481	f	t
1337	41	34	2017-07-31 11:25:16.62051	f	t
1338	41	37	2017-08-03 11:25:16.620539	f	t
1339	41	36	2017-08-15 11:25:16.620568	f	t
1340	41	31	2017-08-03 11:25:16.620597	f	t
1341	41	32	2017-08-04 11:25:16.620625	f	t
1342	41	29	2017-08-02 11:25:16.620654	f	t
1343	41	27	2017-08-13 11:25:16.620693	f	t
1344	41	19	2017-08-15 11:25:16.620732	f	t
1345	41	9	2017-08-14 11:25:16.62076	f	t
1346	41	21	2017-08-04 11:25:16.620789	f	t
1347	41	8	2017-07-27 11:25:16.620818	f	t
1348	42	12	2017-08-01 11:25:16.620847	t	t
1349	42	17	2017-08-10 11:25:16.620875	t	t
1350	42	35	2017-07-26 11:25:16.620904	t	t
1351	42	18	2017-08-06 11:25:16.620952	t	t
1352	42	16	2017-07-27 11:25:16.620982	t	t
1353	42	33	2017-08-07 11:25:16.621011	t	t
1354	42	33	2017-08-15 11:25:16.62104	f	t
1355	42	36	2017-08-08 11:25:16.621069	f	t
1356	42	15	2017-08-19 11:25:16.621097	f	t
1357	42	23	2017-08-07 11:25:16.621126	f	t
1358	42	34	2017-08-03 11:25:16.621155	f	t
1359	44	29	2017-07-26 11:25:16.621184	t	t
1360	44	18	2017-08-17 11:25:16.621212	t	t
1361	44	36	2017-07-29 11:25:16.62124	t	t
1362	44	10	2017-08-08 11:25:16.621269	t	t
1363	44	27	2017-08-06 11:25:16.621297	t	t
1364	44	16	2017-08-18 11:25:16.621325	f	t
1365	44	21	2017-08-08 11:25:16.621354	f	t
1366	44	18	2017-08-04 11:25:16.621383	f	t
1367	44	22	2017-07-26 11:25:16.621412	f	t
1368	44	24	2017-07-28 11:25:16.62144	f	t
1369	44	29	2017-08-01 11:25:16.621468	f	t
1370	46	8	2017-08-09 11:25:16.621497	f	t
1371	46	18	2017-07-25 11:25:16.621525	f	t
1372	46	34	2017-07-30 11:25:16.621553	f	t
1373	46	21	2017-08-01 11:25:16.621581	f	t
1374	46	35	2017-08-13 11:25:16.62161	f	t
1375	46	22	2017-07-26 11:25:16.621638	f	t
1376	47	14	2017-08-11 11:25:16.621667	t	t
1377	47	10	2017-08-02 11:25:16.621695	t	t
1378	47	29	2017-08-10 11:25:16.621723	t	t
1379	47	33	2017-08-12 11:25:16.621752	f	t
1380	47	17	2017-07-28 11:25:16.62178	f	t
1381	47	10	2017-08-08 11:25:16.621808	f	t
1382	49	7	2017-07-30 11:25:16.621837	f	t
1383	49	9	2017-07-26 11:25:16.621865	f	t
1384	49	26	2017-08-05 11:25:16.621893	f	t
1385	50	23	2017-08-14 11:25:16.621921	t	t
1386	50	12	2017-07-25 11:25:16.621949	t	t
1387	50	22	2017-08-18 11:25:16.621977	t	t
1388	50	27	2017-07-29 11:25:16.622006	t	t
1389	50	28	2017-07-26 11:25:16.622035	t	t
1390	50	7	2017-07-28 11:25:16.622063	f	t
1391	50	35	2017-08-15 11:25:16.622092	f	t
1392	50	21	2017-07-30 11:25:16.62212	f	t
1393	50	17	2017-08-03 11:25:16.622149	f	t
1394	50	34	2017-08-11 11:25:16.622178	f	t
1395	50	12	2017-08-13 11:25:16.622206	f	t
1396	50	36	2017-08-09 11:25:16.622234	f	t
1397	50	33	2017-08-13 11:25:16.622262	f	t
1398	50	20	2017-08-02 11:25:16.62229	f	t
1399	51	37	2017-07-28 11:25:16.622323	t	t
1400	51	34	2017-07-27 11:25:16.622353	t	t
1401	54	36	2017-07-25 11:25:16.622381	t	t
1402	54	28	2017-08-16 11:25:16.62241	t	t
1403	54	14	2017-08-18 11:25:16.622438	t	t
1404	54	11	2017-07-29 11:25:16.622467	t	t
1405	54	8	2017-08-19 11:25:16.622495	t	t
1406	54	16	2017-08-17 11:25:16.622524	t	t
1407	54	13	2017-08-12 11:25:16.622553	t	t
1408	54	9	2017-08-11 11:25:16.622581	t	t
1409	54	37	2017-07-27 11:25:16.62261	f	t
1410	55	11	2017-07-29 11:25:16.622639	t	t
1411	55	26	2017-08-14 11:25:16.622668	t	t
1412	55	33	2017-08-07 11:25:16.622696	t	t
1413	55	35	2017-08-19 11:25:16.622725	t	t
1414	55	31	2017-07-30 11:25:16.622754	t	t
1415	55	10	2017-08-17 11:25:16.622782	t	t
1416	55	36	2017-08-11 11:25:16.622811	t	t
1417	55	16	2017-07-27 11:25:16.622839	t	t
1418	55	15	2017-08-08 11:25:16.622868	t	t
1419	55	14	2017-08-10 11:25:16.622896	t	t
1420	55	13	2017-08-02 11:25:16.622925	t	t
1421	56	25	2017-08-18 11:25:16.622953	t	t
1422	56	37	2017-08-15 11:25:16.622982	f	t
1423	56	28	2017-07-28 11:25:16.62301	f	t
1424	56	7	2017-08-10 11:25:16.623039	f	t
1425	56	27	2017-08-18 11:25:16.623068	f	t
1426	56	17	2017-08-18 11:25:16.623097	f	t
1427	56	29	2017-08-19 11:25:16.623126	f	t
1428	56	19	2017-08-02 11:25:16.623154	f	t
1429	56	9	2017-07-31 11:25:16.623182	f	t
1430	56	29	2017-08-05 11:25:16.623211	f	t
1431	56	13	2017-08-03 11:25:16.62324	f	t
1432	56	23	2017-07-25 11:25:16.623279	f	t
1433	56	12	2017-08-16 11:25:16.623312	f	t
1434	56	36	2017-08-08 11:25:16.623342	f	t
1435	56	16	2017-07-28 11:25:16.623382	f	t
1436	57	17	2017-08-09 11:25:16.623422	t	t
1437	57	18	2017-07-29 11:25:16.623473	t	t
1438	57	7	2017-07-27 11:25:16.623513	t	t
1439	57	10	2017-08-14 11:25:16.623551	t	t
1440	57	31	2017-08-04 11:25:16.62358	t	t
1441	57	29	2017-08-02 11:25:16.623609	t	t
1442	57	9	2017-08-18 11:25:16.623637	t	t
1443	57	14	2017-08-11 11:25:16.623666	f	t
1444	57	8	2017-07-26 11:25:16.623695	f	t
1445	57	25	2017-08-09 11:25:16.623724	f	t
1446	57	34	2017-07-28 11:25:16.623753	f	t
1447	57	22	2017-08-14 11:25:16.623782	f	t
1448	57	28	2017-08-18 11:25:16.623811	f	t
1449	57	37	2017-07-30 11:25:16.623839	f	t
1450	57	29	2017-07-25 11:25:16.623868	f	t
1451	57	13	2017-08-03 11:25:16.623897	f	t
1452	58	34	2017-08-05 11:25:16.623925	t	t
1453	58	20	2017-08-13 11:25:16.623953	t	t
1454	58	31	2017-08-16 11:25:16.623981	t	t
1455	58	23	2017-08-15 11:25:16.62401	t	t
1456	58	13	2017-08-03 11:25:16.624038	t	t
1457	58	36	2017-08-14 11:25:16.624066	t	t
1458	58	14	2017-08-17 11:25:16.624095	t	t
1459	58	33	2017-08-05 11:25:16.624124	t	t
1460	58	16	2017-08-03 11:25:16.624152	t	t
1461	58	8	2017-08-12 11:25:16.62418	t	t
1462	58	28	2017-07-27 11:25:16.624209	t	t
1463	58	32	2017-08-06 11:25:16.624238	t	t
1464	58	9	2017-07-30 11:25:16.624266	t	t
1465	58	24	2017-07-28 11:25:16.624294	t	t
1466	58	35	2017-08-16 11:25:16.624323	t	t
1467	58	25	2017-08-12 11:25:16.624352	t	t
1468	58	12	2017-08-01 11:25:16.62438	t	t
1469	58	11	2017-07-28 11:25:16.624408	t	t
1470	58	37	2017-08-03 11:25:16.624437	f	t
1471	58	7	2017-08-13 11:25:16.624466	f	t
1472	58	35	2017-08-04 11:25:16.624494	f	t
1473	58	21	2017-08-12 11:25:16.624522	f	t
1474	58	17	2017-08-09 11:25:16.624549	f	t
1475	58	29	2017-08-18 11:25:16.624578	f	t
1476	58	11	2017-08-09 11:25:16.624605	f	t
1477	58	23	2017-08-16 11:25:16.624634	f	t
1478	58	31	2017-07-30 11:25:16.624662	f	t
1479	58	10	2017-08-18 11:25:16.62469	f	t
1480	58	29	2017-08-16 11:25:16.624718	f	t
1481	58	24	2017-08-11 11:25:16.624746	f	t
1482	58	26	2017-07-25 11:25:16.624774	f	t
1483	58	13	2017-08-17 11:25:16.624803	f	t
1484	58	19	2017-08-15 11:25:16.624831	f	t
1485	59	12	2017-08-14 11:25:16.62486	f	t
1486	59	23	2017-08-04 11:25:16.624889	f	t
1487	59	11	2017-07-28 11:25:16.624917	f	t
1488	59	27	2017-08-13 11:25:16.624946	f	t
1489	59	29	2017-07-25 11:25:16.624974	f	t
1490	59	24	2017-08-10 11:25:16.625003	f	t
1491	59	36	2017-07-28 11:25:16.625031	f	t
1492	59	28	2017-07-27 11:25:16.625061	f	t
1493	59	25	2017-08-05 11:25:16.625089	f	t
1494	59	13	2017-08-10 11:25:16.625118	f	t
1495	59	20	2017-07-30 11:25:16.625146	f	t
1496	59	22	2017-08-14 11:25:16.625174	f	t
1497	59	35	2017-08-19 11:25:16.625203	f	t
1498	59	19	2017-08-16 11:25:16.625232	f	t
1499	59	32	2017-07-30 11:25:16.625261	f	t
1500	59	17	2017-08-15 11:25:16.62529	f	t
1501	60	32	2017-08-03 11:25:16.625319	t	t
1502	60	11	2017-08-09 11:25:16.625347	t	t
1503	60	29	2017-07-30 11:25:16.625376	t	t
1504	60	25	2017-07-30 11:25:16.625404	t	t
1505	60	8	2017-08-04 11:25:16.625433	f	t
1506	60	9	2017-08-01 11:25:16.625461	f	t
1507	60	16	2017-08-05 11:25:16.625489	f	t
1508	60	26	2017-08-14 11:25:16.625517	f	t
1509	60	17	2017-08-19 11:25:16.625546	f	t
1510	60	21	2017-08-06 11:25:16.625574	f	t
1511	60	14	2017-08-03 11:25:16.625602	f	t
1512	61	18	2017-08-07 11:25:16.62563	t	t
1513	61	16	2017-07-27 11:25:16.625658	t	t
1514	61	9	2017-08-02 11:25:16.625686	t	t
1515	61	37	2017-08-13 11:25:16.625715	t	t
1516	61	20	2017-08-05 11:25:16.625743	t	t
1517	61	26	2017-08-13 11:25:16.625771	t	t
1518	61	17	2017-08-16 11:25:16.625799	t	t
1519	61	29	2017-08-07 11:25:16.625828	t	t
1520	61	22	2017-08-12 11:25:16.625855	t	t
1521	61	25	2017-07-29 11:25:16.625883	t	t
1522	61	14	2017-08-04 11:25:16.625912	f	t
1523	61	24	2017-07-29 11:25:16.625939	f	t
1524	61	36	2017-07-27 11:25:16.625968	f	t
1525	61	22	2017-08-06 11:25:16.625996	f	t
1526	61	35	2017-08-17 11:25:16.626024	f	t
1527	62	33	2017-07-29 11:25:16.626052	t	t
1528	62	29	2017-08-18 11:25:16.626081	t	t
1529	62	7	2017-08-13 11:25:16.626109	t	t
1530	62	12	2017-08-05 11:25:16.626137	t	t
1531	62	27	2017-07-28 11:25:16.626166	f	t
1532	62	31	2017-07-27 11:25:16.626194	f	t
1533	62	22	2017-08-06 11:25:16.626223	f	t
1534	62	28	2017-08-18 11:25:16.626252	f	t
1535	62	13	2017-08-09 11:25:16.626281	f	t
1536	62	8	2017-07-31 11:25:16.626309	f	t
1537	63	35	2017-08-11 11:25:16.626356	t	t
1538	63	9	2017-07-31 11:25:16.626406	t	t
1539	63	17	2017-08-16 11:25:16.626445	t	t
1540	63	7	2017-07-28 11:25:16.626474	t	t
1541	63	36	2017-08-02 11:25:16.626515	t	t
1542	63	22	2017-07-29 11:25:16.626564	t	t
1543	63	16	2017-08-07 11:25:16.626592	t	t
1544	63	20	2017-08-07 11:25:16.626621	t	t
1545	63	31	2017-08-04 11:25:16.626649	t	t
1546	63	29	2017-07-29 11:25:16.626677	t	t
1547	63	37	2017-07-25 11:25:16.626705	f	t
1548	63	7	2017-08-10 11:25:16.626733	f	t
1549	63	27	2017-08-10 11:25:16.626761	f	t
1550	63	26	2017-08-15 11:25:16.626789	f	t
1551	63	12	2017-08-17 11:25:16.626818	f	t
1552	63	28	2017-07-26 11:25:16.626847	f	t
1553	63	14	2017-08-17 11:25:16.626876	f	t
1554	63	22	2017-08-05 11:25:16.626904	f	t
1555	63	17	2017-07-27 11:25:16.626932	f	t
1556	63	29	2017-08-18 11:25:16.62696	f	t
1557	63	11	2017-08-08 11:25:16.626988	f	t
1558	63	9	2017-08-03 11:25:16.627017	f	t
1559	63	32	2017-08-10 11:25:16.627045	f	t
1560	64	11	2017-08-06 11:25:16.627073	t	t
1561	64	27	2017-07-29 11:25:16.627101	t	t
1562	64	21	2017-07-28 11:25:16.627129	f	t
1563	64	25	2017-08-18 11:25:16.627158	f	t
1564	64	26	2017-08-15 11:25:16.627186	f	t
1565	65	23	2017-07-26 11:25:16.627214	t	t
1566	65	32	2017-08-02 11:25:16.627243	t	t
1567	65	14	2017-07-25 11:25:16.627271	t	t
1568	65	31	2017-08-18 11:25:16.627299	t	t
1569	65	21	2017-07-30 11:25:16.627327	t	t
1570	65	12	2017-08-09 11:25:16.627355	t	t
1571	65	37	2017-08-10 11:25:16.627383	f	t
1572	65	14	2017-08-02 11:25:16.627412	f	t
1573	65	31	2017-08-05 11:25:16.62744	f	t
1574	66	23	2017-08-10 11:25:16.627469	t	t
1575	66	24	2017-08-08 11:25:16.627497	t	t
1576	66	32	2017-07-28 11:25:16.627524	t	t
1577	66	16	2017-08-12 11:25:16.627552	t	t
1578	66	20	2017-08-02 11:25:16.62758	f	t
1579	66	24	2017-08-07 11:25:16.627608	f	t
1580	66	14	2017-08-18 11:25:16.627637	f	t
1581	66	32	2017-08-16 11:25:16.627665	f	t
1582	66	29	2017-07-30 11:25:16.627694	f	t
1583	66	7	2017-07-26 11:25:16.627723	f	t
1584	66	21	2017-07-26 11:25:16.627769	f	t
1585	66	25	2017-08-02 11:25:16.627798	f	t
1586	66	27	2017-07-25 11:25:16.627827	f	t
1587	66	12	2017-08-09 11:25:16.627865	f	t
1588	66	19	2017-08-08 11:25:16.627905	f	t
1589	67	19	2017-07-31 11:25:16.627933	t	t
1590	67	7	2017-08-14 11:25:16.627962	t	t
1591	68	8	2017-08-17 11:25:16.627991	t	t
1592	68	33	2017-07-29 11:25:16.62802	t	t
1593	68	21	2017-07-31 11:25:16.628048	t	t
1594	68	29	2017-08-05 11:25:16.628077	t	t
1595	68	7	2017-08-04 11:25:16.628105	t	t
1596	68	28	2017-08-14 11:25:16.628133	t	t
1597	68	32	2017-07-28 11:25:16.628162	t	t
1598	68	23	2017-08-06 11:25:16.62819	t	t
1599	68	36	2017-07-29 11:25:16.628218	t	t
1600	68	12	2017-07-31 11:25:16.628246	t	t
1601	68	25	2017-08-08 11:25:16.628275	t	t
1602	68	35	2017-08-07 11:25:16.628304	t	t
1603	68	29	2017-08-17 11:25:16.628332	t	t
1604	68	24	2017-08-01 11:25:16.628361	t	t
1605	68	31	2017-08-10 11:25:16.62839	t	t
1606	68	18	2017-08-05 11:25:16.628419	t	t
1607	68	36	2017-08-02 11:25:16.628447	f	t
1608	68	28	2017-08-09 11:25:16.628475	f	t
1609	68	10	2017-08-19 11:25:16.628515	f	t
1610	68	15	2017-08-15 11:25:16.628564	f	t
1611	68	33	2017-07-25 11:25:16.628603	f	t
1612	68	16	2017-08-01 11:25:16.628631	f	t
1613	68	32	2017-08-15 11:25:16.628659	f	t
1614	68	20	2017-08-18 11:25:16.628687	f	t
1615	68	37	2017-08-06 11:25:16.628715	f	t
1616	68	35	2017-07-27 11:25:16.628754	f	t
1617	68	25	2017-07-27 11:25:16.628843	f	t
1618	68	29	2017-08-17 11:25:16.628892	f	t
1619	68	31	2017-08-05 11:25:16.628946	f	t
1620	68	26	2017-08-18 11:25:16.629016	f	t
1621	6	21	2017-08-19 11:25:16.629051	t	t
1622	6	11	2017-07-27 11:25:16.629081	t	t
1623	7	19	2017-08-09 11:25:16.629111	t	t
1624	7	24	2017-08-19 11:25:16.62914	t	t
1625	7	26	2017-08-10 11:25:16.629169	t	t
1626	7	25	2017-07-29 11:25:16.629198	f	t
1627	7	10	2017-08-07 11:25:16.629227	f	t
1628	7	17	2017-08-15 11:25:16.629256	f	t
1629	7	36	2017-07-31 11:25:16.629285	f	t
1630	7	8	2017-07-28 11:25:16.629314	f	t
1631	7	31	2017-08-19 11:25:16.629343	f	t
1632	7	14	2017-08-01 11:25:16.629373	f	t
1633	7	27	2017-08-08 11:25:16.629402	f	t
1634	7	35	2017-08-16 11:25:16.62943	f	t
1635	7	24	2017-08-07 11:25:16.629459	f	t
1636	7	26	2017-07-25 11:25:16.629487	f	t
1637	9	26	2017-07-30 11:25:16.629516	t	t
1638	9	23	2017-07-25 11:25:16.629545	t	t
1639	9	28	2017-08-15 11:25:16.629574	t	t
1640	9	33	2017-08-18 11:25:16.629603	t	t
1641	9	25	2017-07-26 11:25:16.629632	t	t
1642	9	11	2017-08-14 11:25:16.62966	t	t
1643	9	35	2017-08-15 11:25:16.629689	t	t
1644	9	20	2017-08-05 11:25:16.629717	t	t
1645	9	17	2017-08-06 11:25:16.629745	t	t
1646	9	16	2017-08-11 11:25:16.629773	t	t
1647	9	11	2017-07-29 11:25:16.629802	f	t
1648	9	26	2017-08-02 11:25:16.629831	f	t
1649	9	31	2017-08-15 11:25:16.62986	f	t
1650	9	35	2017-08-08 11:25:16.629888	f	t
1651	9	15	2017-08-11 11:25:16.629918	f	t
1652	9	7	2017-08-05 11:25:16.629947	f	t
1653	9	12	2017-08-03 11:25:16.629977	f	t
1654	9	19	2017-08-18 11:25:16.630006	f	t
1655	9	34	2017-07-25 11:25:16.630035	f	t
1656	9	27	2017-07-28 11:25:16.630064	f	t
1657	9	20	2017-08-03 11:25:16.630094	f	t
1658	9	18	2017-08-17 11:25:16.630122	f	t
1659	9	25	2017-08-04 11:25:16.630151	f	t
1660	9	29	2017-08-09 11:25:16.63018	f	t
1661	9	22	2017-08-01 11:25:16.630208	f	t
1662	9	8	2017-08-07 11:25:16.630237	f	t
1663	13	23	2017-08-18 11:25:16.630266	t	t
1664	13	36	2017-07-30 11:25:16.630295	t	t
1665	13	35	2017-08-08 11:25:16.630341	t	t
1666	13	8	2017-07-25 11:25:16.630391	t	t
1667	13	16	2017-07-29 11:25:16.630421	t	t
1668	13	34	2017-08-02 11:25:16.63045	t	t
1669	13	29	2017-08-05 11:25:16.630479	t	t
1670	13	12	2017-08-13 11:25:16.630507	f	t
1671	13	28	2017-07-25 11:25:16.630536	f	t
1672	13	37	2017-08-12 11:25:16.630565	f	t
1673	13	29	2017-08-14 11:25:16.630593	f	t
1674	14	15	2017-08-15 11:25:16.630622	t	t
1675	14	29	2017-08-12 11:25:16.630651	t	t
1676	14	26	2017-08-14 11:25:16.63068	t	t
1677	14	14	2017-08-17 11:25:16.630709	f	t
1678	14	23	2017-07-26 11:25:16.630738	f	t
1679	18	34	2017-08-09 11:25:16.630767	t	t
1680	18	8	2017-08-11 11:25:16.630796	t	t
1681	18	21	2017-08-18 11:25:16.630824	t	t
1682	18	22	2017-07-26 11:25:16.630852	t	t
1683	18	33	2017-08-13 11:25:16.630881	t	t
1684	18	9	2017-08-10 11:25:16.63091	t	t
1685	18	14	2017-08-03 11:25:16.630938	t	t
1686	18	19	2017-08-16 11:25:16.630967	t	t
1687	18	29	2017-08-18 11:25:16.630996	t	t
1688	18	29	2017-08-09 11:25:16.631025	t	t
1689	18	10	2017-08-07 11:25:16.631053	t	t
1690	18	36	2017-07-25 11:25:16.631081	t	t
1691	18	37	2017-08-19 11:25:16.63111	t	t
1692	18	13	2017-08-08 11:25:16.631139	t	t
1693	18	15	2017-08-03 11:25:16.631167	f	t
1694	18	27	2017-08-06 11:25:16.631195	f	t
1695	18	14	2017-08-19 11:25:16.631223	f	t
1696	18	35	2017-08-16 11:25:16.631253	f	t
1697	18	31	2017-08-07 11:25:16.631281	f	t
1698	18	23	2017-08-11 11:25:16.631311	f	t
1699	18	9	2017-08-03 11:25:16.631352	f	t
1700	18	37	2017-08-07 11:25:16.631383	f	t
1701	18	32	2017-07-29 11:25:16.631413	f	t
1702	18	16	2017-08-01 11:25:16.631442	f	t
1703	18	36	2017-08-02 11:25:16.631472	f	t
1704	18	19	2017-07-26 11:25:16.631501	f	t
1705	18	28	2017-08-19 11:25:16.63153	f	t
1706	18	25	2017-08-11 11:25:16.631559	f	t
1707	18	34	2017-08-14 11:25:16.631588	f	t
1708	18	29	2017-08-12 11:25:16.631616	f	t
1709	18	33	2017-08-07 11:25:16.631645	f	t
1710	18	21	2017-07-29 11:25:16.631673	f	t
1711	18	13	2017-07-30 11:25:16.631702	f	t
1712	18	20	2017-08-14 11:25:16.63173	f	t
1713	18	11	2017-08-01 11:25:16.631759	f	t
1714	18	17	2017-07-26 11:25:16.631787	f	t
1715	22	28	2017-08-17 11:25:16.631816	t	t
1716	22	25	2017-07-26 11:25:16.631845	t	t
1717	22	20	2017-08-11 11:25:16.631873	t	t
1718	22	12	2017-07-25 11:25:16.631902	t	t
1719	22	13	2017-08-10 11:25:16.631931	t	t
1720	22	26	2017-08-17 11:25:16.63196	f	t
1721	22	36	2017-08-09 11:25:16.631989	f	t
1722	22	10	2017-08-03 11:25:16.632018	f	t
1723	22	28	2017-07-25 11:25:16.632048	f	t
1724	22	29	2017-08-19 11:25:16.632076	f	t
1725	25	32	2017-07-27 11:25:16.632105	t	t
1726	25	15	2017-08-04 11:25:16.632134	t	t
1727	25	8	2017-08-16 11:25:16.632163	t	t
1728	25	9	2017-08-12 11:25:16.632192	t	t
1729	25	14	2017-08-08 11:25:16.63222	f	t
1730	25	16	2017-08-18 11:25:16.632249	f	t
1731	25	29	2017-08-06 11:25:16.632278	f	t
1732	25	23	2017-08-12 11:25:16.632306	f	t
1733	31	7	2017-08-01 11:25:16.632334	t	t
1734	31	17	2017-08-04 11:25:16.632363	t	t
1735	31	20	2017-08-18 11:25:16.632391	t	t
1736	31	36	2017-07-25 11:25:16.632419	t	t
1737	31	27	2017-08-04 11:25:16.632447	t	t
1738	31	16	2017-07-29 11:25:16.632476	t	t
1739	31	12	2017-08-14 11:25:16.632504	t	t
1740	31	26	2017-07-29 11:25:16.632533	t	t
1741	31	28	2017-08-06 11:25:16.632561	t	t
1742	31	35	2017-08-03 11:25:16.632589	t	t
1743	31	32	2017-08-10 11:25:16.632618	t	t
1744	31	29	2017-08-19 11:25:16.632646	t	t
1745	31	33	2017-08-06 11:25:16.632675	t	t
1746	31	25	2017-08-03 11:25:16.632703	t	t
1747	31	15	2017-07-26 11:25:16.632732	t	t
1748	31	24	2017-08-01 11:25:16.632761	t	t
1749	31	33	2017-08-10 11:25:16.632789	f	t
1750	31	34	2017-07-30 11:25:16.632817	f	t
1751	31	18	2017-08-02 11:25:16.632846	f	t
1752	31	29	2017-08-18 11:25:16.632874	f	t
1753	31	37	2017-07-30 11:25:16.632903	f	t
1754	31	31	2017-08-16 11:25:16.632931	f	t
1755	31	21	2017-08-02 11:25:16.63296	f	t
1756	31	26	2017-08-13 11:25:16.632988	f	t
1757	31	15	2017-08-06 11:25:16.633016	f	t
1758	31	12	2017-07-26 11:25:16.633044	f	t
1759	31	27	2017-08-12 11:25:16.633072	f	t
1760	31	28	2017-08-05 11:25:16.633101	f	t
1761	31	8	2017-08-04 11:25:16.633129	f	t
1762	33	17	2017-08-15 11:25:16.633157	t	t
1763	33	10	2017-08-15 11:25:16.633185	f	t
1764	33	22	2017-08-15 11:25:16.633214	f	t
1765	33	8	2017-08-15 11:25:16.633242	f	t
1766	33	24	2017-08-14 11:25:16.63327	f	t
1767	37	13	2017-08-01 11:25:16.633298	f	t
1768	37	29	2017-08-18 11:25:16.633327	f	t
1769	38	7	2017-08-02 11:25:16.633355	t	t
1770	38	31	2017-08-09 11:25:16.633383	t	t
1771	38	23	2017-08-09 11:25:16.633411	t	t
1772	38	26	2017-08-01 11:25:16.633439	t	t
1773	38	36	2017-08-11 11:25:16.633467	t	t
1774	38	18	2017-07-26 11:25:16.633495	t	t
1775	38	33	2017-08-11 11:25:16.633523	t	t
1776	38	29	2017-08-10 11:25:16.633552	t	t
1777	38	25	2017-07-28 11:25:16.63358	t	t
1778	38	14	2017-08-01 11:25:16.633608	t	t
1779	38	35	2017-08-16 11:25:16.633636	t	t
1780	38	10	2017-08-01 11:25:16.633665	t	t
1781	38	13	2017-07-27 11:25:16.633693	t	t
1782	38	15	2017-08-15 11:25:16.633722	t	t
1783	38	12	2017-07-26 11:25:16.63375	t	t
1784	38	11	2017-08-15 11:25:16.633778	t	t
1785	38	11	2017-07-31 11:25:16.633807	f	t
1786	38	7	2017-08-06 11:25:16.633835	f	t
1787	38	14	2017-07-30 11:25:16.633863	f	t
1788	38	31	2017-07-25 11:25:16.633891	f	t
1789	38	15	2017-08-07 11:25:16.633919	f	t
1790	38	22	2017-08-18 11:25:16.633947	f	t
1791	38	17	2017-08-09 11:25:16.633976	f	t
1792	38	16	2017-08-14 11:25:16.634004	f	t
1793	38	33	2017-08-04 11:25:16.634032	f	t
1794	38	34	2017-07-31 11:25:16.634061	f	t
1795	38	13	2017-08-15 11:25:16.63409	f	t
1796	38	10	2017-08-03 11:25:16.634119	f	t
1797	43	10	2017-07-29 11:25:16.634148	t	t
1798	43	31	2017-08-14 11:25:16.634177	t	t
1799	43	28	2017-08-19 11:25:16.634206	t	t
1800	43	12	2017-08-07 11:25:16.634234	t	t
1801	43	35	2017-08-16 11:25:16.634263	t	t
1802	43	14	2017-08-10 11:25:16.634292	f	t
1803	43	11	2017-08-01 11:25:16.634337	f	t
1804	43	16	2017-08-15 11:25:16.634379	f	t
1805	45	15	2017-08-07 11:25:16.634408	t	t
1806	45	24	2017-07-25 11:25:16.634437	t	t
1807	45	28	2017-08-07 11:25:16.634465	t	t
1808	45	23	2017-08-18 11:25:16.634493	t	t
1809	45	9	2017-08-02 11:25:16.634522	t	t
1810	45	27	2017-07-27 11:25:16.634551	t	t
1811	45	22	2017-08-01 11:25:16.634579	t	t
1812	45	8	2017-07-30 11:25:16.634608	t	t
1813	45	32	2017-07-28 11:25:16.634636	t	t
1814	45	19	2017-08-01 11:25:16.634664	t	t
1815	45	37	2017-08-01 11:25:16.634692	t	t
1816	45	29	2017-08-10 11:25:16.63472	t	t
1817	45	17	2017-07-29 11:25:16.634768	t	t
1818	45	11	2017-08-05 11:25:16.634798	t	t
1819	45	26	2017-07-25 11:25:16.634828	t	t
1820	45	13	2017-08-06 11:25:16.634857	t	t
1821	45	7	2017-08-09 11:25:16.634886	t	t
1822	45	18	2017-08-14 11:25:16.634914	t	t
1823	45	25	2017-07-27 11:25:16.634943	t	t
1824	45	22	2017-08-13 11:25:16.634971	f	t
1825	45	12	2017-08-09 11:25:16.634999	f	t
1826	45	13	2017-08-12 11:25:16.635027	f	t
1827	45	18	2017-07-28 11:25:16.635054	f	t
1828	45	29	2017-08-11 11:25:16.635083	f	t
1829	45	9	2017-08-06 11:25:16.635111	f	t
1830	48	33	2017-08-01 11:25:16.635139	t	t
1831	48	13	2017-08-10 11:25:16.635166	t	t
1832	48	10	2017-07-29 11:25:16.635194	t	t
1833	48	17	2017-08-10 11:25:16.635222	t	t
1834	48	14	2017-08-18 11:25:16.635249	t	t
1835	48	34	2017-08-09 11:25:16.635278	t	t
1836	48	24	2017-07-27 11:25:16.635307	t	t
1837	48	7	2017-08-18 11:25:16.635335	t	t
1838	48	9	2017-08-15 11:25:16.635363	t	t
1839	48	35	2017-07-30 11:25:16.635392	t	t
1840	48	19	2017-08-14 11:25:16.63542	t	t
1841	48	22	2017-07-31 11:25:16.635449	t	t
1842	48	37	2017-08-09 11:25:16.635478	t	t
1843	48	27	2017-07-31 11:25:16.635506	t	t
1844	48	15	2017-08-15 11:25:16.635535	t	t
1845	48	36	2017-08-03 11:25:16.635564	f	t
1846	48	23	2017-08-11 11:25:16.635592	f	t
1847	48	26	2017-08-08 11:25:16.63562	f	t
1848	48	13	2017-07-26 11:25:16.635649	f	t
1849	48	24	2017-08-10 11:25:16.635677	f	t
1850	48	10	2017-07-25 11:25:16.635706	f	t
1851	48	21	2017-07-25 11:25:16.635734	f	t
1852	48	28	2017-08-17 11:25:16.635763	f	t
1853	52	29	2017-08-05 11:25:16.635791	f	t
1854	52	24	2017-08-01 11:25:16.63582	f	t
1855	52	28	2017-07-27 11:25:16.635849	f	t
1856	52	11	2017-07-31 11:25:16.635877	f	t
1857	52	12	2017-08-01 11:25:16.635905	f	t
1858	52	18	2017-08-11 11:25:16.635934	f	t
1859	52	13	2017-07-25 11:25:16.635963	f	t
1860	52	33	2017-08-12 11:25:16.635991	f	t
1861	52	9	2017-07-31 11:25:16.636019	f	t
1862	52	36	2017-08-10 11:25:16.636047	f	t
1863	52	22	2017-07-31 11:25:16.636076	f	t
1864	52	8	2017-08-11 11:25:16.636105	f	t
1865	52	25	2017-08-06 11:25:16.636133	f	t
1866	52	26	2017-08-14 11:25:16.636161	f	t
1867	52	34	2017-08-19 11:25:16.63619	f	t
1868	52	17	2017-07-28 11:25:16.636218	f	t
1869	52	29	2017-07-25 11:25:16.636246	f	t
1870	53	19	2017-08-07 11:25:16.636275	t	t
1871	53	13	2017-07-27 11:25:16.636303	t	t
1872	53	31	2017-08-03 11:25:16.636331	t	t
1873	53	37	2017-08-06 11:25:16.636358	t	t
1874	53	17	2017-07-27 11:25:16.636387	f	t
1875	53	29	2017-07-29 11:25:16.636415	f	t
1876	53	32	2017-07-29 11:25:16.636443	f	t
1877	53	10	2017-08-12 11:25:16.636471	f	t
1878	53	23	2017-08-12 11:25:16.636499	f	t
1879	53	12	2017-07-28 11:25:16.636527	f	t
1880	53	21	2017-08-17 11:25:16.636556	f	t
1881	53	11	2017-08-13 11:25:16.636584	f	t
1882	69	21	2017-08-11 11:25:16.636613	t	t
1883	69	37	2017-08-02 11:25:16.636641	t	t
1884	69	29	2017-08-18 11:25:16.63667	f	t
1885	69	35	2017-07-30 11:25:16.636698	f	t
1886	69	15	2017-08-06 11:25:16.636726	f	t
1887	69	24	2017-08-19 11:25:16.636755	f	t
1888	69	26	2017-08-18 11:25:16.636783	f	t
1889	69	25	2017-08-04 11:25:16.636812	f	t
1890	69	16	2017-08-11 11:25:16.636841	f	t
1891	69	18	2017-08-18 11:25:16.636869	f	t
1892	69	19	2017-08-03 11:25:16.636897	f	t
\.


--
-- Name: clicked_arguments_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('clicked_arguments_uid_seq', 1892, true);


--
-- Data for Name: clicked_statements; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY clicked_statements (uid, statement_uid, author_uid, "timestamp", is_up_vote, is_valid) FROM stdin;
1313	1	10	2017-08-08 11:25:16.359903	t	t
1314	1	17	2017-08-09 11:25:16.360009	f	t
1315	1	32	2017-08-09 11:25:16.360048	f	t
1316	2	16	2017-07-30 11:25:16.360081	t	t
1317	2	17	2017-08-06 11:25:16.360112	t	t
1318	2	17	2017-07-27 11:25:16.360142	t	t
1319	2	12	2017-08-08 11:25:16.360171	t	t
1320	2	26	2017-08-03 11:25:16.3602	t	t
1321	2	25	2017-08-02 11:25:16.360229	t	t
1322	2	12	2017-08-15 11:25:16.360257	t	t
1323	2	26	2017-08-12 11:25:16.360286	t	t
1324	2	29	2017-08-01 11:25:16.360315	t	t
1325	2	21	2017-08-08 11:25:16.360343	t	t
1326	2	9	2017-08-14 11:25:16.360371	t	t
1327	2	32	2017-08-13 11:25:16.3604	t	t
1328	2	10	2017-08-07 11:25:16.360429	t	t
1329	2	35	2017-07-25 11:25:16.360457	t	t
1330	2	14	2017-08-07 11:25:16.360486	t	t
1331	2	18	2017-08-19 11:25:16.360514	t	t
1332	2	35	2017-08-15 11:25:16.360543	f	t
1333	2	31	2017-07-28 11:25:16.360572	f	t
1334	2	24	2017-07-27 11:25:16.3606	f	t
1335	2	22	2017-08-15 11:25:16.360629	f	t
1336	2	10	2017-08-01 11:25:16.360658	f	t
1337	2	18	2017-07-30 11:25:16.360687	f	t
1338	3	7	2017-08-05 11:25:16.360715	t	t
1339	4	22	2017-08-16 11:25:16.360744	t	t
1340	4	36	2017-08-06 11:25:16.360773	t	t
1341	4	11	2017-08-10 11:25:16.360801	t	t
1342	4	11	2017-08-18 11:25:16.360829	t	t
1343	4	12	2017-07-31 11:25:16.360858	t	t
1344	4	36	2017-08-02 11:25:16.360887	t	t
1345	4	28	2017-07-31 11:25:16.360915	t	t
1346	4	34	2017-08-09 11:25:16.360943	t	t
1347	4	35	2017-08-11 11:25:16.360972	t	t
1348	4	16	2017-07-29 11:25:16.361	t	t
1349	4	29	2017-08-02 11:25:16.361029	f	t
1350	4	35	2017-08-06 11:25:16.361057	f	t
1351	4	24	2017-08-10 11:25:16.361085	f	t
1352	4	29	2017-08-11 11:25:16.361113	f	t
1353	4	14	2017-07-26 11:25:16.361141	f	t
1354	4	13	2017-08-19 11:25:16.36117	f	t
1355	4	18	2017-07-26 11:25:16.361208	f	t
1356	4	17	2017-07-29 11:25:16.361237	f	t
1357	4	29	2017-08-10 11:25:16.361276	f	t
1358	4	31	2017-08-09 11:25:16.361304	f	t
1359	4	9	2017-08-02 11:25:16.361332	f	t
1360	4	15	2017-07-30 11:25:16.361359	f	t
1361	4	7	2017-08-11 11:25:16.361388	f	t
1362	4	20	2017-08-12 11:25:16.361416	f	t
1363	4	29	2017-07-29 11:25:16.361444	f	t
1364	4	19	2017-08-11 11:25:16.361472	f	t
1365	4	11	2017-08-02 11:25:16.3615	f	t
1366	4	9	2017-07-30 11:25:16.361528	f	t
1367	4	33	2017-08-07 11:25:16.361557	f	t
1368	4	36	2017-08-09 11:25:16.361588	f	t
1369	4	32	2017-08-18 11:25:16.361635	f	t
1370	4	29	2017-07-28 11:25:16.361698	f	t
1371	4	17	2017-07-27 11:25:16.361772	f	t
1372	4	24	2017-08-17 11:25:16.361809	f	t
1373	5	27	2017-07-30 11:25:16.361863	t	t
1374	5	35	2017-07-31 11:25:16.36191	t	t
1375	5	19	2017-08-19 11:25:16.36196	t	t
1376	5	11	2017-07-31 11:25:16.362013	t	t
1377	5	24	2017-08-19 11:25:16.362044	t	t
1378	5	29	2017-08-15 11:25:16.362073	t	t
1379	5	15	2017-07-31 11:25:16.362103	f	t
1380	6	36	2017-08-05 11:25:16.362132	t	t
1381	6	10	2017-07-27 11:25:16.362162	t	t
1382	6	28	2017-07-30 11:25:16.36219	t	t
1383	6	18	2017-07-30 11:25:16.36222	t	t
1384	6	20	2017-07-26 11:25:16.362249	t	t
1385	6	34	2017-08-09 11:25:16.362277	t	t
1386	6	29	2017-08-02 11:25:16.362306	f	t
1387	6	9	2017-08-07 11:25:16.362341	f	t
1388	6	8	2017-08-07 11:25:16.362371	f	t
1389	6	37	2017-08-01 11:25:16.3624	f	t
1390	6	23	2017-08-12 11:25:16.362429	f	t
1391	6	22	2017-08-08 11:25:16.362457	f	t
1392	6	18	2017-08-01 11:25:16.362486	f	t
1393	6	27	2017-08-05 11:25:16.362515	f	t
1394	6	8	2017-08-14 11:25:16.362544	f	t
1395	7	13	2017-07-26 11:25:16.362573	t	t
1396	7	22	2017-07-26 11:25:16.362601	t	t
1397	7	12	2017-08-18 11:25:16.362629	t	t
1398	7	34	2017-08-09 11:25:16.362658	t	t
1399	7	28	2017-08-01 11:25:16.362686	t	t
1400	7	36	2017-07-31 11:25:16.362714	t	t
1401	7	7	2017-08-15 11:25:16.362744	t	t
1402	7	16	2017-08-17 11:25:16.362773	t	t
1403	7	37	2017-07-28 11:25:16.362801	t	t
1404	8	9	2017-08-08 11:25:16.36283	t	t
1405	8	27	2017-08-15 11:25:16.362859	t	t
1406	8	15	2017-07-30 11:25:16.362888	t	t
1407	8	34	2017-08-15 11:25:16.362917	t	t
1408	8	13	2017-08-05 11:25:16.362946	t	t
1409	8	29	2017-08-14 11:25:16.362975	t	t
1410	8	16	2017-07-29 11:25:16.363004	t	t
1411	8	16	2017-08-13 11:25:16.363033	t	t
1412	8	19	2017-08-01 11:25:16.363062	t	t
1413	8	27	2017-08-06 11:25:16.363091	t	t
1414	8	7	2017-08-05 11:25:16.363119	t	t
1415	8	27	2017-07-30 11:25:16.363147	t	t
1416	8	18	2017-08-09 11:25:16.363176	f	t
1417	8	12	2017-07-31 11:25:16.363205	f	t
1418	8	37	2017-07-30 11:25:16.363234	f	t
1419	8	29	2017-08-19 11:25:16.363263	f	t
1420	8	16	2017-08-02 11:25:16.363292	f	t
1421	8	8	2017-07-31 11:25:16.36332	f	t
1422	8	24	2017-08-13 11:25:16.363349	f	t
1423	8	25	2017-07-29 11:25:16.363377	f	t
1424	8	37	2017-08-03 11:25:16.363406	f	t
1425	8	21	2017-08-03 11:25:16.363435	f	t
1426	9	25	2017-08-02 11:25:16.363463	t	t
1427	9	10	2017-08-16 11:25:16.363491	t	t
1428	9	15	2017-07-28 11:25:16.36352	t	t
1429	9	37	2017-08-06 11:25:16.363549	t	t
1430	9	7	2017-08-11 11:25:16.363578	t	t
1431	9	12	2017-08-08 11:25:16.363606	t	t
1432	9	15	2017-08-16 11:25:16.363635	t	t
1433	9	19	2017-08-17 11:25:16.363664	t	t
1434	9	12	2017-08-12 11:25:16.363693	t	t
1435	9	37	2017-08-19 11:25:16.363721	t	t
1436	9	15	2017-08-08 11:25:16.36375	t	t
1437	9	12	2017-08-13 11:25:16.363778	t	t
1438	9	35	2017-08-13 11:25:16.363807	t	t
1439	9	32	2017-08-08 11:25:16.363835	t	t
1440	9	16	2017-08-13 11:25:16.363864	t	t
1441	9	13	2017-08-12 11:25:16.363892	t	t
1442	9	7	2017-08-11 11:25:16.36392	t	t
1443	9	32	2017-07-31 11:25:16.363949	t	t
1444	9	32	2017-07-27 11:25:16.363977	t	t
1445	9	15	2017-08-06 11:25:16.364006	t	t
1446	9	11	2017-07-27 11:25:16.364034	t	t
1447	9	9	2017-08-10 11:25:16.364063	t	t
1448	9	21	2017-08-05 11:25:16.364091	t	t
1449	9	27	2017-07-26 11:25:16.36412	f	t
1450	9	15	2017-07-27 11:25:16.364148	f	t
1451	9	24	2017-08-19 11:25:16.364176	f	t
1452	9	31	2017-08-17 11:25:16.364205	f	t
1453	9	12	2017-08-11 11:25:16.364233	f	t
1454	9	14	2017-08-05 11:25:16.364262	f	t
1455	9	21	2017-08-07 11:25:16.364291	f	t
1456	9	31	2017-08-03 11:25:16.36432	f	t
1457	9	22	2017-08-15 11:25:16.364348	f	t
1458	9	28	2017-08-17 11:25:16.364378	f	t
1459	9	10	2017-08-07 11:25:16.364406	f	t
1460	9	7	2017-08-10 11:25:16.364435	f	t
1461	9	31	2017-08-16 11:25:16.364463	f	t
1462	10	14	2017-08-15 11:25:16.364492	t	t
1463	10	36	2017-08-12 11:25:16.364521	t	t
1464	10	29	2017-08-08 11:25:16.36455	t	t
1465	10	29	2017-08-13 11:25:16.364578	t	t
1466	10	19	2017-08-09 11:25:16.364607	t	t
1467	10	8	2017-08-15 11:25:16.364636	t	t
1468	10	28	2017-08-17 11:25:16.364665	t	t
1469	10	29	2017-08-18 11:25:16.364694	t	t
1470	10	10	2017-08-18 11:25:16.364722	t	t
1471	10	29	2017-07-26 11:25:16.364751	t	t
1472	10	20	2017-08-14 11:25:16.36478	f	t
1473	10	18	2017-08-19 11:25:16.364808	f	t
1474	10	15	2017-08-11 11:25:16.364837	f	t
1475	10	16	2017-07-29 11:25:16.364865	f	t
1476	10	12	2017-08-17 11:25:16.364893	f	t
1477	10	16	2017-08-11 11:25:16.364922	f	t
1478	10	28	2017-08-04 11:25:16.36495	f	t
1479	10	28	2017-07-26 11:25:16.364978	f	t
1480	10	24	2017-08-01 11:25:16.365007	f	t
1481	10	21	2017-08-15 11:25:16.365035	f	t
1482	11	20	2017-08-13 11:25:16.365064	t	t
1483	11	16	2017-08-12 11:25:16.365093	t	t
1484	11	19	2017-08-11 11:25:16.365121	f	t
1485	11	23	2017-08-16 11:25:16.365149	f	t
1486	11	8	2017-08-06 11:25:16.365178	f	t
1487	12	7	2017-07-25 11:25:16.365206	t	t
1488	13	31	2017-08-08 11:25:16.365234	t	t
1489	13	15	2017-08-13 11:25:16.365262	t	t
1490	13	23	2017-08-19 11:25:16.36529	t	t
1491	13	29	2017-08-07 11:25:16.365319	t	t
1492	13	16	2017-08-11 11:25:16.365347	t	t
1493	13	10	2017-07-28 11:25:16.365376	f	t
1494	13	19	2017-08-12 11:25:16.365405	f	t
1495	13	29	2017-07-30 11:25:16.365433	f	t
1496	14	24	2017-08-01 11:25:16.365462	t	t
1497	14	16	2017-08-03 11:25:16.36549	t	t
1498	14	36	2017-08-02 11:25:16.365518	t	t
1499	14	7	2017-08-13 11:25:16.365547	t	t
1500	14	24	2017-08-16 11:25:16.365575	t	t
1501	14	36	2017-08-19 11:25:16.365603	t	t
1502	15	14	2017-08-19 11:25:16.365632	t	t
1503	15	7	2017-08-01 11:25:16.365661	t	t
1504	15	27	2017-08-12 11:25:16.365689	t	t
1505	15	12	2017-07-29 11:25:16.365718	t	t
1506	15	16	2017-08-09 11:25:16.365746	f	t
1507	16	8	2017-08-13 11:25:16.365774	t	t
1508	16	11	2017-07-25 11:25:16.365803	t	t
1509	16	13	2017-08-02 11:25:16.365831	t	t
1510	16	33	2017-08-18 11:25:16.365859	t	t
1511	16	34	2017-08-01 11:25:16.365888	t	t
1512	16	34	2017-08-01 11:25:16.365916	t	t
1513	16	19	2017-08-14 11:25:16.365944	t	t
1514	16	19	2017-07-27 11:25:16.365972	t	t
1515	16	33	2017-07-25 11:25:16.366	t	t
1516	16	29	2017-08-03 11:25:16.366028	t	t
1517	16	25	2017-08-14 11:25:16.366056	t	t
1518	16	29	2017-08-18 11:25:16.366085	t	t
1519	16	32	2017-08-18 11:25:16.366113	t	t
1520	16	12	2017-08-01 11:25:16.366141	t	t
1521	16	29	2017-08-15 11:25:16.36617	t	t
1522	16	15	2017-07-29 11:25:16.366198	t	t
1523	16	8	2017-08-11 11:25:16.366226	f	t
1524	16	35	2017-08-03 11:25:16.366255	f	t
1525	16	26	2017-08-07 11:25:16.366283	f	t
1526	16	19	2017-07-29 11:25:16.366311	f	t
1527	16	12	2017-07-29 11:25:16.366344	f	t
1528	16	28	2017-08-17 11:25:16.366373	f	t
1529	16	27	2017-07-31 11:25:16.366402	f	t
1530	16	15	2017-08-01 11:25:16.36643	f	t
1531	16	24	2017-08-07 11:25:16.366458	f	t
1532	16	32	2017-07-30 11:25:16.366487	f	t
1533	16	33	2017-08-19 11:25:16.366515	f	t
1534	16	12	2017-08-01 11:25:16.366544	f	t
1535	17	20	2017-08-10 11:25:16.366572	t	t
1536	17	16	2017-08-03 11:25:16.366601	t	t
1537	17	12	2017-08-07 11:25:16.366629	t	t
1538	17	28	2017-08-12 11:25:16.366658	t	t
1539	17	22	2017-08-14 11:25:16.366687	t	t
1540	17	34	2017-08-10 11:25:16.366716	t	t
1541	17	12	2017-07-29 11:25:16.366744	t	t
1542	17	10	2017-08-08 11:25:16.366773	t	t
1543	17	18	2017-07-31 11:25:16.366801	t	t
1544	17	29	2017-08-13 11:25:16.366829	t	t
1545	17	21	2017-08-14 11:25:16.366858	t	t
1546	17	29	2017-08-08 11:25:16.366886	t	t
1547	17	29	2017-08-05 11:25:16.366915	t	t
1548	17	21	2017-08-15 11:25:16.366943	t	t
1549	17	27	2017-08-10 11:25:16.366972	t	t
1550	17	34	2017-08-08 11:25:16.367	t	t
1551	17	27	2017-08-08 11:25:16.367028	t	t
1552	17	12	2017-08-12 11:25:16.367057	f	t
1553	17	22	2017-07-30 11:25:16.367085	f	t
1554	17	10	2017-08-11 11:25:16.367113	f	t
1555	17	25	2017-07-30 11:25:16.367142	f	t
1556	17	18	2017-07-31 11:25:16.36717	f	t
1557	17	17	2017-07-31 11:25:16.367198	f	t
1558	17	7	2017-08-05 11:25:16.367227	f	t
1559	17	29	2017-08-01 11:25:16.367254	f	t
1560	17	14	2017-08-05 11:25:16.367282	f	t
1561	17	28	2017-08-16 11:25:16.36731	f	t
1562	17	27	2017-08-11 11:25:16.367357	f	t
1563	17	17	2017-08-06 11:25:16.367386	f	t
1564	17	29	2017-07-28 11:25:16.367414	f	t
1565	17	37	2017-08-19 11:25:16.367442	f	t
1566	17	25	2017-08-07 11:25:16.367471	f	t
1567	18	22	2017-08-13 11:25:16.367499	t	t
1568	18	29	2017-08-11 11:25:16.367528	t	t
1569	18	22	2017-07-30 11:25:16.367556	t	t
1570	18	8	2017-08-14 11:25:16.367584	t	t
1571	18	21	2017-07-26 11:25:16.367613	t	t
1572	18	33	2017-08-12 11:25:16.367641	t	t
1573	18	8	2017-08-16 11:25:16.367669	t	t
1574	18	17	2017-08-06 11:25:16.367697	f	t
1575	18	15	2017-08-11 11:25:16.367724	f	t
1576	19	22	2017-08-08 11:25:16.367752	t	t
1577	19	16	2017-07-29 11:25:16.36778	t	t
1578	19	37	2017-08-14 11:25:16.367808	t	t
1579	19	27	2017-08-11 11:25:16.367837	f	t
1580	20	24	2017-08-07 11:25:16.367865	f	t
1581	20	13	2017-08-02 11:25:16.367894	f	t
1582	20	25	2017-07-26 11:25:16.367922	f	t
1583	20	29	2017-07-31 11:25:16.36795	f	t
1584	20	20	2017-07-26 11:25:16.367978	f	t
1585	20	21	2017-08-02 11:25:16.368007	f	t
1586	20	10	2017-08-06 11:25:16.368035	f	t
1587	20	23	2017-07-29 11:25:16.368064	f	t
1588	21	34	2017-08-14 11:25:16.368092	t	t
1589	21	29	2017-07-30 11:25:16.36812	t	t
1590	21	13	2017-08-02 11:25:16.368148	t	t
1591	22	37	2017-08-14 11:25:16.368176	t	t
1592	22	19	2017-08-17 11:25:16.368205	t	t
1593	22	21	2017-07-27 11:25:16.368233	t	t
1594	22	18	2017-08-15 11:25:16.368262	t	t
1595	22	27	2017-08-11 11:25:16.36829	t	t
1596	22	27	2017-07-31 11:25:16.368319	t	t
1597	22	18	2017-07-26 11:25:16.368347	t	t
1598	22	20	2017-08-15 11:25:16.368376	t	t
1599	22	7	2017-07-29 11:25:16.368405	f	t
1600	22	7	2017-08-17 11:25:16.368433	f	t
1601	22	11	2017-08-19 11:25:16.368462	f	t
1602	22	7	2017-08-14 11:25:16.36849	f	t
1603	22	9	2017-08-08 11:25:16.368518	f	t
1604	22	9	2017-08-04 11:25:16.368546	f	t
1605	22	22	2017-08-11 11:25:16.368575	f	t
1606	22	13	2017-07-26 11:25:16.368603	f	t
1607	22	11	2017-08-06 11:25:16.368631	f	t
1608	22	20	2017-08-17 11:25:16.368659	f	t
1609	22	28	2017-08-12 11:25:16.368688	f	t
1610	23	20	2017-08-06 11:25:16.368716	t	t
1611	23	11	2017-08-05 11:25:16.368744	t	t
1612	23	35	2017-08-17 11:25:16.368774	t	t
1613	23	10	2017-08-07 11:25:16.368803	t	t
1614	23	32	2017-08-11 11:25:16.368831	t	t
1615	23	21	2017-08-11 11:25:16.36886	t	t
1616	23	35	2017-07-30 11:25:16.368888	t	t
1617	23	23	2017-08-17 11:25:16.368916	t	t
1618	23	17	2017-08-18 11:25:16.368945	t	t
1619	23	32	2017-08-01 11:25:16.368973	t	t
1620	23	35	2017-08-05 11:25:16.369002	t	t
1621	23	17	2017-08-05 11:25:16.36903	t	t
1622	23	26	2017-08-17 11:25:16.369059	t	t
1623	23	25	2017-08-18 11:25:16.369088	t	t
1624	23	17	2017-07-28 11:25:16.369116	t	t
1625	23	18	2017-08-11 11:25:16.369145	t	t
1626	23	11	2017-08-13 11:25:16.369174	t	t
1627	23	26	2017-08-19 11:25:16.369202	t	t
1628	23	9	2017-08-16 11:25:16.36923	t	t
1629	23	13	2017-08-16 11:25:16.369258	t	t
1630	23	37	2017-08-02 11:25:16.369287	t	t
1631	23	12	2017-08-17 11:25:16.369315	f	t
1632	23	10	2017-08-18 11:25:16.369343	f	t
1633	23	10	2017-08-07 11:25:16.369372	f	t
1634	23	37	2017-08-05 11:25:16.3694	f	t
1635	24	13	2017-07-30 11:25:16.369429	t	t
1636	24	10	2017-08-12 11:25:16.369457	t	t
1637	24	12	2017-08-08 11:25:16.369486	t	t
1638	24	11	2017-08-16 11:25:16.369515	t	t
1639	24	8	2017-08-02 11:25:16.369543	t	t
1640	24	18	2017-08-14 11:25:16.369571	t	t
1641	24	36	2017-08-12 11:25:16.3696	t	t
1642	24	23	2017-08-09 11:25:16.369628	t	t
1643	24	26	2017-08-08 11:25:16.369656	t	t
1644	24	29	2017-08-13 11:25:16.369685	t	t
1645	24	37	2017-08-17 11:25:16.369713	t	t
1646	24	7	2017-08-04 11:25:16.369742	t	t
1647	24	11	2017-08-08 11:25:16.36977	t	t
1648	24	25	2017-08-13 11:25:16.369799	t	t
1649	24	22	2017-07-25 11:25:16.369827	t	t
1650	24	16	2017-08-19 11:25:16.369856	t	t
1651	24	8	2017-07-29 11:25:16.369885	t	t
1652	24	23	2017-08-03 11:25:16.369913	t	t
1653	24	9	2017-08-14 11:25:16.369941	f	t
1654	24	17	2017-07-27 11:25:16.369969	f	t
1655	24	13	2017-08-17 11:25:16.369997	f	t
1656	24	24	2017-07-25 11:25:16.370026	f	t
1657	24	21	2017-08-14 11:25:16.370055	f	t
1658	24	18	2017-08-15 11:25:16.370083	f	t
1659	24	15	2017-08-11 11:25:16.370112	f	t
1660	24	10	2017-08-08 11:25:16.37014	f	t
1661	24	11	2017-08-17 11:25:16.370168	f	t
1662	24	32	2017-08-13 11:25:16.370196	f	t
1663	24	10	2017-08-04 11:25:16.370224	f	t
1664	24	18	2017-08-02 11:25:16.370253	f	t
1665	24	7	2017-08-15 11:25:16.370293	f	t
1666	24	24	2017-08-06 11:25:16.370347	f	t
1667	24	14	2017-08-01 11:25:16.370377	f	t
1668	24	10	2017-08-08 11:25:16.370416	f	t
1669	24	32	2017-08-18 11:25:16.370444	f	t
1670	24	35	2017-07-30 11:25:16.370472	f	t
1671	24	25	2017-07-26 11:25:16.370501	f	t
1672	24	19	2017-08-12 11:25:16.37053	f	t
1673	24	11	2017-08-13 11:25:16.370559	f	t
1674	24	33	2017-08-11 11:25:16.370587	f	t
1675	24	32	2017-07-27 11:25:16.370615	f	t
1676	25	25	2017-07-30 11:25:16.370643	t	t
1677	25	25	2017-08-01 11:25:16.370672	f	t
1678	25	32	2017-08-13 11:25:16.3707	f	t
1679	25	29	2017-08-08 11:25:16.370729	f	t
1680	25	15	2017-08-06 11:25:16.370757	f	t
1681	25	35	2017-07-28 11:25:16.370786	f	t
1682	25	29	2017-08-10 11:25:16.370814	f	t
1683	25	21	2017-08-03 11:25:16.370842	f	t
1684	26	19	2017-07-29 11:25:16.370871	t	t
1685	26	26	2017-08-06 11:25:16.370899	f	t
1686	26	19	2017-08-09 11:25:16.370927	f	t
1687	27	16	2017-07-30 11:25:16.370956	f	t
1688	28	9	2017-08-13 11:25:16.370984	t	t
1689	28	35	2017-07-30 11:25:16.371013	t	t
1690	28	7	2017-08-17 11:25:16.371041	t	t
1691	28	29	2017-08-18 11:25:16.37107	f	t
1692	28	34	2017-08-06 11:25:16.371099	f	t
1693	28	25	2017-08-02 11:25:16.371127	f	t
1694	28	35	2017-07-29 11:25:16.371155	f	t
1695	28	7	2017-08-14 11:25:16.371183	f	t
1696	28	13	2017-08-19 11:25:16.371212	f	t
1697	28	36	2017-07-26 11:25:16.37124	f	t
1698	28	7	2017-07-26 11:25:16.371268	f	t
1699	28	17	2017-08-03 11:25:16.371296	f	t
1700	29	17	2017-08-04 11:25:16.371324	f	t
1701	30	22	2017-08-15 11:25:16.371353	t	t
1702	30	9	2017-07-30 11:25:16.371381	t	t
1703	30	13	2017-08-11 11:25:16.371409	t	t
1704	30	37	2017-08-01 11:25:16.371437	t	t
1705	30	7	2017-07-29 11:25:16.371466	t	t
1706	30	19	2017-08-09 11:25:16.371494	t	t
1707	30	32	2017-07-26 11:25:16.371524	t	t
1708	30	35	2017-08-13 11:25:16.371552	t	t
1709	30	8	2017-08-01 11:25:16.371581	t	t
1710	30	35	2017-07-27 11:25:16.37161	t	t
1711	30	21	2017-08-06 11:25:16.371639	f	t
1712	30	23	2017-08-01 11:25:16.371668	f	t
1713	30	13	2017-08-19 11:25:16.371696	f	t
1714	30	22	2017-08-10 11:25:16.371725	f	t
1715	30	15	2017-08-08 11:25:16.371753	f	t
1716	30	29	2017-08-19 11:25:16.371782	f	t
1717	30	8	2017-08-02 11:25:16.371811	f	t
1718	30	33	2017-08-02 11:25:16.371839	f	t
1719	30	27	2017-08-01 11:25:16.371868	f	t
1720	30	37	2017-07-27 11:25:16.371896	f	t
1721	30	33	2017-08-03 11:25:16.371924	f	t
1722	30	19	2017-07-29 11:25:16.371952	f	t
1723	30	32	2017-08-07 11:25:16.37198	f	t
1724	30	7	2017-08-19 11:25:16.372009	f	t
1725	31	27	2017-08-04 11:25:16.372039	t	t
1726	31	20	2017-08-15 11:25:16.372067	t	t
1727	31	34	2017-07-29 11:25:16.372096	t	t
1728	31	7	2017-07-31 11:25:16.372124	t	t
1729	31	17	2017-08-06 11:25:16.372153	t	t
1730	32	34	2017-08-05 11:25:16.372181	t	t
1731	32	20	2017-08-05 11:25:16.372209	t	t
1732	32	13	2017-08-10 11:25:16.372237	t	t
1733	32	17	2017-08-10 11:25:16.372266	t	t
1734	32	36	2017-08-05 11:25:16.372294	t	t
1735	32	21	2017-08-03 11:25:16.372322	t	t
1736	32	26	2017-08-07 11:25:16.372351	t	t
1737	32	17	2017-08-10 11:25:16.37238	t	t
1738	32	16	2017-07-27 11:25:16.372408	t	t
1739	32	36	2017-08-12 11:25:16.372437	t	t
1740	32	29	2017-07-25 11:25:16.372465	t	t
1741	32	25	2017-08-05 11:25:16.372494	t	t
1742	32	8	2017-07-31 11:25:16.372523	t	t
1743	32	20	2017-08-13 11:25:16.372562	t	t
1744	32	28	2017-07-31 11:25:16.372591	t	t
1745	32	14	2017-08-03 11:25:16.372631	t	t
1746	32	13	2017-08-18 11:25:16.372682	t	t
1747	32	14	2017-07-26 11:25:16.37273	t	t
1748	32	29	2017-07-29 11:25:16.372758	t	t
1749	32	20	2017-07-26 11:25:16.372786	t	t
1750	32	22	2017-07-31 11:25:16.372815	t	t
1751	32	26	2017-07-29 11:25:16.372843	t	t
1752	32	22	2017-08-03 11:25:16.372871	f	t
1753	32	37	2017-08-02 11:25:16.3729	f	t
1754	32	25	2017-08-01 11:25:16.372928	f	t
1755	32	16	2017-08-09 11:25:16.372957	f	t
1756	32	28	2017-08-14 11:25:16.372987	f	t
1757	32	19	2017-08-14 11:25:16.373015	f	t
1758	32	26	2017-08-08 11:25:16.373044	f	t
1759	32	24	2017-07-27 11:25:16.373072	f	t
1760	32	17	2017-07-31 11:25:16.373101	f	t
1761	32	12	2017-07-28 11:25:16.373129	f	t
1762	32	34	2017-08-03 11:25:16.373158	f	t
1763	32	14	2017-08-11 11:25:16.373185	f	t
1764	32	23	2017-08-18 11:25:16.373214	f	t
1765	32	31	2017-08-18 11:25:16.373243	f	t
1766	32	11	2017-07-30 11:25:16.373271	f	t
1767	33	36	2017-08-06 11:25:16.3733	t	t
1768	33	29	2017-07-31 11:25:16.373328	t	t
1769	33	34	2017-08-02 11:25:16.373356	t	t
1770	33	20	2017-07-31 11:25:16.373384	t	t
1771	33	31	2017-08-11 11:25:16.373412	t	t
1772	33	36	2017-08-17 11:25:16.37344	f	t
1773	33	34	2017-08-07 11:25:16.373469	f	t
1774	33	17	2017-08-19 11:25:16.373497	f	t
1775	33	35	2017-08-08 11:25:16.373526	f	t
1776	33	19	2017-08-19 11:25:16.373554	f	t
1777	34	29	2017-07-25 11:25:16.373582	t	t
1778	34	29	2017-08-12 11:25:16.37361	f	t
1779	35	31	2017-08-07 11:25:16.373638	f	t
1780	35	8	2017-08-17 11:25:16.373667	f	t
1781	35	23	2017-08-09 11:25:16.373695	f	t
1782	35	36	2017-08-13 11:25:16.373723	f	t
1783	35	27	2017-08-14 11:25:16.373751	f	t
1784	35	31	2017-08-05 11:25:16.37378	f	t
1785	36	21	2017-07-30 11:25:16.373809	f	t
1786	36	37	2017-08-11 11:25:16.373837	f	t
1787	37	17	2017-08-02 11:25:16.373865	t	t
1788	37	19	2017-08-10 11:25:16.373893	t	t
1789	37	27	2017-08-18 11:25:16.373921	t	t
1790	37	8	2017-08-10 11:25:16.373949	t	t
1791	38	35	2017-08-01 11:25:16.373977	t	t
1792	38	33	2017-07-26 11:25:16.374005	t	t
1793	38	34	2017-08-19 11:25:16.374033	t	t
1794	38	22	2017-07-29 11:25:16.374062	t	t
1795	38	27	2017-07-27 11:25:16.374106	t	t
1796	38	11	2017-07-28 11:25:16.374134	t	t
1797	38	27	2017-08-04 11:25:16.374163	t	t
1798	38	21	2017-08-17 11:25:16.374191	t	t
1799	38	23	2017-08-16 11:25:16.37422	f	t
1800	38	14	2017-08-08 11:25:16.374249	f	t
1801	38	14	2017-08-11 11:25:16.374277	f	t
1802	38	22	2017-08-06 11:25:16.374305	f	t
1803	38	32	2017-08-15 11:25:16.374337	f	t
1804	38	10	2017-08-09 11:25:16.374365	f	t
1805	39	8	2017-08-06 11:25:16.374393	t	t
1806	39	17	2017-08-10 11:25:16.374421	t	t
1807	39	15	2017-08-03 11:25:16.374449	t	t
1808	39	21	2017-08-05 11:25:16.374477	f	t
1809	39	24	2017-08-02 11:25:16.374505	f	t
1810	39	28	2017-07-31 11:25:16.374534	f	t
1811	39	19	2017-07-27 11:25:16.374562	f	t
1812	39	10	2017-08-07 11:25:16.374591	f	t
1813	39	21	2017-08-16 11:25:16.374619	f	t
1814	39	25	2017-08-08 11:25:16.374649	f	t
1815	39	21	2017-07-26 11:25:16.374677	f	t
1816	39	34	2017-08-07 11:25:16.374705	f	t
1817	39	35	2017-08-12 11:25:16.374733	f	t
1818	40	14	2017-08-04 11:25:16.374761	t	t
1819	40	19	2017-08-14 11:25:16.37479	t	t
1820	40	31	2017-08-06 11:25:16.374818	t	t
1821	40	36	2017-08-03 11:25:16.374846	t	t
1822	40	17	2017-08-07 11:25:16.374874	t	t
1823	40	21	2017-07-27 11:25:16.374902	t	t
1824	40	25	2017-07-29 11:25:16.37493	t	t
1825	40	32	2017-08-12 11:25:16.374958	t	t
1826	40	20	2017-08-02 11:25:16.374985	t	t
1827	40	22	2017-08-06 11:25:16.375013	t	t
1828	40	34	2017-08-19 11:25:16.375041	t	t
1829	40	15	2017-07-29 11:25:16.375069	t	t
1830	40	29	2017-08-11 11:25:16.375097	t	t
1831	40	32	2017-07-30 11:25:16.375125	t	t
1832	40	7	2017-08-10 11:25:16.375153	t	t
1833	40	15	2017-07-26 11:25:16.37518	t	t
1834	40	13	2017-08-13 11:25:16.375208	t	t
1835	40	37	2017-08-12 11:25:16.375237	t	t
1836	40	22	2017-08-06 11:25:16.375264	t	t
1837	40	23	2017-08-17 11:25:16.375292	t	t
1838	40	24	2017-07-27 11:25:16.37532	t	t
1839	40	19	2017-08-01 11:25:16.375348	t	t
1840	40	32	2017-08-08 11:25:16.375376	t	t
1841	40	34	2017-08-19 11:25:16.375404	t	t
1842	40	22	2017-07-25 11:25:16.375432	f	t
1843	40	24	2017-07-30 11:25:16.375461	f	t
1844	40	15	2017-07-27 11:25:16.375489	f	t
1845	40	35	2017-08-08 11:25:16.375517	f	t
1846	40	21	2017-08-03 11:25:16.375545	f	t
1847	40	20	2017-08-13 11:25:16.375573	f	t
1848	40	11	2017-08-07 11:25:16.375601	f	t
1849	40	11	2017-08-07 11:25:16.37563	f	t
1850	40	29	2017-08-16 11:25:16.375658	f	t
1851	40	7	2017-08-10 11:25:16.375686	f	t
1852	40	28	2017-08-04 11:25:16.375714	f	t
1853	40	21	2017-07-28 11:25:16.375743	f	t
1854	40	20	2017-08-10 11:25:16.375771	f	t
1855	40	14	2017-08-05 11:25:16.375799	f	t
1856	40	31	2017-08-11 11:25:16.375827	f	t
1857	40	18	2017-08-18 11:25:16.375855	f	t
1858	40	25	2017-08-01 11:25:16.375883	f	t
1859	40	19	2017-07-27 11:25:16.37591	f	t
1860	40	9	2017-08-08 11:25:16.375938	f	t
1861	40	28	2017-08-15 11:25:16.375966	f	t
1862	42	8	2017-08-10 11:25:16.375994	t	t
1863	42	15	2017-07-27 11:25:16.376022	t	t
1864	42	23	2017-08-04 11:25:16.37605	t	t
1865	42	11	2017-08-12 11:25:16.376078	t	t
1866	42	36	2017-08-18 11:25:16.376106	t	t
1867	42	16	2017-08-19 11:25:16.376134	t	t
1868	42	18	2017-07-31 11:25:16.376162	t	t
1869	42	13	2017-07-31 11:25:16.37619	t	t
1870	42	34	2017-08-09 11:25:16.376217	t	t
1871	42	21	2017-08-16 11:25:16.376246	t	t
1872	42	16	2017-07-30 11:25:16.376273	t	t
1873	42	35	2017-07-29 11:25:16.376301	t	t
1874	42	21	2017-08-02 11:25:16.376329	t	t
1875	42	29	2017-07-28 11:25:16.376357	t	t
1876	42	15	2017-08-01 11:25:16.376385	t	t
1877	42	29	2017-08-16 11:25:16.376412	t	t
1878	42	29	2017-08-17 11:25:16.37644	t	t
1879	42	37	2017-08-09 11:25:16.376469	t	t
1880	42	13	2017-08-15 11:25:16.376497	t	t
1881	43	23	2017-08-09 11:25:16.376525	t	t
1882	43	8	2017-08-14 11:25:16.376553	t	t
1883	43	21	2017-08-11 11:25:16.376581	t	t
1884	43	29	2017-07-31 11:25:16.376609	t	t
1885	43	28	2017-07-31 11:25:16.376637	t	t
1886	43	27	2017-08-14 11:25:16.376664	t	t
1887	43	23	2017-08-09 11:25:16.376692	t	t
1888	43	15	2017-08-12 11:25:16.37672	t	t
1889	43	20	2017-07-28 11:25:16.376747	t	t
1890	43	33	2017-08-14 11:25:16.376775	t	t
1891	43	9	2017-07-28 11:25:16.376803	t	t
1892	43	37	2017-07-29 11:25:16.376831	t	t
1893	43	20	2017-07-29 11:25:16.376859	t	t
1894	43	18	2017-08-04 11:25:16.376887	t	t
1895	43	31	2017-08-07 11:25:16.376915	t	t
1896	43	14	2017-08-11 11:25:16.376943	t	t
1897	43	13	2017-08-06 11:25:16.376972	t	t
1898	43	20	2017-07-26 11:25:16.376999	t	t
1899	43	32	2017-08-01 11:25:16.377027	t	t
1900	43	11	2017-07-28 11:25:16.377055	t	t
1901	43	27	2017-08-16 11:25:16.377083	t	t
1902	43	11	2017-07-27 11:25:16.377112	f	t
1903	43	29	2017-07-29 11:25:16.37714	f	t
1904	43	19	2017-08-01 11:25:16.377168	f	t
1905	43	25	2017-07-25 11:25:16.377196	f	t
1906	43	19	2017-07-25 11:25:16.377224	f	t
1907	43	12	2017-08-06 11:25:16.377252	f	t
1908	44	23	2017-07-25 11:25:16.37728	t	t
1909	44	29	2017-08-02 11:25:16.377308	t	t
1910	44	23	2017-07-31 11:25:16.377336	t	t
1911	44	16	2017-08-09 11:25:16.377364	t	t
1912	44	19	2017-08-11 11:25:16.377393	t	t
1913	44	31	2017-07-30 11:25:16.37742	t	t
1914	44	15	2017-08-02 11:25:16.377449	t	t
1915	44	26	2017-08-17 11:25:16.377477	f	t
1916	44	21	2017-08-12 11:25:16.377506	f	t
1917	44	33	2017-08-18 11:25:16.377534	f	t
1918	44	25	2017-08-10 11:25:16.377563	f	t
1919	44	35	2017-08-13 11:25:16.377591	f	t
1920	44	27	2017-08-15 11:25:16.377619	f	t
1921	45	27	2017-08-06 11:25:16.377648	t	t
1922	45	18	2017-08-19 11:25:16.377676	t	t
1923	45	17	2017-07-28 11:25:16.377726	t	t
1924	45	31	2017-08-12 11:25:16.377757	t	t
1925	45	25	2017-08-17 11:25:16.377796	t	t
1926	45	32	2017-08-12 11:25:16.377825	t	t
1927	45	18	2017-07-25 11:25:16.377854	t	t
1928	45	34	2017-08-06 11:25:16.377892	t	t
1929	45	12	2017-07-31 11:25:16.37792	t	t
1930	45	11	2017-08-14 11:25:16.377949	t	t
1931	45	19	2017-08-07 11:25:16.377978	f	t
1932	45	17	2017-07-26 11:25:16.378007	f	t
1933	45	9	2017-08-12 11:25:16.378037	f	t
1934	45	20	2017-07-25 11:25:16.378104	f	t
1935	45	11	2017-08-06 11:25:16.378175	f	t
1936	45	11	2017-08-04 11:25:16.378235	f	t
1937	45	17	2017-08-01 11:25:16.378304	f	t
1938	45	9	2017-08-01 11:25:16.378345	f	t
1939	45	8	2017-08-03 11:25:16.378375	f	t
1940	45	33	2017-08-15 11:25:16.378405	f	t
1941	45	35	2017-08-12 11:25:16.378434	f	t
1942	45	25	2017-08-09 11:25:16.378463	f	t
1943	45	23	2017-07-25 11:25:16.378492	f	t
1944	45	10	2017-08-05 11:25:16.37852	f	t
1945	45	28	2017-07-28 11:25:16.378549	f	t
1946	45	24	2017-08-09 11:25:16.378578	f	t
1947	45	29	2017-08-06 11:25:16.378606	f	t
1948	46	35	2017-08-15 11:25:16.378635	t	t
1949	46	18	2017-07-30 11:25:16.378664	t	t
1950	46	21	2017-07-30 11:25:16.378692	t	t
1951	46	28	2017-07-31 11:25:16.378721	t	t
1952	46	11	2017-08-10 11:25:16.37875	t	t
1953	46	12	2017-08-19 11:25:16.378778	t	t
1954	46	36	2017-08-05 11:25:16.378807	t	t
1955	46	7	2017-07-27 11:25:16.378835	t	t
1956	46	27	2017-07-27 11:25:16.378863	t	t
1957	46	18	2017-08-09 11:25:16.378892	t	t
1958	46	8	2017-07-31 11:25:16.37892	t	t
1959	46	10	2017-08-04 11:25:16.378948	t	t
1960	46	27	2017-07-31 11:25:16.378977	f	t
1961	46	8	2017-08-06 11:25:16.379005	f	t
1962	46	24	2017-07-25 11:25:16.379034	f	t
1963	47	32	2017-07-27 11:25:16.379062	t	t
1964	47	13	2017-08-08 11:25:16.37909	t	t
1965	47	20	2017-07-31 11:25:16.37913	f	t
1966	47	37	2017-08-18 11:25:16.379168	f	t
1967	48	13	2017-07-29 11:25:16.379197	t	t
1968	48	28	2017-08-02 11:25:16.379225	t	t
1969	48	34	2017-08-09 11:25:16.379254	t	t
1970	48	29	2017-08-04 11:25:16.379282	t	t
1971	48	26	2017-08-08 11:25:16.37931	t	t
1972	48	33	2017-08-15 11:25:16.379338	t	t
1973	48	18	2017-08-18 11:25:16.379366	t	t
1974	48	29	2017-08-17 11:25:16.379394	t	t
1975	48	10	2017-08-14 11:25:16.379423	t	t
1976	48	21	2017-08-14 11:25:16.379451	t	t
1977	48	33	2017-08-03 11:25:16.379478	t	t
1978	48	23	2017-08-19 11:25:16.379507	t	t
1979	48	28	2017-07-25 11:25:16.379535	t	t
1980	48	16	2017-07-29 11:25:16.379564	t	t
1981	48	21	2017-08-10 11:25:16.379592	t	t
1982	48	22	2017-07-26 11:25:16.379621	t	t
1983	48	15	2017-08-05 11:25:16.379649	t	t
1984	48	19	2017-08-16 11:25:16.379677	t	t
1985	48	33	2017-08-01 11:25:16.379706	t	t
1986	48	20	2017-08-18 11:25:16.379735	f	t
1987	48	12	2017-08-01 11:25:16.379763	f	t
1988	48	32	2017-08-04 11:25:16.379791	f	t
1989	48	15	2017-08-11 11:25:16.379819	f	t
1990	48	29	2017-08-14 11:25:16.379847	f	t
1991	48	10	2017-08-02 11:25:16.379876	f	t
1992	48	10	2017-08-07 11:25:16.379904	f	t
1993	48	17	2017-08-08 11:25:16.379932	f	t
1994	48	11	2017-07-27 11:25:16.379961	f	t
1995	48	36	2017-07-27 11:25:16.379989	f	t
1996	48	32	2017-08-13 11:25:16.380018	f	t
1997	48	7	2017-07-30 11:25:16.380046	f	t
1998	48	20	2017-08-03 11:25:16.380075	f	t
1999	48	31	2017-07-28 11:25:16.380102	f	t
2000	48	19	2017-08-18 11:25:16.380131	f	t
2001	48	13	2017-07-30 11:25:16.380159	f	t
2002	48	18	2017-07-28 11:25:16.380187	f	t
2003	48	14	2017-08-14 11:25:16.380216	f	t
2004	49	25	2017-08-13 11:25:16.380244	t	t
2005	49	13	2017-08-08 11:25:16.380272	t	t
2006	49	14	2017-07-30 11:25:16.3803	t	t
2007	49	27	2017-08-07 11:25:16.380329	t	t
2008	49	19	2017-08-06 11:25:16.380358	f	t
2009	49	7	2017-08-10 11:25:16.380387	f	t
2010	49	23	2017-08-04 11:25:16.380415	f	t
2011	49	12	2017-08-18 11:25:16.380443	f	t
2012	49	35	2017-08-03 11:25:16.380471	f	t
2013	49	36	2017-07-25 11:25:16.380499	f	t
2014	49	8	2017-07-26 11:25:16.380527	f	t
2015	49	37	2017-08-06 11:25:16.380554	f	t
2016	49	14	2017-08-05 11:25:16.380583	f	t
2017	49	29	2017-08-02 11:25:16.38061	f	t
2018	50	35	2017-07-26 11:25:16.380638	t	t
2019	50	7	2017-08-08 11:25:16.380667	t	t
2020	50	32	2017-07-25 11:25:16.380694	t	t
2021	50	29	2017-08-16 11:25:16.380723	t	t
2022	50	37	2017-08-18 11:25:16.380751	t	t
2023	50	10	2017-08-16 11:25:16.38078	t	t
2024	50	27	2017-08-14 11:25:16.380808	f	t
2025	50	19	2017-08-08 11:25:16.380836	f	t
2026	51	23	2017-08-07 11:25:16.380864	f	t
2027	51	34	2017-08-08 11:25:16.380892	f	t
2028	51	17	2017-07-30 11:25:16.381116	f	t
2029	51	9	2017-08-01 11:25:16.381149	f	t
2030	51	18	2017-08-05 11:25:16.381179	f	t
2031	51	24	2017-08-02 11:25:16.381208	f	t
2032	51	28	2017-08-13 11:25:16.381237	f	t
2033	51	24	2017-07-31 11:25:16.381266	f	t
2034	51	8	2017-08-01 11:25:16.381294	f	t
2035	51	25	2017-08-15 11:25:16.381322	f	t
2036	51	27	2017-08-18 11:25:16.38135	f	t
2037	51	37	2017-07-25 11:25:16.381379	f	t
2038	51	9	2017-08-19 11:25:16.381407	f	t
2039	51	15	2017-08-03 11:25:16.381436	f	t
2040	51	17	2017-07-31 11:25:16.381464	f	t
2041	51	28	2017-08-16 11:25:16.381492	f	t
2042	51	7	2017-08-12 11:25:16.381521	f	t
2043	51	37	2017-08-10 11:25:16.381549	f	t
2044	51	14	2017-08-18 11:25:16.381578	f	t
2045	51	15	2017-08-13 11:25:16.381607	f	t
2046	51	31	2017-07-30 11:25:16.381635	f	t
2047	51	29	2017-08-05 11:25:16.381663	f	t
2048	52	29	2017-08-11 11:25:16.381692	t	t
2049	52	19	2017-07-29 11:25:16.38172	t	t
2050	52	35	2017-08-16 11:25:16.381748	t	t
2051	52	29	2017-07-26 11:25:16.381777	t	t
2052	52	15	2017-07-27 11:25:16.381805	t	t
2053	52	15	2017-08-03 11:25:16.381832	t	t
2054	52	32	2017-08-08 11:25:16.38186	t	t
2055	52	28	2017-07-29 11:25:16.381888	f	t
2056	52	24	2017-08-04 11:25:16.381915	f	t
2057	52	10	2017-08-06 11:25:16.381944	f	t
2058	52	29	2017-08-03 11:25:16.381972	f	t
2059	52	14	2017-08-15 11:25:16.381999	f	t
2060	52	29	2017-08-05 11:25:16.382027	f	t
2061	52	25	2017-07-30 11:25:16.382055	f	t
2062	52	14	2017-07-31 11:25:16.382098	f	t
2063	52	35	2017-08-04 11:25:16.382141	f	t
2064	52	16	2017-08-11 11:25:16.382172	f	t
2065	52	29	2017-08-01 11:25:16.3822	f	t
2066	52	29	2017-08-15 11:25:16.382229	f	t
2067	52	34	2017-08-19 11:25:16.382257	f	t
2068	52	13	2017-08-17 11:25:16.382285	f	t
2069	52	29	2017-08-11 11:25:16.382319	f	t
2070	52	18	2017-08-11 11:25:16.382349	f	t
2071	53	11	2017-08-08 11:25:16.382377	t	t
2072	53	27	2017-07-29 11:25:16.382405	t	t
2073	54	27	2017-08-19 11:25:16.382433	t	t
2074	54	7	2017-08-15 11:25:16.382462	t	t
2075	54	29	2017-08-13 11:25:16.38249	t	t
2076	54	11	2017-08-03 11:25:16.382518	t	t
2077	54	27	2017-07-29 11:25:16.382545	t	t
2078	54	29	2017-07-31 11:25:16.382574	t	t
2079	54	19	2017-08-01 11:25:16.382601	t	t
2080	54	8	2017-08-16 11:25:16.382629	t	t
2081	54	18	2017-07-25 11:25:16.382657	t	t
2082	54	16	2017-08-18 11:25:16.382685	t	t
2083	54	13	2017-08-11 11:25:16.382714	t	t
2084	54	7	2017-08-15 11:25:16.382741	t	t
2085	54	10	2017-08-19 11:25:16.382769	t	t
2086	54	22	2017-07-29 11:25:16.382797	t	t
2087	54	27	2017-08-02 11:25:16.382824	t	t
2088	54	9	2017-08-06 11:25:16.382851	f	t
2089	54	29	2017-08-01 11:25:16.382878	f	t
2090	54	35	2017-08-01 11:25:16.382906	f	t
2091	54	28	2017-08-08 11:25:16.382934	f	t
2092	54	36	2017-08-06 11:25:16.382962	f	t
2093	54	14	2017-08-16 11:25:16.38299	f	t
2094	54	7	2017-08-09 11:25:16.383017	f	t
2095	54	31	2017-07-25 11:25:16.383045	f	t
2096	54	31	2017-08-02 11:25:16.383073	f	t
2097	54	17	2017-08-02 11:25:16.383101	f	t
2098	54	8	2017-08-06 11:25:16.383128	f	t
2099	54	8	2017-08-16 11:25:16.383156	f	t
2100	54	25	2017-08-08 11:25:16.383184	f	t
2101	54	31	2017-08-14 11:25:16.383211	f	t
2102	54	22	2017-08-18 11:25:16.383239	f	t
2103	54	12	2017-08-19 11:25:16.383268	f	t
2104	54	15	2017-08-18 11:25:16.383297	f	t
2105	54	33	2017-08-13 11:25:16.383327	f	t
2106	54	29	2017-08-17 11:25:16.383355	f	t
2107	54	29	2017-08-17 11:25:16.383384	f	t
2108	54	11	2017-07-27 11:25:16.383412	f	t
2109	54	20	2017-08-18 11:25:16.383441	f	t
2110	54	11	2017-08-12 11:25:16.383469	f	t
2111	54	31	2017-08-08 11:25:16.383497	f	t
2112	55	13	2017-08-10 11:25:16.383525	t	t
2113	55	35	2017-08-11 11:25:16.383553	t	t
2114	55	34	2017-07-26 11:25:16.383581	t	t
2115	55	11	2017-07-26 11:25:16.383608	t	t
2116	55	32	2017-08-03 11:25:16.383636	t	t
2117	55	14	2017-08-12 11:25:16.383663	t	t
2118	55	27	2017-08-03 11:25:16.383693	t	t
2119	55	28	2017-07-31 11:25:16.383721	t	t
2120	55	31	2017-07-28 11:25:16.38375	t	t
2121	55	15	2017-08-14 11:25:16.383778	f	t
2122	56	36	2017-07-30 11:25:16.383806	t	t
2123	56	7	2017-07-29 11:25:16.383833	t	t
2124	56	27	2017-07-25 11:25:16.38386	t	t
2125	56	18	2017-07-31 11:25:16.383888	t	t
2126	56	20	2017-08-10 11:25:16.383916	t	t
2127	56	7	2017-08-06 11:25:16.383943	t	t
2128	56	15	2017-07-31 11:25:16.383971	t	t
2129	56	15	2017-08-04 11:25:16.384	t	t
2130	56	8	2017-07-28 11:25:16.384028	f	t
2131	56	28	2017-07-25 11:25:16.384056	f	t
2132	56	12	2017-07-27 11:25:16.384083	f	t
2133	56	28	2017-08-19 11:25:16.384111	f	t
2134	56	24	2017-08-13 11:25:16.384138	f	t
2135	56	13	2017-07-26 11:25:16.384166	f	t
2136	56	14	2017-08-10 11:25:16.384193	f	t
2137	56	20	2017-08-16 11:25:16.384221	f	t
2138	57	23	2017-08-02 11:25:16.384249	t	t
2139	57	29	2017-08-14 11:25:16.384277	f	t
2140	57	18	2017-07-28 11:25:16.384305	f	t
2141	57	15	2017-08-14 11:25:16.384335	f	t
2142	58	26	2017-08-08 11:25:16.384362	t	t
2143	58	10	2017-08-11 11:25:16.38439	t	t
2144	58	13	2017-07-30 11:25:16.384417	t	t
2145	58	28	2017-07-29 11:25:16.384445	t	t
2146	58	31	2017-08-12 11:25:16.384474	t	t
2147	58	29	2017-07-29 11:25:16.384503	t	t
2148	58	15	2017-08-07 11:25:16.384531	t	t
2149	58	36	2017-08-06 11:25:16.384559	t	t
2150	58	13	2017-07-27 11:25:16.384587	t	t
2151	58	26	2017-08-17 11:25:16.384615	t	t
2152	58	11	2017-08-08 11:25:16.384646	t	t
2153	58	20	2017-07-25 11:25:16.384673	t	t
2154	58	19	2017-08-03 11:25:16.384701	t	t
2155	58	37	2017-08-16 11:25:16.384729	t	t
2156	58	8	2017-08-05 11:25:16.384757	f	t
2157	58	34	2017-08-05 11:25:16.384785	f	t
2158	58	35	2017-07-30 11:25:16.384813	f	t
2159	58	9	2017-07-31 11:25:16.384841	f	t
2160	58	21	2017-08-02 11:25:16.384869	f	t
2161	58	35	2017-07-26 11:25:16.384897	f	t
2162	58	29	2017-08-17 11:25:16.384924	f	t
2163	58	36	2017-08-01 11:25:16.384953	f	t
2164	59	7	2017-08-06 11:25:16.38498	t	t
2165	59	22	2017-07-27 11:25:16.385007	f	t
2166	60	32	2017-08-10 11:25:16.385035	t	t
2167	60	26	2017-07-28 11:25:16.385062	t	t
2168	60	36	2017-07-28 11:25:16.38509	t	t
2169	60	27	2017-08-14 11:25:16.385118	t	t
2170	60	27	2017-08-09 11:25:16.385146	t	t
2171	60	33	2017-08-09 11:25:16.385174	t	t
2172	60	29	2017-08-09 11:25:16.385201	t	t
2173	60	31	2017-08-05 11:25:16.385229	f	t
2174	60	13	2017-07-29 11:25:16.385259	f	t
2175	60	16	2017-08-19 11:25:16.385287	f	t
2176	60	17	2017-08-01 11:25:16.385315	f	t
2177	60	29	2017-08-07 11:25:16.385345	f	t
2178	60	24	2017-08-08 11:25:16.385373	f	t
2179	61	25	2017-08-15 11:25:16.385401	t	t
2180	61	32	2017-07-25 11:25:16.38543	t	t
2181	61	9	2017-07-31 11:25:16.385458	t	t
2182	61	32	2017-08-19 11:25:16.385485	t	t
2183	61	33	2017-08-01 11:25:16.385513	t	t
2184	61	28	2017-07-30 11:25:16.38554	t	t
2185	61	15	2017-08-05 11:25:16.385567	t	t
2186	62	15	2017-08-08 11:25:16.385595	t	t
2187	62	36	2017-08-10 11:25:16.385623	t	t
2188	62	14	2017-08-13 11:25:16.385651	t	t
2189	62	37	2017-08-14 11:25:16.385679	t	t
2190	63	16	2017-07-27 11:25:16.385707	f	t
2191	64	23	2017-08-19 11:25:16.385735	t	t
2192	64	27	2017-08-04 11:25:16.385762	t	t
2193	64	19	2017-08-01 11:25:16.38579	t	t
2194	64	27	2017-08-11 11:25:16.385818	t	t
2195	64	22	2017-07-30 11:25:16.385847	t	t
2196	64	26	2017-08-19 11:25:16.385875	t	t
2197	64	19	2017-08-13 11:25:16.385904	t	t
2198	64	20	2017-08-15 11:25:16.385932	t	t
2199	64	10	2017-08-15 11:25:16.38596	f	t
2200	64	18	2017-08-09 11:25:16.385988	f	t
2201	64	22	2017-07-28 11:25:16.386016	f	t
2202	64	27	2017-08-06 11:25:16.386044	f	t
2203	64	37	2017-08-18 11:25:16.386073	f	t
2204	64	25	2017-08-17 11:25:16.386101	f	t
2205	64	26	2017-08-16 11:25:16.386129	f	t
2206	64	14	2017-08-02 11:25:16.386156	f	t
2207	65	21	2017-08-04 11:25:16.386184	t	t
2208	65	13	2017-08-19 11:25:16.386214	t	t
2209	65	18	2017-08-05 11:25:16.386242	f	t
2210	65	32	2017-08-03 11:25:16.38627	f	t
2211	65	28	2017-08-09 11:25:16.386297	f	t
2212	66	11	2017-08-14 11:25:16.38633	t	t
2213	66	22	2017-08-09 11:25:16.386361	t	t
2214	66	26	2017-08-18 11:25:16.38639	t	t
2215	66	28	2017-08-16 11:25:16.386418	t	t
2216	66	29	2017-08-16 11:25:16.386446	t	t
2217	66	7	2017-08-11 11:25:16.386473	t	t
2218	66	35	2017-08-04 11:25:16.386501	t	t
2219	66	31	2017-07-31 11:25:16.386529	t	t
2220	66	23	2017-07-28 11:25:16.386556	t	t
2221	66	8	2017-08-16 11:25:16.386584	f	t
2222	66	13	2017-08-15 11:25:16.386612	f	t
2223	66	29	2017-08-15 11:25:16.386639	f	t
2224	66	34	2017-07-26 11:25:16.386667	f	t
2225	66	19	2017-07-26 11:25:16.386695	f	t
2226	66	36	2017-08-18 11:25:16.386723	f	t
2227	66	28	2017-08-11 11:25:16.386751	f	t
2228	66	9	2017-07-27 11:25:16.386779	f	t
2229	66	7	2017-08-18 11:25:16.386807	f	t
2230	66	37	2017-08-18 11:25:16.386837	f	t
2231	66	24	2017-08-13 11:25:16.386866	f	t
2232	66	31	2017-07-30 11:25:16.386896	f	t
2233	66	22	2017-07-26 11:25:16.386925	f	t
2234	66	31	2017-08-03 11:25:16.386953	f	t
2235	66	15	2017-08-15 11:25:16.38698	f	t
2236	66	37	2017-07-31 11:25:16.387008	f	t
2237	66	36	2017-08-07 11:25:16.387035	f	t
2238	66	11	2017-07-30 11:25:16.387063	f	t
2239	66	28	2017-08-14 11:25:16.387091	f	t
2240	66	32	2017-08-12 11:25:16.387118	f	t
2241	66	31	2017-08-09 11:25:16.387146	f	t
2242	66	31	2017-07-26 11:25:16.387174	f	t
2243	66	35	2017-08-17 11:25:16.387201	f	t
2244	66	28	2017-08-17 11:25:16.387229	f	t
2245	66	8	2017-07-30 11:25:16.387257	f	t
2246	67	33	2017-08-02 11:25:16.387285	t	t
2247	67	34	2017-08-18 11:25:16.387312	t	t
2248	67	24	2017-08-05 11:25:16.387341	t	t
2249	68	8	2017-08-15 11:25:16.387372	t	t
2250	68	7	2017-08-04 11:25:16.3874	t	t
2251	68	11	2017-07-28 11:25:16.387428	t	t
2252	68	8	2017-07-27 11:25:16.387455	t	t
2253	68	37	2017-08-04 11:25:16.387485	t	t
2254	68	20	2017-08-03 11:25:16.387513	f	t
2255	69	32	2017-08-17 11:25:16.387541	t	t
2256	69	7	2017-07-25 11:25:16.387571	t	t
2257	69	35	2017-08-04 11:25:16.387599	t	t
2258	69	13	2017-08-13 11:25:16.387627	t	t
2259	69	9	2017-07-29 11:25:16.387654	f	t
2260	69	25	2017-08-02 11:25:16.387681	f	t
2261	69	34	2017-07-26 11:25:16.387709	f	t
2262	69	22	2017-08-08 11:25:16.387737	f	t
2263	70	29	2017-07-27 11:25:16.387764	t	t
2264	70	24	2017-08-09 11:25:16.387792	t	t
2265	70	21	2017-08-10 11:25:16.387836	t	t
2266	70	29	2017-07-27 11:25:16.387864	t	t
2267	70	26	2017-08-01 11:25:16.387892	t	t
2268	70	7	2017-08-07 11:25:16.38792	t	t
2269	70	20	2017-08-07 11:25:16.387948	t	t
2270	70	10	2017-08-08 11:25:16.387976	t	t
2271	70	13	2017-08-10 11:25:16.388003	t	t
2272	70	31	2017-07-29 11:25:16.38803	t	t
2273	70	31	2017-08-14 11:25:16.388058	t	t
2274	70	11	2017-08-04 11:25:16.388085	t	t
2275	70	22	2017-08-03 11:25:16.388113	f	t
2276	70	34	2017-07-30 11:25:16.38814	f	t
2277	70	23	2017-07-28 11:25:16.388167	f	t
2278	70	11	2017-08-17 11:25:16.388195	f	t
2279	70	24	2017-07-25 11:25:16.388223	f	t
2280	70	9	2017-08-13 11:25:16.388253	f	t
2281	70	15	2017-07-26 11:25:16.388281	f	t
2282	71	32	2017-08-04 11:25:16.388309	t	t
2283	71	36	2017-08-03 11:25:16.388337	t	t
2284	71	13	2017-08-10 11:25:16.388365	t	t
2285	71	25	2017-08-11 11:25:16.388395	t	t
2286	71	16	2017-08-15 11:25:16.388424	f	t
2287	71	29	2017-07-26 11:25:16.388453	f	t
2288	71	17	2017-07-31 11:25:16.388481	f	t
2289	72	17	2017-08-02 11:25:16.388509	t	t
2290	72	11	2017-08-19 11:25:16.388537	t	t
2291	72	17	2017-07-28 11:25:16.388564	t	t
2292	72	16	2017-08-05 11:25:16.388592	t	t
2293	72	10	2017-07-29 11:25:16.38862	t	t
2294	72	22	2017-07-28 11:25:16.388648	t	t
2295	72	34	2017-08-16 11:25:16.388676	t	t
2296	72	13	2017-07-25 11:25:16.388703	t	t
2297	72	32	2017-08-02 11:25:16.388732	t	t
2298	72	20	2017-07-31 11:25:16.38876	t	t
2299	72	18	2017-07-25 11:25:16.388788	t	t
2300	72	28	2017-08-17 11:25:16.388815	f	t
2301	72	18	2017-08-13 11:25:16.388843	f	t
2302	72	29	2017-08-03 11:25:16.38887	f	t
2303	72	36	2017-07-26 11:25:16.388898	f	t
2304	72	9	2017-08-17 11:25:16.388926	f	t
2305	72	8	2017-08-10 11:25:16.388954	f	t
2306	72	15	2017-07-28 11:25:16.388982	f	t
2307	72	29	2017-08-07 11:25:16.38901	f	t
2308	72	9	2017-08-16 11:25:16.389038	f	t
2309	72	32	2017-08-04 11:25:16.389065	f	t
2310	72	24	2017-07-30 11:25:16.389093	f	t
2311	72	26	2017-08-08 11:25:16.389121	f	t
2312	73	24	2017-07-30 11:25:16.389148	t	t
2313	73	17	2017-08-13 11:25:16.389175	t	t
2314	73	7	2017-08-13 11:25:16.389203	t	t
2315	73	29	2017-08-13 11:25:16.389231	t	t
2316	73	24	2017-08-06 11:25:16.389259	f	t
2317	73	27	2017-08-10 11:25:16.389286	f	t
2318	73	29	2017-08-12 11:25:16.389314	f	t
2319	74	9	2017-08-05 11:25:16.389341	t	t
2320	74	25	2017-08-02 11:25:16.389368	t	t
2321	74	16	2017-07-27 11:25:16.389398	t	t
2322	74	20	2017-08-13 11:25:16.389425	t	t
2323	74	7	2017-07-31 11:25:16.389453	t	t
2324	74	32	2017-08-06 11:25:16.38948	t	t
2325	74	31	2017-08-08 11:25:16.389508	t	t
2326	74	31	2017-08-11 11:25:16.389535	t	t
2327	74	32	2017-07-27 11:25:16.389563	t	t
2328	74	16	2017-07-26 11:25:16.389593	t	t
2329	74	15	2017-08-17 11:25:16.389621	f	t
2330	74	28	2017-08-14 11:25:16.389649	f	t
2331	74	9	2017-08-17 11:25:16.389676	f	t
2332	74	29	2017-08-09 11:25:16.389704	f	t
2333	74	37	2017-08-06 11:25:16.389732	f	t
2334	74	33	2017-08-09 11:25:16.38976	f	t
2335	74	7	2017-07-31 11:25:16.389787	f	t
2336	74	20	2017-08-09 11:25:16.389815	f	t
2337	75	21	2017-08-10 11:25:16.389842	t	t
2338	75	29	2017-07-25 11:25:16.38987	t	t
2339	75	11	2017-08-11 11:25:16.389897	t	t
2340	75	14	2017-08-19 11:25:16.389925	t	t
2341	75	12	2017-08-14 11:25:16.389952	t	t
2342	75	34	2017-08-05 11:25:16.389982	f	t
2343	75	36	2017-08-14 11:25:16.390009	f	t
2344	75	35	2017-07-25 11:25:16.390036	f	t
2345	75	26	2017-07-31 11:25:16.390064	f	t
2346	75	8	2017-08-09 11:25:16.390091	f	t
2347	75	12	2017-07-29 11:25:16.390119	f	t
2348	75	21	2017-08-09 11:25:16.390147	f	t
2349	75	23	2017-07-28 11:25:16.390175	f	t
2350	75	37	2017-07-26 11:25:16.390202	f	t
2351	75	23	2017-08-09 11:25:16.39023	f	t
2352	75	24	2017-08-19 11:25:16.390259	f	t
2353	75	21	2017-07-28 11:25:16.390287	f	t
2354	75	20	2017-08-12 11:25:16.39032	f	t
2355	75	12	2017-08-10 11:25:16.39035	f	t
2356	75	29	2017-08-08 11:25:16.390378	f	t
2357	75	33	2017-08-17 11:25:16.390408	f	t
2358	75	11	2017-08-17 11:25:16.390437	f	t
2359	75	8	2017-07-30 11:25:16.390465	f	t
2360	75	37	2017-07-30 11:25:16.390492	f	t
2361	76	21	2017-07-25 11:25:16.39052	f	t
2362	76	23	2017-08-14 11:25:16.390547	f	t
2363	76	32	2017-07-28 11:25:16.390574	f	t
2364	76	27	2017-08-02 11:25:16.390601	f	t
2365	76	33	2017-07-31 11:25:16.390629	f	t
2366	76	29	2017-08-03 11:25:16.390656	f	t
2367	76	17	2017-08-19 11:25:16.390684	f	t
2368	76	37	2017-08-14 11:25:16.390711	f	t
2369	76	7	2017-08-01 11:25:16.390738	f	t
2370	76	37	2017-08-07 11:25:16.390766	f	t
2371	76	31	2017-07-29 11:25:16.390793	f	t
2372	76	34	2017-07-30 11:25:16.39082	f	t
2373	76	8	2017-08-07 11:25:16.390849	f	t
2374	76	11	2017-08-12 11:25:16.390877	f	t
2375	76	24	2017-08-17 11:25:16.390905	f	t
2376	76	31	2017-08-02 11:25:16.390934	f	t
2377	76	12	2017-08-09 11:25:16.390963	f	t
2378	76	36	2017-08-06 11:25:16.39099	f	t
2379	76	34	2017-08-16 11:25:16.391018	f	t
2380	76	33	2017-08-03 11:25:16.391046	f	t
2381	76	22	2017-08-19 11:25:16.391075	f	t
2382	77	13	2017-08-07 11:25:16.391103	t	t
2383	77	17	2017-08-18 11:25:16.391131	f	t
2384	77	8	2017-08-18 11:25:16.391159	f	t
2385	77	19	2017-08-01 11:25:16.391187	f	t
2386	77	29	2017-08-16 11:25:16.391214	f	t
2387	77	33	2017-08-01 11:25:16.391242	f	t
2388	77	32	2017-07-30 11:25:16.391269	f	t
2389	77	11	2017-08-10 11:25:16.391296	f	t
2390	77	24	2017-07-27 11:25:16.391324	f	t
2391	77	21	2017-08-17 11:25:16.391351	f	t
2392	77	35	2017-08-05 11:25:16.391379	f	t
2393	77	32	2017-08-09 11:25:16.391409	f	t
2394	77	14	2017-08-07 11:25:16.391437	f	t
2395	77	15	2017-08-07 11:25:16.391464	f	t
2396	77	35	2017-08-06 11:25:16.391492	f	t
2397	77	35	2017-07-26 11:25:16.391519	f	t
2398	77	36	2017-07-28 11:25:16.391549	f	t
2399	77	8	2017-08-17 11:25:16.391578	f	t
2400	77	24	2017-08-14 11:25:16.391607	f	t
2401	78	33	2017-08-19 11:25:16.391635	f	t
2402	78	18	2017-07-30 11:25:16.391663	f	t
2403	79	29	2017-07-25 11:25:16.391691	t	t
2404	79	21	2017-07-29 11:25:16.391719	t	t
2405	79	24	2017-08-01 11:25:16.391747	f	t
2406	79	35	2017-08-08 11:25:16.391775	f	t
2407	79	17	2017-08-02 11:25:16.391803	f	t
2408	79	14	2017-08-16 11:25:16.391831	f	t
2409	79	14	2017-08-06 11:25:16.391858	f	t
2410	79	14	2017-08-05 11:25:16.391886	f	t
2411	79	13	2017-08-02 11:25:16.391914	f	t
2412	80	21	2017-08-16 11:25:16.391942	t	t
2413	80	31	2017-08-18 11:25:16.39197	t	t
2414	80	21	2017-08-04 11:25:16.391998	t	t
2415	80	28	2017-07-30 11:25:16.392026	t	t
2416	80	11	2017-08-14 11:25:16.392055	t	t
2417	80	26	2017-08-13 11:25:16.392084	t	t
2418	80	16	2017-08-11 11:25:16.392112	t	t
2419	80	12	2017-08-08 11:25:16.39214	t	t
2420	80	9	2017-08-08 11:25:16.392168	t	t
2421	80	16	2017-07-28 11:25:16.392196	t	t
2422	80	11	2017-08-08 11:25:16.392224	t	t
2423	80	32	2017-08-06 11:25:16.392253	f	t
2424	80	28	2017-08-14 11:25:16.392282	f	t
2425	80	24	2017-08-08 11:25:16.392311	f	t
2426	80	19	2017-07-31 11:25:16.392339	f	t
2427	80	7	2017-08-05 11:25:16.392367	f	t
2428	80	32	2017-08-01 11:25:16.392395	f	t
2429	80	9	2017-08-17 11:25:16.392424	f	t
2430	80	14	2017-07-26 11:25:16.392453	f	t
2431	80	16	2017-08-16 11:25:16.392481	f	t
2432	80	15	2017-07-26 11:25:16.392509	f	t
2433	80	13	2017-08-14 11:25:16.392536	f	t
2434	81	13	2017-08-14 11:25:16.392564	f	t
2435	82	16	2017-08-18 11:25:16.392592	t	t
2436	82	7	2017-07-27 11:25:16.39262	t	t
2437	82	29	2017-08-19 11:25:16.392648	t	t
2438	82	31	2017-08-13 11:25:16.392676	t	t
2439	82	27	2017-08-05 11:25:16.392704	t	t
2440	82	23	2017-08-06 11:25:16.392731	t	t
2441	82	10	2017-07-31 11:25:16.39276	t	t
2442	82	37	2017-07-26 11:25:16.392787	t	t
2443	82	32	2017-08-15 11:25:16.392815	f	t
2444	82	16	2017-08-03 11:25:16.392843	f	t
2445	82	27	2017-08-11 11:25:16.392871	f	t
2446	82	21	2017-07-27 11:25:16.392898	f	t
2447	82	17	2017-07-26 11:25:16.392926	f	t
2448	82	10	2017-08-10 11:25:16.392956	f	t
2449	82	14	2017-08-16 11:25:16.392984	f	t
2450	82	34	2017-07-26 11:25:16.393012	f	t
\.


--
-- Name: clicked_statements_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('clicked_statements_uid_seq', 2450, true);


--
-- Data for Name: groups; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY groups (uid, name) FROM stdin;
1	admins
2	authors
3	users
4	specials
\.


--
-- Name: groups_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('groups_uid_seq', 4, true);


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
1	Town has to cut spending 	town-has-to-cut-spending	Our town needs to cut spending. Please discuss ideas how this should be done.		2017-08-19 11:25:09.092381	2	1	t
2	Cat or Dog	cat-or-dog	Your family argues about whether to buy a cat or dog as pet. Now your opinion matters!		2017-08-19 11:25:09.092531	2	1	f
3	Make the world better	make-the-world-better	How can we make this world a better place?		2017-08-19 11:25:09.092636	2	1	f
4	Elektroautos	elektroautos	Elektroautos - Die Autos der Zukunft? Bitte diskutieren Sie dazu.		2017-08-19 11:25:09.092737	2	2	f
5	Unterstützung der Sekretariate	unterstutzung-der-sekretariate	Unsere Sekretariate in der Informatik sind arbeitsmäßig stark überlastet. Bitte diskutieren Sie Möglichkeiten um dies zu verbessern.		2017-08-19 11:25:09.093618	2	2	f
6	Verbesserung des Informatik-Studiengangs	verbesserung-des-informatik-studiengangs	Wie können der Informatik-Studiengang verbessert und die Probleme, die durch die große Anzahl der Studierenden entstanden sind, gelöst werden?	Die Anzahl der Studierenden in der Informatik hat sich in den letzten Jahren stark erhöht. Dadurch treten zahlreiche Probleme auf, wie z.B. Raumknappheit, überfüllte Lehrveranstaltungen und ein Mangel an Plätzen zum Lernen. Wir möchten Sie gerne dazu einladen, gemeinsam mit den Dozierenden der Informatik über Lösungsmöglichkeiten zu diskutieren: Wie können der Studiengang verbessert und die Probleme, die durch die große Anzahl der Studierenden entstanden sind, gelöst werden?	2017-08-19 11:25:09.093742	2	2	t
7	Bürgerbeteiligung in der Kommune	burgerbeteiligung-in-der-kommune	Es werden Vorschläge zur Verbesserung des Zusammenlebens in unserer Kommune gesammelt.		2017-08-19 11:25:09.093865	2	2	f
8	Read only Issue	read-only-issue	Dieses Thema ist zum Testm für die read-only Property.		2017-08-19 11:25:09.093865	2	2	f
\.


--
-- Name: issues_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('issues_uid_seq', 8, true);


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
1	14	1	t	2017-08-19 11:25:11.946538
2	16	1	f	2017-08-19 11:25:11.946627
3	17	1	t	2017-08-19 11:25:11.946712
4	22	1	t	2017-08-19 11:25:11.946795
5	23	1	t	2017-08-19 11:25:11.946887
6	20	2	f	2017-08-19 11:25:11.946969
7	21	2	t	2017-08-19 11:25:11.94705
8	18	2	f	2017-08-19 11:25:11.94713
9	34	2	t	2017-08-19 11:25:11.947212
10	24	2	f	2017-08-19 11:25:11.947291
11	25	2	f	2017-08-19 11:25:11.94737
12	26	2	f	2017-08-19 11:25:11.94745
13	27	3	f	2017-08-19 11:25:11.94753
14	28	3	f	2017-08-19 11:25:11.94761
15	33	3	f	2017-08-19 11:25:11.947689
16	19	8	t	2017-08-19 11:25:11.947768
17	35	8	t	2017-08-19 11:25:11.947846
18	36	8	t	2017-08-19 11:25:11.947926
\.


--
-- Name: last_reviewers_delete_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('last_reviewers_delete_uid_seq', 18, true);


--
-- Data for Name: last_reviewers_duplicates; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY last_reviewers_duplicates (uid, reviewer_uid, review_uid, is_okay, "timestamp") FROM stdin;
1	12	1	t	2017-08-19 11:25:11.94802
2	13	2	t	2017-08-19 11:25:11.948103
3	14	2	t	2017-08-19 11:25:11.948184
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
1	29	1	t	2017-08-19 11:25:11.945932
2	31	1	t	2017-08-19 11:25:11.946061
3	32	1	t	2017-08-19 11:25:11.946153
4	12	2	f	2017-08-19 11:25:11.946241
5	13	2	f	2017-08-19 11:25:11.946347
6	15	2	f	2017-08-19 11:25:11.946436
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
1	1	1	f	1	2017-08-19 11:25:09.308848	2	t
2	2	5	f	1	2017-08-19 11:25:09.308983	2	f
3	3	6	f	1	2017-08-19 11:25:09.309062	2	f
4	4	7	f	1	2017-08-19 11:25:09.309138	2	f
5	5	8	f	1	2017-08-19 11:25:09.309212	2	f
6	6	9	f	1	2017-08-19 11:25:09.309286	2	f
7	7	10	f	1	2017-08-19 11:25:09.309358	2	f
8	8	11	f	1	2017-08-19 11:25:09.309431	2	f
9	9	12	f	1	2017-08-19 11:25:09.309503	2	f
10	10	13	f	1	2017-08-19 11:25:09.309574	2	f
11	11	14	f	1	2017-08-19 11:25:09.309646	2	f
12	12	15	f	1	2017-08-19 11:25:09.309717	2	f
13	12	16	f	1	2017-08-19 11:25:09.309788	2	f
14	13	17	f	1	2017-08-19 11:25:09.309859	2	f
15	14	18	f	1	2017-08-19 11:25:09.30993	2	f
16	15	19	f	1	2017-08-19 11:25:09.310001	2	f
17	16	20	f	1	2017-08-19 11:25:09.310073	2	f
18	17	21	f	1	2017-08-19 11:25:09.310144	2	f
19	18	22	f	1	2017-08-19 11:25:09.310216	2	f
20	19	23	f	1	2017-08-19 11:25:09.310287	2	f
21	20	24	f	1	2017-08-19 11:25:09.310374	2	f
22	21	25	f	1	2017-08-19 11:25:09.310448	2	f
23	22	26	f	1	2017-08-19 11:25:09.31052	2	f
24	23	27	f	1	2017-08-19 11:25:09.310591	2	f
25	24	28	f	1	2017-08-19 11:25:09.310663	2	f
26	25	29	f	1	2017-08-19 11:25:09.310735	2	f
27	26	30	f	1	2017-08-19 11:25:09.310806	2	f
28	27	31	f	1	2017-08-19 11:25:09.310877	2	f
29	28	32	f	1	2017-08-19 11:25:09.310949	2	f
30	29	33	f	1	2017-08-19 11:25:09.311019	2	f
31	30	34	f	1	2017-08-19 11:25:09.31109	2	f
32	9	35	f	1	2017-08-19 11:25:09.311161	2	f
33	31	39	f	1	2017-08-19 11:25:09.311233	1	f
34	32	40	f	1	2017-08-19 11:25:09.311305	1	f
35	33	41	f	1	2017-08-19 11:25:09.311377	1	f
36	34	42	f	1	2017-08-19 11:25:09.311448	1	f
37	35	43	f	1	2017-08-19 11:25:09.31152	1	f
38	36	44	f	1	2017-08-19 11:25:09.311592	1	f
39	37	45	f	1	2017-08-19 11:25:09.311664	1	f
40	38	46	f	1	2017-08-19 11:25:09.311736	1	f
41	39	47	f	1	2017-08-19 11:25:09.311808	1	f
42	40	48	f	1	2017-08-19 11:25:09.311879	1	f
43	41	49	f	1	2017-08-19 11:25:09.311971	1	f
44	42	50	f	1	2017-08-19 11:25:09.312052	1	f
45	43	51	f	1	2017-08-19 11:25:09.31212	1	f
46	44	52	f	1	2017-08-19 11:25:09.312193	1	f
47	45	53	f	1	2017-08-19 11:25:09.312263	1	f
48	46	54	f	1	2017-08-19 11:25:09.312332	1	f
49	47	55	f	1	2017-08-19 11:25:09.312401	1	f
50	48	56	f	1	2017-08-19 11:25:09.31247	1	f
51	49	57	f	1	2017-08-19 11:25:09.312541	1	f
52	52	61	f	1	2017-08-19 11:25:09.312753	4	f
53	53	62	f	1	2017-08-19 11:25:09.312824	4	f
54	54	63	f	1	2017-08-19 11:25:09.312951	4	f
55	55	64	f	1	2017-08-19 11:25:09.313025	4	f
56	56	65	f	1	2017-08-19 11:25:09.313099	4	f
57	57	66	f	1	2017-08-19 11:25:09.313172	4	f
58	50	59	f	1	2017-08-19 11:25:09.312612	4	f
59	51	60	f	1	2017-08-19 11:25:09.312683	4	f
60	61	68	f	5	2017-08-19 11:25:09.313241	4	f
61	62	71	f	1	2017-08-19 11:25:09.313313	5	f
62	63	72	f	1	2017-08-19 11:25:09.313384	5	f
63	64	73	f	1	2017-08-19 11:25:09.313453	5	f
64	65	74	f	1	2017-08-19 11:25:09.313524	5	f
65	66	75	f	1	2017-08-19 11:25:09.313594	5	f
66	67	77	f	1	2017-08-19 11:25:09.313663	7	f
67	68	78	f	1	2017-08-19 11:25:09.313732	7	f
68	69	79	f	1	2017-08-19 11:25:09.313812	7	f
69	70	80	f	1	2017-08-19 11:25:09.313883	7	f
70	70	81	f	1	2017-08-19 11:25:09.313961	7	f
71	71	82	f	1	2017-08-19 11:25:09.314031	7	f
\.


--
-- Name: premises_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('premises_uid_seq', 71, true);


--
-- Data for Name: reputation_history; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY reputation_history (uid, reputator_uid, reputation_uid, "timestamp") FROM stdin;
1	23	1	2017-08-17 11:25:11.97799
2	23	2	2017-08-18 11:25:11.97799
3	23	3	2017-08-19 11:25:11.97799
4	25	1	2017-08-17 11:25:11.97799
5	25	2	2017-08-18 11:25:11.97799
6	25	3	2017-08-19 11:25:11.97799
7	22	1	2017-08-17 11:25:11.97799
8	22	2	2017-08-18 11:25:11.97799
9	22	3	2017-08-19 11:25:11.97799
10	34	1	2017-08-17 11:25:11.97799
11	34	2	2017-08-18 11:25:11.97799
12	34	3	2017-08-19 11:25:11.97799
13	3	1	2017-08-17 11:25:11.97799
14	3	2	2017-08-18 11:25:11.97799
15	3	3	2017-08-19 11:25:11.97799
16	3	8	2017-08-19 11:25:11.97799
17	3	3	2017-08-17 11:25:11.97799
18	3	4	2017-08-17 11:25:11.97799
19	3	5	2017-08-18 11:25:11.97799
20	3	6	2017-08-18 11:25:11.97799
21	3	9	2017-08-19 11:25:11.97799
22	3	8	2017-08-19 11:25:11.97799
23	2	4	2017-08-17 11:25:11.97799
24	2	5	2017-08-17 11:25:11.97799
25	2	6	2017-08-18 11:25:11.97799
26	2	9	2017-08-18 11:25:11.97799
27	2	7	2017-08-19 11:25:11.97799
28	2	10	2017-08-19 11:25:11.97799
29	2	8	2017-08-19 11:25:11.97799
30	2	11	2017-08-19 11:25:11.97799
31	2	12	2017-08-19 11:25:11.97799
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
1	18	7	\N	2017-08-19 11:25:11.92031	t	1	f
2	19	6	\N	2017-08-19 11:25:11.920387	t	1	f
3	20	\N	19	2017-08-19 11:25:11.920459	t	1	f
4	21	\N	9	2017-08-19 11:25:11.920531	f	2	f
5	22	\N	7	2017-08-19 11:25:11.920604	f	1	f
6	23	\N	8	2017-08-19 11:25:11.920676	f	1	f
7	24	26	\N	2017-08-19 11:25:11.920748	f	1	f
8	25	11	\N	2017-08-19 11:25:11.92082	f	2	f
9	26	26	\N	2017-08-19 11:25:11.920891	f	1	f
10	27	1	\N	2017-08-19 11:25:11.920964	t	1	f
\.


--
-- Name: review_deletes_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('review_deletes_uid_seq', 10, true);


--
-- Data for Name: review_duplicates; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY review_duplicates (uid, detector_uid, duplicate_statement_uid, original_statement_uid, "timestamp", is_executed, is_revoked) FROM stdin;
1	28	6	1	2017-08-19 11:25:11.921042	f	f
2	29	4	1	2017-08-19 11:25:11.921111	t	f
3	29	22	7	2017-08-19 11:25:11.921176	f	f
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
1	3	\N	2	2017-08-19 11:25:11.992842	f	f
\.


--
-- Name: review_edits_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('review_edits_uid_seq', 1, true);


--
-- Data for Name: review_merge; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY review_merge (uid, detector_uid, premisesgroup_uid, "timestamp", is_executed, is_revoked) FROM stdin;
1	31	1	2017-08-19 11:25:11.921251	f	f
2	32	5	2017-08-19 11:25:11.921318	f	f
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
1	12	30	\N	2017-08-19 11:25:11.919824	t	f
2	13	\N	27	2017-08-19 11:25:11.919943	t	f
3	14	\N	16	2017-08-19 11:25:11.920017	f	f
4	16	22	\N	2017-08-19 11:25:11.920156	f	f
5	17	16	\N	2017-08-19 11:25:11.920224	f	f
6	15	\N	29	2017-08-19 11:25:11.920088	f	f
\.


--
-- Name: review_optimizations_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('review_optimizations_uid_seq', 6, true);


--
-- Data for Name: review_split; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY review_split (uid, detector_uid, premisesgroup_uid, "timestamp", is_executed, is_revoked) FROM stdin;
1	33	10	2017-08-19 11:25:11.921389	f	f
2	34	12	2017-08-19 11:25:11.921457	f	f
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
1191	1	33
1192	1	22
1193	1	21
1194	1	36
1195	2	8
1196	2	18
1197	2	21
1198	2	13
1199	2	25
1200	2	24
1201	2	34
1202	2	31
1203	2	14
1204	2	26
1205	2	29
1206	2	12
1207	2	35
1208	2	16
1209	2	20
1210	2	27
1211	2	29
1212	2	36
1213	2	11
1214	2	37
1215	2	28
1216	2	23
1217	2	9
1218	2	22
1219	2	15
1220	2	17
1221	2	32
1222	3	15
1223	3	33
1224	3	21
1225	3	16
1226	3	37
1227	3	35
1228	3	11
1229	3	22
1230	3	12
1231	3	31
1232	3	20
1233	3	9
1234	3	13
1235	3	8
1236	4	33
1237	4	37
1238	4	22
1239	4	8
1240	4	11
1241	4	9
1242	4	27
1243	4	14
1244	4	35
1245	4	25
1246	4	18
1247	4	17
1248	4	24
1249	4	31
1250	4	16
1251	4	10
1252	4	34
1253	4	26
1254	4	20
1255	4	36
1256	4	13
1257	4	19
1258	4	28
1259	4	29
1260	5	29
1261	5	13
1262	5	34
1263	5	37
1264	5	29
1265	5	32
1266	5	26
1267	5	17
1268	5	9
1269	5	8
1270	5	18
1271	5	36
1272	5	16
1273	5	35
1274	8	35
1275	8	21
1276	8	17
1277	8	24
1278	8	13
1279	8	14
1280	8	29
1281	8	18
1282	8	31
1283	8	28
1284	8	29
1285	8	23
1286	8	22
1287	8	11
1288	8	7
1289	8	27
1290	8	10
1291	8	19
1292	8	9
1293	8	20
1294	8	37
1295	8	15
1296	10	19
1297	10	21
1298	10	32
1299	10	16
1300	10	36
1301	10	31
1302	10	17
1303	10	8
1304	10	15
1305	10	24
1306	10	29
1307	10	9
1308	10	25
1309	10	34
1310	10	12
1311	10	11
1312	10	29
1313	10	27
1314	10	37
1315	10	14
1316	10	20
1317	10	10
1318	11	33
1319	11	15
1320	11	29
1321	11	19
1322	11	37
1323	11	28
1324	11	8
1325	11	13
1326	11	29
1327	11	9
1328	11	35
1329	11	31
1330	11	32
1331	11	10
1332	11	34
1333	11	12
1334	11	21
1335	11	27
1336	11	25
1337	11	26
1338	11	20
1339	11	23
1340	11	16
1341	11	7
1342	11	24
1343	11	11
1344	11	36
1345	11	22
1346	11	18
1347	12	31
1348	12	12
1349	12	16
1350	12	20
1351	12	33
1352	12	21
1353	12	15
1354	12	24
1355	12	9
1356	12	27
1357	12	23
1358	12	17
1359	12	8
1360	12	13
1361	15	19
1362	15	10
1363	15	16
1364	15	29
1365	15	9
1366	15	23
1367	15	15
1368	15	25
1369	15	36
1370	15	28
1371	15	13
1372	15	29
1373	15	11
1374	16	10
1375	16	29
1376	16	16
1377	16	17
1378	16	22
1379	16	9
1380	16	12
1381	16	8
1382	16	15
1383	16	18
1384	17	34
1385	17	23
1386	17	7
1387	17	20
1388	17	33
1389	17	25
1390	17	10
1391	17	15
1392	17	16
1393	17	27
1394	17	11
1395	17	29
1396	17	9
1397	17	18
1398	17	31
1399	17	36
1400	17	21
1401	17	14
1402	17	12
1403	17	13
1404	17	26
1405	17	22
1406	17	29
1407	17	37
1408	17	17
1409	17	8
1410	17	19
1411	17	35
1412	19	33
1413	19	12
1414	19	32
1415	19	16
1416	19	20
1417	19	8
1418	20	36
1419	20	13
1420	20	26
1421	20	27
1422	20	37
1423	20	14
1424	20	18
1425	20	31
1426	20	20
1427	20	33
1428	20	19
1429	20	9
1430	20	23
1431	20	11
1432	20	32
1433	20	29
1434	20	15
1435	20	29
1436	20	28
1437	20	24
1438	20	25
1439	20	34
1440	20	12
1441	20	35
1442	21	37
1443	21	21
1444	21	10
1445	21	31
1446	23	23
1447	23	36
1448	23	34
1449	23	33
1450	23	17
1451	23	26
1452	23	18
1453	23	28
1454	23	14
1455	23	27
1456	23	22
1457	23	10
1458	23	12
1459	23	21
1460	23	11
1461	23	25
1462	23	9
1463	23	16
1464	24	14
1465	24	13
1466	24	12
1467	24	18
1468	24	16
1469	24	22
1470	24	25
1471	26	22
1472	26	7
1473	26	18
1474	26	16
1475	27	18
1476	27	25
1477	27	26
1478	27	14
1479	27	15
1480	27	37
1481	27	23
1482	27	32
1483	27	29
1484	27	34
1485	27	17
1486	28	29
1487	28	21
1488	28	24
1489	28	19
1490	28	23
1491	28	8
1492	28	34
1493	28	14
1494	28	18
1495	28	22
1496	29	26
1497	29	33
1498	29	14
1499	29	20
1500	29	36
1501	29	19
1502	29	8
1503	29	13
1504	29	29
1505	29	12
1506	29	34
1507	29	35
1508	30	15
1509	30	13
1510	30	10
1511	30	35
1512	30	8
1513	30	24
1514	30	28
1515	30	26
1516	30	32
1517	30	7
1518	30	27
1519	30	33
1520	30	31
1521	30	29
1522	30	18
1523	30	22
1524	30	19
1525	30	14
1526	30	21
1527	30	16
1528	32	24
1529	32	11
1530	32	35
1531	32	31
1532	32	22
1533	32	32
1534	32	23
1535	32	21
1536	32	15
1537	32	16
1538	32	20
1539	32	14
1540	32	10
1541	32	29
1542	32	25
1543	32	34
1544	32	29
1545	32	37
1546	32	33
1547	32	13
1548	32	27
1549	32	26
1550	32	28
1551	32	12
1552	32	9
1553	32	17
1554	32	18
1555	32	8
1556	32	36
1557	34	20
1558	34	37
1559	34	19
1560	34	27
1561	34	24
1562	34	23
1563	34	36
1564	34	25
1565	34	14
1566	34	8
1567	34	32
1568	34	22
1569	34	7
1570	34	10
1571	35	26
1572	35	31
1573	35	7
1574	35	12
1575	35	19
1576	35	14
1577	35	18
1578	35	16
1579	35	33
1580	35	37
1581	35	13
1582	35	9
1583	35	34
1584	35	29
1585	36	15
1586	36	35
1587	36	19
1588	36	12
1589	36	29
1590	36	10
1591	36	32
1592	36	8
1593	36	34
1594	36	24
1595	36	22
1596	36	16
1597	36	33
1598	36	37
1599	36	13
1600	36	25
1601	36	18
1602	36	31
1603	36	9
1604	36	26
1605	39	18
1606	39	12
1607	39	27
1608	39	34
1609	39	33
1610	39	31
1611	39	22
1612	39	10
1613	39	20
1614	39	7
1615	39	21
1616	39	37
1617	39	14
1618	39	9
1619	39	8
1620	39	16
1621	39	28
1622	39	19
1623	39	11
1624	39	25
1625	39	36
1626	39	35
1627	39	26
1628	40	37
1629	40	26
1630	40	15
1631	40	27
1632	40	12
1633	40	17
1634	40	24
1635	40	16
1636	41	16
1637	41	28
1638	41	15
1639	41	29
1640	41	10
1641	41	14
1642	41	18
1643	41	36
1644	41	21
1645	41	12
1646	41	35
1647	41	31
1648	41	34
1649	41	33
1650	41	7
1651	41	9
1652	41	11
1653	41	17
1654	41	23
1655	41	32
1656	41	8
1657	41	37
1658	41	20
1659	41	27
1660	41	29
1661	41	25
1662	41	26
1663	41	19
1664	42	19
1665	42	13
1666	42	27
1667	42	29
1668	42	35
1669	42	18
1670	42	9
1671	42	7
1672	42	21
1673	42	14
1674	42	33
1675	42	37
1676	42	12
1677	44	12
1678	44	8
1679	44	25
1680	44	20
1681	44	14
1682	44	36
1683	44	13
1684	44	15
1685	44	31
1686	44	29
1687	44	24
1688	44	28
1689	44	11
1690	44	7
1691	44	33
1692	44	9
1693	46	9
1694	46	11
1695	46	12
1696	46	10
1697	46	24
1698	46	13
1699	46	20
1700	46	32
1701	46	28
1702	46	37
1703	46	26
1704	47	35
1705	47	22
1706	47	15
1707	47	23
1708	47	27
1709	49	35
1710	49	13
1711	49	25
1712	49	10
1713	49	24
1714	50	31
1715	50	28
1716	50	18
1717	50	11
1718	50	25
1719	50	26
1720	50	33
1721	50	13
1722	50	34
1723	50	21
1724	50	12
1725	50	37
1726	50	16
1727	50	17
1728	50	32
1729	50	29
1730	50	35
1731	50	27
1732	50	22
1733	50	19
1734	51	21
1735	51	9
1736	51	20
1737	51	34
1738	51	31
1739	51	14
1740	51	32
1741	54	20
1742	54	23
1743	54	18
1744	54	11
1745	54	29
1746	54	7
1747	54	36
1748	54	33
1749	54	24
1750	54	37
1751	54	27
1752	54	35
1753	54	8
1754	55	17
1755	55	24
1756	55	34
1757	55	18
1758	55	19
1759	55	31
1760	55	9
1761	55	20
1762	55	28
1763	55	27
1764	55	29
1765	55	29
1766	55	15
1767	55	12
1768	55	22
1769	55	35
1770	55	26
1771	55	7
1772	55	36
1773	55	25
1774	55	33
1775	56	20
1776	56	18
1777	56	31
1778	56	28
1779	56	15
1780	56	26
1781	56	7
1782	56	19
1783	56	25
1784	56	8
1785	56	23
1786	56	11
1787	56	35
1788	56	13
1789	56	36
1790	56	16
1791	56	29
1792	56	24
1793	57	11
1794	57	13
1795	57	22
1796	57	31
1797	57	24
1798	57	21
1799	57	27
1800	57	17
1801	57	19
1802	57	37
1803	57	25
1804	57	15
1805	57	28
1806	58	22
1807	58	10
1808	58	23
1809	58	13
1810	58	11
1811	58	34
1812	58	20
1813	58	8
1814	58	33
1815	58	21
1816	58	26
1817	58	17
1818	58	7
1819	58	28
1820	58	37
1821	58	9
1822	58	35
1823	58	29
1824	58	18
1825	58	19
1826	58	36
1827	58	15
1828	58	32
1829	58	31
1830	58	14
1831	58	24
1832	58	16
1833	59	21
1834	59	31
1835	59	10
1836	59	25
1837	59	12
1838	59	27
1839	59	19
1840	59	11
1841	59	20
1842	59	37
1843	59	36
1844	59	15
1845	59	14
1846	59	9
1847	59	13
1848	59	7
1849	59	32
1850	59	23
1851	59	26
1852	59	28
1853	59	18
1854	59	34
1855	59	22
1856	59	29
1857	59	33
1858	60	29
1859	60	13
1860	60	17
1861	60	20
1862	60	27
1863	60	37
1864	60	9
1865	60	7
1866	60	18
1867	61	25
1868	61	14
1869	61	31
1870	61	37
1871	61	29
1872	61	22
1873	61	26
1874	61	17
1875	61	12
1876	61	11
1877	61	27
1878	61	10
1879	62	35
1880	62	15
1881	62	12
1882	62	32
1883	62	22
1884	62	9
1885	62	11
1886	62	17
1887	63	35
1888	63	8
1889	63	29
1890	63	37
1891	63	11
1892	63	28
1893	63	20
1894	63	21
1895	63	9
1896	63	33
1897	63	12
1898	63	34
1899	63	22
1900	63	17
1901	63	31
1902	63	13
1903	63	18
1904	63	25
1905	64	24
1906	64	18
1907	64	34
1908	64	9
1909	64	10
1910	64	17
1911	64	14
1912	64	32
1913	64	8
1914	64	21
1915	64	29
1916	64	28
1917	64	20
1918	65	29
1919	65	15
1920	65	23
1921	65	33
1922	65	18
1923	65	16
1924	65	26
1925	65	29
1926	65	25
1927	65	22
1928	65	35
1929	66	25
1930	66	12
1931	66	7
1932	66	16
1933	66	37
1934	66	31
1935	66	14
1936	66	19
1937	66	24
1938	66	32
1939	66	17
1940	66	28
1941	66	35
1942	66	18
1943	66	22
1944	66	36
1945	66	27
1946	66	33
1947	67	8
1948	67	28
1949	67	32
1950	67	11
1951	68	32
1952	68	29
1953	68	21
1954	68	33
1955	68	14
1956	68	29
1957	68	23
1958	68	28
1959	68	24
1960	68	13
1961	68	15
1962	68	10
1963	68	17
1964	68	35
1965	68	18
1966	68	25
1967	68	8
1968	68	22
1969	68	34
1970	68	19
1971	68	36
1972	68	7
1973	6	16
1974	6	33
1975	6	10
1976	6	13
1977	7	29
1978	7	31
1979	7	13
1980	7	20
1981	7	15
1982	7	29
1983	7	35
1984	7	19
1985	7	28
1986	7	7
1987	7	32
1988	7	36
1989	7	14
1990	7	22
1991	9	36
1992	9	27
1993	9	13
1994	9	14
1995	9	29
1996	9	24
1997	9	22
1998	9	35
1999	9	18
2000	9	15
2001	9	12
2002	9	23
2003	9	34
2004	9	31
2005	9	21
2006	9	33
2007	9	16
2008	9	28
2009	9	17
2010	9	25
2011	9	11
2012	9	37
2013	13	28
2014	13	13
2015	13	25
2016	13	37
2017	13	32
2018	13	35
2019	13	10
2020	13	29
2021	13	26
2022	14	24
2023	14	18
2024	14	8
2025	14	17
2026	14	37
2027	14	9
2028	14	28
2029	14	21
2030	14	22
2031	14	34
2032	14	29
2033	14	32
2034	14	16
2035	14	36
2036	14	11
2037	14	20
2038	18	11
2039	18	13
2040	18	10
2041	18	27
2042	18	34
2043	18	18
2044	18	14
2045	18	29
2046	18	12
2047	18	7
2048	18	22
2049	18	24
2050	18	36
2051	18	20
2052	18	37
2053	18	32
2054	18	28
2055	18	8
2056	18	15
2057	18	25
2058	18	17
2059	18	21
2060	18	19
2061	18	33
2062	18	29
2063	18	16
2064	22	7
2065	22	21
2066	22	22
2067	22	10
2068	22	32
2069	22	29
2070	22	20
2071	22	37
2072	22	15
2073	22	35
2074	22	8
2075	22	17
2076	22	18
2077	22	13
2078	22	11
2079	25	15
2080	25	33
2081	25	7
2082	25	27
2083	25	18
2084	25	9
2085	25	11
2086	25	16
2087	25	32
2088	25	35
2089	25	8
2090	25	22
2091	25	37
2092	31	23
2093	31	33
2094	31	12
2095	31	22
2096	31	37
2097	31	13
2098	31	29
2099	31	9
2100	31	17
2101	31	34
2102	31	19
2103	31	8
2104	31	21
2105	31	28
2106	31	35
2107	31	24
2108	31	32
2109	31	16
2110	31	31
2111	31	15
2112	31	36
2113	33	28
2114	33	15
2115	33	29
2116	33	14
2117	33	36
2118	33	8
2119	33	17
2120	37	32
2121	37	20
2122	37	37
2123	37	25
2124	38	34
2125	38	32
2126	38	26
2127	38	25
2128	38	35
2129	38	28
2130	38	22
2131	38	7
2132	38	20
2133	38	33
2134	38	27
2135	38	16
2136	38	24
2137	38	21
2138	38	8
2139	38	23
2140	38	19
2141	38	11
2142	38	37
2143	38	31
2144	38	29
2145	38	15
2146	38	18
2147	38	9
2148	38	10
2149	38	29
2150	38	14
2151	38	12
2152	43	25
2153	43	14
2154	43	24
2155	43	32
2156	43	37
2157	43	7
2158	43	35
2159	43	26
2160	43	29
2161	45	9
2162	45	27
2163	45	33
2164	45	32
2165	45	36
2166	45	24
2167	45	14
2168	45	13
2169	45	17
2170	45	18
2171	45	28
2172	45	22
2173	45	7
2174	45	29
2175	45	31
2176	45	26
2177	45	11
2178	45	15
2179	45	29
2180	45	19
2181	45	35
2182	48	21
2183	48	31
2184	48	8
2185	48	18
2186	48	37
2187	48	34
2188	48	12
2189	48	35
2190	48	22
2191	48	15
2192	48	33
2193	48	32
2194	48	26
2195	48	29
2196	48	29
2197	48	14
2198	48	10
2199	48	23
2200	48	11
2201	48	36
2202	48	17
2203	48	9
2204	48	27
2205	48	24
2206	48	13
2207	48	28
2208	48	7
2209	48	20
2210	52	12
2211	52	27
2212	52	33
2213	52	29
2214	52	7
2215	52	11
2216	52	35
2217	52	29
2218	52	19
2219	52	32
2220	52	16
2221	52	18
2222	52	8
2223	52	21
2224	52	13
2225	52	14
2226	52	36
2227	52	24
2228	52	22
2229	52	20
2230	52	23
2231	52	28
2232	52	9
2233	52	15
2234	53	29
2235	53	33
2236	53	21
2237	53	9
2238	53	18
2239	53	14
2240	53	23
2241	53	13
2242	53	37
2243	53	32
2244	69	27
2245	69	21
2246	69	26
2247	69	11
2248	69	16
2249	69	20
2250	69	12
2251	69	14
2252	69	8
2253	69	17
2254	69	25
2255	69	35
\.


--
-- Name: seen_arguments_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('seen_arguments_uid_seq', 2255, true);


--
-- Data for Name: seen_statements; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY seen_statements (uid, statement_uid, user_uid) FROM stdin;
1464	1	11
1465	1	33
1466	1	29
1467	1	21
1468	1	34
1469	1	37
1470	2	29
1471	2	34
1472	2	33
1473	2	28
1474	2	12
1475	2	13
1476	2	31
1477	2	14
1478	2	29
1479	2	17
1480	2	10
1481	2	15
1482	2	24
1483	2	9
1484	2	20
1485	2	21
1486	2	27
1487	2	7
1488	2	37
1489	2	22
1490	2	26
1491	2	18
1492	2	25
1493	2	23
1494	2	35
1495	3	24
1496	3	34
1497	3	12
1498	3	20
1499	3	31
1500	3	33
1501	4	37
1502	4	13
1503	4	23
1504	4	31
1505	4	12
1506	4	26
1507	4	9
1508	4	11
1509	4	24
1510	4	25
1511	4	8
1512	4	29
1513	4	22
1514	4	20
1515	4	15
1516	4	27
1517	4	10
1518	4	16
1519	4	33
1520	4	21
1521	4	7
1522	4	34
1523	4	36
1524	4	18
1525	4	28
1526	4	19
1527	5	21
1528	5	37
1529	5	35
1530	5	15
1531	5	20
1532	5	26
1533	5	13
1534	5	34
1535	5	7
1536	5	27
1537	6	20
1538	6	14
1539	6	12
1540	6	7
1541	6	9
1542	6	22
1543	6	34
1544	6	27
1545	6	33
1546	6	28
1547	6	17
1548	6	13
1549	6	19
1550	6	29
1551	6	32
1552	7	33
1553	7	27
1554	7	12
1555	7	13
1556	7	14
1557	7	21
1558	7	18
1559	7	20
1560	7	24
1561	7	11
1562	7	31
1563	7	10
1564	7	28
1565	7	15
1566	7	25
1567	7	16
1568	7	37
1569	7	22
1570	8	29
1571	8	7
1572	8	31
1573	8	11
1574	8	24
1575	8	34
1576	8	32
1577	8	33
1578	8	14
1579	8	17
1580	8	25
1581	8	22
1582	8	20
1583	8	9
1584	8	13
1585	8	12
1586	9	11
1587	9	26
1588	9	8
1589	9	12
1590	9	21
1591	9	25
1592	9	22
1593	9	7
1594	9	36
1595	9	23
1596	9	32
1597	9	9
1598	9	14
1599	9	15
1600	9	31
1601	9	33
1602	9	29
1603	9	28
1604	9	24
1605	9	19
1606	9	18
1607	9	16
1608	9	29
1609	9	27
1610	9	34
1611	9	17
1612	10	35
1613	10	28
1614	10	29
1615	10	8
1616	10	33
1617	10	14
1618	10	7
1619	10	22
1620	10	16
1621	10	13
1622	10	15
1623	10	31
1624	10	10
1625	11	23
1626	11	33
1627	11	28
1628	11	9
1629	11	12
1630	12	13
1631	12	31
1632	12	10
1633	12	11
1634	12	35
1635	12	14
1636	13	21
1637	13	22
1638	13	7
1639	13	32
1640	13	19
1641	13	10
1642	13	18
1643	14	19
1644	14	13
1645	14	29
1646	14	23
1647	14	24
1648	14	10
1649	14	32
1650	14	31
1651	14	33
1652	15	35
1653	15	28
1654	15	16
1655	15	33
1656	15	31
1657	15	14
1658	15	29
1659	15	8
1660	15	37
1661	15	20
1662	15	22
1663	15	32
1664	15	17
1665	16	7
1666	16	19
1667	16	9
1668	16	18
1669	16	15
1670	16	35
1671	16	21
1672	16	8
1673	16	17
1674	16	32
1675	16	29
1676	16	12
1677	16	14
1678	16	13
1679	16	16
1680	16	20
1681	16	22
1682	16	27
1683	16	23
1684	17	26
1685	17	33
1686	17	34
1687	17	13
1688	17	35
1689	17	29
1690	17	29
1691	17	18
1692	17	9
1693	17	31
1694	17	7
1695	17	19
1696	17	24
1697	17	37
1698	17	23
1699	17	15
1700	17	10
1701	17	11
1702	17	27
1703	17	20
1704	17	28
1705	17	8
1706	17	21
1707	17	32
1708	17	25
1709	17	36
1710	17	22
1711	18	25
1712	18	15
1713	18	35
1714	18	9
1715	18	16
1716	18	24
1717	18	19
1718	18	20
1719	18	33
1720	18	32
1721	18	12
1722	18	28
1723	18	11
1724	19	20
1725	19	31
1726	19	29
1727	19	21
1728	19	32
1729	19	7
1730	19	22
1731	20	36
1732	20	8
1733	20	29
1734	20	27
1735	20	37
1736	20	26
1737	20	14
1738	20	9
1739	20	20
1740	20	7
1741	20	13
1742	20	15
1743	20	32
1744	20	35
1745	20	21
1746	20	28
1747	20	29
1748	21	17
1749	21	20
1750	21	24
1751	21	25
1752	21	22
1753	21	19
1754	21	9
1755	21	7
1756	21	34
1757	21	21
1758	21	35
1759	21	23
1760	21	36
1761	21	31
1762	22	32
1763	22	9
1764	22	36
1765	22	24
1766	22	33
1767	22	21
1768	22	27
1769	22	7
1770	22	29
1771	22	11
1772	22	18
1773	22	25
1774	22	26
1775	22	8
1776	22	28
1777	22	13
1778	22	37
1779	22	10
1780	22	20
1781	22	31
1782	22	35
1783	23	32
1784	23	28
1785	23	17
1786	23	7
1787	23	36
1788	23	24
1789	23	27
1790	23	11
1791	23	29
1792	23	8
1793	23	20
1794	23	25
1795	23	14
1796	23	21
1797	23	23
1798	23	31
1799	23	15
1800	23	13
1801	23	18
1802	23	35
1803	23	33
1804	23	16
1805	23	12
1806	23	22
1807	24	25
1808	24	29
1809	24	7
1810	24	8
1811	24	22
1812	24	14
1813	24	32
1814	24	26
1815	24	20
1816	24	31
1817	24	15
1818	24	23
1819	24	28
1820	24	37
1821	24	35
1822	24	13
1823	24	21
1824	24	12
1825	24	9
1826	24	24
1827	24	36
1828	24	29
1829	24	33
1830	24	18
1831	24	16
1832	24	17
1833	24	10
1834	25	28
1835	25	13
1836	25	15
1837	25	29
1838	25	8
1839	25	29
1840	25	35
1841	25	14
1842	25	22
1843	26	32
1844	26	35
1845	26	21
1846	26	19
1847	26	24
1848	27	20
1849	27	11
1850	27	31
1851	27	17
1852	27	16
1853	27	12
1854	27	35
1855	27	26
1856	27	29
1857	27	15
1858	27	7
1859	27	32
1860	27	13
1861	27	33
1862	27	34
1863	27	25
1864	27	24
1865	27	9
1866	27	19
1867	27	10
1868	27	22
1869	27	36
1870	27	14
1871	28	18
1872	28	17
1873	28	33
1874	28	31
1875	28	15
1876	28	26
1877	28	37
1878	28	28
1879	28	29
1880	28	27
1881	28	10
1882	28	14
1883	28	7
1884	28	36
1885	28	11
1886	28	19
1887	29	14
1888	29	26
1889	29	29
1890	29	21
1891	29	29
1892	29	11
1893	29	9
1894	30	18
1895	30	25
1896	30	10
1897	30	14
1898	30	35
1899	30	23
1900	30	26
1901	30	8
1902	30	17
1903	30	9
1904	30	20
1905	30	28
1906	30	16
1907	30	34
1908	30	19
1909	30	13
1910	30	21
1911	30	32
1912	30	27
1913	30	37
1914	30	29
1915	30	33
1916	31	12
1917	31	25
1918	31	37
1919	31	13
1920	31	9
1921	31	21
1922	31	29
1923	32	21
1924	32	37
1925	32	22
1926	32	19
1927	32	36
1928	32	34
1929	32	14
1930	32	13
1931	32	17
1932	32	23
1933	32	32
1934	32	12
1935	32	29
1936	32	35
1937	32	20
1938	32	25
1939	32	9
1940	32	27
1941	32	26
1942	32	28
1943	32	10
1944	32	31
1945	32	29
1946	32	8
1947	32	33
1948	32	7
1949	32	11
1950	32	24
1951	32	16
1952	33	29
1953	33	12
1954	33	8
1955	33	21
1956	33	23
1957	33	13
1958	33	19
1959	33	24
1960	33	15
1961	33	29
1962	33	32
1963	33	34
1964	33	14
1965	33	10
1966	33	28
1967	33	7
1968	33	22
1969	33	25
1970	33	26
1971	33	9
1972	33	35
1973	33	31
1974	33	17
1975	33	37
1976	33	16
1977	34	8
1978	34	28
1979	34	10
1980	34	19
1981	34	24
1982	34	35
1983	34	22
1984	34	16
1985	35	25
1986	35	14
1987	35	33
1988	35	15
1989	35	13
1990	35	18
1991	35	23
1992	35	28
1993	35	11
1994	36	7
1995	36	33
1996	36	19
1997	36	35
1998	36	36
1999	36	8
2000	37	35
2001	37	11
2002	37	14
2003	37	13
2004	37	12
2005	37	10
2006	37	16
2007	37	33
2008	37	17
2009	37	15
2010	37	25
2011	37	29
2012	37	21
2013	37	7
2014	38	31
2015	38	36
2016	38	9
2017	38	35
2018	38	20
2019	38	29
2020	38	22
2021	38	29
2022	38	16
2023	38	37
2024	38	15
2025	38	13
2026	38	28
2027	38	17
2028	39	23
2029	39	36
2030	39	27
2031	39	15
2032	39	32
2033	39	10
2034	39	19
2035	39	24
2036	39	28
2037	39	34
2038	39	14
2039	39	9
2040	39	8
2041	39	20
2042	39	29
2043	39	21
2044	39	29
2045	39	13
2046	39	33
2047	39	11
2048	39	17
2049	39	26
2050	40	16
2051	40	20
2052	40	35
2053	40	29
2054	40	12
2055	40	37
2056	40	36
2057	40	27
2058	40	31
2059	40	33
2060	40	25
2061	40	13
2062	40	19
2063	40	17
2064	40	23
2065	40	8
2066	40	21
2067	40	29
2068	40	7
2069	40	14
2070	40	24
2071	40	10
2072	40	15
2073	40	34
2074	40	11
2075	40	26
2076	40	22
2077	40	18
2078	40	9
2079	41	24
2080	41	11
2081	41	27
2082	41	36
2083	41	19
2084	41	13
2085	42	26
2086	42	21
2087	42	33
2088	42	24
2089	42	16
2090	42	22
2091	42	32
2092	42	19
2093	42	28
2094	42	20
2095	42	11
2096	42	27
2097	42	37
2098	42	8
2099	42	29
2100	42	23
2101	42	17
2102	42	13
2103	42	14
2104	42	29
2105	42	35
2106	42	25
2107	42	9
2108	42	31
2109	42	15
2110	42	18
2111	42	12
2112	42	7
2113	43	33
2114	43	18
2115	43	11
2116	43	34
2117	43	37
2118	43	29
2119	43	25
2120	43	13
2121	43	23
2122	43	22
2123	43	10
2124	43	29
2125	43	8
2126	43	19
2127	43	14
2128	43	12
2129	43	17
2130	43	28
2131	43	31
2132	43	36
2133	43	35
2134	43	9
2135	43	16
2136	43	27
2137	43	26
2138	43	7
2139	43	32
2140	44	25
2141	44	32
2142	44	29
2143	44	31
2144	44	27
2145	44	22
2146	44	10
2147	44	36
2148	44	21
2149	44	9
2150	44	14
2151	45	14
2152	45	16
2153	45	13
2154	45	23
2155	45	27
2156	45	12
2157	45	19
2158	45	18
2159	45	20
2160	45	15
2161	45	24
2162	45	29
2163	45	8
2164	45	33
2165	45	11
2166	45	35
2167	45	28
2168	45	22
2169	45	21
2170	45	31
2171	45	34
2172	45	17
2173	45	7
2174	45	36
2175	45	37
2176	45	25
2177	45	10
2178	45	29
2179	45	26
2180	46	11
2181	46	36
2182	46	35
2183	46	14
2184	46	31
2185	46	15
2186	46	33
2187	46	16
2188	46	23
2189	46	10
2190	46	22
2191	46	8
2192	46	21
2193	46	34
2194	46	12
2195	46	29
2196	46	28
2197	46	29
2198	46	9
2199	47	16
2200	47	10
2201	47	27
2202	47	28
2203	47	32
2204	48	32
2205	48	21
2206	48	22
2207	48	37
2208	48	35
2209	48	23
2210	48	25
2211	48	19
2212	48	27
2213	48	28
2214	48	33
2215	48	11
2216	48	36
2217	48	14
2218	48	13
2219	48	34
2220	48	9
2221	48	31
2222	48	10
2223	48	16
2224	48	29
2225	48	8
2226	48	18
2227	49	8
2228	49	11
2229	49	31
2230	49	7
2231	49	37
2232	49	32
2233	49	23
2234	49	12
2235	49	29
2236	49	10
2237	49	15
2238	49	13
2239	49	25
2240	50	29
2241	50	35
2242	50	22
2243	50	25
2244	50	9
2245	50	29
2246	50	24
2247	50	18
2248	50	34
2249	50	31
2250	50	33
2251	50	8
2252	50	17
2253	50	19
2254	51	22
2255	51	20
2256	51	36
2257	51	26
2258	51	9
2259	51	32
2260	51	8
2261	51	34
2262	51	21
2263	51	29
2264	51	31
2265	51	7
2266	51	16
2267	51	10
2268	51	33
2269	51	29
2270	51	35
2271	51	15
2272	51	18
2273	51	13
2274	51	11
2275	51	37
2276	51	19
2277	51	27
2278	51	17
2279	52	34
2280	52	21
2281	52	27
2282	52	33
2283	52	17
2284	52	24
2285	52	12
2286	52	18
2287	52	15
2288	52	9
2289	52	29
2290	52	25
2291	52	11
2292	52	26
2293	52	14
2294	52	10
2295	52	20
2296	52	32
2297	52	28
2298	52	31
2299	53	15
2300	53	13
2301	53	31
2302	53	21
2303	53	29
2304	54	17
2305	54	13
2306	54	16
2307	54	19
2308	54	32
2309	54	18
2310	54	12
2311	54	24
2312	54	7
2313	54	36
2314	54	27
2315	54	29
2316	54	15
2317	54	8
2318	54	9
2319	54	29
2320	54	25
2321	54	33
2322	54	10
2323	54	34
2324	54	11
2325	54	23
2326	54	31
2327	54	20
2328	54	14
2329	54	26
2330	55	14
2331	55	23
2332	55	32
2333	55	33
2334	55	12
2335	55	18
2336	55	28
2337	55	36
2338	55	25
2339	55	11
2340	55	20
2341	55	10
2342	55	22
2343	55	29
2344	55	29
2345	55	31
2346	55	37
2347	55	7
2348	56	8
2349	56	7
2350	56	32
2351	56	20
2352	56	19
2353	56	22
2354	56	37
2355	56	31
2356	56	26
2357	56	14
2358	56	21
2359	56	24
2360	56	17
2361	57	33
2362	57	20
2363	57	28
2364	57	12
2365	57	37
2366	58	22
2367	58	13
2368	58	34
2369	58	33
2370	58	23
2371	58	12
2372	58	16
2373	58	32
2374	58	35
2375	58	8
2376	58	25
2377	58	36
2378	58	29
2379	58	18
2380	58	7
2381	58	27
2382	58	9
2383	59	33
2384	59	13
2385	59	31
2386	59	8
2387	59	19
2388	60	13
2389	60	15
2390	60	8
2391	60	28
2392	60	10
2393	60	32
2394	60	26
2395	60	9
2396	60	20
2397	60	7
2398	60	21
2399	60	27
2400	60	12
2401	60	37
2402	60	35
2403	61	10
2404	61	31
2405	61	29
2406	61	13
2407	61	8
2408	61	36
2409	61	14
2410	61	29
2411	61	15
2412	61	28
2413	61	27
2414	61	16
2415	61	24
2416	61	26
2417	61	7
2418	61	9
2419	61	32
2420	62	31
2421	62	33
2422	62	36
2423	62	25
2424	62	28
2425	62	29
2426	62	29
2427	62	17
2428	62	26
2429	62	15
2430	62	22
2431	62	16
2432	62	10
2433	62	32
2434	62	35
2435	62	8
2436	62	23
2437	62	18
2438	62	24
2439	62	11
2440	62	12
2441	62	13
2442	62	20
2443	63	31
2444	63	33
2445	63	26
2446	63	16
2447	63	15
2448	64	29
2449	64	32
2450	64	16
2451	64	31
2452	64	29
2453	64	27
2454	64	15
2455	64	28
2456	64	23
2457	64	35
2458	64	24
2459	64	37
2460	64	8
2461	64	26
2462	64	22
2463	64	14
2464	64	19
2465	64	13
2466	64	18
2467	64	33
2468	65	29
2469	65	29
2470	65	16
2471	65	34
2472	65	26
2473	65	22
2474	65	23
2475	65	15
2476	65	27
2477	65	31
2478	65	10
2479	65	36
2480	65	11
2481	66	8
2482	66	7
2483	66	25
2484	66	18
2485	66	21
2486	66	23
2487	66	32
2488	66	35
2489	66	24
2490	66	29
2491	66	29
2492	66	13
2493	66	19
2494	66	37
2495	66	11
2496	66	28
2497	66	36
2498	66	26
2499	66	10
2500	66	20
2501	66	9
2502	66	15
2503	66	31
2504	66	17
2505	66	14
2506	66	34
2507	66	27
2508	66	16
2509	67	16
2510	67	14
2511	67	17
2512	67	26
2513	67	24
2514	67	32
2515	67	15
2516	67	29
2517	67	20
2518	67	33
2519	68	14
2520	68	16
2521	68	15
2522	68	11
2523	68	29
2524	68	26
2525	68	34
2526	68	28
2527	68	17
2528	68	22
2529	68	33
2530	68	29
2531	69	24
2532	69	25
2533	69	18
2534	69	29
2535	69	37
2536	69	22
2537	69	17
2538	69	8
2539	69	10
2540	69	9
2541	69	21
2542	69	34
2543	69	14
2544	69	36
2545	69	19
2546	69	27
2547	69	23
2548	69	20
2549	69	29
2550	69	12
2551	70	7
2552	70	37
2553	70	28
2554	70	14
2555	70	36
2556	70	22
2557	70	20
2558	70	12
2559	70	18
2560	70	16
2561	70	31
2562	70	19
2563	70	8
2564	70	11
2565	70	10
2566	70	17
2567	70	15
2568	70	26
2569	71	17
2570	71	12
2571	71	11
2572	71	37
2573	71	33
2574	71	31
2575	71	15
2576	71	36
2577	72	24
2578	72	28
2579	72	14
2580	72	29
2581	72	25
2582	72	31
2583	72	34
2584	72	8
2585	72	15
2586	72	32
2587	72	7
2588	72	17
2589	72	36
2590	72	22
2591	72	12
2592	72	20
2593	72	35
2594	72	10
2595	72	9
2596	72	23
2597	72	16
2598	72	26
2599	72	18
2600	72	33
2601	72	29
2602	72	11
2603	72	19
2604	72	27
2605	73	19
2606	73	21
2607	73	14
2608	73	18
2609	73	10
2610	73	20
2611	74	27
2612	74	28
2613	74	7
2614	74	12
2615	74	9
2616	74	18
2617	74	13
2618	74	25
2619	74	29
2620	74	33
2621	74	26
2622	74	23
2623	74	8
2624	74	31
2625	74	14
2626	74	24
2627	74	17
2628	74	15
2629	74	36
2630	74	10
2631	74	19
2632	74	32
2633	74	20
2634	74	34
2635	74	11
2636	74	37
2637	75	18
2638	75	8
2639	75	19
2640	75	11
2641	75	36
2642	75	31
2643	75	29
2644	75	32
2645	75	29
2646	75	10
2647	75	28
2648	75	26
2649	75	23
2650	75	9
2651	75	34
2652	75	21
2653	75	35
2654	75	16
2655	75	22
2656	75	7
2657	75	13
2658	75	33
2659	75	24
2660	75	14
2661	75	37
2662	75	25
2663	75	15
2664	76	8
2665	76	15
2666	76	11
2667	76	35
2668	76	34
2669	76	29
2670	76	36
2671	76	7
2672	76	14
2673	76	32
2674	76	31
2675	76	9
2676	76	28
2677	76	24
2678	76	23
2679	76	37
2680	76	20
2681	76	26
2682	76	17
2683	76	12
2684	76	29
2685	76	21
2686	76	18
2687	76	13
2688	76	16
2689	76	27
2690	76	22
2691	76	33
2692	77	26
2693	77	36
2694	77	37
2695	77	21
2696	77	10
2697	77	35
2698	77	24
2699	77	14
2700	77	29
2701	77	32
2702	77	15
2703	77	31
2704	77	11
2705	77	28
2706	77	25
2707	77	34
2708	77	7
2709	77	23
2710	77	22
2711	77	17
2712	77	12
2713	77	20
2714	77	18
2715	77	19
2716	77	9
2717	78	34
2718	78	11
2719	78	27
2720	78	17
2721	78	15
2722	79	24
2723	79	33
2724	79	21
2725	79	19
2726	79	11
2727	79	16
2728	79	14
2729	79	12
2730	79	7
2731	79	34
2732	79	20
2733	79	13
2734	79	37
2735	79	28
2736	79	25
2737	79	31
2738	79	8
2739	79	26
2740	79	10
2741	79	36
2742	79	32
2743	79	23
2744	79	22
2745	79	29
2746	80	10
2747	80	25
2748	80	29
2749	80	8
2750	80	13
2751	80	21
2752	80	17
2753	80	27
2754	80	24
2755	80	34
2756	80	26
2757	80	36
2758	80	31
2759	80	23
2760	80	9
2761	80	22
2762	81	31
2763	81	14
2764	81	7
2765	81	36
2766	82	22
2767	82	18
2768	82	21
2769	82	17
2770	82	19
2771	82	8
2772	82	33
2773	82	7
2774	82	15
2775	82	26
2776	82	34
2777	82	20
2778	82	31
\.


--
-- Name: seen_statements_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('seen_statements_uid_seq', 2778, true);


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
1	Ein Radar überwacht den Abstand, eine Frontkamera erkennt Fahrspuren und andere Verkehrsteilnehmer, und je sechs Ultraschallsensoren vorne und hinten helfen beim Einparken und messen während der Fahrt Distanzen im Zentimeterbereich	localhost:3449	/devcards/index.html	5	68	4	2017-08-19 11:25:08.482712
2	Zunächst einmal unterscheidet sich die Hardware für den Autopiloten nicht oder nur marginal von dem, was selbst für einen VW Polo erhältlich ist	localhost:3449	/	5	68	4	2017-08-19 11:25:08.482712
3	Katzen sind kleine Tiger	http://www.iflscience.com/	plants-and-animals/no-your-cat-isnt-plotting-kill-youbut-it-has-lions-personality/	2	15	2	2017-08-19 11:25:08.482712
4	Katzen sind kleine Tiger	http://www.iflscience.com/	plants-and-animals/no-your-cat-isnt-plotting-kill-youbut-it-has-lions-personality/	2	16	2	2017-08-19 11:25:08.482712
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

COPY statements (uid, is_startpoint, issue_uid, is_disabled) FROM stdin;
1	t	2	t
2	t	2	f
3	t	2	f
4	t	2	f
5	f	2	f
6	f	2	f
7	f	2	f
8	f	2	f
9	f	2	f
10	f	2	f
11	f	2	f
12	f	2	f
13	f	2	f
14	f	2	f
15	f	2	f
16	f	2	f
17	f	2	f
18	f	2	f
19	f	2	f
20	f	2	f
21	f	2	f
22	f	2	f
23	f	2	f
24	f	2	f
25	f	2	f
26	f	2	f
27	f	2	f
28	f	2	f
29	f	2	f
30	f	2	f
31	f	2	f
32	f	2	f
33	f	2	f
34	f	2	f
35	f	2	f
36	t	1	f
37	t	1	f
38	t	1	f
39	f	1	f
40	f	1	f
41	f	1	f
42	f	1	f
43	f	1	f
44	f	1	f
45	f	1	f
46	f	1	f
47	f	1	f
48	f	1	f
49	f	1	f
50	f	1	f
51	f	1	f
52	f	1	f
53	f	1	f
54	f	1	f
55	f	1	f
56	f	1	f
57	f	1	f
58	t	4	f
59	f	4	f
60	f	4	f
61	f	4	f
62	f	4	f
63	f	4	f
64	f	4	f
65	f	4	f
66	f	4	f
67	t	4	f
68	f	4	f
69	t	5	f
70	t	5	f
71	f	5	f
72	f	5	f
73	f	5	f
74	f	5	f
75	f	5	f
76	t	7	f
77	f	7	f
78	f	7	f
79	f	7	f
80	f	7	f
81	f	7	f
82	f	7	f
\.


--
-- Name: statements_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('statements_uid_seq', 82, true);


--
-- Data for Name: textversions; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY textversions (uid, statement_uid, content, author_uid, "timestamp", is_disabled) FROM stdin;
1	2	we should get a cat	1	2017-08-03 11:25:09.221826	f
2	3	we should get a dog	1	2017-08-19 11:25:09.221927	f
3	4	we could get both, a cat and a dog	1	2017-08-06 11:25:09.221967	f
4	5	cats are very independent	1	2017-08-19 11:25:09.222	f
5	6	cats are capricious	1	2017-08-05 11:25:09.222032	f
6	7	dogs can act as watch dogs	1	2017-07-28 11:25:09.222062	f
7	8	you have to take the dog for a walk every day, which is tedious	1	2017-07-31 11:25:09.222092	f
8	9	we have no use for a watch dog	1	2017-08-01 11:25:09.222122	f
9	10	going for a walk with the dog every day is good for social interaction and physical exercise	1	2017-07-29 11:25:09.222151	f
10	11	it would be no problem	1	2017-07-29 11:25:09.22218	f
11	12	a cat and a dog will generally not get along well	1	2017-08-06 11:25:09.222209	f
12	13	we do not have enough money for two pets	1	2017-08-09 11:25:09.222238	f
13	14	a dog costs taxes and will be more expensive than a cat	1	2017-08-14 11:25:09.222266	f
14	15	cats are fluffy	1	2017-08-13 11:25:09.222295	f
15	16	cats are small	1	2017-08-04 11:25:09.222347	f
16	17	fluffy animals losing much hair and I'm allergic to animal hair	1	2017-08-10 11:25:09.222389	f
17	18	you could use a automatic vacuum cleaner	1	2017-08-07 11:25:09.222417	f
18	19	cats ancestors are animals in wildlife, who are hunting alone and not in groups	1	2017-07-25 11:25:09.222444	f
19	20	this is not true for overbred races	1	2017-08-19 11:25:09.222471	f
20	21	this lies in their the natural conditions	1	2017-07-26 11:25:09.222499	f
21	22	the purpose of a pet is to have something to take care of	1	2017-07-27 11:25:09.222537	f
22	23	several cats of friends of mine are real as*holes	1	2017-08-12 11:25:09.222576	f
23	24	the fact, that cats are capricious, is based on the cats race	1	2017-08-09 11:25:09.222604	f
24	25	not every cat is capricious	1	2017-08-08 11:25:09.222631	f
25	26	this is based on the cats race and a little bit on the breeding	1	2017-08-13 11:25:09.222659	f
26	27	next to the taxes you will need equipment like a dog lead, anti-flea-spray, and so on	1	2017-08-09 11:25:09.222687	f
27	28	the equipment for running costs of cats and dogs are nearly the same	1	2017-08-04 11:25:09.222714	f
28	29	this is just a claim without any justification	1	2017-08-04 11:25:09.222742	f
29	30	in Germany you have to pay for your second dog even more taxes!	1	2017-07-29 11:25:09.222769	f
30	31	it is important, that pets are small and fluffy!	1	2017-08-16 11:25:09.222796	f
31	32	cats are little, sweet and innocent cuddle toys	1	2017-08-06 11:25:09.222823	f
32	33	do you have ever seen a sphinx cat or savannah cats?	1	2017-08-07 11:25:09.222851	f
33	34	it is much work to take care of both animals	1	2017-07-31 11:25:09.222878	f
34	35	won't be best friends	1	2017-08-13 11:25:09.222906	f
35	36	the city should reduce the number of street festivals	3	2017-08-12 11:25:09.222933	f
36	37	we should shut down University Park	3	2017-08-05 11:25:09.22296	f
37	38	we should close public swimming pools	1	2017-08-15 11:25:09.222988	f
38	39	reducing the number of street festivals can save up to $50.000 a year	1	2017-08-06 11:25:09.223015	f
39	40	every street festival is funded by large companies	1	2017-07-29 11:25:09.223042	f
40	41	then we will have more money to expand out pedestrian zone	1	2017-07-29 11:25:09.22307	f
41	42	our city will get more attractive for shopping	1	2017-08-10 11:25:09.223098	f
42	43	street festivals attract many people, which will increase the citys income	1	2017-07-26 11:25:09.223126	f
43	44	spending of the city for these festivals are higher than the earnings	1	2017-08-13 11:25:09.223153	f
44	45	money does not solve problems of our society	1	2017-08-04 11:25:09.22318	f
45	46	criminals use University Park to sell drugs	1	2017-07-29 11:25:09.223207	f
46	47	shutting down University Park will save $100.000 a year	1	2017-08-12 11:25:09.223234	f
47	48	we should not give in to criminals	1	2017-08-15 11:25:09.223261	f
48	49	the number of police patrols has been increased recently	1	2017-07-27 11:25:09.223288	f
49	50	this is the only park in our city	1	2017-08-11 11:25:09.223315	f
50	51	there are many parks in neighbouring towns	1	2017-08-01 11:25:09.223342	f
51	52	the city is planing a new park in the upcoming month	3	2017-07-28 11:25:09.223369	f
52	53	parks are very important for our climate	3	2017-08-10 11:25:09.223396	f
53	54	our swimming pools are very old and it would take a major investment to repair them	3	2017-08-17 11:25:09.223424	f
54	55	schools need the swimming pools for their sports lessons	1	2017-07-25 11:25:09.223451	f
55	56	the rate of non-swimmers is too high	1	2017-08-02 11:25:09.223479	f
56	57	the police cannot patrol in the park for 24/7	1	2017-08-13 11:25:09.223506	f
57	58	E-Autos "optimal" für den Stadtverkehr sind	1	2017-08-10 11:25:09.223533	f
58	59	dadurch die Lärmbelästigung in der Stadt sinkt	1	2017-08-08 11:25:09.223559	f
77	77	Straßenfeste viel Lärm verursachen	1	2017-07-25 11:25:09.22408	f
59	60	die Anzahl an Ladestationen in der Stadt nicht ausreichend ist	1	2017-08-01 11:25:09.223586	f
60	61	das Unfallrisiko steigt, da die Autos kaum Geräusche verursachen	1	2017-08-07 11:25:09.223613	f
61	62	die Autos auch zuhause geladen werden können und das pro Tag ausreichen sollte	1	2017-08-16 11:25:09.223641	f
62	63	Elektroautos keine lauten Geräusche beim Anfahren produzieren	1	2017-07-29 11:25:09.223668	f
63	64	Lärmbelästigung kein wirkliches Problem in den Städten ist	1	2017-08-06 11:25:09.223696	f
64	65	nicht jede normale Tankstelle auch Stromtankstellen hat	1	2017-08-17 11:25:09.223723	f
65	66	die Länder und Kommunen den Ausbau nun stark fördern wollen	1	2017-08-04 11:25:09.223751	f
66	67	E-Autos das autonome Fahren vorantreiben	5	2017-08-19 11:25:09.223778	f
67	68	Tesla mutig bestehende Techniken einsetzt und zeigt was sie können	5	2017-07-30 11:25:09.223806	f
68	69	durch rücksichtsvolle Verhaltensanpassungen der wissenschaftlichen Mitarbeitenden der Arbeitsaufwand der Sekretärinnen gesenkt werden könnte	1	2017-08-14 11:25:09.223833	f
69	70	wir Standard-Formulare, wie Urlaubsanträge, selbst faxen können	1	2017-08-12 11:25:09.223861	f
70	71	etliche Abläufe durch ein besseres Zusammenarbeiten optimiert werden können. Dies sollte auch schriftlich als Anleitungen festgehalten werden, damit neue Angestellt einen leichten Einstieg finden	1	2017-08-02 11:25:09.223889	f
71	72	viele Arbeiten auch durch die Mitarbeiter erledigt werden können	1	2017-08-12 11:25:09.223916	f
72	73	"rücksichtsvolle Verhaltensanpassungen" viel zu allgemein gehalten ist	1	2017-08-01 11:25:09.223943	f
73	74	das Faxgerät nicht immer zugänglich ist, wenn die Sekretärinnen nicht anwesend sind	1	2017-08-02 11:25:09.22397	f
74	75	wir keine eigenen Faxgeräte haben und so oder so entweder bei Martin stören müssten oder doch bei Sabine im Büro landen würden	1	2017-08-03 11:25:09.223998	f
75	1	Cats are fucking stupid and bloody fuzzy critters!	1	2017-08-06 11:25:09.224025	f
76	76	Die Anzahl der Straßenfeste sollte reduziert werden	1	2017-08-17 11:25:09.224052	f
78	78	Straßenfeste ein wichtiger Bestandteil unserer Kultur sind	1	2017-08-06 11:25:09.224108	f
79	79	Straßenfeste der Kommune Geld einbringen	1	2017-08-05 11:25:09.224135	f
80	80	die Einnahmen der Kommune durch Straßenfeste nur gering sind	1	2017-08-13 11:25:09.224162	f
81	81	Straßenfeste der Kommune hohe Kosten verursachen durch Polizeieinsätze, Säuberung, etc.	1	2017-08-01 11:25:09.224189	f
82	82	die Innenstadt ohnehin sehr laut ist	1	2017-08-03 11:25:09.224216	f
\.


--
-- Name: textversions_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('textversions_uid_seq', 82, true);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY users (uid, firstname, surname, nickname, public_nickname, email, gender, password, group_uid, last_action, last_login, registered, token, token_timestamp) FROM stdin;
1	anonymous	anonymous	anonymous	anonymous		m	$2a$10$6SJJ6ibhXwWs83GvlFSMe.4NZBZZXlp7lD9CgdeqRCkgYLBN2/w9e	3	2017-08-19 11:25:09.058735	2017-08-19 11:25:09.058853	2017-08-19 11:25:09.058907		\N
2	Tobias	Krauthoff	Tobias	Tobias	krauthoff@cs.uni-duesseldorf.de	m	$2a$10$9P5biPvyX2xVeMcCLm82tO0XFQhmdMFwgAhPaUkCHoVL1F5kEAjIa	1	2017-08-19 11:25:09.059	2017-08-19 11:25:09.059061	2017-08-19 11:25:09.059115		\N
3	Christian	Meter	Christian	Christian	meter@cs.uni-duesseldorf.de	m	$2a$10$Ou/pHV1MoZRqvt5U8cV09up0qqbIz70ZjwEeanRkyyfR/rrMHcBfe	1	2017-08-19 11:25:09.059193	2017-08-19 11:25:09.059239	2017-08-19 11:25:09.059284		\N
5	Teresa	Uebber	Teresa	Teresa	teresa.uebber@uni-duesseldorf.de	f	$2a$10$sVQFxayuieT.vpmNcmyUSeGwnKUYfP3QawEq/YRLPaXJPDSsRvPbe	1	2017-08-19 11:25:09.064404	2017-08-19 11:25:09.064454	2017-08-19 11:25:09.064502		\N
6	Bob	Bubbles	Bob	Bob	tobias.krauthoff+dbas.usert31@gmail.com	n	$2a$10$82Prq3AVM9SPmRexBbBiV.1BBxptoTdL2f7WRRbQ5oAbtoghkAigi	1	2017-08-19 11:25:09.064586	2017-08-19 11:25:09.064635	2017-08-19 11:25:09.064683		\N
7	Pascal	Lux	Pascal	Pascal	tobias.krauthoff+dbas.usert00@gmail.com	m	$2a$10$82Prq3AVM9SPmRexBbBiV.1BBxptoTdL2f7WRRbQ5oAbtoghkAigi	3	2017-08-19 11:25:09.064869	2017-08-19 11:25:09.064921	2017-08-19 11:25:09.064967		\N
8	Kurt	Hecht	Kurt	Kurt	tobias.krauthoff+dbas.usert01@gmail.com	m	$2a$10$82Prq3AVM9SPmRexBbBiV.1BBxptoTdL2f7WRRbQ5oAbtoghkAigi	3	2017-08-19 11:25:09.065045	2017-08-19 11:25:09.065092	2017-08-19 11:25:09.065136		\N
9	Torben	Hartl	Torben	Torben	tobias.krauthoff+dbas.usert02@gmail.com	m	$2a$10$82Prq3AVM9SPmRexBbBiV.1BBxptoTdL2f7WRRbQ5oAbtoghkAigi	3	2017-08-19 11:25:09.065212	2017-08-19 11:25:09.065259	2017-08-19 11:25:09.065304		\N
10	Thorsten	Scherer	Thorsten	Thorsten	tobias.krauthoff+dbas.usert03@gmail.com	m	$2a$10$82Prq3AVM9SPmRexBbBiV.1BBxptoTdL2f7WRRbQ5oAbtoghkAigi	3	2017-08-19 11:25:09.06538	2017-08-19 11:25:09.065427	2017-08-19 11:25:09.065471		\N
11	Friedrich	Schutte	Friedrich	Friedrich	tobias.krauthoff+dbas.usert04@gmail.com	m	$2a$10$82Prq3AVM9SPmRexBbBiV.1BBxptoTdL2f7WRRbQ5oAbtoghkAigi	3	2017-08-19 11:25:09.065547	2017-08-19 11:25:09.065593	2017-08-19 11:25:09.065637		\N
12	Aayden	Westermann	Aayden	Aayden	tobias.krauthoff+dbas.usert05@gmail.com	m	$2a$10$82Prq3AVM9SPmRexBbBiV.1BBxptoTdL2f7WRRbQ5oAbtoghkAigi	3	2017-08-19 11:25:09.065713	2017-08-19 11:25:09.065759	2017-08-19 11:25:09.065803		\N
13	Hermann	Grasshoff	Hermann	Hermann	tobias.krauthoff+dbas.usert06@gmail.com	m	$2a$10$82Prq3AVM9SPmRexBbBiV.1BBxptoTdL2f7WRRbQ5oAbtoghkAigi	3	2017-08-19 11:25:09.065877	2017-08-19 11:25:09.065924	2017-08-19 11:25:09.065968		\N
14	Wolf	Himmler	Wolf	Wolf	tobias.krauthoff+dbas.usert07@gmail.com	m	$2a$10$82Prq3AVM9SPmRexBbBiV.1BBxptoTdL2f7WRRbQ5oAbtoghkAigi	3	2017-08-19 11:25:09.066042	2017-08-19 11:25:09.066088	2017-08-19 11:25:09.066132		\N
15	Jakob	Winter	Jakob	Jakob	tobias.krauthoff+dbas.usert08@gmail.com	m	$2a$10$82Prq3AVM9SPmRexBbBiV.1BBxptoTdL2f7WRRbQ5oAbtoghkAigi	3	2017-08-19 11:25:09.066206	2017-08-19 11:25:09.066252	2017-08-19 11:25:09.066296		\N
16	Alwin	Wechter	Alwin	Alwin	tobias.krauthoff+dbas.usert09@gmail.com	m	$2a$10$82Prq3AVM9SPmRexBbBiV.1BBxptoTdL2f7WRRbQ5oAbtoghkAigi	3	2017-08-19 11:25:09.066419	2017-08-19 11:25:09.066467	2017-08-19 11:25:09.066512		\N
17	Walter	Weisser	Walter	Walter	tobias.krauthoff+dbas.usert10@gmail.com	m	$2a$10$82Prq3AVM9SPmRexBbBiV.1BBxptoTdL2f7WRRbQ5oAbtoghkAigi	3	2017-08-19 11:25:09.066586	2017-08-19 11:25:09.066632	2017-08-19 11:25:09.066676		\N
18	Volker	Keitel	Volker	Volker	tobias.krauthoff+dbas.usert11@gmail.com	m	$2a$10$82Prq3AVM9SPmRexBbBiV.1BBxptoTdL2f7WRRbQ5oAbtoghkAigi	3	2017-08-19 11:25:09.066763	2017-08-19 11:25:09.066811	2017-08-19 11:25:09.066857		\N
19	Benedikt	Feuerstein	Benedikt	Benedikt	tobias.krauthoff+dbas.usert12@gmail.com	m	$2a$10$82Prq3AVM9SPmRexBbBiV.1BBxptoTdL2f7WRRbQ5oAbtoghkAigi	3	2017-08-19 11:25:09.066937	2017-08-19 11:25:09.066985	2017-08-19 11:25:09.067031		\N
20	Engelbert	Gottlieb	Engelbert	Engelbert	tobias.krauthoff+dbas.usert13@gmail.com	m	$2a$10$82Prq3AVM9SPmRexBbBiV.1BBxptoTdL2f7WRRbQ5oAbtoghkAigi	3	2017-08-19 11:25:09.067107	2017-08-19 11:25:09.067154	2017-08-19 11:25:09.0672		\N
21	Elias	Auerbach	Elias	Elias	tobias.krauthoff+dbas.usert14@gmail.com	m	$2a$10$82Prq3AVM9SPmRexBbBiV.1BBxptoTdL2f7WRRbQ5oAbtoghkAigi	3	2017-08-19 11:25:09.067276	2017-08-19 11:25:09.067331	2017-08-19 11:25:09.067374		\N
22	Rupert	Wenz	Rupert	Rupert	tobias.krauthoff+dbas.usert15@gmail.com	m	$2a$10$82Prq3AVM9SPmRexBbBiV.1BBxptoTdL2f7WRRbQ5oAbtoghkAigi	3	2017-08-19 11:25:09.067459	2017-08-19 11:25:09.067524	2017-08-19 11:25:09.067569		\N
23	Marga	Wegscheider	Marga	Marga	tobias.krauthoff+dbas.usert16@gmail.com	f	$2a$10$82Prq3AVM9SPmRexBbBiV.1BBxptoTdL2f7WRRbQ5oAbtoghkAigi	3	2017-08-19 11:25:09.067642	2017-08-19 11:25:09.06769	2017-08-19 11:25:09.067733		\N
24	Larissa	Clauberg	Larissa	Larissa	tobias.krauthoff+dbas.usert17@gmail.com	f	$2a$10$82Prq3AVM9SPmRexBbBiV.1BBxptoTdL2f7WRRbQ5oAbtoghkAigi	3	2017-08-19 11:25:09.067805	2017-08-19 11:25:09.067849	2017-08-19 11:25:09.067892		\N
25	Emmi	Rosch	Emmi	Emmi	tobias.krauthoff+dbas.usert18@gmail.com	f	$2a$10$82Prq3AVM9SPmRexBbBiV.1BBxptoTdL2f7WRRbQ5oAbtoghkAigi	3	2017-08-19 11:25:09.067963	2017-08-19 11:25:09.068007	2017-08-19 11:25:09.06805		\N
26	Konstanze	Krebs	Konstanze	Konstanze	tobias.krauthoff+dbas.usert19@gmail.com	f	$2a$10$82Prq3AVM9SPmRexBbBiV.1BBxptoTdL2f7WRRbQ5oAbtoghkAigi	3	2017-08-19 11:25:09.068125	2017-08-19 11:25:09.068171	2017-08-19 11:25:09.068214		\N
27	Catrin	Fahnrich	Catrin	Catrin	tobias.krauthoff+dbas.usert20@gmail.com	f	$2a$10$82Prq3AVM9SPmRexBbBiV.1BBxptoTdL2f7WRRbQ5oAbtoghkAigi	3	2017-08-19 11:25:09.068286	2017-08-19 11:25:09.068331	2017-08-19 11:25:09.068373		\N
28	Antonia	Bartram	Antonia	Antonia	tobias.krauthoff+dbas.usert21@gmail.com	f	$2a$10$82Prq3AVM9SPmRexBbBiV.1BBxptoTdL2f7WRRbQ5oAbtoghkAigi	3	2017-08-19 11:25:09.068445	2017-08-19 11:25:09.068489	2017-08-19 11:25:09.068531		\N
29	Nora	Kempf	Nora	Nora	tobias.krauthoff+dbas.usert22@gmail.com	f	$2a$10$82Prq3AVM9SPmRexBbBiV.1BBxptoTdL2f7WRRbQ5oAbtoghkAigi	3	2017-08-19 11:25:09.068602	2017-08-19 11:25:09.068647	2017-08-19 11:25:09.068693		\N
30	Julia	Wetter	Julia	Julia	tobias.krauthoff+dbas.usert23@gmail.com	f	$2a$10$82Prq3AVM9SPmRexBbBiV.1BBxptoTdL2f7WRRbQ5oAbtoghkAigi	3	2017-08-19 11:25:09.068768	2017-08-19 11:25:09.068813	2017-08-19 11:25:09.068856		\N
31	Jutta	Munch	Jutta	Jutta	tobias.krauthoff+dbas.usert24@gmail.com	f	$2a$10$82Prq3AVM9SPmRexBbBiV.1BBxptoTdL2f7WRRbQ5oAbtoghkAigi	3	2017-08-19 11:25:09.068927	2017-08-19 11:25:09.068971	2017-08-19 11:25:09.069014		\N
32	Helga	Heilmann	Helga	Helga	tobias.krauthoff+dbas.usert25@gmail.com	f	$2a$10$82Prq3AVM9SPmRexBbBiV.1BBxptoTdL2f7WRRbQ5oAbtoghkAigi	3	2017-08-19 11:25:09.069085	2017-08-19 11:25:09.069132	2017-08-19 11:25:09.069176		\N
33	Denise	Tietjen	Denise	Denise	tobias.krauthoff+dbas.usert26@gmail.com	f	$2a$10$82Prq3AVM9SPmRexBbBiV.1BBxptoTdL2f7WRRbQ5oAbtoghkAigi	3	2017-08-19 11:25:09.06925	2017-08-19 11:25:09.069297	2017-08-19 11:25:09.06934		\N
34	Hanne	Beckmann	Hanne	Hanne	tobias.krauthoff+dbas.usert27@gmail.com	f	$2a$10$82Prq3AVM9SPmRexBbBiV.1BBxptoTdL2f7WRRbQ5oAbtoghkAigi	3	2017-08-19 11:25:09.069412	2017-08-19 11:25:09.069456	2017-08-19 11:25:09.069499		\N
35	Elly	Landauer	Elly	Elly	tobias.krauthoff+dbas.usert28@gmail.com	f	$2a$10$82Prq3AVM9SPmRexBbBiV.1BBxptoTdL2f7WRRbQ5oAbtoghkAigi	3	2017-08-19 11:25:09.069571	2017-08-19 11:25:09.069615	2017-08-19 11:25:09.069658		\N
36	Sybille	Redlich	Sybille	Sybille	tobias.krauthoff+dbas.usert29@gmail.com	f	$2a$10$82Prq3AVM9SPmRexBbBiV.1BBxptoTdL2f7WRRbQ5oAbtoghkAigi	3	2017-08-19 11:25:09.06973	2017-08-19 11:25:09.069774	2017-08-19 11:25:09.06982		\N
37	Ingeburg	Fischer	Ingeburg	Ingeburg	tobias.krauthoff+dbas.usert30@gmail.com	f	$2a$10$82Prq3AVM9SPmRexBbBiV.1BBxptoTdL2f7WRRbQ5oAbtoghkAigi	3	2017-08-19 11:25:09.069893	2017-08-19 11:25:09.069938	2017-08-19 11:25:09.06998		\N
4	Björn	Ebbinghaus	Björn	Björn	bjoern.ebbinghaus@uni-duesseldorf.de	m	$2a$10$FJBWZ4CRBRR2b7LqalRwDOwZwXFg2at74ZimABsTX4fd.1mulb2/m	1	2017-09-28 17:31:40.926313	2017-08-19 11:25:09.064261	2017-08-19 11:25:09.064313		\N
\.


--
-- Name: users_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('users_uid_seq', 37, true);


SET search_path = news, pg_catalog;

--
-- Name: news news_pkey; Type: CONSTRAINT; Schema: news; Owner: dbas
--

ALTER TABLE ONLY news
    ADD CONSTRAINT news_pkey PRIMARY KEY (uid);


SET search_path = public, pg_catalog;

--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: arguments_added_by_premisegroups_split arguments_added_by_premisegroups_split_pkey; Type: CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY arguments_added_by_premisegroups_split
    ADD CONSTRAINT arguments_added_by_premisegroups_split_pkey PRIMARY KEY (uid);


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
-- Name: arguments_added_by_premisegroups_split arguments_added_by_premisegroups_split_argument_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY arguments_added_by_premisegroups_split
    ADD CONSTRAINT arguments_added_by_premisegroups_split_argument_uid_fkey FOREIGN KEY (argument_uid) REFERENCES arguments(uid);


--
-- Name: arguments_added_by_premisegroups_split arguments_added_by_premisegroups_split_review_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbas
--

ALTER TABLE ONLY arguments_added_by_premisegroups_split
    ADD CONSTRAINT arguments_added_by_premisegroups_split_review_uid_fkey FOREIGN KEY (review_uid) REFERENCES review_split(uid);


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
-- Name: news; Type: ACL; Schema: -; Owner: postgres
--

GRANT ALL ON SCHEMA news TO dbas;


SET search_path = news, pg_catalog;

--
-- Name: news; Type: ACL; Schema: news; Owner: dbas
--

GRANT SELECT ON TABLE news TO read_only_discussion;


SET search_path = public, pg_catalog;

--
-- Name: arguments; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE arguments TO read_only_discussion;


--
-- Name: arguments_added_by_premisegroups_split; Type: ACL; Schema: public; Owner: dbas
--

GRANT SELECT ON TABLE arguments_added_by_premisegroups_split TO read_only_discussion;


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

\connect postgres

SET default_transaction_read_only = off;

--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.5
-- Dumped by pg_dump version 9.6.5

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

-- Dumped from database version 9.6.5
-- Dumped by pg_dump version 9.6.5

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

