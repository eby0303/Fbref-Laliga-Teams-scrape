# from apscheduler.schedulers.blocking import BlockingScheduler
# import scraper

# def job():
#     print("Running scheduled scraping job...")
#     scraped_data = scraper.run_all_scrapers()
#     scraper.update_data(scraped_data)

# scheduler = BlockingScheduler()
# scheduler.add_job(job, 'interval', hours=1)  # Run every hour

# if __name__ == "__main__":
#     print("Starting scheduler...")
#     scheduler.start()
