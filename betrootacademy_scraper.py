from playwright.sync_api import sync_playwright
import pandas as pd

def main():
    with sync_playwright() as p:
        page_url = 'https://xk.beetroot.academy/courses/online'

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(page_url, timeout=60000)
        
        trainings = page.locator('//div[@class="col-lg-4 col-md-6 col-sm-6 intro_boxWrap"]').all()
        print(f'There are {len(trainings)} trainings.')

        trainings_list = []
        for training in trainings:
            try:
                training_name = training.locator('.blueTextWeight').inner_text(timeout=5000)
                training_level = training.locator('.design_skill').inner_text(timeout=5000)
                training_description = training.locator('.blackTextSmall').inner_text(timeout=5000)
                training_duration = training.locator('.intro_monthIcon').inner_text(timeout=5000)
                
                trainings_list.append({
                    'Title': training_name,
                    'Level': training_level,
                    'Description': training_description,
                    'Duration': training_duration
                })
            except Exception as e:
                print(f"An error occurred while processing a training: {e}")

        browser.close()

        # Convert the list to a DataFrame
        df = pd.DataFrame(trainings_list)

        # Write the DataFrame to an Excel file
        df.to_excel('betrootacademy_data.xlsx', index=False)
        print("Data has been written to betrootacademy_data.xlsx")

if __name__=='__main__':
    main()
