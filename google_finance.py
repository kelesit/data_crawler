from playwright.sync_api import sync_playwright

def get_top_story():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        try:
            # 导航到 Google Finance 主页
            page.goto("https://www.google.com/finance")
            page.wait_for_selector("div.yY3Lee")
            articles = page.locator("div.yY3Lee").all()

            print("提取数据中...")
            # 提取文章标题和链接
            top_stories = []
            for article in articles:
                try:
                    title = article.locator("div.Yfwt5").text_content().strip()
                    source = article.get_attribute("data-article-source-name")
                    time = article.locator("div.Adak").text_content().strip()
                    link = article.locator("a").first.get_attribute("href")
                    img_url = article.locator("img").get_attribute("src")

                    top_stories.append({
                        "title": title,
                        "source": source,
                        "time": time,
                        "link": link,
                        "image": img_url
                    })
                except Exception as e:
                    print(f"Error processing an article: {e}")
                    continue

            return top_stories
        
        except TimeoutError:
            print("页面加载超时")
            return []
        except Exception as e:
            print(f"出现错误: {e}")
            return []
        finally:
            browser.close()

if __name__ == "__main__":
    stories = get_top_story()
    for story in stories:
        print(f"Title: {story['title']}")
        print(f"Source: {story['source']}")
        print(f"Time: {story['time']}")
        print(f"Link: {story['link']}")
        print(f"Image URL: {story['image']}")
        print("-" * 50)