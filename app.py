import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time

html_temp = """
              <div style="background-color:{};padding:1px">
              
              </div>
            """

st.title(":world_map: Location Extractor")
st.markdown(html_temp.format("rgba(55, 53, 47, 0.16)"),unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    # About 
    Google Map Location Extractor is a Selenium webscraper that scraps Google Map information based on your queries. 
    """)
    st.markdown(html_temp.format("rgba(55, 53, 47, 0.16)"),unsafe_allow_html=True)
    st.markdown("""
    # How does it work
    Simply enter the type of location you are looking for and a csv file of relevant places with URLs will be provided.
    """)
    st.markdown(html_temp.format("rgba(55, 53, 47, 0.16)"),unsafe_allow_html=True)
    st.markdown("""
    Made by [@nainia_ayoub](https://twitter.com/nainia_ayoub)
    """,
    unsafe_allow_html=True,
    )


col1, col2 = st.columns(2)
with col1:
  place = st.text_input("What are you looking for (ex: Restaurant, Library, etc)")
with col2:
  country = st.text_input("Country, state, and/or city")
if place and country:
  query = place+" in "+country
  search = 'Searching for: '+query
  result = 'Results for: '+query
  query = "+".join(query.split())
  url = 'https://www.google.com/maps/search/'+query+'/'
  #Preparing the chrome webdriver to scrap Google results:
  chrome_options = Options()
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  chrome_options.add_argument("user-agent=whatever you want")
  driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options=chrome_options)
  driver.get(url)
  with st.spinner(search):
    time.sleep(2)
  soup = BeautifulSoup(driver.page_source, 'html.parser')
  urls = []
  labels = []
  for div in soup.findAll('div', attrs={'class':'Nv2PK THOPZb CpccDe'}):
    with st.spinner('Extracting info from the map...'):
      time.sleep(2)

    a = div.find("a")
    url = a['href']
    urls.append(url)
    label = a['aria-label']
    labels.append(label)

  ny_df = pd.DataFrame(list(zip(labels, urls)), columns=['Label', 'URL'])
  st.info(result)
  with st.expander("Open Location Results"):
    st.dataframe(ny_df)
