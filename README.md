# D-BAS

D-BAS is based on [Pyramid](http://www.pylonsproject.org/), [Bootstrap](http://getbootstrap.com/),
[jQuery](https://jquery.com/) and shipped via [Docker Containers](https://www.docker.com/). It is a novel approach to online
argumentation. It avoids the pitfalls of  unstructured systems such as asynchronous threaded discussions and it is
usable by any participant without training while still supporting the full complexity  of real-world argumentation.
The key idea is to let users exchange arguments  with each other in the form of a time-shifted dialog where arguments
are presented and acted upon one-at-a-time.

Currently, the main development-process happens in our GitLab instance, but you
can open issues here, submit pull requests etc. and we will coordinate your
contributions.

Of course, you can try out D-BAS on [https://dbas.cs.uni-duesseldorf.de/](https://dbas.cs.uni-duesseldorf.de/).

## Setup for Linux

Ensure that the following tools are installed:

* Python >= 3.6
* [Docker](https://docs.docker.com/engine/installation/)
* [Docker Compose](https://docs.docker.com/compose/install/)

Then copy the `skeleton.env` to `development.env` and fill out the fields you need.
At least the following field should be set:
 - `DB_*` ; Please fill out every value of your used database.
 - `MAIL_*`; Please fill out every value of your mail server.
 - `WEBSOCKET_PORT` with the port of the small node.js server. Default is 5222. On modification, please set the new port on `websocket/static/js/websocket.js` too. 
 - `MIN_LENGTH_OF_STATEMENT` is the minimal length of any statement in D-BAS. We think, that `10` is a good default value.

Then follow these steps:

    docker-compose up

If you want to include the notification service as well as elastic search:

    docker-compose -f docker-compose.yml -f docker-compose.notifications.yml -f docker-compose.search.yml up

Production mode:

    docker-compose -f docker-compose.production.yml up --build

After this you can hit [http://localhost:4284](http://localhost:4284) for D-BAS.

If your container stucks during the first start up, please install D-BAS manually via:

    docker-compose exec web ./build_assets.sh

Afterwards everything should be fine.


## Maintainers

* [Christian Meter](mailto:meter@cs.uni-duesseldorf.de)
* [Tobias Krauthoff](mailto:krauthoff@cs.uni-duesseldorf.de) (Alumnus)


### Contributors

We thank all contributors to this project! In order of appearance:

* Björn Ebbinghaus
* Alexander Schneider
* Marc Feger


### Former Contributors

Thanks to all former contributors! In order of appearance:

* Teresa Uebber (JS Graphs and Visualizations)


## License

Copyright (c) 2016 - 2018 Tobias Krauthoff, Christian Meter
Copyright (c) 2018 hhucn

Distributed under the [MIT License](LICENSE).
