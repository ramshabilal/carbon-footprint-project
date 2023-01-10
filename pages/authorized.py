import json
import requests
import math
import streamlit as st
from nordigen import NordigenClient
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from PIL import Image

st.write("Authorization Complete! Please close this tab and move back to the previous tab")