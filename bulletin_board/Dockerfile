FROM python:3.9.2-slim

WORKDIR /code

COPY Pipfile Pipfile.lock /code/

RUN pip install pipenv && pipenv install --system

# copy entrypoint.sh
COPY ./entrypoint.sh /code/
RUN sed -i 's/\r$//g' /code/entrypoint.sh
RUN chmod +x /code/entrypoint.sh

# copy project
COPY . /code/

# run entrypoint.sh
ENTRYPOINT ["sh", "/code/entrypoint.sh"]