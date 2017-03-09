--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.5
-- Dumped by pg_dump version 9.5.5

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
1	1	1	\N	t	3	2017-01-26 17:08:49	1	f
2	2	1	\N	f	3	2017-01-26 17:08:49	1	f
3	3	4	\N	t	6	2017-01-26 17:09:18	1	f
4	4	6	\N	t	5	2017-01-26 17:09:18	1	f
5	5	1	\N	f	4	2017-01-26 17:09:18	1	f
6	6	4	\N	t	7	2017-01-26 17:09:18	1	f
7	7	4	\N	f	9	2017-01-26 17:09:18	1	f
8	8	\N	7	f	10	2017-01-27 08:55:37	1	f
9	9	\N	7	f	11	2017-01-27 08:55:37	1	f
10	10	6	\N	f	12	2017-01-27 08:55:37	1	f
11	11	\N	4	f	12	2017-01-27 08:55:37	1	f
12	12	\N	5	f	12	2017-01-27 08:55:37	1	f
13	14	\N	5	f	12	2017-01-27 08:55:37	1	f
14	13	\N	5	f	12	2017-01-27 08:55:37	1	f
15	15	19	\N	t	14	2017-01-27 08:55:37	1	f
16	16	1	\N	f	14	2017-01-27 08:55:37	1	f
17	17	1	\N	f	14	2017-01-27 08:55:37	1	f
18	18	2	\N	f	14	2017-01-27 08:55:37	1	f
19	19	4	\N	f	14	2017-01-27 08:55:37	1	f
20	20	14	\N	f	4	2017-01-27 08:55:37	1	f
21	21	14	\N	f	4	2017-01-27 08:55:37	1	f
22	22	1	\N	f	14	2017-01-27 08:55:37	1	f
23	23	1	\N	t	13	2017-01-27 08:55:37	1	f
24	24	\N	1	f	14	2017-01-27 08:55:37	1	f
25	25	\N	1	f	12	2017-01-27 08:55:37	1	f
26	26	\N	2	f	13	2017-01-27 08:55:37	1	f
27	27	\N	21	f	12	2017-01-27 08:55:37	1	f
28	28	1	\N	f	11	2017-01-27 08:55:37	1	f
29	26	34	\N	t	6	2017-01-27 08:55:37	1	f
30	29	\N	19	f	13	2017-01-27 08:55:37	1	f
31	29	34	\N	t	13	2017-01-27 08:55:37	1	f
32	30	4	\N	t	13	2017-01-27 08:55:37	1	f
33	31	\N	30	f	14	2017-01-27 08:55:37	1	f
34	32	\N	7	f	13	2017-01-27 08:55:37	1	f
35	33	37	\N	f	14	2017-01-27 08:55:37	1	f
36	34	37	\N	t	11	2017-01-27 08:55:37	1	f
37	35	\N	35	f	11	2017-01-27 08:55:37	1	f
38	36	38	\N	f	13	2017-01-27 08:55:37	1	f
39	37	26	\N	f	13	2017-01-27 08:55:37	1	f
40	38	6	\N	f	13	2017-01-27 08:55:37	1	f
41	39	48	\N	t	13	2017-01-27 08:55:37	1	f
42	40	48	\N	t	13	2017-01-27 08:55:37	1	f
43	41	\N	37	f	14	2017-01-27 08:55:37	1	f
44	42	48	\N	t	12	2017-01-27 08:55:37	1	f
45	43	48	\N	f	4	2017-01-27 08:55:37	1	f
46	44	\N	41	f	12	2017-01-27 08:55:37	1	f
47	45	\N	10	f	5	2017-01-27 08:55:37	1	f
48	46	\N	46	f	13	2017-01-27 08:55:37	1	f
49	47	54	\N	f	13	2017-01-27 08:55:37	1	f
50	48	54	\N	f	13	2017-01-27 08:55:37	1	f
51	49	17	\N	f	16	2017-01-29 11:35:54	1	f
52	50	17	\N	f	16	2017-01-29 11:35:54	1	f
53	51	17	\N	f	16	2017-01-29 11:35:54	1	f
54	51	17	\N	f	16	2017-01-29 11:35:54	1	f
55	49	17	\N	f	16	2017-01-29 11:35:54	1	f
56	52	17	\N	f	16	2017-01-29 11:35:54	1	f
57	53	17	\N	f	16	2017-01-29 11:35:54	1	f
58	54	19	\N	t	16	2017-01-29 11:35:54	1	f
59	55	34	\N	f	16	2017-01-29 11:35:54	1	f
60	56	31	\N	f	16	2017-01-29 11:35:54	1	f
61	57	4	\N	t	7	2017-01-29 11:35:54	1	f
62	58	37	\N	t	6	2017-01-30 14:52:10	1	f
63	59	\N	35	f	5	2017-01-30 14:52:10	1	f
64	60	34	\N	t	13	2017-01-30 14:52:10	1	f
65	61	69	\N	f	13	2017-01-30 14:52:10	1	f
66	62	77	\N	t	13	2017-01-30 14:52:10	1	f
67	63	77	\N	t	13	2017-01-30 14:52:10	1	f
68	64	\N	23	f	18	2017-02-01 07:12:22.772434	1	f
69	65	74	\N	f	9	2017-02-02 14:36:12.260823	1	f
70	66	19	\N	t	21	2017-02-03 09:41:33.989518	1	f
71	67	48	\N	f	21	2017-02-03 09:41:33.953233	1	f
72	68	34	\N	f	21	2017-02-03 09:41:33.953233	1	f
73	69	77	\N	f	21	2017-02-03 09:41:33.992991	1	f
74	70	88	\N	f	1	2017-02-15 10:05:04.114164	3	t
75	71	88	\N	t	1	2017-02-15 10:05:04.114164	3	f
76	72	88	\N	f	1	2017-02-15 10:05:04.114164	3	f
77	73	89	\N	t	1	2017-02-15 10:05:04.114164	3	f
78	74	89	\N	f	1	2017-02-15 10:05:04.114164	3	f
81	77	90	\N	t	1	2017-02-15 10:05:04.114164	3	f
83	79	97	\N	f	1	2017-02-15 10:05:04.114164	3	f
84	80	88	\N	t	1	2017-02-15 10:05:04.114164	3	f
85	81	88	\N	t	1	2017-02-15 10:05:04.114164	3	f
88	84	91	\N	t	1	2017-02-15 10:05:04.114164	3	f
89	85	91	\N	f	1	2017-02-15 10:05:04.114164	3	f
90	86	91	\N	t	1	2017-02-15 10:05:04.114164	3	f
92	88	92	\N	t	1	2017-02-15 10:05:04.114164	3	f
93	89	92	\N	f	1	2017-02-15 10:05:04.114164	3	f
94	90	92	\N	f	1	2017-02-15 10:05:04.114164	3	f
96	92	100	\N	f	1	2017-02-15 10:05:04.114164	3	f
97	93	100	\N	t	1	2017-02-15 10:05:04.114164	3	f
99	95	100	\N	t	1	2017-02-15 10:05:04.114164	3	f
100	96	101	\N	t	1	2017-02-15 10:05:04.114164	3	f
101	96	102	\N	t	1	2017-02-15 10:05:04.114164	3	f
102	97	101	\N	t	1	2017-02-15 10:05:04.114164	3	f
103	98	101	\N	f	1	2017-02-15 10:05:04.114164	3	f
105	100	122	\N	t	3	2017-02-15 10:05:04.114164	2	f
107	102	125	\N	t	3	2017-02-15 10:05:04.114164	2	f
108	103	127	\N	t	1	2017-02-15 10:05:04.114164	2	f
109	104	122	\N	f	1	2017-02-15 10:05:04.114164	2	f
112	107	123	\N	t	1	2017-02-15 10:05:04.114164	2	f
113	108	123	\N	t	1	2017-02-15 10:05:04.114164	2	f
114	110	132	\N	f	1	2017-02-15 10:05:04.114164	2	f
115	111	123	\N	f	1	2017-02-15 10:05:04.114164	2	f
117	113	136	\N	f	1	2017-02-15 10:05:04.114164	2	f
119	114	136	\N	t	1	2017-02-15 10:05:04.114164	2	f
120	115	124	\N	t	1	2017-02-15 10:05:04.114164	2	f
122	117	124	\N	f	1	2017-02-15 10:05:04.114164	2	f
123	118	135	\N	f	1	2017-02-15 10:05:04.114164	2	f
124	120	144	\N	f	1	2017-02-15 10:05:04.114164	4	f
127	123	145	\N	t	1	2017-02-15 10:05:04.114164	4	f
128	124	145	\N	f	1	2017-02-15 10:05:04.114164	4	f
129	125	146	\N	t	1	2017-02-15 10:05:04.114164	4	f
130	126	146	\N	f	1	2017-02-15 10:05:04.114164	4	f
131	119	144	\N	t	1	2017-02-15 10:05:04.114164	4	f
132	130	153	\N	t	1	2017-02-15 10:05:04.114164	4	f
79	75	\N	77	f	1	2017-02-15 10:05:04.114164	3	f
80	76	\N	78	f	1	2017-02-15 10:05:04.114164	3	f
82	78	\N	81	f	1	2017-02-15 10:05:04.114164	3	f
86	82	\N	85	f	1	2017-02-15 10:05:04.114164	3	f
87	83	\N	86	f	1	2017-02-15 10:05:04.114164	3	f
91	87	\N	75	f	1	2017-02-15 10:05:04.114164	3	f
95	91	\N	76	f	1	2017-02-15 10:05:04.114164	3	f
98	94	\N	84	f	1	2017-02-15 10:05:04.114164	3	f
104	99	\N	88	f	1	2017-02-15 10:05:04.114164	3	f
106	101	\N	105	f	3	2017-02-15 10:05:04.114164	2	f
110	105	\N	109	f	1	2017-02-15 10:05:04.114164	2	f
111	106	\N	109	f	1	2017-02-15 10:05:04.114164	2	f
116	112	\N	115	f	1	2017-02-15 10:05:04.114164	2	f
118	109	\N	112	f	1	2017-02-15 10:05:04.114164	2	f
121	116	\N	120	f	1	2017-02-15 10:05:04.114164	2	f
125	121	\N	131	f	1	2017-02-15 10:05:04.114164	4	f
126	122	\N	124	f	1	2017-02-15 10:05:04.114164	4	f
\.


--
-- Name: arguments_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('arguments_uid_seq', 132, true);


--
-- Data for Name: clicked_arguments; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY clicked_arguments (uid, argument_uid, author_uid, "timestamp", is_up_vote, is_valid) FROM stdin;
1	3	6	2017-01-26 17:14:12	t	t
7	4	3	2017-01-26 18:05:30	t	t
8	3	9	2017-01-26 20:06:52	t	t
9	7	9	2017-01-26 20:08:09	t	t
6	6	7	2017-01-26 17:37:07	t	f
11	7	7	2017-01-27 08:57:07	t	f
10	7	3	2017-01-26 20:40:56	t	f
12	6	3	2017-01-27 08:59:30	t	f
14	7	3	2017-01-27 09:01:02	t	f
13	6	7	2017-01-27 09:00:13	t	f
16	8	10	2017-01-27 09:16:26	t	t
18	9	11	2017-01-27 09:19:39	t	t
20	3	11	2017-01-27 09:20:44	t	f
21	6	11	2017-01-27 09:21:24	t	f
19	7	11	2017-01-27 09:19:39	f	f
23	6	11	2017-01-27 09:23:53	t	t
22	7	11	2017-01-27 09:23:24	t	f
25	8	4	2017-01-27 09:39:08	t	t
24	7	4	2017-01-27 09:29:40	t	f
26	7	4	2017-01-27 09:39:08	f	t
27	6	3	2017-01-27 09:40:06	t	f
28	6	3	2017-01-27 09:49:04	t	f
29	7	3	2017-01-27 09:49:13	t	f
30	7	3	2017-01-27 09:50:14	t	f
31	6	3	2017-01-27 09:51:09	t	f
34	11	12	2017-01-27 10:09:27	t	t
33	10	12	2017-01-27 10:04:22	t	f
38	4	4	2017-01-27 10:12:25	t	t
36	10	4	2017-01-27 10:10:52	t	f
39	12	12	2017-01-27 10:29:22	t	t
41	13	12	2017-01-27 10:29:23	t	t
40	5	12	2017-01-27 10:29:22	f	f
42	15	14	2017-01-27 10:31:41	t	t
43	15	12	2017-01-27 10:34:04	t	t
44	3	12	2017-01-27 10:34:31	t	t
46	8	12	2017-01-27 10:35:05	t	t
47	7	12	2017-01-27 10:35:05	f	t
48	18	14	2017-01-27 10:35:51	t	t
49	19	14	2017-01-27 10:39:41	t	t
52	24	14	2017-01-27 10:45:05	t	t
53	1	14	2017-01-27 10:45:05	f	t
45	16	14	2017-01-27 10:34:34	t	f
50	22	14	2017-01-27 10:43:50	t	f
54	25	12	2017-01-27 10:45:54	t	t
37	1	12	2017-01-27 10:11:32	t	f
55	1	12	2017-01-27 10:45:54	f	t
35	4	12	2017-01-27 10:09:27	f	f
57	26	13	2017-01-27 10:47:52	t	t
58	2	13	2017-01-27 10:47:52	f	t
51	23	13	2017-01-27 10:44:59	t	f
59	1	13	2017-01-27 10:50:45	t	t
61	27	12	2017-01-27 10:53:50	t	t
62	21	12	2017-01-27 10:53:50	f	t
64	28	10	2017-01-27 10:56:03	t	t
65	29	6	2017-01-27 10:56:10	t	t
66	30	13	2017-01-27 10:56:21	t	t
68	18	10	2017-01-27 10:56:43	t	t
60	3	13	2017-01-27 10:51:55	t	f
63	28	11	2017-01-27 10:54:00	t	f
72	32	13	2017-01-27 11:04:23	t	t
70	6	13	2017-01-27 11:00:04	t	f
71	1	11	2017-01-27 11:02:22	t	f
73	33	14	2017-01-27 11:08:21	t	t
17	7	10	2017-01-27 09:16:26	f	f
76	19	10	2017-01-27 11:10:02	t	f
75	32	10	2017-01-27 11:09:49	t	f
79	29	12	2017-01-27 11:11:18	t	t
80	34	13	2017-01-27 11:11:30	t	t
67	19	13	2017-01-27 10:56:21	f	f
82	32	10	2017-01-27 11:11:56	t	t
77	3	10	2017-01-27 11:10:48	t	f
78	19	10	2017-01-27 11:10:57	t	f
81	7	13	2017-01-27 11:11:30	f	f
84	35	14	2017-01-27 11:14:48	t	t
85	36	11	2017-01-27 11:16:06	t	t
83	19	13	2017-01-27 11:12:19	f	f
86	37	11	2017-01-27 11:20:45	t	t
87	35	11	2017-01-27 11:20:45	f	t
88	38	13	2017-01-27 11:25:32	t	t
90	39	13	2017-01-27 11:31:18	t	t
92	11	13	2017-01-27 11:33:55	t	t
93	4	13	2017-01-27 11:33:55	f	t
89	10	13	2017-01-27 11:29:00	t	f
91	40	13	2017-01-27 11:32:52	t	f
94	19	13	2017-01-27 11:34:21	f	t
95	15	13	2017-01-27 11:43:04	t	t
96	43	14	2017-01-27 11:59:41	t	t
74	30	14	2017-01-27 11:08:21	f	f
97	37	14	2017-01-27 11:59:41	f	t
98	21	4	2017-01-27 12:14:09	t	t
100	45	4	2017-01-27 12:29:59	t	t
101	46	12	2017-01-27 12:38:27	t	t
102	41	12	2017-01-27 12:38:27	f	t
99	44	12	2017-01-27 12:23:38	t	f
103	45	5	2017-01-27 12:44:32	t	t
2	4	5	2017-01-26 17:16:27	t	f
104	47	5	2017-01-27 12:49:53	t	t
105	10	5	2017-01-27 12:49:53	f	f
106	47	12	2017-01-27 12:51:53	t	t
56	10	12	2017-01-27 10:46:09	t	f
107	10	12	2017-01-27 12:51:53	f	t
109	48	13	2017-01-27 12:57:04	t	t
110	46	13	2017-01-27 12:57:04	f	t
111	30	5	2017-01-27 12:57:55	t	t
108	19	5	2017-01-27 12:56:25	t	f
112	19	5	2017-01-27 12:57:55	f	t
114	49	13	2017-01-27 13:01:18	t	t
115	50	13	2017-01-27 13:01:45	t	t
116	5	16	2017-01-30 01:16:43	t	t
118	49	16	2017-01-30 01:31:01	t	t
117	41	16	2017-01-30 01:26:54	t	f
119	58	16	2017-01-30 01:32:14	t	t
120	59	16	2017-01-30 01:37:58	t	t
121	60	16	2017-01-30 01:39:33	t	t
122	6	16	2017-01-30 01:39:58	t	t
124	30	16	2017-01-30 01:41:29	t	t
123	19	16	2017-01-30 01:40:36	t	f
125	19	16	2017-01-30 01:41:29	f	t
127	36	7	2017-01-30 08:54:48	t	t
128	35	7	2017-01-30 08:55:30	t	t
129	43	7	2017-01-30 08:56:57	t	t
130	37	7	2017-01-30 08:56:57	f	t
131	61	7	2017-01-30 09:08:59	t	t
15	7	7	2017-01-27 09:15:51	t	f
133	58	4	2017-01-30 13:02:48	t	t
69	31	13	2017-01-27 10:57:39	t	f
113	42	13	2017-01-27 12:59:39	t	f
4	2	5	2017-01-26 17:19:26	t	f
32	6	3	2017-01-27 09:58:53	t	f
126	7	3	2017-01-30 08:36:23	t	f
132	15	4	2017-01-30 13:02:45	t	f
134	62	6	2017-01-30 14:58:07	t	t
135	35	6	2017-01-30 14:58:34	t	t
137	63	5	2017-01-30 15:25:37	t	t
138	35	5	2017-01-30 15:25:37	f	t
139	1	4	2017-01-30 15:26:04	t	t
3	5	4	2017-01-26 17:17:01	t	f
136	62	5	2017-01-30 15:21:27	t	f
140	2	3	2017-01-30 19:59:42	t	t
141	64	13	2017-01-31 11:20:22	t	t
142	65	13	2017-01-31 11:24:06	t	t
143	41	13	2017-01-31 11:25:30	t	t
5	5	5	2017-01-26 17:20:45	t	f
144	1	5	2017-01-31 13:01:12	t	f
145	66	13	2017-02-01 10:05:40.76086	t	t
147	68	18	2017-02-01 14:19:46.453817	t	t
146	5	18	2017-02-01 14:12:35.8623	t	f
149	1	18	2017-02-01 14:21:28.372848	t	f
150	1	18	2017-02-01 14:21:36.525657	t	f
151	1	18	2017-02-01 14:21:41.709373	t	f
152	1	18	2017-02-01 14:21:45.153514	t	t
153	5	18	2017-02-01 14:26:33.104649	t	t
148	23	18	2017-02-01 14:19:46.491565	f	f
155	36	19	2017-02-02 09:16:28.29602	t	t
154	62	19	2017-02-02 09:16:04.707567	t	f
156	58	19	2017-02-02 09:18:51.871664	t	t
157	58	8	2017-02-02 10:50:29.497487	t	t
158	4	8	2017-02-02 10:52:01.805293	t	t
159	3	3	2017-02-02 14:36:42.285553	t	t
161	23	9	2017-02-02 15:33:46.039774	t	t
160	1	9	2017-02-02 15:32:23.2935	t	f
162	35	9	2017-02-02 15:34:43.758617	t	t
163	69	9	2017-02-02 15:37:43.434601	t	t
164	45	20	2017-02-02 22:10:27.568842	t	t
165	70	21	2017-02-03 12:51:38.532487	t	t
166	71	21	2017-02-03 12:54:40.981043	t	t
167	59	21	2017-02-03 12:58:11.00005	t	t
168	72	21	2017-02-03 12:59:56.764917	t	t
169	73	21	2017-02-03 13:10:35.137026	t	t
\.


--
-- Name: clicked_arguments_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('clicked_arguments_uid_seq', 169, true);


--
-- Data for Name: clicked_statements; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY clicked_statements (uid, statement_uid, author_uid, "timestamp", is_up_vote, is_valid) FROM stdin;
3	5	6	2017-01-26 17:14:12	t	t
4	6	5	2017-01-26 17:14:24	t	t
5	7	5	2017-01-26 17:16:27	t	t
6	8	4	2017-01-26 17:17:01	t	t
11	3	5	2017-01-26 17:19:26	t	t
12	8	5	2017-01-26 17:20:45	t	t
14	9	7	2017-01-26 17:37:07	t	t
15	10	7	2017-01-26 17:37:07	t	t
16	6	3	2017-01-26 18:05:15	f	f
17	6	3	2017-01-26 18:05:26	t	t
18	7	3	2017-01-26 18:05:30	t	t
20	5	9	2017-01-26 20:06:52	t	t
19	4	9	2017-01-26 20:06:30	t	f
21	4	9	2017-01-26 20:07:31	f	t
22	11	9	2017-01-26 20:08:09	t	t
24	11	3	2017-01-26 20:40:56	t	t
25	11	7	2017-01-27 08:57:07	t	t
13	4	7	2017-01-26 17:35:51	t	f
26	4	7	2017-01-27 08:57:07	f	f
28	9	3	2017-01-27 08:59:30	t	t
29	10	3	2017-01-27 08:59:30	t	t
23	4	3	2017-01-26 20:39:04	f	f
30	4	3	2017-01-27 08:59:30	t	f
31	4	3	2017-01-27 09:01:02	f	f
27	4	7	2017-01-27 08:57:23	t	f
34	12	10	2017-01-27 09:16:26	t	t
35	11	10	2017-01-27 09:16:26	t	t
37	13	11	2017-01-27 09:19:39	t	t
38	11	11	2017-01-27 09:19:39	t	t
40	5	11	2017-01-27 09:20:44	t	t
41	9	11	2017-01-27 09:21:24	t	t
42	10	11	2017-01-27 09:21:24	t	t
39	4	11	2017-01-27 09:19:39	t	f
43	4	11	2017-01-27 09:23:24	f	f
44	4	11	2017-01-27 09:23:54	t	t
45	11	4	2017-01-27 09:29:40	t	t
9	4	4	2017-01-26 17:19:13	f	f
46	4	4	2017-01-27 09:38:41	t	f
48	12	4	2017-01-27 09:39:08	t	t
47	4	4	2017-01-27 09:38:45	f	f
49	4	4	2017-01-27 09:39:08	t	t
32	4	3	2017-01-27 09:01:34	t	f
50	4	3	2017-01-27 09:49:13	f	f
51	4	3	2017-01-27 09:49:26	t	f
52	4	3	2017-01-27 09:50:06	f	f
55	14	12	2017-01-27 10:04:22	t	t
7	6	4	2017-01-26 17:17:20	t	f
57	15	12	2017-01-27 10:09:27	t	t
58	7	12	2017-01-27 10:09:27	t	t
54	6	12	2017-01-27 10:00:28	f	f
56	6	4	2017-01-27 10:07:06	f	f
60	6	4	2017-01-27 10:10:39	t	f
63	1	12	2017-01-27 10:11:15	t	t
61	6	4	2017-01-27 10:10:44	f	f
64	6	4	2017-01-27 10:11:23	t	t
65	2	12	2017-01-27 10:11:32	t	t
66	7	4	2017-01-27 10:12:25	t	t
67	17	12	2017-01-27 10:29:22	t	t
68	8	12	2017-01-27 10:29:22	t	t
69	18	12	2017-01-27 10:29:23	t	t
70	19	14	2017-01-27 10:30:59	t	t
71	20	14	2017-01-27 10:31:41	t	t
73	19	12	2017-01-27 10:33:57	t	t
74	20	12	2017-01-27 10:34:04	t	t
75	4	12	2017-01-27 10:34:22	t	t
76	5	12	2017-01-27 10:34:31	t	t
77	21	14	2017-01-27 10:34:34	t	t
78	12	12	2017-01-27 10:35:05	t	t
79	11	12	2017-01-27 10:35:05	t	t
80	23	14	2017-01-27 10:35:51	t	t
82	1	13	2017-01-27 10:36:08	t	t
83	4	14	2017-01-27 10:38:10	f	t
84	24	14	2017-01-27 10:39:41	t	t
2	4	6	2017-01-26 17:12:56	t	f
85	4	6	2017-01-27 10:40:58	f	t
86	27	14	2017-01-27 10:43:50	t	t
87	28	13	2017-01-27 10:44:59	t	t
88	29	14	2017-01-27 10:45:05	t	t
81	2	14	2017-01-27 10:35:51	f	f
89	2	14	2017-01-27 10:45:05	t	t
72	1	14	2017-01-27 10:32:31	f	f
90	1	14	2017-01-27 10:45:05	t	t
91	30	12	2017-01-27 10:45:54	t	t
59	6	12	2017-01-27 10:09:27	t	f
93	31	13	2017-01-27 10:47:52	t	t
94	3	13	2017-01-27 10:47:52	t	t
95	2	13	2017-01-27 10:50:45	t	t
97	4	13	2017-01-27 10:51:34	t	t
98	5	13	2017-01-27 10:51:55	t	t
99	1	6	2017-01-27 10:53:25	t	t
100	32	12	2017-01-27 10:53:50	t	t
101	26	12	2017-01-27 10:53:50	t	t
102	33	11	2017-01-27 10:54:00	t	t
103	1	10	2017-01-27 10:55:25	f	t
104	34	6	2017-01-27 10:55:44	t	t
105	33	10	2017-01-27 10:56:03	t	t
106	31	6	2017-01-27 10:56:10	t	t
107	35	13	2017-01-27 10:56:21	t	t
108	24	13	2017-01-27 10:56:21	t	t
109	23	10	2017-01-27 10:56:43	t	t
110	2	10	2017-01-27 10:56:43	f	t
111	34	13	2017-01-27 10:56:45	t	t
112	9	13	2017-01-27 11:00:04	t	t
113	10	13	2017-01-27 11:00:04	t	t
96	1	11	2017-01-27 10:51:23	f	f
115	2	11	2017-01-27 11:02:22	t	t
116	34	12	2017-01-27 11:02:58	t	t
114	1	11	2017-01-27 11:01:56	t	f
118	36	13	2017-01-27 11:04:23	t	t
117	1	11	2017-01-27 11:04:23	f	f
119	1	11	2017-01-27 11:04:28	t	t
120	38	14	2017-01-27 11:08:21	t	t
121	35	14	2017-01-27 11:08:21	f	t
122	36	10	2017-01-27 11:09:49	t	t
123	24	10	2017-01-27 11:10:02	t	t
36	4	10	2017-01-27 09:16:26	t	f
125	5	10	2017-01-27 11:10:48	t	t
124	4	10	2017-01-27 11:10:02	f	f
126	4	10	2017-01-27 11:10:48	t	f
128	31	12	2017-01-27 11:11:18	t	t
129	39	13	2017-01-27 11:11:30	t	t
130	11	13	2017-01-27 11:11:30	t	t
127	4	10	2017-01-27 11:10:57	f	f
131	4	10	2017-01-27 11:11:56	t	t
132	37	14	2017-01-27 11:12:09	t	f
62	14	4	2017-01-27 10:10:52	t	f
92	6	12	2017-01-27 10:46:09	f	f
8	4	5	2017-01-26 17:17:58	f	f
53	4	3	2017-01-27 09:51:09	t	f
33	4	7	2017-01-27 09:15:30	f	f
1	1	4	2017-01-26 17:10:14	f	f
10	1	5	2017-01-26 17:19:16	f	f
133	37	14	2017-01-27 11:12:35	f	t
134	37	11	2017-01-27 11:13:18	t	f
135	37	11	2017-01-27 11:13:34	f	f
137	40	14	2017-01-27 11:14:48	t	t
138	41	14	2017-01-27 11:14:48	t	t
136	37	11	2017-01-27 11:13:43	t	f
140	42	11	2017-01-27 11:16:06	t	t
139	37	11	2017-01-27 11:14:59	f	f
141	37	11	2017-01-27 11:16:06	t	t
142	43	11	2017-01-27 11:20:45	t	t
143	40	11	2017-01-27 11:20:45	t	t
144	41	11	2017-01-27 11:20:45	t	t
145	38	13	2017-01-27 11:23:15	f	t
146	44	13	2017-01-27 11:25:32	t	t
147	45	13	2017-01-27 11:25:32	t	t
149	14	13	2017-01-27 11:29:00	t	t
150	46	13	2017-01-27 11:31:18	t	t
151	26	13	2017-01-27 11:31:18	f	t
152	47	13	2017-01-27 11:32:52	t	t
153	15	13	2017-01-27 11:33:55	t	t
154	7	13	2017-01-27 11:33:55	t	t
148	6	13	2017-01-27 11:28:50	f	f
155	6	13	2017-01-27 11:33:55	t	t
156	20	13	2017-01-27 11:43:04	t	t
157	19	13	2017-01-27 11:43:04	t	t
158	48	13	2017-01-27 11:45:25	t	t
159	51	14	2017-01-27 11:59:41	t	t
160	52	14	2017-01-27 11:59:41	t	t
161	43	14	2017-01-27 11:59:41	f	t
162	26	4	2017-01-27 12:14:09	t	t
163	14	4	2017-01-27 12:14:09	f	t
165	48	12	2017-01-27 12:22:22	t	t
166	53	12	2017-01-27 12:23:38	t	t
167	48	4	2017-01-27 12:28:48	f	t
169	55	12	2017-01-27 12:38:27	t	t
170	49	12	2017-01-27 12:38:27	t	t
171	48	5	2017-01-27 12:44:22	f	t
172	54	5	2017-01-27 12:44:32	t	t
173	56	5	2017-01-27 12:49:53	t	t
174	14	5	2017-01-27 12:49:53	t	t
175	56	12	2017-01-27 12:51:53	t	t
176	6	12	2017-01-27 12:51:53	t	t
177	24	5	2017-01-27 12:56:25	t	t
178	57	13	2017-01-27 12:57:04	t	t
179	55	13	2017-01-27 12:57:04	f	t
180	35	5	2017-01-27 12:57:55	t	t
181	4	5	2017-01-27 12:57:55	t	t
182	50	13	2017-01-27 12:59:39	t	t
183	58	13	2017-01-27 13:01:18	t	t
184	59	13	2017-01-27 13:01:18	t	t
185	60	13	2017-01-27 13:01:18	t	t
186	54	13	2017-01-27 13:01:18	f	t
187	61	13	2017-01-27 13:01:45	t	t
188	27	5	2017-01-29 15:37:22	f	t
189	19	4	2017-01-29 20:00:59	t	t
190	1	16	2017-01-30 01:12:27	f	t
191	8	16	2017-01-30 01:16:43	t	t
192	49	16	2017-01-30 01:26:54	t	t
193	48	16	2017-01-30 01:26:54	t	t
194	58	16	2017-01-30 01:31:01	t	t
195	59	16	2017-01-30 01:31:01	t	t
196	60	16	2017-01-30 01:31:01	t	t
197	54	16	2017-01-30 01:31:01	f	t
198	19	16	2017-01-30 01:31:39	t	t
199	68	16	2017-01-30 01:32:14	t	t
200	34	16	2017-01-30 01:36:16	f	t
201	69	16	2017-01-30 01:37:58	t	t
202	70	16	2017-01-30 01:39:33	t	t
203	31	16	2017-01-30 01:39:33	f	t
205	9	16	2017-01-30 01:39:58	t	t
206	10	16	2017-01-30 01:39:58	t	t
207	24	16	2017-01-30 01:40:36	t	t
204	4	16	2017-01-30 01:39:46	t	f
209	35	16	2017-01-30 01:41:29	t	t
208	4	16	2017-01-30 01:40:36	f	f
210	4	16	2017-01-30 01:41:29	t	t
213	42	7	2017-01-30 08:54:48	t	t
214	40	7	2017-01-30 08:55:30	t	t
215	41	7	2017-01-30 08:55:30	t	t
212	37	7	2017-01-30 08:54:12	t	f
216	37	7	2017-01-30 08:55:30	f	t
217	51	7	2017-01-30 08:56:57	t	t
218	52	7	2017-01-30 08:56:57	t	t
219	43	7	2017-01-30 08:56:57	f	t
168	54	4	2017-01-27 12:29:59	t	f
221	4	7	2017-01-30 09:07:04	t	t
222	71	7	2017-01-30 09:08:59	t	t
223	72	7	2017-01-30 09:08:59	t	t
224	20	4	2017-01-30 13:02:45	t	t
225	68	4	2017-01-30 13:02:48	t	t
226	37	4	2017-01-30 13:07:56	t	t
227	73	6	2017-01-30 14:58:07	t	t
228	40	6	2017-01-30 14:58:34	t	t
229	41	6	2017-01-30 14:58:34	t	t
164	37	6	2017-01-27 12:21:40	t	f
230	37	6	2017-01-30 14:58:34	f	t
231	37	5	2017-01-30 15:03:38	t	t
232	73	5	2017-01-30 15:21:27	t	t
233	74	5	2017-01-30 15:25:37	t	t
234	40	5	2017-01-30 15:25:37	t	t
235	41	5	2017-01-30 15:25:37	t	t
236	1	4	2017-01-30 15:26:02	t	t
237	2	4	2017-01-30 15:26:04	t	t
238	37	3	2017-01-30 19:54:15	t	t
240	3	3	2017-01-30 19:59:42	t	t
241	75	13	2017-01-31 11:20:22	t	t
242	76	13	2017-01-31 11:24:06	t	t
243	69	13	2017-01-31 11:24:06	f	t
244	49	13	2017-01-31 11:25:30	t	t
245	77	13	2017-01-31 11:29:42	t	t
246	1	5	2017-01-31 12:40:53	t	f
247	1	5	2017-01-31 12:58:57	f	f
248	1	5	2017-01-31 12:59:17	t	t
249	2	5	2017-01-31 13:01:12	t	t
239	1	3	2017-01-30 19:59:36	f	f
251	78	13	2017-02-01 10:05:40.772063	t	t
253	8	18	2017-02-01 14:12:35.880323	t	t
254	80	18	2017-02-01 14:19:46.48767	t	t
255	28	18	2017-02-01 14:19:46.510686	t	t
252	1	18	2017-02-01 14:12:11.828268	f	f
256	1	18	2017-02-01 14:19:46.51553	t	f
257	1	18	2017-02-01 14:21:19.568639	f	f
259	2	18	2017-02-01 14:21:28.391988	t	t
258	1	18	2017-02-01 14:21:22.203076	t	f
260	1	18	2017-02-01 14:26:09.495638	f	t
261	37	19	2017-02-02 09:15:49.814643	t	t
262	73	19	2017-02-02 09:16:04.719742	t	t
263	42	19	2017-02-02 09:16:28.308335	t	t
264	19	19	2017-02-02 09:17:45.263915	t	t
265	34	19	2017-02-02 09:18:35.856776	t	t
266	68	19	2017-02-02 09:18:51.882011	t	t
267	19	8	2017-02-02 10:50:15.663052	t	t
250	1	3	2017-02-01 07:23:10.294659	t	f
268	68	8	2017-02-02 10:50:29.510328	t	t
269	6	8	2017-02-02 10:51:46.370576	t	t
270	7	8	2017-02-02 10:52:01.817642	t	t
211	4	3	2017-01-30 08:36:23	f	f
271	4	3	2017-02-02 14:36:36.437445	t	t
272	5	3	2017-02-02 14:36:42.30624	t	t
273	1	9	2017-02-02 15:32:16.16825	t	t
274	2	9	2017-02-02 15:32:23.313281	t	t
275	28	9	2017-02-02 15:33:46.058714	t	t
276	37	9	2017-02-02 15:34:26.224136	f	t
277	40	9	2017-02-02 15:34:43.770219	t	t
278	41	9	2017-02-02 15:34:43.77491	t	t
279	81	9	2017-02-02 15:37:43.444443	t	t
280	74	9	2017-02-02 15:37:43.44831	f	t
281	1	3	2017-02-02 19:59:29.747683	f	t
282	48	20	2017-02-02 22:10:24.031719	f	t
283	54	20	2017-02-02 22:10:27.581773	t	t
284	19	21	2017-02-03 12:50:54.801012	t	t
285	82	21	2017-02-03 12:51:38.545056	t	t
286	48	21	2017-02-03 12:54:12.366866	f	t
287	83	21	2017-02-03 12:54:40.996111	t	t
288	34	21	2017-02-03 12:58:07.290819	f	t
289	69	21	2017-02-03 12:58:11.012638	t	t
290	84	21	2017-02-03 12:59:56.779895	t	t
291	77	21	2017-02-03 13:04:59.213001	f	t
292	85	21	2017-02-03 13:10:35.14914	t	t
293	86	21	2017-02-03 13:10:35.154148	t	t
294	19	3	2017-02-06 08:30:10.321307	t	t
295	77	3	2017-02-06 08:30:49.262675	f	t
220	54	4	2017-01-30 09:01:23	f	f
296	54	4	2017-02-06 12:15:27.348455	t	t
\.


--
-- Name: clicked_statements_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('clicked_statements_uid_seq', 296, true);


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
1	4	/	2017-01-26 17:09:28
2	5	/	2017-01-26 17:09:56
3	5	/	2017-01-26 17:09:57
4	5	/discuss	2017-01-26 17:10:02
5	4	/discuss	2017-01-26 17:10:09
6	4	/attitude/1	2017-01-26 17:10:11
8	4	/justify/1/f	2017-01-26 17:10:14
9	4	/publications	2017-01-26 17:10:47
10	6	/discuss	2017-01-26 17:12:27
11	6	/discuss	2017-01-26 17:12:27
12	4	/discuss	2017-01-26 17:12:28
13	6	/attitude/4	2017-01-26 17:12:54
15	6	/justify/4/t	2017-01-26 17:12:56
16	6	/reaction/3/end/0	2017-01-26 17:14:12
17	5	/attitude/6	2017-01-26 17:14:20
19	5	/justify/6/t	2017-01-26 17:14:24
23	4	/justify/1/f	2017-01-26 17:14:58
24	4	/settings	2017-01-26 17:15:03
25	4	/settings	2017-01-26 17:15:18
26	4	/settings	2017-01-26 17:15:40
27	4	/discuss	2017-01-26 17:16:01
28	4	/attitude/1	2017-01-26 17:16:06
30	4	/justify/1/f	2017-01-26 17:16:07
31	5	/reaction/4/end/0	2017-01-26 17:16:27
32	4	/reaction/5/rebut/1	2017-01-26 17:17:01
33	4	/discuss	2017-01-26 17:17:07
34	4	/attitude/6	2017-01-26 17:17:16
36	4	/justify/6/t	2017-01-26 17:17:20
37	5	/discuss	2017-01-26 17:17:46
38	5	/attitude/4	2017-01-26 17:17:56
40	5	/justify/4/f	2017-01-26 17:17:58
41	4	/	2017-01-26 17:18:54
42	4	/	2017-01-26 17:18:54
43	5	/discuss	2017-01-26 17:18:59
44	4	/review	2017-01-26 17:19:01
45	4	/discuss	2017-01-26 17:19:05
46	4	/attitude/4	2017-01-26 17:19:09
48	4	/justify/4/f	2017-01-26 17:19:13
49	5	/attitude/1	2017-01-26 17:19:13
51	5	/justify/1/f	2017-01-26 17:19:16
52	5	/reaction/2/rebut/1	2017-01-26 17:19:26
54	5	/justify/1/f	2017-01-26 17:19:46
55	5	/reaction/5/rebut/1	2017-01-26 17:20:45
56	5	/review	2017-01-26 17:23:16
57	5	/review	2017-01-26 17:26:01
58	5	/discuss	2017-01-26 17:31:10
59	5	/discuss	2017-01-26 17:31:16
60	7	/notifications	2017-01-26 17:31:50
61	7	/notifications	2017-01-26 17:31:50
62	7	/review	2017-01-26 17:32:21
63	7	/settings	2017-01-26 17:32:31
64	5	/notifications	2017-01-26 17:32:40
65	5	/discuss	2017-01-26 17:33:01
66	5	/	2017-01-26 17:33:05
67	7	/user/rabia100	2017-01-26 17:34:17
68	7	/news	2017-01-26 17:34:26
69	7	/discuss	2017-01-26 17:35:19
70	7	/attitude/4	2017-01-26 17:35:47
72	7	/justify/4/t	2017-01-26 17:35:51
73	7	/reaction/6/end/0	2017-01-26 17:37:07
74	7	/	2017-01-26 17:37:14
75	7	/contact	2017-01-26 17:37:38
76	7	/contact	2017-01-26 17:37:44
77	4	/discuss	2017-01-26 17:39:42
78	4	/discuss	2017-01-26 17:39:42
79	4	/attitude/6	2017-01-26 17:39:59
80	4	/discuss	2017-01-26 17:40:23
81	3	/	2017-01-26 17:54:18
82	3	/	2017-01-26 17:54:43
83	3	/admin/	2017-01-26 17:54:55
84	3	/review	2017-01-26 17:55:38
85	8	/discuss	2017-01-26 18:00:16
86	8	/discuss	2017-01-26 18:00:16
87	8		2017-01-26 18:00:28
88	8	/attitude/6	2017-01-26 18:00:30
89	3	/	2017-01-26 18:00:32
91	8	/justify/6/d	2017-01-26 18:00:33
92	3	/discuss	2017-01-26 18:01:08
93	3	/jump/6	2017-01-26 18:03:11
94	3	/admin/	2017-01-26 18:03:19
95	3	/admin/TextVersion	2017-01-26 18:03:22
96	3	/discuss	2017-01-26 18:04:49
97	3	/admin/	2017-01-26 18:04:55
98	3	/admin/User	2017-01-26 18:04:59
99	3	/discuss	2017-01-26 18:05:01
100	3	/attitude/6	2017-01-26 18:05:10
102	3	/justify/6/f	2017-01-26 18:05:15
103	3	/attitude/6	2017-01-26 18:05:24
105	3	/justify/6/t	2017-01-26 18:05:26
106	3	/reaction/4/end/0	2017-01-26 18:05:30
107	3	/jump/4	2017-01-26 18:06:43
108	8	/	2017-01-26 18:08:11
109	8	/discuss	2017-01-26 18:08:12
110	8	/attitude/6	2017-01-26 18:08:16
112	8	/justify/6/d	2017-01-26 18:08:21
114	3	/justify/6/d	2017-01-26 18:38:04
116	8	/justify/6/d	2017-01-26 18:43:01
117	4		2017-01-26 19:44:10
118	9	/	2017-01-26 20:02:54
119	9	/	2017-01-26 20:02:55
120	9	/discuss	2017-01-26 20:03:24
121	9	/settings	2017-01-26 20:03:48
122	9	/discuss	2017-01-26 20:06:20
123	9	/attitude/4	2017-01-26 20:06:26
125	9	/justify/4/t	2017-01-26 20:06:30
126	9	/reaction/3/end/0	2017-01-26 20:06:52
128	9	/justify/4/f	2017-01-26 20:07:31
129	9	/reaction/7/rebut/6	2017-01-26 20:08:09
131	9	/justify/4/f	2017-01-26 20:08:25
132	9	/reaction/7/rebut/3	2017-01-26 20:08:29
134	9	/justify/4/f	2017-01-26 20:09:06
138	6	/justify/7/t/undercut	2017-01-26 20:10:14
140	3	/justify/4/f	2017-01-26 20:39:04
142	3	/attitude/4	2017-01-26 20:40:50
146	3	/admin/	2017-01-26 20:41:13
148	5	/	2017-01-26 22:11:11
152	5	/justify/1/f	2017-01-26 22:11:54
153	5	/justify/1/f	2017-01-26 22:11:54
160	3	/justify/4/f	2017-01-27 08:02:59
163	3	/review	2017-01-27 08:50:55
141	3	/discuss	2017-01-26 20:40:45
151	5	/attitude/1	2017-01-26 22:11:43
158	3	/admin/Argument	2017-01-27 07:04:21
161	3	/admin/	2017-01-27 08:18:11
143	3	/justify/4/f	2017-01-26 20:40:51
149	5	/	2017-01-26 22:11:11
150	5	/discuss	2017-01-26 22:11:16
155	5	/justify/1/f	2017-01-26 22:13:19
156	5	/justify/1/f	2017-01-26 22:13:19
157	5	/reaction/5/rebut/1	2017-01-26 22:13:29
162	3	/admin/User	2017-01-27 08:18:13
145	3	/reaction/7/rebut/6	2017-01-26 20:40:56
164	3	/review	2017-01-27 08:55:46
165	3	/admin/Argument	2017-01-27 08:55:52
167	3	/justify/4/f	2017-01-27 08:56:01
168	3	/reaction/7/rebut/6	2017-01-27 08:56:53
169	7	/reaction/7/rebut/6	2017-01-27 08:57:07
170	7	/reaction/6/rebut/7	2017-01-27 08:57:23
171	3	/reaction/6/rebut/7	2017-01-27 08:59:30
173	7	/justify/7/t/undercut	2017-01-27 08:59:40
174	7	verbesserung-des-informatik-studiengangs	2017-01-27 08:59:55
175	7	/attitude/4	2017-01-27 09:00:04
177	7	/justify/4/t	2017-01-27 09:00:07
178	7	/reaction/6/rebut/7	2017-01-27 09:00:13
180	3	/justify/4/t	2017-01-27 09:00:25
181	3	/reaction/7/rebut/6	2017-01-27 09:01:02
183	3	/justify/4/f	2017-01-27 09:01:21
184	3	/reaction/7/rebut/6	2017-01-27 09:01:25
186	3	/justify/6/f/undermine	2017-01-27 09:01:29
188	3	/justify/6/f/undercut	2017-01-27 09:01:32
189	3	/reaction/6/rebut/7	2017-01-27 09:01:34
190	7	/reaction/6/rebut/7	2017-01-27 09:06:51
194	10	/justify/7/t/undercut	2017-01-27 09:10:06
195	7	/discuss	2017-01-27 09:14:34
196	7	/attitude/4	2017-01-27 09:14:39
198	7	/justify/4/t	2017-01-27 09:14:41
199	7	verbesserung-des-informatik-studiengangs	2017-01-27 09:15:01
200	7	/attitude/4	2017-01-27 09:15:26
202	7	/justify/4/f	2017-01-27 09:15:30
203	7	/reaction/7/rebut/3	2017-01-27 09:15:51
204	10	/reaction/8/end/0	2017-01-27 09:16:26
208	11	/justify/7/t/undercut	2017-01-27 09:17:10
209	10	/discuss	2017-01-27 09:17:47
210	10	/attitude/4	2017-01-27 09:17:53
211	10	/	2017-01-27 09:17:57
212	11	/reaction/9/end/0	2017-01-27 09:19:39
213	11	verbesserung-des-informatik-studiengangs	2017-01-27 09:20:23
214	11	/attitude/4	2017-01-27 09:20:29
216	11	/justify/4/t	2017-01-27 09:20:32
217	11	/reaction/3/rebut/7	2017-01-27 09:20:44
218	11	verbesserung-des-informatik-studiengangs	2017-01-27 09:21:10
219	11	/attitude/4	2017-01-27 09:21:12
221	11	/justify/4/t	2017-01-27 09:21:14
222	11	/reaction/6/rebut/7	2017-01-27 09:21:24
224	11	/justify/4/t	2017-01-27 09:22:29
225	11	/reaction/6/rebut/7	2017-01-27 09:22:44
226	11	/reaction/7/rebut/6	2017-01-27 09:23:24
227	11	/reaction/6/rebut/7	2017-01-27 09:23:53
229	11	/justify/7/t/undercut	2017-01-27 09:24:16
233	11	/justify/4/t	2017-01-27 09:27:16
234	4	/reaction/7/rebut/6	2017-01-27 09:29:40
235	4	/reaction/7/rebut/6	2017-01-27 09:29:41
236	4	/discuss	2017-01-27 09:30:24
237	4	/discuss	2017-01-27 09:30:46
238	4	/attitude/4	2017-01-27 09:30:48
240	4	/justify/4/f	2017-01-27 09:30:50
241	4	/reaction/7/rebut/6	2017-01-27 09:32:37
242	4	/discuss	2017-01-27 09:36:06
243	4	/attitude/6	2017-01-27 09:36:13
245	4	/justify/6/t	2017-01-27 09:36:14
246	4	/news	2017-01-27 09:38:23
247	4	/discuss	2017-01-27 09:38:23
248	4	/attitude/4	2017-01-27 09:38:25
250	4	/justify/4/t	2017-01-27 09:38:41
252	4	/justify/4/f	2017-01-27 09:38:45
253	4	/reaction/7/undercut/8	2017-01-27 09:38:54
254	4	/reaction/8/end/0	2017-01-27 09:39:08
255	4	verbesserung-des-informatik-studiengangs	2017-01-27 09:39:26
256	3	/reaction/6/rebut/7	2017-01-27 09:40:06
257	3	/reaction/6/rebut/7	2017-01-27 09:40:15
258	3	/reaction/6/rebut/7	2017-01-27 09:49:04
259	3	/reaction/7/rebut/6	2017-01-27 09:49:13
260	3	/reaction/6/rebut/7	2017-01-27 09:49:26
261	3	/discuss	2017-01-27 09:49:51
262	3	/attitude/4	2017-01-27 09:50:01
264	3	/justify/4/f	2017-01-27 09:50:06
265	3	/reaction/7/rebut/3	2017-01-27 09:50:14
267	3	/justify/4/f	2017-01-27 09:50:18
268	3	/reaction/7/undercut/9	2017-01-27 09:50:19
270	3	/justify/4/f	2017-01-27 09:50:24
271	3	/reaction/7/rebut/3	2017-01-27 09:50:25
273	3	/justify/4/f	2017-01-27 09:50:27
274	3	/reaction/7/undercut/9	2017-01-27 09:50:28
276	3	/justify/4/f	2017-01-27 09:50:30
277	3	/reaction/7/undercut/8	2017-01-27 09:50:31
279	3	/justify/4/f	2017-01-27 09:50:33
280	3	/reaction/7/rebut/6	2017-01-27 09:50:34
281	3	/reaction/6/rebut/7	2017-01-27 09:51:09
282	3	/reaction/6/rebut/7	2017-01-27 09:58:48
283	3	/reaction/6/rebut/7	2017-01-27 09:58:53
284	4	verbesserung-des-informatik-studiengangs	2017-01-27 09:59:28
285	4	/review	2017-01-27 09:59:30
286	4	/admin/	2017-01-27 09:59:34
287	4	/admin/History	2017-01-27 09:59:38
288	4	/discuss	2017-01-27 10:00:23
289	4	/admin/	2017-01-27 10:00:26
296	12	/justify/4/f/undercut	2017-01-27 10:05:12
300	4	/justify/6/f	2017-01-27 10:07:07
306	4	/attitude/6	2017-01-27 10:10:37
309	4	/justify/6/f	2017-01-27 10:10:44
320	12	/reaction/1/rebut/5	2017-01-27 10:11:32
290	12	/justify/6/f	2017-01-27 10:00:28
311	4	/reaction/10/rebut/4	2017-01-27 10:10:52
291	12	/justify/6/f	2017-01-27 10:00:28
302	4	/discuss	2017-01-27 10:09:00
317	4	/attitude/6	2017-01-27 10:11:21
292	12	/justify/6/f	2017-01-27 10:00:28
293	12	/justify/6/f	2017-01-27 10:00:28
295	12	/reaction/10/rebut/4	2017-01-27 10:04:22
298	4	/justify/6/f	2017-01-27 10:07:06
299	4	/justify/6/f	2017-01-27 10:07:06
305	4	/discuss	2017-01-27 10:10:34
307	4	/justify/6/t	2017-01-27 10:10:39
314	12	/justify/1/t	2017-01-27 10:11:15
315	12	/justify/1/t	2017-01-27 10:11:15
318	4	/justify/6/t	2017-01-27 10:11:23
319	4	/justify/6/t	2017-01-27 10:11:23
294	4	/admin/StatementSeenBy	2017-01-27 10:00:36
297	12	/justify/4/f/undercut	2017-01-27 10:05:12
303	12	/reaction/11/end/0	2017-01-27 10:09:27
313	12	/attitude/1	2017-01-27 10:11:09
316	4	verbesserung-des-informatik-studiengangs	2017-01-27 10:11:19
321	4	/settings	2017-01-27 10:11:57
322	4	/reaction/4/rebut/10	2017-01-27 10:12:25
324	4	/justify/10/t/undermine	2017-01-27 10:12:39
326	12	/justify/5/t/undercut	2017-01-27 10:14:24
327	10	/	2017-01-27 10:19:44
328	10	/notifications	2017-01-27 10:19:50
329	10	/news	2017-01-27 10:19:59
330	10	/discuss	2017-01-27 10:20:18
332	12	/justify/5/t/undercut	2017-01-27 10:24:51
333	12	/reaction/12/end/0	2017-01-27 10:29:22
334	12	/reaction/13/end/0	2017-01-27 10:29:23
335	13	/	2017-01-27 10:29:38
336	13	/	2017-01-27 10:29:38
337	14	/discuss	2017-01-27 10:30:05
338	14	/discuss	2017-01-27 10:30:06
339	13	/discuss	2017-01-27 10:30:20
340	14	/attitude/19	2017-01-27 10:30:54
342	14	/justify/19/t	2017-01-27 10:30:59
343	13	/attitude/1	2017-01-27 10:31:01
345	13	/justify/1/d	2017-01-27 10:31:23
346	13	/user/Tobias	2017-01-27 10:31:30
347	14	/reaction/15/end/0	2017-01-27 10:31:41
348	14	verbesserung-des-informatik-studiengangs	2017-01-27 10:31:48
349	14	/attitude/1	2017-01-27 10:32:26
351	14	/justify/1/f	2017-01-27 10:32:31
352	12	verbesserung-des-informatik-studiengangs	2017-01-27 10:32:45
353	12	/attitude/19	2017-01-27 10:33:52
355	12	/justify/19/t	2017-01-27 10:33:57
356	12	/reaction/15/end/0	2017-01-27 10:34:04
357	12	verbesserung-des-informatik-studiengangs	2017-01-27 10:34:11
358	14	/choose/f/f/1/16/17	2017-01-27 10:34:16
359	12	/attitude/4	2017-01-27 10:34:18
361	12	/justify/4/t	2017-01-27 10:34:22
362	12	/reaction/3/rebut/7	2017-01-27 10:34:31
363	14	/reaction/16/rebut/1	2017-01-27 10:34:34
365	12	/justify/7/t/undercut	2017-01-27 10:34:48
367	14	/justify/1/f/undermine	2017-01-27 10:34:56
368	12	/reaction/8/end/0	2017-01-27 10:35:05
369	14	/reaction/18/end/0	2017-01-27 10:35:51
370	14	verbesserung-des-informatik-studiengangs	2017-01-27 10:36:02
371	4	/discuss	2017-01-27 10:36:07
372	13	/justify/1/t	2017-01-27 10:36:08
373	14	/settings	2017-01-27 10:36:08
374	13	/justify/1/t	2017-01-27 10:36:08
375	14	/discuss	2017-01-27 10:37:00
376	14	/settings	2017-01-27 10:37:22
377	14	/user/graffi	2017-01-27 10:37:28
378	14	/discuss	2017-01-27 10:37:32
379	14	/attitude/4	2017-01-27 10:37:35
381	14	/justify/4/d	2017-01-27 10:37:47
383	14	/justify/4/f	2017-01-27 10:38:10
384	14	/reaction/19/rebut/6	2017-01-27 10:39:41
385	12	verbesserung-des-informatik-studiengangs	2017-01-27 10:40:09
386	4	/choose/f/f/14/20/21	2017-01-27 10:40:49
388	6	/justify/4/f	2017-01-27 10:40:58
389	6	/user/graffi	2017-01-27 10:41:22
391	14	/justify/6/f/undermine	2017-01-27 10:41:24
392	14	verbesserung-des-informatik-studiengangs	2017-01-27 10:42:37
393	14	/attitude/1	2017-01-27 10:42:43
395	14	/justify/1/f	2017-01-27 10:42:51
396	14	/reaction/22/rebut/1	2017-01-27 10:43:50
397	12	/attitude/1	2017-01-27 10:43:55
399	12	/justify/1/d	2017-01-27 10:43:59
401	14	/justify/1/f/undercut	2017-01-27 10:44:12
403	12	/justify/1/t/undercut	2017-01-27 10:44:30
404	13	/reaction/23/rebut/2	2017-01-27 10:44:59
405	14	/reaction/24/end/0	2017-01-27 10:45:05
406	14	/news	2017-01-27 10:45:11
407	4	/discuss	2017-01-27 10:45:53
408	12	/reaction/25/end/0	2017-01-27 10:45:54
409	12	verbesserung-des-informatik-studiengangs	2017-01-27 10:46:02
410	12	/notifications	2017-01-27 10:46:05
411	12	/reaction/10/undermine/21	2017-01-27 10:46:09
413	13	/justify/2/t/undercut	2017-01-27 10:46:12
414	12	/discuss	2017-01-27 10:46:28
415	13	/reaction/26/end/0	2017-01-27 10:47:52
416	13	/reaction/23/rebut/2	2017-01-27 10:48:09
418	13	/justify/1/t	2017-01-27 10:48:34
419	13	/notifications	2017-01-27 10:49:12
420	10	/	2017-01-27 10:49:13
421	10	/review	2017-01-27 10:49:16
422	13	/review	2017-01-27 10:49:19
423	13	/review/ongoing	2017-01-27 10:49:25
424	10	/review/edits	2017-01-27 10:49:41
425	10	/review	2017-01-27 10:50:09
426	13	/discuss	2017-01-27 10:50:25
427	13	/attitude/1	2017-01-27 10:50:31
429	13	/justify/1/t	2017-01-27 10:50:34
430	13	/reaction/1/rebut/17	2017-01-27 10:50:45
431	10	/review	2017-01-27 10:50:48
432	10	/review/ongoing	2017-01-27 10:50:50
433	10	/discuss	2017-01-27 10:51:00
437	11	/justify/1/f	2017-01-27 10:51:23
438	13	verbesserung-des-informatik-studiengangs	2017-01-27 10:51:24
439	13	/attitude/4	2017-01-27 10:51:29
441	13	/justify/4/t	2017-01-27 10:51:34
446	6	/review	2017-01-27 10:52:38
450	6	/discuss	2017-01-27 10:53:19
464	11	/justify/1/f/undercut	2017-01-27 10:54:14
467	12	verbesserung-des-informatik-studiengangs	2017-01-27 10:54:48
469	12	/review/edits	2017-01-27 10:54:58
483	12	/review/ongoing	2017-01-27 10:56:22
489	13	/justify/34/t	2017-01-27 10:56:45
442	13	/reaction/3/rebut/19	2017-01-27 10:51:55
443	12	/justify/21/f/undercut	2017-01-27 10:52:02
447	6	/review/edits	2017-01-27 10:52:42
449	6	/notifications	2017-01-27 10:53:07
452	13	/justify/19/t/undercut	2017-01-27 10:53:24
456	6	/discuss	2017-01-27 10:53:29
472	10	/justify/1/f	2017-01-27 10:55:24
475	6	/justify/34/t	2017-01-27 10:55:44
477	10	/reaction/28/rebut/1	2017-01-27 10:56:03
444	12	/justify/21/f/undercut	2017-01-27 10:52:02
453	13	/justify/19/t/undercut	2017-01-27 10:53:24
458	4	/notifications	2017-01-27 10:53:39
460	12	/reaction/27/end/0	2017-01-27 10:53:50
466	6	/discuss	2017-01-27 10:54:15
468	12	/review	2017-01-27 10:54:51
471	10	/attitude/1	2017-01-27 10:55:19
473	10	/justify/1/f	2017-01-27 10:55:25
474	6	/attitude/34	2017-01-27 10:55:41
476	6	/justify/34/t	2017-01-27 10:55:44
479	12	/review/edits	2017-01-27 10:56:12
484	13	verbesserung-des-informatik-studiengangs	2017-01-27 10:56:29
487	13	/attitude/34	2017-01-27 10:56:41
492	10	/review/ongoing	2017-01-27 10:57:00
493	13	/reaction/31/end/0	2017-01-27 10:57:39
445	6	/	2017-01-27 10:52:33
457	4	/news	2017-01-27 10:53:36
459	4	/reaction/5/undercut/13	2017-01-27 10:53:42
465	11	/justify/1/f/undercut	2017-01-27 10:54:14
478	6	/reaction/29/end/0	2017-01-27 10:56:10
490	13	/justify/34/t	2017-01-27 10:56:45
491	10	/review	2017-01-27 10:56:54
495	13	/	2017-01-27 10:57:59
448	6	/review/edits	2017-01-27 10:53:02
455	6	/justify/1/t	2017-01-27 10:53:25
462	4	/justify/13/f/undermine	2017-01-27 10:54:02
480	4	/review/edits	2017-01-27 10:56:14
481	12	/review	2017-01-27 10:56:15
485	10	/justify/1/f/undermine	2017-01-27 10:56:33
488	10	/reaction/18/end/0	2017-01-27 10:56:43
494	13	verbesserung-des-informatik-studiengangs	2017-01-27 10:57:46
451	6	/attitude/1	2017-01-27 10:53:23
454	6	/justify/1/t	2017-01-27 10:53:25
461	11	/reaction/28/rebut/1	2017-01-27 10:54:00
463	4	/justify/13/f/undermine	2017-01-27 10:54:02
470	4	/review	2017-01-27 10:55:05
482	13	/reaction/30/end/0	2017-01-27 10:56:21
486	10	/justify/1/f/undermine	2017-01-27 10:56:33
496	13	/discuss	2017-01-27 10:58:04
497	4	/review/edits	2017-01-27 10:58:24
498	4	/notifications	2017-01-27 10:58:27
499	13	/attitude/4	2017-01-27 10:59:57
501	13	/justify/4/t	2017-01-27 10:59:59
502	13	/reaction/6/rebut/7	2017-01-27 11:00:04
504	13	/justify/4/t	2017-01-27 11:01:10
505	11	verbesserung-des-informatik-studiengangs	2017-01-27 11:01:44
506	12	/discuss	2017-01-27 11:01:45
507	11	/attitude/1	2017-01-27 11:01:52
509	11	/justify/1/t	2017-01-27 11:01:56
510	11	/reaction/1/undercut/25	2017-01-27 11:02:22
511	12	/attitude/34	2017-01-27 11:02:52
513	12	/justify/34/t	2017-01-27 11:02:58
515	11	/justify/1/t	2017-01-27 11:03:12
516	4	/discuss	2017-01-27 11:03:31
518	11	/justify/25/t/undercut	2017-01-27 11:03:34
519	4	/news	2017-01-27 11:03:42
520	4	/notifications	2017-01-27 11:03:44
521	12	/news	2017-01-27 11:03:50
522	12	/notifications	2017-01-27 11:03:54
523	11	/discuss	2017-01-27 11:04:13
524	11	/attitude/1	2017-01-27 11:04:17
526	11	/justify/1/f	2017-01-27 11:04:23
527	13	/reaction/32/rebut/7	2017-01-27 11:04:23
528	14	/reaction/19/undercut/30	2017-01-27 11:04:24
530	11	/justify/1/t	2017-01-27 11:04:28
531	11	/reaction/1/undercut/25	2017-01-27 11:04:37
533	14	/justify/30/f/undercut	2017-01-27 11:05:05
534	12	/	2017-01-27 11:05:13
535	4	/notifications	2017-01-27 11:05:13
536	12	/discuss	2017-01-27 11:05:15
537	12	/notifications	2017-01-27 11:05:51
538	12	/	2017-01-27 11:05:56
539	12	/discuss	2017-01-27 11:05:58
540	11	verbesserung-des-informatik-studiengangs	2017-01-27 11:06:04
541	12	/attitude/34	2017-01-27 11:06:04
543	12	/justify/34/t	2017-01-27 11:06:07
544	11	/attitude/1	2017-01-27 11:06:07
546	11	/justify/1/t	2017-01-27 11:06:15
547	11	/attitude/31	2017-01-27 11:07:02
548	11	/attitude/37	2017-01-27 11:07:35
549	11	verbesserung-des-informatik-studiengangs	2017-01-27 11:07:47
551	13	/justify/7/t/undercut	2017-01-27 11:07:52
552	11	/attitude/31	2017-01-27 11:08:09
553	11	verbesserung-des-informatik-studiengangs	2017-01-27 11:08:15
554	14	/reaction/33/end/0	2017-01-27 11:08:21
555	10	/	2017-01-27 11:08:24
556	10	/discuss	2017-01-27 11:08:26
557	11	/attitude/4	2017-01-27 11:09:17
558	10	/attitude/1	2017-01-27 11:09:20
559	10	verbesserung-des-informatik-studiengangs	2017-01-27 11:09:25
560	10	/attitude/4	2017-01-27 11:09:30
561	11	/attitude/35	2017-01-27 11:09:31
563	10	/justify/4/t	2017-01-27 11:09:32
564	10	/reaction/32/rebut/19	2017-01-27 11:09:49
565	10	/reaction/19/rebut/3	2017-01-27 11:10:02
566	11	/attitude/35	2017-01-27 11:10:24
567	10	/reaction/3/rebut/19	2017-01-27 11:10:48
568	10	/reaction/19/rebut/32	2017-01-27 11:10:57
569	14	verbesserung-des-informatik-studiengangs	2017-01-27 11:11:10
570	12	/reaction/29/end/0	2017-01-27 11:11:18
571	13	/reaction/34/end/0	2017-01-27 11:11:30
572	13	verbesserung-des-informatik-studiengangs	2017-01-27 11:11:34
573	11	/attitude/10	2017-01-27 11:11:43
574	12	verbesserung-des-informatik-studiengangs	2017-01-27 11:11:56
575	10	/reaction/32/rebut/19	2017-01-27 11:11:56
576	14	/attitude/37	2017-01-27 11:12:02
578	14	/justify/37/t	2017-01-27 11:12:09
579	10	/discuss	2017-01-27 11:12:12
580	10	/discuss	2017-01-27 11:12:19
581	13	/reaction/30/undercut/33	2017-01-27 11:12:19
582	14	verbesserung-des-informatik-studiengangs	2017-01-27 11:12:24
583	14	/attitude/37	2017-01-27 11:12:26
585	14	/justify/37/f	2017-01-27 11:12:35
586	11	/attitude/15	2017-01-27 11:12:42
587	14	verbesserung-des-informatik-studiengangs	2017-01-27 11:12:45
588	14	/attitude/37	2017-01-27 11:12:48
590	14	/justify/37/d	2017-01-27 11:12:52
591	14	verbesserung-des-informatik-studiengangs	2017-01-27 11:12:55
592	14	/attitude/37	2017-01-27 11:12:57
594	14	/justify/37/f	2017-01-27 11:13:05
595	11	/attitude/37	2017-01-27 11:13:14
597	11	/justify/37/t	2017-01-27 11:13:18
599	11	/justify/37/f	2017-01-27 11:13:34
601	11	/justify/37/t	2017-01-27 11:13:43
602	14	/reaction/35/end/0	2017-01-27 11:14:48
604	11	/justify/37/f	2017-01-27 11:14:59
605	13	/justify/33/f/undermine	2017-01-27 11:15:37
608	13	/justify/33/f/undermine	2017-01-27 11:15:48
610	13	/justify/33/f/undermine	2017-01-27 11:15:52
612	11	/reaction/36/rebut/35	2017-01-27 11:16:06
613	12	/attitude/37	2017-01-27 11:16:24
614	12	/justify/37/d	2017-01-27 11:16:27
615	12	/justify/37/d	2017-01-27 11:16:27
622	11	/justify/35/t/undercut	2017-01-27 11:18:02
625	5	/	2017-01-27 11:18:50
634	11	/reaction/37/end/0	2017-01-27 11:20:45
637	13	/justify/38/f	2017-01-27 11:23:15
644	14	/reaction/35/undercut/37	2017-01-27 11:29:26
654	13	/reaction/40/rebut/4	2017-01-27 11:32:52
656	13	/justify/4/f/undercut	2017-01-27 11:33:11
664	13	/review/ongoing	2017-01-27 11:36:33
667	13	/user/hisch100	2017-01-27 11:37:39
668	13	/review/reputation	2017-01-27 11:38:08
671	13	/user/hisch100	2017-01-27 11:40:13
672	13	/discuss	2017-01-27 11:40:21
697	13	verbesserung-des-informatik-studiengangs	2017-01-27 11:46:52
703	13	/review/history	2017-01-27 11:54:15
704	13	/review/ongoing	2017-01-27 11:54:21
710	13	/justify/48/d	2017-01-27 11:55:08
712	13	/justify/48/t	2017-01-27 11:55:11
616	12	/	2017-01-27 11:16:39
618	13	/justify/33/f/undermine	2017-01-27 11:17:09
624	12	/discuss	2017-01-27 11:18:37
626	13	/justify/33/f/undermine	2017-01-27 11:19:23
630	13	/justify/33/f/undermine	2017-01-27 11:19:35
632	5	/review/edits	2017-01-27 11:19:38
635	11	/notifications	2017-01-27 11:20:56
639	13	verbesserung-des-informatik-studiengangs	2017-01-27 11:26:11
642	13	/justify/6/f	2017-01-27 11:28:50
651	13	/attitude/6	2017-01-27 11:31:35
658	13	verbesserung-des-informatik-studiengangs	2017-01-27 11:34:06
662	13	/justify/33/f/undermine	2017-01-27 11:34:25
666	13	/user/hisch100	2017-01-27 11:37:04
669	13	/news	2017-01-27 11:39:44
674	13	/settings	2017-01-27 11:41:27
675	13	/review	2017-01-27 11:41:28
680	13	/attitude/19	2017-01-27 11:42:45
681	13	/justify/19/d	2017-01-27 11:42:52
685	5	/review/edits	2017-01-27 11:43:45
692	5	/review/edits	2017-01-27 11:44:51
709	13	/justify/48/d	2017-01-27 11:54:56
714	14	/reaction/43/end/0	2017-01-27 11:59:41
721	14	/review	2017-01-27 12:01:52
617	12	/discuss	2017-01-27 11:16:42
645	14	/justify/37/f/undercut	2017-01-27 11:29:50
648	13	/justify/21/f/undermine	2017-01-27 11:30:24
649	13	/reaction/39/end/0	2017-01-27 11:31:18
653	13	/justify/6/f	2017-01-27 11:31:37
657	13	/reaction/11/end/0	2017-01-27 11:33:55
663	13	/review	2017-01-27 11:36:31
665	13	/settings	2017-01-27 11:36:59
670	13	/settings	2017-01-27 11:39:50
673	13	/review	2017-01-27 11:40:26
676	13	/review/ongoing	2017-01-27 11:41:31
679	13	/discuss	2017-01-27 11:42:34
686	5	/review	2017-01-27 11:43:55
688	5	/review/optimizations	2017-01-27 11:43:59
695	13	/justify/48/t	2017-01-27 11:45:25
706	13	/discuss	2017-01-27 11:54:47
640	13	/attitude/6	2017-01-27 11:28:48
641	13	/justify/6/f	2017-01-27 11:28:50
650	13	verbesserung-des-informatik-studiengangs	2017-01-27 11:31:23
659	13	/notifications	2017-01-27 11:34:11
661	13	/justify/33/f/undermine	2017-01-27 11:34:25
682	13	/justify/19/d	2017-01-27 11:42:52
693	13	/attitude/48	2017-01-27 11:45:20
699	13	/review/history	2017-01-27 11:53:26
701	13	/review/edits	2017-01-27 11:54:05
702	13	/review	2017-01-27 11:54:08
705	13	/settings	2017-01-27 11:54:44
708	13	/justify/48/d	2017-01-27 11:54:56
716	14	/review	2017-01-27 12:00:57
717	14	/review/edits	2017-01-27 12:01:08
620	4	/discuss	2017-01-27 11:17:53
621	11	/justify/35/t/undercut	2017-01-27 11:18:02
628	5	/review	2017-01-27 11:19:29
629	13	/reaction/30/undercut/33	2017-01-27 11:19:33
636	13	/justify/38/f	2017-01-27 11:23:15
643	13	/reaction/10/undermine/21	2017-01-27 11:29:00
655	13	/justify/4/f/undercut	2017-01-27 11:33:11
677	13	/user/alsch132	2017-01-27 11:42:04
678	13	/news	2017-01-27 11:42:14
684	13	verbesserung-des-informatik-studiengangs	2017-01-27 11:43:07
687	5	/review	2017-01-27 11:43:56
690	5	/review	2017-01-27 11:44:40
691	5	/review/edits	2017-01-27 11:44:45
700	13	/review/edits	2017-01-27 11:53:44
711	13	/justify/48/d	2017-01-27 11:55:08
713	13	/justify/48/t	2017-01-27 11:55:12
715	14	/notifications	2017-01-27 12:00:55
718	14	/review/edits	2017-01-27 12:01:34
719	14	/review/edits	2017-01-27 12:01:43
720	14	/review/edits	2017-01-27 12:01:49
623	12	/attitude/4	2017-01-27 11:18:20
638	13	/reaction/38/end/0	2017-01-27 11:25:32
646	14	/justify/37/f/undercut	2017-01-27 11:29:50
647	13	/justify/21/f/undermine	2017-01-27 11:30:24
652	13	/justify/6/f	2017-01-27 11:31:37
660	13	/reaction/30/undercut/33	2017-01-27 11:34:21
683	13	/reaction/15/end/0	2017-01-27 11:43:04
689	5	/review/optimizations	2017-01-27 11:44:38
694	13	/justify/48/t	2017-01-27 11:45:25
696	13	/choose/f/t/48/39/40	2017-01-27 11:46:41
698	13	/review	2017-01-27 11:53:21
707	13	/attitude/48	2017-01-27 11:54:52
722	4	/discuss	2017-01-27 12:13:54
723	4	/discuss	2017-01-27 12:14:01
724	4	/notifications	2017-01-27 12:14:05
725	4	/reaction/21/undermine/39	2017-01-27 12:14:09
726	4	/discuss	2017-01-27 12:14:30
727	11	/discuss	2017-01-27 12:15:46
728	11	/discuss	2017-01-27 12:15:46
729	11	/attitude/31	2017-01-27 12:16:05
730	12	/	2017-01-27 12:16:59
731	12	/review	2017-01-27 12:17:04
732	3	/discuss	2017-01-27 12:17:05
733	12	/review/history	2017-01-27 12:17:10
734	12	/review/edits	2017-01-27 12:17:16
735	4	/discuss	2017-01-27 12:17:23
736	4	/discuss	2017-01-27 12:17:30
737	4	/review	2017-01-27 12:17:31
738	3	/attitude/48	2017-01-27 12:17:39
739	4	/review/edits	2017-01-27 12:17:40
740	3	/attitude/31	2017-01-27 12:17:42
741	12	/review/edits	2017-01-27 12:17:44
743	4	/notifications	2017-01-27 12:17:59
744	4	/discuss	2017-01-27 12:18:01
745	6	/	2017-01-27 12:21:26
746	6	/discuss	2017-01-27 12:21:29
748	6	/justify/37/t	2017-01-27 12:21:40
749	6	/justify/37/t	2017-01-27 12:21:40
750	12	/review/edits	2017-01-27 12:22:07
751	12	/discuss	2017-01-27 12:22:10
753	12	/justify/48/t	2017-01-27 12:22:22
754	12	/justify/48/t	2017-01-27 12:22:22
755	12	/reaction/44/end/0	2017-01-27 12:23:38
756	12	verbesserung-des-informatik-studiengangs	2017-01-27 12:24:32
757	12	/attitude/48	2017-01-27 12:24:41
758	12	/justify/48/d	2017-01-27 12:24:43
759	12	/justify/48/d	2017-01-27 12:24:43
760	10	/	2017-01-27 12:27:36
761	10	/discuss	2017-01-27 12:27:41
762	4	/discuss	2017-01-27 12:28:03
763	4	/discuss	2017-01-27 12:28:07
764	4	/discuss	2017-01-27 12:28:10
766	4	/admin/	2017-01-27 12:28:18
767	4	/notifications	2017-01-27 12:28:20
768	4	/review	2017-01-27 12:28:35
769	4	/discuss	2017-01-27 12:28:37
770	4	/attitude/48	2017-01-27 12:28:45
771	4	/justify/48/f	2017-01-27 12:28:47
773	6	/discuss	2017-01-27 12:29:58
774	4	/reaction/45/rebut/41	2017-01-27 12:29:59
775	6	/attitude/1	2017-01-27 12:30:03
776	6	/discuss	2017-01-27 12:30:06
777	6	/discuss	2017-01-27 12:35:57
778	12	/justify/41/t/undercut	2017-01-27 12:37:23
779	12	/justify/41/t/undercut	2017-01-27 12:37:24
780	12	/reaction/46/end/0	2017-01-27 12:38:27
781	5	/	2017-01-27 12:38:34
782	12	verbesserung-des-informatik-studiengangs	2017-01-27 12:38:39
783	5	/discuss	2017-01-27 12:38:40
785	5	/	2017-01-27 12:43:44
786	5	/contact	2017-01-27 12:43:52
788	5	/discuss	2017-01-27 12:44:11
789	5	/attitude/48	2017-01-27 12:44:18
790	5	/justify/48/f	2017-01-27 12:44:22
792	5	/reaction/45/rebut/41	2017-01-27 12:44:32
794	5	/justify/41/f/undercut	2017-01-27 12:45:45
795	5	/discuss	2017-01-27 12:46:07
796	5	/attitude/37	2017-01-27 12:46:23
798	5	/justify/37/d	2017-01-27 12:46:32
799	5	/justify/36/t/undercut	2017-01-27 12:47:01
801	5	/discuss	2017-01-27 12:47:36
802	5	/attitude/6	2017-01-27 12:47:40
803	5	/justify/6/t	2017-01-27 12:47:55
804	5	/justify/6/t	2017-01-27 12:47:55
805	5	/reaction/4/rebut/10	2017-01-27 12:47:59
806	5	/justify/10/t/undercut	2017-01-27 12:48:20
807	5	/justify/10/t/undercut	2017-01-27 12:48:20
808	5	/reaction/47/end/0	2017-01-27 12:49:53
809	5	/reaction/47/end/0	2017-01-27 12:50:45
810	12	verbesserung-des-informatik-studiengangs	2017-01-27 12:51:12
811	12	/notifications	2017-01-27 12:51:16
812	12	/reaction/10/undercut/47	2017-01-27 12:51:20
813	12	/reaction/47/end/0	2017-01-27 12:51:53
814	12	verbesserung-des-informatik-studiengangs	2017-01-27 12:52:03
815	6	/	2017-01-27 12:52:11
816	6	/discuss	2017-01-27 12:52:15
817	3	/discuss	2017-01-27 12:52:16
818	5	/settings	2017-01-27 12:53:53
819	5	/settings	2017-01-27 12:54:06
821	5	/	2017-01-27 12:54:29
825	5	/attitude/4	2017-01-27 12:56:03
826	5	/justify/4/f	2017-01-27 12:56:05
827	5	/justify/4/f	2017-01-27 12:56:05
828	13	/justify/46/t/undercut	2017-01-27 12:56:09
829	13	/justify/46/t/undercut	2017-01-27 12:56:09
830	13	/justify/46/t/undercut	2017-01-27 12:56:09
831	13	/justify/46/t/undercut	2017-01-27 12:56:09
832	5	/reaction/19/undercut/30	2017-01-27 12:56:25
833	13	/reaction/48/end/0	2017-01-27 12:57:04
834	13	/review	2017-01-27 12:57:15
836	13	/review	2017-01-27 12:57:33
837	13	/user/alsch132	2017-01-27 12:57:39
839	13	/discuss	2017-01-27 12:59:14
840	13	/attitude/48	2017-01-27 12:59:29
841	13	/justify/48/d	2017-01-27 12:59:33
842	13	/justify/48/d	2017-01-27 12:59:33
843	13	/reaction/42/rebut/45	2017-01-27 12:59:39
844	13	/justify/45/t/undermine	2017-01-27 12:59:51
845	13	/justify/45/t/undermine	2017-01-27 12:59:51
846	5	/discuss	2017-01-27 13:00:29
847	5	/review	2017-01-27 13:01:07
848	5	/review/history	2017-01-27 13:01:09
849	13	/reaction/49/end/0	2017-01-27 13:01:18
850	5	/review	2017-01-27 13:01:39
851	13	/reaction/50/end/0	2017-01-27 13:01:45
852	5	/review/history	2017-01-27 13:01:54
853	13	/notifications	2017-01-27 13:02:11
854	13	/notifications	2017-01-27 13:02:20
855	3	/discuss	2017-01-27 13:12:21
856	3	/discuss	2017-01-27 13:29:55
857	3	/discuss	2017-01-27 13:31:55
858	3	/discuss	2017-01-27 13:32:51
859	3	/discuss	2017-01-27 13:35:13
860	3	/discuss	2017-01-27 13:37:18
861	3	/discuss	2017-01-27 13:40:36
862	3	/review	2017-01-27 13:40:56
863	3	/review/history	2017-01-27 13:41:02
864	3	/review	2017-01-27 13:42:30
865	3	/admin/	2017-01-27 13:42:32
866	3	/admin/Argument	2017-01-27 13:42:35
867	3	/admin/User	2017-01-27 13:44:15
868	5	/discuss	2017-01-27 13:52:35
869	3	/admin/Argument	2017-01-27 13:54:08
870	3	/admin/Statements	2017-01-27 13:57:26
871	3	/admin/Statement	2017-01-27 13:57:30
872	3	/review	2017-01-27 13:57:50
873	3	/review/history	2017-01-27 13:57:53
874	5	/discuss	2017-01-27 13:59:06
875	5	finish	2017-01-27 13:59:18
876	3	/discuss	2017-01-27 14:37:13
877	3	/discuss	2017-01-27 14:37:15
878	3	/admin/	2017-01-27 14:55:01
879	3	/admin/	2017-01-27 15:40:01
880	3	/discuss	2017-01-27 15:40:10
881	3	/discuss	2017-01-27 15:45:39
882	6	/discuss	2017-01-27 16:15:08
883	3	/admin/	2017-01-27 17:57:36
884	3	/notifications	2017-01-27 18:03:13
885	3	/discuss	2017-01-27 18:05:33
886	3	/notifications	2017-01-27 19:55:34
887	5	/discuss	2017-01-27 20:23:45
888	3	/discuss	2017-01-27 20:48:11
889	3	/review	2017-01-27 22:20:52
890	3	/review/history	2017-01-27 22:20:57
891	3	/review/history	2017-01-27 22:21:24
892	3	/discuss	2017-01-27 23:24:22
893	3	/admin/	2017-01-27 23:39:47
894	3	/admin/ReviewDeleteReason	2017-01-27 23:39:51
895	3	/admin/ReviewDeleteReason	2017-01-27 23:39:58
896	3	/admin/ReviewDeleteReason	2017-01-27 23:43:29
897	7	/	2017-01-28 07:35:50
898	7	/	2017-01-28 07:35:50
899	7	/notifications	2017-01-28 07:36:00
900	7	/settings	2017-01-28 07:36:07
901	7	/review/reputation	2017-01-28 07:36:21
902	7	/review	2017-01-28 07:36:34
903	7	/review/history	2017-01-28 07:36:58
904	3	/review/history	2017-01-28 08:29:59
905	7	/	2017-01-28 08:32:52
906	7	/review	2017-01-28 08:32:55
907	7	/review/history	2017-01-28 08:33:02
908	3	/review	2017-01-28 08:34:56
909	15	/	2017-01-28 08:35:13
910	15	/	2017-01-28 08:35:14
911	7	/review	2017-01-28 08:35:31
912	15	/review	2017-01-28 08:35:32
913	15	/review/history	2017-01-28 08:35:43
914	15	/review/reputation	2017-01-28 08:36:02
915	15	/admin/User	2017-01-28 08:37:09
916	3	/	2017-01-28 08:48:07
917	3	/	2017-01-28 08:48:07
918	3	/admin/	2017-01-28 08:48:10
919	3	/admin/User	2017-01-28 08:48:11
920	3	/admin/User	2017-01-28 08:48:22
921	3	/admin/User	2017-01-28 08:48:53
922	3	/admin/User	2017-01-28 08:49:04
923	3	/admin/User	2017-01-28 08:49:20
924	7	/	2017-01-28 08:50:46
925	7	/review	2017-01-28 08:50:50
926	7	/review/history	2017-01-28 08:51:01
927	3	/	2017-01-28 08:57:01
928	3	/	2017-01-28 08:57:05
929	3	/review	2017-01-28 08:57:09
930	3	/admin/	2017-01-28 08:57:37
931	3	/admin/Settings	2017-01-28 08:57:40
932	3	/admin/	2017-01-28 08:57:46
933	3	/admin/User	2017-01-28 08:57:48
934	3	/admin/User	2017-01-28 08:58:03
935	3	/admin/User	2017-01-28 08:58:20
936	3	/admin/History	2017-01-28 09:00:30
937	3	/admin/User	2017-01-28 09:01:37
938	3	/admin/User	2017-01-28 09:01:45
939	3	/	2017-01-28 12:53:36
941	15	/	2017-01-28 13:05:28
942	15	/	2017-01-28 13:05:28
943	15	/justify/43/f/undermine	2017-01-28 20:58:14
945	15	/	2017-01-28 20:58:18
946	15	/discuss	2017-01-28 21:15:33
947	15	/justify/43/f/undermine	2017-01-28 21:15:45
948	15	/justify/43/f/undermine	2017-01-28 21:15:45
949	15	/	2017-01-28 21:21:51
950	3	/	2017-01-28 21:22:18
951	3	/	2017-01-28 21:22:18
952	3	/admin/	2017-01-28 21:22:26
953	3	/discuss	2017-01-29 11:12:01
954	5	/discuss	2017-01-29 15:33:30
956	5	/discuss	2017-01-29 15:33:43
957	5	/jump/22	2017-01-29 15:36:30
958	3	/admin/	2017-01-29 15:37:00
959	3	/admin/	2017-01-29 15:37:02
960	3	/admin/	2017-01-29 15:37:04
964	5	/	2017-01-29 15:37:53
965	3	/admin/	2017-01-29 15:38:12
966	3	/admin/History	2017-01-29 15:42:44
968	4	/justify/19/t	2017-01-29 20:00:59
970	4	/justify/19/t	2017-01-29 20:00:59
971	4	/justify/19/t	2017-01-29 20:00:59
991	16	/discuss	2017-01-30 01:01:57
997	16		2017-01-30 01:06:38
1003	16	/justify/1/f	2017-01-30 01:12:27
1019	16	/reaction/49/end/0	2017-01-30 01:31:23
1032	16	/justify/34/f	2017-01-30 01:36:16
1033	16	/reaction/59/rebut/29	2017-01-30 01:37:58
1037	16	verbesserung-des-informatik-studiengangs	2017-01-30 01:39:36
988	16	/settings	2017-01-30 00:55:17
989	16	/user/Tobias	2017-01-30 00:55:19
990	16	/news	2017-01-30 00:58:59
993	16	/review/history	2017-01-30 01:02:06
995	16	/review/history	2017-01-30 01:04:29
996	16	/discuss	2017-01-30 01:06:32
999	16	/attitude/1	2017-01-30 01:09:50
1000	16		2017-01-30 01:10:04
1001	16	/attitude/1	2017-01-30 01:12:19
1004	16	/reaction/5/undercut/12	2017-01-30 01:16:43
1008	16	/discuss	2017-01-30 01:26:20
1009	16	/attitude/48	2017-01-30 01:26:38
1010	16	/justify/48/d	2017-01-30 01:26:42
1011	16	/justify/48/d	2017-01-30 01:26:42
1013	16	/justify/45/t/undermine	2017-01-30 01:27:09
1014	16	/justify/45/t/undermine	2017-01-30 01:27:09
1015	16	/reaction/49/end/0	2017-01-30 01:31:01
1017	16	/justify/45/t/undermine	2017-01-30 01:31:18
1018	16	/justify/45/t/undermine	2017-01-30 01:31:18
1020	16	verbesserung-des-informatik-studiengangs	2017-01-30 01:31:33
1021	16	/attitude/19	2017-01-30 01:31:37
1022	16	/justify/19/t	2017-01-30 01:31:39
1023	16	/justify/19/t	2017-01-30 01:31:39
1024	16	/reaction/58/end/0	2017-01-30 01:32:14
1025	16	/justify/19/t	2017-01-30 01:32:21
1026	16	/justify/19/t	2017-01-30 01:32:21
1027	16	/justify/19/t	2017-01-30 01:32:46
1028	16	/justify/19/t	2017-01-30 01:32:46
1029	16	verbesserung-des-informatik-studiengangs	2017-01-30 01:36:05
1030	16	/attitude/34	2017-01-30 01:36:12
1031	16	/justify/34/f	2017-01-30 01:36:16
1034	16	/justify/29/f/undermine	2017-01-30 01:38:28
1035	16	/justify/29/f/undermine	2017-01-30 01:38:28
1036	16	/reaction/60/end/0	2017-01-30 01:39:33
1038	16	/attitude/4	2017-01-30 01:39:43
1039	16	/justify/4/t	2017-01-30 01:39:46
1040	16	/justify/4/t	2017-01-30 01:39:46
1041	16	/reaction/6/rebut/19	2017-01-30 01:39:58
1042	16	/reaction/19/undercut/30	2017-01-30 01:40:36
1043	16	/reaction/30/end/0	2017-01-30 01:41:29
1044	16	verbesserung-des-informatik-studiengangs	2017-01-30 01:41:33
1045	3	/admin/History	2017-01-30 07:25:54
1046	3	/admin/History	2017-01-30 08:01:06
1047	3	/admin/	2017-01-30 08:02:08
1048	3	/admin/TextVersion	2017-01-30 08:02:13
1049	3	/discuss	2017-01-30 08:02:46
1050	7	/discuss	2017-01-30 08:03:06
1051	7	/review	2017-01-30 08:03:45
1052	7	/review	2017-01-30 08:07:26
1053	7	/reaction/7/rebut/6	2017-01-30 08:18:00
1054	7	/reaction/7/rebut/6	2017-01-30 08:18:07
1055	7	/reaction/7/rebut/6	2017-01-30 08:18:34
1056	7	/reaction/7/rebut/6	2017-01-30 08:19:24
1057	7	/	2017-01-30 08:20:30
1058	12	/discuss	2017-01-30 08:22:55
1059	7	/reaction/7/rebut/6	2017-01-30 08:26:30
1060	7	/reaction/7/rebut/6	2017-01-30 08:26:38
1061	7	/reaction/7/rebut/6	2017-01-30 08:26:54
1062	7	/reaction/7/rebut/6	2017-01-30 08:28:10
1063	7	/reaction/7/rebut/6	2017-01-30 08:28:20
1064	3	/reaction/7/rebut/6	2017-01-30 08:36:23
1065	3	/reaction/7/rebut/6	2017-01-30 08:36:30
1066	7	/review	2017-01-30 08:45:59
1067	7	/	2017-01-30 08:46:09
1068	7	/discuss	2017-01-30 08:49:02
1069	7	/attitude/37	2017-01-30 08:53:10
1070	7	/justify/37/t	2017-01-30 08:54:12
1071	7	/justify/37/t	2017-01-30 08:54:12
1072	7	/reaction/36/rebut/35	2017-01-30 08:54:48
1073	7	/reaction/35/undercut/37	2017-01-30 08:55:30
1074	7	/justify/37/f/undercut	2017-01-30 08:56:39
1075	7	/justify/37/f/undercut	2017-01-30 08:56:39
1076	7	/reaction/43/end/0	2017-01-30 08:56:57
1077	4	/	2017-01-30 08:58:15
1078	4	/	2017-01-30 08:58:15
1079	7	/discuss	2017-01-30 08:58:54
1080	7	/jump/37	2017-01-30 08:59:26
1081	4	/notifications	2017-01-30 09:00:10
1082	4	/reaction/45/undermine/50	2017-01-30 09:00:15
1083	4	/justify/54/f	2017-01-30 09:01:23
1084	4	/justify/54/f	2017-01-30 09:01:23
1085	7	/jump/58	2017-01-30 09:01:40
1086	4	/jump/58	2017-01-30 09:02:14
1087	3	/admin/TextVersion	2017-01-30 09:03:08
1088	7	/jump/6	2017-01-30 09:03:39
1089	3	/jump/58	2017-01-30 09:03:48
1090	3	/jump/6	2017-01-30 09:04:03
1091	12	/jump/58	2017-01-30 09:04:07
1092	12	/review	2017-01-30 09:04:19
1093	7	/justify/4/t	2017-01-30 09:07:04
1094	7	/justify/4/t	2017-01-30 09:07:04
1095	12	/jump/58	2017-01-30 09:07:09
1096	7	/reaction/61/rebut/19	2017-01-30 09:08:59
1097	7	/review	2017-01-30 09:09:08
1098	7	/discuss	2017-01-30 09:09:18
1099	7	/jump/22	2017-01-30 09:09:46
1100	4	/jump/58	2017-01-30 09:19:43
1101	4	/admin/	2017-01-30 09:22:59
1102	4	/review	2017-01-30 09:23:15
1103	4	/review/optimizations	2017-01-30 09:23:20
1104	3	/	2017-01-30 09:28:21
1105	7	/	2017-01-30 09:29:18
1106	7	/settings	2017-01-30 09:29:26
1107	15	/	2017-01-30 09:29:40
1108	15	/	2017-01-30 09:29:40
1109	7	/settings	2017-01-30 09:29:56
1110	7	/settings	2017-01-30 09:30:06
1111	7	/settings	2017-01-30 09:37:15
1112	7	/settings	2017-01-30 09:38:28
1113	15	/news	2017-01-30 10:33:45
1114	4	/discuss	2017-01-30 12:59:36
1115	4	/discuss	2017-01-30 12:59:36
1116	4	/justify/19/t	2017-01-30 13:02:32
1117	4	/reaction/15/end/0	2017-01-30 13:02:45
1118	4	/reaction/58/end/0	2017-01-30 13:02:48
1119	4	/news	2017-01-30 13:03:02
1120	4	/discuss	2017-01-30 13:03:08
1121	4	/	2017-01-30 13:03:12
1122	4	/discuss	2017-01-30 13:07:49
1123	4	/attitude/37	2017-01-30 13:07:53
1124	4	/justify/37/t	2017-01-30 13:07:56
1125	15	/discuss	2017-01-30 14:14:21
1126	15	/discuss	2017-01-30 14:14:22
1127	3	/	2017-01-30 14:14:37
1128	3	/	2017-01-30 14:14:37
1129	4	/	2017-01-30 14:30:22
1130	4	/	2017-01-30 14:30:22
1131	17	/	2017-01-30 14:30:32
1132	17	/	2017-01-30 14:30:32
1133	17	/discuss	2017-01-30 14:31:47
1134	17	/notifications	2017-01-30 14:31:52
1135	4	/	2017-01-30 14:31:58
1136	4	/	2017-01-30 14:31:58
1137	3	/discuss	2017-01-30 14:34:47
1138	15	/	2017-01-30 14:43:25
1139	15	/	2017-01-30 14:43:26
1140	6	/	2017-01-30 14:53:02
1141	6	/	2017-01-30 14:53:02
1142	6	/settings	2017-01-30 14:53:07
1143	6	/settings	2017-01-30 14:53:23
1144	6	/	2017-01-30 14:53:40
1145	6	/	2017-01-30 14:53:40
1146	6	/notifications	2017-01-30 14:54:15
1147	6	/review	2017-01-30 14:54:26
1148	6	/review/optimizations	2017-01-30 14:54:31
1149	6	/review	2017-01-30 14:54:49
1150	6	/review/edits	2017-01-30 14:54:53
1151	6	/review/edits	2017-01-30 14:55:17
1152	6	/review/edits	2017-01-30 14:55:24
1153	6	/review/edits	2017-01-30 14:55:32
1154	6	/review/edits	2017-01-30 14:56:19
1155	6	/discuss	2017-01-30 14:56:28
1156	6	/attitude/37	2017-01-30 14:56:37
1157	6	/justify/37/t	2017-01-30 14:56:41
1158	6	/reaction/62/rebut/35	2017-01-30 14:58:07
1159	6	/reaction/35/rebut/36	2017-01-30 14:58:34
1160	6	/justify/36/f/undercut	2017-01-30 14:59:26
1161	6	/discuss	2017-01-30 15:00:24
1162	5	/justify/37/t	2017-01-30 15:03:38
1163	5	/justify/37/t	2017-01-30 15:07:44
1164	4	/	2017-01-30 15:16:57
1165	4	/settings	2017-01-30 15:18:21
1166	5	/reaction/62/rebut/35	2017-01-30 15:21:27
1167	5	/justify/35/t/undercut	2017-01-30 15:22:43
1168	5	/reaction/63/end/0	2017-01-30 15:25:37
1169	5	/review	2017-01-30 15:25:44
1170	5	/review/optimizations	2017-01-30 15:25:47
1171	4	/	2017-01-30 15:25:54
1172	4	/discuss	2017-01-30 15:25:56
1173	4	/attitude/1	2017-01-30 15:25:57
1174	4	/justify/1/t	2017-01-30 15:26:02
1175	4	/reaction/1/undercut/25	2017-01-30 15:26:04
1176	4	/justify/25/t/undermine	2017-01-30 15:26:08
1177	5	/settings	2017-01-30 15:26:09
1178	5	/user/bjebb100	2017-01-30 15:26:19
1179	5	/user/bjebb100	2017-01-30 15:26:43
1180	5	/user/bjebb100	2017-01-30 15:27:04
1181	5	/settings	2017-01-30 15:28:12
1182	5	/discuss	2017-01-30 15:28:49
1183	3	/discuss	2017-01-30 15:37:40
1184	4	/	2017-01-30 15:38:51
1185	4	/discuss	2017-01-30 15:38:58
1186	3	/discuss	2017-01-30 15:39:19
1187	3	/discuss	2017-01-30 15:39:20
1188	4	/user/bjebb100	2017-01-30 15:43:07
1189	5	/review	2017-01-30 15:44:42
1190	5	/review/edits	2017-01-30 15:44:44
1191	3	/notifications	2017-01-30 16:04:47
1192	3	/notifications	2017-01-30 16:10:50
1193	3	/notifications	2017-01-30 16:11:54
1194	3	/review	2017-01-30 16:15:37
1195	3	/review/edits	2017-01-30 16:15:42
1196	5	/review	2017-01-30 16:43:09
1197	5	/review/edits	2017-01-30 16:43:13
1198	5	/review/edits	2017-01-30 16:43:47
1199	5	/review/edits	2017-01-30 16:43:57
1200	5	/review/edits	2017-01-30 16:43:59
1201	5	/review/edits	2017-01-30 16:44:06
1202	5	/review	2017-01-30 16:44:09
1203	5	/review/optimizations	2017-01-30 16:44:18
1204	5	/discuss	2017-01-30 16:44:25
1205	5	/notifications	2017-01-30 16:44:54
1206	5	/justify/37/t	2017-01-30 16:44:58
1207	5	/reaction/62/rebut/35	2017-01-30 16:45:05
1208	5	/review	2017-01-30 16:46:41
1209	5	/review/optimizations	2017-01-30 16:46:43
1210	5	/discuss	2017-01-30 16:46:56
1211	5	/jump/35	2017-01-30 16:48:28
1212	5	/	2017-01-30 16:49:01
1213	5	/news	2017-01-30 16:49:16
1214	5	/	2017-01-30 16:49:26
1215	5	/settings	2017-01-30 16:59:32
1216	5	/user/bjebb100	2017-01-30 16:59:46
1217	5	/review	2017-01-30 17:01:01
1218	3	/justify/37/t	2017-01-30 19:54:15
1219	3	/justify/37/t	2017-01-30 19:55:26
1220	5	/jump/18	2017-01-30 19:57:56
1221	5	/discuss	2017-01-30 19:57:59
1222	3	/jump/1	2017-01-30 19:59:30
1223	3	/justify/1/f	2017-01-30 19:59:36
1224	3	/reaction/2/rebut/23	2017-01-30 19:59:42
1225	5	/discuss	2017-01-30 20:01:06
1226	5	/jump/35	2017-01-30 20:01:37
1227	5	/justify/37/t	2017-01-30 20:02:03
1228	5	/justify/37/t	2017-01-30 20:02:51
1229	5	/justify/37/t	2017-01-30 20:03:03
1230	5	/jump/62	2017-01-30 20:03:29
1231	5	/settings	2017-01-30 20:04:47
1232	5	/review/reputation	2017-01-30 20:05:28
1233	5	/review	2017-01-30 20:05:33
1234	5	/settings	2017-01-30 20:08:23
1235	5	/user/bjebb100	2017-01-30 20:10:35
1236	5	/review	2017-01-30 20:10:47
1237	5	/review/optimizations	2017-01-30 20:10:49
1238	5	/user/phhag101	2017-01-30 20:10:52
1239	5	/rss	2017-01-30 20:12:57
1240	5	/discuss	2017-01-30 20:15:11
1241	3	/justify/37/t	2017-01-30 20:43:01
1242	3	/justify/37/t	2017-01-30 20:43:03
1243	3	/review/edits	2017-01-30 21:55:31
1244	7	/	2017-01-31 07:16:36
1245	6	/	2017-01-31 11:02:53
1246	6	/	2017-01-31 11:02:53
1247	6	/review	2017-01-31 11:02:57
1248	6	/review/optimizations	2017-01-31 11:03:01
1249	6	/review/optimizations	2017-01-31 11:03:21
1250	13	/	2017-01-31 11:05:14
1251	13	/	2017-01-31 11:05:14
1252	13	/settings	2017-01-31 11:05:18
1253	13	/settings	2017-01-31 11:05:41
1254	13	/review	2017-01-31 11:07:25
1255	13	/review/optimizations	2017-01-31 11:07:29
1256	3	/discuss	2017-01-31 11:08:00
1257	3	/discuss	2017-01-31 11:08:00
1258	13	/review	2017-01-31 11:08:45
1259	13	/review/edits	2017-01-31 11:08:48
1260	13	/review/edits	2017-01-31 11:09:24
1261	13	/review/edits	2017-01-31 11:09:33
1262	13	/review/edits	2017-01-31 11:09:37
1263	13	/review/edits	2017-01-31 11:10:12
1264	13	/review	2017-01-31 11:10:14
1265	13	/discuss	2017-01-31 11:10:30
1266	13	/review	2017-01-31 11:11:03
1267	13	/discuss	2017-01-31 11:11:06
1268	13	/jump/49	2017-01-31 11:11:34
1269	13	/reaction/49/end/0	2017-01-31 11:11:55
1270	13	/jump/49	2017-01-31 11:14:49
1271	13	/discuss	2017-01-31 11:14:59
1272	13		2017-01-31 11:15:01
1273	13	/attitude/1	2017-01-31 11:15:05
1274	13	/justify/1/t	2017-01-31 11:15:13
1276	13	/attitude/34	2017-01-31 11:17:29
1275	13	verbesserung-des-informatik-studiengangs	2017-01-31 11:17:18
1280	13	/reaction/65/end/0	2017-01-31 11:24:06
1299	16	/notifications	2017-01-31 12:06:35
1300	16	/reaction/59/undermine/65	2017-01-31 12:06:38
1303	5	/settings	2017-01-31 12:38:21
1311	5	/attitude/1	2017-01-31 12:58:55
1315	5	/justify/1/t	2017-01-31 12:59:17
1317	5	/reaction/1/undercut/24	2017-01-31 13:02:28
1321	3	/discuss	2017-01-31 15:48:00
1277	13	/justify/34/t	2017-01-31 11:17:31
1289	13	/justify/46/t/undercut	2017-01-31 11:25:59
1301	5	/justify/37/t	2017-01-31 12:36:53
1309	5	/attitude/1	2017-01-31 12:44:00
1313	5	/justify/1/f	2017-01-31 12:59:03
1278	13	/reaction/64/rebut/59	2017-01-31 11:20:22
1283	13	/settings	2017-01-31 11:24:49
1288	13	/reaction/41/undercut/46	2017-01-31 11:25:30
1293	13	/justify/77/t	2017-01-31 11:29:42
1305	5	/attitude/1	2017-01-31 12:40:40
1314	5	/reaction/2/rebut/1	2017-01-31 12:59:06
1279	13	/justify/59/t/undermine	2017-01-31 11:22:41
1282	13	/review/optimizations	2017-01-31 11:24:18
1284	13	/review	2017-01-31 11:25:02
1286	13	/attitude/48	2017-01-31 11:25:17
1290	13	verbesserung-des-informatik-studiengangs	2017-01-31 11:26:58
1295	13	verbesserung-des-informatik-studiengangs	2017-01-31 11:33:10
1297	13	/discuss	2017-01-31 11:52:23
1307	5	/discuss	2017-01-31 12:42:24
1316	5	/reaction/1/undercut/24	2017-01-31 13:01:12
1319	3	/imprint	2017-01-31 13:41:11
1281	13	/review	2017-01-31 11:24:16
1287	13	/justify/48/d	2017-01-31 11:25:20
1292	13	/attitude/77	2017-01-31 11:29:34
1296	13	/review	2017-01-31 11:33:53
1298	3	/discuss	2017-01-31 12:05:40
1302	5	/settings	2017-01-31 12:37:16
1304	5	/discuss	2017-01-31 12:39:12
1306	5	/justify/1/t	2017-01-31 12:40:53
1312	5	/justify/1/f	2017-01-31 12:58:57
1318	5	/rss	2017-01-31 13:02:53
1320	3	/discuss	2017-01-31 15:36:45
1285	13	/discuss	2017-01-31 11:25:13
1291	16	/reaction/59/undermine/65	2017-01-31 11:27:19
1294	13	/choose/f/t/77/62/63	2017-01-31 11:32:56
1308	5	/attitude/1	2017-01-31 12:42:34
1310	5	/discuss	2017-01-31 12:58:49
1322	3	/	2017-01-31 16:07:18
1323	3	/discuss	2017-01-31 16:07:22
1324	3	/discuss	2017-01-31 15:09:23.083141
1325	15	/	2017-01-31 15:09:38.454987
1326	15	/	2017-01-31 15:09:41.61082
1327	6	/	2017-01-31 15:12:46.347058
1328	6	/	2017-01-31 15:12:46.457127
1329	6	/review	2017-01-31 15:12:53.845215
1332	15	/	2017-01-31 15:13:25.033277
1333	3	/	2017-01-31 15:13:35.422755
1334	3	/	2017-01-31 15:13:35.553375
1335	3	/review	2017-01-31 15:13:37.546347
1339	3	/review/edits	2017-01-31 15:27:18.538159
1340	3	/review/edits	2017-01-31 15:27:25.956678
1341	3	/review/optimizations	2017-01-31 15:27:27.27378
1342	3	/review/deletes	2017-01-31 15:27:32.458934
1343	3	/review/deletes	2017-01-31 15:27:37.223395
1344	3	/review/optimizations	2017-01-31 15:27:39.321055
1345	3	/review/edits	2017-01-31 15:27:40.287627
1346	3	/	2017-02-01 06:54:46.319
1347	3	/discuss	2017-02-01 06:54:48.506274
1348	3	/discuss	2017-02-01 06:58:29.334586
1349	3	/discuss	2017-02-01 06:58:40.293521
1350	3	/discuss	2017-02-01 07:01:31.656943
1351	3	/attitude/1	2017-02-01 07:01:38.671425
1352	3	/discuss	2017-02-01 07:01:46.406918
1353	3	/discuss	2017-02-01 07:02:16.622115
1354	3	/discuss	2017-02-01 07:10:02.517943
1355	3	/discuss	2017-02-01 07:10:05.674298
1356	3	/discuss	2017-02-01 07:12:18.135009
1358	3	/news	2017-02-01 07:22:54.960907
1359	3	/discuss	2017-02-01 07:23:01.282281
1360	3	/attitude/1	2017-02-01 07:23:04.586818
1361	3	/justify/1/t	2017-02-01 07:23:10.245626
1362	3	/discuss	2017-02-01 07:24:23.011277
1363	3	/discuss	2017-02-01 08:31:24.982037
1364	3	/discuss	2017-02-01 08:32:57.738798
1365	3	/attitude/1	2017-02-01 08:33:00.137796
1366	3	/attitude/1	2017-02-01 08:33:04.694616
1367	3	/justify/1/t	2017-02-01 08:33:06.695439
1368	3	/justify/1/t	2017-02-01 08:33:08.774739
1369	3	/justify/1/t	2017-02-01 08:33:29.684659
1370	3	/justify/1/t	2017-02-01 08:33:31.591525
1371	3	/discuss	2017-02-01 08:33:42.407892
1372	3	/discuss	2017-02-01 08:37:40.503585
1373	3	/discuss	2017-02-01 08:42:41.447117
1374	3	/discuss	2017-02-01 08:42:43.637577
1375	3	/discuss	2017-02-01 08:42:45.463043
1376	3	/discuss	2017-02-01 08:42:45.560657
1377	3	/discuss	2017-02-01 08:42:46.094164
1378	5	/review	2017-02-01 08:43:31.480918
1379	5	/review/deletes	2017-02-01 08:43:43.472056
1380	5	/review/edits	2017-02-01 08:43:49.473792
1381	5	/review/edits	2017-02-01 08:44:02.463405
1382	5	/review	2017-02-01 08:44:10.769466
1383	5	/review/optimizations	2017-02-01 08:44:13.862949
1384	5	/discuss	2017-02-01 08:45:06.447006
1385	5	/jump/22	2017-02-01 08:49:05.12123
1386	5	/justify/27/f	2017-02-01 08:49:29.004231
1387	3	/	2017-02-01 09:30:58.604401
1388	13	/	2017-02-01 10:05:00.023429
1389	13	/	2017-02-01 10:05:00.132557
1390	13	/discuss	2017-02-01 10:05:02.664929
1391	13	/review	2017-02-01 10:05:07.729285
1392	13	/discuss	2017-02-01 10:05:12.349434
1393	13	/attitude/77	2017-02-01 10:05:16.163465
1394	13	/justify/77/d	2017-02-01 10:05:19.871254
1395	13	/reaction/66/end/0	2017-02-01 10:05:40.747706
1396	13	/news	2017-02-01 10:05:44.182443
1397	5	/review/optimizations	2017-02-01 11:26:08.506528
1398	4	/discuss	2017-02-01 12:42:03.376509
1399	4	/discuss	2017-02-01 12:42:03.579792
1400	4	/review	2017-02-01 12:42:08.329017
1401	4	/review/deletes	2017-02-01 12:42:22.178798
1402	4	/review/deletes	2017-02-01 12:42:34.855889
1403	4	/review	2017-02-01 12:42:37.366607
1404	4	/review/optimizations	2017-02-01 12:42:39.454782
1405	4	/discuss	2017-02-01 12:43:06.968183
1406	4	/notifications	2017-02-01 12:43:09.992888
1407	4	/notifications	2017-02-01 12:44:18.028364
1408	4	/notifications	2017-02-01 12:44:34.912455
1409	5	/discuss	2017-02-01 13:42:23.506436
1410	5	/review/optimizations	2017-02-01 13:42:24.489106
1411	18	/discuss	2017-02-01 14:11:17.15561
1412	18	/discuss	2017-02-01 14:11:17.332578
1413	18	/notifications	2017-02-01 14:11:22.001028
1414	18	/discuss	2017-02-01 14:11:33.521388
1415	18	/attitude/1	2017-02-01 14:12:07.412933
1416	18	/justify/1/f	2017-02-01 14:12:11.783266
1417	18	/reaction/5/undercut/13	2017-02-01 14:12:35.846295
1418	18	/reaction/5/rebut/23	2017-02-01 14:16:51.314717
1419	18	/justify/23/f/undercut	2017-02-01 14:17:30.738841
1420	18	/reaction/68/end/0	2017-02-01 14:19:46.440278
1421	18	/review	2017-02-01 14:19:54.961065
1422	18	/review/deletes	2017-02-01 14:20:00.016901
1423	18	/review/deletes	2017-02-01 14:21:03.534676
1424	18	/review/deletes	2017-02-01 14:21:06.804267
1425	18	/discuss	2017-02-01 14:21:12.060657
1426	18	/attitude/1	2017-02-01 14:21:16.135153
1427	18	/justify/1/f	2017-02-01 14:21:19.522387
1428	18	/justify/1/t	2017-02-01 14:21:22.157185
1429	18	/reaction/1/rebut/28	2017-02-01 14:21:28.360927
1430	18	/reaction/1/undercut/25	2017-02-01 14:21:34.342343
1431	18	/reaction/1/undermine/18	2017-02-01 14:21:36.513563
1432	18	/reaction/1/undercut/24	2017-02-01 14:21:38.907086
1433	18	/reaction/1/undermine/18	2017-02-01 14:21:41.697227
1434	18	/reaction/1/undercut/24	2017-02-01 14:21:43.301451
1435	18	/reaction/1/rebut/17	2017-02-01 14:21:45.141486
1436	18	/review	2017-02-01 14:21:50.503202
1437	18	/review/deletes	2017-02-01 14:21:52.811704
1438	18	/discuss	2017-02-01 14:26:05.199078
1439	18	/attitude/1	2017-02-01 14:26:06.733977
1440	18	/justify/1/f	2017-02-01 14:26:09.448564
1441	18	/reaction/5/undercut/14	2017-02-01 14:26:33.093038
1442	18	/reaction/5/rebut/23	2017-02-01 14:26:35.120695
1443	18	/reaction/5/undercut/14	2017-02-01 14:26:37.419451
1444	18	/reaction/5/rebut/1	2017-02-01 14:26:40.195044
1445	18	/reaction/5/undercut/13	2017-02-01 14:26:52.789946
1446	18	/reaction/5/rebut/1	2017-02-01 14:27:03.332335
1447	3	/	2017-02-01 14:39:16.251194
1448	3	/review	2017-02-01 14:39:22.474705
1449	3	/review/deletes	2017-02-01 14:39:25.370025
1450	9	/	2017-02-01 15:40:38.857468
1451	9	/	2017-02-01 15:40:38.952882
1453	9	/review	2017-02-01 15:41:02.273642
1452	9	/discuss	2017-02-01 15:40:42.448537
1463	3	/jump/6	2017-02-01 21:05:16.693624
1465	19	/	2017-02-02 09:14:47.227984
1470	19	/justify/37/t	2017-02-02 09:15:49.769146
1487	19	verbesserung-des-informatik-studiengangs	2017-02-02 09:19:08.785968
1454	9	/discuss	2017-02-01 15:41:27.729163
1466	19	/notifications	2017-02-02 09:14:52.236987
1468	19	/imprint	2017-02-02 09:15:06.31926
1472	19	/reaction/36/rebut/35	2017-02-02 09:16:28.283392
1475	19	verbesserung-des-informatik-studiengangs	2017-02-02 09:17:28.772075
1483	19	/attitude/19	2017-02-02 09:18:45.062044
1485	19	/reaction/58/end/0	2017-02-02 09:18:51.860121
1455	9	/notifications	2017-02-01 15:42:23.535031
1460	15	/jump/22	2017-02-01 20:00:16.151504
1476	19	/attitude/19	2017-02-02 09:17:42.523966
1480	19	/attitude/34	2017-02-02 09:18:22.017568
1484	19	/justify/19/t	2017-02-02 09:18:47.503259
1456	15	/	2017-02-01 19:58:52.714468
1459	15	/discuss	2017-02-01 19:59:34.016548
1461	15	/justify/22/t/undercut	2017-02-01 20:01:05.906349
1478	19	/review	2017-02-02 09:18:03.35085
1479	19	/discuss	2017-02-02 09:18:18.246039
1457	15	/	2017-02-01 19:58:53.037319
1458	15	/discuss	2017-02-01 19:59:05.059402
1462	15	/discuss	2017-02-01 20:01:10.833516
1467	19	/discuss	2017-02-02 09:14:57.880904
1471	19	/reaction/62/rebut/35	2017-02-02 09:16:04.692508
1474	19	/attitude/1	2017-02-02 09:16:39.827611
1477	19	/justify/19/t	2017-02-02 09:17:45.219205
1481	19	/justify/34/t	2017-02-02 09:18:35.811517
1482	19	verbesserung-des-informatik-studiengangs	2017-02-02 09:18:41.749836
1464	19	/	2017-02-02 09:14:46.950373
1469	19	/attitude/37	2017-02-02 09:15:46.413402
1473	19	verbesserung-des-informatik-studiengangs	2017-02-02 09:16:37.401007
1486	19	/justify/19/t	2017-02-02 09:19:02.414531
1488	3	/	2017-02-02 10:09:14.738943
1489	8	/discuss	2017-02-02 10:49:48.607623
1490	8	/discuss	2017-02-02 10:49:48.978669
1491	8	/attitude/19	2017-02-02 10:50:11.125343
1492	8	/justify/19/t	2017-02-02 10:50:15.615886
1493	8	/reaction/58/end/0	2017-02-02 10:50:29.480293
1494	8	/settings	2017-02-02 10:50:56.149352
1495	8	/discuss	2017-02-02 10:51:18.419421
1496	8	/attitude/6	2017-02-02 10:51:44.257499
1497	8	/justify/6/t	2017-02-02 10:51:46.325457
1498	8	/reaction/4/undercut/11	2017-02-02 10:52:01.79144
1499	8	verbesserung-des-informatik-studiengangs	2017-02-02 10:52:34.835367
1500	8	/notifications	2017-02-02 10:52:39.715281
1501	8	/discuss	2017-02-02 10:52:50.925956
1502	8	/news	2017-02-02 10:53:19.909794
1503	8	/discuss	2017-02-02 10:53:43.560265
1504	8	/review	2017-02-02 10:53:45.873628
1505	8	/review	2017-02-02 10:53:46.202336
1506	8	/discuss	2017-02-02 10:54:45.845494
1507	8	/attitude/6	2017-02-02 10:54:55.900225
1508	8	/	2017-02-02 11:50:49.670079
1509	8	/discuss	2017-02-02 11:50:53.047164
1510	8	/attitude/1	2017-02-02 11:51:02.565432
1511	8	/justify/1/d	2017-02-02 11:51:08.369321
1512	8	/attitude/4	2017-02-02 11:52:32.000842
1513	8	/justify/4/d	2017-02-02 11:52:34.785302
1514	8	/user/7	2017-02-02 11:52:46.455467
1515	8	/attitude/34	2017-02-02 11:53:05.16098
1516	8	/justify/34/d	2017-02-02 11:53:08.638514
1517	8	/attitude/48	2017-02-02 11:53:33.607741
1518	8	/justify/48/d	2017-02-02 11:53:36.34395
1519	8	/attitude/37	2017-02-02 11:53:56.656935
1520	8	/justify/37/d	2017-02-02 11:53:59.704414
1521	3	/	2017-02-02 12:37:31.731998
1522	3	/	2017-02-02 13:49:24.230594
1523	3	/	2017-02-02 14:00:47.671258
1524	3	/review	2017-02-02 14:00:49.815257
1525	3	/	2017-02-02 14:27:06.672715
1526	3	/	2017-02-02 14:27:06.812794
1527	3	/user/6	2017-02-02 14:27:40.159899
1528	3	/user/5	2017-02-02 14:27:41.039117
1529	3	/user/7	2017-02-02 14:27:41.690018
1530	3	/discuss	2017-02-02 14:36:31.941065
1531	3	/attitude/4	2017-02-02 14:36:34.861735
1532	3	/justify/4/t?history=/attitude/4	2017-02-02 14:36:36.36733
1533	3	/reaction/3/rebut/7?history=/attitude/4-/justify/4/t	2017-02-02 14:36:42.269149
1534	3	/justify/7/t/undercut?history=/attitude/4-/justify/4/t-/reaction/3/rebut/7	2017-02-02 14:37:00.308529
1535	9	/	2017-02-02 15:32:03.371561
1536	9	/	2017-02-02 15:32:03.803089
1537	9	/discuss	2017-02-02 15:32:08.805072
1538	9	/attitude/1	2017-02-02 15:32:12.690765
1539	9	/justify/1/t?history=/attitude/1	2017-02-02 15:32:16.12164
1540	9	/reaction/1/undercut/24?history=/attitude/1-/justify/1/t	2017-02-02 15:32:23.281566
1541	9	/justify/1/t?history=/attitude/1-/justify/1/t-/reaction/1/undercut/24	2017-02-02 15:33:37.264135
1542	9	/reaction/23/rebut/16?history=/attitude/1-/justify/1/t-/reaction/1/undercut/24-/justify/1/t	2017-02-02 15:33:46.028194
1543	9	/review	2017-02-02 15:34:05.345226
1544	9	/discuss	2017-02-02 15:34:14.355956
1545	9	/attitude/37	2017-02-02 15:34:22.269912
1546	9	/justify/37/f?history=/attitude/37	2017-02-02 15:34:26.178903
1547	9	/reaction/35/undercut/63?history=/attitude/37-/justify/37/f	2017-02-02 15:34:43.746866
1548	9	/justify/63/f/undermine?history=/attitude/37-/justify/37/f-/reaction/35/undercut/63	2017-02-02 15:35:11.562974
1549	9	/reaction/69/end/0?history=/attitude/37-/justify/37/f-/reaction/35/undercut/63-/justify/63/f/undermine	2017-02-02 15:37:43.422872
1550	9	/review	2017-02-02 15:37:56.955466
1551	9	/review/deletes	2017-02-02 15:38:04.797509
1552	9	/review/deletes	2017-02-02 15:38:32.619693
1553	9	/review	2017-02-02 15:38:36.573137
1554	9	/review/optimizations	2017-02-02 15:38:41.46914
1555	9	/review/optimizations	2017-02-02 15:42:49.587657
1556	9	/review	2017-02-02 15:42:49.854299
1557	9	/review	2017-02-02 15:42:55.386938
1558	9	/review/edits	2017-02-02 15:42:59.808962
1559	9	/review/edits	2017-02-02 15:46:37.20099
1560	9	/review/edits	2017-02-02 15:46:43.769979
1561	9	/review/edits	2017-02-02 15:47:03.447292
1562	9	/review/edits	2017-02-02 15:47:27.12234
1563	9	/review/edits	2017-02-02 15:47:44.591063
1564	9	/review/edits	2017-02-02 15:47:56.303525
1565	9	/review/edits	2017-02-02 15:48:04.497255
1566	9	/review	2017-02-02 15:48:13.014131
1567	9	/review/edits	2017-02-02 15:48:19.191717
1568	9	/review/edits	2017-02-02 15:48:25.82896
1569	3	/	2017-02-02 15:48:31.321116
1570	9	/review	2017-02-02 15:48:41.936201
1571	13	/justify/1/t?history=/attitude/1	2017-02-02 16:06:11.18347
1572	13	/justify/1/t?history=/attitude/1	2017-02-02 16:06:11.442869
1573	13	/justify/1/t?history=/attitude/1	2017-02-02 16:06:14.473295
1574	13	/review	2017-02-02 16:07:13.226594
1575	13	/review/optimizations	2017-02-02 16:07:19.904142
1576	13	/user/16	2017-02-02 16:08:39.653698
1577	13	/discuss	2017-02-02 16:09:08.865802
1578	13	/attitude/77	2017-02-02 16:09:16.490117
1579	13	/justify/77/d?history=/attitude/77	2017-02-02 16:09:22.374606
1580	13	/discuss	2017-02-02 16:10:41.807604
1581	13	/attitude/19	2017-02-02 16:11:39.070913
1582	13	/justify/19/t?history=/attitude/19	2017-02-02 16:11:42.64753
1583	3	/discuss	2017-02-02 18:08:22.905255
1584	3	/user/9	2017-02-02 18:19:16.933084
1585	3	/discuss	2017-02-02 19:59:06.300938
1586	3	/attitude/1	2017-02-02 19:59:21.675095
1587	3	/justify/1/t?history=/attitude/1	2017-02-02 19:59:24.575282
1588	3	/justify/1/f?history=/attitude/1	2017-02-02 19:59:29.701584
1589	3	/discuss	2017-02-02 19:59:49.404354
1590	3	/discuss	2017-02-02 19:59:53.995257
1591	20	/justify/46/t/undercut?history=/attitude/48-/justify/48/t-/reaction/41/undercut/46	2017-02-02 21:46:59.881005
1592	20	/justify/46/t/undercut?history=/attitude/48-/justify/48/t-/reaction/41/undercut/46	2017-02-02 21:47:00.404138
1593	20	/review	2017-02-02 22:09:31.037624
1594	20	/discuss	2017-02-02 22:10:07.894894
1595	20	/attitude/48	2017-02-02 22:10:19.064576
1596	20	/justify/48/f?history=/attitude/48	2017-02-02 22:10:23.985085
1597	20	/reaction/45/undermine/50?history=/attitude/48-/justify/48/f	2017-02-02 22:10:27.552487
1598	20	/justify/50/f/undercut?history=/attitude/48-/justify/48/f-/reaction/45/undermine/50	2017-02-02 22:10:29.912388
1599	20	verbesserung-des-informatik-studiengangs	2017-02-02 22:10:59.52396
1600	3	/	2017-02-03 06:10:56.825251
1601	3	/	2017-02-03 06:30:49.413277
1602	3	/discuss	2017-02-03 06:30:51.517238
1603	3	/attitude/1	2017-02-03 06:30:53.174341
1615	3	/	2017-02-03 09:36:49.05599
1604	3	/justify/1/d?history=/attitude/1	2017-02-03 06:30:54.650841
1608	3	/justify/1/d?history=/attitude/1	2017-02-03 06:31:01.797306
1612	3	/justify/1/d?history=/attitude/1	2017-02-03 06:31:14.899805
1605	3	/attitude/1	2017-02-03 06:30:57.278308
1609	3	/attitude/1	2017-02-03 06:31:05.548088
1613	3	/attitude/1	2017-02-03 06:31:18.829447
1616	3	/discuss	2017-02-03 09:36:53.024219
1606	3	/justify/1/d?history=/attitude/1	2017-02-03 06:30:58.449264
1610	3	/justify/1/d?history=/attitude/1	2017-02-03 06:31:06.731535
1614	3	/justify/1/d?history=/attitude/1	2017-02-03 06:31:20.038723
1607	3	/attitude/1	2017-02-03 06:31:00.579116
1611	3	/attitude/1	2017-02-03 06:31:13.703614
1617	3	/rss	2017-02-03 09:47:34.092813
1618	21	/discuss	2017-02-03 12:50:12.65089
1619	21	/discuss	2017-02-03 12:50:13.882572
1620	21	/attitude/19	2017-02-03 12:50:51.192149
1621	21	/justify/19/t?history=/attitude/19	2017-02-03 12:50:54.715606
1622	21	/reaction/70/end/0?history=/attitude/19-/justify/19/t	2017-02-03 12:51:38.514926
1623	21	verbesserung-des-informatik-studiengangs	2017-02-03 12:51:41.929143
1624	21	/attitude/19	2017-02-03 12:51:51.153517
1625	21	/justify/19/t?history=/attitude/19	2017-02-03 12:51:52.61988
1626	3	/	2017-02-03 12:53:43.997674
1627	21	verbesserung-des-informatik-studiengangs	2017-02-03 12:54:07.107686
1628	21	/attitude/48	2017-02-03 12:54:10.833333
1629	21	/justify/48/f?history=/attitude/48	2017-02-03 12:54:12.321219
1630	21	/reaction/71/rebut/44?history=/attitude/48-/justify/48/f	2017-02-03 12:54:40.968201
1631	21	/justify/48/f?history=/attitude/48-/justify/48/f-/reaction/71/rebut/44	2017-02-03 12:55:39.677005
1632	21	verbesserung-des-informatik-studiengangs	2017-02-03 12:58:01.46665
1633	21	/attitude/34	2017-02-03 12:58:04.395287
1634	21	/justify/34/f?history=/attitude/34	2017-02-03 12:58:07.240784
1635	21	/reaction/59/undermine/65?history=/attitude/34-/justify/34/f	2017-02-03 12:58:10.987633
1636	21	/reaction/59/rebut/29?history=/attitude/34-/justify/34/f-/reaction/59/undermine/65	2017-02-03 12:58:41.272813
1637	21	/justify/34/f?history=/attitude/34	2017-02-03 12:59:11.17306
1638	21	/reaction/72/rebut/64?history=/attitude/34-/justify/34/f	2017-02-03 12:59:56.752999
1639	21	/justify/64/f/undermine?history=/attitude/34-/justify/34/f-/reaction/72/rebut/64	2017-02-03 13:02:03.560164
1640	21	/reaction/72/rebut/29?history=/attitude/34-/justify/34/f-/reaction/72/rebut/64	2017-02-03 13:04:33.886103
1641	21	/justify/34/f?history=/attitude/34	2017-02-03 13:04:39.801291
1642	21	verbesserung-des-informatik-studiengangs	2017-02-03 13:04:44.916506
1643	21	/attitude/77	2017-02-03 13:04:53.110781
1644	21	/justify/77/f?history=/attitude/77	2017-02-03 13:04:59.168015
1645	21	/reaction/73/rebut/66?history=/attitude/77-/justify/77/f	2017-02-03 13:10:35.124941
1646	21	/justify/66/f/undermine?history=/attitude/77-/justify/77/f-/reaction/73/rebut/66	2017-02-03 13:11:00.641516
1647	21	verbesserung-des-informatik-studiengangs	2017-02-03 13:11:07.99254
1648	3	/justify/19/t?history=/attitude/19-/justify/19/t-/reaction/15/end/0	2017-02-06 08:30:10.213252
1649	3	/justify/77/f?history=/attitude/77-/justify/77/f	2017-02-06 08:30:49.217091
1650	4	/	2017-02-06 12:15:11.018101
1651	4	/	2017-02-06 12:15:11.155463
1652	4	/notifications	2017-02-06 12:15:13.913961
1653	4	/reaction/45/undermine/49?history=/attitude/48-/justify/42/d-/reaction/42/rebut/45-/justify/45/t/undermine	2017-02-06 12:15:27.317906
1654	4	/reaction/45/undermine/49?history=/attitude/48-/justify/42/d-/reaction/42/rebut/45-/justify/45/t/undermine	2017-02-06 12:16:24.159323
\.


--
-- Name: history_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('history_uid_seq', 1654, true);


--
-- Data for Name: issues; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY issues (uid, title, info, long_info, date, author_uid, lang_uid, is_disabled) FROM stdin;
1	Verbesserung des Informatik-Studiengangs	Wie können der Informatik-Studiengang verbessert und die Probleme, die durch die große Anzahl der Studierenden entstanden sind, gelöst werden?	Die Anzahl der Studierenden in der Informatik hat sich in den letzten Jahren stark erhöht. Dadurch treten zahlreiche Probleme auf, wie z.B. Raumknappheit, überfüllte Lehrveranstaltungen und ein Mangel an Plätzen zum Lernen. Wir möchten Sie gerne dazu einladen, gemeinsam mit den Dozierenden der Informatik über Lösungsmöglichkeiten zu diskutieren: Wie können der Studiengang verbessert und die Probleme, die durch die große Anzahl der Studierenden entstanden sind, gelöst werden?	2017-01-26 17:08:49	2	2	f
2	Town has to cut spending 	Our town needs to cut spending. Please discuss ideas how this should be done.		2017-02-15 10:05:04.066858	2	1	f
3	Cat or Dog	Your family argues about whether to buy a cat or dog as pet. Now your opinion matters!		2017-02-15 10:05:04.066858	2	1	f
4	Elektroautos	Elektroautos - Die Autos der Zukunft? Bitte diskutieren Sie dazu.		2017-02-15 10:05:04.066858	2	2	f
\.


--
-- Name: issues_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('issues_uid_seq', 4, true);


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
1	4	1	f	2017-02-01 12:42:34.732419
2	9	1	t	2017-02-02 15:38:32.313916
\.


--
-- Name: last_reviewers_delete_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('last_reviewers_delete_uid_seq', 2, true);


--
-- Data for Name: last_reviewers_duplicates; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY last_reviewers_duplicates (uid, reviewer_uid, review_uid, is_okay, "timestamp") FROM stdin;
\.


--
-- Name: last_reviewers_duplicates_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('last_reviewers_duplicates_uid_seq', 1, false);


--
-- Data for Name: last_reviewers_edit; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY last_reviewers_edit (uid, reviewer_uid, review_uid, is_okay, "timestamp") FROM stdin;
1	6	1	t	2017-01-27 10:53:02
2	12	1	f	2017-01-27 10:56:12
3	4	1	t	2017-01-27 10:58:24
4	5	1	t	2017-01-27 11:43:45
5	5	2	t	2017-01-27 11:44:51
6	13	3	t	2017-01-27 11:54:05
7	14	1	t	2017-01-27 12:01:34
8	14	3	t	2017-01-27 12:01:43
9	14	2	t	2017-01-27 12:01:48
10	12	3	t	2017-01-27 12:17:44
11	4	2	t	2017-01-27 12:17:53
12	6	7	f	2017-01-30 14:55:17
13	6	6	f	2017-01-30 14:55:24
14	6	5	f	2017-01-30 14:55:32
15	6	4	f	2017-01-30 14:56:19
16	5	4	f	2017-01-30 16:43:47
17	5	7	f	2017-01-30 16:43:57
18	5	6	f	2017-01-30 16:43:59
19	5	5	t	2017-01-30 16:44:06
20	13	6	f	2017-01-31 11:09:24
21	13	5	t	2017-01-31 11:09:33
22	13	7	f	2017-01-31 11:09:36
23	13	4	f	2017-01-31 11:10:12
24	5	8	t	2017-02-01 08:44:02.288813
25	9	5	t	2017-02-02 15:47:02.272081
26	9	4	f	2017-02-02 15:47:26.943377
27	9	9	t	2017-02-02 15:47:44.413211
28	9	8	t	2017-02-02 15:47:56.116965
29	9	7	f	2017-02-02 15:48:04.322296
30	9	6	f	2017-02-02 15:48:24.699775
\.


--
-- Name: last_reviewers_edit_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('last_reviewers_edit_uid_seq', 30, true);


--
-- Data for Name: last_reviewers_optimization; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY last_reviewers_optimization (uid, reviewer_uid, review_uid, is_okay, "timestamp") FROM stdin;
1	5	1	f	2017-01-27 11:44:38
\.


--
-- Name: last_reviewers_optimization_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('last_reviewers_optimization_uid_seq', 1, true);


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
3	2	3	Aussage wurde hinzugefügt	Hey, jemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/justify/1/f?history=/attitude/1-/justify/1/f">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/justify/1/f?history=/attitude/1-/justify/1/f</a>	2017-01-26 17:17:01	f	t
4	3	7	Willkommen	Willkommen im neuen dialog-basierten Argumentations-System.<br>Wir wünschen viel Spaß beim Diskutieren!	2017-01-26 17:31:49	t	t
21	2	3	Aussage wurde hinzugefügt	Hey, jemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/justify/1/f?history=/attitude/1-/justify/1/f">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/justify/1/f?history=/attitude/1-/justify/1/f</a>	2017-01-27 10:34:16	f	t
7	3	9	Willkommen	Willkommen im neuen dialog-basierten Argumentations-System.<br>Wir wünschen viel Spaß beim Diskutieren!	2017-01-26 20:02:53	f	t
10	2	9	Argument was added	Hey, jemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/7/undercut/8?history=/attitude/4-/justify/4/t-/reaction/6/rebut/7-/justify/7/t/undercut">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/7/undercut/8?history=/attitude/4-/justify/4/t-/reaction/6/rebut/7-/justify/7/t/undercut</a>	2017-01-27 09:16:26	f	t
11	3	11	Willkommen	Willkommen im neuen dialog-basierten Argumentations-System.<br>Wir wünschen viel Spaß beim Diskutieren!	2017-01-27 09:17:09	f	t
12	2	9	Argument was added	Hey, jemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/7/undercut/9?history=/attitude/4-/justify/4/t-/reaction/6/rebut/7-/justify/7/t/undercut">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/7/undercut/9?history=/attitude/4-/justify/4/t-/reaction/6/rebut/7-/justify/7/t/undercut</a>	2017-01-27 09:19:39	f	t
22	2	3	Argument was added	Hey, jemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/1/undermine/18?history=/attitude/1-/justify/1/f-/choose/f/f/1/16/17-/reaction/16/rebut/1-/justify/1/f/undermine">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/1/undermine/18?history=/attitude/1-/justify/1/f-/choose/f/f/1/16/17-/reaction/16/rebut/1-/justify/1/f/undermine</a>	2017-01-27 10:35:51	f	t
9	3	10	Willkommen	Willkommen im neuen dialog-basierten Argumentations-System.<br>Wir wünschen viel Spaß beim Diskutieren!	2017-01-27 09:10:05	t	t
16	2	4	Argument was added	Hey, jemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/5/undercut/12?history=/attitude/1-/justify/1/t-/reaction/1/rebut/5-/justify/5/t/undercut">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/5/undercut/12?history=/attitude/1-/justify/1/t-/reaction/1/rebut/5-/justify/5/t/undercut</a>	2017-01-27 10:29:22	f	t
17	2	4	Argument was added	Hey, jemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/5/undercut/14?history=/attitude/1-/justify/1/t-/reaction/1/rebut/5-/justify/5/t/undercut">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/5/undercut/14?history=/attitude/1-/justify/1/t-/reaction/1/rebut/5-/justify/5/t/undercut</a>	2017-01-27 10:29:22	f	t
20	3	14	Willkommen	Willkommen im neuen dialog-basierten Argumentations-System.<br>Wir wünschen viel Spaß beim Diskutieren!	2017-01-27 10:30:05	f	t
19	3	13	Willkommen	Willkommen im neuen dialog-basierten Argumentations-System.<br>Wir wünschen viel Spaß beim Diskutieren!	2017-01-27 10:29:37	t	t
18	2	4	Argument was added	Hey, jemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/5/undercut/13?history=/attitude/1-/justify/1/t-/reaction/1/rebut/5-/justify/5/t/undercut">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/5/undercut/13?history=/attitude/1-/justify/1/t-/reaction/1/rebut/5-/justify/5/t/undercut</a>	2017-01-27 10:29:22	t	t
31	2	3	Aussage wurde hinzugefügt	Hey, jemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/justify/1/f?history=/attitude/1-/justify/1/f">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/justify/1/f?history=/attitude/1-/justify/1/f</a>	2017-01-27 10:54:00	f	t
38	4	12	SQL Injection	test OR 1=1`; DROP TABLE news; `	2017-01-27 11:04:42	t	f
37	4	12	SQL Injection	test OR 1=1`; DROP TABLE news; `	2017-01-27 11:04:42	t	t
15	2	5	Argument was added	Hey, jemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/4/undercut/11?history=/attitude/6-/justify/4/d-/justify/6/f-/reaction/10/rebut/4-/justify/4/f/undercut">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/4/undercut/11?history=/attitude/6-/justify/4/d-/justify/6/f-/reaction/10/rebut/4-/justify/4/f/undercut</a>	2017-01-27 10:09:27	t	t
14	2	5	Aussage wurde hinzugefügt	Hey, jemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/justify/6/f?history=/attitude/6-/justify/4/d-/justify/6/f">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/justify/6/f?history=/attitude/6-/justify/4/d-/justify/6/f</a>	2017-01-27 10:04:22	t	t
76	3	19	Willkommen	Willkommen im neuen dialog-basierten Argumentations-System.<br>Wir wünschen viel Spaß beim Diskutieren!	2017-02-02 09:14:40.073624	t	t
6	3	8	Willkommen	Willkommen im neuen dialog-basierten Argumentations-System.<br>Wir wünschen viel Spaß beim Diskutieren!	2017-01-26 18:00:16	t	t
25	2	3	Aussage wurde hinzugefügt	Hey, jemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/justify/1/f?history=/attitude/1-/justify/1/f">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/justify/1/f?history=/attitude/1-/justify/1/f</a>	2017-01-27 10:43:50	f	t
26	2	3	Aussage wurde hinzugefügt	Hey, jemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/justify/1/t?history=/attitude/1-/justify/1/t">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/justify/1/t?history=/attitude/1-/justify/1/t</a>	2017-01-27 10:44:59	f	t
24	2	12	Argument was added	Hey, jemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/10/undermine/21?history=/attitude/6-/justify/6/t-/reaction/4/rebut/10-/justify/10/t/undermine">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/10/undermine/21?history=/attitude/6-/justify/6/t-/reaction/4/rebut/10-/justify/10/t/undermine</a>	2017-01-27 10:40:49	t	t
30	2	4	Argument was added	Hey, jemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/21/undercut/27?history=/attitude/6-/justify/6/t-/reaction/4/rebut/10-/justify/10/t/undermine-/reaction/10/undermine/21-/justify/21/f/undercut">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/21/undercut/27?history=/attitude/6-/justify/6/t-/reaction/4/rebut/10-/justify/10/t/undermine-/reaction/10/undermine/21-/justify/21/f/undercut</a>	2017-01-27 10:53:50	f	t
32	2	14	Argument was added	Hey, jemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/19/undercut/30?history=/attitude/4-/justify/4/t-/reaction/3/rebut/19-/justify/19/t/undercut">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/19/undercut/30?history=/attitude/4-/justify/4/t-/reaction/3/rebut/19-/justify/19/t/undercut</a>	2017-01-27 10:56:21	f	t
35	4	12	SQL Injection	test`; DROP TABLE discussion; `	2017-01-27 11:03:15	t	f
34	4	12	SQL Injection	test`; DROP TABLE discussion; `	2017-01-27 11:03:15	t	t
29	2	3	Argument was added	Hey, jemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/2/undercut/26?history=/attitude/1-/justify/1/t-/reaction/23/rebut/2-/justify/2/t/undercut">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/2/undercut/26?history=/attitude/1-/justify/1/t-/reaction/23/rebut/2-/justify/2/t/undercut</a>	2017-01-27 10:47:52	t	t
27	2	3	Argument was added	Hey, jemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/1/undercut/24?history=/attitude/1-/justify/1/f-/reaction/22/rebut/1-/justify/1/f/undercut">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/1/undercut/24?history=/attitude/1-/justify/1/f-/reaction/22/rebut/1-/justify/1/f/undercut</a>	2017-01-27 10:45:05	t	t
40	2	9	Argument was added	Hey, jemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/7/undercut/34?history=/attitude/4-/justify/4/t-/reaction/6/rebut/7-/justify/4/t-/reaction/32/rebut/7-/justify/7/t/undercut">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/7/undercut/34?history=/attitude/4-/justify/4/t-/reaction/6/rebut/7-/justify/4/t-/reaction/32/rebut/7-/justify/7/t/undercut</a>	2017-01-27 11:11:30	f	t
42	2	14	Argument was added	Hey, jemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/35/undercut/37?history=/attitude/37-/justify/37/f-/justify/37/f-/reaction/36/rebut/35-/justify/35/t/undercut">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/35/undercut/37?history=/attitude/37-/justify/37/f-/justify/37/f-/reaction/36/rebut/35-/justify/35/t/undercut</a>	2017-01-27 11:20:45	f	t
41	2	11	Aussage wurde hinzugefügt	Hey, jemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/justify/37/f?history=/attitude/37-/justify/37/f">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/justify/37/f?history=/attitude/37-/justify/37/f</a>	2017-01-27 11:14:48	t	t
43	2	14	Aussage wurde hinzugefügt	Hey, jemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/justify/38/f?history=/jump/33-/justify/38/f">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/justify/38/f?history=/jump/33-/justify/38/f</a>	2017-01-27 11:25:32	f	t
39	2	13	Argument was added	Hey, jemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/30/undercut/33?history=/attitude/4-/justify/4/t-/reaction/3/rebut/19-/justify/19/t/undercut-/reaction/19/undercut/30-/justify/30/f/undercut">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/30/undercut/33?history=/attitude/4-/justify/4/t-/reaction/3/rebut/19-/justify/19/t/undercut-/reaction/19/undercut/30-/justify/30/f/undercut</a>	2017-01-27 11:08:21	t	t
46	2	11	Argument was added	Hey, jemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/37/undercut/43?history=/attitude/37-/justify/37/f-/justify/37/f-/reaction/36/rebut/35-/justify/35/t/undercut-/reaction/35/undercut/37-/justify/37/f/undercut">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/37/undercut/43?history=/attitude/37-/justify/37/f-/justify/37/f-/reaction/36/rebut/35-/justify/35/t/undercut-/reaction/35/undercut/37-/justify/37/f/undercut</a>	2017-01-27 11:59:41	f	t
44	2	4	Argument was added	Hey, jemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/21/undermine/39?history=/attitude/6-/justify/6/f-/reaction/10/undermine/21-/justify/21/f/undermine">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/21/undermine/39?history=/attitude/6-/justify/6/f-/reaction/10/undermine/21-/justify/21/f/undermine</a>	2017-01-27 11:31:18	t	t
50	2	12	Argument was added	Hey, jemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/10/undercut/47?history=/attitude/6-/justify/6/t-/reaction/4/rebut/10-/justify/10/t/undercut">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/10/undercut/47?history=/attitude/6-/justify/6/t-/reaction/4/rebut/10-/justify/10/t/undercut</a>	2017-01-27 12:49:53	t	t
45	2	5	Aussage wurde hinzugefügt	Hey, jemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/justify/6/f?history=/attitude/6-/justify/6/f">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/justify/6/f?history=/attitude/6-/justify/6/f</a>	2017-01-27 11:32:52	t	t
51	2	12	Argument was added	Hey, jemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/46/undercut/48?history=/attitude/48-/justify/41/d-/justify/41/t/undercut-/reaction/41/undercut/46-/justify/46/t/undercut">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/46/undercut/48?history=/attitude/48-/justify/41/d-/justify/41/t/undercut-/reaction/41/undercut/46-/justify/46/t/undercut</a>	2017-01-27 12:57:04	f	t
48	2	13	Aussage wurde hinzugefügt	Hey, jemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/justify/48/f?history=/attitude/48-/justify/48/f">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/justify/48/f?history=/attitude/48-/justify/48/f</a>	2017-01-27 12:29:59	t	t
47	2	13	Aussage wurde hinzugefügt	Hey, jemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/justify/48/t?history=/attitude/48-/justify/48/t">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/justify/48/t?history=/attitude/48-/justify/48/t</a>	2017-01-27 12:23:38	t	t
28	2	3	Argument was added	Hey, jemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/1/undercut/25?history=/attitude/1-/justify/1/d-/justify/1/t/undercut">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/1/undercut/25?history=/attitude/1-/justify/1/d-/justify/1/t/undercut</a>	2017-01-27 10:45:54	t	t
52	2	4	Argument was added	Hey, jemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/45/undermine/49?history=/attitude/48-/justify/42/d-/reaction/42/rebut/45-/justify/45/t/undermine">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/45/undermine/49?history=/attitude/48-/justify/42/d-/reaction/42/rebut/45-/justify/45/t/undermine</a>	2017-01-27 13:01:18	t	t
49	2	13	Argument was added	Hey, jemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/41/undercut/46?history=/attitude/48-/justify/41/d-/justify/41/t/undercut">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/41/undercut/46?history=/attitude/48-/justify/41/d-/justify/41/t/undercut</a>	2017-01-27 12:38:27	t	t
54	3	15	Willkommen	Willkommen im neuen dialog-basierten Argumentations-System.<br>Wir wünschen viel Spaß beim Diskutieren!	2017-01-28 08:35:12	f	t
55	3	16	Welcome	Welcome to the novel dialog-based argumentation system.<br>We hope you enjoy using this system and happy arguing!	2017-01-30 00:49:18	t	t
56	2	12	Argument wurde hinzugefügt	Hey Alexander,\n\njemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/12/undermine/51?history=/attitude/1-/justify/1/f-/reaction/5/undercut/12-/justify/12/f/undermine">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/12/undermine/51?history=/attitude/1-/justify/1/f-/reaction/5/undercut/12-/justify/12/f/undermine</a>	2017-01-30 01:26:08	f	t
57	2	12	Argument wurde hinzugefügt	Hey Alexander,\n\njemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/12/undermine/53?history=/attitude/1-/justify/1/f-/reaction/5/undercut/12-/justify/12/f/undermine">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/12/undermine/53?history=/attitude/1-/justify/1/f-/reaction/5/undercut/12-/justify/12/f/undermine</a>	2017-01-30 01:26:09	f	t
58	2	12	Argument wurde hinzugefügt	Hey Alexander,\n\njemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/12/undermine/56?history=/attitude/1-/justify/1/f-/reaction/5/undercut/12-/justify/12/f/undermine">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/12/undermine/56?history=/attitude/1-/justify/1/f-/reaction/5/undercut/12-/justify/12/f/undermine</a>	2017-01-30 01:26:09	f	t
59	2	12	Argument wurde hinzugefügt	Hey Alexander,\n\njemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/12/undermine/57?history=/attitude/1-/justify/1/f-/reaction/5/undercut/12-/justify/12/f/undermine">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/12/undermine/57?history=/attitude/1-/justify/1/f-/reaction/5/undercut/12-/justify/12/f/undermine</a>	2017-01-30 01:26:09	f	t
60	2	14	Aussage wurde hinzugefügt	Hey Kálmán,\n\njemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/justify/19/t?history=/attitude/19-/justify/19/t">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/justify/19/t?history=/attitude/19-/justify/19/t</a>	2017-01-30 01:32:14	f	t
53	2	4	Argument was added	Hey, jemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/45/undermine/50?history=/attitude/48-/justify/42/d-/reaction/42/rebut/45-/justify/45/t/undermine-/reaction/49/end/0">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/45/undermine/50?history=/attitude/48-/justify/42/d-/reaction/42/rebut/45-/justify/45/t/undermine-/reaction/49/end/0</a>	2017-01-27 13:01:44	t	t
64	3	17	Willkommen	Willkommen im neuen dialog-basierten Argumentations-System.<br>Wir wünschen viel Spaß beim Diskutieren!	2017-01-30 14:30:32	f	t
65	2	11	Aussage wurde hinzugefügt	Hey Tobias,\n\njemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/justify/37/t?history=/attitude/37-/justify/37/t">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/justify/37/t?history=/attitude/37-/justify/37/t</a>	2017-01-30 14:58:07	f	t
67	2	14	Argument wurde hinzugefügt	Hey Kálmán,\n\njemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/35/undercut/63?history=/attitude/37-/justify/37/t-/justify/37/t-/reaction/62/rebut/35-/justify/35/t/undercut">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/35/undercut/63?history=/attitude/37-/justify/37/t-/justify/37/t-/reaction/62/rebut/35-/justify/35/t/undercut</a>	2017-01-30 15:25:37	f	t
69	3	4	Testnachricht	Will #274 debuggen	2017-01-30 16:05:15	t	f
66	2	5	Aussage wurde hinzugefügt	Hey Björn,\n\njemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/justify/37/t?history=/attitude/37-/justify/37/t">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/justify/37/t?history=/attitude/37-/justify/37/t</a>	2017-01-30 14:58:07	t	t
70	2	6	Aussage wurde hinzugefügt	Hey Daniel Tobias Pablo,\n\njemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/justify/34/t?history=/attitude/34-/justify/34/t">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/justify/34/t?history=/attitude/34-/justify/34/t</a>	2017-01-31 11:20:22	f	t
71	2	16	Argument wurde hinzugefügt	Hey Philipp,\n\njemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/59/undermine/65?history=/attitude/34-/justify/34/t-/reaction/64/rebut/59-/justify/59/t/undermine">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/59/undermine/65?history=/attitude/34-/justify/34/t-/reaction/64/rebut/59-/justify/59/t/undermine</a>	2017-01-31 11:24:06	t	t
68	3	4	Testnachricht	Will #274 debuggen	2017-01-30 16:05:15	t	t
72	4	3	überschriften sind überflüssig	`&#x27;`I am groot; ``&#x27;&#x27;´	2017-02-01 12:44:17.93832	f	t
73	4	3	überschriften sind überflüssig	`&#x27;`I am groot; ``&#x27;&#x27;´	2017-02-01 12:44:17.938472	t	f
74	3	18	Willkommen	Willkommen im neuen dialog-basierten Argumentations-System.<br>Wir wünschen viel Spaß beim Diskutieren!	2017-02-01 14:10:56.464296	t	t
75	2	13	Argument wurde hinzugefügt	Hey Hilmar,\n\njemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/23/undercut/68?history=/attitude/1-/justify/1/f-/reaction/5/undercut/13-/reaction/5/rebut/23-/justify/23/f/undercut">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/23/undercut/68?history=/attitude/1-/justify/1/f-/reaction/5/undercut/13-/reaction/5/rebut/23-/justify/23/f/undercut</a>	2017-02-01 14:19:46.381361	f	t
77	2	5	Argument wurde hinzugefügt	Hey Björn,\n\njemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/63/undermine/69?history=/attitude/37-/justify/37/f-/reaction/35/undercut/63-/justify/63/f/undermine">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/reaction/63/undermine/69?history=/attitude/37-/justify/37/f-/reaction/35/undercut/63-/justify/63/f/undermine</a>	2017-02-02 15:37:43.25857	f	t
78	3	20	Willkommen	Willkommen im neuen dialog-basierten Argumentations-System.<br>Wir wünschen viel Spaß beim Diskutieren!	2017-02-02 21:46:44.258854	f	t
79	3	21	Willkommen	Willkommen im neuen dialog-basierten Argumentations-System.<br>Wir wünschen viel Spaß beim Diskutieren!	2017-02-03 12:50:06.486889	f	t
80	2	14	Aussage wurde hinzugefügt	Hey Kálmán,\n\njemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/justify/19/t?history=/attitude/19-/justify/19/t">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/justify/19/t?history=/attitude/19-/justify/19/t</a>	2017-02-03 12:51:38.460467	f	t
81	2	13	Aussage wurde hinzugefügt	Hey Hilmar,\n\njemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/justify/48/f?history=/attitude/48-/justify/48/f">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/justify/48/f?history=/attitude/48-/justify/48/f</a>	2017-02-03 12:54:40.91084	f	t
82	2	6	Aussage wurde hinzugefügt	Hey Daniel Tobias Pablo,\n\njemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/justify/34/f?history=/attitude/34-/justify/34/f">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/justify/34/f?history=/attitude/34-/justify/34/f</a>	2017-02-03 12:59:56.692463	f	t
83	2	13	Aussage wurde hinzugefügt	Hey Hilmar,\n\njemand hat seine Meinung zu Ihrer Aussage hinzugefügt!<br>Wo: <a href="https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/justify/77/f?history=/attitude/77-/justify/77/f">https://dbas.cs.uni-duesseldorf.de/discuss/verbesserung-des-informatik-studiengangs/justify/77/f?history=/attitude/77-/justify/77/f</a>	2017-02-03 13:10:35.063346	f	t
\.


--
-- Name: messages_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('messages_uid_seq', 83, true);


--
-- Data for Name: optimization_review_locks; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY optimization_review_locks (author_uid, review_optimization_uid, locked_since) FROM stdin;
\.


--
-- Data for Name: premisegroups; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY premisegroups (uid, author_uid) FROM stdin;
1	3
2	3
3	6
4	5
5	4
6	7
7	9
8	10
9	11
10	12
11	12
12	12
13	12
14	12
15	14
16	14
17	14
18	14
19	14
20	4
21	4
22	14
23	13
24	14
25	12
26	13
27	12
28	11
29	13
30	13
31	14
32	13
33	14
34	11
35	11
36	13
37	13
38	13
39	13
40	13
41	14
42	12
43	4
44	12
45	5
46	13
47	13
48	13
49	16
50	16
51	16
52	16
53	16
54	16
55	16
56	16
57	7
58	6
59	5
60	13
61	13
62	13
63	13
64	18
65	9
66	21
67	21
68	21
69	21
70	1
71	1
72	1
73	1
74	1
75	1
76	1
77	1
78	1
79	1
80	1
81	1
82	1
83	1
84	1
85	1
86	1
87	1
88	1
89	1
90	1
91	1
92	1
93	1
94	1
95	1
96	1
97	1
98	1
99	1
100	1
101	1
102	1
103	1
104	1
105	1
106	1
107	1
108	1
109	1
110	1
111	1
112	1
113	1
114	1
115	1
116	1
117	1
118	1
119	1
120	1
121	1
122	1
123	1
124	1
125	1
126	1
127	1
128	1
129	1
130	5
131	1
132	1
133	1
134	1
135	1
\.


--
-- Name: premisegroups_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('premisegroups_uid_seq', 135, true);


--
-- Data for Name: premises; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY premises (uid, premisesgroup_uid, statement_uid, is_negated, author_uid, "timestamp", issue_uid, is_disabled) FROM stdin;
1	1	2	f	3	2017-01-26 17:08:50	1	f
2	2	3	f	3	2017-01-26 17:08:50	1	f
3	3	5	f	6	2017-01-26 17:14:12	1	f
4	4	7	f	5	2017-01-26 17:16:27	1	f
5	5	8	f	4	2017-01-26 17:17:01	1	f
6	6	9	f	7	2017-01-26 17:37:05	1	f
7	6	10	f	7	2017-01-26 17:37:05	1	f
8	7	11	f	9	2017-01-26 20:08:07	1	f
9	8	12	f	10	2017-01-27 09:16:25	1	f
10	9	13	f	11	2017-01-27 09:19:38	1	f
11	10	14	f	12	2017-01-27 10:04:21	1	f
12	11	15	f	12	2017-01-27 10:09:26	1	f
13	12	17	f	12	2017-01-27 10:29:22	1	f
14	13	16	f	12	2017-01-27 10:29:22	1	f
15	14	18	f	12	2017-01-27 10:29:22	1	f
16	15	20	f	14	2017-01-27 10:31:41	1	f
17	16	21	f	14	2017-01-27 10:34:16	1	f
18	17	22	f	14	2017-01-27 10:34:16	1	f
19	18	23	f	14	2017-01-27 10:35:51	1	f
20	19	24	f	14	2017-01-27 10:39:40	1	f
21	20	25	f	4	2017-01-27 10:40:48	1	f
22	21	26	f	4	2017-01-27 10:40:48	1	f
23	22	27	f	14	2017-01-27 10:43:49	1	f
24	23	28	f	13	2017-01-27 10:44:58	1	f
25	24	29	f	14	2017-01-27 10:45:05	1	f
26	25	30	f	12	2017-01-27 10:45:54	1	f
27	26	31	f	13	2017-01-27 10:47:52	1	f
28	27	32	f	12	2017-01-27 10:53:50	1	f
29	28	33	f	11	2017-01-27 10:53:59	1	f
30	29	35	f	13	2017-01-27 10:56:20	1	f
31	30	36	f	13	2017-01-27 11:04:21	1	f
32	31	38	f	14	2017-01-27 11:08:20	1	f
33	32	39	f	13	2017-01-27 11:11:28	1	f
34	33	40	f	14	2017-01-27 11:14:47	1	f
35	33	41	f	14	2017-01-27 11:14:47	1	f
36	34	42	f	11	2017-01-27 11:16:06	1	f
37	35	43	f	11	2017-01-27 11:20:43	1	f
38	36	44	f	13	2017-01-27 11:25:30	1	f
39	36	45	f	13	2017-01-27 11:25:30	1	f
40	37	46	f	13	2017-01-27 11:31:18	1	f
41	38	47	f	13	2017-01-27 11:32:51	1	f
42	39	49	f	13	2017-01-27 11:46:41	1	f
43	40	50	f	13	2017-01-27 11:46:41	1	f
44	41	51	f	14	2017-01-27 11:59:39	1	f
45	41	52	f	14	2017-01-27 11:59:39	1	f
46	42	53	f	12	2017-01-27 12:23:36	1	f
47	43	54	f	4	2017-01-27 12:29:58	1	f
48	44	55	f	12	2017-01-27 12:38:25	1	f
49	45	56	f	5	2017-01-27 12:49:51	1	f
50	46	57	f	13	2017-01-27 12:57:03	1	f
51	47	58	f	13	2017-01-27 13:01:18	1	f
52	47	59	f	13	2017-01-27 13:01:18	1	f
53	47	60	f	13	2017-01-27 13:01:18	1	f
54	48	61	f	13	2017-01-27 13:01:44	1	f
55	49	62	f	16	2017-01-30 01:26:07	1	f
56	49	63	f	16	2017-01-30 01:26:07	1	f
57	50	62	f	16	2017-01-30 01:26:07	1	f
58	50	63	f	16	2017-01-30 01:26:07	1	f
59	51	64	f	16	2017-01-30 01:26:07	1	f
60	52	66	f	16	2017-01-30 01:26:07	1	f
61	53	62	f	16	2017-01-30 01:26:07	1	f
62	53	65	f	16	2017-01-30 01:26:07	1	f
63	53	67	f	16	2017-01-30 01:26:07	1	f
64	54	68	f	16	2017-01-30 01:32:12	1	f
65	55	69	f	16	2017-01-30 01:37:56	1	f
66	56	70	f	16	2017-01-30 01:39:31	1	f
67	57	71	f	7	2017-01-30 09:08:58	1	f
68	57	72	f	7	2017-01-30 09:08:58	1	f
69	58	73	f	6	2017-01-30 14:58:04	1	f
70	59	74	f	5	2017-01-30 15:25:36	1	f
71	60	75	f	13	2017-01-31 11:20:20	1	f
72	61	76	f	13	2017-01-31 11:24:05	1	f
73	62	78	f	13	2017-01-31 11:32:55	1	f
74	63	79	f	13	2017-01-31 11:32:55	1	f
75	64	80	f	18	2017-02-01 14:19:45	1	f
76	65	81	f	9	2017-02-02 15:37:41	1	f
77	66	82	f	21	2017-02-03 12:51:37	1	f
78	67	83	f	21	2017-02-03 12:54:39	1	f
79	68	84	f	21	2017-02-03 12:59:55	1	f
80	69	85	f	21	2017-02-03 13:10:33	1	f
81	69	86	f	21	2017-02-03 13:10:33	1	f
82	70	87	f	1	2017-02-15 10:05:04.109258	3	t
83	71	91	f	1	2017-02-15 10:05:04.109258	3	f
84	72	92	f	1	2017-02-15 10:05:04.109258	3	f
85	73	93	f	1	2017-02-15 10:05:04.109258	3	f
86	74	94	f	1	2017-02-15 10:05:04.109258	3	f
87	75	95	f	1	2017-02-15 10:05:04.109258	3	f
88	76	96	f	1	2017-02-15 10:05:04.109258	3	f
89	77	97	f	1	2017-02-15 10:05:04.109258	3	f
90	78	98	f	1	2017-02-15 10:05:04.109258	3	f
91	79	99	f	1	2017-02-15 10:05:04.109258	3	f
92	80	100	f	1	2017-02-15 10:05:04.109258	3	f
93	81	101	f	1	2017-02-15 10:05:04.109258	3	f
94	81	102	f	1	2017-02-15 10:05:04.109258	3	f
95	82	103	f	1	2017-02-15 10:05:04.109258	3	f
96	83	104	f	1	2017-02-15 10:05:04.109258	3	f
97	84	105	f	1	2017-02-15 10:05:04.109258	3	f
98	85	106	f	1	2017-02-15 10:05:04.109258	3	f
99	86	107	f	1	2017-02-15 10:05:04.109258	3	f
100	87	108	f	1	2017-02-15 10:05:04.109258	3	f
101	88	109	f	1	2017-02-15 10:05:04.109258	3	f
102	89	110	f	1	2017-02-15 10:05:04.109258	3	f
103	90	111	f	1	2017-02-15 10:05:04.109258	3	f
104	91	112	f	1	2017-02-15 10:05:04.109258	3	f
105	92	113	f	1	2017-02-15 10:05:04.109258	3	f
106	93	114	f	1	2017-02-15 10:05:04.109258	3	f
107	94	115	f	1	2017-02-15 10:05:04.109258	3	f
108	95	116	f	1	2017-02-15 10:05:04.109258	3	f
109	96	117	f	1	2017-02-15 10:05:04.109258	3	f
110	97	118	f	1	2017-02-15 10:05:04.109258	3	f
111	98	119	f	1	2017-02-15 10:05:04.109258	3	f
112	99	120	f	1	2017-02-15 10:05:04.109258	3	f
113	78	121	f	1	2017-02-15 10:05:04.109258	3	f
114	100	125	f	1	2017-02-15 10:05:04.109258	2	f
115	101	126	f	1	2017-02-15 10:05:04.109258	2	f
116	102	127	f	1	2017-02-15 10:05:04.109258	2	f
117	103	128	f	1	2017-02-15 10:05:04.109258	2	f
118	104	129	f	1	2017-02-15 10:05:04.109258	2	f
119	105	130	f	1	2017-02-15 10:05:04.109258	2	f
120	106	131	f	1	2017-02-15 10:05:04.109258	2	f
121	107	132	f	1	2017-02-15 10:05:04.109258	2	f
122	108	133	f	1	2017-02-15 10:05:04.109258	2	f
123	109	134	f	1	2017-02-15 10:05:04.109258	2	f
124	110	135	f	1	2017-02-15 10:05:04.109258	2	f
125	111	136	f	1	2017-02-15 10:05:04.109258	2	f
126	112	137	f	1	2017-02-15 10:05:04.109258	2	f
127	113	138	f	1	2017-02-15 10:05:04.109258	2	f
128	114	139	f	1	2017-02-15 10:05:04.109258	2	f
129	115	140	f	1	2017-02-15 10:05:04.109258	2	f
130	116	141	f	1	2017-02-15 10:05:04.109258	2	f
131	117	142	f	1	2017-02-15 10:05:04.109258	2	f
132	118	143	f	1	2017-02-15 10:05:04.109258	2	f
133	121	147	f	1	2017-02-15 10:05:04.109258	4	f
134	122	148	f	1	2017-02-15 10:05:04.109258	4	f
135	123	149	f	1	2017-02-15 10:05:04.109258	4	f
136	124	150	f	1	2017-02-15 10:05:04.109258	4	f
137	125	151	f	1	2017-02-15 10:05:04.109258	4	f
138	126	152	f	1	2017-02-15 10:05:04.109258	4	f
139	119	145	f	1	2017-02-15 10:05:04.109258	4	f
140	120	146	f	1	2017-02-15 10:05:04.109258	4	f
141	130	154	f	5	2017-02-15 10:05:04.109258	4	f
\.


--
-- Name: premises_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('premises_uid_seq', 141, true);


--
-- Data for Name: reputation_history; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY reputation_history (uid, reputator_uid, reputation_uid, "timestamp") FROM stdin;
\.


--
-- Name: reputation_history_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('reputation_history_uid_seq', 108, true);


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
9	rep_reason_bad_flag	-1
10	rep_reason_bad_edit	-1
11	rep_reason_success_duplicate	3
12	rep_reason_bad_duplicate	-1
\.


--
-- Name: reputation_reasons_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('reputation_reasons_uid_seq', 10, true);


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
1	13	\N	37	2017-01-31 11:10:56	f	1	f
\.


--
-- Name: review_deletes_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('review_deletes_uid_seq', 1, true);


--
-- Data for Name: review_duplicates; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY review_duplicates (uid, detector_uid, duplicate_statement_uid, original_statement_uid, "timestamp", is_executed, is_revoked) FROM stdin;
\.


--
-- Name: review_duplicates_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('review_duplicates_uid_seq', 1, false);


--
-- Data for Name: review_edit_values; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY review_edit_values (uid, review_edit_uid, statement_uid, typeof, content) FROM stdin;
1	1	28	statement	Viele Studierende sich anmelden, ohne genau zu wissen was es braucht um dieses Fach zu studieren.
2	2	37	statement	Eine Zulassungsbeschränkung auch über einen Vortest geregelt werden kann, statt über den Abiturschnitt
3	3	37	statement	Eine Zulassungsbeschränkung auch über einen Vortest geregelt werden kann, statt über den Abiturschnitt
4	4	1	statement	Trolle Argumente verändern können
5	5	68	statement	Mehr Studierende erfordern mehr Lehrpersonal
6	6	68	statement	Mehr Studierende erfordern mehr Leehrpersonal
7	7	68	statement	Mehr Studierende erfordern mehr Leehrpersonal
8	8	57	statement	Es schonmal ein erster Schritt ist, um das Studium internationaler zu machen
9	9	77	statement	im Curriculum verankerte praktische Übungskurse auch durch Praktikas in der Wirtschaft abgedeckt werden können sollten
10	11	68	statement	Mehr Studierende erfordern mehr Lehrpersonal
11	11	68	statement	Mehr Studierende erfordern mehr Lehrpersonal
12	13	68	statement	Mehr Studierende erfordern mehr Lehrpersonal
13	13	68	statement	Mehr Studierende erfordern mehr Lehrpersonal
\.


--
-- Name: review_edit_values_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('review_edit_values_uid_seq', 13, true);


--
-- Data for Name: review_edits; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY review_edits (uid, detector_uid, argument_uid, statement_uid, "timestamp", is_executed, is_revoked) FROM stdin;
1	13	\N	28	2017-01-27 12:01:34	t	f
3	5	\N	37	2017-01-27 12:17:44	t	f
2	13	\N	37	2017-01-27 12:17:53	t	f
4	16	\N	1	2017-01-30 01:12:13	f	f
5	16	\N	68	2017-01-30 01:32:43	f	f
6	16	\N	68	2017-01-30 01:34:47	f	f
7	16	\N	68	2017-01-30 01:35:07	f	f
8	13	\N	57	2017-01-31 11:26:16	f	f
9	13	\N	77	2017-01-31 11:33:47	f	f
10	21	\N	68	2017-02-03 12:53:39.392385	f	f
11	21	\N	68	2017-02-03 12:53:39.393504	f	f
12	21	\N	68	2017-02-03 12:53:39.423417	f	f
13	21	\N	68	2017-02-03 12:53:39.425254	f	f
\.


--
-- Name: review_edits_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('review_edits_uid_seq', 13, true);


--
-- Data for Name: review_optimizations; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY review_optimizations (uid, detector_uid, argument_uid, statement_uid, "timestamp", is_executed, is_revoked) FROM stdin;
1	13	\N	37	2017-01-27 11:44:38	t	f
2	16	\N	58	2017-01-30 01:35:59	f	f
\.


--
-- Name: review_optimizations_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('review_optimizations_uid_seq', 2, true);


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
1	6	1	Position wurde hinzugefügt	...das Anforderungsniveau des Studiums erhöht werden sollte...	2017-01-26 17:12:54
2	6	1	Aussage wurde hinzugefügt	...die Studierendenzahlen durch ein hohes Anforderungsniveau auf natürliche Weise gesenkt werden können...	2017-01-26 17:14:12
3	6	1	Argument wurde hinzugefügt	...Es ist richtig, dass das Anforderungsniveau des Studiums erhöht werden sollte, weil die Studierendenzahlen durch ein hohes Anforderungsniveau auf natürliche Weise gesenkt werden können...	2017-01-26 17:14:12
4	5	1	Position wurde hinzugefügt	...Grundmodule mehrere Termine haben sollten, um die Anzahl der Studierenden pro Veranstaltung zu reduzieren...	2017-01-26 17:14:20
5	5	1	Aussage wurde hinzugefügt	...Veranstaltungen mit weniger Teilnehmern angenehmer sind...	2017-01-26 17:16:26
6	5	1	Argument wurde hinzugefügt	...Es ist richtig, dass Grundmodule mehrere Termine haben sollten, um die Anzahl der Studierenden pro Veranstaltung zu reduzieren, weil Veranstaltungen mit weniger Teilnehmern angenehmer sind...	2017-01-26 17:16:27
7	4	1	Aussage wurde hinzugefügt	...man lieber die Kapazitäten der Universität aufstocken sollte anstatt neue Studierende vom Studium auszuschließen...	2017-01-26 17:17:00
8	4	1	Argument wurde hinzugefügt	...Es ist falsch, dass  es nicht richtig ist, dass eine Zulassungsbeschränkung eingeführt werden soll, weil man lieber die Kapazitäten der Universität aufstocken sollte anstatt neue Studierende vom Studium auszuschließen...	2017-01-26 17:17:01
9	7	1	Aussage wurde hinzugefügt	...die Studierenden einen fachlich höheren Abschluss erlangen...	2017-01-26 17:37:05
10	7	1	Aussage wurde hinzugefügt	...zu einem guten Ruf der Universität beitragen...	2017-01-26 17:37:05
11	7	1	Argument wurde hinzugefügt	...Es ist richtig, dass das Anforderungsniveau des Studiums erhöht werden sollte, weil die Studierenden einen fachlich höheren Abschluss erlangen und zu einem guten Ruf der Universität beitragen...	2017-01-26 17:37:05
12	9	1	Aussage wurde hinzugefügt	...bereits jetzt viele Studenten das Studium abbrechen...	2017-01-26 20:08:07
13	9	1	Argument wurde hinzugefügt	...Es ist falsch, dass  es nicht richtig ist, dass das Anforderungsniveau des Studiums erhöht werden sollte, weil bereits jetzt viele Studenten das Studium abbrechen...	2017-01-26 20:08:07
14	10	1	Aussage wurde hinzugefügt	...ein Großteil der Studenten aufgrund gesellschaftlicher Vorgaben (u.a. Eltern, die Abitur/Studium vorgeben) studieren. Hier sollte Qualität vor Quantität der Ausbildung gehen...	2017-01-27 09:16:25
15	11	1	Aussage wurde hinzugefügt	...Viele Studenten wissen nach dem Abitur nicht, welche Karriereweg sie einschlagen möchten. Oft merken sie erst im Studium, dass es ihnen nicht liegt...	2017-01-27 09:19:38
16	12	1	Aussage wurde hinzugefügt	...die Termine sich von der Qualität stark unterscheiden können, insbesondere wenn diese von verschiedenen Lehrkräften gehalten werden. Das sorgt für Ungleichheit der Lehre...	2017-01-27 10:04:21
17	12	1	Argument wurde hinzugefügt	...Es ist falsch, dass  es nicht richtig ist, dass Grundmodule mehrere Termine haben sollten, um die Anzahl der Studierenden pro Veranstaltung zu reduzieren, weil die Termine sich von der Qualität stark unterscheiden können, insbesondere wenn diese von verschiedenen Lehrkräften gehalten werden. Das sorgt für Ungleichheit der Lehre...	2017-01-27 10:04:21
18	12	1	Aussage wurde hinzugefügt	...das einen erheblichen Mehraufwand an Arbeit bedeutet, der in keiner Relation zu den Vorteilen steht...	2017-01-27 10:09:26
19	12	1	Aussage wurde hinzugefügt	...es aktuell nicht einfach ist, mehr Geld pro Studierenden so zu verteilen, dass es eine bessere Raum- und Betreuungssituation ergibt...	2017-01-27 10:29:22
20	12	1	Aussage wurde hinzugefügt	...es aktuell nicht einfach ist, mehr Geld pro Studierenden so zu verteilen, dass es eine bessere Raum- und Betreuungssituation ergibt...	2017-01-27 10:29:22
21	12	1	Aussage wurde hinzugefügt	...es aktuell nicht einfach ist, mehr Geld pro Studierenden so zu verteilen, dass es eine bessere Raum- und Betreuungssituation ergibt...	2017-01-27 10:29:22
22	14	1	Position wurde hinzugefügt	...mehr Lehrpersonal angestellt werden müsste: Professoren, Doktoranden, Hilfskräfte...	2017-01-27 10:30:53
23	14	1	Aussage wurde hinzugefügt	...Ein höheres Betreuungsverhältnis fördert den Lernerfolg...	2017-01-27 10:31:41
24	14	1	Argument wurde hinzugefügt	...Es ist richtig, dass mehr Lehrpersonal angestellt werden müsste: Professoren, Doktoranden, Hilfskräfte, weil Ein höheres Betreuungsverhältnis fördert den Lernerfolg...	2017-01-27 10:31:41
25	14	1	Aussage wurde hinzugefügt	...man nur Rheinbahnstudenten abschrecken würde, die auch jetzt nicht zu den Vorlesungen kommen...	2017-01-27 10:34:16
26	14	1	Argument wurde hinzugefügt	...Es ist falsch, dass  es nicht richtig ist, dass eine Zulassungsbeschränkung eingeführt werden soll, weil man nur Rheinbahnstudenten abschrecken würde, die auch jetzt nicht zu den Vorlesungen kommen...	2017-01-27 10:34:16
27	14	1	Aussage wurde hinzugefügt	...Weniger angemeldete Studenten auch weniger Geld für die Betreuung der tatsächlich studierenden bedeuten würde...	2017-01-27 10:34:16
28	14	1	Argument wurde hinzugefügt	...Es ist falsch, dass  es nicht richtig ist, dass eine Zulassungsbeschränkung eingeführt werden soll, weil Weniger angemeldete Studenten auch weniger Geld für die Betreuung der tatsächlich studierenden bedeuten würde...	2017-01-27 10:34:16
29	14	1	Aussage wurde hinzugefügt	...das kein Argument ist. Warum muss zu einer hohen Nachfrage automatisch das Angebot beschränkt werden...	2017-01-27 10:35:51
30	14	1	Aussage wurde hinzugefügt	...man nicht die Abbrecherquote erhöhen sollte, sondern die Anzahl der weniger begabten Erstsemestler...	2017-01-27 10:39:40
31	14	1	Argument wurde hinzugefügt	...Es ist falsch, dass  es nicht richtig ist, dass das Anforderungsniveau des Studiums erhöht werden sollte, weil man nicht die Abbrecherquote erhöhen sollte, sondern die Anzahl der weniger begabten Erstsemestler...	2017-01-27 10:39:40
32	4	1	Aussage wurde hinzugefügt	...das vernachlässigbar ist, da die Vorlesungsmaterialien die selben sind...	2017-01-27 10:40:48
33	4	1	Aussage wurde hinzugefügt	...das vernachlässigbar ist, da die Skills der Dozenten sich nicht allzu sehr unterscheiden sollten in den Grundlagenveranstaltungen...	2017-01-27 10:40:48
34	14	1	Aussage wurde hinzugefügt	...weil es Montags immer Brötchen in der Mensa gibt...	2017-01-27 10:43:49
35	14	1	Argument wurde hinzugefügt	...Es ist falsch, dass  es nicht richtig ist, dass eine Zulassungsbeschränkung eingeführt werden soll, weil weil es Montags immer Brötchen in der Mensa gibt...	2017-01-27 10:43:49
36	13	1	Aussage wurde hinzugefügt	...Viele Studierende sich anmelden, ohne genau zu wissen was es braucht um dieses Fach zu studieren. Ein Vortest wäre sinnvoll...	2017-01-27 10:44:58
41	12	1	Aussage wurde hinzugefügt	...auch Fragen und Mitarbeit der Studierenden, welche wichtige Aha-Momente für die Mithörer im Raum auslösen, zwischen den Terminen variieren...	2017-01-27 10:53:50
37	13	1	Argument wurde hinzugefügt	...Es ist richtig, dass eine Zulassungsbeschränkung eingeführt werden soll, weil Viele Studierende sich anmelden, ohne genau zu wissen was es braucht um dieses Fach zu studieren. Ein Vortest wäre sinnvoll...	2017-01-27 10:44:59
38	14	1	Aussage wurde hinzugefügt	...nicht die die Nachfrage künstlich verknappt werden sollte, sondern das Angebot, d.h. Uni-Ressourcen, erweitert werden sollten...	2017-01-27 10:45:05
40	13	1	Aussage wurde hinzugefügt	...Eine Zulassungsbeschränkung auch über einen Vortest geregelt werden kann, statt über den Abiturschnitt...	2017-01-27 10:47:52
39	12	1	Aussage wurde hinzugefügt	...eine Beschränkung nicht zwingend die Nachfrage nach dem Studiengang senkt, sondern nur die Anzahl der tatsächlich studierenden pro Semester. Siehe Medizin und deren Wartelisten als Beispiel...	2017-01-27 10:45:54
42	11	1	Aussage wurde hinzugefügt	...Eine Abiturnote sagt nichts über die Fähigkeiten im Studienfach aus. Bsp.: Medizin benötigt kein Vorwissen...	2017-01-27 10:53:59
43	11	1	Argument wurde hinzugefügt	...Es ist falsch, dass  es nicht richtig ist, dass eine Zulassungsbeschränkung eingeführt werden soll, weil Eine Abiturnote sagt nichts über die Fähigkeiten im Studienfach aus. Bsp.: Medizin benötigt kein Vorwissen...	2017-01-27 10:53:59
46	13	1	Aussage wurde hinzugefügt	...Einen Vortest einzuführen dazu beitragen würde, dass das Anforderungsniveau erhöht wird, aber nicht die Abbrecherquote...	2017-01-27 10:56:20
44	6	1	Position wurde hinzugefügt	...man die für den Informatikstudiengang ungeeigneten Studierenden durch einen Vortest &quot;aussortieren&quot; sollte...	2017-01-27 10:55:41
48	13	1	Aussage wurde hinzugefügt	...um international mithalten zu können wir nicht um eine Erhöhung des Anforderungsniveaus herumkommen...	2017-01-27 11:04:21
49	13	1	Argument wurde hinzugefügt	...Es ist richtig, dass das Anforderungsniveau des Studiums erhöht werden sollte, weil um international mithalten zu können wir nicht um eine Erhöhung des Anforderungsniveaus herumkommen...	2017-01-27 11:04:21
45	6	1	Argument wurde hinzugefügt	...Es ist richtig, dass man die für den Informatikstudiengang ungeeigneten Studierenden durch einen Vortest &quot;aussortieren&quot; sollte, weil Eine Zulassungsbeschränkung auch über einen Vortest geregelt werden kann, statt über den Abiturschnitt...	2017-01-27 10:56:10
50	11	1	Position wurde hinzugefügt	...Eine Zulassungsbeschräeinnkung auch über einen Vortest geregelt werden kann, statt über den Abiturschnitt...	2017-01-27 11:07:35
51	14	1	Aussage wurde hinzugefügt	...sie mir ja zustimmen. Ein Vortest filtert die schlechten Erstis raus, hat aber keinen Einfluss auf das Niveau des Studiums...	2017-01-27 11:08:19
47	13	1	Argument wurde hinzugefügt	...Es ist richtig, dass man die für den Informatikstudiengang ungeeigneten Studierenden durch einen Vortest &quot;aussortieren&quot; sollte, weil Einen Vortest einzuführen dazu beitragen würde, dass das Anforderungsniveau erhöht wird, aber nicht die Abbrecherquote...	2017-01-27 10:57:37
52	13	1	Aussage wurde hinzugefügt	...wir das Ausbildungsniveau nicht deshalb absenken sollten, nur weil es viele Abbrecher gibt in einem bis dato zulassungsfreien Studiengang...	2017-01-27 11:11:28
53	14	1	Aussage wurde hinzugefügt	...Jede Aussage mit &quot;kann&quot; ist richtig, ich fände das aber falsch, da ein Vortest enormen Aufwand für das Lehrpersonal bedeutet, die Ihre Zeit von der eigentliche Lehre abziehen müssten...	2017-01-27 11:14:46
54	14	1	Aussage wurde hinzugefügt	...es so zu einer schlechteren Lehre führt...	2017-01-27 11:14:47
55	14	1	Argument wurde hinzugefügt	...Es ist falsch, dass  es nicht richtig ist, dass Eine Zulassungsbeschräeinnkung auch über einen Vortest geregelt werden kann, statt über den Abiturschnitt, weil Jede Aussage mit &quot;kann&quot; ist richtig, ich fände das aber falsch, da ein Vortest enormen Aufwand für das Lehrpersonal bedeutet, die Ihre Zeit von der eigentliche Lehre abziehen müssten und es so zu einer schlechteren Lehre führt...	2017-01-27 11:14:47
56	11	1	Aussage wurde hinzugefügt	...der Vortest kann auf das Fach abgestimmt werden...	2017-01-27 11:16:06
57	11	1	Argument wurde hinzugefügt	...Es ist richtig, dass Eine Zulassungsbeschräeinnkung auch über einen Vortest geregelt werden kann, statt über den Abiturschnitt, weil der Vortest kann auf das Fach abgestimmt werden...	2017-01-27 11:16:06
58	11	1	Aussage wurde hinzugefügt	...man statt Vortest auch andere Qualifikationen prüfen könnte. Bsp. Medizin: hat ein(e) Student(in) bereits Erfahrung, z.B. durch Beruf, Zivildienst, freiwilliges soziales Jahr...	2017-01-27 11:20:43
59	13	1	Aussage wurde hinzugefügt	...ein Vortest dazu führt, dass mehr begabte Studierende eingeschrieben sind...	2017-01-27 11:25:30
60	13	1	Aussage wurde hinzugefügt	...somit die Kurse anspruchvoller gestaltet werden können...	2017-01-27 11:25:30
61	13	1	Argument wurde hinzugefügt	...Es ist falsch, dass  es nicht richtig ist, dass sie mir ja zustimmen. Ein Vortest filtert die schlechten Erstis raus, hat aber keinen Einfluss auf das Niveau des Studiums, weil ein Vortest dazu führt, dass mehr begabte Studierende eingeschrieben sind und somit die Kurse anspruchvoller gestaltet werden können...	2017-01-27 11:25:30
62	13	1	Aussage wurde hinzugefügt	...Selbst in Grundveranstaltungen die Lehrkräfte in ihren Kursen auf verschiedene inhaltliche Dinge Wert legen...	2017-01-27 11:31:18
63	13	1	Aussage wurde hinzugefügt	...Lehrkräfte somit unnötig doppelt belastet werden, wenn man bedenkt, dass viele der Studierenden sowieso abbrechen werden...	2017-01-27 11:32:50
64	13	1	Argument wurde hinzugefügt	...Es ist falsch, dass  es nicht richtig ist, dass Grundmodule mehrere Termine haben sollten, um die Anzahl der Studierenden pro Veranstaltung zu reduzieren, weil Lehrkräfte somit unnötig doppelt belastet werden, wenn man bedenkt, dass viele der Studierenden sowieso abbrechen werden...	2017-01-27 11:32:51
65	13	1	Position wurde hinzugefügt	...Die Unterrichtssprache des Informatik-Studiums Englisch sein sollte...	2017-01-27 11:45:20
66	13	1	Aussage wurde hinzugefügt	...das Studium so internationaler wäre...	2017-01-27 11:46:41
67	13	1	Argument wurde hinzugefügt	...Es ist richtig, dass Die Unterrichtssprache des Informatik-Studiums Englisch sein sollte, weil das Studium so internationaler wäre...	2017-01-27 11:46:41
68	13	1	Aussage wurde hinzugefügt	...Fachbegriffe sowieso auf Englisch sind...	2017-01-27 11:46:41
69	13	1	Argument wurde hinzugefügt	...Es ist richtig, dass Die Unterrichtssprache des Informatik-Studiums Englisch sein sollte, weil Fachbegriffe sowieso auf Englisch sind...	2017-01-27 11:46:41
70	14	1	Aussage wurde hinzugefügt	...fast alle Anfänger direkt nach dem Abi ihr Studium beginnen...	2017-01-27 11:59:39
71	14	1	Aussage wurde hinzugefügt	...man für diese 90% dennoch einen aufwändigen Vortest durchführen müsste...	2017-01-27 11:59:39
72	12	1	Aussage wurde hinzugefügt	...es Informatiker (in der Wissenschaft als auch in der Industrie) einen enormen Vorteil bietet die de facto lingua franca der Branche sehr gut zu beherrschen...	2017-01-27 12:23:36
73	12	1	Argument wurde hinzugefügt	...Es ist richtig, dass Die Unterrichtssprache des Informatik-Studiums Englisch sein sollte, weil es Informatiker (in der Wissenschaft als auch in der Industrie) einen enormen Vorteil bietet die de facto lingua franca der Branche sehr gut zu beherrschen...	2017-01-27 12:23:36
74	4	1	Aussage wurde hinzugefügt	...das nur Sinn ergibt, wenn man in die Wissenschaft geht, was aber nicht bei jedem Bachelorstudenten gegeben ist...	2017-01-27 12:29:57
75	4	1	Argument wurde hinzugefügt	...Es ist falsch, dass  es nicht richtig ist, dass Die Unterrichtssprache des Informatik-Studiums Englisch sein sollte, weil das nur Sinn ergibt, wenn man in die Wissenschaft geht, was aber nicht bei jedem Bachelorstudenten gegeben ist...	2017-01-27 12:29:58
76	12	1	Aussage wurde hinzugefügt	...zu einem international hervorragenden Studium mehr dazu gehört als nur die Studiumssprache auf Englisch zu haben...	2017-01-27 12:38:25
77	5	1	Aussage wurde hinzugefügt	...die Vorteile einer besseren Arbeitsumgebung, die möglichen Nachteile der Ungleichheit überwiegen...	2017-01-27 12:49:51
78	13	1	Aussage wurde hinzugefügt	...Es schonmal ein erster Schritt ist, um ein das Studium internationaler zu machen...	2017-01-27 12:57:03
79	13	1	Aussage wurde hinzugefügt	...Auch in der Wirtschaft...	2017-01-27 13:01:17
80	13	1	Aussage wurde hinzugefügt	...anderen Bereichen sind Fachbegriffe...	2017-01-27 13:01:17
81	13	1	Aussage wurde hinzugefügt	...Terminologie auf Englisch...	2017-01-27 13:01:18
82	13	1	Aussage wurde hinzugefügt	...Auch in der Wirtschaft und anderen Bereichen sind Fachbegriffe und Terminologie auf Englisch...	2017-01-27 13:01:44
83	16	1	Aussage wurde hinzugefügt	...Mehr Räume kann man notfalls durch Container kurzfristig schaffen...	2017-01-30 01:26:06
84	16	1	Aussage wurde hinzugefügt	...freie Seminarräume gibt&#x27;s z.B. im Neubau...	2017-01-30 01:26:07
85	16	1	Aussage wurde hinzugefügt	...Gute und Hiwi-willige Studierende sollten proportional zur Anzahl der Gesamtstudierenden sein...	2017-01-30 01:26:07
86	16	1	Aussage wurde hinzugefügt	...innerhalb der Uni finden sich sicher noch ungenutzte Kapazitäten - unsere Seminarräume sind ja keineswegs nahe 100% ausgebucht. Gute...	2017-01-30 01:26:07
87	16	1	Aussage wurde hinzugefügt	...t. Gute und Hiwi-willige Studierende sollten proportional zur Anzahl der Gesamtstudierenden sein...	2017-01-30 01:26:07
88	16	1	Aussage wurde hinzugefügt	...Hiwi-willige Studierende sollten proportional zur Anzahl der Gesamtstudierenden sein...	2017-01-30 01:26:07
89	16	1	Aussage wurde hinzugefügt	...Mehr Studierende erfordern mehr Leerpersonal...	2017-01-30 01:32:12
90	16	1	Argument wurde hinzugefügt	...Es ist richtig, dass mehr Lehrpersonal angestellt werden müsste: Professoren, Doktoranden, Hilfskräfte, weil Mehr Studierende erfordern mehr Leerpersonal...	2017-01-30 01:32:12
94	7	1	Aussage wurde hinzugefügt	...die Studierenden eine fachlich angemessenere Ausbildung erlangen...	2017-01-30 09:08:57
95	7	1	Aussage wurde hinzugefügt	...auf dem Arbeitsmarkt damit eine bessere Stellung erhalten...	2017-01-30 09:08:57
96	7	1	Argument wurde hinzugefügt	...Es ist richtig, dass das Anforderungsniveau des Studiums erhöht werden sollte, weil die Studierenden eine fachlich angemessenere Ausbildung erlangen und auf dem Arbeitsmarkt damit eine bessere Stellung erhalten...	2017-01-30 09:08:58
91	16	1	Aussage wurde hinzugefügt	...es ist unklar was man überhaupt testen könnte, ohne gleich Inhalte des ersten Semesters zu verlangen...	2017-01-30 01:37:56
92	16	1	Argument wurde hinzugefügt	...Es ist falsch, dass  es nicht richtig ist, dass man die für den Informatikstudiengang ungeeigneten Studierenden durch einen Vortest &quot;aussortieren&quot; sollte, weil es ist unklar was man überhaupt testen könnte, ohne gleich Inhalte des ersten Semesters zu verlangen...	2017-01-30 01:37:56
93	16	1	Aussage wurde hinzugefügt	...der Vortest würde die Inhalte des ersten Semesters verlangen, anstatt die generelle Lernwilligkeit...	2017-01-30 01:39:31
97	6	1	Aussage wurde hinzugefügt	...ein Vortest die fachspezifische Eignung sicherstellt anstatt allgemein guter Leistung...	2017-01-30 14:58:04
98	6	1	Argument wurde hinzugefügt	...Es ist richtig, dass Eine Zulassungsbeschränkung auch über einen Vortest geregelt werden kann, statt über den Abiturschnitt, weil ein Vortest die fachspezifische Eignung sicherstellt anstatt allgemein guter Leistung...	2017-01-30 14:58:04
99	5	1	Aussage wurde hinzugefügt	...ein Vortest auch maschinell erfolgen kann...	2017-01-30 15:25:36
100	13	1	Aussage wurde hinzugefügt	...so die Anzahl an &quot;Rheinbahnstudenten&quot; vermutlich verringert werden würde...	2017-01-31 11:20:20
101	13	1	Argument wurde hinzugefügt	...Es ist richtig, dass man die für den Informatikstudiengang ungeeigneten Studierenden durch einen Vortest &quot;aussortieren&quot; sollte, weil so die Anzahl an &quot;Rheinbahnstudenten&quot; vermutlich verringert werden würde...	2017-01-31 11:20:21
102	13	1	Aussage wurde hinzugefügt	...Es genügend Beispiele von Vortests gibt, die allgemeines logisches Verständnis prüfen, ohne gelerntes Wissen abzufragen...	2017-01-31 11:24:05
103	13	1	Position wurde hinzugefügt	...im Curriculum verankerte praktische Übungskurse auch durch Praktikas in der Wirtschaft abgedeckt werden können sollte...	2017-01-31 11:29:33
104	13	1	Aussage wurde hinzugefügt	...so die Wirtschaft stärker mit der Universität vernetzt werden würde...	2017-01-31 11:32:55
105	13	1	Argument wurde hinzugefügt	...Es ist richtig, dass im Curriculum verankerte praktische Übungskurse auch durch Praktikas in der Wirtschaft abgedeckt werden können sollte, weil so die Wirtschaft stärker mit der Universität vernetzt werden würde...	2017-01-31 11:32:55
106	13	1	Aussage wurde hinzugefügt	...so die Lehrkräfte entlastet werden durch weniger Übungsbetrieb...	2017-01-31 11:32:55
107	13	1	Argument wurde hinzugefügt	...Es ist richtig, dass im Curriculum verankerte praktische Übungskurse auch durch Praktikas in der Wirtschaft abgedeckt werden können sollte, weil so die Lehrkräfte entlastet werden durch weniger Übungsbetrieb...	2017-01-31 11:32:55
108	18	1	Aussage wurde hinzugefügt	...Studis sollen aber auch ruhig mal n wenig ausprobieren können...	2017-02-01 14:19:44.839699
109	9	1	Aussage wurde hinzugefügt	...es viele Fähigkeiten, wie z.B. logisches Denken gibt, die (noch) nicht automatisiert geprüft werden können...	2017-02-02 15:37:41.179969
110	21	1	Aussage wurde hinzugefügt	...dadurch noch mehr Vorlesungen angeboten werden können...	2017-02-03 12:51:36.786855
111	21	1	Argument wurde hinzugefügt	...Es ist richtig, dass mehr Lehrpersonal angestellt werden müsste: Professoren, Doktoranden, Hilfskräfte, weil dadurch noch mehr Vorlesungen angeboten werden können...	2017-02-03 12:51:37.088381
112	21	1	Aussage wurde hinzugefügt	...es im Bachelorstudiengang die meisten Studierenden überfordern würde...	2017-02-03 12:54:39.364785
113	21	1	Argument wurde hinzugefügt	...Es ist falsch, dass  es nicht richtig ist, dass Die Unterrichtssprache des Informatik-Studiums Englisch sein sollte, weil es im Bachelorstudiengang die meisten Studierenden überfordern würde...	2017-02-03 12:54:39.593127
114	21	1	Aussage wurde hinzugefügt	...das eventuell Studenten ausfiltert, die unter Einsatz von Fleiß doch zu geeigneten Studenten werden...	2017-02-03 12:59:55.07237
115	21	1	Argument wurde hinzugefügt	...Es ist falsch, dass  es nicht richtig ist, dass man die für den Informatikstudiengang ungeeigneten Studierenden durch einen Vortest &quot;aussortieren&quot; sollte, weil das eventuell Studenten ausfiltert, die unter Einsatz von Fleiß doch zu geeigneten Studenten werden...	2017-02-03 12:59:55.298223
116	21	1	Aussage wurde hinzugefügt	...entsprechende Praktikumsbescheinigungen keinen Qualitätskontrollen genügen können...	2017-02-03 13:10:33.140235
117	21	1	Aussage wurde hinzugefügt	...somit ausgestellt werden können, ohne das ein Student entsprechende praktische Erfahrung gesammelt hat...	2017-02-03 13:10:33.355933
118	21	1	Argument wurde hinzugefügt	...Es ist falsch, dass  es nicht richtig ist, dass im Curriculum verankerte praktische Übungskurse auch durch Praktikas in der Wirtschaft abgedeckt werden können sollte, weil entsprechende Praktikumsbescheinigungen keinen Qualitätskontrollen genügen können und somit ausgestellt werden können, ohne das ein Student entsprechende praktische Erfahrung gesammelt hat...	2017-02-03 13:10:33.589619
\.


--
-- Name: rss_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('rss_uid_seq', 118, true);


--
-- Data for Name: seen_arguments; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY seen_arguments (uid, argument_uid, user_uid) FROM stdin;
1	2	4
2	3	6
3	4	5
4	5	4
5	4	4
6	2	5
7	5	5
8	3	7
9	6	7
10	4	8
11	4	3
12	3	9
13	6	9
14	7	9
15	7	3
16	7	7
17	6	3
18	3	3
19	8	10
20	7	10
21	7	11
22	9	11
23	3	11
24	6	11
25	7	4
26	3	4
27	6	4
28	8	4
29	10	12
30	10	4
31	11	12
32	4	12
33	1	12
34	12	12
35	5	12
36	13	12
37	1	13
38	15	14
39	2	14
40	5	14
41	15	12
42	3	12
43	6	12
44	16	14
45	7	12
46	8	12
47	18	14
48	6	14
49	7	14
50	19	14
51	7	6
52	19	6
53	17	14
54	22	14
55	23	13
56	24	14
57	1	14
58	25	12
59	26	13
60	2	13
61	2	11
62	5	11
63	16	11
64	17	11
65	22	11
66	3	13
67	6	13
68	1	6
69	23	6
70	27	12
71	21	12
72	28	11
73	1	11
74	2	10
75	5	10
76	16	10
77	17	10
78	22	10
79	28	10
80	29	6
81	30	13
82	19	13
83	1	10
84	18	10
85	29	13
86	31	13
87	23	11
88	29	12
89	31	12
90	32	13
91	7	13
92	33	14
93	30	14
94	3	10
95	6	10
96	32	10
97	19	10
98	34	13
99	35	14
100	35	11
101	36	11
102	36	12
103	37	11
104	38	13
105	10	13
106	39	13
107	40	13
108	4	13
109	11	13
110	33	13
111	15	13
112	42	13
113	41	13
114	43	14
115	37	14
116	21	4
117	36	6
118	41	12
119	42	12
120	44	12
121	45	4
122	46	12
123	45	5
124	41	5
125	36	5
126	47	5
127	10	5
128	47	12
129	7	5
130	19	5
131	48	13
132	46	13
133	30	5
134	49	13
135	50	13
136	15	4
137	2	16
138	5	16
139	16	16
140	17	16
141	22	16
142	28	16
143	41	16
144	45	16
145	49	16
146	15	16
147	58	16
148	59	16
149	60	16
150	3	16
151	6	16
152	32	16
153	19	16
154	30	16
155	36	7
156	35	7
157	37	7
158	43	7
159	49	4
160	50	4
161	32	7
162	61	7
163	58	4
164	36	4
165	62	6
166	35	6
167	62	5
168	35	5
169	63	5
170	1	4
171	23	4
172	36	3
173	62	3
174	2	3
175	5	3
176	16	3
177	17	3
178	22	3
179	28	3
180	64	13
181	65	13
182	1	5
183	23	5
184	16	5
185	17	5
186	22	5
187	28	5
188	1	3
189	23	3
190	66	13
191	2	18
192	5	18
193	16	18
194	17	18
195	22	18
196	28	18
197	68	18
198	23	18
199	1	18
200	36	19
201	62	19
202	15	19
203	58	19
204	29	19
205	31	19
206	64	19
207	15	8
208	58	8
209	1	8
210	61	8
211	64	8
212	42	8
213	36	8
214	32	3
215	61	3
216	1	9
217	23	9
218	35	9
219	69	9
220	67	13
221	58	13
222	46	20
223	45	20
224	15	21
225	58	21
226	70	21
227	45	21
228	71	21
229	59	21
230	72	21
231	73	21
232	15	3
233	58	3
234	70	3
235	73	3
236	1	1
237	2	1
238	3	1
239	4	1
240	5	1
241	6	1
242	7	1
243	8	1
244	9	1
245	10	1
246	11	1
247	12	1
248	13	1
249	14	1
250	15	1
251	16	1
252	17	1
253	18	1
254	19	1
255	20	1
256	21	1
257	22	1
258	23	1
259	24	1
260	25	1
261	26	1
262	27	1
263	28	1
264	29	1
265	30	1
266	31	1
267	32	1
268	33	1
269	34	1
270	35	1
271	36	1
272	37	1
273	38	1
274	39	1
275	40	1
276	41	1
277	42	1
278	43	1
279	44	1
280	45	1
281	46	1
282	47	1
283	48	1
284	49	1
285	50	1
286	51	1
287	52	1
288	53	1
289	54	1
290	55	1
291	56	1
292	57	1
293	58	1
294	59	1
295	60	1
296	61	1
297	62	1
298	63	1
299	64	1
300	65	1
301	66	1
302	67	1
303	68	1
304	69	1
305	70	1
306	71	1
307	72	1
308	73	1
309	74	1
310	75	1
311	76	1
312	77	1
313	78	1
314	81	1
315	83	1
316	84	1
317	85	1
318	88	1
319	89	1
320	90	1
321	92	1
322	93	1
323	94	1
324	96	1
325	97	1
326	99	1
327	100	1
328	101	1
329	102	1
330	103	1
331	105	1
332	107	1
333	108	1
334	109	1
335	112	1
336	113	1
337	114	1
338	115	1
339	117	1
340	119	1
341	120	1
342	122	1
343	123	1
344	124	1
345	127	1
346	128	1
347	129	1
348	130	1
349	131	1
350	132	1
351	79	1
352	80	1
353	82	1
354	86	1
355	87	1
356	91	1
357	95	1
358	98	1
359	104	1
360	106	1
361	110	1
362	111	1
363	116	1
364	118	1
365	121	1
366	125	1
367	126	1
\.


--
-- Name: seen_arguments_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('seen_arguments_uid_seq', 367, true);


--
-- Data for Name: seen_statements; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY seen_statements (uid, statement_uid, user_uid) FROM stdin;
1	1	5
2	1	4
3	3	4
4	1	6
5	4	6
6	6	5
7	4	4
8	6	4
9	7	4
10	4	5
11	3	5
12	8	5
13	1	7
14	4	7
15	6	7
16	5	7
17	1	8
18	4	8
19	6	8
20	7	8
21	1	3
22	4	3
23	6	3
24	7	3
25	1	9
26	4	9
27	6	9
28	5	9
29	9	9
30	10	9
31	11	9
32	11	3
33	9	7
34	10	7
35	5	3
36	9	3
37	10	3
38	11	7
39	11	11
40	4	11
41	1	10
42	4	10
43	6	10
44	1	11
45	6	11
46	5	11
47	9	11
48	10	11
49	11	4
50	5	4
51	9	4
52	10	4
53	6	12
54	14	4
55	1	12
56	4	12
57	2	12
58	1	14
59	4	14
60	6	14
61	1	13
62	4	13
63	6	13
64	19	14
65	2	13
66	3	14
67	8	14
68	19	12
69	20	12
70	21	14
71	22	14
72	5	12
73	9	12
74	10	12
75	11	12
76	19	4
77	9	14
78	10	14
79	11	14
80	25	4
81	26	4
82	11	6
83	24	6
84	28	13
85	19	13
86	19	10
87	3	11
88	8	11
89	21	11
90	22	11
91	27	11
92	5	13
93	9	13
94	10	13
95	6	6
96	19	6
97	2	6
98	28	6
99	2	11
100	3	10
101	8	10
102	21	10
103	22	10
104	27	10
105	33	10
106	34	6
107	34	13
108	2	10
109	31	13
110	19	11
111	34	11
112	34	12
113	28	11
114	31	12
115	35	12
116	34	4
117	33	11
118	37	11
119	11	13
120	34	10
121	37	10
122	5	10
123	9	10
124	10	10
125	36	10
126	34	14
127	37	14
128	37	13
129	37	12
130	40	11
131	41	11
132	42	12
133	37	4
134	38	13
135	14	13
136	7	13
137	20	13
138	48	13
139	49	13
140	50	13
141	48	4
142	48	11
143	19	3
144	34	3
145	37	3
146	48	3
147	48	6
148	37	6
149	42	6
150	48	12
151	49	12
152	50	12
153	48	10
154	19	5
155	34	5
156	48	5
157	37	5
158	54	5
159	49	5
160	42	5
161	7	5
162	11	5
163	24	5
164	1	15
165	4	15
166	6	15
167	19	15
168	34	15
169	48	15
170	37	15
171	27	5
172	20	4
173	1	16
174	4	16
175	6	16
176	19	16
177	34	16
178	48	16
179	37	16
180	3	16
181	8	16
182	21	16
183	22	16
184	27	16
185	33	16
186	62	16
187	63	16
188	64	16
189	49	16
190	54	16
191	20	16
192	68	16
193	5	16
194	9	16
195	10	16
196	36	16
201	42	7
203	54	4
204	58	4
205	59	4
206	60	4
207	61	4
208	36	7
197	19	7
198	34	7
199	48	7
200	37	7
202	43	7
209	68	4
210	42	4
211	1	17
212	4	17
213	6	17
214	19	17
215	34	17
216	48	17
217	37	17
218	73	5
219	40	5
220	41	5
221	2	4
222	28	4
223	42	3
224	73	3
225	3	3
226	8	3
227	21	3
228	22	3
229	27	3
230	33	3
231	35	13
232	55	13
233	77	13
234	78	13
235	79	13
236	77	3
237	77	5
238	2	5
239	28	5
240	21	5
241	22	5
242	33	5
243	2	3
244	28	3
245	77	4
246	1	18
247	4	18
248	6	18
249	19	18
250	34	18
251	48	18
252	37	18
253	77	18
254	3	18
255	8	18
256	21	18
257	22	18
258	27	18
259	33	18
260	2	18
261	28	18
262	19	9
263	34	9
264	48	9
265	37	9
266	77	9
267	77	15
268	1	19
269	4	19
270	6	19
271	19	19
272	34	19
273	48	19
274	37	19
275	77	19
276	42	19
277	73	19
278	20	19
279	68	19
280	31	19
281	35	19
282	75	19
283	19	8
284	34	8
285	48	8
286	37	8
287	77	8
288	20	8
289	68	8
290	2	8
291	71	8
292	72	8
293	75	8
294	50	8
295	42	8
296	36	3
297	71	3
298	72	3
299	2	9
300	28	9
301	40	9
302	41	9
303	68	13
304	55	20
305	48	20
306	1	20
307	4	20
308	6	20
309	19	20
310	34	20
311	37	20
312	77	20
313	54	20
314	1	21
315	4	21
316	6	21
317	19	21
318	34	21
319	48	21
320	37	21
321	77	21
322	20	21
323	68	21
324	82	21
325	54	21
326	83	21
327	69	21
328	84	21
329	20	3
330	68	3
331	82	3
332	85	3
333	86	3
334	1	1
335	2	1
336	3	1
337	4	1
338	5	1
339	6	1
340	7	1
341	8	1
342	9	1
343	10	1
344	11	1
345	12	1
346	13	1
347	14	1
348	15	1
349	16	1
350	17	1
351	18	1
352	19	1
353	20	1
354	21	1
355	22	1
356	23	1
357	24	1
358	25	1
359	26	1
360	27	1
361	29	1
362	30	1
363	31	1
364	32	1
365	33	1
366	34	1
367	35	1
368	36	1
369	38	1
370	39	1
371	40	1
372	41	1
373	42	1
374	43	1
375	44	1
376	45	1
377	46	1
378	47	1
379	48	1
380	49	1
381	50	1
382	51	1
383	52	1
384	28	1
385	37	1
386	53	1
387	54	1
388	55	1
389	56	1
390	57	1
391	58	1
392	59	1
393	60	1
394	61	1
395	62	1
396	63	1
397	64	1
398	65	1
399	66	1
400	67	1
401	68	1
402	69	1
403	70	1
404	71	1
405	72	1
406	73	1
407	74	1
408	75	1
409	76	1
410	77	1
411	78	1
412	79	1
413	80	1
414	81	1
415	82	1
416	83	1
417	84	1
418	85	1
419	86	1
420	87	1
421	88	1
422	89	1
423	90	1
424	91	1
425	92	1
426	93	1
427	94	1
428	95	1
429	96	1
430	97	1
431	98	1
432	99	1
433	100	1
434	101	1
435	102	1
436	103	1
437	104	1
438	105	1
439	106	1
440	107	1
441	108	1
442	109	1
443	110	1
444	111	1
445	112	1
446	113	1
447	114	1
448	115	1
449	116	1
450	117	1
451	118	1
452	119	1
453	120	1
454	121	1
455	122	1
456	123	1
457	124	1
458	125	1
459	126	1
460	127	1
461	128	1
462	129	1
463	130	1
464	131	1
465	132	1
466	133	1
467	134	1
468	135	1
469	136	1
470	137	1
471	138	1
472	139	1
473	140	1
474	141	1
475	142	1
476	143	1
477	144	1
478	145	1
479	146	1
480	147	1
481	148	1
482	149	1
483	150	1
484	151	1
485	152	1
486	153	1
487	154	1
\.


--
-- Name: seen_statements_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('seen_statements_uid_seq', 487, true);


--
-- Data for Name: settings; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY settings (author_uid, should_send_mails, should_send_notifications, should_show_public_nickname, last_topic_uid, lang_uid, keep_logged_in) FROM stdin;
1	f	t	t	1	2	f
2	f	t	t	1	2	f
3	f	t	t	1	2	f
5	t	t	t	1	2	f
6	t	t	t	1	2	f
7	t	t	t	1	2	f
8	t	t	t	1	2	f
9	t	t	t	1	2	f
10	t	t	t	1	2	t
11	t	t	t	1	2	f
12	t	t	t	1	2	t
4	f	t	t	1	2	t
14	t	t	t	1	2	f
13	t	t	t	1	2	f
15	f	t	t	1	2	f
16	t	t	t	1	2	f
17	f	t	t	1	2	f
18	f	t	t	1	2	f
19	f	t	t	1	2	f
20	f	t	t	1	2	f
21	f	t	t	1	2	f
\.


--
-- Data for Name: statement_references; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY statement_references (uid, reference, host, path, author_uid, statement_uid, issue_uid, created) FROM stdin;
1	In anderen Fächern übersteigt das Interesse bei den Abiturientinnen und Abiturienten das Angebot an Studienplätzen, in manchen Fällen um ein Vielfaches.	http://www.faz.net/	aktuell/beruf-chance/campus/pro-und-contra-brauchen-wir-den-numerus-clausus-13717801.html	3	2	1	2017-01-26 17:08:49
2	Kern der Kritik am Numerus clausus ist seit jeher die mangelnde Vergleichbarkeit des Abiturschnitts	http://www.faz.net/	aktuell/beruf-chance/campus/pro-und-contra-brauchen-wir-den-numerus-clausus-13717801.html	3	3	1	2017-01-26 17:08:49
\.


--
-- Name: statement_references_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('statement_references_uid_seq', 2, true);


--
-- Data for Name: statements; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY statements (uid, textversion_uid, is_startpoint, issue_uid, is_disabled) FROM stdin;
1	1	t	1	f
2	2	f	1	f
3	3	f	1	f
4	4	t	1	f
5	5	f	1	f
6	6	t	1	f
7	7	f	1	f
8	8	f	1	f
9	9	f	1	f
10	10	f	1	f
11	11	f	1	f
12	12	f	1	f
13	13	f	1	f
14	14	f	1	f
15	15	f	1	f
16	16	f	1	f
17	17	f	1	f
18	18	f	1	f
19	19	t	1	f
20	20	f	1	f
21	21	f	1	f
22	22	f	1	f
23	23	f	1	f
24	24	f	1	f
25	25	f	1	f
26	26	f	1	f
27	27	f	1	f
29	29	f	1	f
30	30	f	1	f
31	31	f	1	f
32	32	f	1	f
33	33	f	1	f
34	34	t	1	f
35	35	f	1	f
36	36	f	1	f
38	38	f	1	f
39	39	f	1	f
40	40	f	1	f
41	41	f	1	f
42	42	f	1	f
43	43	f	1	f
44	44	f	1	f
45	45	f	1	f
46	46	f	1	f
47	47	f	1	f
48	48	t	1	f
49	49	f	1	f
50	50	f	1	f
51	51	f	1	f
52	52	f	1	f
28	53	f	1	f
37	54	t	1	f
53	55	f	1	f
54	56	f	1	f
55	57	f	1	f
56	58	f	1	f
57	59	f	1	f
58	60	f	1	f
59	61	f	1	f
60	62	f	1	f
61	63	f	1	f
62	64	f	1	f
63	65	f	1	f
64	66	f	1	f
65	67	f	1	f
66	68	f	1	f
67	69	f	1	f
68	70	f	1	f
69	71	f	1	f
70	72	f	1	f
71	73	f	1	f
72	74	f	1	f
73	75	f	1	f
74	76	f	1	f
75	77	f	1	f
76	78	f	1	f
77	79	t	1	f
78	80	f	1	f
79	81	f	1	f
80	82	f	1	f
81	83	f	1	f
82	84	f	1	f
83	85	f	1	f
84	86	f	1	f
85	87	f	1	f
86	88	f	1	f
87	156	t	3	t
88	89	t	3	f
89	90	t	3	f
90	91	t	3	f
91	92	f	3	f
92	93	f	3	f
93	94	f	3	f
94	95	f	3	f
95	96	f	3	f
96	97	f	3	f
97	98	f	3	f
98	99	f	3	f
99	100	f	3	f
100	101	f	3	f
101	102	f	3	f
102	103	f	3	f
103	104	f	3	f
104	105	f	3	f
105	106	f	3	f
106	107	f	3	f
107	108	f	3	f
108	109	f	3	f
109	110	f	3	f
110	111	f	3	f
111	112	f	3	f
112	113	f	3	f
113	114	f	3	f
114	115	f	3	f
115	116	f	3	f
116	117	f	3	f
117	118	f	3	f
118	119	f	3	f
119	120	f	3	f
120	121	f	3	f
121	122	f	3	f
122	123	t	2	f
123	124	t	2	f
124	125	t	2	f
125	126	f	2	f
126	127	f	2	f
127	128	f	2	f
128	129	f	2	f
129	130	f	2	f
130	131	f	2	f
131	132	f	2	f
132	133	f	2	f
133	134	f	2	f
134	135	f	2	f
135	136	f	2	f
136	137	f	2	f
137	138	f	2	f
138	139	f	2	f
139	140	f	2	f
140	141	f	2	f
141	142	f	2	f
142	143	f	2	f
143	144	f	2	f
144	145	t	4	f
145	146	f	4	f
146	147	f	4	f
147	148	f	4	f
148	149	f	4	f
149	150	f	4	f
150	151	f	4	f
151	152	f	4	f
152	153	f	4	f
153	154	t	4	f
154	155	f	4	f
\.


--
-- Name: statements_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('statements_uid_seq', 154, true);


--
-- Data for Name: textversions; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY textversions (uid, statement_uid, content, author_uid, "timestamp", is_disabled) FROM stdin;
10	10	zu einem guten Ruf der Universität beitragen.	7	2017-02-11 10:05:04.794475	f
1	1	eine Zulassungsbeschränkung eingeführt werden soll	3	2017-01-31 10:05:04.793924	f
2	2	die Nachfrage nach dem Fach zu groß ist, sodass eine Beschränkung eingeführt werden muss	3	2017-02-12 10:05:04.794068	f
3	3	die Vergleichbarkeit des Abiturschnitts nicht gegeben ist	3	2017-02-07 10:05:04.794135	f
4	4	das Anforderungsniveau des Studiums erhöht werden sollte.	6	2017-02-09 10:05:04.794191	f
5	5	die Studierendenzahlen durch ein hohes Anforderungsniveau auf natürliche Weise gesenkt werden können.	6	2017-02-14 10:05:04.794242	f
6	6	Grundmodule mehrere Termine haben sollten, um die Anzahl der Studierenden pro Veranstaltung zu reduzieren.	5	2017-01-27 10:05:04.79429	f
7	7	Veranstaltungen mit weniger Teilnehmern angenehmer sind.	5	2017-01-30 10:05:04.794338	f
8	8	man lieber die Kapazitäten der Universität aufstocken sollte anstatt neue Studierende vom Studium auszuschließen.	4	2017-02-11 10:05:04.794383	f
9	9	die Studierenden einen fachlich höheren Abschluss erlangen.	7	2017-01-28 10:05:04.794429	f
11	11	bereits jetzt viele Studenten das Studium abbrechen.	9	2017-01-25 10:05:04.794521	f
12	12	ein Großteil der Studenten aufgrund gesellschaftlicher Vorgaben (u.a. Eltern, die Abitur/Studium vorgeben) studieren. Hier sollte Qualität vor Quantität der Ausbildung gehen.	10	2017-02-06 10:05:04.794565	f
13	13	Viele Studenten wissen nach dem Abitur nicht, welche Karriereweg sie einschlagen möchten. Oft merken sie erst im Studium, dass es ihnen nicht liegt.	11	2017-02-09 10:05:04.794609	f
14	14	die Termine sich von der Qualität stark unterscheiden können, insbesondere wenn diese von verschiedenen Lehrkräften gehalten werden. Das sorgt für Ungleichheit der Lehre.	12	2017-02-03 10:05:04.794653	f
15	15	das einen erheblichen Mehraufwand an Arbeit bedeutet, der in keiner Relation zu den Vorteilen steht.	12	2017-01-30 10:05:04.794697	f
16	16	es aktuell nicht einfach ist, mehr Geld pro Studierenden so zu verteilen, dass es eine bessere Raum- und Betreuungssituation ergibt.	12	2017-01-28 10:05:04.794785	f
17	17	es aktuell nicht einfach ist, mehr Geld pro Studierenden so zu verteilen, dass es eine bessere Raum- und Betreuungssituation ergibt.	12	2017-01-22 10:05:04.794829	f
18	18	es aktuell nicht einfach ist, mehr Geld pro Studierenden so zu verteilen, dass es eine bessere Raum- und Betreuungssituation ergibt.	12	2017-02-11 10:05:04.794741	f
19	19	mehr Lehrpersonal angestellt werden müsste: Professoren, Doktoranden, Hilfskräfte.	14	2017-02-03 10:05:04.794872	f
20	20	Ein höheres Betreuungsverhältnis fördert den Lernerfolg.	14	2017-01-25 10:05:04.794917	f
21	21	man nur Rheinbahnstudenten abschrecken würde, die auch jetzt nicht zu den Vorlesungen kommen.	14	2017-02-09 10:05:04.794962	f
22	22	Weniger angemeldete Studenten auch weniger Geld für die Betreuung der tatsächlich studierenden bedeuten würde.	14	2017-02-09 10:05:04.795005	f
23	23	das kein Argument ist. Warum muss zu einer hohen Nachfrage automatisch das Angebot beschränkt werden?	14	2017-02-07 10:05:04.795049	f
24	24	man nicht die Abbrecherquote erhöhen sollte, sondern die Anzahl der weniger begabten Erstsemestler.	14	2017-01-30 10:05:04.795092	f
25	25	das vernachlässigbar ist, da die Vorlesungsmaterialien die selben sind.	4	2017-01-22 10:05:04.795136	f
26	26	das vernachlässigbar ist, da die Skills der Dozenten sich nicht allzu sehr unterscheiden sollten in den Grundlagenveranstaltungen.	4	2017-01-25 10:05:04.795179	f
27	27	weil es Montags immer Brötchen in der Mensa gibt.	14	2017-02-11 10:05:04.795223	f
28	28	Viele Studierende sich anmelden, ohne genau zu wissen was es braucht um dieses Fach zu studieren. Ein Vortest wäre sinnvoll.	13	2017-02-13 10:05:04.795267	f
29	29	nicht die die Nachfrage künstlich verknappt werden sollte, sondern das Angebot, d.h. Uni-Ressourcen, erweitert werden sollten.	14	2017-02-14 10:05:04.795312	f
30	30	eine Beschränkung nicht zwingend die Nachfrage nach dem Studiengang senkt, sondern nur die Anzahl der tatsächlich studierenden pro Semester. Siehe Medizin und deren Wartelisten als Beispiel.	12	2017-02-13 10:05:04.795356	f
31	31	Eine Zulassungsbeschränkung auch über einen Vortest geregelt werden kann, statt über den Abiturschnitt.	13	2017-01-30 10:05:04.7954	f
32	32	auch Fragen und Mitarbeit der Studierenden, welche wichtige Aha-Momente für die Mithörer im Raum auslösen, zwischen den Terminen variieren.	12	2017-02-15 10:05:04.795444	f
33	33	Eine Abiturnote sagt nichts über die Fähigkeiten im Studienfach aus. Bsp.: Medizin benötigt kein Vorwissen.	11	2017-01-28 10:05:04.795488	f
34	34	man die für den Informatikstudiengang ungeeigneten Studierenden durch einen Vortest &quot;aussortieren&quot; sollte.	6	2017-02-09 10:05:04.795532	f
35	35	Einen Vortest einzuführen dazu beitragen würde, dass das Anforderungsniveau erhöht wird, aber nicht die Abbrecherquote.	13	2017-02-03 10:05:04.795577	f
36	36	um international mithalten zu können wir nicht um eine Erhöhung des Anforderungsniveaus herumkommen.	13	2017-02-13 10:05:04.795622	f
37	37	Eine Zulassungsbeschräeinnkung auch über einen Vortest geregelt werden kann, statt über den Abiturschnitt.	11	2017-02-14 10:05:04.795667	f
38	38	sie mir ja zustimmen. Ein Vortest filtert die schlechten Erstis raus, hat aber keinen Einfluss auf das Niveau des Studiums.	14	2017-01-28 10:05:04.795711	f
39	39	wir das Ausbildungsniveau nicht deshalb absenken sollten, nur weil es viele Abbrecher gibt in einem bis dato zulassungsfreien Studiengang.	13	2017-01-28 10:05:04.795754	f
40	40	Jede Aussage mit &quot;kann&quot; ist richtig, ich fände das aber falsch, da ein Vortest enormen Aufwand für das Lehrpersonal bedeutet, die Ihre Zeit von der eigentliche Lehre abziehen müssten.	14	2017-02-13 10:05:04.795797	f
41	41	es so zu einer schlechteren Lehre führt.	14	2017-02-11 10:05:04.795841	f
42	42	der Vortest kann auf das Fach abgestimmt werden.	11	2017-01-24 10:05:04.795884	f
43	43	man statt Vortest auch andere Qualifikationen prüfen könnte. Bsp. Medizin: hat ein(e) Student(in) bereits Erfahrung, z.B. durch Beruf, Zivildienst, freiwilliges soziales Jahr.	11	2017-01-23 10:05:04.795928	f
44	44	ein Vortest dazu führt, dass mehr begabte Studierende eingeschrieben sind.	13	2017-02-04 10:05:04.795994	f
45	45	somit die Kurse anspruchvoller gestaltet werden können.	13	2017-01-21 10:05:04.796075	f
46	46	Selbst in Grundveranstaltungen die Lehrkräfte in ihren Kursen auf verschiedene inhaltliche Dinge Wert legen.	13	2017-02-06 10:05:04.796126	f
47	47	Lehrkräfte somit unnötig doppelt belastet werden, wenn man bedenkt, dass viele der Studierenden sowieso abbrechen werden.	13	2017-02-06 10:05:04.796259	f
48	48	Die Unterrichtssprache des Informatik-Studiums Englisch sein sollte.	13	2017-01-29 10:05:04.796171	f
49	49	das Studium so internationaler wäre.	13	2017-01-27 10:05:04.796215	f
50	50	Fachbegriffe sowieso auf Englisch sind.	13	2017-02-07 10:05:04.796392	f
51	51	fast alle Anfänger direkt nach dem Abi ihr Studium beginnen.	14	2017-02-12 10:05:04.796303	f
52	52	man für diese 90% dennoch einen aufwändigen Vortest durchführen müsste.	14	2017-02-07 10:05:04.796348	f
53	28	Viele Studierende sich anmelden, ohne genau zu wissen was es braucht um dieses Fach zu studieren	13	2017-02-05 10:05:04.796435	f
54	37	Eine Zulassungsbeschränkung auch über einen Vortest geregelt werden kann, statt über den Abiturschnitt	5	2017-02-15 10:05:04.796478	f
55	53	es Informatiker (in der Wissenschaft als auch in der Industrie) einen enormen Vorteil bietet die de facto lingua franca der Branche sehr gut zu beherrschen.	12	2017-02-13 10:05:04.796522	f
56	54	das nur Sinn ergibt, wenn man in die Wissenschaft geht, was aber nicht bei jedem Bachelorstudenten gegeben ist.	4	2017-02-04 10:05:04.796566	f
57	55	zu einem international hervorragenden Studium mehr dazu gehört als nur die Studiumssprache auf Englisch zu haben.	12	2017-02-10 10:05:04.796609	f
58	56	die Vorteile einer besseren Arbeitsumgebung, die möglichen Nachteile der Ungleichheit überwiegen.	5	2017-01-22 10:05:04.796652	f
59	57	Es schonmal ein erster Schritt ist, um ein das Studium internationaler zu machen.	13	2017-01-24 10:05:04.796696	f
60	58	Auch in der Wirtschaft.	13	2017-01-30 10:05:04.796738	f
61	59	anderen Bereichen sind Fachbegriffe.	13	2017-02-07 10:05:04.796781	f
62	60	Terminologie auf Englisch.	13	2017-01-27 10:05:04.796824	f
63	61	Auch in der Wirtschaft und anderen Bereichen sind Fachbegriffe und Terminologie auf Englisch.	13	2017-02-11 10:05:04.796866	f
64	62	Mehr Räume kann man notfalls durch Container kurzfristig schaffen.	16	2017-02-03 10:05:04.79691	f
65	63	freie Seminarräume gibt&#x27;s z.B. im Neubau.	16	2017-02-05 10:05:04.796957	f
66	64	Gute und Hiwi-willige Studierende sollten proportional zur Anzahl der Gesamtstudierenden sein.	16	2017-02-14 10:05:04.797003	f
67	65	innerhalb der Uni finden sich sicher noch ungenutzte Kapazitäten - unsere Seminarräume sind ja keineswegs nahe 100% ausgebucht. Gute.	16	2017-01-25 10:05:04.797048	f
68	66	t. Gute und Hiwi-willige Studierende sollten proportional zur Anzahl der Gesamtstudierenden sein.	16	2017-01-22 10:05:04.797091	f
69	67	Hiwi-willige Studierende sollten proportional zur Anzahl der Gesamtstudierenden sein.	16	2017-02-04 10:05:04.797134	f
70	68	Mehr Studierende erfordern mehr Leerpersonal.	16	2017-02-14 10:05:04.79718	f
71	69	es ist unklar was man überhaupt testen könnte, ohne gleich Inhalte des ersten Semesters zu verlangen.	16	2017-01-23 10:05:04.797225	f
72	70	der Vortest würde die Inhalte des ersten Semesters verlangen, anstatt die generelle Lernwilligkeit.	16	2017-01-23 10:05:04.797269	f
73	71	die Studierenden eine fachlich angemessenere Ausbildung erlangen.	7	2017-01-30 10:05:04.797313	f
74	72	auf dem Arbeitsmarkt damit eine bessere Stellung erhalten.	7	2017-01-21 10:05:04.797355	f
75	73	ein Vortest die fachspezifische Eignung sicherstellt anstatt allgemein guter Leistung.	6	2017-01-30 10:05:04.797412	f
76	74	ein Vortest auch maschinell erfolgen kann.	5	2017-01-31 10:05:04.79746	f
77	75	so die Anzahl an &quot;Rheinbahnstudenten&quot; vermutlich verringert werden würde.	13	2017-01-31 10:05:04.797505	f
78	76	Es genügend Beispiele von Vortests gibt, die allgemeines logisches Verständnis prüfen, ohne gelerntes Wissen abzufragen.	13	2017-01-23 10:05:04.797549	f
79	77	im Curriculum verankerte praktische Übungskurse auch durch Praktikas in der Wirtschaft abgedeckt werden können sollte.	13	2017-01-23 10:05:04.797593	f
80	78	so die Wirtschaft stärker mit der Universität vernetzt werden würde.	13	2017-02-06 10:05:04.797637	f
81	79	so die Lehrkräfte entlastet werden durch weniger Übungsbetrieb.	13	2017-01-23 10:05:04.79768	f
82	80	Studis sollen aber auch ruhig mal n wenig ausprobieren können	18	2017-01-23 10:05:04.797724	f
83	81	es viele Fähigkeiten, wie z.B. logisches Denken gibt, die (noch) nicht automatisiert geprüft werden können	9	2017-02-04 10:05:04.797771	f
84	82	dadurch noch mehr Vorlesungen angeboten werden können	21	2017-02-08 10:05:04.797826	f
85	83	es im Bachelorstudiengang die meisten Studierenden überfordern würde	21	2017-02-13 10:05:04.797873	f
86	84	das eventuell Studenten ausfiltert, die unter Einsatz von Fleiß doch zu geeigneten Studenten werden	21	2017-02-03 10:05:04.797917	f
87	85	entsprechende Praktikumsbescheinigungen keinen Qualitätskontrollen genügen können	21	2017-02-06 10:05:04.797961	f
88	86	somit ausgestellt werden können, ohne das ein Student entsprechende praktische Erfahrung gesammelt hat	21	2017-01-25 10:05:04.798004	f
89	88	we should get a cat	1	2017-02-06 10:05:04.798051	f
90	89	we should get a dog	1	2017-02-12 10:05:04.798097	f
91	90	we could get both, a cat and a dog	1	2017-02-05 10:05:04.798142	f
92	91	cats are very independent	1	2017-01-24 10:05:04.798187	f
93	92	cats are capricious	1	2017-02-04 10:05:04.798231	f
94	93	dogs can act as watch dogs	1	2017-02-06 10:05:04.798275	f
95	94	you have to take the dog for a walk every day, which is tedious	1	2017-02-02 10:05:04.798319	f
96	95	we have no use for a watch dog	1	2017-02-05 10:05:04.798363	f
97	96	going for a walk with the dog every day is good for social interaction and physical exercise	1	2017-02-04 10:05:04.798407	f
98	97	it would be no problem	1	2017-01-30 10:05:04.798451	f
99	98	a cat and a dog will generally not get along well	1	2017-02-13 10:05:04.798494	f
100	99	we do not have enough money for two pets	1	2017-02-08 10:05:04.798538	f
101	100	a dog costs taxes and will be more expensive than a cat	1	2017-02-14 10:05:04.798581	f
102	101	cats are fluffy	1	2017-01-21 10:05:04.798625	f
103	102	cats are small	1	2017-01-31 10:05:04.79867	f
104	103	fluffy animals losing much hair and I'm allergic to animal hair	1	2017-02-10 10:05:04.798714	f
105	104	you could use a automatic vacuum cleaner	1	2017-02-15 10:05:04.798758	f
106	105	cats ancestors are animals in wildlife, who are hunting alone and not in groups	1	2017-02-06 10:05:04.798802	f
107	106	this is not true for overbred races	1	2017-02-07 10:05:04.798846	f
108	107	this lies in their the natural conditions	1	2017-02-14 10:05:04.79889	f
109	108	the purpose of a pet is to have something to take care of	1	2017-01-31 10:05:04.798935	f
110	109	several cats of friends of mine are real as*holes	1	2017-02-14 10:05:04.798978	f
111	110	the fact, that cats are capricious, is based on the cats race	1	2017-01-23 10:05:04.799022	f
112	111	not every cat is capricious	1	2017-01-23 10:05:04.799066	f
113	112	this is based on the cats race and a little bit on the breeding	1	2017-02-09 10:05:04.79911	f
114	113	next to the taxes you will need equipment like a dog lead, anti-flea-spray, and so on	1	2017-02-06 10:05:04.799153	f
115	114	the equipment for running costs of cats and dogs are nearly the same	1	2017-01-21 10:05:04.799196	f
116	115	this is just a claim without any justification	1	2017-02-15 10:05:04.79924	f
117	116	in Germany you have to pay for your second dog even more taxes!	1	2017-02-09 10:05:04.799284	f
118	117	it is important, that pets are small and fluffy!	1	2017-01-31 10:05:04.799328	f
119	118	cats are little, sweet and innocent cuddle toys	1	2017-01-22 10:05:04.799371	f
120	119	do you have ever seen a sphinx cat or savannah cats?	1	2017-01-24 10:05:04.799415	f
121	120	it is much work to take care of both animals	1	2017-01-21 10:05:04.799458	f
122	121	won't be best friends	1	2017-01-29 10:05:04.799502	f
123	122	the city should reduce the number of street festivals	3	2017-02-11 10:05:04.799546	f
124	123	we should shut down University Park	3	2017-01-29 10:05:04.79959	f
125	124	we should close public swimming pools	1	2017-02-14 10:05:04.799633	f
126	125	reducing the number of street festivals can save up to $50.000 a year	1	2017-02-03 10:05:04.799678	f
127	126	every street festival is funded by large companies	1	2017-01-21 10:05:04.799721	f
128	127	then we will have more money to expand out pedestrian zone	1	2017-01-30 10:05:04.799765	f
129	128	our city will get more attractive for shopping	1	2017-01-30 10:05:04.799808	f
130	129	street festivals attract many people, which will increase the citys income	1	2017-02-04 10:05:04.799852	f
131	130	spending of the city for these festivals are higher than the earnings	1	2017-02-04 10:05:04.799896	f
132	131	money does not solve problems of our society	1	2017-02-01 10:05:04.799939	f
133	132	criminals use University Park to sell drugs	1	2017-02-12 10:05:04.799983	f
134	133	shutting down University Park will save $100.000 a year	1	2017-02-10 10:05:04.800027	f
135	134	we should not give in to criminals	1	2017-02-13 10:05:04.80007	f
136	135	the number of police patrols has been increased recently	1	2017-01-27 10:05:04.800114	f
137	136	this is the only park in our city	1	2017-02-04 10:05:04.800158	f
138	137	there are many parks in neighbouring towns	1	2017-02-08 10:05:04.800201	f
139	138	the city is planing a new park in the upcoming month	3	2017-02-02 10:05:04.800245	f
140	139	parks are very important for our climate	3	2017-01-27 10:05:04.800293	f
141	140	our swimming pools are very old and it would take a major investment to repair them	3	2017-01-25 10:05:04.800338	f
142	141	schools need the swimming pools for their sports lessons	1	2017-02-10 10:05:04.800382	f
143	142	the rate of non-swimmers is too high	1	2017-02-02 10:05:04.800426	f
144	143	the police cannot patrol in the park for 24/7	1	2017-02-03 10:05:04.800475	f
145	144	E-Autos "optimal" für den Stadtverkehr sind	1	2017-01-21 10:05:04.800519	f
146	145	dadurch die Lärmbelästigung in der Stadt sinkt	1	2017-01-21 10:05:04.800563	f
147	146	die Anzahl an Ladestationen in der Stadt nicht ausreichend ist	1	2017-02-12 10:05:04.800606	f
148	147	das Unfallrisiko steigt, da die Autos kaum Geräusche verursachen	1	2017-02-05 10:05:04.80065	f
149	148	die Autos auch zuhause geladen werden können und das pro Tag ausreichen sollte	1	2017-02-09 10:05:04.800693	f
150	149	Elektroautos keine lauten Geräusche beim Anfahren produzieren	1	2017-02-10 10:05:04.800737	f
151	150	Lärmbelästigung kein wirkliches Problem in den Städten ist	1	2017-02-04 10:05:04.800839	f
152	151	nicht jede normale Tankstelle auch Stromtankstellen hat	1	2017-02-14 10:05:04.800886	f
153	152	die Länder und Kommunen den Ausbau nun stark fördern wollen	1	2017-02-13 10:05:04.800931	f
154	153	E-Autos das autonome Fahren vorantreiben	5	2017-02-02 10:05:04.800975	f
155	154	Tesla mutig bestehende Techniken einsetzt und zeigt was sie können	5	2017-02-10 10:05:04.801019	f
156	87	Cats are fucking stupid and bloody fuzzy critters!	1	2017-02-13 10:05:04.801063	f
\.


--
-- Name: textversions_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('textversions_uid_seq', 156, true);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY users (uid, firstname, surname, nickname, public_nickname, email, gender, password, group_uid, last_action, last_login, registered, token, token_timestamp) FROM stdin;
1	anonymous	anonymous	anonymous	anonymous		m	$2a$10$zmJLWq55wj.kGSMSDJx8V.ZMY7S.a9XJTRhxzbrjx8Ti6xyaochTm	3	2017-01-26 17:08:50	2017-01-26 17:08:50	2017-01-26 17:08:50		\N
2	admin	admin	admin	admin	dbas.hhu@gmail.com	m	$2a$10$hMmR6eJsYGLWZZhWJGwT3eiolhW.2RZw3lqe23qFZSq6hiAQjwpeW	1	2017-01-26 17:08:50	2017-01-26 17:08:50	2017-01-26 17:08:50		\N
6	Daniel Tobias Pablo	Neugebauer	daneu102	daneu102	neugebauer@cs.uni-duesseldorf.de	m	$2a$10$v.HczFzEwvplduCi64C5Cu1/n/PpqCxqKbowvu304CRHMEshKApKe	3	2017-01-31 15:13:05.541664	2017-01-31 15:12:45.806335	2017-01-26 17:12:25		\N
12	Alexander	Schneider	alsch132	alsch132	Alexander.Schneider@hhu.de	m	$2a$1...	3	2017-01-30 09:07:09	2017-01-27 10:00:27	2017-01-27 10:00:26		\N
11	Tobias	Amft	toamf100	toamf100	Tobias.Amft@uni-duesseldorf.de	m	$2a$1...	3	2017-01-27 12:16:05	2017-01-27 12:15:45	2017-01-27 09:17:08		\N
8	Katharina	Esau	kaesa100	kaesa100	Katharina.Esau@uni-duesseldorf.de	f	$2a$1...	3	2017-02-02 11:53:59.699453	2017-02-02 10:49:47.711722	2017-01-26 18:00:13		\N
13	Hilmar	Schadrack	hisch100	hisch100	Hilmar.Schadrack@uni-duesseldorf.de	m	$2a$10$sLMnqgTx6Wpck7mQZHQdje/.p0xuIpHWvSTGvwrx5XbCiCopmDHIy	3	2017-02-02 16:11:42.64313	2017-02-02 16:06:10.650141	2017-01-27 10:29:36		\N
18	Andre	Ippisch	anipp100	anipp100	ippisch@cs.uni-duesseldorf.de	m	$2a$10$tj37nQ9BDgSvF0QFnfUWCuxvhuR7AKIh/ZGT7TM7Pfea67kixLO4q	3	2017-02-01 14:27:03.327977	2017-02-01 14:11:16.624882	2017-02-01 14:10:54.569345		\N
5	Björn	Ebbinghaus	bjebb100	bjebb100	Bjoern.Ebbinghaus@uni-duesseldorf.de	m	$2a$1...	3	2017-02-01 13:42:24.48439	2017-01-27 12:54:28	2017-01-26 17:09:55		\N
10	Thomas	Spitzlei	spitzlei	spitzlei	spitzlei@cs.uni-duesseldorf.de	m	$2a$1...	3	2017-01-27 12:27:41	2017-01-27 09:10:05	2017-01-27 09:10:04		\N
14	Kálmán	Graffi	graffi	graffi	Kalman.Graffi@uni-duesseldorf.de	m	$2a$1...	3	2017-01-27 13:53:34	2017-01-27 10:30:05	2017-01-27 10:30:04		\N
16	Philipp	Hagemeister	phhag101	phhag101	Philipp.Hagemeister@uni-duesseldorf.de	m	$2a$1...	3	2017-01-31 12:06:38	2017-01-30 01:04:29	2017-01-30 00:49:16		\N
20	Pauline	Schur	pasch161	pasch161	Pauline.Schur@uni-duesseldorf.de	f	$2a$10$mkgcNuMlkt78cpLyZrXDoutdEWt2KWOTkl10eVotdd4NPDboH21GC	3	2017-02-02 22:10:59.519143	2017-02-02 21:46:59.245213	2017-02-02 21:46:42.726862		\N
9	Martin	Mauve	mamau002	mamau002	Mauve@uni-duesseldorf.de	m	$2a$1...	3	2017-02-02 15:48:41.931014	2017-02-02 15:32:02.79239	2017-01-26 20:02:52		\N
19	Tobias	Escher	escher	escher	Tobias.Escher@uni-duesseldorf.de	m	$2a$10$NNa7WC.ZyaDn7E1amKnGbehHWj20P9w94q5EhVmmRm3LlcWbptVTe	3	2017-02-02 09:19:08.781577	2017-02-02 09:14:46.390319	2017-02-02 09:14:38.102634		\N
3	Tobias	Krauthoff	Tobias	Tobias	krauthoff@cs.uni-duesseldorf.de	m	$2a$10$TQTR3yo.cOqoKyufaOAcX.jDwrN57Jfa27JgmwNY.4gKtPZyhpCSa	1	2017-02-06 08:30:49.212561	2017-02-05 07:56:20.108564	2017-01-26 17:08:50		\N
15	Tobias	Krauthoff	tokra100	tokra100	krauthoff@cs.uni-duesseldorf.de	m	$2a$10$eHhCkoPJIDHRPK.hGCjncur/53JHN9s2TAK2KLJv26LKIGwUoO3f.	3	2017-02-02 14:23:09.838923	2017-02-02 14:23:09.029142	2017-01-28 08:35:11		\N
4	Christian	Meter	Christian	Christian	meter@cs.uni-duesseldorf.de	m	$2a$10$dZxvbDlVQj8qDJxzIKuYluIdDFu9OoPiVpqs.0DxlQCZUrUqqb59C	1	2017-02-06 12:16:24.154674	2017-02-06 12:15:10.490072	2017-01-26 17:08:50		\N
21	Matthias	Liebeck	malie102	malie102	Matthias.Liebeck@uni-duesseldorf.de	m	$2a$10$a9aG/DC9QQcixOU4FxZeW.KOBdyMe205sdTLIqnYn.RW4MRzsopfS	3	2017-02-03 13:11:07.988006	2017-02-03 12:50:12.12274	2017-02-03 12:50:05.046016		\N
17	Christian	Meter	chmet101	chmet101	meter@cs.uni-duesseldorf.de	m	$2a$10$Uqt.kkZRt.7YZIxu4/08.u7Qofymp2ZPqX0ayfvcWSB1W0ppbtaku	2	2017-01-30 14:31:52	2017-01-30 14:30:32	2017-01-30 14:30:30		\N
7	Raphael	Bialon	rabia100	rabia100	bialon@cs.uni-duesseldorf.de	m	$2a$1...	3	2017-01-31 07:16:36	2017-01-28 07:35:49	2017-01-26 17:31:48		\N
\.


--
-- Name: users_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('users_uid_seq', 21, true);


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
-- Name: arguments; Type: ACL; Schema: public; Owner: dbas
--

REVOKE ALL ON TABLE arguments FROM PUBLIC;
REVOKE ALL ON TABLE arguments FROM dbas;
GRANT ALL ON TABLE arguments TO dbas;
GRANT SELECT ON TABLE arguments TO dolan;


--
-- Name: clicked_arguments; Type: ACL; Schema: public; Owner: dbas
--

REVOKE ALL ON TABLE clicked_arguments FROM PUBLIC;
REVOKE ALL ON TABLE clicked_arguments FROM dbas;
GRANT ALL ON TABLE clicked_arguments TO dbas;
GRANT SELECT ON TABLE clicked_arguments TO dolan;


--
-- Name: clicked_statements; Type: ACL; Schema: public; Owner: dbas
--

REVOKE ALL ON TABLE clicked_statements FROM PUBLIC;
REVOKE ALL ON TABLE clicked_statements FROM dbas;
GRANT ALL ON TABLE clicked_statements TO dbas;
GRANT SELECT ON TABLE clicked_statements TO dolan;


--
-- Name: groups; Type: ACL; Schema: public; Owner: dbas
--

REVOKE ALL ON TABLE groups FROM PUBLIC;
REVOKE ALL ON TABLE groups FROM dbas;
GRANT ALL ON TABLE groups TO dbas;
GRANT SELECT ON TABLE groups TO dolan;


--
-- Name: history; Type: ACL; Schema: public; Owner: dbas
--

REVOKE ALL ON TABLE history FROM PUBLIC;
REVOKE ALL ON TABLE history FROM dbas;
GRANT ALL ON TABLE history TO dbas;
GRANT SELECT ON TABLE history TO dolan;


--
-- Name: issues; Type: ACL; Schema: public; Owner: dbas
--

REVOKE ALL ON TABLE issues FROM PUBLIC;
REVOKE ALL ON TABLE issues FROM dbas;
GRANT ALL ON TABLE issues TO dbas;
GRANT SELECT ON TABLE issues TO dolan;


--
-- Name: languages; Type: ACL; Schema: public; Owner: dbas
--

REVOKE ALL ON TABLE languages FROM PUBLIC;
REVOKE ALL ON TABLE languages FROM dbas;
GRANT ALL ON TABLE languages TO dbas;
GRANT SELECT ON TABLE languages TO dolan;


--
-- Name: last_reviewers_delete; Type: ACL; Schema: public; Owner: dbas
--

REVOKE ALL ON TABLE last_reviewers_delete FROM PUBLIC;
REVOKE ALL ON TABLE last_reviewers_delete FROM dbas;
GRANT ALL ON TABLE last_reviewers_delete TO dbas;
GRANT SELECT ON TABLE last_reviewers_delete TO dolan;


--
-- Name: last_reviewers_duplicates; Type: ACL; Schema: public; Owner: dbas
--

REVOKE ALL ON TABLE last_reviewers_duplicates FROM PUBLIC;
REVOKE ALL ON TABLE last_reviewers_duplicates FROM dbas;
GRANT ALL ON TABLE last_reviewers_duplicates TO dbas;
GRANT SELECT ON TABLE last_reviewers_duplicates TO dolan;


--
-- Name: last_reviewers_edit; Type: ACL; Schema: public; Owner: dbas
--

REVOKE ALL ON TABLE last_reviewers_edit FROM PUBLIC;
REVOKE ALL ON TABLE last_reviewers_edit FROM dbas;
GRANT ALL ON TABLE last_reviewers_edit TO dbas;
GRANT SELECT ON TABLE last_reviewers_edit TO dolan;


--
-- Name: last_reviewers_optimization; Type: ACL; Schema: public; Owner: dbas
--

REVOKE ALL ON TABLE last_reviewers_optimization FROM PUBLIC;
REVOKE ALL ON TABLE last_reviewers_optimization FROM dbas;
GRANT ALL ON TABLE last_reviewers_optimization TO dbas;
GRANT SELECT ON TABLE last_reviewers_optimization TO dolan;


--
-- Name: marked_arguments; Type: ACL; Schema: public; Owner: dbas
--

REVOKE ALL ON TABLE marked_arguments FROM PUBLIC;
REVOKE ALL ON TABLE marked_arguments FROM dbas;
GRANT ALL ON TABLE marked_arguments TO dbas;
GRANT SELECT ON TABLE marked_arguments TO dolan;


--
-- Name: marked_statements; Type: ACL; Schema: public; Owner: dbas
--

REVOKE ALL ON TABLE marked_statements FROM PUBLIC;
REVOKE ALL ON TABLE marked_statements FROM dbas;
GRANT ALL ON TABLE marked_statements TO dbas;
GRANT SELECT ON TABLE marked_statements TO dolan;


--
-- Name: messages; Type: ACL; Schema: public; Owner: dbas
--

REVOKE ALL ON TABLE messages FROM PUBLIC;
REVOKE ALL ON TABLE messages FROM dbas;
GRANT ALL ON TABLE messages TO dbas;
GRANT SELECT ON TABLE messages TO dolan;


--
-- Name: optimization_review_locks; Type: ACL; Schema: public; Owner: dbas
--

REVOKE ALL ON TABLE optimization_review_locks FROM PUBLIC;
REVOKE ALL ON TABLE optimization_review_locks FROM dbas;
GRANT ALL ON TABLE optimization_review_locks TO dbas;
GRANT SELECT ON TABLE optimization_review_locks TO dolan;


--
-- Name: premisegroups; Type: ACL; Schema: public; Owner: dbas
--

REVOKE ALL ON TABLE premisegroups FROM PUBLIC;
REVOKE ALL ON TABLE premisegroups FROM dbas;
GRANT ALL ON TABLE premisegroups TO dbas;
GRANT SELECT ON TABLE premisegroups TO dolan;


--
-- Name: premises; Type: ACL; Schema: public; Owner: dbas
--

REVOKE ALL ON TABLE premises FROM PUBLIC;
REVOKE ALL ON TABLE premises FROM dbas;
GRANT ALL ON TABLE premises TO dbas;
GRANT SELECT ON TABLE premises TO dolan;


--
-- Name: reputation_history; Type: ACL; Schema: public; Owner: dbas
--

REVOKE ALL ON TABLE reputation_history FROM PUBLIC;
REVOKE ALL ON TABLE reputation_history FROM dbas;
GRANT ALL ON TABLE reputation_history TO dbas;
GRANT SELECT ON TABLE reputation_history TO dolan;


--
-- Name: reputation_reasons; Type: ACL; Schema: public; Owner: dbas
--

REVOKE ALL ON TABLE reputation_reasons FROM PUBLIC;
REVOKE ALL ON TABLE reputation_reasons FROM dbas;
GRANT ALL ON TABLE reputation_reasons TO dbas;
GRANT SELECT ON TABLE reputation_reasons TO dolan;


--
-- Name: review_canceled; Type: ACL; Schema: public; Owner: dbas
--

REVOKE ALL ON TABLE review_canceled FROM PUBLIC;
REVOKE ALL ON TABLE review_canceled FROM dbas;
GRANT ALL ON TABLE review_canceled TO dbas;
GRANT SELECT ON TABLE review_canceled TO dolan;


--
-- Name: review_delete_reasons; Type: ACL; Schema: public; Owner: dbas
--

REVOKE ALL ON TABLE review_delete_reasons FROM PUBLIC;
REVOKE ALL ON TABLE review_delete_reasons FROM dbas;
GRANT ALL ON TABLE review_delete_reasons TO dbas;
GRANT SELECT ON TABLE review_delete_reasons TO dolan;


--
-- Name: review_deletes; Type: ACL; Schema: public; Owner: dbas
--

REVOKE ALL ON TABLE review_deletes FROM PUBLIC;
REVOKE ALL ON TABLE review_deletes FROM dbas;
GRANT ALL ON TABLE review_deletes TO dbas;
GRANT SELECT ON TABLE review_deletes TO dolan;


--
-- Name: review_duplicates; Type: ACL; Schema: public; Owner: dbas
--

REVOKE ALL ON TABLE review_duplicates FROM PUBLIC;
REVOKE ALL ON TABLE review_duplicates FROM dbas;
GRANT ALL ON TABLE review_duplicates TO dbas;
GRANT SELECT ON TABLE review_duplicates TO dolan;


--
-- Name: review_edit_values; Type: ACL; Schema: public; Owner: dbas
--

REVOKE ALL ON TABLE review_edit_values FROM PUBLIC;
REVOKE ALL ON TABLE review_edit_values FROM dbas;
GRANT ALL ON TABLE review_edit_values TO dbas;
GRANT SELECT ON TABLE review_edit_values TO dolan;


--
-- Name: review_edits; Type: ACL; Schema: public; Owner: dbas
--

REVOKE ALL ON TABLE review_edits FROM PUBLIC;
REVOKE ALL ON TABLE review_edits FROM dbas;
GRANT ALL ON TABLE review_edits TO dbas;
GRANT SELECT ON TABLE review_edits TO dolan;


--
-- Name: review_optimizations; Type: ACL; Schema: public; Owner: dbas
--

REVOKE ALL ON TABLE review_optimizations FROM PUBLIC;
REVOKE ALL ON TABLE review_optimizations FROM dbas;
GRANT ALL ON TABLE review_optimizations TO dbas;
GRANT SELECT ON TABLE review_optimizations TO dolan;


--
-- Name: revoked_content; Type: ACL; Schema: public; Owner: dbas
--

REVOKE ALL ON TABLE revoked_content FROM PUBLIC;
REVOKE ALL ON TABLE revoked_content FROM dbas;
GRANT ALL ON TABLE revoked_content TO dbas;
GRANT SELECT ON TABLE revoked_content TO dolan;


--
-- Name: revoked_content_history; Type: ACL; Schema: public; Owner: dbas
--

REVOKE ALL ON TABLE revoked_content_history FROM PUBLIC;
REVOKE ALL ON TABLE revoked_content_history FROM dbas;
GRANT ALL ON TABLE revoked_content_history TO dbas;
GRANT SELECT ON TABLE revoked_content_history TO dolan;


--
-- Name: revoked_duplicate; Type: ACL; Schema: public; Owner: dbas
--

REVOKE ALL ON TABLE revoked_duplicate FROM PUBLIC;
REVOKE ALL ON TABLE revoked_duplicate FROM dbas;
GRANT ALL ON TABLE revoked_duplicate TO dbas;
GRANT SELECT ON TABLE revoked_duplicate TO dolan;


--
-- Name: rss; Type: ACL; Schema: public; Owner: dbas
--

REVOKE ALL ON TABLE rss FROM PUBLIC;
REVOKE ALL ON TABLE rss FROM dbas;
GRANT ALL ON TABLE rss TO dbas;
GRANT SELECT ON TABLE rss TO dolan;


--
-- Name: seen_arguments; Type: ACL; Schema: public; Owner: dbas
--

REVOKE ALL ON TABLE seen_arguments FROM PUBLIC;
REVOKE ALL ON TABLE seen_arguments FROM dbas;
GRANT ALL ON TABLE seen_arguments TO dbas;
GRANT SELECT ON TABLE seen_arguments TO dolan;


--
-- Name: seen_statements; Type: ACL; Schema: public; Owner: dbas
--

REVOKE ALL ON TABLE seen_statements FROM PUBLIC;
REVOKE ALL ON TABLE seen_statements FROM dbas;
GRANT ALL ON TABLE seen_statements TO dbas;
GRANT SELECT ON TABLE seen_statements TO dolan;


--
-- Name: settings; Type: ACL; Schema: public; Owner: dbas
--

REVOKE ALL ON TABLE settings FROM PUBLIC;
REVOKE ALL ON TABLE settings FROM dbas;
GRANT ALL ON TABLE settings TO dbas;
GRANT SELECT ON TABLE settings TO dolan;


--
-- Name: statement_references; Type: ACL; Schema: public; Owner: dbas
--

REVOKE ALL ON TABLE statement_references FROM PUBLIC;
REVOKE ALL ON TABLE statement_references FROM dbas;
GRANT ALL ON TABLE statement_references TO dbas;
GRANT SELECT ON TABLE statement_references TO dolan;


--
-- Name: statements; Type: ACL; Schema: public; Owner: dbas
--

REVOKE ALL ON TABLE statements FROM PUBLIC;
REVOKE ALL ON TABLE statements FROM dbas;
GRANT ALL ON TABLE statements TO dbas;
GRANT SELECT ON TABLE statements TO dolan;


--
-- Name: textversions; Type: ACL; Schema: public; Owner: dbas
--

REVOKE ALL ON TABLE textversions FROM PUBLIC;
REVOKE ALL ON TABLE textversions FROM dbas;
GRANT ALL ON TABLE textversions TO dbas;
GRANT SELECT ON TABLE textversions TO dolan;


--
-- Name: users; Type: ACL; Schema: public; Owner: dbas
--

REVOKE ALL ON TABLE users FROM PUBLIC;
REVOKE ALL ON TABLE users FROM dbas;
GRANT ALL ON TABLE users TO dbas;
GRANT SELECT ON TABLE users TO dolan;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: public; Owner: dbas
--

ALTER DEFAULT PRIVILEGES FOR ROLE dbas IN SCHEMA public REVOKE ALL ON TABLES  FROM PUBLIC;
ALTER DEFAULT PRIVILEGES FOR ROLE dbas IN SCHEMA public REVOKE ALL ON TABLES  FROM dbas;
ALTER DEFAULT PRIVILEGES FOR ROLE dbas IN SCHEMA public GRANT SELECT ON TABLES  TO dolan;


--
-- PostgreSQL database dump complete
--

