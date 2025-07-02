import time
import subprocess
import sys
import threading
import pyautogui
import cv2
import numpy as np
import pyperclip


def install_package(package):
    try:
        __import__(package)
    except ImportError:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def get_user_links():
    install_package('pyperclip')
    links = []
    last_clipboard = ""
    paused = threading.Event()
    done_event = threading.Event()

    print("\n=== Link Collection Mode ===")
    print("Copy video links (Ctrl+C), type 'pause', 'resume', or 'done'.")

    def check_clipboard():  # Fixed the function name here
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
    print(f"Looking for button using template: {template_path}")
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        print(f"Template image '{template_path}' not found or could not be loaded.")
        return False
    w, h = template.shape[::-1]

    for attempt in range(max_tries):
        # Ensure dependencies are installed before taking screenshot
        install_package('pyscreeze')
        install_package('Pillow')

        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

        res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        print(f"Attempt {attempt + 1}: Match confidence = {max_val:.2f}")

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


def open_link_and_click_buttons(link, quality, download_choice):
    # Open the link in the default web browser
    import webbrowser
    webbrowser.open(link)
    time.sleep(7)  # Wait for the page to load

    # Click on Download button
    if not click_button_with_opencv("download.png"):
        print("Download button not found.")
        return

    # Click on the selected quality button using OpenCV
    quality_template = f"{quality}.png"  # Assuming quality images are named "360p.png", "720p.png", "1080p.png"
    if not click_button_with_opencv(quality_template):
        print(f"{quality} button not found.")
        return

    if download_choice == 'now':
        # Click on the Start Download button (assuming it's named "start_download.png")
        if not click_button_with_opencv("start_download.png"):  # Add your start download image here
            print("Start Download button not found.")
            return
        print("Download started. Check your download manager for progress.")
        minimize_idm()  # Minimize IDM after starting the download

    elif download_choice == 'later':
        # Click on Download Later button
        if not click_button_with_opencv("download_later.png"):  # Assuming the image is named "download_later.png"
            print("Download Later button not found.")
            return
        print("Video will be downloaded later. Check your download manager for progress.")

    else:
        print("Invalid choice. Please enter 'now' or 'later'.")


def minimize_idm():
    # Click the minimize button in IDM
    if not click_button_with_opencv("minimize_idm.png"):  # Assuming the image is named "minimize_idm.png"
        print("Minimize button not found in IDM.")


def open_idm_and_start_queue():
    # Open Internet Download Manager
    subprocess.Popen(["C:\\Program Files (x86)\\Internet Download Manager\\IDMan.exe"])  # Adjust the path if necessary
    time.sleep(5)  # Wait for IDM to open

    # Click the Start Queue button in IDM
    if not click_button_with_opencv("start_queue.png"):  # Assuming the image is named "start_queue.png"
        print("Start Queue button not found in IDM.")


def main():
    # Install all required dependencies first
    install_package('pyautogui')
    install_package('opencv-python')
    install_package('numpy')
    install_package('pyscreeze')
    install_package('Pillow')
    install_package('pyperclip')

    while True:  # Loop to keep asking for links until valid links are collected
        links = get_user_links()
        if not links:
            print("No links collected. Please copy video links and type 'done' when finished.")
            continue  # Ask for links again

        while True:  # Loop for quality selection
            quality = input("Enter the desired download quality (360p, 720p, 1080p): ").strip()
            if quality in ['360p', '720p', '1080p']:
                break  # Valid quality input, exit the loop
            else:
                print("Invalid quality selected. Please enter 360p, 720p, or 1080p.")

        while True:  # Loop for download choice selection
            download_choice = input(
                "Do you want to start the download now or download later? (Enter 'now' or 'later'): ").strip().lower()
            if download_choice in ['now', 'later']:
                break  # Valid download choice, exit the loop
            else:
                print("Invalid choice. Please enter 'now' or 'later'.")

        # Process each link one by one
        for link in links:
            print(f"Processing link: {link}")
            open_link_and_click_buttons(link, quality, download_choice)
            time.sleep(2)  # Wait a bit before closing the tab (if needed)
            # Close the current tab (if using a browser that supports this)
            pyautogui.hotkey('ctrl', 'w')  # Close the current tab
            time.sleep(1)  # Wait for the tab to close

        if download_choice == 'later':
            open_idm_and_start_queue()

        print("All links processed.")
        break  # Exit the loop after processing the links


if __name__ == "__main__":
    main()
