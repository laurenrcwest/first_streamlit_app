
import streamlit
import pandas
import requests
import snowflake.connector

from urllib.error import URLErorr

streamlit.title('My Moms New Healthy Diner')

streamlit.header('Breakfast Favorites')

streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')

streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')

streamlit.text('🐔 Hard-Boiled Free-Range Egg')

streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.header("Fruityvice Fruit Advice!")

fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

#import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+  fruit_choice)

# normalized the json data
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

# displays normalized json data
streamlit.text(fruityvice_normalized)

#stop code from here for troubleshooting
streamlit.stop()

#import snowflake.connector
#snowflake connection query
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
streamlit.text("The fruit load list contains:")
my_cur.execute("SELECT * from PC_RIVERY_DB.PUBLIC.fruit_load_list ")
my_data_rows = my_cur.fetchall()
streamlit.dataframe(my_data_rows)

add_my_fruit= streamlit.text_input('What fruit would you like to add?','Jackfruit')
streamlit.write('Thanks for adding ', add_my_fruit)
my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.fruit_load_list values ('" + add_my_fruit + "') ")



