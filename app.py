#1. Importing Libraries

import numpy as np
import streamlit as st
import pickle
from datetime import date

#2.Page Configuration

st.set_page_config(
    page_title="Industrial Copper Modelling",
    page_icon="ICM.jpg",
    layout="wide"
)
st.markdown(f'### <html><body><h1 style="font-family:Google Sans; font-size:40px"> Industrial Copper Modelling</h1></body></html>', unsafe_allow_html=True)
column1,column2=st.columns(2)
column3,column4=st.columns(2)

with column1:
    st.image('about2.jpg')
    st.image('about3.jpg')

with column2:
    st.image('about4.jpg')
    st.image('about5.jpg')


#3.Main Page

st.markdown(f'### <html><body><h1 style="font-family:Google Sans; font-size:40px"> Project Outcome:</h1></body></html>', unsafe_allow_html=True)
            
class options:

    country_values = [25.0, 26.0, 27.0, 28.0, 30.0, 32.0, 38.0, 39.0, 40.0, 77.0, 
                    78.0, 79.0, 80.0, 84.0, 89.0, 107.0, 113.0]

    status_values = ['Won', 'Lost', 'Draft', 'To be approved', 'Not lost for AM',
                    'Wonderful', 'Revised', 'Offered', 'Offerable']
    status_dict = {'Lost':0, 'Won':1, 'Draft':2, 'To be approved':3, 'Not lost for AM':4,
                'Wonderful':5, 'Revised':6, 'Offered':7, 'Offerable':8}

    item_type_values = ['W', 'WI', 'S', 'PL', 'IPL', 'SLAWR', 'Others']
    item_type_dict = {'W':5.0, 'WI':6.0, 'S':3.0, 'Others':1.0, 'PL':2.0, 'IPL':0.0, 'SLAWR':4.0}

    application_values = [2.0, 3.0, 4.0, 5.0, 10.0, 15.0, 19.0, 20.0, 22.0, 25.0, 26.0, 27.0, 28.0, 29.0, 38.0, 39.0, 40.0, 41.0, 42.0, 56.0, 58.0, 59.0, 65.0, 66.0, 67.0, 68.0, 69.0, 70.0, 79.0, 99.0]

    product_ref_values = [611728, 611733, 611993, 628112, 628117, 628377, 640400, 
                        640405, 640665, 164141591, 164336407, 164337175, 929423819, 
                        1282007633, 1332077137, 1665572032, 1665572374, 1665584320, 
                        1665584642, 1665584662, 1668701376, 1668701698, 1668701718, 
                        1668701725, 1670798778, 1671863738, 1671876026, 1690738206, 
                        1690738219, 1693867550, 1693867563, 1721130331, 1722207579]

# Get input data from users both regression and classification methods

class prediction:

    def regression():

        with st.form('Regression'):
            col1,col2,col3 = st.columns([0.5,0.1,0.5])

            with col1:
                quantity = st.text_input(label='Quantity Tons (Min: 0.00001 & Max: 1000000000)')
                country = st.selectbox(label='Country', options=options.country_values)
                item_type = st.selectbox(label='Item Type', options=options.item_type_values)
                item_date = st.date_input(label='Item Date', min_value=date(2020,7,1), 
                                        max_value=date(2021,5,31), value=date(2020,7,1))
                thickness = st.number_input(label='Thickness', min_value=0.1, max_value=2500000.0, value=1.0)
                
            
            with col3:
                status = st.selectbox(label='Status', options=options.status_values)
                application = st.selectbox(label='Application', options=options.application_values)
                width = st.number_input(label='Width', min_value=1.0, max_value=2990000.0, value=1.0)
                delivery_date = st.date_input(label='Delivery Date', min_value=date(2020,8,1), 
                                            max_value=date(2022,2,28), value=date(2020,8,1))
                product_ref = st.selectbox(label='Product Ref', options=options.product_ref_values)
                st.write('')
                st.write('')
                button = st.form_submit_button(label='SUBMIT')

        # give information to users
        col1,col2 = st.columns([0.65,0.35])
        with col2:
            st.caption(body='*Min and Max values are reference only')
               
        # user entered the all input values and click the button
        if button:
            # load the regression pickle model
            with open(r'regression_model.pkl', 'rb') as f:
                model = pickle.load(f)
            
            # make array for all user input values in required order for model prediction
            user_data = np.array([[
                                country, 
                                options.status_dict[status], 
                                options.item_type_dict[item_type], 
                                application, 
                                width, 
                                product_ref, 
                                np.log(float(quantity)), 
                                np.log(float(thickness)),
                                item_date.day, item_date.month, item_date.year,
                                delivery_date.day, delivery_date.month, delivery_date.year
                                ]])
            
            # model predict the selling price based on user input
            y_pred = model.predict(user_data)
            # inverse transformation for log transformation data
            selling_price = np.exp(y_pred[0])
            # round the value with 2 decimal point (Eg: 1.35678 to 1.36)
            selling_price = round(selling_price, 2)
            return selling_price


    def classification():

        with st.form('Classification'):
            col1,col2,col3 = st.columns([0.5,0.1,0.5])

            with col1:            
                quantity = st.text_input(label='Quantity Tons (Min: 0.00001 & Max: 1000000000)')
                country = st.selectbox(label='Country', options=options.country_values)
                item_type = st.selectbox(label='Item Type', options=options.item_type_values)
                item_date = st.date_input(label='Item Date', min_value=date(2020,7,1), 
                                        max_value=date(2021,5,31), value=date(2020,7,1))
                thickness = st.number_input(label='Thickness', min_value=0.1, max_value=2500000.0, value=1.0)
                

            with col3:
                selling_price = st.text_input(label='Selling Price (Min: 0.1 & Max: 100001000)')
                application = st.selectbox(label='Application', options=options.application_values)
                width = st.number_input(label='Width', min_value=1.0, max_value=2990000.0, value=1.0)
                delivery_date = st.date_input(label='Delivery Date', min_value=date(2020,8,1), 
                                            max_value=date(2022,2,28), value=date(2020,8,1))
                product_ref = st.selectbox(label='Product Ref', options=options.product_ref_values)
                st.write('')
                st.write('')
                button = st.form_submit_button(label='SUBMIT')
      
        # give information to users
        col1,col2 = st.columns([0.65,0.35])
        with col2:
            st.caption(body='*Min and Max values are reference only')

        # user entered the all input values and click the button
        if button:        
        # load the classification pickle model
            with open(r'classification_model.pkl', 'rb') as f:
                model = pickle.load(f)
            
        # make array for all user input values in required order for model prediction
            user_data = np.array([[
                                country, 
                                options.item_type_dict[item_type], 
                                application, 
                                width, 
                                product_ref, 
                                np.log(float(quantity)), 
                                np.log(float(thickness)),
                                np.log(float(selling_price)),
                               item_date.day, item_date.month, item_date.year,
                                delivery_date.day, delivery_date.month, delivery_date.year]])
            
            # model predict the status based on user input
            y_pred = model.predict(user_data)
            # we get the single output in list, so we access the output using index method
            status = y_pred[0]
            return status  

# Creating Tab for Each Model
tab1, tab2 = st.tabs(['PREDICT SELLING PRICE', 'PREDICT STATUS'])

with tab1:

    try:
        selling_price = prediction.regression()

        if selling_price:
            st.markdown(f'### <html><body><h1 style="font-family:Neutro; font-size:40px"> Predicted Price={selling_price} </h1></body></html>', unsafe_allow_html=True)
            st.balloons()

    except ValueError:
        col1,col2,col3 = st.columns([0.26,0.55,0.26])
        with col2:
            st.warning('##### Quantity Tons / Customer ID is empty')

with tab2:

    try:
        status = prediction.classification()
        if status == 1:
            hide_streamlit_style = """ <html><body><h1 style="font-family:Google Sans; font-size:40px"> Predicted Status=Won </h1></body></html>"""
            st.markdown(hide_streamlit_style, unsafe_allow_html=True)
            st.balloons()
            

        elif status == 0:
            hide_streamlit_style = """ <html><body><h1 style="font-family:Google Sans; font-size:40px"> Predicted Status=Loss </h1></body></html>"""
            st.markdown(hide_streamlit_style, unsafe_allow_html=True)
            st.snow()

    except ValueError:
        col1,col2,col3 = st.columns([0.15,0.70,0.15])
        with col2:
            st.warning('##### Quantity Tons / Customer ID / Selling Price is empty')


#4.About My Project...................
Col5,Col6=st.columns(2)

with Col5:

    hide_streamlit_style = """ <html> <body>
    <h1 style="font-family:Google Sans; color:blue;font-size:40px"> About this Project </h1>
    <p style="font-family:Google Sans; font-size:20px">
    <b>Project_Title</b>: Industrial Copper Modeling <br>
    <b>Aim</b>: The main aim of this project is to create a user friendly streamlit application to predict the Selling price  and Status   in Industrial Copper Market using Supervised machine learning model
    <b>Technologies_Used</b> :Python scripting, Data Preprocessing,EDA, Streamlit, Machine Learning<br>
    <b>Dataset: </b><a href='https://docs.google.com/spreadsheets/d/18eR6DBe5TMWU9FnIewaGtsepDbV4BOyr/edit?usp=sharing&ouid=104970222914596366601&rtpof=true&sd=true'>Link</a> <br>
    <b>Domain </b> : Manufacturing<br>
    <b>Author</b> : M.KOBALAN <br>
    <b>Linkedin</b> <a href='https://www.linkedin.com/in/kobalan-m-106267227/'>Link</a>
    </p>
    </body>  </html>  """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

with Col6:
    st.image('about.jpg')