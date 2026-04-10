# FB Marketplace Auto Lister

This is a GUI application to automate listing items on Facebook Marketplace using a Hybrid API approach (Undetected ChromeDriver + Requests API XHR Injection).

## Requirements

1. Python 3.7+
2. Google Chrome installed on your machine.

## Installation

Install the required Python packages using pip:

```bash
pip install requests selenium undetected-chromedriver
```

## How to use

1. Run the script:
```bash
python fb_marketplace_ui.py
```
2. In the "Chrome Profile Selection", click "Browse Profile Folder" and select your Google Chrome profile folder (usually located at `C:\Users\YOUR_NAME\AppData\Local\Google\Chrome\User Data`). It is highly recommended that you first open Chrome manually, log into Facebook, and close it before selecting this path. This ensures the script has access to your active session cookies.
3. Fill in your listing details (Title, Price, etc.).
4. Select images from your computer using "Select Images".
5. Click either "Draft Listing" or "Publish Listing". The script will automatically boot up an undetected Chrome browser, bypass simple bot detections, and execute native JS fetch requests within the authenticated browser context to publish the listing fast.
