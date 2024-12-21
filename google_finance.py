from playwright.sync_api import sync_playwright

def parse_article_content(context, link):
    """
    存在问题需解决：
    1. 不同来源的页面文章结构不同
    2. 有些需要登录才能查看文章
    3. 有些文章内容是通过 JavaScript 动态加载的
    """
    try:
        article_page = context.new_page()
        article_page.goto(link)
        # article_page.wait_for_selector("article")
        content = article_page.locator("article").first.text_content()
        article_page.close()
        print("处理成功")
        return content
    except Exception as e:
        print(f"Error parsing article content: {e}")
        return ""

def get_top_story():
    """
    获取 Google Finance 首页 Today's financial news 栏目的
    Top stories
    """
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

                    print(f"正在处理: {title}")
                    print(f"来源: {source}")

                    content = parse_article_content(context, link)

                    top_stories.append({
                        "title": title,
                        "source": source,
                        "time": time,
                        "link": link,
                        "image": img_url,
                        "content": content
                    })

                    print(f"已提取: {title}")

                    
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
    save_dir = "google_finance_articles"
    stories = get_top_story()
    for story in stories:
        # save as a text file
        with open(f"{save_dir}/{story['title']}.txt", "w") as f:
            f.write(story['content'])

        print(f"Title: {story['title']}")
        print(f"Source: {story['source']}")
        print(f"Time: {story['time']}")
        print(f"Link: {story['link']}")
        print(f"Image URL: {story['image']}")
        print("-" * 50)