# Data Scraping Example

## Overview
This project includes scripts to scrape job data from various websites and save the data either to an Excel file or a MySQL database.

## Files

### Excel Data Saving
These files scrape data from websites and save it to Excel files:
- **`betrootacademy_scraper.py`**
- **`probit_scraping.py`**
- **`shpiktrainings_scraping.py`**

### Database Data Saving
This file scrapes data and saves it to a MySQL database:
- **`kosovajob.py`**

## Database Setup
To save data using the `kosovajob.py` script, you need to set up a MySQL database. Follow these steps:

1. **Create the database:**
   ```sql
   CREATE DATABASE IF NOT EXISTS job_data;
2. **Use the database:**
   ```sql
   USE job_data;
3. **Create the table:**
   ```sql
    CREATE TABLE IF NOT EXISTS job_listings (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255),
        city VARCHAR(100),
        expires VARCHAR(50),
        link VARCHAR(255),
        company_logo VARCHAR(255),
        source VARCHAR(50)
        );

Running the Scripts
-------------------

1.  Ensure you have Python installed.
2.  Install the necessary libraries using pip:
    
    ```bash
    pip install requests beautifulsoup4 mysqlclient
    ```
    
3.  Run the desired script:
    *   For Excel:
        
        ```bash
        python betrootacademy_scraper.py
        python probit_scraping.py
        python shpiktrainings_scraping.py
        ```
        
    *   For Database:
        
        ```bash
        python kosovajob.py
        ```
