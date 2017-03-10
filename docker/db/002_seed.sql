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
1	1	2	\N	f	1	2017-03-09 12:37:50.839428	2	t
2	2	2	\N	t	1	2017-03-09 12:37:50.839428	2	f
3	3	2	\N	f	1	2017-03-09 12:37:50.839428	2	f
4	4	3	\N	t	1	2017-03-09 12:37:50.839428	2	f
5	5	3	\N	f	1	2017-03-09 12:37:50.839428	2	f
8	8	4	\N	t	1	2017-03-09 12:37:50.839428	2	f
10	10	11	\N	f	1	2017-03-09 12:37:50.839428	2	f
11	11	2	\N	t	1	2017-03-09 12:37:50.839428	2	f
12	12	2	\N	t	1	2017-03-09 12:37:50.839428	2	f
15	15	5	\N	t	1	2017-03-09 12:37:50.839428	2	f
16	16	5	\N	f	1	2017-03-09 12:37:50.839428	2	f
17	17	5	\N	t	1	2017-03-09 12:37:50.839428	2	f
19	19	6	\N	t	1	2017-03-09 12:37:50.839428	2	f
20	20	6	\N	f	1	2017-03-09 12:37:50.839428	2	f
21	21	6	\N	f	1	2017-03-09 12:37:50.839428	2	f
23	23	14	\N	f	1	2017-03-09 12:37:50.839428	2	f
24	24	14	\N	t	1	2017-03-09 12:37:50.839428	2	f
26	26	14	\N	t	1	2017-03-09 12:37:50.839428	2	f
27	27	15	\N	t	1	2017-03-09 12:37:50.839428	2	f
28	27	16	\N	t	1	2017-03-09 12:37:50.839428	2	f
29	28	15	\N	t	1	2017-03-09 12:37:50.839428	2	f
30	29	15	\N	f	1	2017-03-09 12:37:50.839428	2	f
35	34	41	\N	t	1	2017-03-09 12:37:50.839428	1	f
36	35	36	\N	f	1	2017-03-09 12:37:50.839428	1	f
39	38	37	\N	t	1	2017-03-09 12:37:50.839428	1	f
40	39	37	\N	t	1	2017-03-09 12:37:50.839428	1	f
41	41	46	\N	f	1	2017-03-09 12:37:50.839428	1	f
42	42	37	\N	f	1	2017-03-09 12:37:50.839428	1	f
44	44	50	\N	f	1	2017-03-09 12:37:50.839428	1	f
46	45	50	\N	t	1	2017-03-09 12:37:50.839428	1	f
47	46	38	\N	t	1	2017-03-09 12:37:50.839428	1	f
49	48	38	\N	f	1	2017-03-09 12:37:50.839428	1	f
50	49	49	\N	f	1	2017-03-09 12:37:50.839428	1	f
51	51	58	\N	f	1	2017-03-09 12:37:50.839428	4	f
54	54	59	\N	t	1	2017-03-09 12:37:50.839428	4	f
55	55	59	\N	f	1	2017-03-09 12:37:50.839428	4	f
56	56	60	\N	t	1	2017-03-09 12:37:50.839428	4	f
57	57	60	\N	f	1	2017-03-09 12:37:50.839428	4	f
58	50	58	\N	t	1	2017-03-09 12:37:50.839428	4	f
59	61	67	\N	t	1	2017-03-09 12:37:50.839428	4	f
60	62	69	\N	t	1	2017-03-09 12:37:50.839428	5	f
61	63	69	\N	t	1	2017-03-09 12:37:50.839428	5	f
62	64	69	\N	f	1	2017-03-09 12:37:50.839428	5	f
63	65	70	\N	f	1	2017-03-09 12:37:50.839428	5	f
64	66	70	\N	f	1	2017-03-09 12:37:50.839428	5	f
6	6	\N	4	f	1	2017-03-09 12:37:50.839428	2	f
7	7	\N	5	f	1	2017-03-09 12:37:50.839428	2	f
9	9	\N	8	f	1	2017-03-09 12:37:50.839428	2	f
13	13	\N	12	f	1	2017-03-09 12:37:50.839428	2	f
14	14	\N	13	f	1	2017-03-09 12:37:50.839428	2	f
18	18	\N	2	f	1	2017-03-09 12:37:50.839428	2	f
22	22	\N	3	f	1	2017-03-09 12:37:50.839428	2	f
25	25	\N	11	f	1	2017-03-09 12:37:50.839428	2	f
31	30	\N	15	f	1	2017-03-09 12:37:50.839428	2	f
37	36	\N	36	f	1	2017-03-09 12:37:50.839428	1	f
38	37	\N	36	f	1	2017-03-09 12:37:50.839428	1	f
43	43	\N	42	f	1	2017-03-09 12:37:50.839428	1	f
45	40	\N	39	f	1	2017-03-09 12:37:50.839428	1	f
48	47	\N	47	f	1	2017-03-09 12:37:50.839428	1	f
52	52	\N	58	f	1	2017-03-09 12:37:50.839428	4	f
53	53	\N	51	f	1	2017-03-09 12:37:50.839428	4	f
32	31	36	\N	t	8	2017-03-09 12:37:50.839428	1	f
34	33	39	\N	t	8	2017-03-09 12:37:50.839428	1	f
33	32	\N	32	f	8	2017-03-09 12:37:50.839428	1	f
\.


--
-- Name: arguments_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('arguments_uid_seq', 64, true);


--
-- Data for Name: clicked_arguments; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY clicked_arguments (uid, argument_uid, author_uid, "timestamp", is_up_vote, is_valid) FROM stdin;
1	53	21	2017-02-24 12:37:54.88432	t	t
2	53	29	2017-02-21 12:37:54.884435	t	t
3	53	19	2017-03-08 12:37:54.884501	t	t
4	53	15	2017-02-28 12:37:54.884555	t	t
5	53	30	2017-02-20 12:37:54.884615	t	t
6	53	24	2017-03-02 12:37:54.884693	t	t
7	53	18	2017-03-05 12:37:54.884743	t	t
8	53	26	2017-02-22 12:37:54.884791	t	t
9	53	37	2017-03-06 12:37:54.884836	t	t
10	53	16	2017-02-27 12:37:54.884881	t	t
11	53	27	2017-03-04 12:37:54.884927	t	t
12	53	34	2017-02-25 12:37:54.884972	t	t
13	53	23	2017-02-22 12:37:54.885016	t	t
14	53	22	2017-02-17 12:37:54.885061	t	t
15	53	10	2017-02-20 12:37:54.885106	t	t
16	53	11	2017-02-26 12:37:54.885153	t	t
17	53	8	2017-02-24 12:37:54.885198	f	t
18	53	12	2017-02-17 12:37:54.885243	f	t
19	53	25	2017-02-25 12:37:54.885286	f	t
20	53	22	2017-02-21 12:37:54.885332	f	t
21	53	14	2017-02-28 12:37:54.885377	f	t
22	53	15	2017-03-02 12:37:54.885423	f	t
\.


--
-- Name: clicked_arguments_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('clicked_arguments_uid_seq', 22, true);


--
-- Data for Name: clicked_statements; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY clicked_statements (uid, statement_uid, author_uid, "timestamp", is_up_vote, is_valid) FROM stdin;
1	75	22	2017-02-23 12:37:54.869693	t	t
2	75	12	2017-02-18 12:37:54.869824	t	t
3	75	9	2017-02-12 12:37:54.869889	t	t
4	75	10	2017-02-23 12:37:54.869941	t	t
5	75	30	2017-02-19 12:37:54.869989	t	t
6	75	30	2017-02-25 12:37:54.870034	t	t
7	75	22	2017-02-14 12:37:54.87008	t	t
8	75	13	2017-02-17 12:37:54.870126	f	t
9	75	32	2017-02-20 12:37:54.870171	f	t
10	75	34	2017-02-20 12:37:54.870216	f	t
11	75	29	2017-03-05 12:37:54.870261	f	t
12	75	22	2017-02-22 12:37:54.870306	f	t
13	75	18	2017-02-27 12:37:54.870351	f	t
14	75	29	2017-02-23 12:37:54.870395	f	t
15	75	38	2017-03-03 12:37:54.870438	f	t
16	75	20	2017-02-27 12:37:54.870482	f	t
17	75	22	2017-02-21 12:37:54.870528	f	t
18	75	30	2017-02-12 12:37:54.870572	f	t
19	75	19	2017-02-16 12:37:54.870616	f	t
20	75	33	2017-02-21 12:37:54.87066	f	t
21	75	30	2017-02-16 12:37:54.870706	f	t
22	75	20	2017-02-22 12:37:54.87075	f	t
23	75	33	2017-03-05 12:37:54.870794	f	t
\.


--
-- Name: clicked_statements_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('clicked_statements_uid_seq', 23, true);


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
1	Town has to cut spending 	Our town needs to cut spending. Please discuss ideas how this should be done.		2017-03-09 12:37:50.792733	2	1	f
2	Cat or Dog	Your family argues about whether to buy a cat or dog as pet. Now your opinion matters!		2017-03-09 12:37:50.792733	2	1	f
3	Make the world better	How can we make this world a better place?		2017-03-09 12:37:50.792733	2	1	f
4	Elektroautos	Elektroautos - Die Autos der Zukunft? Bitte diskutieren Sie dazu.		2017-03-09 12:37:50.792733	2	2	f
5	Unterstützung der Sekretariate	Unsere Sekretariate in der Informatik sind arbeitsmäßig stark überlastet. Bitte diskutieren Sie Möglichkeiten um dies zu verbessern.		2017-03-09 12:37:50.792733	2	2	f
6	Verbesserung des Informatik-Studiengangs	Wie können der Informatik-Studiengang verbessert und die Probleme, die durch die große Anzahl der Studierenden entstanden sind, gelöst werden?	Die Anzahl der Studierenden in der Informatik hat sich in den letzten Jahren stark erhöht. Dadurch treten zahlreiche Probleme auf, wie z.B. Raumknappheit, überfüllte Lehrveranstaltungen und ein Mangel an Plätzen zum Lernen. Wir möchten Sie gerne dazu einladen, gemeinsam mit den Dozierenden der Informatik über Lösungsmöglichkeiten zu diskutieren: Wie können der Studiengang verbessert und die Probleme, die durch die große Anzahl der Studierenden entstanden sind, gelöst werden?	2017-03-09 12:37:50.792733	2	2	t
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
1	15	1	t	2017-03-09 12:37:50.894133
2	17	1	f	2017-03-09 12:37:50.894133
3	18	1	t	2017-03-09 12:37:50.894133
4	23	1	t	2017-03-09 12:37:50.894133
5	24	1	t	2017-03-09 12:37:50.894133
6	21	2	f	2017-03-09 12:37:50.894133
7	22	2	t	2017-03-09 12:37:50.894133
8	19	2	f	2017-03-09 12:37:50.894133
9	35	2	t	2017-03-09 12:37:50.894133
10	25	2	f	2017-03-09 12:37:50.894133
11	26	2	f	2017-03-09 12:37:50.894133
12	27	2	f	2017-03-09 12:37:50.894133
13	28	3	f	2017-03-09 12:37:50.894133
14	29	3	f	2017-03-09 12:37:50.894133
15	34	3	f	2017-03-09 12:37:50.894133
16	20	8	t	2017-03-09 12:37:50.894133
17	36	8	t	2017-03-09 12:37:50.894133
18	37	8	t	2017-03-09 12:37:50.894133
\.


--
-- Name: last_reviewers_delete_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('last_reviewers_delete_uid_seq', 18, true);


--
-- Data for Name: last_reviewers_duplicates; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY last_reviewers_duplicates (uid, reviewer_uid, review_uid, is_okay, "timestamp") FROM stdin;
1	13	1	t	2017-03-09 12:37:50.897702
2	14	2	t	2017-03-09 12:37:50.897702
3	15	2	t	2017-03-09 12:37:50.897702
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
1	30	1	t	2017-03-09 12:37:50.905162
2	32	1	t	2017-03-09 12:37:50.905162
3	33	1	t	2017-03-09 12:37:50.905162
4	13	2	f	2017-03-09 12:37:50.905162
5	14	2	f	2017-03-09 12:37:50.905162
6	16	2	f	2017-03-09 12:37:50.905162
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
62	1
63	1
64	1
65	1
66	1
61	8
\.


--
-- Name: premisegroups_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('premisegroups_uid_seq', 66, true);


--
-- Data for Name: premises; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY premises (uid, premisesgroup_uid, statement_uid, is_negated, author_uid, "timestamp", issue_uid, is_disabled) FROM stdin;
1	1	1	f	1	2017-03-09 12:37:50.8341	2	t
2	2	5	f	1	2017-03-09 12:37:50.8341	2	f
3	3	6	f	1	2017-03-09 12:37:50.8341	2	f
4	4	7	f	1	2017-03-09 12:37:50.8341	2	f
5	5	8	f	1	2017-03-09 12:37:50.8341	2	f
6	6	9	f	1	2017-03-09 12:37:50.8341	2	f
7	7	10	f	1	2017-03-09 12:37:50.8341	2	f
8	8	11	f	1	2017-03-09 12:37:50.8341	2	f
9	9	12	f	1	2017-03-09 12:37:50.8341	2	f
10	10	13	f	1	2017-03-09 12:37:50.8341	2	f
11	11	14	f	1	2017-03-09 12:37:50.8341	2	f
12	12	15	f	1	2017-03-09 12:37:50.8341	2	f
13	12	16	f	1	2017-03-09 12:37:50.8341	2	f
14	13	17	f	1	2017-03-09 12:37:50.8341	2	f
15	14	18	f	1	2017-03-09 12:37:50.8341	2	f
16	15	19	f	1	2017-03-09 12:37:50.8341	2	f
17	16	20	f	1	2017-03-09 12:37:50.8341	2	f
18	17	21	f	1	2017-03-09 12:37:50.8341	2	f
19	18	22	f	1	2017-03-09 12:37:50.8341	2	f
20	19	23	f	1	2017-03-09 12:37:50.8341	2	f
21	20	24	f	1	2017-03-09 12:37:50.8341	2	f
22	21	25	f	1	2017-03-09 12:37:50.8341	2	f
23	22	26	f	1	2017-03-09 12:37:50.8341	2	f
24	23	27	f	1	2017-03-09 12:37:50.8341	2	f
25	24	28	f	1	2017-03-09 12:37:50.8341	2	f
26	25	29	f	1	2017-03-09 12:37:50.8341	2	f
27	26	30	f	1	2017-03-09 12:37:50.8341	2	f
28	27	31	f	1	2017-03-09 12:37:50.8341	2	f
29	28	32	f	1	2017-03-09 12:37:50.8341	2	f
30	29	33	f	1	2017-03-09 12:37:50.8341	2	f
31	30	34	f	1	2017-03-09 12:37:50.8341	2	f
32	9	35	f	1	2017-03-09 12:37:50.8341	2	f
33	31	39	f	1	2017-03-09 12:37:50.8341	1	f
34	32	40	f	1	2017-03-09 12:37:50.8341	1	f
35	33	41	f	1	2017-03-09 12:37:50.8341	1	f
36	34	42	f	1	2017-03-09 12:37:50.8341	1	f
37	35	43	f	1	2017-03-09 12:37:50.8341	1	f
38	36	44	f	1	2017-03-09 12:37:50.8341	1	f
39	37	45	f	1	2017-03-09 12:37:50.8341	1	f
40	38	46	f	1	2017-03-09 12:37:50.8341	1	f
41	39	47	f	1	2017-03-09 12:37:50.8341	1	f
42	40	48	f	1	2017-03-09 12:37:50.8341	1	f
43	41	49	f	1	2017-03-09 12:37:50.8341	1	f
44	42	50	f	1	2017-03-09 12:37:50.8341	1	f
45	43	51	f	1	2017-03-09 12:37:50.8341	1	f
46	44	52	f	1	2017-03-09 12:37:50.8341	1	f
47	45	53	f	1	2017-03-09 12:37:50.8341	1	f
48	46	54	f	1	2017-03-09 12:37:50.8341	1	f
49	47	55	f	1	2017-03-09 12:37:50.8341	1	f
50	48	56	f	1	2017-03-09 12:37:50.8341	1	f
51	49	57	f	1	2017-03-09 12:37:50.8341	1	f
52	52	61	f	1	2017-03-09 12:37:50.8341	4	f
53	53	62	f	1	2017-03-09 12:37:50.8341	4	f
54	54	63	f	1	2017-03-09 12:37:50.8341	4	f
55	55	64	f	1	2017-03-09 12:37:50.8341	4	f
56	56	65	f	1	2017-03-09 12:37:50.8341	4	f
57	57	66	f	1	2017-03-09 12:37:50.8341	4	f
58	50	59	f	1	2017-03-09 12:37:50.8341	4	f
59	51	60	f	1	2017-03-09 12:37:50.8341	4	f
61	62	71	f	1	2017-03-09 12:37:50.8341	5	f
62	63	72	f	1	2017-03-09 12:37:50.8341	5	f
63	64	73	f	1	2017-03-09 12:37:50.8341	5	f
64	65	74	f	1	2017-03-09 12:37:50.8341	5	f
65	66	75	f	1	2017-03-09 12:37:50.8341	5	f
60	61	68	f	8	2017-03-09 12:37:50.8341	4	f
\.


--
-- Name: premises_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('premises_uid_seq', 65, true);


--
-- Data for Name: reputation_history; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY reputation_history (uid, reputator_uid, reputation_uid, "timestamp") FROM stdin;
1	24	1	2017-03-07 12:37:55.060601
2	24	2	2017-03-08 12:37:55.060601
3	24	3	2017-03-09 12:37:55.060601
4	26	1	2017-03-07 12:37:55.060601
5	26	2	2017-03-08 12:37:55.060601
6	26	3	2017-03-09 12:37:55.060601
7	23	1	2017-03-07 12:37:55.060601
8	23	2	2017-03-08 12:37:55.060601
9	23	3	2017-03-09 12:37:55.060601
10	35	1	2017-03-07 12:37:55.060601
11	35	2	2017-03-08 12:37:55.060601
12	35	3	2017-03-09 12:37:55.060601
13	2	1	2017-03-07 12:37:55.060601
14	2	2	2017-03-08 12:37:55.060601
15	2	3	2017-03-09 12:37:55.060601
16	2	8	2017-03-09 12:37:55.060601
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
1	19	23	\N	2017-03-09 12:37:50.867917	t	2	f
2	20	7	\N	2017-03-09 12:37:50.867917	t	1	f
3	21	\N	26	2017-03-09 12:37:50.867917	t	1	f
4	22	\N	14	2017-03-09 12:37:50.867917	f	2	f
5	23	\N	22	2017-03-09 12:37:50.867917	f	2	f
6	24	\N	29	2017-03-09 12:37:50.867917	f	2	f
7	25	11	\N	2017-03-09 12:37:50.867917	f	1	f
8	26	8	\N	2017-03-09 12:37:50.867917	f	2	f
9	27	11	\N	2017-03-09 12:37:50.867917	f	1	f
10	28	1	\N	2017-03-09 12:37:50.867917	t	1	f
\.


--
-- Name: review_deletes_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('review_deletes_uid_seq', 10, true);


--
-- Data for Name: review_duplicates; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY review_duplicates (uid, detector_uid, duplicate_statement_uid, original_statement_uid, "timestamp", is_executed, is_revoked) FROM stdin;
1	29	6	1	2017-03-09 12:37:50.887785	f	f
2	30	4	1	2017-03-09 12:37:50.887785	t	f
3	30	22	7	2017-03-09 12:37:50.887785	f	f
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
1	7	\N	2	2017-03-09 12:37:50.873028	f	f
\.


--
-- Name: review_edits_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('review_edits_uid_seq', 1, true);


--
-- Data for Name: review_optimizations; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY review_optimizations (uid, detector_uid, argument_uid, statement_uid, "timestamp", is_executed, is_revoked) FROM stdin;
1	13	11	\N	2017-03-09 12:37:50.882541	t	f
2	14	\N	30	2017-03-09 12:37:50.882541	t	f
3	15	\N	7	2017-03-09 12:37:50.882541	f	f
4	17	11	\N	2017-03-09 12:37:50.882541	f	f
5	18	7	\N	2017-03-09 12:37:50.882541	f	f
6	16	\N	13	2017-03-09 12:37:50.882541	f	f
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
65	1	35
66	1	15
67	1	28
68	1	19
69	1	12
70	1	33
71	1	25
72	1	36
73	1	20
74	1	9
75	1	17
76	1	32
77	1	23
78	1	8
79	1	30
80	1	24
81	1	37
82	1	29
83	1	18
84	1	10
85	1	14
86	1	22
87	1	21
88	1	16
89	2	30
90	2	26
91	2	12
92	2	38
93	2	8
94	2	27
95	2	10
96	2	35
97	2	34
98	2	36
99	2	15
100	2	22
101	2	25
102	2	32
103	2	20
104	2	18
105	2	37
106	2	13
107	2	9
108	2	29
109	2	24
110	3	22
111	3	17
112	3	20
113	3	18
114	3	38
115	4	13
116	4	21
117	4	14
118	4	17
119	4	28
120	4	10
121	4	9
122	4	16
123	4	32
124	4	25
125	5	10
126	5	23
127	5	8
128	5	22
129	5	11
130	5	35
131	5	20
132	5	32
133	5	13
134	5	30
135	5	37
136	5	33
137	5	27
138	5	25
139	5	38
140	5	26
141	5	30
142	5	36
143	5	15
144	5	18
145	5	34
146	5	28
147	5	19
148	5	24
149	5	16
150	5	9
151	5	12
152	5	14
153	5	21
154	8	26
155	8	34
156	8	30
157	8	9
158	8	32
159	8	21
160	8	22
161	8	38
162	8	33
163	8	35
164	8	30
165	8	27
166	8	16
167	8	12
168	8	14
169	8	13
170	8	36
171	8	25
172	8	23
173	8	8
174	8	17
175	8	20
176	8	10
177	8	28
178	8	11
179	8	37
180	10	19
181	10	33
182	10	9
183	10	34
184	10	18
185	10	36
186	10	14
187	10	30
188	10	13
189	10	10
190	10	17
191	10	12
192	10	35
193	10	23
194	10	37
195	10	8
196	11	23
197	11	25
198	11	11
199	11	37
200	11	32
201	11	12
202	11	30
203	11	9
204	11	22
205	11	33
206	11	21
207	11	18
208	11	10
209	11	20
210	11	29
211	11	17
212	12	27
213	12	37
214	12	34
215	12	13
216	12	23
217	12	29
218	12	11
219	12	22
220	12	26
221	12	32
222	12	8
223	12	33
224	12	10
225	12	28
226	12	17
227	12	19
228	12	35
229	12	25
230	12	30
231	12	14
232	12	24
233	12	20
234	12	9
235	12	38
236	12	16
237	12	12
238	12	21
239	15	21
240	15	34
241	15	20
242	15	25
243	15	14
244	15	29
245	15	32
246	15	24
247	15	35
248	15	16
249	15	27
250	15	33
251	15	36
252	15	37
253	15	30
254	15	17
255	15	30
256	15	38
257	15	18
258	15	23
259	15	13
260	15	10
261	15	12
262	15	9
263	15	22
264	16	24
265	16	9
266	16	35
267	16	32
268	16	27
269	16	23
270	16	15
271	16	29
272	16	37
273	16	13
274	16	36
275	16	11
276	16	34
277	16	28
278	16	25
279	16	8
280	16	22
281	16	18
282	16	17
283	16	20
284	16	14
285	16	10
286	16	12
287	16	38
288	16	33
289	16	26
290	16	19
291	16	16
292	17	12
293	17	10
294	17	30
295	17	21
296	17	19
297	17	27
298	17	11
299	17	17
300	19	34
301	19	17
302	19	29
303	19	25
304	19	28
305	19	13
306	19	30
307	19	38
308	19	32
309	19	21
310	19	8
311	19	10
312	19	30
313	20	14
314	20	34
315	20	26
316	20	35
317	20	32
318	20	30
319	20	22
320	21	37
321	21	25
322	21	34
323	21	20
324	21	12
325	21	35
326	21	13
327	21	33
328	21	28
329	21	30
330	21	38
331	21	29
332	21	21
333	21	9
334	21	18
335	21	10
336	21	24
337	21	14
338	21	22
339	21	8
340	21	15
341	21	30
342	21	23
343	21	26
344	21	27
345	23	25
346	23	33
347	23	22
348	23	30
349	23	16
350	23	30
351	23	35
352	23	13
353	23	17
354	23	14
355	23	24
356	23	38
357	23	37
358	23	20
359	23	8
360	23	29
361	23	10
362	23	36
363	24	27
364	24	21
365	24	10
366	24	9
367	24	13
368	24	8
369	24	34
370	24	11
371	24	12
372	24	30
373	24	26
374	24	37
375	24	24
376	24	18
377	24	32
378	24	36
379	24	38
380	24	15
381	24	25
382	24	22
383	24	16
384	24	30
385	24	33
386	26	27
387	26	30
388	26	15
389	26	18
390	26	33
391	26	37
392	26	23
393	26	24
394	26	25
395	26	17
396	26	10
397	26	16
398	26	21
399	26	35
400	26	14
401	26	36
402	26	34
403	26	19
404	26	26
405	26	11
406	26	8
407	26	22
408	26	30
409	26	9
410	26	28
411	26	13
412	26	12
413	27	30
414	27	22
415	27	33
416	27	25
417	27	8
418	27	27
419	27	21
420	27	17
421	27	10
422	27	12
423	27	11
424	27	29
425	27	36
426	27	14
427	27	37
428	27	34
429	27	24
430	27	15
431	27	18
432	27	20
433	27	28
434	27	13
435	27	30
436	27	32
437	28	19
438	28	38
439	28	30
440	28	22
441	28	21
442	28	30
443	28	28
444	28	15
445	28	32
446	28	12
447	28	34
448	28	35
449	28	9
450	28	26
451	28	33
452	28	37
453	29	30
454	29	18
455	29	15
456	29	17
457	29	22
458	29	19
459	29	8
460	29	24
461	29	20
462	29	23
463	29	10
464	29	11
465	29	13
466	29	35
467	29	37
468	29	30
469	29	21
470	29	9
471	29	14
472	29	16
473	29	26
474	29	32
475	29	38
476	29	33
477	29	12
478	29	27
479	29	28
480	29	36
481	29	34
482	30	29
483	30	17
484	30	11
485	30	16
486	30	9
487	30	26
488	30	37
489	30	15
490	30	8
491	30	19
492	30	12
493	30	22
494	30	18
495	30	20
496	32	29
497	32	35
498	32	38
499	32	33
500	32	18
501	32	23
502	32	17
503	32	19
504	34	18
505	34	20
506	34	9
507	34	10
508	34	32
509	34	27
510	34	13
511	34	28
512	34	29
513	34	11
514	34	33
515	34	12
516	34	30
517	34	15
518	34	38
519	34	8
520	34	34
521	34	14
522	34	19
523	34	36
524	34	37
525	34	26
526	34	35
527	34	17
528	34	21
529	34	30
530	34	16
531	35	30
532	35	30
533	35	34
534	35	17
535	35	38
536	35	36
537	35	18
538	35	23
539	35	20
540	35	37
541	35	33
542	35	8
543	35	16
544	35	19
545	35	15
546	36	27
547	36	18
548	36	9
549	36	22
550	36	25
551	36	35
552	36	11
553	36	38
554	36	20
555	36	33
556	36	36
557	36	34
558	36	30
559	36	12
560	36	19
561	36	13
562	36	24
563	36	10
564	36	17
565	36	8
566	36	37
567	39	13
568	39	19
569	39	18
570	39	11
571	39	9
572	39	30
573	39	17
574	39	35
575	39	14
576	40	14
577	40	38
578	40	21
579	40	19
580	40	34
581	40	30
582	40	15
583	40	10
584	40	28
585	40	30
586	40	18
587	40	26
588	40	17
589	40	20
590	40	33
591	40	11
592	40	13
593	41	19
594	41	38
595	41	11
596	41	20
597	41	8
598	41	36
599	41	32
600	41	12
601	41	15
602	41	33
603	41	35
604	41	26
605	41	18
606	41	29
607	42	9
608	42	34
609	42	11
610	42	16
611	42	14
612	42	29
613	42	8
614	42	25
615	42	21
616	42	35
617	42	12
618	42	18
619	42	19
620	42	33
621	42	15
622	44	22
623	44	30
624	44	11
625	44	13
626	44	12
627	44	27
628	44	28
629	44	32
630	44	26
631	44	23
632	44	10
633	44	24
634	44	19
635	44	18
636	44	29
637	44	17
638	44	15
639	44	9
640	44	36
641	44	30
642	44	8
643	44	21
644	44	20
645	44	16
646	44	14
647	44	35
648	44	25
649	44	38
650	44	37
651	46	36
652	46	24
653	46	8
654	46	37
655	46	25
656	46	26
657	46	12
658	46	14
659	46	19
660	46	16
661	46	18
662	46	9
663	46	38
664	46	28
665	46	34
666	46	32
667	46	30
668	46	15
669	46	23
670	46	20
671	46	17
672	46	11
673	46	29
674	46	21
675	46	13
676	46	22
677	46	10
678	46	33
679	46	27
680	47	36
681	47	25
682	47	13
683	47	16
684	47	17
685	47	26
686	47	30
687	47	8
688	49	18
689	49	14
690	49	25
691	49	38
692	49	30
693	50	8
694	50	27
695	50	24
696	50	20
697	50	12
698	50	32
699	50	22
700	50	26
701	51	29
702	51	9
703	51	10
704	51	11
705	51	16
706	51	26
707	51	22
708	51	33
709	51	23
710	51	24
711	51	34
712	51	14
713	51	17
714	51	38
715	51	36
716	51	12
717	51	28
718	51	18
719	51	30
720	51	25
721	51	37
722	51	15
723	54	29
724	54	17
725	54	18
726	54	25
727	54	28
728	54	22
729	54	26
730	55	13
731	55	28
732	55	22
733	55	36
734	55	24
735	55	17
736	55	30
737	55	27
738	55	10
739	55	34
740	55	8
741	55	12
742	55	37
743	55	35
744	55	33
745	55	18
746	55	29
747	55	16
748	55	9
749	55	14
750	55	21
751	55	23
752	55	20
753	56	37
754	56	8
755	56	15
756	56	30
757	56	10
758	56	28
759	56	30
760	56	12
761	56	9
762	56	32
763	56	24
764	56	17
765	56	22
766	56	27
767	56	21
768	57	16
769	57	38
770	57	25
771	57	29
772	57	11
773	57	27
774	57	8
775	57	34
776	57	30
777	57	36
778	57	37
779	57	32
780	57	19
781	58	21
782	58	24
783	58	19
784	58	30
785	58	28
786	58	33
787	58	9
788	59	9
789	59	35
790	59	15
791	59	16
792	59	17
793	59	37
794	59	12
795	59	10
796	59	21
797	60	20
798	60	35
799	60	21
800	60	27
801	60	13
802	60	18
803	60	30
804	60	17
805	60	16
806	60	36
807	60	12
808	60	8
809	60	23
810	60	26
811	60	24
812	60	32
813	60	33
814	60	38
815	60	37
816	60	9
817	60	10
818	60	11
819	60	28
820	60	25
821	60	29
822	60	14
823	60	34
824	60	22
825	60	19
826	61	30
827	61	26
828	61	21
829	61	25
830	61	29
831	61	9
832	61	28
833	61	13
834	61	14
835	61	32
836	61	18
837	61	16
838	61	35
839	61	10
840	61	17
841	61	37
842	61	38
843	61	33
844	61	34
845	61	30
846	61	24
847	61	36
848	62	17
849	62	24
850	62	10
851	62	25
852	62	32
853	62	26
854	62	8
855	62	11
856	62	37
857	62	12
858	62	34
859	62	28
860	62	29
861	62	30
862	62	38
863	62	21
864	62	16
865	63	8
866	63	38
867	63	32
868	63	20
869	63	35
870	63	24
871	63	14
872	63	28
873	63	21
874	63	27
875	63	10
876	63	9
877	63	34
878	63	16
879	63	26
880	63	17
881	63	13
882	63	30
883	63	30
884	63	12
885	64	12
886	64	9
887	64	27
888	64	16
889	64	25
890	64	19
891	64	11
892	64	14
893	64	23
894	64	33
895	64	18
896	64	32
897	64	34
898	64	26
899	64	22
900	64	20
901	64	21
902	64	8
903	64	24
904	64	35
905	64	36
906	64	30
907	64	17
908	64	28
909	64	30
910	6	10
911	6	20
912	6	33
913	6	35
914	6	15
915	6	9
916	6	34
917	6	28
918	6	14
919	6	11
920	6	22
921	6	19
922	6	23
923	6	21
924	6	24
925	6	26
926	6	13
927	6	8
928	6	36
929	6	16
930	6	30
931	6	17
932	6	32
933	6	37
934	6	18
935	6	27
936	6	29
937	6	30
938	7	19
939	7	29
940	7	17
941	7	14
942	7	32
943	7	30
944	7	21
945	7	34
946	7	26
947	7	15
948	7	16
949	7	36
950	7	20
951	7	25
952	9	21
953	9	30
954	9	25
955	9	10
956	9	16
957	9	37
958	9	22
959	9	15
960	9	14
961	9	19
962	9	29
963	9	30
964	9	9
965	13	8
966	13	17
967	13	14
968	13	28
969	13	33
970	13	11
971	13	15
972	13	18
973	13	27
974	13	23
975	13	10
976	13	24
977	13	21
978	13	37
979	13	26
980	13	19
981	13	38
982	13	13
983	14	27
984	14	14
985	14	21
986	14	16
987	14	15
988	14	38
989	14	22
990	14	30
991	14	34
992	14	26
993	14	18
994	14	10
995	14	37
996	14	29
997	14	36
998	14	17
999	14	12
1000	14	25
1001	14	19
1002	14	9
1003	14	30
1004	14	33
1005	14	8
1006	14	13
1007	14	35
1008	18	16
1009	18	30
1010	18	20
1011	18	18
1012	18	38
1013	18	33
1014	18	24
1015	18	8
1016	18	32
1017	18	37
1018	18	35
1019	18	26
1020	18	22
1021	22	26
1022	22	36
1023	22	18
1024	22	27
1025	22	8
1026	22	33
1027	22	9
1028	22	34
1029	22	10
1030	22	35
1031	22	24
1032	25	35
1033	25	30
1034	25	37
1035	25	11
1036	31	27
1037	31	21
1038	31	25
1039	31	34
1040	31	20
1041	31	14
1042	31	30
1043	31	35
1044	31	24
1045	31	15
1046	31	37
1047	31	30
1048	31	36
1049	33	23
1050	33	10
1051	33	24
1052	33	32
1053	33	30
1054	33	19
1055	33	11
1056	33	26
1057	33	34
1058	33	33
1059	33	21
1060	33	30
1061	33	36
1062	33	17
1063	33	18
1064	33	27
1065	33	38
1066	33	16
1067	37	20
1068	37	30
1069	37	33
1070	37	19
1071	37	25
1072	37	10
1073	37	34
1074	37	9
1075	37	21
1076	37	13
1077	37	12
1078	37	14
1079	37	22
1080	37	15
1081	37	38
1082	37	37
1083	37	24
1084	37	16
1085	37	27
1086	37	8
1087	37	28
1088	37	17
1089	37	36
1090	37	18
1091	37	23
1092	38	28
1093	38	30
1094	38	34
1095	38	37
1096	38	12
1097	38	27
1098	38	36
1099	38	25
1100	38	8
1101	38	23
1102	38	10
1103	38	20
1104	38	35
1105	38	18
1106	38	21
1107	38	16
1108	38	9
1109	38	15
1110	38	30
1111	38	29
1112	38	38
1113	38	19
1114	38	22
1115	38	33
1116	38	24
1117	38	17
1118	38	26
1119	38	32
1120	43	30
1121	43	25
1122	43	18
1123	43	29
1124	43	22
1125	43	11
1126	43	13
1127	43	15
1128	43	38
1129	43	20
1130	43	21
1131	43	26
1132	43	14
1133	43	27
1134	43	32
1135	43	17
1136	45	10
1137	45	11
1138	45	17
1139	45	18
1140	45	34
1141	45	12
1142	45	21
1143	45	29
1144	45	36
1145	45	9
1146	45	38
1147	45	30
1148	48	35
1149	48	9
1150	48	8
1151	48	34
1152	48	37
1153	48	12
1154	48	11
1155	48	18
1156	48	22
1157	48	30
1158	48	28
1159	48	16
1160	48	32
1161	48	13
1162	48	30
1163	52	26
1164	52	12
1165	52	33
1166	52	38
1167	52	30
1168	52	24
1169	52	30
1170	52	13
1171	52	17
1172	52	16
1173	52	35
1174	52	22
1175	52	15
1176	52	21
1177	52	20
1178	52	19
1179	52	32
1180	52	36
1181	53	21
1182	53	28
1183	53	17
1184	53	27
1185	53	9
1186	53	29
1187	53	10
1188	53	22
1189	53	16
1190	53	20
1191	53	24
1192	53	38
1193	53	15
1194	53	30
1195	53	12
1196	53	32
1197	53	8
1198	53	35
1199	53	37
1200	53	25
1201	53	30
\.


--
-- Name: seen_arguments_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('seen_arguments_uid_seq', 1201, true);


--
-- Data for Name: seen_statements; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY seen_statements (uid, statement_uid, user_uid) FROM stdin;
76	1	10
77	1	26
78	1	11
79	1	32
80	1	33
81	1	29
82	1	24
83	1	17
84	1	13
85	1	18
86	1	30
87	1	28
88	1	19
89	1	21
90	1	23
91	1	8
92	1	37
93	1	35
94	1	34
95	1	38
96	1	14
97	1	25
98	1	15
99	1	22
100	2	16
101	2	27
102	2	24
103	2	10
104	2	20
105	2	15
106	2	29
107	2	8
108	2	19
109	2	35
110	2	23
111	2	11
112	2	37
113	2	13
114	2	32
115	2	26
116	2	21
117	2	17
118	2	25
119	2	28
120	2	12
121	2	38
122	2	18
123	2	34
124	2	36
125	2	30
126	3	30
127	3	35
128	3	17
129	3	25
130	3	9
131	3	22
132	3	38
133	3	23
134	3	13
135	3	37
136	3	27
137	3	10
138	3	19
139	3	12
140	3	32
141	3	30
142	3	24
143	3	33
144	4	10
145	4	29
146	4	38
147	4	24
148	4	23
149	4	28
150	4	18
151	4	14
152	4	34
153	4	12
154	5	36
155	5	16
156	5	9
157	5	20
158	5	35
159	5	30
160	5	8
161	5	29
162	5	30
163	5	23
164	5	21
165	5	19
166	5	10
167	5	22
168	5	26
169	5	28
170	5	34
171	6	8
172	6	35
173	6	36
174	6	29
175	7	38
176	7	36
177	7	27
178	7	13
179	7	34
180	7	12
181	7	29
182	7	8
183	7	32
184	7	18
185	7	20
186	7	17
187	7	19
188	7	24
189	8	30
190	8	15
191	8	24
192	8	9
193	8	25
194	8	17
195	8	8
196	8	11
197	8	32
198	8	36
199	8	19
200	9	21
201	9	8
202	9	35
203	9	12
204	9	30
205	9	14
206	9	22
207	9	20
208	9	10
209	9	13
210	9	34
211	9	32
212	9	9
213	9	11
214	9	18
215	9	28
216	9	25
217	9	16
218	10	29
219	10	34
220	10	35
221	10	30
222	10	18
223	10	25
224	10	12
225	10	26
226	10	14
227	10	37
228	10	33
229	10	15
230	10	23
231	10	32
232	11	18
233	11	10
234	11	29
235	11	21
236	11	28
237	11	16
238	11	36
239	12	11
240	12	9
241	12	10
242	12	20
243	12	25
244	12	26
245	12	8
246	12	16
247	12	29
248	12	15
249	12	27
250	12	35
251	12	22
252	12	23
253	12	17
254	12	30
255	12	30
256	12	12
257	12	18
258	12	38
259	12	34
260	12	21
261	12	32
262	12	19
263	13	23
264	13	22
265	13	24
266	13	27
267	13	18
268	13	28
269	13	34
270	13	13
271	13	9
272	13	29
273	14	17
274	14	12
275	14	36
276	14	28
277	14	23
278	14	38
279	14	20
280	14	33
281	14	37
282	14	21
283	14	24
284	14	30
285	14	14
286	14	19
287	15	30
288	15	24
289	15	21
290	15	18
291	16	35
292	16	30
293	16	10
294	16	37
295	16	29
296	16	17
297	16	19
298	16	33
299	16	32
300	16	23
301	16	14
302	16	18
303	16	8
304	17	25
305	17	9
306	17	30
307	17	10
308	17	32
309	18	27
310	18	29
311	18	30
312	18	11
313	18	25
314	18	28
315	18	34
316	18	30
317	18	23
318	18	15
319	18	37
320	18	12
321	18	20
322	18	16
323	18	17
324	18	22
325	18	13
326	18	14
327	19	9
328	19	28
329	19	33
330	19	15
331	19	36
332	19	25
333	19	10
334	19	8
335	19	32
336	19	19
337	19	30
338	19	14
339	19	37
340	19	29
341	19	30
342	19	21
343	19	20
344	19	26
345	20	30
346	20	15
347	20	8
348	20	24
349	20	12
350	20	17
351	20	10
352	20	13
353	20	36
354	20	21
355	20	9
356	20	32
357	20	14
358	20	34
359	20	25
360	20	19
361	20	29
362	20	26
363	20	11
364	21	11
365	21	23
366	21	17
367	21	36
368	21	22
369	21	25
370	21	37
371	21	28
372	21	16
373	21	30
374	22	19
375	22	16
376	22	23
377	22	12
378	22	8
379	22	38
380	22	20
381	22	33
382	22	10
383	22	18
384	22	9
385	22	30
386	22	11
387	22	36
388	22	17
389	23	29
390	23	8
391	23	9
392	23	18
393	23	36
394	23	30
395	23	16
396	23	12
397	23	20
398	23	17
399	23	19
400	24	24
401	24	10
402	24	16
403	24	27
404	24	25
405	25	13
406	25	26
407	25	30
408	25	22
409	25	28
410	25	34
411	25	27
412	25	21
413	25	17
414	25	25
415	25	11
416	25	33
417	25	14
418	25	8
419	25	29
420	25	38
421	25	20
422	25	24
423	25	10
424	25	18
425	25	35
426	25	32
427	25	12
428	25	37
429	25	9
430	25	16
431	25	15
432	25	30
433	26	21
434	26	17
435	26	35
436	26	37
437	26	12
438	26	27
439	26	19
440	26	9
441	26	36
442	26	8
443	27	22
444	27	33
445	27	28
446	27	9
447	27	27
448	27	30
449	27	36
450	27	21
451	27	32
452	27	37
453	27	8
454	27	11
455	27	26
456	27	23
457	27	38
458	28	30
459	28	22
460	28	30
461	28	10
462	28	16
463	28	21
464	28	15
465	28	12
466	28	9
467	28	27
468	28	32
469	28	14
470	28	13
471	28	20
472	28	23
473	28	35
474	28	28
475	28	25
476	28	37
477	28	17
478	28	24
479	29	29
480	29	8
481	29	18
482	29	36
483	29	37
484	29	20
485	29	24
486	29	33
487	29	15
488	29	30
489	29	12
490	29	21
491	29	19
492	29	30
493	29	11
494	29	27
495	29	17
496	29	23
497	29	34
498	29	22
499	29	38
500	29	35
501	29	16
502	29	28
503	29	10
504	29	32
505	29	13
506	29	14
507	30	14
508	30	10
509	30	12
510	30	29
511	30	35
512	30	25
513	31	25
514	31	29
515	31	37
516	31	27
517	31	24
518	31	26
519	31	38
520	31	30
521	31	20
522	31	13
523	31	18
524	32	21
525	32	30
526	32	38
527	32	10
528	32	30
529	32	18
530	32	9
531	32	13
532	32	8
533	32	37
534	32	36
535	32	28
536	32	27
537	32	19
538	32	12
539	32	16
540	32	23
541	32	33
542	32	14
543	32	15
544	32	22
545	33	21
546	33	30
547	33	15
548	33	19
549	33	26
550	33	16
551	33	22
552	33	29
553	34	30
554	34	38
555	34	17
556	34	20
557	34	37
558	34	14
559	34	11
560	34	22
561	34	36
562	34	9
563	34	25
564	34	16
565	34	8
566	34	24
567	35	25
568	35	13
569	35	30
570	35	18
571	35	21
572	35	10
573	35	28
574	35	35
575	35	15
576	35	34
577	35	9
578	35	23
579	35	14
580	35	32
581	35	36
582	35	17
583	35	24
584	35	26
585	35	8
586	35	16
587	35	29
588	35	37
589	35	33
590	35	38
591	35	20
592	36	25
593	36	13
594	36	21
595	36	8
596	36	30
597	36	19
598	36	33
599	36	26
600	36	9
601	36	28
602	36	32
603	36	23
604	36	16
605	36	29
606	36	36
607	36	27
608	36	11
609	36	34
610	36	12
611	36	14
612	36	22
613	37	37
614	37	24
615	37	12
616	37	33
617	37	34
618	37	28
619	37	38
620	37	23
621	37	26
622	37	11
623	37	21
624	37	27
625	37	35
626	37	25
627	37	30
628	37	13
629	37	15
630	37	8
631	37	30
632	37	9
633	37	17
634	37	10
635	37	22
636	37	19
637	37	18
638	37	29
639	38	20
640	38	27
641	38	16
642	38	30
643	38	26
644	38	13
645	38	34
646	38	22
647	38	11
648	38	14
649	38	21
650	38	29
651	38	35
652	38	8
653	38	17
654	38	18
655	38	32
656	38	37
657	38	28
658	38	24
659	38	23
660	38	33
661	38	30
662	38	10
663	39	27
664	39	24
665	39	38
666	39	30
667	39	22
668	39	20
669	39	9
670	39	32
671	39	26
672	39	17
673	39	23
674	39	13
675	39	15
676	39	33
677	39	19
678	39	30
679	39	25
680	39	14
681	39	21
682	39	29
683	39	8
684	39	12
685	39	18
686	39	10
687	39	35
688	39	36
689	39	28
690	40	14
691	40	11
692	40	27
693	40	25
694	40	36
695	40	29
696	40	20
697	40	13
698	40	38
699	41	18
700	41	38
701	41	9
702	41	12
703	41	26
704	41	27
705	41	29
706	41	23
707	41	32
708	41	35
709	41	34
710	41	30
711	41	33
712	41	24
713	42	27
714	42	37
715	42	8
716	42	12
717	42	24
718	42	14
719	42	28
720	42	38
721	42	36
722	42	22
723	42	18
724	42	23
725	42	20
726	43	12
727	43	17
728	43	15
729	43	33
730	43	16
731	44	30
732	44	17
733	44	35
734	44	26
735	44	19
736	45	15
737	45	30
738	45	9
739	45	10
740	45	28
741	45	16
742	45	37
743	45	36
744	45	12
745	45	29
746	45	13
747	45	8
748	45	22
749	45	32
750	45	26
751	45	17
752	45	34
753	45	33
754	45	19
755	45	23
756	45	20
757	45	24
758	45	27
759	45	21
760	45	18
761	45	11
762	45	14
763	45	38
764	45	30
765	46	24
766	46	30
767	46	25
768	46	35
769	46	22
770	46	29
771	46	12
772	46	37
773	46	33
774	46	36
775	46	32
776	46	14
777	46	34
778	46	10
779	46	11
780	46	30
781	46	19
782	46	15
783	46	13
784	46	9
785	46	27
786	46	26
787	47	30
788	47	17
789	47	35
790	47	13
791	47	26
792	47	23
793	47	18
794	47	12
795	47	16
796	47	38
797	47	36
798	47	21
799	47	15
800	47	33
801	47	8
802	47	30
803	47	22
804	47	32
805	47	14
806	47	10
807	47	28
808	47	34
809	47	19
810	47	20
811	47	27
812	47	29
813	47	11
814	47	9
815	48	26
816	48	9
817	48	16
818	48	21
819	48	11
820	48	29
821	48	12
822	48	27
823	48	17
824	48	37
825	48	20
826	48	30
827	48	22
828	48	10
829	48	33
830	48	38
831	48	15
832	48	19
833	48	32
834	48	25
835	48	14
836	48	36
837	48	28
838	48	18
839	48	35
840	48	8
841	48	13
842	48	34
843	49	18
844	49	23
845	49	27
846	49	33
847	49	20
848	49	24
849	49	10
850	49	17
851	49	8
852	49	26
853	49	14
854	49	30
855	49	32
856	49	16
857	49	12
858	49	22
859	49	28
860	49	30
861	49	11
862	49	15
863	49	21
864	49	35
865	49	38
866	49	37
867	49	19
868	49	36
869	49	29
870	49	34
871	50	21
872	50	20
873	50	37
874	50	35
875	50	28
876	50	27
877	50	13
878	50	36
879	50	32
880	50	8
881	50	23
882	50	24
883	50	19
884	50	10
885	50	12
886	50	17
887	50	29
888	50	22
889	50	30
890	50	25
891	50	9
892	51	30
893	51	24
894	51	10
895	51	19
896	51	21
897	51	12
898	51	29
899	51	28
900	52	20
901	52	11
902	52	26
903	52	8
904	52	23
905	52	19
906	52	12
907	52	28
908	52	21
909	52	18
910	52	25
911	52	29
912	52	30
913	52	27
914	52	38
915	52	24
916	52	35
917	52	30
918	52	16
919	52	9
920	52	34
921	52	33
922	52	14
923	52	10
924	52	17
925	52	13
926	53	37
927	53	14
928	53	28
929	53	17
930	53	11
931	53	25
932	53	24
933	53	27
934	53	30
935	53	35
936	53	22
937	53	12
938	53	20
939	53	38
940	53	29
941	53	36
942	53	23
943	53	26
944	53	34
945	53	8
946	53	30
947	54	33
948	54	36
949	54	34
950	54	15
951	54	26
952	54	21
953	54	35
954	54	29
955	54	37
956	54	10
957	54	22
958	54	13
959	54	32
960	54	19
961	55	32
962	55	22
963	55	38
964	55	17
965	55	25
966	55	19
967	55	20
968	55	30
969	55	21
970	56	16
971	56	13
972	56	27
973	56	22
974	56	24
975	56	9
976	57	13
977	57	24
978	57	27
979	57	16
980	57	14
981	57	25
982	57	12
983	57	15
984	57	34
985	57	19
986	57	18
987	57	28
988	57	17
989	57	38
990	57	35
991	57	22
992	57	37
993	57	20
994	57	8
995	57	9
996	57	36
997	57	30
998	57	33
999	57	21
1000	57	29
1001	57	11
1002	57	30
1003	58	28
1004	58	26
1005	58	17
1006	58	22
1007	58	14
1008	58	25
1009	58	8
1010	58	19
1011	58	12
1012	58	13
1013	58	11
1014	58	34
1015	58	21
1016	58	20
1017	58	36
1018	58	30
1019	58	33
1020	58	29
1021	58	23
1022	59	27
1023	59	30
1024	59	11
1025	59	37
1026	59	21
1027	59	38
1028	59	28
1029	59	8
1030	59	15
1031	59	22
1032	59	33
1033	59	16
1034	59	20
1035	59	30
1036	59	9
1037	59	10
1038	59	25
1039	59	35
1040	59	26
1041	59	29
1042	60	16
1043	60	35
1044	60	37
1045	60	34
1046	60	38
1047	60	29
1048	60	9
1049	61	19
1050	61	27
1051	61	30
1052	61	8
1053	61	25
1054	61	30
1055	61	18
1056	61	36
1057	61	16
1058	61	9
1059	61	22
1060	61	23
1061	61	12
1062	61	26
1063	61	38
1064	61	29
1065	61	11
1066	61	10
1067	61	17
1068	61	32
1069	61	13
1070	61	24
1071	61	37
1072	61	35
1073	62	22
1074	62	16
1075	62	24
1076	62	14
1077	62	19
1078	62	8
1079	62	38
1080	62	28
1081	62	29
1082	62	25
1083	62	13
1084	62	37
1085	62	23
1086	62	15
1087	62	32
1088	62	36
1089	62	20
1090	62	18
1091	62	33
1092	62	27
1093	62	30
1094	62	9
1095	62	11
1096	62	12
1097	62	21
1098	62	26
1099	63	19
1100	63	10
1101	63	17
1102	63	27
1103	63	8
1104	63	20
1105	63	32
1106	63	29
1107	63	25
1108	63	28
1109	63	9
1110	63	26
1111	63	15
1112	63	35
1113	63	16
1114	63	22
1115	63	34
1116	63	33
1117	63	11
1118	63	37
1119	63	12
1120	63	38
1121	63	23
1122	63	24
1123	63	36
1124	63	14
1125	63	30
1126	63	30
1127	64	25
1128	64	18
1129	64	11
1130	64	22
1131	64	30
1132	64	10
1133	64	36
1134	65	22
1135	65	33
1136	65	37
1137	65	9
1138	65	34
1139	65	35
1140	66	23
1141	66	33
1142	66	16
1143	66	21
1144	66	9
1145	66	29
1146	66	22
1147	66	28
1148	66	14
1149	67	11
1150	67	12
1151	67	10
1152	67	27
1153	67	16
1154	67	14
1155	67	36
1156	67	29
1157	67	15
1158	67	13
1159	67	18
1160	67	25
1161	67	34
1162	67	21
1163	67	28
1164	67	22
1165	67	30
1166	67	35
1167	67	30
1168	67	19
1169	67	24
1170	67	20
1171	67	26
1172	67	37
1173	67	8
1174	67	9
1175	67	17
1176	67	32
1177	68	15
1178	68	35
1179	68	11
1180	68	24
1181	68	36
1182	68	10
1183	68	18
1184	69	19
1185	69	27
1186	69	32
1187	69	36
1188	69	12
1189	69	22
1190	69	38
1191	69	16
1192	69	37
1193	69	18
1194	69	9
1195	69	10
1196	69	24
1197	69	17
1198	69	28
1199	69	29
1200	69	20
1201	69	13
1202	69	33
1203	69	30
1204	69	14
1205	69	8
1206	69	30
1207	69	15
1208	69	35
1209	69	11
1210	69	34
1211	70	8
1212	70	30
1213	70	16
1214	70	22
1215	70	20
1216	70	9
1217	70	33
1218	70	23
1219	70	35
1220	70	38
1221	70	11
1222	70	12
1223	70	25
1224	70	26
1225	71	8
1226	71	21
1227	71	30
1228	71	11
1229	71	35
1230	71	37
1231	71	36
1232	71	19
1233	71	33
1234	71	20
1235	71	22
1236	71	15
1237	71	10
1238	71	28
1239	71	29
1240	71	12
1241	71	24
1242	71	16
1243	72	20
1244	72	30
1245	72	25
1246	72	30
1247	72	32
1248	72	9
1249	72	19
1250	72	29
1251	72	16
1252	72	38
1253	72	14
1254	72	18
1255	72	24
1256	72	15
1257	72	33
1258	72	21
1259	73	36
1260	73	28
1261	73	16
1262	73	30
1263	73	24
1264	73	15
1265	73	33
1266	73	17
1267	73	14
1268	73	18
1269	73	32
1270	73	30
1271	73	12
1272	73	9
1273	73	37
1274	73	13
1275	73	38
1276	73	22
1277	73	25
1278	73	19
1279	73	23
1280	74	37
1281	74	9
1282	74	36
1283	74	13
1284	74	23
1285	74	15
1286	74	26
1287	74	24
1288	74	8
1289	75	9
1290	75	16
1291	75	17
1292	75	19
1293	75	14
1294	75	28
1295	75	22
1296	75	33
1297	75	36
1298	75	30
1299	75	24
1300	75	10
1301	75	13
1302	75	29
1303	75	15
1304	75	21
1305	75	12
1306	75	30
1307	75	27
1308	75	8
1309	75	26
1310	75	25
1311	75	23
1312	75	32
\.


--
-- Name: seen_statements_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('seen_statements_uid_seq', 1312, true);


--
-- Data for Name: settings; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY settings (author_uid, should_send_mails, should_send_notifications, should_show_public_nickname, last_topic_uid, lang_uid, keep_logged_in) FROM stdin;
1	f	t	t	1	2	f
2	f	t	t	1	2	f
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
3	Katzen sind kleine Tiger	http://www.iflscience.com/	plants-and-animals/no-your-cat-isnt-plotting-kill-youbut-it-has-lions-personality/	2	15	2	2017-03-09 12:37:50.818831
4	Katzen sind kleine Tiger	http://www.iflscience.com/	plants-and-animals/no-your-cat-isnt-plotting-kill-youbut-it-has-lions-personality/	2	16	2	2017-03-09 12:37:50.818831
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
51	52	the city is planing a new park in the upcoming month	1	2017-02-16 12:37:53.071393	f
53	54	our swimming pools are very old and it would take a major investment to repair them	1	2017-03-09 12:37:53.07148	f
35	36	the city should reduce the number of street festivals	1	2017-02-27 12:37:53.070674	f
1	2	we should get a cat	1	2017-02-25 12:37:53.069063	f
2	3	we should get a dog	1	2017-02-26 12:37:53.069205	f
3	4	we could get both, a cat and a dog	1	2017-02-27 12:37:53.06927	f
4	5	cats are very independent	1	2017-03-05 12:37:53.069323	f
5	6	cats are capricious	1	2017-03-01 12:37:53.069371	f
6	7	dogs can act as watch dogs	1	2017-03-01 12:37:53.069416	f
7	8	you have to take the dog for a walk every day, which is tedious	1	2017-02-24 12:37:53.069461	f
8	9	we have no use for a watch dog	1	2017-02-16 12:37:53.069505	f
9	10	going for a walk with the dog every day is good for social interaction and physical exercise	1	2017-02-26 12:37:53.069548	f
10	11	it would be no problem	1	2017-02-20 12:37:53.069591	f
11	12	a cat and a dog will generally not get along well	1	2017-03-02 12:37:53.069634	f
12	13	we do not have enough money for two pets	1	2017-02-24 12:37:53.069676	f
13	14	a dog costs taxes and will be more expensive than a cat	1	2017-03-04 12:37:53.06972	f
14	15	cats are fluffy	1	2017-02-14 12:37:53.069764	f
15	16	cats are small	1	2017-03-09 12:37:53.06981	f
16	17	fluffy animals losing much hair and I'm allergic to animal hair	1	2017-02-26 12:37:53.069855	f
17	18	you could use a automatic vacuum cleaner	1	2017-02-25 12:37:53.069898	f
18	19	cats ancestors are animals in wildlife, who are hunting alone and not in groups	1	2017-03-02 12:37:53.069941	f
19	20	this is not true for overbred races	1	2017-03-07 12:37:53.069985	f
20	21	this lies in their the natural conditions	1	2017-02-27 12:37:53.070029	f
21	22	the purpose of a pet is to have something to take care of	1	2017-03-06 12:37:53.070072	f
22	23	several cats of friends of mine are real as*holes	1	2017-02-20 12:37:53.070116	f
23	24	the fact, that cats are capricious, is based on the cats race	1	2017-02-17 12:37:53.070159	f
24	25	not every cat is capricious	1	2017-03-04 12:37:53.070202	f
25	26	this is based on the cats race and a little bit on the breeding	1	2017-02-25 12:37:53.070245	f
26	27	next to the taxes you will need equipment like a dog lead, anti-flea-spray, and so on	1	2017-03-06 12:37:53.070288	f
27	28	the equipment for running costs of cats and dogs are nearly the same	1	2017-03-06 12:37:53.070332	f
28	29	this is just a claim without any justification	1	2017-02-14 12:37:53.070375	f
29	30	in Germany you have to pay for your second dog even more taxes!	1	2017-02-13 12:37:53.070417	f
30	31	it is important, that pets are small and fluffy!	1	2017-02-25 12:37:53.07046	f
31	32	cats are little, sweet and innocent cuddle toys	1	2017-02-28 12:37:53.070503	f
32	33	do you have ever seen a sphinx cat or savannah cats?	1	2017-03-08 12:37:53.070545	f
33	34	it is much work to take care of both animals	1	2017-03-06 12:37:53.070588	f
34	35	won't be best friends	1	2017-02-24 12:37:53.070631	f
37	38	we should close public swimming pools	1	2017-02-27 12:37:53.07076	f
38	39	reducing the number of street festivals can save up to $50.000 a year	1	2017-02-26 12:37:53.070803	f
39	40	every street festival is funded by large companies	1	2017-02-19 12:37:53.070845	f
40	41	then we will have more money to expand out pedestrian zone	1	2017-02-16 12:37:53.070888	f
41	42	our city will get more attractive for shopping	1	2017-02-12 12:37:53.070931	f
42	43	street festivals attract many people, which will increase the citys income	1	2017-03-08 12:37:53.070974	f
43	44	spending of the city for these festivals are higher than the earnings	1	2017-02-26 12:37:53.071017	f
44	45	money does not solve problems of our society	1	2017-02-27 12:37:53.07106	f
45	46	criminals use University Park to sell drugs	1	2017-02-16 12:37:53.071102	f
46	47	shutting down University Park will save $100.000 a year	1	2017-03-05 12:37:53.071144	f
47	48	we should not give in to criminals	1	2017-03-06 12:37:53.071212	f
48	49	the number of police patrols has been increased recently	1	2017-03-09 12:37:53.071262	f
49	50	this is the only park in our city	1	2017-02-16 12:37:53.071306	f
50	51	there are many parks in neighbouring towns	1	2017-02-19 12:37:53.071349	f
54	55	schools need the swimming pools for their sports lessons	1	2017-02-14 12:37:53.071522	f
55	56	the rate of non-swimmers is too high	1	2017-02-16 12:37:53.071565	f
56	57	the police cannot patrol in the park for 24/7	1	2017-03-04 12:37:53.071608	f
57	58	E-Autos "optimal" für den Stadtverkehr sind	1	2017-02-18 12:37:53.071651	f
58	59	dadurch die Lärmbelästigung in der Stadt sinkt	1	2017-02-18 12:37:53.071694	f
59	60	die Anzahl an Ladestationen in der Stadt nicht ausreichend ist	1	2017-02-18 12:37:53.071738	f
60	61	das Unfallrisiko steigt, da die Autos kaum Geräusche verursachen	1	2017-02-28 12:37:53.07178	f
61	62	die Autos auch zuhause geladen werden können und das pro Tag ausreichen sollte	1	2017-02-19 12:37:53.071823	f
62	63	Elektroautos keine lauten Geräusche beim Anfahren produzieren	1	2017-03-07 12:37:53.071866	f
63	64	Lärmbelästigung kein wirkliches Problem in den Städten ist	1	2017-02-23 12:37:53.071909	f
64	65	nicht jede normale Tankstelle auch Stromtankstellen hat	1	2017-02-18 12:37:53.071952	f
65	66	die Länder und Kommunen den Ausbau nun stark fördern wollen	1	2017-02-23 12:37:53.071995	f
68	69	durch rücksichtsvolle Verhaltensanpassungen der wissenschaftlichen Mitarbeitenden der Arbeitsaufwand der Sekretärinnen gesenkt werden könnte	1	2017-03-02 12:37:53.072122	f
69	70	wir Standard-Formulare, wie Urlaubsanträge, selbst faxen können	1	2017-02-25 12:37:53.072164	f
74	75	wir keine eigenen Faxgeräte haben und so oder so entweder bei Martin stören müssten oder doch bei Sabine im Büro landen würden	1	2017-02-13 12:37:53.072376	f
36	37	we should shut down University Park	1	2017-02-22 12:37:53.070717	f
52	53	parks are very important for our climate	1	2017-02-21 12:37:53.071437	f
66	67	E-Autos das autonome Fahren vorantreiben	8	2017-02-13 12:37:53.072037	f
67	68	Tesla mutig bestehende Techniken einsetzt und zeigt was sie können	8	2017-03-08 12:37:53.07208	f
70	71	etliche Abläufe durch ein besseres Zusammenarbeiten optimiert werden können. Dies sollte auch schriftlich als Anleitungen festgehalten werden, damit neue Angestellt einen leichten Einstieg finden	1	2017-02-17 12:37:53.072206	f
71	72	viele Arbeiten auch durch die Mitarbeiter erledigt werden können	1	2017-03-04 12:37:53.072249	f
72	73	"rücksichtsvolle Verhaltensanpassungen" viel zu allgemein gehalten ist	1	2017-02-25 12:37:53.072292	f
73	74	das Faxgerät nicht immer zugänglich ist, wenn die Sekretärinnen nicht anwesend sind	1	2017-02-27 12:37:53.072334	f
75	1	Cats are fucking stupid and bloody fuzzy critters!	1	2017-03-02 12:37:53.072419	f
\.


--
-- Name: textversions_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: dbas
--

SELECT pg_catalog.setval('textversions_uid_seq', 75, true);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: dbas
--

COPY users (uid, firstname, surname, nickname, public_nickname, email, gender, password, group_uid, last_action, last_login, registered, token, token_timestamp) FROM stdin;
1	anonymous	anonymous	anonymous	anonymous		m	$2a$10$GGVmK7DIXrtGIXI0FMzFtOMVmklZ.SsAjQzceKOx8SxksYALqDC9S	3	2017-03-09 12:37:50.805069	2017-03-09 12:37:50.805234	2017-03-09 12:37:50.805376		\N
2	admin	admin	admin	admin	dbas.hhu@gmail.com	m	$2a$10$zq4Q38I3HHSCjqhsPs.S1e2kdQwah2vI4fOf9MZ4Mx/jlzoycElb2	1	2017-03-09 12:37:50.805069	2017-03-09 12:37:50.805234	2017-03-09 12:37:50.805376		\N
7	Bob	Bubbles	Bob	Bob	tobias.krauthoff+dbas.usert31@gmail.com	n	$2a$10$XxTP5nH0O4SCzUNyWeLA0OZR8drUZcJrzWyTmkA9ASNJuRRtIMkby	1	2017-03-09 12:37:50.805069	2017-03-09 12:37:50.805234	2017-03-09 12:37:50.805376		\N
8	Pascal	Lux	Pascal	Pascal	tobias.krauthoff+dbas.usert00@gmail.com	m	$2a$10$XxTP5nH0O4SCzUNyWeLA0OZR8drUZcJrzWyTmkA9ASNJuRRtIMkby	3	2017-03-09 12:37:50.805069	2017-03-09 12:37:50.805234	2017-03-09 12:37:50.805376		\N
9	Kurt	Hecht	Kurt	Kurt	tobias.krauthoff+dbas.usert01@gmail.com	m	$2a$10$XxTP5nH0O4SCzUNyWeLA0OZR8drUZcJrzWyTmkA9ASNJuRRtIMkby	3	2017-03-09 12:37:50.805069	2017-03-09 12:37:50.805234	2017-03-09 12:37:50.805376		\N
10	Torben	Hartl	Torben	Torben	tobias.krauthoff+dbas.usert02@gmail.com	m	$2a$10$XxTP5nH0O4SCzUNyWeLA0OZR8drUZcJrzWyTmkA9ASNJuRRtIMkby	3	2017-03-09 12:37:50.805069	2017-03-09 12:37:50.805234	2017-03-09 12:37:50.805376		\N
11	Thorsten	Scherer	Thorsten	Thorsten	tobias.krauthoff+dbas.usert03@gmail.com	m	$2a$10$XxTP5nH0O4SCzUNyWeLA0OZR8drUZcJrzWyTmkA9ASNJuRRtIMkby	3	2017-03-09 12:37:50.805069	2017-03-09 12:37:50.805234	2017-03-09 12:37:50.805376		\N
12	Friedrich	Schutte	Friedrich	Friedrich	tobias.krauthoff+dbas.usert04@gmail.com	m	$2a$10$XxTP5nH0O4SCzUNyWeLA0OZR8drUZcJrzWyTmkA9ASNJuRRtIMkby	3	2017-03-09 12:37:50.805069	2017-03-09 12:37:50.805234	2017-03-09 12:37:50.805376		\N
13	Aayden	Westermann	Aayden	Aayden	tobias.krauthoff+dbas.usert05@gmail.com	m	$2a$10$XxTP5nH0O4SCzUNyWeLA0OZR8drUZcJrzWyTmkA9ASNJuRRtIMkby	3	2017-03-09 12:37:50.805069	2017-03-09 12:37:50.805234	2017-03-09 12:37:50.805376		\N
14	Hermann	Grasshoff	Hermann	Hermann	tobias.krauthoff+dbas.usert06@gmail.com	m	$2a$10$XxTP5nH0O4SCzUNyWeLA0OZR8drUZcJrzWyTmkA9ASNJuRRtIMkby	3	2017-03-09 12:37:50.805069	2017-03-09 12:37:50.805234	2017-03-09 12:37:50.805376		\N
15	Wolf	Himmler	Wolf	Wolf	tobias.krauthoff+dbas.usert07@gmail.com	m	$2a$10$XxTP5nH0O4SCzUNyWeLA0OZR8drUZcJrzWyTmkA9ASNJuRRtIMkby	3	2017-03-09 12:37:50.805069	2017-03-09 12:37:50.805234	2017-03-09 12:37:50.805376		\N
16	Jakob	Winter	Jakob	Jakob	tobias.krauthoff+dbas.usert08@gmail.com	m	$2a$10$XxTP5nH0O4SCzUNyWeLA0OZR8drUZcJrzWyTmkA9ASNJuRRtIMkby	3	2017-03-09 12:37:50.805069	2017-03-09 12:37:50.805234	2017-03-09 12:37:50.805376		\N
17	Alwin	Wechter	Alwin	Alwin	tobias.krauthoff+dbas.usert09@gmail.com	m	$2a$10$XxTP5nH0O4SCzUNyWeLA0OZR8drUZcJrzWyTmkA9ASNJuRRtIMkby	3	2017-03-09 12:37:50.805069	2017-03-09 12:37:50.805234	2017-03-09 12:37:50.805376		\N
18	Walter	Weisser	Walter	Walter	tobias.krauthoff+dbas.usert10@gmail.com	m	$2a$10$XxTP5nH0O4SCzUNyWeLA0OZR8drUZcJrzWyTmkA9ASNJuRRtIMkby	3	2017-03-09 12:37:50.805069	2017-03-09 12:37:50.805234	2017-03-09 12:37:50.805376		\N
19	Volker	Keitel	Volker	Volker	tobias.krauthoff+dbas.usert11@gmail.com	m	$2a$10$XxTP5nH0O4SCzUNyWeLA0OZR8drUZcJrzWyTmkA9ASNJuRRtIMkby	3	2017-03-09 12:37:50.805069	2017-03-09 12:37:50.805234	2017-03-09 12:37:50.805376		\N
20	Benedikt	Feuerstein	Benedikt	Benedikt	tobias.krauthoff+dbas.usert12@gmail.com	m	$2a$10$XxTP5nH0O4SCzUNyWeLA0OZR8drUZcJrzWyTmkA9ASNJuRRtIMkby	3	2017-03-09 12:37:50.805069	2017-03-09 12:37:50.805234	2017-03-09 12:37:50.805376		\N
21	Engelbert	Gottlieb	Engelbert	Engelbert	tobias.krauthoff+dbas.usert13@gmail.com	m	$2a$10$XxTP5nH0O4SCzUNyWeLA0OZR8drUZcJrzWyTmkA9ASNJuRRtIMkby	3	2017-03-09 12:37:50.805069	2017-03-09 12:37:50.805234	2017-03-09 12:37:50.805376		\N
22	Elias	Auerbach	Elias	Elias	tobias.krauthoff+dbas.usert14@gmail.com	m	$2a$10$XxTP5nH0O4SCzUNyWeLA0OZR8drUZcJrzWyTmkA9ASNJuRRtIMkby	3	2017-03-09 12:37:50.805069	2017-03-09 12:37:50.805234	2017-03-09 12:37:50.805376		\N
23	Rupert	Wenz	Rupert	Rupert	tobias.krauthoff+dbas.usert15@gmail.com	m	$2a$10$XxTP5nH0O4SCzUNyWeLA0OZR8drUZcJrzWyTmkA9ASNJuRRtIMkby	3	2017-03-09 12:37:50.805069	2017-03-09 12:37:50.805234	2017-03-09 12:37:50.805376		\N
24	Marga	Wegscheider	Marga	Marga	tobias.krauthoff+dbas.usert16@gmail.com	f	$2a$10$XxTP5nH0O4SCzUNyWeLA0OZR8drUZcJrzWyTmkA9ASNJuRRtIMkby	3	2017-03-09 12:37:50.805069	2017-03-09 12:37:50.805234	2017-03-09 12:37:50.805376		\N
25	Larissa	Clauberg	Larissa	Larissa	tobias.krauthoff+dbas.usert17@gmail.com	f	$2a$10$XxTP5nH0O4SCzUNyWeLA0OZR8drUZcJrzWyTmkA9ASNJuRRtIMkby	3	2017-03-09 12:37:50.805069	2017-03-09 12:37:50.805234	2017-03-09 12:37:50.805376		\N
26	Emmi	Rosch	Emmi	Emmi	tobias.krauthoff+dbas.usert18@gmail.com	f	$2a$10$XxTP5nH0O4SCzUNyWeLA0OZR8drUZcJrzWyTmkA9ASNJuRRtIMkby	3	2017-03-09 12:37:50.805069	2017-03-09 12:37:50.805234	2017-03-09 12:37:50.805376		\N
27	Konstanze	Krebs	Konstanze	Konstanze	tobias.krauthoff+dbas.usert19@gmail.com	f	$2a$10$XxTP5nH0O4SCzUNyWeLA0OZR8drUZcJrzWyTmkA9ASNJuRRtIMkby	3	2017-03-09 12:37:50.805069	2017-03-09 12:37:50.805234	2017-03-09 12:37:50.805376		\N
28	Catrin	Fahnrich	Catrin	Catrin	tobias.krauthoff+dbas.usert20@gmail.com	f	$2a$10$XxTP5nH0O4SCzUNyWeLA0OZR8drUZcJrzWyTmkA9ASNJuRRtIMkby	3	2017-03-09 12:37:50.805069	2017-03-09 12:37:50.805234	2017-03-09 12:37:50.805376		\N
29	Antonia	Bartram	Antonia	Antonia	tobias.krauthoff+dbas.usert21@gmail.com	f	$2a$10$XxTP5nH0O4SCzUNyWeLA0OZR8drUZcJrzWyTmkA9ASNJuRRtIMkby	3	2017-03-09 12:37:50.805069	2017-03-09 12:37:50.805234	2017-03-09 12:37:50.805376		\N
30	Nora	Kempf	Nora	Nora	tobias.krauthoff+dbas.usert22@gmail.com	f	$2a$10$XxTP5nH0O4SCzUNyWeLA0OZR8drUZcJrzWyTmkA9ASNJuRRtIMkby	3	2017-03-09 12:37:50.805069	2017-03-09 12:37:50.805234	2017-03-09 12:37:50.805376		\N
31	Julia	Wetter	Julia	Julia	tobias.krauthoff+dbas.usert23@gmail.com	f	$2a$10$XxTP5nH0O4SCzUNyWeLA0OZR8drUZcJrzWyTmkA9ASNJuRRtIMkby	3	2017-03-09 12:37:50.805069	2017-03-09 12:37:50.805234	2017-03-09 12:37:50.805376		\N
32	Jutta	Munch	Jutta	Jutta	tobias.krauthoff+dbas.usert24@gmail.com	f	$2a$10$XxTP5nH0O4SCzUNyWeLA0OZR8drUZcJrzWyTmkA9ASNJuRRtIMkby	3	2017-03-09 12:37:50.805069	2017-03-09 12:37:50.805234	2017-03-09 12:37:50.805376		\N
33	Helga	Heilmann	Helga	Helga	tobias.krauthoff+dbas.usert25@gmail.com	f	$2a$10$XxTP5nH0O4SCzUNyWeLA0OZR8drUZcJrzWyTmkA9ASNJuRRtIMkby	3	2017-03-09 12:37:50.805069	2017-03-09 12:37:50.805234	2017-03-09 12:37:50.805376		\N
34	Denise	Tietjen	Denise	Denise	tobias.krauthoff+dbas.usert26@gmail.com	f	$2a$10$XxTP5nH0O4SCzUNyWeLA0OZR8drUZcJrzWyTmkA9ASNJuRRtIMkby	3	2017-03-09 12:37:50.805069	2017-03-09 12:37:50.805234	2017-03-09 12:37:50.805376		\N
35	Hanne	Beckmann	Hanne	Hanne	tobias.krauthoff+dbas.usert27@gmail.com	f	$2a$10$XxTP5nH0O4SCzUNyWeLA0OZR8drUZcJrzWyTmkA9ASNJuRRtIMkby	3	2017-03-09 12:37:50.805069	2017-03-09 12:37:50.805234	2017-03-09 12:37:50.805376		\N
36	Elly	Landauer	Elly	Elly	tobias.krauthoff+dbas.usert28@gmail.com	f	$2a$10$XxTP5nH0O4SCzUNyWeLA0OZR8drUZcJrzWyTmkA9ASNJuRRtIMkby	3	2017-03-09 12:37:50.805069	2017-03-09 12:37:50.805234	2017-03-09 12:37:50.805376		\N
37	Sybille	Redlich	Sybille	Sybille	tobias.krauthoff+dbas.usert29@gmail.com	f	$2a$10$XxTP5nH0O4SCzUNyWeLA0OZR8drUZcJrzWyTmkA9ASNJuRRtIMkby	3	2017-03-09 12:37:50.805069	2017-03-09 12:37:50.805234	2017-03-09 12:37:50.805376		\N
38	Ingeburg	Fischer	Ingeburg	Ingeburg	tobias.krauthoff+dbas.usert30@gmail.com	f	$2a$10$XxTP5nH0O4SCzUNyWeLA0OZR8drUZcJrzWyTmkA9ASNJuRRtIMkby	3	2017-03-09 12:37:50.805069	2017-03-09 12:37:50.805234	2017-03-09 12:37:50.805376		\N
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

