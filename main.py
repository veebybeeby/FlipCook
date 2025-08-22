import streamlit as st
import random
import json
from pathlib import Path

# --- File paths ---
data_folder = Path(".")
preferences_file = data_folder / "preferences.json"

# --- Load items from text file ---
def load_items_from_txt(filename):
    try:
        with open(data_folder / filename, "r") as file:
            return [line.strip() for line in file if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        return []

proteins = load_items_from_txt("proteins.txt")
carbs = load_items_from_txt("carbs.txt")
vegetables = load_items_from_txt("veg.txt")

# --- Load or initialize preferences ---
try:
    with open(preferences_file, "r") as file:
        preferences = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    preferences = {
        "James": {"proteins": proteins.copy(), "carbs": carbs.copy(), "vegetables": vegetables.copy()},
        "Jess": {"proteins": proteins.copy(), "carbs": carbs.copy(), "vegetables": vegetables.copy()}
    }

# --- User selection ---
selected_user = st.selectbox("Select User:", list(preferences.keys()))

# --- Streamlit UI ---
st.title("🍳 Flip Cook – Mix & Match Menu")
st.markdown("Pick your favourite foods and mix your meal by randomising each component!")

# --- Initialize session_state for menu ---
if "menu" not in st.session_state or st.session_state.get("user") != selected_user:
    st.session_state.user = selected_user
    user_pref = preferences[selected_user]
    st.session_state.menu = {
        "protein": random.choice(user_pref["proteins"] or proteins),
        "carb": random.choice(user_pref["carbs"] or carbs),
        "veg": random.choice(user_pref["vegetables"] or vegetables)
    }

# --- Functions to randomise ---
def randomise_protein():
    st.session_state.menu["protein"] = random.choice(preferences[selected_user]["proteins"] or proteins)

def randomise_carb():
    st.session_state.menu["carb"] = random.choice(preferences[selected_user]["carbs"] or carbs)

def randomise_veg():
    st.session_state.menu["veg"] = random.choice(preferences[selected_user]["vegetables"] or vegetables)

def randomise_full():
    randomise_protein()
    randomise_carb()
    randomise_veg()

# --- Flip your meal section ---
st.markdown("### Flip your meal:")

st.button("🎲 randomise Full Meal", on_click=randomise_full, key="btn_full")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🥩 Protein")
    st.markdown(f"<span style='font-size:20px'>{st.session_state.menu['protein']}</span>", unsafe_allow_html=True)
    st.button("randomise Protein", on_click=randomise_protein, key="btn_protein")

with col2:
    st.subheader("🍞 Carb")
    st.markdown(f"<span style='font-size:20px'>{st.session_state.menu['carb']}</span>", unsafe_allow_html=True)
    st.button("randomise Carb", on_click=randomise_carb, key="btn_carb")

with col3:
    st.subheader("🥦 Veg")
    st.markdown(f"<span style='font-size:20px'>{st.session_state.menu['veg']}</span>", unsafe_allow_html=True)
    st.button("randomise Veg", on_click=randomise_veg, key="btn_veg")

# --- Update Preferences section ---
st.markdown("---")
st.markdown(f"### Update {selected_user}'s preferences:")

preferences[selected_user]["proteins"] = st.multiselect(
    "🥩 Proteins",
    options=proteins,
    default=preferences[selected_user]["proteins"]
)

preferences[selected_user]["carbs"] = st.multiselect(
    "🍞 Carbs",
    options=carbs,
    default=preferences[selected_user]["carbs"]
)

preferences[selected_user]["vegetables"] = st.multiselect(
    "🥦 Vegetables",
    options=vegetables,
    default=preferences[selected_user]["vegetables"]
)

# Save preferences
with open(preferences_file, "w") as file:
    json.dump(preferences, file, indent=2)
