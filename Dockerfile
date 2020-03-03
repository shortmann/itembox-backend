FROM python:3.7-alpine as build

RUN apk add --no-cache gcc make musl-dev

WORKDIR /src

RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

RUN pip install wheel

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY setup.cfg .
COPY setup.py .
COPY MANIFEST.in .
COPY itembox itembox
RUN pip install .

FROM python:3.7-alpine

COPY --from=build /venv /venv
ENV PATH="/venv/bin:$PATH"

ENTRYPOINT [ "itembox" ]
CMD [ "run" ]