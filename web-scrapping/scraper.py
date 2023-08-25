from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

START_URL = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"


empty_list = []

def scrape_more_data(hyperlink):
    try:
        page = requests.get(hyperlink)
        
        soup = BeautifulSoup(page.content, "html.parser")

        temp_list = []

        for tr_tag in soup.find_all("tr", attrs={"class": "fact_row"}):
            td_tags = tr_tag.find_all("td")
          
            for td_tag in td_tags:
                try: 
                    temp_list.append(td_tag.find_all("div", attrs={"class": "value"})[0].contents[0])
                except:
                    temp_list.append("")
                    
        empty_list.append(temp_list)

    except:
        time.sleep(1)
        scrape_more_data(hyperlink)
        

scrapped_data = []

for row in empty_list:
    replaced = []
    for el in row: 
        el = el.replace("\n", "")
        replaced.append(el)
    scrapped_data.append(replaced)

print(scrapped_data)


headers = ["name", "distance", "mass", "radius"]
new_planet_df_1 = pd.DataFrame(scrapped_data,columns = headers)
new_planet_df_1.to_csv('updated_scraped_data.csv',index=True, index_label="id")
