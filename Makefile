clean:
	rm -rf ./data/transcriptions/* ./data/processed/* ./data/tokenized/* ./data/raw/* 

run-scraper:
	python3 youtube_scraper

run-procesor:
	python3 video_procesor


