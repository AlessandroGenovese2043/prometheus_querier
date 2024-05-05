FROM python:3

WORKDIR /app
ENV PYTHONPATH "/app"
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY .. ./lib

CMD [ "python", "lib/querier/main.py" ]