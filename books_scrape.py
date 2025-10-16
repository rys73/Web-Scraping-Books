from playwright.sync_api import sync_playwright
from urllib.parse import urljoin
import time, csv

url_base = "https://books.toscrape.com/"
chemin_csv = r"C:\Users\ighik\OneDrive\Escritorio\html\py-js\playwirght_projet\projet2\ex2.csv"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url_base)

    data = []

    while True:
        page.wait_for_load_state("networkidle")
        page.wait_for_selector("article.product_pod")

        livres = page.locator("article.product_pod")
        total = livres.count()
        print(f"Page Actuelle : {page.url} ({total} livres)")
        for i in range(total):
            try:
              titre = livres.nth(i).locator("h3 a").get_attribute("title")
            except Exception as e:
                titre = "Pas de titre"
                print(f"Erreur ===> {e}")
            try:
              prix = livres.nth(i).locator("p.price_color").inner_text()
            except Exception as e:
               prix = "Pas de prix"
               print(f"Erreur ===> {e}")
            try:
              href = livres.nth(i).locator("h3 a[href]").get_attribute("href")
              url = urljoin(url_base, href)
            except Exception as e:
               url = "Pas de url"
               print(f"Erreur ===> {e}")
            data.append({"Titre": titre, "Prix": prix, "URL": url})
        next_btn = page.locator("li.next a")
        if next_btn.count() == 0 or not next_btn.is_visible():
            print("Plus de page suivante")
            break
        print("Page suivante...")
        next_btn.click()
        page.wait_for_load_state("networkidle")
        time.sleep(1.5)
    with open(chemin_csv, "w", newline="", encoding="utf-8-sig") as f:
       writer = csv.DictWriter(f, fieldnames=["Titre", "Prix", "URL"])
       writer.writeheader()
       writer.writerows(data)
    browser.close()


