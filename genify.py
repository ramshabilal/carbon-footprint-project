import streamlit as st
from uuid import uuid4
from nordigen import NordigenClient
import webbrowser
from bokeh.models.widgets import Div



# initialize Nordigen client and pass SECRET_ID and SECRET_KEY
client = NordigenClient(
    secret_id="f1d3361e-f3d7-44f7-a615-108dd3faf937",
    secret_key="961ba8860159509b6d85dc56b3577bc69b0e26a30418f222a14b85eced3aefc545fcbefd21ad89b1a22fe534c70e75fde4e9ba4fae83177b931bfa9376a23e00"
)

if "client" not in st.session_state:
	st.session_state["client"]=client

# Create new access and refresh token
# Parameters can be loaded from .env or passed as a string
# Note: access_token is automatically injected to other requests after you successfully obtain it
token_data = client.generate_token()

countries = {
    "Austria": "AT",
    "Belgium": "BE",
    "Bulgaria": "BG",
    "Croatia": "HR",
    "Cyprus": "CY",
    "Czech Republic": "CZ",
    "Denmark": "DK",
    "Estonia": "EE",
    "Finland": "FI",
    "France": "FR",
    "Germany": "DE",
    "Greece": "GR",
    "Hungary": "HU",
    "Iceland": "IS",
    "Ireland": "IE",
    "Italy": "IT",
    "Latvia": "LV",
    "Lithuania": "LT",
    "Liechtenstein": "LI",
    "Luxembourg": "LU",
    "Malta": "MT",
    "Netherlands": "NL",
    "Norway": "NO",
    "Poland": "PL",
    "Portugal": "PT",
    "Romania": "RO",
    "Slovakia": "SK",
    "Slovenia": "SI",
    "Spain": "ES",
    "Sweden": "SE",
    "United Kingdom": "UK",
    "Sandbox": "Sandbox" 
}


country_name = st.selectbox("Please enter the country of the bank: ", countries.keys())
country = countries[country_name]

if (country!="Sandbox"):

	institutions = client.institution.get_institutions(country)

	array=[]

	for i in institutions:
		array.append(i["name"])
	institution=st.selectbox("Please select the name of the insitution: ", array)


if st.button("Submit"):
	if country == "Sandbox":
		institution_id="SANDBOXFINANCE_SFIN0000"

	else:
		# Get institution id by bank name and country
		institution_id = client.institution.get_institution_id_by_name(
		    country=country,
		    institution=institution
		)

	# Initialize bank session
	init = client.initialize_session(
	    # institution id
	    institution_id=institution_id, #"SANDBOXFINANCE_SFIN0000"
	    # redirect url after successful authentication
	    redirect_uri="https://ramshabilal-carbon-footprint-project-genify-izy4f3.streamlit.app/contact", 
	    # additional layer of unique ID defined by you
	    reference_id=str(uuid4())
	)

	if "init" not in st.session_state:
		st.session_state["init"]=init



	# Get requisition_id and link to initiate authorization process with a bank
	link = init.link # bank authorization link
	requisition_id = init.requisition_id
	
	link2= "https://www.youtube.com/"

	#webbrowser.open(link) 
	
	js = "window.open('{}')".format(link)  # New tab or window
	html = '<img src onerror="{}">'.format(js)
	div = Div(text=html)
	st.bokeh_chart(div)

	
 	
 	



