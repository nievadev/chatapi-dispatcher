FROM python:3.8

EXPOSE 8001

RUN pip install pipenv

ENV PROJECT_DIR /usr/local/app/

WORKDIR ${PROJECT_DIR}

COPY Pipfile Pipfile.lock ${PROJECT_DIR}

RUN pipenv install --system --deploy

COPY . .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8001"]
