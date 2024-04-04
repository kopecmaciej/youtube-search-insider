SCRAPER_DOCKERFILE = ./scraper.Dockerfile

.PHONY: clean run-scraper run-procesor build-scraper requirements

clean:
	rm -rf ./data/transcriptions/* ./data/processed/* ./data/tokenized/* ./data/raw/* 

run-scraper:
	python3 youtube_scraper

run-procesor:
	python3 video_processor

build-scraper:
	docker build -t youtube-scraper -f $(SCRAPER_DOCKERFILE) .

requirements:
	pipreqs . --force --ignore .venv

test:
	python3 -m unittest discover ./youtube_scraper -v
	python3 -m unittest discover ./video_processor -v
