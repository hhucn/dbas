# D-BAS

[![build status](https://gitlab.cs.uni-duesseldorf.de/cn-tsn/project/dbas/dbas/badges/master/build.svg)](https://gitlab.cs.uni-duesseldorf.de/cn-tsn/project/dbas/dbas/commits/master)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![coverage report](https://gitlab.cs.uni-duesseldorf.de/cn-tsn/project/dbas/dbas/badges/master/coverage.svg)](https://gitlab.cs.uni-duesseldorf.de/cn-tsn/project/dbas/dbas/commits/master)

D-BAS is based on [Pyramid](http://www.pylonsproject.org/), [Bootstrap](http://getbootstrap.com/),
[jQuery](https://jquery.com/) and shipped via [Docker Containers](https://www.docker.com/). It is a novel approach to online
argumentation. It avoids the pitfalls of  unstructured systems such as asynchronous threaded discussions and it is
usable by any participant without training while still supporting the full complexity  of real-world argumentation.
The key idea is to let users exchange arguments  with each other in the form of a time-shifted dialog where arguments
are presented and acted upon one-at-a-time.

Currently, the main development-process happens in our GitLab instance, but you
can open issues here, submit pull requests etc. and we will coordinate your
contributions.

## Setup for Linux

Ensure that the following tools are installed:

* Python >= 3.5
* [Docker](https://docs.docker.com/engine/installation/)
* [Docker Compose](https://docs.docker.com/compose/install/)

Then follow these steps:

    docker-compose build
    docker-compose up

Example for a fresh build

    docker-compose up --build

Production mode:

    docker-compose -f docker-compose.production.yml up --build

After this you can hit [http://localhost:4284](http://localhost:4284) for D-BAS.

If your container stucks during the first start up, please install D-BAS manually via:

    docker exec -i -t dbas_web_1 /bin/bash
    python setup.py --quiet develop
    google-closure-compiler-js --createSourceMap --compilationLevel SIMPLE ./dbas/static/js/{main,ajax,d3,discussion,review}/*.js > dbas/static/js/dbas.min.js
    sass dbas/static/css/main.sass dbas/static/css/main.css --style compressed
    cd dbas && ./i18n.sh
    cd ../admin && ./i18n.sh

Afterwards everything should be fine.


## Maintainers and Main Contributors

* Tobias Krauthoff
* Christian Meter


## Contributors

We thank all contributors to this project! In order of appearance:

* Teresa Uebber
* Björn Ebbinghaus
* Alexander Schneider
* Marc Feger


## License

Copyright © 2016 - 2017 Tobias Krauthoff, Christian Meter

Distributed under the [MIT License](https://gitlab.cs.uni-duesseldorf.de/project/dbas/raw/master/LICENSE).
