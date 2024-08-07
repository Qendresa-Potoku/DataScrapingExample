from playwright.sync_api import sync_playwright
import pandas as pd

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto('https://trajnimet.info/', timeout=60000)

        loaded_courses = set()
        all_courses_loaded = False

        while not all_courses_loaded:
            page.evaluate('window.scrollBy(0, document.body.scrollHeight)')
            page.wait_for_timeout(2000)  # Wait for 2 seconds to load new content

            courses = page.locator('//div[contains(@class, "item")]')
            current_courses = [course.locator('a.training-post').get_attribute('href') for course in courses.all()]
            
            new_courses = set(current_courses) - loaded_courses
            loaded_courses.update(new_courses)
            
            if not new_courses:
                all_courses_loaded = True

            print(f'Current loaded courses count: {len(loaded_courses)}')
            if len(loaded_courses) >= 437:
                all_courses_loaded = True

        print(f'Total courses found: {len(loaded_courses)}')

        courses_list = []
        for course_href in loaded_courses:
            try:
                page.goto(course_href, timeout=60000)
                page.wait_for_load_state('networkidle')  # Ensure the page has fully loaded

                # Extracting data
                title = page.locator('.course-content-box h2').inner_text(timeout=10000) if page.locator('.course-content-box h2').count() > 0 else 'N/A'
                field_of_education = page.locator('p:has-text("Fusha e edukimit:")').inner_text(timeout=10000).replace('Fusha e edukimit:', '').strip() if page.locator('p:has-text("Fusha e edukimit:")').count() > 0 else 'N/A'
                application_deadline = page.locator('p:has-text("Afati i aplikimit:") cite').inner_text(timeout=10000).replace('Afati i aplikimit:', '').strip() if page.locator('p:has-text("Afati i aplikimit:") cite').count() > 0 else 'N/A'
                location = page.locator('p:has-text("Lokacioni:")').inner_text(timeout=10000).replace('Lokacioni:', '').strip() if page.locator('p:has-text("Lokacioni:")').count() > 0 else 'N/A'
                trainer = page.locator('p:has-text("Trajner:")').inner_text(timeout=10000).replace('Trajner:', '').strip() if page.locator('p:has-text("Trajner:")').count() > 0 else 'N/A'
                level = page.locator('p:has-text("Niveli:")').inner_text(timeout=10000).replace('Niveli:', '').strip() if page.locator('p:has-text("Niveli:")').count() > 0 else 'N/A'
                hours = page.locator('p:has-text("Nr.i orëve:")').inner_text(timeout=10000).replace('Nr.i orëve:', '').strip() if page.locator('p:has-text("Nr.i orëve:")').count() > 0 else 'N/A'
                email = page.locator('p:has-text("Email:")').inner_text(timeout=10000).replace('Email:', '').strip() if page.locator('p:has-text("Email:")').count() > 0 else 'N/A'
                phone = page.locator('p:has-text("Telefoni:")').inner_text(timeout=10000).replace('Telefoni:', '').strip() if page.locator('p:has-text("Telefoni:")').count() > 0 else 'N/A'
                website = page.locator('p:has-text("Uebsajti:")').inner_text(timeout=10000).replace('Uebsajti:', '').strip() if page.locator('p:has-text("Uebsajti:")').count() > 0 else 'N/A'
                price = page.locator('p:has-text("Çmimi:")').inner_text(timeout=10000).replace('Çmimi:', '').strip() if page.locator('p:has-text("Çmimi:")').count() > 0 else 'N/A'

                # Append to the list
                courses_list.append({
                    'Title': title,
                    'Field of Education': field_of_education,
                    'Application Deadline': application_deadline,
                    'Location': location,
                    'Trainer': trainer,
                    'Level': level,
                    'Number of Hours': hours,
                    'Email': email,
                    'Phone': phone,
                    'Website': website,
                    'Price': price
                })
            except Exception as e:
                print(f"An error occurred while processing a course: {str(e).encode('utf-8', 'replace').decode('utf-8')}")

        # Convert to DataFrame
        df = pd.DataFrame(courses_list)
        
        # Save to Excel directly
        df.to_excel('courses_data.xlsx', index=False)
        
        print("Data saved to courses_data.xlsx")

        browser.close()

if __name__ == '__main__':
    main()
