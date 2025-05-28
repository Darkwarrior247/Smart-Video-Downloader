def install_package(package, import_name=None):
import_name = import_name or package
try:
import(import_name)
except ImportError:
print(f"Installing {package}...")
subprocess.check_call([sys.executable, "-m", "pip", "install", package])
 
 

def get_user_links():
install_package('pyperclip')
import pyperclip
 
 

links = []
last_clipboard = ""
paused = threading.Event()
done_event = threading.Event()
 
 

print("\n=== Link Collection Mode ===")
print("Copy video links (Ctrl+C), type 'pause', 'resume', or 'done'.")
 
 

def check_clipboard():
    nonlocal last_clipboard
    while not done_event.is_set():
        if not paused.is_set():
            current_url = pyperclip.paste().strip()
            if (current_url.startswith(('http://', 'https://')) and
                current_url not in links and
                current_url != last_clipboard):
                links.append(current_url)
                last_clipboard = current_url
                print(f"Added link {len(links)}: {current_url}")
        time.sleep(1)
 
 

clipboard_thread = threading.Thread(target=check_clipboard, daemon=True)
clipboard_thread.start()
 
 

try:
    while True:
        user_input = input().lower()
        if user_input == 'done':
            done_event.set()
            break
        elif user_input == 'pause':
            paused.set()
            print("Paused.")
        elif user_input == 'resume':
            paused.clear()
            pyperclip.copy('')
            last_clipboard = ""
            print("Resumed.")
except KeyboardInterrupt:
    done_event.set()
 
 

clipboard_thread.join()
return links
 
 

def click_button_with_opencv(template_path, threshold=0.8, max_tries=5):
install_package("opencv-python", "cv2")
install_package("numpy")
install_package("pyautogui")
import cv2
import numpy as np
import pyautogui
 
 

print(f"Looking for button using template: {template_path}")
template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
if template is None:
    print(f"Template image '{template_path}' not found or could not be loaded.")
    return False
w, h = template.shape[::-1]
 
 

for attempt in range(max_tries):
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
 
 

    res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
 
 

    print(f"Attempt {attempt+1}: Match confidence = {max_val:.2f}")
 
 

    if max_val >= threshold:
        center_x = max_loc[0] + w // 2
        center_y = max_loc[1] + h // 2
        pyautogui.moveTo(center_x, center_y, duration=0.2)
        pyautogui.click()
        print(f"Clicked the button: {template_path}")
        return True
    else:
        time.sleep(1)
print(f"Button not found on screen: {template_path}")
return False
 
 

def open_and_click_video_buttons(links):
install_package("selenium")
install_package("webdriver-manager")
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
 
 

print("\nOpening links in Firefox...")
 
 

# Set Firefox options
firefox_options = webdriver.FirefoxOptions()
firefox_options.add_argument("--disable-notifications")
firefox_options.add_argument("--mute-audio")
# You can add more options if needed
 
 

driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)
 
 

for i, link in enumerate(links, 1):
    print(f"Opening {i}/{len(links)}: {link}")
    driver.get(link)
    time.sleep(7)  # Wait for page to load and video to appear
 
 

    # 1. Try HD-1, then HD-2
    if not click_button_with_opencv("HD-1.png"):
        print("HD-1 not found, trying HD-2...")
        click_button_with_opencv("HD-2.png")
    time.sleep(2)
 
 

    # 2. Try play, then download
    if not click_button_with_opencv("play.png"):
        print("Play button not found, trying download button...")
        click_button_with_opencv("download.png")
    time.sleep(3)  # Give IDM time to catch the video
 
 

print("\nAll links opened and buttons clicked. Check IDM for download progress.")
 
 

def main():
links = get_user_links()
if not links:
print("No links collected.")
return
open_and_click_video_buttons(links)
 
 

if name == "main":
main()