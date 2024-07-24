import streamlit as st
import mysql.connector
from mysql.connector import Error

# Function to connect to the MySQL database
def create_connection(host, user, password, database):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        return connection
    except Error as e:
        st.error(f"The error '{e}' occurred")
        return None

# Function to execute a query and fetch results
def execute_read_query(connection, query, params=None):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query, params)
        result = cursor.fetchall()
        return result
    except Error as e:
        st.error(f"The error '{e}' occurred")
    finally:
        cursor.close()

# Streamlit application starts here
st.title("RedBus  Application")

# User inputs for database connection
st.sidebar.header("Database Connection Settings")
host = st.sidebar.text_input("Host", "localhost")
user = st.sidebar.text_input("User", "root")
password = st.sidebar.text_input("Password", type="password")
database = st.sidebar.text_input("Database", "redbus")

if st.sidebar.button("Connect"):
    connection = create_connection(host, user, password, database)
    if connection:
        st.session_state.connection = connection

if 'connection' in st.session_state:
    st.subheader("Bus Booking Details")

    # Fetching route names from the database
    query = "SELECT DISTINCT Route_Name FROM Bus_routes"
    route_names = execute_read_query(st.session_state.connection, query)
    route_names_list = [name[0] for name in route_names] if route_names else []
    
    query = "SELECT DISTINCT Bus_Type FROM Bus_routes"
    route_names = execute_read_query(st.session_state.connection, query)
    bus_type_list = [name[0] for name in route_names] if route_names else []
    
    query = "SELECT DISTINCT Bus_Name FROM Bus_routes"
    route_names = execute_read_query(st.session_state.connection, query)
    bus_name_list = [name[0] for name in route_names] if route_names else []
    
    query = "SELECT DISTINCT Start_Time FROM Bus_routes"
    route_names = execute_read_query(st.session_state.connection, query)
    start_time_list = [name[0] for name in route_names] if route_names else []
    
    query = "SELECT DISTINCT End_Time FROM Bus_routes"
    route_names = execute_read_query(st.session_state.connection, query)
    end_time_list = [name[0] for name in route_names] if route_names else []
    
    query = "SELECT DISTINCT Rating FROM Bus_routes"
    route_names = execute_read_query(st.session_state.connection, query)
    rating_list = [name[0] for name in route_names] if route_names else []
    
    query = "SELECT DISTINCT Price FROM Bus_routes"
    route_names = execute_read_query(st.session_state.connection, query)
    price_list = [name[0] for name in route_names] if route_names else []
    
    query = "SELECT DISTINCT Seat_Availability FROM Bus_routes"
    route_names = execute_read_query(st.session_state.connection, query)
    seat_avail_list = [name[0] for name in route_names] if route_names else []

    # Displaying the select box with route names
    route_name = st.selectbox("Route Name", route_names_list)
    bus_type = st.selectbox("Bus Type", bus_type_list)
    bus_name = st.selectbox("Bus Name", bus_name_list)
    start_time = st.selectbox("Start Time", start_time_list)
    end_time = st.selectbox("End Time", end_time_list)
    rating = st.selectbox("Rating", rating_list)
    price = st.selectbox("Price", price_list)
    seat_available = st.selectbox("Seat_Availability", seat_avail_list)

    if st.button("Search Buses"):
        query = """
        SELECT
            Route_Name,
            Bus_Name,
            Bus_Type,
            Start_Time,
            End_Time,
            Rating,
            Price,
            Seat_Availability
        FROM
            Bus_routes
        WHERE
            route_name LIKE '%{route_name}%'
            bus_type LIKE '%{bus_type}%'
            bus_name  LIKE '%{bus_name}%'
            start_time LIKE '%{start_time}%'
            end_time  LIKE '%{end_time}%'
            rating  LIKE '%{rating}%'
            price  LIKE '%{price}%'
            seat_available  LIKE '%{seat_available}%'
        """
        params = (f"%{route_name}%",f"%{bus_type}%",f"%{bus_name}%",f"%{start_time}%",f"%{end_time}%",f"%{rating}%",f"%{price}%",f"%{seat_available}%")
        buses = execute_read_query(st.session_state.connection, query, params)
        if buses:
            for bus in buses:
                st.markdown(f"*Route Name:* {bus[0]}")
                st.markdown(f"*Bus Name:* {bus[1]}")
                st.markdown(f"*Bus Type:* {bus[2]}")
                st.markdown(f"*Start Time:* {bus[3]}")
                st.markdown(f"*End Time:* {bus[4]}")
                st.markdown(f"*Rating:* {bus[5]}")
                st.markdown(f"*Price:* {bus[6]}")
                st.markdown(f"*Seat Availability:* {bus[7]}")
                st.markdown("---")
