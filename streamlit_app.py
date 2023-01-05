import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError
streamlit.title("my first app, this is easy")


streamlit.header('Breakfast Menu')
streamlit.text(' 🥗 Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))

streamlit.dataframe(my_fruit_list)

def get_frtData(frt_choice):
  frt_resp = requests.get("https://fruityvice.com/api/fruit/"+frt_choice)
  frt_nrml = pandas.json_normalize(frt_resp.json())
  return frt_nrml


streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("please select a fruit")
  else:
    fun_ret=get_frtData(fruit_choice)
    streamlit.dataframe(fun_ret)
except URLError as e:
  streamlit.error()
#streamlit.write('The user entered ', fruit_choice)

streamlit.header("The fruit load list contains:")
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from fruit_load_list")
    return my_cur.fetchall()
  
if streamlit.button('get fruit list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows=get_fruit_load_list()
  streamlit.dataframe(my_data_rows)


def insert_row_snwflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values('from streamlit')")
    retrun 'thanks for adding : '+ new_fruit

add_my_fruit= streamlit.text_input('what fruit to add: ?')
if streamlit.button(' add a fruit'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  bf_frm_fun= insert_row_snwflake(add_my_fruit)
  streamlit.text(bf_frm_fun)
  
streamlit.stop()



my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)



