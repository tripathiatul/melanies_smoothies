# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f"Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Chose the fruits you want in your Custom smoothie!
  """)
name_on_order = st.text_input("Name on Smoothie:")
st.write("Your name on Smoothie will be", name_on_order)

# session = get_active_session()


cnx=st.connection("snowflake")
session=cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()
ingredients_list=st.multiselect(
    'Choose upto 5 ingredients:',
    my_dataframe,
)
ingredients_string=''
if ingredients_list:

 for fruit_chosen in ingredients_list:
     ingredients_string+=fruit_chosen
     st.subheader(fruit_chosen+' Nutrition_information')
     smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+fruit_chosen)
     sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
 st.write(ingredients_string)

my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

st.write(my_insert_stmt)
# st.stop()
time_to_insert=st.button('Submit Order')

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!')




