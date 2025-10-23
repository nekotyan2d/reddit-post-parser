from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

import time
from datetime import datetime, timezone, timedelta
from dateutil import parser as date_parser

import psycopg2

from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, USER_AGENT, SCROLLS, MIN_AGE_HOURS, MIN_SCORE, WAIT_TIME_SECONDS, SUBREDDIT, HEADLESS

def parse():
    options = webdriver.FirefoxOptions()
    options.set_preference("dom.webdriver.enabled", False)
    options.set_preference("general.useragent.override", USER_AGENT)

    if HEADLESS:
        options.add_argument('--headless')

    driver = webdriver.Firefox(options=options)

    try:
        url = f'https://www.reddit.com/r/{SUBREDDIT}/'
        driver.get(url)
        time.sleep(WAIT_TIME_SECONDS)  # ждем пока страница загрузится

        for _ in range(SCROLLS):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(WAIT_TIME_SECONDS)  # ждем подгрузки новых постов

            post_elements = driver.find_elements(By.CSS_SELECTOR, "shreddit-post[post-type='image'], shreddit-post[post-type='gallery']")
            for post in post_elements:
                if(post.get_attribute("post-type") == "gallery"):
                    img = post.find_element(By.CSS_SELECTOR, ".post-background-image-filter").get_attribute("src")
                else:
                    img = post.get_attribute("content-href")

                score_num = int(post.get_attribute("score"))

                post_id = post.get_attribute("permalink").replace(f"/r/{SUBREDDIT}/comments/", "")
                created_at = post.get_attribute("created-timestamp")

                try:
                    post_time = date_parser.parse(created_at)
                    now = datetime.now(timezone.utc)
                    age = now - post_time
                    if age < timedelta(hours=MIN_AGE_HOURS):
                        continue
                except Exception:
                    continue

                if score_num < MIN_SCORE:
                    continue

                insert_post(post_id, score_num, img, created_at)
    finally:
        driver.quit()

def insert_post(post_id, score, img_url, created_at):
    try:
        conn = psycopg2.connect(
            dbname = DB_NAME,
            user = DB_USER,
            password = DB_PASSWORD,
            host = DB_HOST,
            port = DB_PORT
        )
        cursor = conn.cursor()
        insert_query = """
        INSERT INTO post (post_id, score, img_url, created_at)
        VALUES (%s, %s, %s, %s::timestamptz)
        ON CONFLICT (post_id) DO NOTHING;
        """
        cursor.execute(insert_query, (post_id, score, img_url, created_at))
        conn.commit()
    except Exception as e:
        print(f"Ошибка при вставке {post_id}: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    parse()