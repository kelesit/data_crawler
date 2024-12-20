from playwright.sync_api import sync_playwright

def scrape_google_finance():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Navigate to Google Finance homepage
        page.goto("https://www.google.com/finance")

        print("Waiting for the page to load...")
        # Wait for the "Today's financial news" section to load
        page.wait_for_selector("text=Today’s financial news")

        print("Scraping the page...")
        # Locate the Top Stories articles
        top_stories_section = page.locator("text=Today’s financial news").locator("..")
        articles = top_stories_section.locator("a").all()

        print("Extracting the data...")
        # Extract article titles and links
        top_stories = []
        for article in articles:
            title = article.text_content()
            link = article.get_attribute("href")
            if title and link:
                top_stories.append({"title": title.strip(), "link": link})

        # Close the browser
        browser.close()

        return top_stories

if __name__ == "__main__":
    stories = scrape_google_finance()
    for story in stories:
        print(f"Title: {story['title']}")
        print(f"Link: {story['link']}")
        print("-")
