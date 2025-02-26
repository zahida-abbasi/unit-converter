import streamlit as st
import requests  # Add this at the top with other imports
from datetime import datetime

# Add custom styling
st.set_page_config(
    page_title="Unit Converter",
    page_icon="🔄",
    layout="wide"
)

# Custom CSS with updated colors
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
        background-color: #f5f5f5;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background-color: #4a90e2;
        padding: 10px 10px 0px;
        border-radius: 10px 10px 0px 0px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #ffffff;
        border-radius: 5px 5px 0px 0px;
        gap: 1px;
        padding: 10px;
        color: #4a90e2; /* Text color for active tab */
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #e0e0e0; /* Hover effect for tabs */
    }
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 16px;
        color: #000080; /* Text color for inactive tabs */
    }
    .stTabs [data-baseweb="tab-list"] button:hover {
        color: #4a90e2; /* Text color on hover */
    }
    .stSuccess {
        background-color: #dff0d8;
        padding: 20px;
        border-radius: 5px;
        border: 1px solid #d6e9c6;
        margin: 20px 0;
        color: #3c763d;
    }
    div.row-widget.stSelectbox > div {
        background-color: #ffffff;
        border-radius: 5px;
        padding: 5px;
        border: 1px solid #4a90e2;
    }
    div.row-widget.stNumberInput > div {
        background-color: #ffffff;
        border-radius: 5px;
        padding: 5px;
        border: 1px solid #4a90e2;
    }
    .title-container {
        background-color: #4a90e2;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        text-align: center;
        color: #ffffff;
    }
    .footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        background-color: #4a90e2;
        padding: 10px;
        text-align: center;
        color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

def length_converter(value, from_unit, to_unit):
    # Conversion factors to meters
    length_units = {
        'Meters': 1,
        'Kilometers': 1000,
        'Centimeters': 0.01,
        'Millimeters': 0.001,
        'Miles': 1609.34,
        'Yards': 0.9144,
        'Feet': 0.3048,
        'Inches': 0.0254,
        'Light Years': 9.461e+15  # 1 light year = 9.461 trillion kilometers
    }
    
    # Convert to meters first, then to target unit
    meters = value * length_units[from_unit]
    result = meters / length_units[to_unit]
    return result

def weight_converter(value, from_unit, to_unit):
    # Conversion factors to kilograms
    weight_units = {
        'Kilograms': 1,
        'Grams': 0.001,
        'Pounds': 0.453592,
        'Ounces': 0.0283495
    }
    
    # Convert to kilograms first, then to target unit
    kilograms = value * weight_units[from_unit]
    result = kilograms / weight_units[to_unit]
    return result

def temperature_converter(value, from_unit, to_unit):
    # Conversion logic for temperatures
    if from_unit == to_unit:
        return value
    
    # Convert to Celsius first
    if from_unit == 'Fahrenheit':
        celsius = (value - 32) * 5/9
    elif from_unit == 'Kelvin':
        celsius = value - 273.15
    else:  # from Celsius
        celsius = value
    
    # Convert from Celsius to target unit
    if to_unit == 'Fahrenheit':
        return (celsius * 9/5) + 32
    elif to_unit == 'Kelvin':
        return celsius + 273.15
    else:  # to Celsius
        return celsius

def volume_converter(value, from_unit, to_unit):
    # Conversion factors to liters
    volume_units = {
        'Liters': 1,
        'Milliliters': 0.001,
        'Cubic Meters': 1000,
        'Gallons': 3.78541,
        'Fluid Ounces': 0.0295735,
        'Cups': 0.236588
    }
    return value * volume_units[from_unit] / volume_units[to_unit]

def time_converter(value, from_unit, to_unit):
    # Conversion factors to seconds
    time_units = {
        'Seconds': 1,
        'Minutes': 60,
        'Hours': 3600,
        'Days': 86400,
        'Weeks': 604800,
        'Months': 2628000,  # Average month (30.44 days)
        'Years': 31536000   # Non-leap year (365 days)
    }
    return value * time_units[from_unit] / time_units[to_unit]

def speed_converter(value, from_unit, to_unit):
    # Conversion factors to meters per second
    speed_units = {
        'Meters per Second': 1,
        'Kilometers per Hour': 0.277778,
        'Miles per Hour': 0.44704,
        'Knots': 0.514444
    }
    return value * speed_units[from_unit] / speed_units[to_unit]

def current_converter(value, from_unit, to_unit):
    # Conversion factors to amperes (A)
    current_units = {
        'Amperes': 1,
        'Milliamperes': 0.001,
        'Microamperes': 0.000001,
        'Kiloamperes': 1000
    }
    return value * current_units[from_unit] / current_units[to_unit]

def currency_converter(value, from_unit, to_unit):
    # Using exchangerate-api.com for real-time rates
    try:
        response = requests.get(f'https://api.exchangerate-api.com/v4/latest/{from_unit}')
        rates = response.json()['rates']
        return value * rates[to_unit]
    except:
        return None  # Return None if API call fails

def main():
    # Wrap title in custom container
    st.markdown("""
    <div class="title-container">
        <h1 style='text-align: center; color: #ffffff;'>🌍 World Unit Wizard Converter</h1>
        <p style='text-align: center; color: #ffffff; font-family: monospace;'>Master unit conversions across the globe—precision at your fingertips!</p>
    </div>
""", unsafe_allow_html=True)
    
    # Add new tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "📏 Length", 
        "⚖️ Weight", 
        "🌡️ Temperature",
        "📊 Volume", 
        "⏰ Time", 
        "🚀 Speed", 
        "⚡ Current",
        "💱 Currency"
    ])
    
    with tab1:
        st.header('Length Converter')
        length_units = ['Meters', 'Kilometers', 'Centimeters', 'Millimeters', 
                       'Miles', 'Yards', 'Feet', 'Inches', 'Light Years']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            value = st.number_input('Enter Value', value=1.0, key='length_value')
        with col2:
            from_unit = st.selectbox('From', length_units, key='length_from')
        with col3:
            to_unit = st.selectbox('To', length_units, key='length_to')
            
        result = length_converter(value, from_unit, to_unit)
        st.success(f'{value} {from_unit} = {result:.4f} {to_unit}')
    
    with tab2:
        st.header('Weight Converter')
        weight_units = ['Kilograms', 'Grams', 'Pounds', 'Ounces']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            value = st.number_input('Enter Value', value=1.0, key='weight_value')
        with col2:
            from_unit = st.selectbox('From', weight_units, key='weight_from')
        with col3:
            to_unit = st.selectbox('To', weight_units, key='weight_to')
            
        result = weight_converter(value, from_unit, to_unit)
        st.success(f'{value} {from_unit} = {result:.4f} {to_unit}')

    with tab3:
        st.header('Temperature Converter')
        temp_units = ['Celsius', 'Fahrenheit', 'Kelvin']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            value = st.number_input('Enter Value', value=0.0, key='temp_value')
        with col2:
            from_unit = st.selectbox('From', temp_units, key='temp_from')
        with col3:
            to_unit = st.selectbox('To', temp_units, key='temp_to')
            
        result = temperature_converter(value, from_unit, to_unit)
        st.success(f'{value} {from_unit} = {result:.2f} {to_unit}')

    with tab4:
        st.header('Volume Converter')
        volume_units = ['Liters', 'Milliliters', 'Cubic Meters', 'Gallons', 'Fluid Ounces', 'Cups']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            value = st.number_input('Enter Value', value=1.0, key='volume_value')
        with col2:
            from_unit = st.selectbox('From', volume_units, key='volume_from')
        with col3:
            to_unit = st.selectbox('To', volume_units, key='volume_to')
            
        result = volume_converter(value, from_unit, to_unit)
        st.success(f'{value} {from_unit} = {result:.4f} {to_unit}')

    with tab5:
        st.header('Time Converter')
        time_units = ['Seconds', 'Minutes', 'Hours', 'Days', 'Weeks', 'Months', 'Years']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            value = st.number_input('Enter Value', value=1.0, key='time_value')
        with col2:
            from_unit = st.selectbox('From', time_units, key='time_from')
        with col3:
            to_unit = st.selectbox('To', time_units, key='time_to')
            
        result = time_converter(value, from_unit, to_unit)
        st.success(f'{value} {from_unit} = {result:.4f} {to_unit}')

    with tab6:
        st.header('Speed Converter')
        speed_units = ['Meters per Second', 'Kilometers per Hour', 'Miles per Hour', 'Knots']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            value = st.number_input('Enter Value', value=1.0, key='speed_value')
        with col2:
            from_unit = st.selectbox('From', speed_units, key='speed_from')
        with col3:
            to_unit = st.selectbox('To', speed_units, key='speed_to')
            
        result = speed_converter(value, from_unit, to_unit)
        st.success(f'{value} {from_unit} = {result:.4f} {to_unit}')

    with tab7:
        st.header('Current Converter')
        current_units = ['Amperes', 'Milliamperes', 'Microamperes', 'Kiloamperes']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            value = st.number_input('Enter Value', value=1.0, key='current_value')
        with col2:
            from_unit = st.selectbox('From', current_units, key='current_from')
        with col3:
            to_unit = st.selectbox('To', current_units, key='current_to')
            
        result = current_converter(value, from_unit, to_unit)
        st.success(f'{value} {from_unit} = {result:.4f} {to_unit}')

    with tab8:
        st.header('Currency Converter')
        currency_units = [
            'USD', 'EUR', 'GBP',  # Major global currencies
            'INR', 'PKR', 'CNY', 'IRR', 'AFN', 'BDT', 'LKR', 'NPR', 'MVR',  # South Asian
            'JPY', 'KRW', 'SGD', 'MYR', 'IDR', 'THB', 'VND'  # East/Southeast Asian
        ]
        
        # Add currency names for better readability
        currency_names = {
            'USD': 'US Dollar',
            'EUR': 'Euro',
            'GBP': 'British Pound',
            'INR': 'Indian Rupee',
            'PKR': 'Pakistani Rupee',
            'CNY': 'Chinese Yuan',
            'IRR': 'Iranian Rial',
            'AFN': 'Afghan Afghani',
            'BDT': 'Bangladeshi Taka',
            'LKR': 'Sri Lankan Rupee',
            'NPR': 'Nepalese Rupee',
            'MVR': 'Maldivian Rufiyaa',
            'JPY': 'Japanese Yen',
            'KRW': 'South Korean Won',
            'SGD': 'Singapore Dollar',
            'MYR': 'Malaysian Ringgit',
            'IDR': 'Indonesian Rupiah',
            'THB': 'Thai Baht',
            'VND': 'Vietnamese Dong'
        }
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            value = st.number_input('Enter Value', value=1.0, key='currency_value')
        with col2:
            from_unit = st.selectbox('From', currency_units, 
                format_func=lambda x: f'{x} - {currency_names[x]}', 
                key='currency_from')
        with col3:
            to_unit = st.selectbox('To', currency_units, 
                format_func=lambda x: f'{x} - {currency_names[x]}', 
                key='currency_to')
            
        result = currency_converter(value, from_unit, to_unit)
        if result is not None:
            st.success(f'{value} {from_unit} ({currency_names[from_unit]}) = {result:.2f} {to_unit} ({currency_names[to_unit]})')
        else:
            st.error('Failed to fetch exchange rates. Please try again later.')

    # Add footer at the end of main()
    st.markdown("""
        <div class="footer">
            <p style='color: #ffffff;'>
                Last updated: {} | Made with ❤️ using Streamlit
            </p>
        </div>
    """.format(datetime.now().strftime("%Y-%m-%d")), unsafe_allow_html=True)

    # Add info section before tabs
    with st.expander("ℹ️ About this converter"):
        st.markdown("""
            This universal converter supports:
            - 📏 Length (including astronomical units)
            - ⚖️ Weight/Mass
            - 🌡️ Temperature
            - 📊 Volume
            - ⏰ Time
            - 🚀 Speed
            - ⚡ Current
            - 💱 Currency (real-time rates)
        """)

if __name__ == '__main__':
    main()
