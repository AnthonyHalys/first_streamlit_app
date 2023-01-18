import streamlit
import requests
import pandas
import snowflake.connector
from urllib.error import URLError

streamlit.title("My Mom\'s New Healthy Dinner")

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text(' 🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

# section pour afficher FuityVice API Response
streamlit.header("Fruityvice Fruit Advice!")
#ajout du choix de fruit ; réponse kiwi par défaut
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
      streamlit.error("Please sekect a fruit to get information.")
  else:
      fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
      # Normalisation de la reponse JSON de FuityVice 
      fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
      # Affiche la table normalisée dans une grille
      streamlit.dataframe(fruityvice_normalized)

except URLError as e:
   streamlit.error()
      
# don't run anything past here while we troubleshoot
streamlit.stop()

#import snowflake.connector

## requete sur les metadata ajoutées
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
# my_cur = my_cnx.cursor()
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
# my_data_row = my_cur.fetchone()
# streamlit.text("Hello from Snowflake:")
# streamlit.text(my_data_row)

## requete sur les données
# my_cur = my_cnx.cursor()
# my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
# my_data_row = my_cur.fetchone()
# streamlit.text("The fruit load list contains :")
# #streamlit.text(my_data_row)
# streamlit.dataframe(my_data_row)

# requete sur TOUTES les données(as juste une ligne
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
my_data_rows = my_cur.fetchall()
streamlit.text("The fruit load list contains :")
#streamlit.text(my_data_row)
streamlit.dataframe(my_data_rows) 

#Permettre l'ajout d'un fruit à la liste ; réponse kiwi par défaut
add_fruit = streamlit.text_input('What fruit would you to add')
streamlit.write('Thanks for adding ', add_fruit)

# ajout dans la base
my_cur.execute("insert into fruit_load_list values ('from streamlit')")

