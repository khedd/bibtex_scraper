#!/usr/bin/env python
"""
Retrieve bibtex entries from other (other than Google Scholar) academic platforms such as
- Microsoft Academic
- Core TODO
- Base TODO

Uses Selenium to open the webpage (due to javascript requirements of these services)
Currently uses Firefox Gecko to handle these requests.
- Chrome TODO

Currently retrieves the first entry, TODO bulk return

Usage:
    from bibtex_scraper import query
    bibtex_entry = query('deep learning')
"""


from urllib.request import Request, urlopen, quote
import time

CORE_SCHOLAR_URL='https://core.ac.uk/'
MICROSOFT_ACADEMIC_URL='https://academic.microsoft.com/'


def _format_search_str(search_str):
    split_search_str = search_str.split(' ')
    return '%20'.join(split_search_str)


def _create_firefox_browser(download_path):
    from selenium import webdriver 
    from selenium.webdriver.firefox.options import Options

    options = Options()
    options.headless = True 

    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.panel.shown", False)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", 
    "text/plain,text/x-csv,text/csv,application/vnd.ms-excel,application/csv,application/x-csv,text/csv,text/comma-separated-values,text/x-comma-separated-values,text/tab-separated-values,application/pdf")
    # profile.set_preference("browser.helperApps.alwaysAsk.force",False)
    profile.set_preference("browser.download.manager.showWhenStarting",False)

    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.dir", download_path)

    browser = webdriver.Firefox(options=options, firefox_profile=profile)  
    return browser


def _firefox_blank_page(browser):
    browser.get('about:blank')


def _download_microsoft_academic_bibtex(browser, search_str, all_results, delay):

    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By

    search_url = ''.join([MICROSOFT_ACADEMIC_URL, 'search?q=', search_str, '&f=&orderBy=0&skip=0&take=10'])
    browser.get(search_url) 

    myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'cite')))
    cite = browser.find_elements_by_class_name('cite')
    cite[0].click()

    myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'download-button')))
    download = browser.find_elements_by_class_name('download-button')
    download[1].click()


def _get_bibtex_contents(download_dir):
    import os
    bib_files = [f for f in os.listdir(download_dir) if f.endswith('.bib')]

    bibtex_contents = []
    for bib_file in bib_files:
        bib_path = os.path.join(download_dir, bib_file)
        with open(bib_path) as bib_content:
            bibtex_contents.append(bib_content.read())

    return bibtex_contents


def query(search_str, all_results=False, download_path=None, delay=120):

    from selenium.common.exceptions import TimeoutException

    # create a folder to download
    if not download_path:
        import tempfile
        download_dir = tempfile.mkdtemp()
    else:
        download_dir = download_path

    browser = _create_firefox_browser(download_dir)
    bibtex_contents = []
    try:
        _download_microsoft_academic_bibtex(browser, search_str, all_results=all_results, delay=delay)
        bibtex_contents = _get_bibtex_contents(download_dir)
    except TimeoutException as e:
        print(e)


    browser.quit()
    if not download_path:
        import shutil
        shutil.rmtree(download_dir)

    return bibtex_contents


def query_all(search_strs, all_results=False, download_path=None, delay=120):
    from selenium.common.exceptions import TimeoutException

    # create a folder to download
    if not download_path:
        import tempfile
        download_dir = tempfile.mkdtemp()
    else:
        download_dir = download_path

    browser = _create_firefox_browser(download_dir)
    bibtex_contents = []

    for search_str in search_strs:
        _firefox_blank_page(browser)
        try:
            _download_microsoft_academic_bibtex(browser, search_str, all_results=all_results, delay=delay)
        except TimeoutException as e:
            print(e)

    bibtex_contents = _get_bibtex_contents(download_dir)

    browser.quit()
    if not download_path:
        import shutil
        shutil.rmtree(download_dir)

    # print(bibtex_contents)
    return bibtex_contents
