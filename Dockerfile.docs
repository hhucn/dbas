FROM gitlab.cs.uni-duesseldorf.de:5001/cn-tsn/project/dbas/dbas

WORKDIR /dbas/docs

RUN apt-get install make
RUN make html

WORKDIR /dbas/docs/_build/html/

RUN mkdir -p docs && \
    mv * docs || true

EXPOSE 8000
CMD ["python", "-m", "http.server", "8000"]
