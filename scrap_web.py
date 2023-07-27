import requests
from bs4 import BeautifulSoup
import json

def openLinkAndReturnSoup(tutorial_link):
    response = requests.get(tutorial_link)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

def get_tutorial_links(tutorial_link):
    tutorial_links = []
    scrap_web = openLinkAndReturnSoup(tutorial_link)
    panel_body = scrap_web.findAll("p", {"class": "article-links"})
    for panel in panel_body:
        anchors = panel.findAll("a")
        for anch in anchors:
            if anch['href']:
                tutorial_links.append(anch["href"])
    return tutorial_links
def get_tutorial_content(tutorial_link):
    tutorial_text = []
    tutorial_content = openLinkAndReturnSoup(tutorial_link)
    tut_soup_content = tutorial_content.findAll("div", {"class": "tutorial-content"})
    for tut_soup in tut_soup_content:
        scrap_tut = tut_soup.findAll("p")
        for tut in scrap_tut:
            select = tut.text.replace("\n", "")
            tutorial_text.append(select)
    return tutorial_text

def get_tutorial_code(tutorial_link):
    tutorial_code = []
    tutorial_content = openLinkAndReturnSoup(tutorial_link)
    tut_soup_code = tutorial_content.findAll("code", {"class": "language-js"})
    for tut_soup in tut_soup_code:
        scrap_tutcodes = tut_soup.findAll("span")
        for scrap_tutcode in scrap_tutcodes:
            codetxt = scrap_tutcode.text
            tutorial_code.append(codetxt)
    tutorial_code_clean = " ".join(tutorial_code).replace("\n", "")
    return tutorial_code_clean
def final_scraping(tuts_link):
    tutorial_links = get_tutorial_links(tuts_link)
    great_dict = dict()
    for tutorial in tutorial_links:
        great_dict[tutorial] = dict()
        tutorial_contents = get_tutorial_content(tutorial)
        great_dict.get(tutorial)["text"] = tutorial_contents
        tutorial_codes = get_tutorial_code(tutorial)
        great_dict.get(tutorial)["code"] = tutorial_codes
    return great_dict

master_dict = final_scraping("https://generativeartistry.com/tutorials/")
print(master_dict)

def write_tutorials_to_jsonfile(json_file, my_dict):
    with open (json_file, "w", encoding="UTF-8") as jsonfile:
        json.dump(my_dict, jsonfile, ensure_ascii=False, indent=4)

print(write_tutorials_to_jsonfile("tutorial_file.json", master_dict))