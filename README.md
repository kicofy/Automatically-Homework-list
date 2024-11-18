# Renweb Homework Fetcher

This tool automatically fetches homework assignments from Renweb by logging into your account.

## Required Files

Make sure you have all these files:
1. `python-3.x.x-amd64.exe` - Python installer
2. `wing-9.1.2.0.exe` - Wing IDE installer
3. `msedgedriver.exe` - Edge browser driver
4. `main.py` - Main program
5. `Download the required libraries.cmd` - Library installation script

## Setup Instructions

1. Install Python
   - Double-click `python-3.x.x-amd64.exe`
   - Must check "Add Python to PATH"
   ![Python Installation](<PIC/Python install.png>)
   - Click "Install Now"

2. Install Wing IDE
   - Double-click `wing-9.1.2.0.exe`
   - Use default options
   - It will automatically detect Python path on first launch

3. Install Required Libraries
   - Double-click `Download the required libraries.cmd`
   - Wait for completion

4. Browser Driver Setup
   - By default, uses Microsoft Edge browser
   - Place `msedgedriver.exe` in the same folder as `main.py`
   
   If you want to use Chrome browser:
   1. Check your Chrome version
      - Open Chrome
      - Click three dots in top-right corner
      - Click "Help" > "About Google Chrome"
      - Note down the version number
   
   2. Download matching ChromeDriver
      - Visit https://chromedriver.chromium.org/downloads
      - Download driver matching your Chrome version
      - Extract the downloaded file
   
   3. Configure driver path
      - Place chromedriver.exe anywhere you like
      - Find `driver_path` variable at the top of `main.py`
      - Fill in the full path to chromedriver.exe, for example:
      ```python
      driver_path = "C:/WebDriver/chromedriver.exe"  # Change to your chromedriver path
      ```
      - If placed in current directory, you can simply write:
      ```python
      driver_path = "chromedriver.exe"
      ```

## Program Configuration

1. Open `main.py` in Wing IDE
2. Modify login information at the top:
```python
username = "...@..."  # Your Renweb username
password = "......."  # Your Renweb password
```
![Configuration](<PIC/Code Change.png>)

## Running the Program
![IDE Interface](<PIC/IDE interface.png>)
1. Open `main.py` in Wing IDE
2. Click the run button (green triangle) or press F5
3. The program will:
   - Open browser
   - Log in
   - Fetch homework
   - Display assignments
   - Close browser

## Troubleshooting

1. "msedgedriver.exe not found"
   - Check driver location

2. "Module not found"
   - Run the library installation script again

3. Can't login
   - Verify username and password
   - Check internet connection

4. Wing IDE can't run Python
   - Verify "Add Python to PATH" was checked
   - Restart Wing IDE
   - Check Python interpreter settings in Wing IDE (Edit > Preferences > Python Configuration)