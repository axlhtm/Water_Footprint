# =============================================================================
# WATER FOOTPRINT FOR PERSONAL USE - HOME
# =============================================================================
# Import Python Libraries
from faker import Faker
from urllib.error import URLError
import altair as alt
import datetime
import geopy.geocoders
import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st
import sqlalchemy as sa

DB_USERNAME = "u106038152_reservoair"
DB_TOKEN = "Delft211295"
DB_HOST = "154.41.240.52"
DB_PORT = 3306
DB_NAME = "u106038152_reservoair"

# =============================================================================
# WATER FOOTPRINT FOR PERSONAL USE - HOME PAGE
# =============================================================================
# Parameter - Home Page
st.set_page_config(layout="wide")
# Def Function - Home Page
def wf_p_home():
    import streamlit as st
    cols = st.columns(2, gap="small")  # Creates two columns
    with cols[0]:
        st.write("### Hi there, welcome! 💦")
        st.write("# Water Footprint for Personal Use!")
        st.markdown(
            """
            ReservoAir's web application is a one-stop shop for understanding your daily water footprint.  
            This user-friendly tool combines a water footprint calculator for personal use, interactive mapping features, and a comprehensive overview section.  

            **👈 Unleash the power of ReservoAir** by selecting a feature from the dropdown menu on your left!

            ### Overview of This Web App
            * **Water Footprint Calculator**
                * Calculate your personal water footprint based on daily activities.
                * Gain a clearer understanding of your water consumption patterns.
                * Identify areas for potential water conservation efforts.
            * **Interactive Water Usage Maps**
                * Visualize regional water usage patterns.
                * Explore how factors like climate and infrastructure influence water use.
                * Discover potential conservation initiatives in your community.
            * **Comprehensive Water Footprint Overview**
                * Learn about the concept of water footprint and its global impact.
                * Discover different water footprint models and their applications.
                * Explore ways to reduce your water footprint and contribute to a more sustainable future.

                
            ##### Served with 💖 by

            """
        )
        st.image("https://reservoair.com/wp-content/uploads/2023/06/logo-HD-RESERVO-AIR-1.png", width=125)

    with cols[1]:
        st.image("C:/Users/axelh/Downloads/An Indian Child in a Pool.jpg", width=650)

# =============================================================================
# WATER FOOTPRINT FOR PERSONAL USE - CALCULATOR PAGE
# =============================================================================
# Parameter - Calculator Page
# Def Function - Calculator Page
def wf_p_calculator():
    # =============================================================================
    # PRE-SECTION: INITIALIZE CONNECTION TO SQL
    # =============================================================================
    # 0.1. Database Connection Details
    engine = sa.create_engine(f"mysql+pymysql://{DB_USERNAME}:{DB_TOKEN}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    # 0.2. Define Table Schema
    table_name = 'wf_p_calculator_raw_data'
    schema = {
        # Record data from Personal Data
        "full_name"    : sa.Column(sa.String(200)),
        "email"        : sa.Column(sa.String(200)),
        "birth_date"   : sa.Column(sa.Date),
        "gender"       : sa.Column(sa.String(200)),   
        "education"    : sa.Column(sa.String(200)),
        "occupation"   : sa.Column(sa.String(200)),
        "city"         : sa.Column(sa.String(200)),
        "subdistrict"  : sa.Column(sa.String(200)),
        "water_source" : sa.Column(sa.String(200)),

        # Record data from Hygiene Consumption Data
        "shower"              : sa.Column(sa.Float),
        "shower_equipment"    : sa.Column(sa.String(200)),
        "shw_dipper_type"     : sa.Column(sa.String(200)),
        "shw_dipper_cal"      : sa.Column(sa.Float),
        "shw_shower_cal"      : sa.Column(sa.Float),
        "defeciate"           : sa.Column(sa.Float),
        "urinate"             : sa.Column(sa.Float),
        "toilet_equipment"    : sa.Column(sa.String(200)),
        "toil_def_button_cal" : sa.Column(sa.Float),
        "toil_uri_button_cal" : sa.Column(sa.Float),
        "toil_dipper_type"    : sa.Column(sa.String(200)),
        "toil_def_dipper_cal" : sa.Column(sa.Float),
        "toil_uri_dipper_cal" : sa.Column(sa.Float),

        # Record data from Food Consumption Data
        "water_glass"     : sa.Column(sa.Float),
        "cooked_rice"     : sa.Column(sa.Float),
        "cooked_rice_cal" : sa.Column(sa.String(200)),

        # Domestic Consumption Data
        "washed_dish"            : sa.Column(sa.Float),
        "washed_dish_cal"        : sa.Column(sa.Float),
        "mop_floor"              : sa.Column(sa.Float),
        "mop_floor_cal"          : sa.Column(sa.Float),
        "washed_cloth"           : sa.Column(sa.Float),
        "washed_cloth_equipment" : sa.Column(sa.String(200)),
        "washed_cloth_cal"       : sa.Column(sa.Float),
        "vehicle_bike"           : sa.Column(sa.Float),
        "vehicle_bike_cal"       : sa.Column(sa.Float),
        "vehicle_bike_shw"       : sa.Column(sa.Float),
        "vehicle_car"            : sa.Column(sa.Float),
        "vehicle_car_cal"        : sa.Column(sa.Float),
        "vehicle_car_shw"        : sa.Column(sa.Float),
        "gardening"              : sa.Column(sa.Float),
        "gardening_cal"          : sa.Column(sa.Float),      
    }
    if "data" not in st.session_state:
        st.session_state.data = []
    
    # =============================================================================
    # PRE-SECTION: PAGE LAYOUT
    # =============================================================================
    st.markdown(f"# {list(page_names_to_funcs.keys())[1]} 🔢")
    col1, col2 = st.columns([3, 2]) 

    # =============================================================================
    # SECTION I: DATA SUBMISSION AND STORAGE - PERSONAL DATA
    # =============================================================================
    
    with col1: 
            
        # I.1. Get User Input
        with st.expander("Section I - Personal Data", expanded=True):
            st.subheader("Section I - Personal Data 🙋‍♂️🙋‍♀️", divider='blue')
            full_name    = st.text_input("What is your full name?")
            email        = st.text_input("What is your email address?")
            birth_date   = st.date_input("When is your birthday?", datetime.date(2000, 1, 1))
            gender       = st.selectbox("What is your gender?", ("Male", "Female"))
            education    = st.selectbox("What is your latest education?", ("Elementary School", "High School", "Undergraduate", "Post Graduate", "Doctoral"), index=None)
            occupation   = st.selectbox("What is your occupation?",(
                "Teacher", "Student", "Entrepreneur", "Doctor", "Police Officer", "Nurse", "Engineer", "Farmer", "Retail Worker", "Factory Worker",
                "Government Official", "Accountant", "Lawyer", "IT Specialist", "Marketing Specialist", "Customer Service Representative", "Web Developer",
                "Graphic Designer", "Chef", "Waiter/Waitress", "Driver", "Construction Worker", "Barista", "Hairdresser/Barber", "Security Guard", "Mechanic", "Housekeeper",
                "Telemarketer", "Social Media Manager", "Content Writer", "Translator", "Travel Agent"), index=None)  
            city         = st.selectbox("What city do you live in?", ("Kota Bandung", "Kota Cimahi", "Kabupaten Bandung Barat", "Kabupaten Bandung"), index=None)
            subdistrict  = st.selectbox("What sub-district do you live in?",(
                "Kecamatan Bandung Kulon", "Kecamatan Babakan Ciparay", "Kecamatan Bojongloa Kidul", "Kecamatan Bojongloa Kaler", "Kecamatan Astanaanyar", "Kecamatan Regol", "Kecamatan Lengkong", "Kecamatan Bandung Kidul", "Kecamatan Buah Batu", "Kecamatan Rancasari", 
                "Kecamatan Gedebage", "Kecamatan Cibiru", "Kecamatan Panyileukan", "Kecamatan Ujungberung", "Kecamatan Cinambo", "Kecamatan Arcamanik", "Kecamatan Antapani", "Kecamatan Mandalajati", "Kecamatan Kiaracondong", "Kecamatan Batununggal",
                "Kecamatan Sumur Bandung", "Kecamatan Andir", "Kecamatan Cicendo", "Kecamatan Bandung Wetan", "Kecamatan Cibeunying Kidul", "Kecamatan Cibeunying Kaler", "Kecamatan Coblong", "Kecamatan Sukajadi", "Kecamatan Sukasari", "Kecamatan Cidadap"), index=None)
            water_source = st.selectbox("What is your water source?", ("Water Utility", "Ground Water"), index=None)

        # ==============================================================================================
        # SECTION II: DATA SUBMISSION AND STORAGE - PERSONAL WATER USAGE FOR HYGIENE CONSUMPTION PATTERN
        # ==============================================================================================
        # II.1. Get User Input
        with st.expander("Section II - Personal Water Usage for Hygiene Consumption Pattern"):
            st.subheader("Section II - Personal Water Usage for Hygiene Consumption Pattern 💦 ", divider='blue')
            shower               = st.slider("How many times do you shower in a day?", 0, 3, 2)
            shower_equipment     = st.selectbox("What type of shower equipment do you use?", ("Dipper", "Shower"), index=0)
            if shower_equipment  == "Dipper": 
                shw_dipper_type     = st.selectbox("What type of dipper do you use for shower?", ("Small Dipper (1.3 L)", "Medium Dipper (1.7 L)", "Large Dipper (2.4L)"), index=1)
                shw_dipper_cal      = st.slider("How many scoops of dipper do you need for one shower?", 10,30,20)
                shw_shower_cal      = 0
            else:
                shw_dipper_type     = "Large Dipper (2.4L)"
                shw_dipper_cal      = 0 
                shw_shower_cal      = st.slider("How long is your typical shower? (Minutes)", 0, 60, 15)
            defeciate            = st.slider("How many times do you defecate in a day?", 0, 5, 1)
            urinate              = st.slider("How many times do you urinate in a day?", 0, 10, 5)
            toilet_equipment     = st.selectbox("How do you flush the toilet after defecating and urinating?", ("Toilet Button", "Dipper"), index=0)
            if toilet_equipment  == "Toilet Button":
                toil_def_button_cal = st.slider("How many times do you flush after defecating?", 0, 5, 1)
                toil_uri_button_cal = st.slider("How many times do you flush after urinating?", 0, 5, 1)
                toil_dipper_type    = "Large Dipper (2.4L)"
                toil_def_dipper_cal = 0
                toil_uri_dipper_cal = 0
            else: 
                toil_dipper_type    = st.selectbox("What type of dipper do you use for toilet?", ("Small Dipper (1.3 L)", "Medium Dipper (1.7 L)", "Large Dipper (2.4L)"), index=1)
                toil_def_dipper_cal = st.slider("How many scoops of dipper do you sue after defecating?", 0, 5, 1)
                toil_uri_dipper_cal = st.slider("How many scoops of dipper do you sue after urinating?", 0, 5, 1)
                toil_def_button_cal = 0
                toil_uri_button_cal = 0
        
        # ============================================================================================
        # SECTION III: DATA SUBMISSION AND STORAGE - PERSONAL WATER USAGE FOR FOOD CONSUMPTION PATTERN
        # ============================================================================================
        # III.1. Get User Input
        with st.expander("Section III - Personal Water Usage for Food Consumption Pattern"):
            st.subheader("Section III - Personal Water Usage for Food Consumption Pattern 🥙 ", divider='blue')
            water_glass      = st.slider("How many glasses of water do you drink in one day? One glass is equal to 250ml of water.", 0, 25, 10)
            cooked_rice      = st.slider("How many times does your family cook rice for one day?", 0, 5, 2)
            cooked_rice_cal  = st.radio("How many liters of rice are cooked in one rice cooker? 4 Cup is equal to 1 liter.", ["1 Liter", "2 Liter", "3 Liter", "4 Liter", "5 Liter"])

        # ===============================================================================================
        # SECTION IV: DATA SUBMISSION AND STORAGE - PERSONAL WATER USAGE FOR DOMESTIC CONSUMPTION PATTERN
        # ===============================================================================================
        # IV.1. Get User Input
        with st.expander("Section IV - Personal Water Usage for Domestic Consumption Pattern"):
            st.subheader("Section IV - Personal Water Usage for Domestic Consumption Pattern 🍽️", divider='blue')
            washed_dish            = st.slider("How many times do you wash your dish in a day?", 0, 5, 2)
            washed_dish_cal        = st.slider("How long you wash your dish? (Minutes)", 0, 30, 15)
            mop_floor              = st.slider("How many times do you mop the floor in one week?", 0, 7, 4)
            mop_floor_cal          = st.slider("How many buckets of water do you use to mop the floor once?", 0, 5, 2)
            washed_cloth           = st.slider("How many times do you wash your clothes in one week?", 0, 7, 2)
            washed_cloth_equipment = st.selectbox("What tools do you use to wash clothes?", ("Washing Machine", "Hand-Wash"), index=0)
            washed_cloth_cal       = st.slider("How many times do you rinse clothes when washing?", 0, 5, 2)
            vehicle_bike           = st.slider("How many motorcycles do you have?", 0, 5, 2)
            vehicle_bike_cal       = st.radio("Do you wash your motorcycles at home?", ["Yes", "No"])
            vehicle_bike_shw       = st.slider("How often do you wash your bike in a week?", 0, 7, 2)
            vehicle_car            = st.slider("How many cars do you have?", 0, 5, 2)
            vehicle_car_cal        = st.radio("Do you wash your car at home?", ["Yes", "No"])
            vehicle_car_shw        = st.slider("How often do you wash your car in a week?", 0, 7, 2)
            gardening              = st.slider("How many times do you water your plants in one day?", 0, 5, 3)
            gardening_cal          = st.slider("How long you water your plant? (Minutes)", 0, 30, 15)

        # Button to submit the form
        if st.button("Submit and Analyze", type="primary"):
        # Check if all fields are filled
            if full_name and email and birth_date and gender and education and occupation and city and subdistrict and water_source:
                # Add new data as dictionary to the list
                wf_p_calculator_raw_data = {
                # Record data from Personal Data
                "full_name"    : full_name, 
                "email"        : email,
                "birth_date"   : birth_date,
                "gender"       : gender,    
                "education"    : education,  
                "occupation"   : occupation,
                "city"         : city,
                "subdistrict"  : subdistrict,
                "water_source" : water_source,

                # Record data from Hygiene Consumption Data
                "shower"              : shower, 
                "shower_equipment"    : shower_equipment,
                "shw_dipper_type"     : shw_dipper_type,
                "shw_dipper_cal"      : shw_dipper_cal,
                "shw_shower_cal"      : shw_shower_cal, 
                "defeciate"           : defeciate,
                "urinate"             : urinate,
                "toilet_equipment"    : toilet_equipment,
                "toil_def_button_cal" : toil_def_button_cal,
                "toil_uri_button_cal" : toil_uri_button_cal,
                "toil_dipper_type"    : toil_dipper_type,
                "toil_def_dipper_cal" : toil_def_dipper_cal,
                "toil_uri_dipper_cal" : toil_uri_dipper_cal,

                # Record data from Food Consumption Data
                "water_glass"     : water_glass, 
                "cooked_rice"     : cooked_rice,
                "cooked_rice_cal" : cooked_rice_cal,

                # Domestic Consumption Data
                "washed_dish"            : washed_dish,
                "washed_dish_cal"        : washed_dish_cal,
                "mop_floor"              : mop_floor,
                "mop_floor_cal"          : mop_floor_cal,
                "washed_cloth"           : washed_cloth,
                "washed_cloth_equipment" : washed_cloth_equipment,
                "washed_cloth_cal"       : washed_cloth_cal,
                "vehicle_bike"           : vehicle_bike,
                "vehicle_bike_cal"       : vehicle_bike_cal, 
                "vehicle_bike_shw"       : vehicle_bike_shw,
                "vehicle_car"            : vehicle_car, 
                "vehicle_car_cal"        : vehicle_car_cal,
                "vehicle_car_shw"        : vehicle_car_shw,
                "gardening"              : gardening,
                "gardening_cal"          : gardening_cal          
                }
                st.session_state.data.append(wf_p_calculator_raw_data)
                st.info("Data submitted successfully!")
            else:
                st.error("Please fill in all required fields.")
        

    with col2:


        with st.container(border=True): 
            st.markdown("#### Have You Calculated Your Daily Water Usage?")
            col3, col4 = st.columns([3,2])
            with col3: 
                email_sliced = st.text_input("Already filled the data?", placeholder="Enter your email address", label_visibility="collapsed")
                def df_wf_p_pros_sliced(): 
                    global sliced_df_wf_p_pros, sliced_wf_hyg, sliced_wf_food, sliced_wf_dom, sliced_wf_total, max_wf_value, max_wf_consumption_source, sliced_wf_name, df_wf_p_pros, df_wf_p_pros_avg_dom, df_wf_p_pros_avg_food, df_wf_p_pros_avg_hyg, df_wf_p_pros_avg_total
                    engine_pros      =  sa.create_engine(f"mysql+pymysql://{DB_USERNAME}:{DB_TOKEN}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
                    table_name_pros  = 'wf_p_calculator_pros_data'
                    # I.2. Define the SQL Query to Retrieve Data
                    query_pros       = f"SELECT * FROM {table_name_pros}"
                    # I.3. Read Data from SQL Table into a DataFrame and Drop Duplicates by Email
                    df_wf_p_pros        = pd.read_sql(query_pros, engine_pros)
                    sliced_df_wf_p_pros = df_wf_p_pros.loc[df_wf_p_pros['email'] == email_sliced]
                    sliced_df_wf_p_pros = sliced_df_wf_p_pros.drop_duplicates(subset='email')
                    sliced_df_wf_p_pros = sliced_df_wf_p_pros.reset_index(drop=True)
                    # I.4. Calculate Average Water Usage
                    df_wf_p_pros            = df_wf_p_pros.drop_duplicates(subset='email')
                    df_wf_p_pros_avg_hyg   = float(df_wf_p_pros['wf_hyg'].mean())
                    df_wf_p_pros_avg_food  = float(df_wf_p_pros['wf_food'].mean())
                    df_wf_p_pros_avg_dom   = float(df_wf_p_pros['wf_dom'].mean())
                    df_wf_p_pros_avg_total = float(df_wf_p_pros['wf_total'].mean())
                    # I.5. Detail Sliced Data
                    sliced_wf_name      = str(sliced_df_wf_p_pros.loc[0,'full_name'])
                    sliced_wf_hyg       = float(sliced_df_wf_p_pros.loc[0,'wf_hyg'])
                    sliced_wf_food      = float(sliced_df_wf_p_pros.loc[0,'wf_food'])
                    sliced_wf_dom       = float(sliced_df_wf_p_pros.loc[0,'wf_dom'])
                    sliced_wf_total     = float(sliced_df_wf_p_pros.loc[0,'wf_total'])
                    max_wf_value = max(sliced_wf_hyg, sliced_wf_food, sliced_wf_dom )
                    if max_wf_value == sliced_wf_hyg:
                        max_wf_consumption_source = "Hygiene Consumption"
                    elif max_wf_value == sliced_wf_food:
                        max_wf_consumption_source = "Food Consumption"
                    else:
                        max_wf_consumption_source = "Domestic Consumption"
                
            with col4:
                search_button = st.button("Find Your Data 💧", type="primary", use_container_width=True)

            if search_button:
                df_wf_p_pros_sliced()

                with st.container(border=True):
                    st.markdown("##### This is Your Water Usage Analysis")
                    col1, col2 = st.columns(2) 

                    if sliced_wf_total > df_wf_p_pros_avg_total:
                        col1.metric("Total Daily Usage", f"{sliced_wf_total} Liter / Day", f"{round(sliced_wf_total - df_wf_p_pros_avg_total),1} Liter above Average", delta_color="inverse")
                    else:
                        col1.metric("Total Daily Usage", f"{sliced_wf_total} Liter / Day", f"{round(sliced_wf_total - df_wf_p_pros_avg_total),1} Liter below Average")

                    col1.metric("Main Consumption Source", f"{round(max_wf_value/sliced_wf_total*100,1)} %", f"from {max_wf_consumption_source}", delta_color="off")   

                    if sliced_wf_hyg > df_wf_p_pros_avg_hyg:  
                        col2.metric("Daily Usage for Hygiene Consuption", f"{sliced_wf_hyg} Liter / Day", f"{round(sliced_wf_hyg - df_wf_p_pros_avg_hyg),1} Liter above Average", delta_color="inverse")
                    else: 
                        col2.metric("Daily Usage for Hygiene Consuption", f"{sliced_wf_hyg} Liter / Day", f"{round(sliced_wf_hyg - df_wf_p_pros_avg_hyg),1} Liter below Average")
                    
                    if sliced_wf_food > df_wf_p_pros_avg_food: 
                        col2.metric("Daily Usage for Food Consumption", f"{sliced_wf_food} Liter / Day", f"{round(sliced_wf_food - df_wf_p_pros_avg_food),1} Liter above Average", delta_color="inverse")
                    else:
                        col2.metric("Daily Usage for Food Consumption", f"{sliced_wf_food} Liter / Day", f"{round(sliced_wf_food - df_wf_p_pros_avg_food),1} Liter below Average")

                    if sliced_wf_dom > df_wf_p_pros_avg_dom: 
                        col2.metric("Daily Usage for Domestic Consumption", f"{sliced_wf_dom} Liter / Day", f"{round(sliced_wf_dom - df_wf_p_pros_avg_dom),1} Liter above Average", delta_color="inverse")
                    else: 
                        col2.metric("Daily Usage for Domestic Consumption", f"{sliced_wf_dom} Liter / Day", f"{round(sliced_wf_dom - df_wf_p_pros_avg_dom),1} Liter below Average")


        with st.container(border=True): 
            st.markdown("#### About Our Web-App")
            st.markdown('''
                        This is a tool to calculate your daily water usage based on your consumption pattern.
                        There are 4 sections that will be analyzed, which are: 
                        * Personal Data Section
                        * Hygiene Consumption Pattern Section
                        * Food Consumption Pattern Section
                        * Domestic Consumption Pattern Section

                        #### Disclaimer
                        All data will be stored in ReservoAir's database, all personal data will be classified. Scientific based research is used as mean of direct water usage calculation method.
                        ''')
    # Convert list to DataFrame and display
    if st.session_state.data:
        df = pd.DataFrame(st.session_state.data)
        #st.dataframe(df)
        df.to_sql(table_name, engine, index=False, if_exists='append') 

        # =============================================================================
        # WATER FOOTPRINT FOR PERSONAL USE - PROCESSING DATA
        # =============================================================================
        def wf_p_pros_func():
            global df_wf_p_pros
            
            # =============================================================================
            # SECTION I. Import Dataframe from MySQL Database
            # =============================================================================
            # I.1. Database Connection Details
            engine_pros      = sa.create_engine(f"mysql+pymysql://{DB_USERNAME}:{DB_TOKEN}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
            table_name_pros  = 'wf_p_calculator_raw_data'
            # I.2. Define the SQL Query to Retrieve Data
            query_pros       = f"SELECT * FROM {table_name_pros}"
            # I.3. Read Data from SQL Table into a DataFrame and Drop Duplicates by Email
            df_wf_p_raw = pd.read_sql(query_pros, engine_pros)
            df_wf_p_raw = df_wf_p_raw.drop_duplicates(subset=['email']).reset_index(drop=True)
            
            # =============================================================================
            # SECTION II. Duplicate Raw Dataframe as Processed Dataframe
            # =============================================================================
            # II.1. Duplicate Data until Column 9
            df_wf_p_pros = df_wf_p_raw.iloc[:, :9]
            # II.2. Add Calculated Column to Dataframe
            df_wf_p_pros["latitude"]  = None
            df_wf_p_pros["longitude"] = None
            df_wf_p_pros["wf_hyg"]    = None
            df_wf_p_pros["wf_food"]   = None 
            df_wf_p_pros["wf_dom"]    = None
            df_wf_p_pros["wf_total"]  = None
            
            for i, row in df_wf_p_raw.iterrows():
            # =============================================================================
            # SECTION III. Calculate Water Usage for Hygiene Consumption Pattern
            # =============================================================================
                # III. 1. Calculate Water Usage for Showering
                if df_wf_p_raw.loc[i, 'shower_equipment'] == 'Shower': 
                    wf_hyg_shower = 6 * 1 * df_wf_p_raw.loc[i, 'shower'] * df_wf_p_raw.loc[i, 'shw_shower_cal']
                else: 
                    if df_wf_p_raw.loc[i, 'shw_dipper_type'] == 'Small Dipper (1.3 L)': 
                        wf_hyg_shower = 1.3 * 0.75 * df_wf_p_raw.loc[i, 'shower'] * df_wf_p_raw.loc[i, 'shw_dipper_cal']
                    elif df_wf_p_raw.loc[i, 'shw_dipper_type'] == 'Medium Dipper (1.7 L)':
                        wf_hyg_shower = 1.7 * 0.75 * df_wf_p_raw.loc[i, 'shower'] * df_wf_p_raw.loc[i, 'shw_dipper_cal']
                    else: 
                        wf_hyg_shower = 2.4 * 0.75 * df_wf_p_raw.loc[i, 'shower'] * df_wf_p_raw.loc[i, 'shw_dipper_cal']
                # III.2. Calculate Water Usage for Defeciating and Urinating
                if df_wf_p_raw.loc[i, 'toilet_equipment'] == 'Toilet Button':
                    wf_hyg_def = 3 * 1 * df_wf_p_raw.loc[i, 'toil_def_button_cal'] * df_wf_p_raw.loc[i, 'defeciate']
                    wf_hyg_uri = 3 * 1 * df_wf_p_raw.loc[i, 'toil_uri_button_cal'] * df_wf_p_raw.loc[i, 'urinate']
                else: 
                    if df_wf_p_raw.loc[i, 'toil_dipper_type'] == 'Small Dipper (1.3 L)': 
                        wf_hyg_def = 1.3 * 0.75 * df_wf_p_raw.loc[i, 'toil_def_dipper_cal'] * df_wf_p_raw.loc[i, 'defeciate'] 
                        wf_hyg_uri = 1.3 * 0.75 * df_wf_p_raw.loc[i, 'toil_uri_dipper_cal'] * df_wf_p_raw.loc[i, 'urinate'] 
                    elif df_wf_p_raw.loc[i, 'toil_dipper_type'] == 'Medium Dipper (1.7 L)':
                        wf_hyg_def = 1.7 * 0.75 * df_wf_p_raw.loc[i, 'toil_def_dipper_cal'] * df_wf_p_raw.loc[i, 'defeciate'] 
                        wf_hyg_uri = 1.7 * 0.75 * df_wf_p_raw.loc[i, 'toil_uri_dipper_cal'] * df_wf_p_raw.loc[i, 'urinate'] 
                    else:
                        wf_hyg_def = 2.4 * 0.75 * df_wf_p_raw.loc[i, 'toil_def_dipper_cal'] * df_wf_p_raw.loc[i, 'defeciate'] 
                        wf_hyg_uri = 2.4 * 0.75 * df_wf_p_raw.loc[i, 'toil_uri_dipper_cal'] * df_wf_p_raw.loc[i, 'urinate'] 
                # III.3. Sum Water Usage for Hygiene Consumption
                wf_hyg = float(wf_hyg_shower + wf_hyg_def + wf_hyg_uri)
                df_wf_p_pros.loc[i, "wf_hyg"] = round(wf_hyg,1)
            # =============================================================================
            # SECTION IV. Calculate Water Usage for Food Consumption Pattern
            # =============================================================================
                # IV.1. Calculate Water Usage for Drinking
                wf_food_dri = df_wf_p_raw.loc[i, 'water_glass'] * 250/1000
                # IV.2 Calculate Water Usage for Eating
                if df_wf_p_raw.loc[i, 'cooked_rice_cal'] == '1 Liter': 
                    wf_food_ric = df_wf_p_raw.loc[i, 'cooked_rice'] * 1.44 * 1
                elif df_wf_p_raw.loc[i, 'cooked_rice_cal'] == '2 Liter': 
                    wf_food_ric = df_wf_p_raw.loc[i, 'cooked_rice'] * 1.44 * 2
                elif df_wf_p_raw.loc[i, 'cooked_rice_cal'] == '3 Liter': 
                    wf_food_ric = df_wf_p_raw.loc[i, 'cooked_rice'] * 1.44 * 3
                elif df_wf_p_raw.loc[i, 'cooked_rice_cal'] == '4 Liter': 
                    wf_food_ric = df_wf_p_raw.loc[i, 'cooked_rice'] * 1.44 * 4
                else :
                    wf_food_ric = df_wf_p_raw.loc[i, 'cooked_rice'] * 1.44 * 5
                # IV.3. Sum Water Usage for Hygiene Consumption
                wf_food = wf_food_dri + wf_food_ric
                df_wf_p_pros.loc[i, "wf_food"] = round(wf_food,1)
            # =============================================================================
            # SECTION V. Calculate Water Usage for Domestic Consumption Pattern
            # =============================================================================
                # V.1. Calculate Water Usage for Dishes Washing
                wf_dom_dish = df_wf_p_raw.loc[i, 'washed_dish'] * df_wf_p_raw.loc[i, 'washed_dish_cal'] * 7
                # V.2. Calculater Water Usage for Mopping
                wf_dom_mop = df_wf_p_raw.loc[i, 'mop_floor'] / 12 * df_wf_p_raw.loc[i, 'mop_floor_cal'] * 2.4
                # V.3. Calculater Water Usage for Clothes Washing
                if df_wf_p_raw.loc[i, 'washed_cloth_equipment'] == 'Washing Machine':
                    wf_dom_cloth = 150 * df_wf_p_raw.loc[i, 'washed_cloth_cal'] * 0.5
                else: 
                    wf_dom_cloth = 50 * df_wf_p_raw.loc[i, 'washed_cloth_cal'] * 0.5
                # V.4. Calculater Water Usage for Bike Washing
                if df_wf_p_raw.loc[i, 'vehicle_bike_cal'] == 'Yes':
                    wf_dom_bike = df_wf_p_raw.loc[i, 'vehicle_bike'] * df_wf_p_raw.loc[i, 'vehicle_bike_shw'] / 12 * 15 
                else:
                    wf_dom_bike = 0 
                # V.5. Calculate Water Usage for Car Washing
                if df_wf_p_raw.loc[i, 'vehicle_car_cal'] == 'Yes':
                    wf_dom_car = df_wf_p_raw.loc[i, 'vehicle_car'] * df_wf_p_raw.loc[i, 'vehicle_car_shw'] / 12 * 50
                else:
                    wf_dom_car = 0 
                # V.6. Calculate Water Usage for Garding
                wf_dom_gar = df_wf_p_raw.loc[i, 'gardening'] * df_wf_p_raw.loc[i, 'gardening_cal'] * 4
                # V.7. Sum Water Usage for Domestic Consumption
                wf_dom = wf_dom_dish + wf_dom_mop + wf_dom_cloth + wf_dom_bike + wf_dom_car + wf_dom_gar
                df_wf_p_pros.loc[i, "wf_dom"] = round(wf_dom,1)
            # =============================================================================
            # SECTION VI. Calculate Total Water Usage
            # =============================================================================
                 # VI.1. Calculate Total Water Usage
                df_wf_p_pros.loc[i, "wf_total"] = round(wf_hyg + wf_food + wf_dom,1)
            # =============================================================================
            # SECTION VII. Add Latitude and Longitude Information
            # =============================================================================
                # VII.1. Define Geolocator Engine
                df_wf_p_pros['subdistrict_name'] = df_wf_p_pros['subdistrict'].str.replace('Kecamatan ', '', regex=True)
                geolocator = geopy.geocoders.Nominatim(user_agent="your_app_name")
                # VII.2. Iterate through each Subdistrict
                for index, row in df_wf_p_pros.iterrows():
                    location_name = row['subdistrict_name'] + ", Indonesia"
                    location = geolocator.geocode(location_name)
                    df_wf_p_pros.loc[index, 'latitude'] = location.latitude
                    df_wf_p_pros.loc[index, 'longitude'] = location.longitude
                df_wf_p_pros= df_wf_p_pros.drop('subdistrict_name', axis=1)
        wf_p_pros_func()
    
        # =============================================================================
        # WATER FOOTPRINT FOR PERSONAL USE - STORING PROCESSING DATA
        # =============================================================================
        def store_wf_p_pros_func():
            # =============================================================================
            # PRE-SECTION: INITIALIZE CONNECTION TO SQL
            # =============================================================================
            # 0.1. Database Connection Details
            engine = sa.create_engine(f"mysql+pymysql://{DB_USERNAME}:{DB_TOKEN}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
            # 0.2. Define Table Schema
            table_name = 'wf_p_calculator_pros_data'
            schema = {
                # Record data from Personal Data
                "full_name"    : sa.Column(sa.String(200)),
                "email"        : sa.Column(sa.String(200)),
                "birth_date"   : sa.Column(sa.Date),
                "gender"       : sa.Column(sa.String(200)),   
                "education"    : sa.Column(sa.String(200)),
                "occupation"   : sa.Column(sa.String(200)),
                "city"         : sa.Column(sa.String(200)),
                "subdistrict"  : sa.Column(sa.String(200)),
                "latitude"     : sa.Column(sa.Float),
                "longitude"    : sa.Column(sa.Float),
                "water_source" : sa.Column(sa.String(200)),
                "wf_hyg"       : sa.Column(sa.Float), 
                "wf_food"      : sa.Column(sa.Float),
                "wf_dom"       : sa.Column(sa.Float),
                "wf_total"     : sa.Column(sa.Float)    
                }
            # 0.3 Store to MySQL
            df_wf_p_pros.to_sql(table_name, engine, index=False, if_exists='append')
        store_wf_p_pros_func()

def wf_p_model():
    st.markdown(f"# {list(page_names_to_funcs.keys())[2]} 💻")
    # =============================================================================
    # Model I. Modelling Map
    # =============================================================================
    def model_map():
        global df_wf_p_pros
        # =============================================================================
        # SECTION I. Import Dataframe from MySQL Database
        # =============================================================================
        # I.1. Database Connection Details
        engine = sa.create_engine(f"mysql+pymysql://{DB_USERNAME}:{DB_TOKEN}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
        table_name = 'wf_p_calculator_pros_data'
        # I.2. Define the SQL query to retrieve data
        query = f"SELECT * FROM {table_name}"  # Selects all columns from user_data table
        # I.3. Read data from SQL table into a DataFrame
        df_wf_p_pros = pd.read_sql(query, engine)
        # I.4 Processed data 
        avg_wf_p_pros_subdistrict = df_wf_p_pros.groupby("subdistrict")[["latitude", "longitude", "wf_hyg", "wf_food", "wf_dom", "wf_total"]].mean()
        wf_data = ['wf_hyg', 'wf_food', 'wf_dom', 'wf_total']
        avg_wf_p_pros_subdistrict[wf_data] = avg_wf_p_pros_subdistrict[wf_data].map('{:.1f}'.format)

        # =============================================================================
        # SECTION II. Set Streamlit UI/UX
        # =============================================================================
        # II.1. Set Streamlit Viewport
        #st.set_page_config(layout="wide")
        # II.2. Define a Layer to Display on a Map
        wf_model_layer = pdk.Layer(
            "ColumnLayer",
            data            = avg_wf_p_pros_subdistrict,
            get_position    = ["longitude", "latitude"], 
            get_elevation   = "wf_total",
            radius          = 50,
            elevation_scale = 25,
            elevation_range = [0, 50],
            pickable        = True,
            extruded        = True,
            auto_highlight  = True, 
            get_fill_color  = ["wf_total", "wf_total * 102", "wf_total * 153", 1000],
        )
        # II.3. Set the Tooltip Cursor
        tooltip = {
            "html": "The average water usage in  this location is <b>{wf_total}</b> litre per day",
            "style": {"background": "grey", "color": "white", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"},
        }
        # II.4. Plot the Layer to Streamlit Board
        st.pydeck_chart(pdk.Deck(
            map_style           = "road",
            tooltip             = tooltip,
            initial_view_state  = pdk.ViewState(
                latitude    = -6.1944,
                longitude   = 106.8229,
                zoom        = 12,
                pitch       = 50,
            ),
            layers=[wf_model_layer]
        ))
    model_map()

# =============================================================================
# WATER FOOTPRINT FOR PERSONAL USE - OVERVIEW PAGE
# =============================================================================
# Parameter - Overview Page
# Def Function - Overview Page
def wf_p_overview():
    st.markdown(f"# {list(page_names_to_funcs.keys())[3]} 🗒️")
    st.write(
        """
        This infographics showcasing the Waterfootprint data that we have been colected.
        """
    )
    # =============================================================================
    # SECTION I. Chart Water Footprint per Country
    # =============================================================================
    # I.1. Read Dataframe
    @st.cache_data
    def get_UN_data():
        AWS_BUCKET_URL = "http://streamlit-demo-data.s3-us-west-2.amazonaws.com"
        df = pd.read_csv(AWS_BUCKET_URL + "/agri.csv.gz")
        return df.set_index("Region")
    df = get_UN_data()
    # I.2. Define Multiselect Button and Plot the Graph
    countries = st.multiselect(
        "Choose countries", list(df.index), ["China", "United States of America"]
    )
    if not countries:
        st.error("Please select at least one country.")
    else:
        data = df.loc[countries]
        data /= 1000000.0
        st.write("### Water Usage per Countries (m3)", data.sort_index())

        data = data.T.reset_index()
        data = pd.melt(data, id_vars=["index"]).rename(
            columns={"index": "year", "value": "Water Usage per Countries (m3)"}
        )
        chart = (
            alt.Chart(data)
            .mark_area(opacity=0.3)
            .encode(
                x="year:T",
                y=alt.Y("Water Usage per Countries (m3):Q", stack=None),
                color="Region:N",
            )
        )
        st.altair_chart(chart, use_container_width=True)
        
    def model_region(): 
        # =============================================================================
        # SECTION I. Import Dataframe from MySQL Database
        # =============================================================================
        # I.1. Database Connection Details
        engine = sa.create_engine(f"mysql+pymysql://{DB_USERNAME}:{DB_TOKEN}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
        table_name = 'wf_p_calculator_pros_data'
        # I.2. Define the SQL query to retrieve data
        query = f"SELECT * FROM {table_name}"  # Selects all columns from user_data table
        # I.3. Read data from SQL table into a DataFrame
        df_wf_p_pros = pd.read_sql(query, engine)
        # I.4 Processed data 
        avg_wf_p_pros_subdistrict = df_wf_p_pros.groupby("subdistrict")[["latitude", "longitude", "wf_hyg", "wf_food", "wf_dom", "wf_total"]].mean()
        wf_data = ['wf_hyg', 'wf_food', 'wf_dom', 'wf_total']
        avg_wf_p_pros_subdistrict[wf_data] = avg_wf_p_pros_subdistrict[wf_data].map('{:.1f}'.format)

        col1,col2,col3 = st.columns(3)
        with col1: 
            city_filter_button         = st.selectbox("What city do you live in?", ("Kota Bandung", "Kota Cimahi", "Kabupaten Bandung Barat", "Kabupaten Bandung"), label_visibility="collapsed", placeholder="What city do you live in?", index=0)
        with col2: 
            subdistrict_filter_button  = st.selectbox("What sub-district do you live in?",(
                "Kecamatan Bandung Kulon", "Kecamatan Babakan Ciparay", "Kecamatan Bojongloa Kidul", "Kecamatan Bojongloa Kaler", "Kecamatan Astanaanyar", "Kecamatan Regol", "Kecamatan Lengkong", "Kecamatan Bandung Kidul", "Kecamatan Buah Batu", "Kecamatan Rancasari", 
                "Kecamatan Gedebage", "Kecamatan Cibiru", "Kecamatan Panyileukan", "Kecamatan Ujungberung", "Kecamatan Cinambo", "Kecamatan Arcamanik", "Kecamatan Antapani", "Kecamatan Mandalajati", "Kecamatan Kiaracondong", "Kecamatan Batununggal",
                "Kecamatan Sumur Bandung", "Kecamatan Andir", "Kecamatan Cicendo", "Kecamatan Bandung Wetan", "Kecamatan Cibeunying Kidul", "Kecamatan Cibeunying Kaler", "Kecamatan Coblong", "Kecamatan Sukajadi", "Kecamatan Sukasari", "Kecamatan Cidadap"), placeholder="What district do you live in?", label_visibility="collapsed", index=4)
        with col3: 
            filter_button = st.button("Find Your Region Data 💧", type="primary", use_container_width=True)

        consumption_type_map = {
            "wf_hyg": "Hygiene Use",
            "wf_dom": "Domestic Use",
            "wf_food": "Food Use",
            "wf_total": "Total Use"
            }
        map_consumption_type = lambda col: consumption_type_map.get(col)
        

        grouped_wf_p_pros_subdistrict = df_wf_p_pros[df_wf_p_pros['subdistrict'] == subdistrict_filter_button]
        grouped_wf_p_pros_subdistrict = grouped_wf_p_pros_subdistrict.drop_duplicates(subset='email')
        grouped_wf_p_pros_subdistrict_gender = round(grouped_wf_p_pros_subdistrict.groupby("gender")[["wf_hyg", "wf_food", "wf_dom", "wf_total"]].mean(), 1)
        grouped_wf_p_pros_subdistrict_gender = grouped_wf_p_pros_subdistrict_gender.reset_index()
        keep_columns = ["subdistrict", "wf_hyg", "wf_dom", "wf_food", "wf_total"]
        grouped_wf_p_pros_subdistrict = grouped_wf_p_pros_subdistrict[[col for col in grouped_wf_p_pros_subdistrict.columns if col in keep_columns]]



        melted_grouped_wf_p_pros_subdistrict = grouped_wf_p_pros_subdistrict.melt(id_vars="subdistrict", var_name="consumption_type", value_name="water_consumption")
        melted_grouped_wf_p_pros_subdistrict['consumption_type'] = melted_grouped_wf_p_pros_subdistrict['consumption_type'].apply(map_consumption_type)
        melted_grouped_wf_p_pros_subdistrict.dropna()
        
        melted_grouped_wf_p_pros_subdistrict_gender = grouped_wf_p_pros_subdistrict_gender.melt(id_vars="gender", var_name="consumption_type", value_name="water_consumption")
        melted_grouped_wf_p_pros_subdistrict_gender['consumption_type'] = melted_grouped_wf_p_pros_subdistrict_gender['consumption_type'].apply(map_consumption_type)
        melted_grouped_wf_p_pros_subdistrict_gender.dropna()
        
        st.markdown("### Average Water Usage in " + subdistrict_filter_button + " - " + city_filter_button) 
        col4,col5 = st.columns([3,2])
        with col4: 
            st.markdown("##### Based on Consumption Type")
        with col5: 
            st.markdown("##### Based on Gender")


        col6,col7 = st.columns([3,2], vertical_alignment="bottom")
        with col6: 
            
            chart_average = alt.Chart(melted_grouped_wf_p_pros_subdistrict.dropna()).mark_bar(opacity=1).encode(
                x= alt.X('mean(water_consumption):Q', title="Total Water Consumption (Liter/Day)"),
                y= alt.Y('consumption_type:N', title=None).sort('x'), 
                color=alt.Color('consumption_type:N', scale=alt.Scale(scheme='tableau20'), legend=None)
            )
            st.altair_chart(chart_average, use_container_width=True)

        with col7: 
            #chart_gender = alt.Chart(melted_grouped_wf_p_pros_subdistrict_gender.sort_values(by='mean(water_consumption)', ascending=False)).mark_bar(opacity=0.8).encode(

            chart_gender = alt.Chart(melted_grouped_wf_p_pros_subdistrict_gender.dropna()).mark_bar(opacity=1).encode(
                x= alt.X('mean(water_consumption):Q', title="Total Water Consumption (Liter/Day)").stack(None),
                y= alt.Y('gender:N', title=None), 
                color=alt.Color('consumption_type:N', scale=alt.Scale(scheme='tableau20'), legend=None)
            )

            st.altair_chart(chart_gender, use_container_width=True)
    model_region()
# =============================================================================
# WATER FOOTPRINT - SIDEBAR
# =============================================================================
# Parameter - Sidebar 
#st.logo("C:/Users/axelh/OneDrive/Documents/Hydroinformatics/ReservoAir/Logo/ReservoAir-Logo.png")
page_names_to_funcs = {
    "Introduction"                  : wf_p_home,
    "Water Footprint Calculator"    : wf_p_calculator,
    "Water Footprint Model"         : wf_p_model,
    "Water Footprint Overview"      : wf_p_overview
}
# Footer - Sidebar
wf_p_sidebar = st.sidebar.selectbox("WF for Personal Use Menu", page_names_to_funcs.keys())
page_names_to_funcs[wf_p_sidebar]()

st.sidebar.write("---")
st.sidebar.markdown("### Do You Want to Do More?")
st.sidebar.button("Recharge the Groundwater Now! 💧", type="primary")

st.sidebar.write("---")
st.sidebar.markdown("### How do We do It?")
st.sidebar.page_link("http://www.reservoair.com", label="Methods & Reference", icon="📓")

# III.2. FOOTER MENU 
st.sidebar.write("---")
st.sidebar.markdown("### Who are We?")
st.sidebar.page_link("http://www.reservoair.com", label="About Us", icon="🌎")
st.sidebar.page_link("http://www.reservoair.com/proyek", label="Projects", icon="📰")
st.sidebar.page_link("http://www.reservoair.com/kontak", label="Contact Us", icon= "☎️")
