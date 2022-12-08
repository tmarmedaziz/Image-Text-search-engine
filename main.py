import streamlit as st
import streamlit.components.v1 as com
from streamlit import caching
import requests
from streamlit_lottie import st_lottie
from PIL import Image
import transform.Transform as tr
import json
import random

import time
st.set_page_config(page_title="Search Engine", page_icon=":mag:", layout="wide")
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


#Calling the css file
local_css("style/styleapp.css")

#define web page , icon de l'application
#----- assests-----


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:                 # if status is unauthorized return nothing
        return None
    return r.json()


# Use local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

#Calling the css file
local_css("style/styleapp.css")

# Image dynamic images
lottie_coding=load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_7fwvvesa.json") 


#Create navbar
st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)
st.markdown("""
<nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #3498DB;">
  <div class="collapse navbar-collapse" id="navbarNav">
    <ul class="navbar-nav">
        <div>My application</div>
    </ul>
  </div>
</nav>
""", unsafe_allow_html=True)

#Create input text  for search engine
with st.container():
    left_column, right_column = st.columns(2)
    with left_column:
        st.title('Welcome to our Application')
        st.time_input('Actual time',key=int)
        st.date_input('Actual date')
    with right_column :
        st_lottie(lottie_coding, height=200, key="coding")
#Adding nav bar
randi = 25
left_container, right_container = st.columns(2)
with right_container:

    
    with st.form("my_form"):
        st.write("Inside the form")
        form_val = st.text_input('', placeholder="Search Here")
        submitted = st.form_submit_button("Search")
        if submitted:
            response = tr.search_by_text_query(form_val).content
            response = json.loads(response)
            images = [(i["_source"]['OriginalURL'], i["_source"]['Title']) for i in response['hits']['hits']]
            images = [images[x:x+4] for x in range(0, len(images), 4)]

            randi = random.randint(0, 10)



#Create input images for search engine

def load_image(image_file):
	img = Image.open(image_file)
	return img      
with left_container:

    st.subheader("Search engine by Image")
    image_file = st.file_uploader(" ", type=["png","jpg","jpeg"])
    

    if ((image_file is not None)and randi==25):


        img = load_image(image_file)
        response = tr.search_by_image_query(img).content
        response = json.loads(response)
        took = response["took"]

        images = [(i["_source"]['OriginalURL'], i["_source"]['Title']) for i in response['hits']['hits']]
        images = [images[x:x+4] for x in range(0, len(images), 4)]
        






try:
    
    if len(response['hits']['hits'])!=0:
        if st.button('Clear'):
            response=[]
            images=[]

        st.write("it took {} ms to search for your query".format(response["took"]))
        st.write("{} results were found".format(len(response['hits']['hits'])))

        for i in images:
            col1, col2, col3 , col4 = st.columns(4)
            with col1:
                st.image(i[0][0], width=400, caption=i[0][1], use_column_width=True)
            with col2:
                try:
                    st.image(i[1][0], width=400, caption=i[1][1], use_column_width=True)
                except:
                    pass
            with col3:
                try:
                    st.image(i[2][0], width=400, caption=i[2][1], use_column_width=True)
                except:
                    pass
            with col4:
                try:
                    st.image(i[3][0], width=400, caption=i[3][1], use_column_width=True)
                except:
                    pass
    else:
        st.write("No result for your query ")
    
except:
    pass




footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position:fixed;  
    padding: 10px;
    bottom: 0px;  
    left: 0;
    width: 100%;  
    background-color: #3498DB;  
text-align: center;
}
</style>
<div class="footer">
 © Tmar Mohamed Aziz & Zouari Rami AIM2023 search-engine </div>
"""
st.markdown(footer,unsafe_allow_html=True)
