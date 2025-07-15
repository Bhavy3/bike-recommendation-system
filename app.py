
import streamlit as st
import pandas as pd
import joblib

# Load the trained model (ensure this file exists after training)
model = joblib.load('model.pkl')

st.set_page_config(layout="wide")
st.markdown("""
<style>
.header-bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  min-width: 100vw;
  z-index: 9999;
  background: linear-gradient(90deg, #0f2027 0%, #2c5364 90%);
  padding: 2vw 0 1vw 0;
  border-radius: 0 0 1.2vw 1.2vw;
  box-sizing: border-box;
}
.header-content {
  width: 100vw;
  max-width: 100vw;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
@media (max-width: 600px) {
  .header-bg { padding: 4vw 0 2vw 0; }
  .header-content h1 { font-size: 5vw !important; }
  .header-content p { font-size: 2.5vw !important; }
}
</style>
<div class='header-bg'>
  <div class='header-content'>
    <h1 style='text-align: center; color:#F7CA18; font-family:Segoe UI,Arial,sans-serif; letter-spacing:0.07vw; font-size:2.5vw;'>🏍️ Used Bike Recommendation App</h1>
    <p style='text-align: center; color:#FDFEFE; font-size:1.3vw; font-family:Segoe UI,Arial,sans-serif;'>Find the best used bikes for your needs and budget!</p>
  </div>
</div>
<div style='height:6vw;'></div>
""", unsafe_allow_html=True)

# Load Used_Bikes.csv for brand/model mapping and data reference
@st.cache_data
def load_bike_data():
    df = pd.read_csv("Used_Bikes.csv")
    return df
df_bikes = load_bike_data()


# Sidebar for user input
with st.sidebar:
    st.markdown("<h2 style='color:#F7CA18;'>🔎 Filter Bikes</h2>", unsafe_allow_html=True)
    brands = sorted(df_bikes['brand'].unique())
    brand = st.selectbox("Brand", brands)
    models_for_brand = sorted(df_bikes[df_bikes['brand'] == brand]['bike_name'].unique())
    model_options = ["(Any)"] + models_for_brand
    model_name = st.selectbox("Bike Name", model_options)
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age (years)", min_value=0, max_value=30, value=5)
    with col2:
        min_price = st.number_input("Min Price (₹)", min_value=0, max_value=2000000, value=50000)
        max_price = st.number_input("Max Price (₹)", min_value=0, max_value=2000000, value=100000)
    st.markdown("<hr style='border:1px solid #F7CA18;'>", unsafe_allow_html=True)



# --- Preprocessing Maps (should match your notebook) ---
maker_map = {
    'TVS': 1, 'Royal Enfield': 2, 'Triumph': 3, 'Yamaha': 4, 'Honda': 5, 'Hero': 6, 'Bajaj': 7, 'Suzuki': 8,
    'Benelli': 9, 'KTM': 10, 'Mahindra': 11, 'Kawasaki': 12, 'Ducati': 13, 'Hyosung': 14, 'Harley-Davidson': 15,
    'Jawa': 16, 'BMW': 17, 'Indian': 18, 'Rajdoot': 19, 'LML': 20, 'Yezdi': 21, 'MV': 22, 'Ideal': 23
}

# Dummy model encoder (replace with your actual encoder if available)
def dummy_model_encoder(model_name):
    # In production, load and use the LabelEncoder from training
    # Here, just hash the model name for demonstration
    return abs(hash(model_name)) % 500



# Recommend button
if st.sidebar.button("✨ Recommend Bikes"):
    # Filter bikes as per user selection
    if model_name != "(Any)":
        filtered = df_bikes[(df_bikes['brand'] == brand) & (df_bikes['bike_name'] == model_name) & (df_bikes['age'] == age) & (df_bikes['price'] <= max_price) & (df_bikes['price'] >= min_price)]
        if filtered.empty:
            st.warning("No bikes found for this brand, bike name, age, and price range.")
        else:
            st.markdown(f"""
                <div style='background: linear-gradient(90deg, #232526 0%, #414345 100%); padding:1.2vw; border-radius:0.7vw; margin-bottom:1vw;'>
                <b style='color:#F7CA18;'>Recommended <span style='color:#FDFEFE'>{brand} {model_name}</span> bikes</b>
                <span style='color:#FDFEFE;'>(Age: <span style='color:#F7CA18'>{age}</span> years, Price: <span style='color:#F7CA18'>₹{min_price:,} - ₹{max_price:,}</span>)</span>
                </div>
            """, unsafe_allow_html=True)
            display_cols = [col for col in ['bike_name', 'price', 'age', 'kms_driven', 'cc', 'power', 'Power (BHP)'] if col in filtered.columns]
            st.metric("Bikes Found", len(filtered))
            for _, row in filtered[display_cols].iterrows():
                st.markdown(f"""
                <div style='background: linear-gradient(90deg, #232526 0%, #414345 100%); border-radius:0.7vw; margin-bottom:1.2vw; padding:1.3vw 1.3vw 0.7vw 1.3vw; box-shadow:0 0.13vw 0.53vw #0002;'>
                  <h4 style='color:#F7CA18; margin-bottom:0.5vw; font-size:1.3vw;'>{row['bike_name']}</h4>
                  <div style='color:#FDFEFE; font-size:1.05vw;'>
                    <b>Price:</b> ₹{int(row['price']):,} &nbsp;|&nbsp; <b>Age:</b> {row['age']} yrs
                    {f"<br><b>Kilometers:</b> {int(row['kms_driven']):,}" if 'kms_driven' in row else ''}
                    {f"<br><b>CC:</b> {row['cc']}" if 'cc' in row else ''}
                  </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        filtered = df_bikes[(df_bikes['brand'] == brand) & (df_bikes['age'] == age) & (df_bikes['price'] <= max_price) & (df_bikes['price'] >= min_price)]
        if filtered.empty:
            st.warning("No bikes found for this brand, age, and price range.")
        else:
            st.markdown(f"""
                <div style='background: linear-gradient(90deg, #232526 0%, #414345 100%); padding:1.2vw; border-radius:0.7vw; margin-bottom:1vw;'>
                <b style='color:#F7CA18;'>Recommended <span style='color:#FDFEFE'>{brand}</span> bikes</b>
                <span style='color:#FDFEFE;'>(Age: <span style='color:#F7CA18'>{age}</span> years, Price: <span style='color:#F7CA18'>₹{min_price:,} - ₹{max_price:,}</span>)</span>
                </div>
            """, unsafe_allow_html=True)
            display_cols = [col for col in ['bike_name', 'price', 'age', 'kms_driven', 'cc', 'power'] if col in filtered.columns]
            st.metric("Bikes Found", len(filtered))
            for _, row in filtered[display_cols].iterrows():
                st.markdown(f"""
                <div style='background: linear-gradient(90deg, #232526 0%, #414345 100%); border-radius:0.7vw; margin-bottom:1.2vw; padding:1.3vw 1.3vw 0.7vw 1.3vw; box-shadow:0 0.13vw 0.53vw #0002;'>
                  <h4 style='color:#F7CA18; margin-bottom:0.5vw; font-size:1.3vw;'>{row['bike_name']}</h4>
                  <div style='color:#FDFEFE; font-size:1.05vw;'>
                    <b>Price:</b> ₹{int(row['price']):,} &nbsp;|&nbsp; <b>Age:</b> {row['age']} yrs
                    {f"<br><b>Kilometers:</b> {int(row['kms_driven']):,}" if 'kms_driven' in row else ''}
                    {f"<br><b>CC:</b> {row['cc']}" if 'cc' in row else ''}
                  </div>
                </div>
                """, unsafe_allow_html=True)

# Main area: instructions or info
st.markdown("""
<div style='background: linear-gradient(90deg, #232526 0%, #414345 100%); padding:1.1vw; border-radius:0.7vw; margin-top:1vw;'>
<h3 style='color:#F7CA18; font-size:1.5vw;'>How to use:</h3>
<ul style='color:#FDFEFE; font-size:1.05vw;'>
<li>Select a <b>brand</b>, then choose a <b>bike name</b> (or leave as (Any) to see all available bikes for that brand).</li>
<li>Enter <b>age</b>, <b>minimum price</b>, and <b>maximum price</b> to filter recommendations.</li>
<li>Click <b>✨ Recommend Bikes</b> to see the list of recommended bikes from our dataset.</li>
</ul>
</div>
<br>
<div style='text-align:center;color:#F7CA18;font-size:1.2vw;'>Made with ❤️ for bike lovers</div>
""", unsafe_allow_html=True)