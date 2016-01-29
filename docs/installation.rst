.. _installation:

Installation
------------
Requirements (Tested on Debian\Ubuntu,  64-Bit is mandatory):

1. Create virtualenv with python3

   - $ mkvirtualenv --python=$(which python3) dbas

2. Install all requirements

   - $ pip install -r requirements.txt

3. Develop application

   - $ python setup.py develop

4. Create database

   - $ initialize_sql development.ini

5. Start development webserver

   - $ pserve development.ini --reload
