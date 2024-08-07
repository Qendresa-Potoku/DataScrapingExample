import requests
from bs4 import BeautifulSoup
import MySQLdb
import time

# Database connection parameters
db_params = {
    'user': 'root',
    'passwd': '1234',
    'host': 'localhost',
    'port': 3306,
    'db': 'job_data'
}

def fetch_and_update_job_listings():
    try:
        # Connect to the database
        db = MySQLdb.connect(**db_params)
        cursor = db.cursor()

        # Fetch the job listings page
        url = 'https://kosovajob.com/rfq'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code == 403:
            print("Access forbidden. Check the website or your access.")
            return
        
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all job cards
        job_cards = soup.find_all('div', class_='jobListCnts')

        if not job_cards:
            print("No job cards found.")
            return
        
        for job_card in job_cards:
            try:
                # Extract job details
                title = job_card.find('div', class_='jobListTitle').text.strip()
                city = job_card.find('div', class_='jobListCity').text.strip()
                expires = job_card.find('div', class_='jobListExpires').text.strip()
                link = job_card.find('a')['href']
                company_logo = job_card.find('div', class_='jobListImage')['data-background-image']

                # Check if the job already exists in the database
                check_query = "SELECT COUNT(*) FROM job_listings WHERE link = %s"
                cursor.execute(check_query, (link,))
                exists = cursor.fetchone()[0] > 0

                if not exists:
                    # Insert new job card into the database
                    insert_query = """
                    INSERT INTO job_listings (title, city, expires, link, company_logo, source)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    data = (title, city, expires, link, company_logo, 'KosovaJob')

                    try:
                        cursor.execute(insert_query, data)
                        db.commit()
                        print(f"Inserted new job: {title}")
                    except MySQLdb.Error as e:
                        db.rollback()
                        print(f"Error inserting data: {e}")
                else:
                    print(f"Job already exists: {title}")

                # Delay between requests
                time.sleep(1)

            except AttributeError as e:
                print(f"Attribute error: {e}")  # Log any errors in parsing job cards

    except requests.RequestException as e:
        print(f"Request error: {e}")
    except MySQLdb.Error as e:
        print(f"MySQL error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        try:
            cursor.close()
            db.close()
        except MySQLdb.Error as e:
            print(f"Error closing connection: {e}")

# Main loop to refresh database every 30 minutes
while True:
    fetch_and_update_job_listings()
    print("Sleeping for 30 minutes...")
    time.sleep(30 * 60)  # Sleep for 30 minutes (30 * 60 seconds)
