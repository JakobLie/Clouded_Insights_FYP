FROM python:3.13-slim
WORKDIR /usr/src/app
COPY ./requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./models ./
COPY ./db_classes.py ./
COPY ./fc_app.py ./
CMD [ "python", "./fc_app.py" ]