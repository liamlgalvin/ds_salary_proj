import glassdoor_scraper as gs
import pandas as pd

path = "C:/Users/Liam Galvin/Documents/University/Coding/ds_salary_proj/chromedrive"

df = gs.get_jobs("data scientist", 10, False, path, 15)
df