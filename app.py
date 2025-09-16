import streamlit as st
import pandas as pd

# Config page
st.set_page_config(
    page_title="Ideas Bank - Data For Life",
    page_icon="💡",
    layout="wide"  
)

# --- Load data ---
@st.cache_data
def load_data(csv_path):
    try:
        df = pd.read_csv(csv_path)
        df = df.fillna('') 
        return df
    except FileNotFoundError:
        return None

CSV_FILE_PATH = 'dataset/CSV_dataset.csv' 
df = load_data(CSV_FILE_PATH)

# --- UI Design ---

# Tittle
st.title("💡 Ideas Bank - Data For Life")
st.write("Use the search bar below to explore ideas for solving social problems.")
if df is None:
    st.error(f"Bug: Can not find file '{CSV_FILE_PATH}'.")
else:
    # Search
    
    # Placeholder
    search_term = st.text_input(
       "Enter the keyword you want to search:", 
    placeholder="Example: transportation, healthcare, logistics, pollution..."
)

    if search_term:
        keyword_lower = search_term
        mask = df.apply(
            lambda row: row.astype(str).str.contains(keyword_lower).any(),
            axis=1
        )
        results = df[mask]
        st.subheader(f"Find {len(results)} results for '{search_term}'")

        if not results.empty:
            for index, row in results.iterrows():
                # Flex block
                with st.expander(f"**{row['title']}** - {row['category']}"):
                    st.markdown(f"**🔗 Link:** [{row['link']}]({row['link']})")
                    
                        #Content
                    if 'Đề xuất' in row and row['Đề xuất']:
                        st.markdown("**Đề xuất:**")
                        st.info(row['Đề xuất'])

                    if 'Đối tượng' in row and row['Đối tượng']:
                        st.markdown("**Đối tượng:**")
                        st.info(row['Đối tượng'])

                    if 'Tác động' in row and row['Tác động']:
                        st.markdown("**Tác động:**")
                        st.info(row['Tác động'])
                        
                    if 'Thời điểm, Bối cảnh' in row and row['Thời điểm, Bối cảnh']:
                        st.markdown("**Thời điểm, Bối cảnh:**")
                        st.info(row['Thời điểm, Bối cảnh'])

                    if 'Thực trạng' in row and row['Thực trạng']:
                        st.markdown("**Thực trạng:**")
                        st.info(row['Thực trạng'])

        else:
            st.warning("No matches words.")
    else:
        st.info("Latest 10 ideas:")
        st.dataframe(df.head(10))