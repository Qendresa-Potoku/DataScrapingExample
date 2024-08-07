from playwright.sync_api import sync_playwright
import pandas as pd

def main():
    with sync_playwright() as p:
        page_url = 'https://probitacademy.com/courses/'

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(page_url, timeout=60000)
        
        # Locate the course cards on the page
        courses = page.locator('//div[contains(@class, "course-grid-4")]').all()
        print(f'There are {len(courses)} courses.')

        courses_list = []
        for course in courses:
            try:
                title = course.locator('.course-title a').inner_text(timeout=5000)
                author = course.locator('.course-author .value a').first.inner_text(timeout=5000)  # Use .first to select the first matching element
                description = course.locator('.course-description p').inner_text(timeout=5000)
                price = course.locator('.course-price .value').first.inner_text(timeout=5000).replace('€', '').strip()
                students = course.locator('.course-students .value').first.inner_text(timeout=5000).strip()
                rating = course.locator('.course-review .value').first.inner_text(timeout=5000).strip()
                image_url = course.locator('.course-thumbnail img').get_attribute('src', timeout=5000)

                courses_list.append({
                    'Title': title,
                    'Author': author,
                    'Description': description,
                    'Price (EUR)': price,
                    'Students': students,
                    'Rating': rating,
                    'Image URL': image_url
                })
            except Exception as e:
                print(f"An error occurred while processing a course: {e}")

        browser.close()

        # Convert the list to a DataFrame
        df = pd.DataFrame(courses_list)

        # Write the DataFrame to an Excel file
        df.to_excel('probit_data.xlsx', index=False)
        print("Data has been written to probit_data.xlsx")

if __name__ == '__main__':
    main()
