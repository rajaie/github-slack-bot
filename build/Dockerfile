FROM python:3.7-alpine
COPY Pipfile.lock /app/
COPY Pipfile /app/
RUN pip install pipenv
WORKDIR /app
RUN pipenv install --system --ignore-pipfile
# TODO: separate out test and runtime images
COPY tests ./tests
COPY github_slack_bot ./github_slack_bot
ENTRYPOINT ["python3.7"]