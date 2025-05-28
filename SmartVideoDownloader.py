import time
import subprocess
import sys
import pyautogui
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

def open_link_and_click_buttons(link):
    # Open the link in the default web browser
    import webbrowser
    webbrowser.open(link)
    time.sleep(7)  # Wait for the page to load
&nbsp;
&nbsp;

    # Simulate mouse clicks for video quality and play buttons
    # You may need to adjust the coordinates based on your screen resolution
    # Click on HD-1 button (replace with actual coordinates)
    pyautogui.click(x=100, y=200)  # Replace with actual coordinates for HD-1
    time.sleep(2)
&nbsp;
&nbsp;

    # Click on Play button (replace with actual coordinates)
    pyautogui.click(x=150, y=250)  # Replace with actual coordinates for Play
    time.sleep(3)  # Wait for the video to start
&nbsp;
&nbsp;

    # Click on Download button (replace with actual coordinates)
    pyautogui.click(x=200, y=300)  # Replace with actual coordinates for Download
&nbsp;
&nbsp;

    print("All actions performed. Check your download manager for progress.")
&nbsp;
&nbsp;

def main():
    install_package('pyautogui')
&nbsp;
&nbsp;

    # Specify the link to open
    link = input("Enter the video link: ")
    open_link_and_click_buttons(link)
&nbsp;
&nbsp;

if __name__ == "__main__":
    main()