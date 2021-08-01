import string
import json

import requests
from bs4 import BeautifulSoup

def json_scraper(): 
    # Request
    url = input()
    request = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})

    if "imdb" and "title" in url and request:

        # SOUP
        soup = BeautifulSoup(request.content, "html.parser")

        # Parse json
        json_dict = json.loads(
            "".join(soup.find("script", {"type": "application/ld+json"}).contents))

        # Parse Og Title
        og_title = json_dict["name"]

        # Parse description
        description = json_dict["description"]

        if og_title is not None and description is not None:
            final_dict = {}
            final_dict["title"] = og_title
            final_dict["description"] = description

            return(final_dict)

        else:
            return("Invalid movie page!")

    else:
        return("Invalid movie page!")





def hmtl_scraper():
    url = "https://www.nature.com/nature/articles"

    news_attribute = {"type": "news"}
    article_links = []

    # Obtaining a request object
    request = requests.get(url, news_attribute)

    if request:  # Checking if the request returned an error
        soup = BeautifulSoup(request.content, "html.parser")
        links_attribute = soup.find_all(
            "a", {"class": "c-card__link u-link-inherit"})

        for attribute in links_attribute:
            article_link = "https://www.nature.com" + attribute.get("href")

            # Checking if the article was already saved
            if article_links.count(article_link) == 0:
                # Storing the link
                article_links.append(article_link)

                # Obtaining a request object for the article url
                article_request = requests.get(article_link)

                # Retrieving the article name
                article_soup = BeautifulSoup(
                    article_request.content, "html.parser")
                file_name = article_soup.find("title").text

                # Replacing whitespaces and punctuation
                for char in file_name:
                    if char in string.punctuation:
                        file_name = file_name.replace(char, "")
                file_name = file_name.replace(" ", "_")

                # Saving the content of the article
                article_file = open(file_name + ".txt", "wt", encoding="UTF-8")

                # Writing the content of the page in the files
                for i in article_soup.find_all("div", {"class": "c-article-body u-clearfix"}):
                    article_file.write(i.text.strip())


        
