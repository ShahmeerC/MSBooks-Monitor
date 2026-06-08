import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape(url,data,failed_urls):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html,"html.parser")

    while True:
        products = soup.find_all("li",class_="product")

        for product in products:
            prod_href = product.find("div",class_="woocommerce-loop-product__header").find("a")["href"]
            success = False
            for attempt in range(3):
                try:
                    time.sleep(2)
                    prod_response = requests.get(prod_href,timeout=40)
                    prod_response.raise_for_status()
                    prod_html = prod_response.text
                    prod_soup = BeautifulSoup(prod_html,"html.parser")

                    p = prod_soup.find("div",class_="summary entry-summary")

                    title = p.find("h1", class_="product_title entry-title").text
                    print (f"Scraping product: {title}")
                    price = p.find("p",class_="price").text
                    price = int(price.replace(",","")[2:])

                    attributes = p.find("div",class_="msbooks-attributes").find_all("p")
                    missing_count = 0

                    try:
                        grade = attributes[0].text
                        if "Grade: " in grade:
                            grade = grade.replace("Grade: ","")
                        else:
                            grade = None
                            missing_count += 1
                        grade = grade.replace("LEVEL", "Level").replace("Levels", "Level").replace("level","Level")
                        grade = grade.replace("AS","A").replace("As","A").replace("A2","A")
                        grade = grade.strip().title()
                    except:
                        grade = None

                    try:
                        author = attributes[1-missing_count].text
                        if "Author: " in author:
                            author = author.replace("Author: ","")
                        else:
                            author = None
                            missing_count +=1
                        author = author.strip()
                    except:
                        author = None

                    try:
                        binding = attributes[2-missing_count].text
                        if "Binding: " not in binding:
                            missing_count += 1
                    except:
                        binding = None

                    try:
                        year = attributes[3-missing_count].text
                        if "Year/Edition: " in year:
                            year = year.replace("Year/Edition: ","")
                        else:
                            year = None
                            missing_count += 1
                        year = year.strip()
                    except:
                        year = None

                    try:
                        size = attributes[4-missing_count].text
                        if "Size: " not in size:
                            missing_count += 1
                    except:
                        size = None

                    try: 
                        code = attributes[5-missing_count].text
                        if "Syllabus: " in code:
                            code = code.replace("Syllabus: ","")
                        else:
                            code = None
                            missing_count +=1
                        code = code.strip()
                    except:
                        code = None

                    try: 
                        type = attributes[6-missing_count].text
                        if "Type: " in type:
                            type = type.replace("Type: ","")
                        else:
                            type = None
                            missing_count += 1
                        type = type.replace("O Level","").replace("A Level","").replace("AS Level","")
                        type = type.title()
                        type = type.replace("Year ","Yearly ")
                        type = type.replace("Past Papers","")
                        type = type.replace(" With Mark Scheme","").replace(" With Marking Schemes","")
                        type = type.replace("Unolved","Unsolved").replace("Unolsved","Unsolved")
                        type = type.strip()
                    except:
                        type = None

                    data.append({
                        "Title": title,
                        "Subject code": code,
                        "Author": author,
                        "Grade": grade,
                        "Type": type,
                        "Edition": year,
                        "Price": price
                    })
                    success = True
                    break

                except requests.exceptions.RequestException as e:
                    print (f"Failed request {attempt+1} of {prod_href}, attempting again: {e}")
            
            if not success:
                failed_urls.append(prod_href)

        next_btn = soup.find("a",class_="next")
        if not next_btn:
            break
        else:
            next_url = next_btn["href"]
            next_response = requests.get(next_url)
            next_html = next_response.text
            soup = BeautifulSoup(next_html,"html.parser")


def mini_scrape(url,data):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html,"html.parser")

    while True:
        products = soup.find_all("li",class_="product")
        for product in products:
            prod_href = product.find("h2",class_="woocommerce-loop-product__title").find("a")["href"]
            title = product.find("h2",class_="woocommerce-loop-product__title").find("a").text
            price = product.find("span",class_="price").text
            price = int(price.replace(",","")[2:])
            data.append({
                "URL": prod_href,
                "Title": title,
                "Price": price
            })
        
        next_btn = soup.find("a",class_="next")
        if not next_btn:
            break
        else:
            next_url = next_btn["href"]
            next_response = requests.get(next_url)
            next_html = next_response.text
            soup = BeautifulSoup(next_html,"html.parser")


def cleaner():
    df = pd.read_csv("data/Books.csv")

    df["Subject code"] = df["Subject code"].fillna("Unknown")
    df["Author"] = df["Author"].fillna("No author")
    df["Type"] = df["Type"].fillna("Unknown")
    df["Edition"] = df["Edition"].fillna("Unknown")

    df.loc[df["Title"].str.contains("IGCSE", case=False, na=False),"Grade"] = "IGCSE"

    df["Grade"] = df["Grade"].replace("Igcse","IGCSE")
    df["Type"] = df["Type"].replace({
    "Yearlyly Unsolved": "Yearly Unsolved",
    "Unsolved Topicals": "Unsolved Topical"
    })

    df.loc[df["Title"].str.contains("Topical", case=False, na=False),"Type"] = "Unsolved Topical"
    df.loc[df["Title"].str.contains("Yearly", case=False, na=False),"Type"] = "Yearly Unsolved"
    df.loc[df["Title"].str.contains("Notes", case=False, na=False),"Type"] = "Notes"

    df = df.drop_duplicates(
        subset=[
            "Title",
            "Subject code",
            "Grade",
            "Type",
            "Edition",
            "Price"
        ]
    )
    
    print (df.info())
    df.to_csv("data/Books_cleaned.csv",index=False)


def run_scraper():
    data = []
    failed_urls = []

    url = "https://msbooks.pk/"
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html,"html.parser")

    olevel = soup.find("li",id="menu-item-73353")
    olevel_href = olevel.find("a")["href"]
    scrape(olevel_href,data,failed_urls)

    alevel = soup.find("li",id="menu-item-73355")
    alevel_href = alevel.find("a")["href"]
    scrape(alevel_href,data,failed_urls)

    igcse = soup.find("li",id="menu-item-73359")
    igcse_href = igcse.find("a")["href"]
    scrape(igcse_href,data,failed_urls)

    print (f"Products scraped: {len(data)}")
    df = pd.DataFrame(data)
    df.to_csv("data/Books.csv",index=False)
    df.info()

    print (f"Failed urls: {len(failed_urls)}")
    failed = pd.Series(failed_urls)
    failed.to_csv("data/Failed_urls.csv",index=False)

    cleaner()


def run_mini():
    data = []

    url = "https://msbooks.pk/"
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html,"html.parser")

    olevel = soup.find("li",id="menu-item-73353")
    olevel_href = olevel.find("a")["href"]
    mini_scrape(olevel_href,data)

    alevel = soup.find("li",id="menu-item-73355")
    alevel_href = alevel.find("a")["href"]
    mini_scrape(alevel_href,data)

    igcse = soup.find("li",id="menu-item-73359")
    igcse_href = igcse.find("a")["href"]
    mini_scrape(igcse_href,data)

    print (f"Products scraped: {len(data)}")
    df = pd.DataFrame(data)
    df.to_csv("data/books_monitor.csv",index=False)
    df.info()
