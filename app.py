import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# --- Streamlit Page Setup ---
st.set_page_config(layout="wide")
st.title("🇸🇬 Singapore Commodity Re-Exports to Overseas")

st.markdown("""
### 📊 About This Dataset

DOWNLOAD dataset HERE : https://data.gov.sg/datasets/d_ccaae92652c42740829ab17013a698c2/view
- This dataset from [data.gov.sg](https://data.gov.sg) provides:

- **Singapore's Commodity re-exports**, categorized by **commodity divisions** (e.g., Beverages, Tobacco, etc.)
- Reported on a **monthly basis**, from **January 1976 to March 2025**
- Does **not include destination countries** — data reflects total overseas re-exports

In international trade statistics and classification systems (like HS, SITC, or CPC), "N.E.S." or "nes" or "Nes" stands for:

👉 "Not Elsewhere Specified"
🔍 What it Means:
It’s a catch-all category for items that:

- Don't fit neatly into the existing detailed classifications
- Are miscellaneous or residual goods in that group
- May be too specific or uncommon to have their own sub-code

📦 Example:
“Non-Metallic Mineral Manufactures, NES” might include:

- Unique construction materials
- Specialized ceramic items
- Non-metal mineral products not classified under other standard codes like glass, cement, or stone

So in the dataset, “NES” just means it’s a miscellaneous category for that commodity group.
            
🏅Example Takeaways:
            
BEVERAGES: 
Notable Beverage Brands: Tiger Beer, Yeo's, Pokka. 
Singapore's beverage re-exports saw:
- Exponential growth from the 90s to mid-2010s
- Volatility and plateauing in the 2020s
- Recent values appear to taper off slightly from 2021–2024, though still at relatively high levels compared to the 1990s.

PHARMA: 
Many U.S. pharmaceutical products are made in Singapore for companies like: Pfizer, GlaxoSmithKline (GSK), AbbVie, Roche, Sanofi, Amgen
- 2000–2019	Steady growth, Investment in pharma, Asia demand, logistics role
- 2020–2022	Dramatic spike, COVID-19 pandemic, vaccine/testing exports
- Post-2022	Fluctuating but high, New pharma logistics norm, continued global role
            
""")

st.caption("📌 Data Source: [data.gov.sg](https://data.gov.sg) — Monthly Commodity Division (1976–2025), again, if you haven't, DOWNLOAD dataset HERE : https://data.gov.sg/datasets/d_ccaae92652c42740829ab17013a698c2/view")

# --- Upload CSV ---
uploaded_file = st.file_uploader("📁 Upload the 'ReExportsByCommodityDivisionMonthly.csv' file", type=["csv"])

if uploaded_file:
    # Load and prepare the data
    df = pd.read_csv(uploaded_file)
    df = df.dropna(subset=["DataSeries"])  # Drop rows with missing commodity names

    # Convert wide to long format
    df_long = df.melt(id_vars=["DataSeries"], var_name="Month", value_name="Value")
    df_long["Month"] = pd.to_datetime(df_long["Month"] + "01", format="%Y%b%d", errors="coerce")
    df_long["Value"] = pd.to_numeric(df_long["Value"], errors="coerce")
    df_long = df_long.dropna(subset=["Month", "Value"])

    # Commodity selection
    commodity_list = sorted(df_long["DataSeries"].unique())
    selected_commodity = st.selectbox("📦 Select a Commodity Division", commodity_list)

    # Filter for the selected commodity
    filtered = df_long[df_long["DataSeries"] == selected_commodity].sort_values("Month")

    # --- Plotting ---
    st.subheader(f"📈 Monthly Re-Exports: {selected_commodity}")
    fig, ax = plt.subplots(figsize=(10, 4))  # Smaller height to reduce white space
    ax.plot(filtered["Month"], filtered["Value"], marker="o", color="orange")
    ax.set_xlabel("Date", labelpad=6)
    ax.set_ylabel("Value (thousands SGD)", labelpad=6)
    ax.set_title(f"Singapore Re-Exports — {selected_commodity}", pad=10)
    ax.grid(True)
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout(pad=1.5)
    st.pyplot(fig)

    # Optional table
    with st.expander("📋 View Raw Data Table"):
        st.dataframe(filtered)
else:
    st.info("Please upload the CSV file to begin.")
