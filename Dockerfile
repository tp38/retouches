FROM python:3.11-bookworm as compiler
ENV PYTHONUNBUFFERED=1
RUN mkdir /code
WORKDIR /code

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY ./admin_tools/requirements.txt /code/requirements.txt
RUN pip install --upgrade pip
RUN pip install -Ur requirements.txt

FROM python:3.11-bookworm as runner
WORKDIR /code/
COPY --from=compiler /opt/venv /opt/venv

# Enable venv
ENV PATH="/opt/venv/bin:$PATH"
COPY . /code/
