import streamlit as st
import mysql.connector
from mysql.connector import Error

# Function to connect to the MySQL database
def create_connection(host, user, password, database):
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    return connection

# Example usage:
connection = create_connection(
    host="localhost",  # Use quotes around 'localhost'
    user="root",
    password="admin@123",
    database="redbus"
)

# Function to execute a query and fetch results
def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        st.error(f"The error '{e}' occurred")

# Streamlit application starts here
st.title("RedBus Application")

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
    
    query = "SELECT DISTINCT Route_Name FROM Bus_routes"
    route_names = execute_read_query(st.session_state.connection, query)
    route_names_list = [name[0] for name in route_names] if route_names else []

    route_name = st.selectbox("Route Name",route_names_list)
    if st.button("Search Buses"):
        query = f"""
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
        """
        
        params = (f"%{route_name}%",)
        buses = execute_read_query(st.session_state.connection, query)
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