from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import win32com.client
import pythoncom

def scrape_and_download(max_pages):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument("disable-blink-features=AutomationControlled")
    options.add_experimental_option("detach", True)

    # Set up download preferences
    download_dir = os.path.join(os.getcwd(), "downloads")
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    
    options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    driver = webdriver.Chrome(options=options)
    
    # Open the initial page
    driver.get("https://main.knesset.gov.il/Activity/Committees/Finance/Pages/CommitteeProtocols.aspx")  

    page_count = 0

    try:
        while page_count < max_pages:
            # Wait for links to be present
            links = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//a[starts-with(@href, 'https://fs.knesset.gov.il')]"))
            )
            
            for link in links:
                href = link.get_attribute('href')
                file_name = href.split('/')[-1]
                
                # Use JavaScript to click the link
                driver.execute_script("arguments[0].click();", link)
                
                # Wait for download to complete

            page_count += 1
            
            if page_count < max_pages:
                # Find and click the "Next" button
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "ctl00_ctl62_g_1ca37dc9_1e14_4b89_aaae_903a30d4c039_ctl00_lnkbtnNext1"))
                )
                next_button.click()
                
                # Wait for the page to load
                time.sleep(10)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Keep the browser open
        input("Press Enter to close the browser...")
        driver.quit()

def convert_docs_to_pdf(download_dir):
    pythoncom.CoInitialize()
    word = win32com.client.Dispatch("Word.Application")
    word.visible = False
    try:
        for filename in os.listdir(download_dir):
            if filename.endswith((".doc", ".docx")):
                in_file = os.path.join(download_dir, filename)
                pdf_file = os.path.join(download_dir, os.path.splitext(filename)[0] + ".pdf")
                
                try:
                    doc = word.Documents.Open(in_file)
                    doc.SaveAs(pdf_file, FileFormat=17)  # FileFormat=17 is for PDF
                    doc.Close()
                    print(f"Converted {filename} to PDF")
                except Exception as e:
                    print(f"Error converting {filename}: {str(e)}")
                
    except Exception as e:
        print(e)
        
    finally:
                    for filename in os.listdir(download_dir):
                        if filename.endswith((".doc", ".docx")):
                            file_path = os.path.join(download_dir, filename)
                            try:
                                os.remove(file_path)
                                print(f"Deleted {filename}")
                            except Exception as e:
                                print(f"Error deleting {filename}: {str(e)}")
    word.Quit()
    pythoncom.CoUninitialize()


if __name__ == '__main__':
    scrape_and_download(max_pages=5)
    download_dir = os.path.join(os.getcwd(), "downloads")
    convert_docs_to_pdf(download_dir)