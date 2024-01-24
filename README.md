# HikePlanner

inspired by https://blog.mimacom.com/data-collection-scrapy-hiketime-prediction/
similar dataset https://www.kaggle.com/datasets/roccoli/gpx-hike-tracks

## Ideas

* Scrape regularly for new / additional data
* Load data into MongoDB
* Regularly update model
    * Produce correlation heatmap
    * Check R2 (bigger and close to 1 is better)
    * Check MSE (lower better, square seconds)
* Use updated model in app

* Personalized Model
    * For a specific Hikr user

## Deployment

* MongoDB on Docker or Online?
* GitHub Action welche Scrapy ausführt und Daten in MongoDB lädt
    * z.B. 100 weitere "neue" Daten eines bestimmten Benutzers 