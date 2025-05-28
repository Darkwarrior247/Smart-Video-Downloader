import time
import subprocess
import sys
import pyautogui
import cv2
import numpy as np
&nbsp;
&nbsp;

def install_package(package):
    try:
        __import__(package)
    except ImportError:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
&nbsp;
&nbsp;

def click_button_with_opencv(template_path, threshold=0.8, max_tries=5):
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        print(f"Template image '{template_path}' not found or could not be loaded.")
        return False
    w, h = template.shape[::-1]
&nbsp;
&nbsp;

    for attempt in range(max_tries):
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
&nbsp;
&nbsp;

        res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
&nbsp;
&nbsp;

        print(f"Attempt {attempt+1}: Match confidence = {max_val:.2f}")
&nbsp;
&nbsp;

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
&nbsp;
&nbsp;

def open_link_and_click_buttons(link, quality):
    # Open the link in the default web browser
    import webbrowser
    webbrowser.open(link)
    time.sleep(7)  # Wait for the page to load
&nbsp;
&nbsp;

    # Click on HD-1 button
    if not click_button_with_opencv("HD-1.png"):
        print("HD-1 button not found.")
    time.sleep(2)
&nbsp;
&nbsp;

    # Click on Play button
    if not click_button_with_opencv("play.png"):
        print("Play button not found.")
    time.sleep(3)  # Wait for the video to start
&nbsp;
&nbsp;

    # Click on Download button
    if not click_button_with_opencv("download.png"):
        print("Download button not found.")
        return
&nbsp;
&nbsp;

    # Click on the selected quality button using OpenCV
    quality_template = f"{quality}.png"  # Assuming quality images are named "360p.png", "720p.png", "1080p.png"
    if not click_button_with_opencv(quality_template):
        print(f"{quality} button not found.")
        return
&nbsp;
&nbsp;

    # Click on Download Later button
    if not click_button_with_opencv("download_later.png"):  # Assuming the image is named "download_later.png"
        print("Download Later button not found.")
&nbsp;
&nbsp;

    print("All actions performed. Check your download manager for progress.")
&nbsp;
&nbsp;

def main():
    install_package('pyautogui')
    install_package('opencv-python')
    install_package('numpy')
&nbsp;
&nbsp;

    # Specify the link to open
    link = input("Enter the video link: ")
    quality = input("Enter the desired download quality (360p, 720p, 1080p): ").strip()
&nbsp;
&nbsp;

    # Validate quality input
    if quality not in ['360p', '720p', '1080p']:
        print("Invalid quality selected. Please enter 360p, 720p, or 1080p.")
        return
&nbsp;
&nbsp;

    open_link_and_click_buttons(link, quality)
&nbsp;
&nbsp;

if __name__ == "__main__":
    main()