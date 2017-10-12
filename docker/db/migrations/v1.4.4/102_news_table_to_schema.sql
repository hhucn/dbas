\connect discussion

CREATE SCHEMA news;
GRANT ALL ON SCHEMA news TO writer;
ALTER TABLE news SET SCHEMA news;
ALTER TABLE news.news OWNER TO writer;