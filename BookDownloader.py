# -----------------------------------------------------#
#          Archive.org Book downloader (R1)            #
# -----------------------------------------------------#
#
#   Downloads books that you need to borrow from
#   archive.org and stores the book pages in a folder.
#   This project uses selenium to interface with
#   archive.org.
#
#   Usage:
#       BookDownloader.py <ID> <username> <password> <output dir>
#       <ID> - the URL ID of the book
#       <username> - Archive.org username
#       <password> - Archive.org password
#       <output dir> - [Optional] Directory to create the <ID>
#                      output directory in. If not specified then
#                      the current working directory is used.
#   Notes:
#       The script downloads the book images to the folder
#       named <ID>. If the folder exists then the script
#       will skip any files of the same name.
#
#       This script only downloads borrowable books from
#       archive.,org. Regular files are not downloadable
#       with this script yet.

#   Import the necessary libraries
import os
import re
import sys
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


username = ''  # archive.org username
password = ''  # archive.org password

archiveId = ''  # archive.org item ID
outputDir = ''  # Directory to create the output directory in

archDir = ''    # Directory to put the files in

# Page variables
currentPage = 1
pageCount = 1
#pageCount_regex = re.compile(r'\s(\d\d\d\d)|\s(\d\d\d)|\s(\d\d)|\s(\d)')  # regex to get the page count
#currentPage_regex = re.compile(r'/\((\d\d\d\d)|\((\d\d\d)|\((\d\d)|\((\d)')  # regex to get the current page
pageFilename_regex = re.compile(r'_\d\d\d\d\.')     # regex to extract the page current number
username_selector = '#maincontent > div > div > div.iaform.col-md-8.login-form-section > section.login-form-element.js-third-party-auth-toggle-view > form > label:nth-child(2) > input'
password_selector = '#maincontent > div > div > div.iaform.col-md-8.login-form-section > section.login-form-element.js-third-party-auth-toggle-view > form > label:nth-child(4) > div > input'
# Selectors for borrow/return button
borrow_selectors = ['#IABookReaderMessageWrapper > div > div.BookReaderMessageBody > div.lending-action-group.btn-group > button.lending-primary-action.btn.btn-primary'
                    , '#IABookReaderMessageWrapper > div > div.BookReaderMessageBody > button'
                    , '#IABookReaderMessageWrapper > div > div.BookReaderMessageBody > button.BRaction.btn.btn-primary']
pagecount_selector = '#BookReader > div.BRfooter > div > nav > ul.controls > li.scrubber > p > span'
nextPage_xpath = '//*[@title="Flip right"]'
page_class = 'BRpageimage'

# Page elements
global borrow_btn
global nextPage_btn

# Timer variables
# start_time = 0      # Start time of the timer
max_time = 55 * 60  # Time in which to borrow the book again
end_time = 0

# function calls
def permissionTest(targetdir) -> bool:
    # Check if a file can be written to the directory
    try:
        pertest = open(targetdir + os.sep + '__permission.test', 'w')
        pertest.close()
        os.remove(targetdir + os.sep + '__permission.test')
        return True
    except:
        return False


#   Open a url in a new tab
def openNewTab(link: str, driver: webdriver.Chrome):
    driver.execute_script("window.open('" + link + "')")
    driver.switch_to.window(driver.window_handles[-1])
    return driver.window_handles[-1]

def downloadFile(fileUrl:str, driver: webdriver.Chrome):
    js = '''
   var link = document.createElement('a');
    link.setAttribute('href', '{0}');
    link.setAttribute('download', '');
    link.click();'''.format(url)
    driver.execute_script(js)

def newChromeBrowser(headless=True, downloadPath=None):
    """ Helper function that creates a new Selenium browser """
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('headless')
    if downloadPath is not None:
        prefs = {}
        prefs["profile.default_content_settings.popups"] = 0
        prefs["download.default_directory"] = downloadPath
        options.add_experimental_option("prefs", prefs)
    newBrowser = webdriver.Chrome(options=options)
    return newBrowser

def refreshElements():
    global nextPage_btn
    global borrow_btn
    global browser

    elementsFound = False
    for selector in borrow_selectors:
        if elementsFound is False:
            try:
                borrow_btn = browser.find_element_by_css_selector(selector)
                elementsFound = True
                break   # Exit loop
            except NoSuchElementException:
                # Cannot find element
                pass

    if elementsFound is False:
        browser.quit()
        print('Cannot refresh elements')
        sys.exit('Exiting....')

    nextPage_btn = browser.find_element_by_xpath(nextPage_xpath)

# Check command line arguments
if len(sys.argv) == 4:
    archiveId = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    outputDir = os.getcwd()  # Set output dir
elif len(sys.argv) == 5:
    archiveId = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    outputDir = sys.argv[4]  # Set output dir

elif len(sys.argv) > 5:
    # End script if there are too many arguments
    sys.exit('Too many arguments')
else:
    # Go to interactive mode if there are too few arguments
    print('Not enough arguments, going to interactive mode.\n')
    print('Archive ID:')
    archiveId = input()

    print('Archive username:')
    username = input()

    print('Archive password:')
    password = input()

    print('Output directory (leave blank for current working directory:')
    outDir = input()
    if len(outDir) == 0:
        outputDir = os.getcwd()
        print('Using working dir: ' + os.getcwd())
    else:
        outputDir = outDir
# Check if dir can be written to
if permissionTest(outputDir) is False:
    print('File permission error, does the folder exist? do you have read/write permissions?')
    sys.exit('File error')

# Create <ID> dir of check if it already exists (resume support)
if os.path.exists(outputDir + os.sep + archiveId) is False:
    print('Creating output directory: ' + outputDir + os.sep + archiveId)
    os.makedirs(outputDir + os.sep + archiveId)
else:
    print('Output directory already exists at: ' + outputDir + os.sep + archiveId)

archDir = outputDir + os.sep + archiveId  # set archive directory

# Open selenium window
browser = newChromeBrowser(False, archDir)  # Open selenium windows (will convert to phantomJS in the future?)

# Log onto archive account
browser.get('https://archive.org/account/login')
time.sleep(30)

# username textbox
username_txt = browser.find_element_by_css_selector(username_selector)
# password textbox
password_txt = browser.find_element_by_css_selector(password_selector)

username_txt.send_keys(username)
password_txt.send_keys(password)
password_txt.submit()

time.sleep(30)  # Wait for page to load

# Check if password is correct
if browser.current_url != 'https://archive.org/':
    # Username or password did to work now exit the application
    browser.quit()
    print('Invalid username or password. Exiting...')
    sys.exit('Incorrect logon details')

# Go to webpage with the current ID and at the first page in 2page mode
browser.get('https://archive.org/details/' + archiveId + '/page/n0/mode/2up')
time.sleep(30)  # Wait for page to load

# Check to see if archive ID is valid
if browser.title == 'Internet Archive: Error':
    # Went to invalid id
    browser.quit()
    print('Wrong archive ID. Exiting...')
    sys.exit('Invalid archive ID')

# Check to see if the item is a book that can be borrowed
elementFound = False
for cssSelector in borrow_selectors:
    if elementFound is False:
        try:
            borrow_btn = browser.find_element_by_css_selector(cssSelector)
            elementFound = True
            break   # Exit loop
        except:
            # Cannot find element or other error
            pass

if elementFound is False:
    browser.quit()
    print('Not a book that can be borrowed. Exiting...')
    sys.exit('Book cannot be borrowed')

# Borrow the book
print('Borrowing the book...')
borrow_btn.click()
time.sleep(30)  # wait 30 seconds to borrow

# Get the page count
pageCount = int(browser.find_element_by_css_selector(pagecount_selector).text.split('of')[1].strip(' ()'))
print('Book page count: ' + str(pageCount))

# Get the next page button
nextPage_btn = browser.find_element_by_xpath(nextPage_xpath)

# Record end time
end_time = time.perf_counter() + max_time

actualPageCount = 1
# Start download loop
while currentPage != pageCount:
    # Get image URL's for both pages
    pages = browser.find_elements_by_class_name(page_class)
    for page in pages:
        print('Downloading page ' + str(actualPageCount))
        url = page.get_attribute('src')
        url = re.sub(r'scale=\d', 'scale=3', url)  # Set the image url to load the medium size image
        # Open new window with the image
        openNewTab(url, browser)
        url = url.replace('scale=3', 'scale=0')  # Set the image url to load the full size image
        time.sleep(15)
        #print(url)
        # Download the image
        downloadFile(url, browser)
        time.sleep(15)
        # Increment page count
        actualPageCount += 1
        # Close current window
        browser.close()
        browser.switch_to.window(browser.window_handles[0])

    if time.perf_counter() > end_time:
        print('Returning and borrowing the book again..,')
        refreshElements()
        # Return to the book and borrow again
        print('Returning book...')
        borrow_btn.click()
        time.sleep(30)  # wait 20 seconds to return
        refreshElements()
        print('Borrowing book...')
        borrow_btn.click()
        time.sleep(30)  # wait 30 seconds to borrow
        refreshElements()
        end_time = time.perf_counter() + max_time
        print('Continuing book downloading...')
    if browser.find_element_by_css_selector(pagecount_selector) is not None:
        currentPage = int(browser.find_element_by_css_selector(pagecount_selector).text.split('of')[0].strip(' ()'))

    nextPage_btn.click()  # Go to the next page
    time.sleep(5)

print('Finished downloading book.')
refreshElements()
print('Returning book...')
borrow_btn.click()
time.sleep(20)
# Close selenium window
browser.quit()

# print download stats
