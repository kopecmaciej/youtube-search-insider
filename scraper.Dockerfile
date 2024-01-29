FROM python:3.9-slim

RUN pip install --upgrade pip

WORKDIR /yt

COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt --quiet

COPY shared shared
COPY youtube_scraper youtube_scraper
COPY .env .env

CMD ["python", "youtube_scraper"]
