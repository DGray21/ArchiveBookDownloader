# :books: Archive.org Book Downloader
Download borrow-only books off archive.org.

## Setup
1. Install Python 3 from [here](https://www.python.org/downloads/) (make sure you click add python to PATH)
2. Install Google Chrome from [here](https://www.google.com/chrome/)
3. Download **BookDownloader.py** and **requirements.txt** from the repo above
4. Download the chrome webdriver [here](https://chromedriver.chromium.org/downloads) for the version of chrome you have installed on your device
5. Install the required modules by running **install_modules.cmd** from the above repo above or directly from the command line with `pip install -r requirements.txt`

## Book Downloading
There are two main ways to use this script:
* Automatic mode (useful batch jobs):
  * `BookDownloader.py <ID> <username> <password> <output dir>`   
   \<ID\> \- The id of the book your are downloading (usually https://archive.org/details/<ID\>)   
   \<username\> \- Archive username  
   \<password\> \- Archive password  
   \<output dir\> \- Output directory to create the output dir in (leave blank to set the current dir as output)  
* Manual mode (for quick downloads)
  * To run in manual mode, run the script without any arguments. It will ask for the id , username, password and output directory.

## TODO for future releases
- [ ] Binary release
- [ ] Headless mode (coming in R2)
- [ ] Webdriver selection (chrome/firefox)
- [ ] Lists/batch support
- [ ] GUI?  



Under MIT licsense
