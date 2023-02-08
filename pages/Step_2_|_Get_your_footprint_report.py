import json
import requests
import math
import streamlit as st
from nordigen import NordigenClient
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
from PIL import Image
import base64





#set page title to Step 2
st.set_page_config(
page_title="Step 2 | Get your footprint report")

#opening the image
#image = Image.open('logo.png')
#displaying the image on streamlit app
#st.image(image, width = 180)

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('back.jpeg')

if 'init' not in st.session_state:
    st.write("You have not authorized with your bank yet. Go to the Genify page to first login to your bank account")
else:
    # Get account id after you have completed authorization with a bank
    # requisition_id can be gathered from initialize_session response
    accounts = st.session_state.client.requisition.get_requisition_by_id(
        requisition_id=st.session_state.init.requisition_id
    )
    if st.session_state.emailAddress == "":
        emailAddress = st.text_input("Your email address was not recorded. Please re-enter: ")
    else:
        emailAddress = st.session_state.emailAddress

    # Get account id from the list.
    account_id = accounts["accounts"][0]
    #account_id="account_0"

    # Create account instance and provide your account id from previous step
    account = st.session_state.client.account_api(id=account_id)


    # Fetch account metadata
    meta_data = account.get_metadata()
    # Fetch details
    details = account.get_details()
    # Fetch balances
    balances = account.get_balances()

    # Fetch transactions
    transactions = account.get_transactions()

    print("hello")
    #st.write("")
    st.write(transactions)

    # Filter transactions by specific date range
    #transactions = account.get_transactions(date_from="2021-12-01", date_to="2022-01-21")

    #f=open("data.json")
    #transactions = json.load(f)


    headers = {
      'username': 'ramsha',
      'carbonfootprint': '1',
      'category': '1',
      'account_id': account_id,
      'model_name': 'model_5',
      'authorization': '6d33727b42d2b57c76eed0664e12f9af'
    }

    total_co2=0

    st.write("This may take a while. Please stay on this page until we email you your report.")
    #st.write(transactions)
    count=0

    transactions_data=[]
    
    for transaction in transactions["transactions"]["booked"]:
        count+=1
        if count == 10:
            break;
        #array not for sandbox
        if st.session_state.country != "Sandbox":
            desc=transaction["remittanceInformationUnstructuredArray"][0]
        else:
            desc = transaction["remittanceInformationUnstructured"]
        #st.write("Description: ")
        #st.write(desc)
        
        amount=transaction["transactionAmount"]["amount"]
        #st.write("amount: ")
        #st.write(amount)
        date = transaction["bookingDate"]
        #st.write("date: " + date)
        country = st.session_state.country
        if country == "Sandbox":
            country = "lt"
        url = f"https://pfm.genify.ai/api/v1.0/txn-data/?date={date}&country={country}&amount={amount}&description={desc}"
        response = requests.get(url, headers=headers)
        try:
            response_json = response.json()
        except ValueError as e:
            print("Error: Not a JSON response")   
            continue
        #response_json=response.json() 
        st.write(response_json)
        
        
        #st.write("response json co2: ")
        
        
        if response_json["Carbon Footprint"] != "Currently not available for this category.":
            total_co2+=float(response_json["Carbon Footprint"])
            #save carbon footprint and category for each transaction
            carbon_footprint = response_json["Carbon Footprint"]
            category = response_json["Category Name"]
            description= response_json["Display Description"]
            # Save transaction data in a dictionary
            transaction_data = { 
                "description": description,
                "amount": amount,
                "carbon_footprint": carbon_footprint,
                "category": category
            }
       
            # Append transaction data to the list
            transactions_data.append(transaction_data)
        
    st.write("transaction count")
    st.write(count)
    total_co2=round(total_co2,2)
    
    # Create an empty dictionary to store the total carbon footprint for each category
    category_footprint = {}

    # Iterate through the transactions
    for transaction in transactions_data:
        # Get the category and carbon footprint of the current transaction
        category = transaction["category"]
        carbon_footprint = transaction["carbon_footprint"]
    
        # Check if the category already exists in the dictionary
        if category in category_footprint:
            # If it does, add the carbon footprint to the existing total
            category_footprint[category] += carbon_footprint
        else:
            # If it doesn't, add the category and carbon footprint to the dictionary
            category_footprint[category] = carbon_footprint

    # Sort the dictionary by carbon footprint in descending order
    category_footprint = {k: v for k, v in sorted(category_footprint.items(), key=lambda item: item[1], reverse=True)}

    # Create a pandas DataFrame from the top 5 categories with the highest carbon footprint
    if len(category_footprint)<5:
        top_5_categories = pd.DataFrame(list(category_footprint.items())[:len(category_footprint)], columns=["Category", "Total Carbon Footprint"])
    else:
        top_5_categories = pd.DataFrame(list(category_footprint.items())[:5], columns=["Category", "Total Carbon Footprint"])
    
    st.write(top_5_categories)
    
    # Sort transactions_data list by carbon_footprint in descending order
    #transactions_data.sort(key=lambda x: x["carbon_footprint"], reverse=True)

    # Display the top 5 transactions with the largest carbon footprints
    #st.write("Top 5 Transactions with Largest Carbon Footprints:")
    #for i in range(5):
     #   transaction = transactions_data[i]
      #  st.write("Description: ", transaction["description"])
       # st.write("Amount: ", transaction["amount"])
        #st.write("Carbon Footprint: ", transaction["carbon_footprint"])
        #st.write("Category: ", transaction["category"])
   
    #st.write("total co2: ")
    #st.write(total_co2)

    # Create a pandas DataFrame from the transaction data
    #transactions_df = pd.DataFrame(transactions_data[:5], columns=["description", "amount", "carbon_footprint", "category"])
    #st.write(transactions_df)
    
    # Generate a table of the top 5 transactions
    table = top_5_categories.to_html()
    #st.write(table)

    # me == my email address
    # you == recipient's email address
    me = "genifyco2@gmail.com"
    you = emailAddress

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Carbon Footprint Report"
    msg['From'] = me
    msg['To'] = you
    
    
    code=total_co2
    code2 = st.session_state.name
    code3 = table
    # Create the body of the message (a plain-text and an HTML version).
    text = "Hi!How are you?Here is your carbon footprint: " + str(total_co2) + " kg"
    html = """\
    <html>
      <head>
        <!-- NAME: 1 COLUMN -->
        <!--[if gte mso 15]>
        <xml>
            <o:OfficeDocumentSettings>
            <o:AllowPNG/>
            <o:PixelsPerInch>96</o:PixelsPerInch>
            </o:OfficeDocumentSettings>
        </xml>
        <![endif]-->
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Your Carbon Footprint</title>
      </head>
    <body>
        <!--*|IF:MC_PREVIEW_TEXT|*-->
        <!--[if !gte mso 9]><!----><span class="mcnPreviewText" style="display:none; font-size:0px; line-height:0px; max-height:0px; max-width:0px; opacity:0; overflow:hidden; visibility:hidden; mso-hide:all;">Carbon Footprint Report</span><!--<![endif]-->
        <!--*|END:IF|*-->
        <center>
            <table align="center" border="0" cellpadding="0" cellspacing="0" height="100%" width="100%" id="bodyTable">
                <tr>
                    <td align="center" valign="top" id="bodyCell">
                        <!-- BEGIN TEMPLATE // -->
                        <!--[if (gte mso 9)|(IE)]>
                        <table align="center" border="0" cellspacing="0" cellpadding="0" width="600" style="width:600px;">
                        <tr>
                        <td align="center" valign="top" width="600" style="width:600px;">
                        <![endif]-->
                        <table border="0" cellpadding="0" cellspacing="0" width="100%" class="templateContainer">
                            <tr>
                                <td valign="top" id="templatePreheader"></td>
                            </tr>
                            <tr>
                                <td valign="top" id="templateHeader"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnImageBlock" style="min-width:100%;">
    <tbody class="mcnImageBlockOuter">
            <tr>
                <td valign="top" style="padding:9px" class="mcnImageBlockInner">
                    <table align="left" width="100%" border="0" cellpadding="0" cellspacing="0" class="mcnImageContentContainer" style="min-width:100%;">
                        <tbody><tr>
                            <td class="mcnImageContent" valign="top" style="padding-right: 9px; padding-left: 9px; padding-top: 0; padding-bottom: 0; text-align:center;">
                                
                                    
                                        <img align="center" alt="" src="https://mcusercontent.com/04342189852af59dbd7e679fa/images/4f669805-fedf-2e7c-8926-950ce997f55a.png" width="564" style="max-width:1920px; padding-bottom: 0; display: inline !important; vertical-align: bottom;" class="mcnImage">
                                    
                                
                            </td>
                        </tr>
                    </tbody></table>
                </td>
            </tr>
    </tbody>
</table></td>
                            </tr>
                            <tr>
                                <td valign="top" id="templateBody"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextBlock" style="min-width:100%;">
    <tbody class="mcnTextBlockOuter">
        <tr>
            <td valign="top" class="mcnTextBlockInner" style="padding-top:9px;">
                <!--[if mso]>
                <table align="left" border="0" cellspacing="0" cellpadding="0" width="100%" style="width:100%;">
                <tr>
                <![endif]-->
                
                <!--[if mso]>
                <td valign="top" width="600" style="width:600px;">
                <![endif]-->
                <table align="left" border="0" cellpadding="0" cellspacing="0" style="max-width:100%; min-width:100%;" width="100%" class="mcnTextContentContainer">
                    <tbody><tr>
                        
                        <td valign="top" class="mcnTextContent" style="padding-top:0; padding-right:18px; padding-bottom:9px; padding-left:18px;">
                        
                            <h1 class="mc-toc-title" style="text-align: center;"><span style="color:#495639"><span style="font-size:22px">Results are in!</span></span></h1>

<div style="text-align: center;">{code2}, your total emissions for the past 3 months&nbsp;have amounted to<br>
<strong>{code}</strong><br>
<br>
See your consumption per category<br>
<div style="text-align: center;"><span style="color:#495639">Here is a list of your top 5 transactions that had the highest carbon footprints<br>
    <center>
        {code3}<br>
    </center><br>
<strong>________________</strong><br>
<br>
Notice, in 2022 the average person's emission for 3 months was<br>
<strong>900 kg</strong></div>

                        </td>
                    </tr>
                </tbody></table>
                <!--[if mso]>
                </td>
                <![endif]-->
                
                <!--[if mso]>
                </tr>
                </table>
                <![endif]-->
            </td>
        </tr>
    </tbody>
</table><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnImageBlock" style="min-width:100%;">
    <tbody class="mcnImageBlockOuter">
            <tr>
                <td valign="top" style="padding:9px" class="mcnImageBlockInner">
                    <table align="left" width="100%" border="0" cellpadding="0" cellspacing="0" class="mcnImageContentContainer" style="min-width:100%;">
                        <tbody><tr>
                            <td class="mcnImageContent" valign="top" style="padding-right: 9px; padding-left: 9px; padding-top: 0; padding-bottom: 0; text-align:center;">
                                
                                    
                                        <img align="center" alt="" src="https://mcusercontent.com/04342189852af59dbd7e679fa/images/a0bc9dc8-7fbf-b99a-36df-808f578fc75d.png" width="90.24" style="max-width:376px; padding-bottom: 0; display: inline !important; vertical-align: bottom;" class="mcnImage">
                                    
                                
                            </td>
                        </tr>
                    </tbody></table>
                </td>
            </tr>
    </tbody>
</table></td>
                            </tr>
                            <tr>
                                <td valign="top" id="templateFooter"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnDividerBlock" style="min-width:100%;">
    <tbody class="mcnDividerBlockOuter">
        <tr>
            <td class="mcnDividerBlockInner" style="min-width: 100%; padding: 10px 18px 25px;">
                <table class="mcnDividerContent" border="0" cellpadding="0" cellspacing="0" width="100%" style="min-width: 100%;border-top: 2px solid #EEEEEE;">
                    <tbody><tr>
                        <td>
                            <span></span>
                        </td>
                    </tr>
                </tbody></table>
<!--            
                <td class="mcnDividerBlockInner" style="padding: 18px;">
                <hr class="mcnDividerContent" style="border-bottom-color:none; border-left-color:none; border-right-color:none; border-bottom-width:0; border-left-width:0; border-right-width:0; margin-top:0; margin-right:0; margin-bottom:0; margin-left:0;" />
-->
            </td>
        </tr>
    </tbody>
</table><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextBlock" style="min-width:100%;">
    <tbody class="mcnTextBlockOuter">
        <tr>
            <td valign="top" class="mcnTextBlockInner" style="padding-top:9px;">
                <!--[if mso]>
                <table align="left" border="0" cellspacing="0" cellpadding="0" width="100%" style="width:100%;">
                <tr>
                <![endif]-->
                
                <!--[if mso]>
                <td valign="top" width="600" style="width:600px;">
                <![endif]-->
                <table align="left" border="0" cellpadding="0" cellspacing="0" style="max-width:100%; min-width:100%;" width="100%" class="mcnTextContentContainer">
                    <tbody><tr>
                        
                        <td valign="top" class="mcnTextContent" style="padding-top:0; padding-right:18px; padding-bottom:9px; padding-left:18px;">
                        
                            <em>Copyright © 2022 Genify.ai, All rights reserved.</em><br>
&nbsp;
                        </td>
                    </tr>
                </tbody></table>
                <!--[if mso]>
                </td>
                <![endif]-->
                
                <!--[if mso]>
                </tr>
                </table>
                <![endif]-->
            </td>
        </tr>
    </tbody>
</table></td>
                            </tr>
                        </table>
                        <!--[if (gte mso 9)|(IE)]>
                        </td>
                        </tr>
                        </table>
                        <![endif]-->
                        <!-- // END TEMPLATE -->
                    </td>
                </tr>
            </table>
        </center>
    <script type="text/javascript"  src="/Tgl4v/5/Ch/orBD/UswUezFt/3aQ5JLrD/LloSAg/eGUZQF/4FAmw"></script></body>

    </html>
    """.format(code=code, code2=code2, code3=code3)

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    part3 = MIMEText(table, 'html')
    
    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)
    #Add the table to the email body
    #msg.attach(part3)
    
    # Send the message via local SMTP server.
    mail = smtplib.SMTP('smtp.gmail.com', 587)

    mail.ehlo()

    mail.starttls()

    mail.login('genifyco2@gmail.com', 'aalnjsoddytheyan')
    mail.sendmail(me, you, msg.as_string())
    mail.quit()

    st.write("Your carbon footprint has been emailed to you! Make sure to check your spam.")
