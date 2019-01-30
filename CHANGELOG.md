### 1.13.2 (2019-01-30)
- Fix Statement validation for cases where a Statement is in multiple Issues !652

### 1.13.1 (2019-01-12)
- Add key-paths for production build to compose file

### 1.13.0 (2019-01-12)

#### Common
- Remove bootstrap-toggle !641
- Optimize building process and don't minify minified files twice !642
- Increase performance of search-engine !646
- Restrict review-queue access to users who participated in the discussion !637
- Let the API handle authors as objects when communicating with EDEN !645

#### API
- Add JWT support !644
- Add PATCH route for issues !640
- Add status-flag of issue !643
- Add Cypher Output to retrieve neo4j-compatible discussions !649
- Add route to bind a reference to a newly created position !648
- Add uid to login-response !638
- Extend API to return single Users !635
- Change HTTP Method to POST to send token to API and revoke it !636
- Remove /discuss prefix in jump-interface !647
- Refactor fields of StatementReferences !639

### 1.12.1 (2018-11-22)
- Fix API routes, add second positional argument to JSONBase !633

### 1.12.0 (2018-11-21)
- Add GraphQL Route to return all statements below a specific position !627
- Add GraphQL Route to export complete graph as JSON data !623
- Add origin to statements !620
- Extend API to support jumps, adding references and retrieving reference usages !618
- Improve search results to only present statements, which have not already been seen !629
- Improve search results when no ElasticSearch is enabled !621
- Remove unused code !626
- Replace deprecated google-closure library !624
- Refactor api.models !632
- Fix timezone !628
- Fix infinite loop in review queue !622
- Fix flake8 issues !625
- Fix wrong transaction commits !631

When updating from 1.11.0: The GraphQL Route "premise.users" has been renamed to "premise.author"

### 1.11.0 (2018-10-26)
- Add overview to see link-only discussions in "My Discussions" !610
- Add new spinner icon, which does not block the website !614
- Fix build process so that build script really fails if there is an error !612
- Fix mutable return values in validators !617
- Fix Model resolving with GraphQL !616
- Fix URL in sent mails !611

### 1.10.6 (2018-10-15)
- Add CLI function to promote / demote a user to an admin !595
- Add more detailed error-msgs in issues !604
- Add route to add new position !605
- Add validators for form-inputs in the discussion !605
- Add public API route `/api/search?q=foo` to search for statements (support for 3rd party applications) !607
- Fix resolve of statements in GraphiQL !600
- Fix Login-problem for API users, which could no longer change their passwords !598
- Refactor magic numbers in Fuzzy Mode !601 !602
- Refactor environment variables !597 !607
- Language fixes !603
- Use Abstract Base Class and generalize Queues !596 !597
- Remove deprecated cryptacular with bcrypt !594

### 1.10.5 (2018-09-21)
- Fix login flow for LDAP users !591
- Kick hardcoded admin from notifications !590
- Add abstract base class for review queues !589

### 1.10.4 (2018-09-19)
- Precompile chameleon templates for production !587
- Remove own logger and use built-in python logger !586 !578
- Re-add "change password" for dbas-users !585
- Simplify reference retrieval via API !584
- Fix loop in review queue after user participated !583
- Remove RSS feed !582

### 1.10.3 (2018-09-14)
- Fix parse error of history in URL
- Make discussion-sidebar more mobile friendly
- Move "Restart discussion" into the discussion

### 1.10.2 (2018-09-13)
- Fix selection of conclusion

### 1.10.1 (2018-09-12)
- Fix graphiql error
- Add more triggers to database

### 1.10.0 (2018-09-05)
- Add route to API to support references again
  - support model abstractions for API entities
- Include all tests for API v1 and v2
- Simplify tests
- Update OAuth modules
- Uniform env-files
- Enable Continuous Delivery through GitLab
- Add security analysis in GitLab CI
- Fix many dead tests
- Fix discussion flow
- Fix CORS headers for HTTP 303 redirects

### 1.9.1 (2018-06-26)
- Many bugfixes for the frontend
- Special thanks to the COMMA18 Reviewer

### 1.9.0 (2018-06-13)
- Introduced Cypress for frontend tests

### 1.8.2 (2018-06-07)
- Fix language set which is derived from the requests header

### 1.8.1 (2018-06-06)
- Update yarn packages

### 1.8.0 (2018-05-30)
- Refactored the review queues. IMPORTANT: Now some logic is switched, so that old discussions are not

### 1.7.0 (2018-05-24)
- Statements are no longer bounded to one issue. Noe we have a many-to-many relationship between statements and issues.

### 1.6.4 (2018-05-10)
- Function to delete an account

### 1.6.3 (2018-05-02)
- Revival of our API

### 1.6.2 (2018-04-10)
- Upgrading JS libs
- Including bumpversion

### 1.6.1 (2018-03-30)
- Splitting compose files

### 1.6.0 (2018-03-02)
- Cleaner code everywhere
- Refactor complete software
- Usage of validators

### 1.5.5 (2018-01-26)
- Add GraphiQL

### 1.5.4 (2018-01-23)
- Jump-step offers the flagging-option
 
### 1.5.3 (2017-12-22)
- Refactoring of the text generators

### 1.5.2 (2017-12-01)
- Discussion can now be set as private or read only
- Remove the webservers request from argumentation logic

### 1.5.1 (2017-11-10)
- Add OAuth registrations for Google, Facebook, Github

### 1.5.0 (2017-10-23)
- New landing page
- Modified header bar
- Redesign of the layout
- Improvements for the inbox and outbox

### 1.4.4 (2017-10-05)
- Manipulated the database to achieve circle-freeness
- Add `alembic` as migration-engine
- Open-Source the database
- Refactor requirements.txt
- Rewrite Authentication via APIv1
- Extend documentation

### 1.4.3 (2017-08-24)
- Entering position and premise at once
- QueueAdapter for split and merge statements
- Discussion for Meta-D-BAS

### 1.4.2 (2017-06-07)
- Splitting the monolith

### 1.4.1 (2017-05-15)
- Fixes while sending system mails
- Fix routing of the contact view
- Fix escaping of passwords
- Improvement for the barometer
- Timeline for the graph

### 1.4.0 (2017-05-08)
- Corrections for the user interface
- Language fixes
- Improvements on many smaller details
- QueueABC version for our fieldtest

### 1.3.4 (2017-05-01)
- Corrections for the user interface
- Language fixes

### 1.3.3 (2017-04-25)
- Fixed graph view during the attitude-step
- Improved buttons in the graph view
- Performance improvements
- Language fixes

### 1.3.2 (2017-04-12)
- Minor bug fixes
- Language fixes for the feedback options
- Improved the popup for the use of the "and"-keyword

### 1.3.1 (2017-04-07)
- Minor bug fixes
- More planar graph

### 1.3.0 (2017-03-10)
- Performance tweaks
- Partial graph instead of complete one
- FAQs, Docs and Help-Page are online
- Search function over all statements
- Many sneaky ui improvements
- Dockerization

### 1.2.3 (2017-02-08)
- QueueAdapter for duplicates
- New step, where the user gets another support/attack for the same conclusion
- Mark statements/arguments as your opinion

### 1.2.2 (2017-02-06)
- Reworked feedback options
- Improved coloring of arguments
- Spelling corrections

### 1.2.1 (2017-02-03)
- Reworked lateral entry
- Minor language fixes

### 1.2.0 (2017-01-30)
- Improvements and bugfix during a second experiment
- Security fixes for better password handling
- Improved 404 pages
- Use of firstname instead of LDAP-name
- Minors, majors and many more

### 1.1.3 (2017-01-29)
Improvements and bugfix during a second experiment

### 1.1.2 (2017-01-24)
- Update for the german language
- Minor improvements and bugfix

### 1.1.1 (2017-01-16)
- Update for the german language
- Minor improvements and bugfix
- Corrections for color coding mechanisms
- Improvements for our RSS feeds

### 1.1.0 (2017-01-05)
- Huge update for the german language
- Minor improvements and bugfix

### 1.0.0 (2017-01-02)
- Captchas
- Minor improvements and language bugfix
- Guided tour at the beginning

### 0.9.1 (2016-12-18)
- Notification if a user is able to review
- RSS-Feed

### 0.9.0 (2016-12-05)
- Rework of the discussions sidebar
- Improved the page at the end of a discussion
- Made the discussion more personal with new sentence openers
- Minor improvements and bugfix
- Added webtests

### 0.8.0 (2016-11-17)
- Minor improvements and bugfix
- Reworked the opinion barometer and argument graph

### 0.7.3 (2016-11-01)
- Add references for statements from the 'outside world'
- Barometer for the behaviour of all users
- Improvements of the graph view

### 0.7.2 (2016-09-28)
- Additional functions for the review mechanisms
- Deleting own statements/arguments
- Report arguments

### 0.7.1 (2016-09-22)
- Fixes for the review mechanisms

### 0.7.0 (2016-09-06)
- Review-Mechanisms

### 0.6.1 (2016-08-24)
- New bootstraping (jump-mechanism)

### 0.6.0 (2016-07-02)
- Publish / Subscribe

### 0.5.17 (2016-06-12)
- Color coding for feedback mechanisms

### 0.5.16 (2016-07-05)
- Improved sidebar

### 0.5.15 (2016-06-28)
- Island view

### 0.5.14 (2016-06-07)
- Many fixes
- Security fixes
- Docker integration

### 0.5.13 (2016-05-09)
- Many fixes for the german language

### 0.5.12 (2016-05-04)
- Separated site and discussion language
- Checking CSRF tokens automatically
- Updated island view and the opinion barometer

### 0.5.11 (2016-04-27)
- Public user page
- Settings for hiding your real nickname behind a fake one
- Participants are able to send notifications to each other
- Revised timestamps with humanized texts
- Revised discussion finished page

### 0.5.10 (2016-04-26)
- Bug fixes
- History management via url parameter

### 0.5.9 (2016-04-05)
- Lot of fixes for COMMA16

### 0.5.8 (2016-03-22)
- Switched to PostgreSQL

### 0.5.7 (2016-03-16)
- Bunch of fixes
- Improved log in and log out

### 0.5.6 (2016-03-11)
- Bunch of fixes

### 0.5.5 (2016-03-02)
- SpeechBubbles instead of text
- History for anonymous users

### 0.5.4 (2016-02-24)
- Improvements for the settings page
- Bug fixes

### 0.5.3 (2016-02-15)
- Simple notification system

### 0.5.2 (2016-02-09)
- Popup for inserting unclear statements

### 0.5.1 (2016-02-05)
- Improving voting helper

### 0.5.0 (2016-01-28)
- Refactoring:
  - Less Ajax, more HTML
  - Using Chameleon and TAL
  - Reduced loading time

### 0.4.8 (2016-01-12)
- Improved weighting helper, also called voting helper
- Moved many string building functions to the server side

### 0.4.7 (2016-01-06)
- Island View
- Profile Picture based on the MD5-value of the user's mail
- Improved weighting helper

### 0.4.6 (2015-12-16)
- Collecting weights for arguments and statements
- Smaller design improvements like badges for the issues

### 0.4.5 (2015-12-01)
- Improved session management
- Improved anti-spam-questions
- Fixes in the GUI for registration

### 0.4.4 (2015-11-30)
- Breadcrumbs hover vs. title
- Supports will redirect to arguments without any justification

### 0.4.3 (2015-11-30)
- Breadcrumbs

### 0.4.2 (2015-11-23)
- Bug

### 0.4.1 (2015-11-16)
- Improving bootstrapping: It is now a two-step process!fixes

### 0.3.15 (2015-11-13)
- Report Button
- Toggle start button
- Second way of bootstrapping: argumentation against initial given position

### 0.3.14 (2015-11-11)
- Material Design

### 0.3.13 (2015-11-10)
- CSRF frontend
- CSRF backend

### 0.3.12 (2015-11-09)
- Bug fixes
- Fixed sharing option

### 0.3.11 (2015-11-05)
- Bug fixes
- Duplicates

### 0.3.10 (2015-11-04)
- Bug fixes
- Bootstrap for the news

### 0.3.9 (2015-10-27)
- Bug fixes
- Back-button issue for browsers fixed

### 0.3.8 (2015-10-20)
- Bug fixes

### 0.3.7 (2015-10-19)
- i18n / l10n for Ajax

### 0.3.6 (2015-10-15)
- Switching topic

### 0.3.5 (2015-10-14)
- Logic for inserting statements

### 0.3.4 (2015-10-06)
- Fuzzy string search for input fields

### 0.3.3 (2015-10-01)
- News interface for authors

### 0.3.2 (2015-09-25)
- Anonymous users

### 0.3.1 (2015-09-01)
- Unique url's

### 0.3.0 (2015-07-23)
- New data structure

### 0.2.3 (2015-07-23)
- i18n / l10n for Chameleon

### 0.2.2 (2015-07-07)
- Smaller changes of design aspects

### 0.2.1 (2015-07-07)
- Ready for production

### 0.2 (2015-06-25)
- Options for adding statements
- Options for editing statement
- Added an email address
- Sessions management and cache region support with beaker
- CSRF prevention

### 0.1 (2015-06-09)
- First milestone
- Suitable discussion is missing

### 0.0 (2015-04-14)
- Initial version
- Starting the project
