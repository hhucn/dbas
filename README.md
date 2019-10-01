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

## Environment variables
D-BAS need some environment variables to be set for running properly.
By default those variables which are required by D-BAS are stored in `.env`.
To get further details on which variables are set or how they can be added/changed take a look at the documentation [here](https://dbas.cs.uni-duesseldorf.de/docs/installation.html).

## Run D-BAS

Then follow these steps:

    docker-compose up

If you want to include the notification service as well as elastic search:

    docker-compose -f docker-compose.yml -f docker-compose.notifications.yml -f docker-compose.search.yml up

Production mode:

    docker-compose -f docker-compose.production.yml up --build

After this you can hit [http://localhost:4284](http://localhost:4284) for D-BAS.

If your container stucks during the first start up, please install D-BAS manually (while the container is running) via:

    docker-compose exec web make

Afterwards everything should be fine.


## Maintainers

* [Christian Meter](mailto:meter@hhu.de)
* [Björn Ebbinghaus](mailto:bjoern.ebbinghaus@uni-duesseldorf.de)
* [Tobias Schröder (neé Krauthoff)](mailto:tobias.krauthoff@uni-duesseldorf.de) (Alumnus)


### Contributors

We thank all contributors to this project! In order of appearance:

* Alexander Schneider
* Marc Feger
* Markus Brenneis

### Former Contributors

Thanks to all former contributors! In order of appearance:

* Teresa Uebber (JS Graphs and Visualizations)


## License

Copyright (c) 2016 - 2018 Tobias Schröder (neé Krauthoff), Christian Meter  
Copyright (c) 2018 - today hhucn

Distributed under the [MIT License](LICENSE).
