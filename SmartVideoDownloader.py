import time
import subprocess
import sys
import threading
import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
 
 

def install_package(package):
try:
import(package)
except ImportError:
print(f"Installing {package}...")
subprocess.check_call([sys.executable, "-m", "pip", "install", package])
 
 

def get_user_links():
install_package('pyperclip')
import pyperclip
 
 

links = []
last_clipboard = ""
paused = False
done_event = threading.Event()
 
 

print("\n=== Link Collection Mode ===")
print("Copy video links (Ctrl+C), type 'pause', 'resume', or 'done'.")
 
 

def check_clipboard():
    nonlocal last_clipboard, paused
    while not done_event.is_set():
        if not paused:
            current_url = pyperclip.paste().strip()
            if (current_url.startswith(('http://', 'https://')) and
                current_url not in links and
                current_url != last_clipboard):
                links.append(current_url)
                last_clipboard = current_url
                print(f"Added link {len(links)}: {current_url}")
        time.sleep(1)
 
 

clipboard_thread = threading.Thread(target=check_clipboard)
clipboard_thread.daemon = True
clipboard_thread.start()
 
 

try:
    while True:
        user_input = input().lower()
        if user_input == 'done':
            done_event.set()
            break
        elif user_input == 'pause':
            paused = True
            print("Paused.")
        elif user_input == 'resume':
            paused = False
            pyperclip.copy('')
            last_clipboard = ""
            print("Resumed.")
except KeyboardInterrupt:
    done_event.set()
 
 

clipboard_thread.join()
return links
 
 

def open_and_trigger_idm(links):
print("\nOpening links in Chrome...")
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)  # Keep Chrome open
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--mute-audio")
 
 

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
 
 

for i, link in enumerate(links, 1):
    print(f"Opening {i}/{len(links)}: {link}")
    driver.execute_script(f"window.open('{link}');")
    time.sleep(5)  # Wait for IDM to detect and show its dialog
 
 

    print("Attempting to auto-confirm IDM...")
    # Method 1: Press Enter (works if IDM window is focused)
    import pyautogui
 
 

    # Try pressing Enter first
    pyautogui.press("enter")
    time.sleep(1)
 
 

    # If pressing Enter doesn't work, use image-based click
    print("Trying image-based click...")
    button_location = pyautogui.locateCenterOnScreen("start_download.png", confidence=0.8)
 
 

    if button_location:
        pyautogui.moveTo(button_location, duration=0.2)
        pyautogui.click()
        print("Clicked 'Start Download' button.")
    else:
        print("Could not find 'Start Download' button on screen.")
 
 

    # Optional: Method 2 (if Enter doesn't work, use image-based click)
    # pyautogui.click(pyautogui.locateCenterOnScreen("start_download.png"))
 
 

    time.sleep(2)
 
 

print("\nAll links opened. Check IDM for download progress.")
 
 

def main():
install_package("selenium")
install_package("webdriver-manager")
install_package("pyperclip")
install_package("pyautogui")
 
 

links = get_user_links()
if not links:
    print("No links collected.")
    return
 
 

open_and_trigger_idm(links)
 
 

if name == "main":
main()