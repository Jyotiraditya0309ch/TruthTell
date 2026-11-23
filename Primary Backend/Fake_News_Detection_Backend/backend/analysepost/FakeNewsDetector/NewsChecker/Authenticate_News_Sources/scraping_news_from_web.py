def ScrapeNewsFromWeb(query, num_articles=10):
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from bs4 import BeautifulSoup

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    )

    driver = webdriver.Chrome(options=chrome_options)

    transformed_query = query.replace(" ", "+")
    url = f"https://www.google.com/search?q={transformed_query}&tbm=nws"

    driver.get(url)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    soup = BeautifulSoup(driver.page_source, "html.parser")

    articles = []
    elements = soup.select("a.WlydOe")  # headline links

    for i, elem in enumerate(elements):
        if i >= num_articles:
            break
        articles.append(elem.get_text())

    driver.quit()

    print("News scraped from web....")
    return articles

if __name__=="__main__":
    query="Delhi Railway station accident 20 dead"
    articles=ScrapeNewsFromWeb(query)
    print(articles)
    print(len(articles))


