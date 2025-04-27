import os
import sys
import time
import streamlit as st

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from utils.data import (
    get_states,
    get_crops,
    get_state_id,
    get_crop_id,
    get_soil_types,
    get_recommendations,
    get_schedule,
)
from utils.format import format_schedule_response


def main():
    st.title("🌾 Agri Apex")

    with st.form(key="recommendation_form"):
        states = get_states()
        state = st.selectbox("Select State", states, index=9)

        #TODO: want to implement a real-time listener
        crops = get_crops(state)
        crop = st.selectbox("Select Crop", crops, index=919)

        soil_options = get_soil_types()
        soil = st.selectbox("Select Soil Type", soil_options)

        area = st.number_input("Area (sq meters)", min_value=0, value=150)
        total_days = st.number_input("Total Days", min_value=1, value=100)
        sowing_date = st.date_input("Sowing Date")

        st.markdown("---")
        st.subheader("Soil Nutrient Content")

        n = st.number_input("Nitrogen (N) kg/ha", value=100)
        p = st.number_input("Phosphorous (P) kg/ha", value=100)
        k = st.number_input("Potassium (K) kg/ha", value=100)

        st.markdown("---")
        st.subheader("Location")
        lat = st.number_input("Latitude", value=12.971724806666074, format="%.15f")
        lon = st.number_input("Longitude", value=80.04313257366428, format="%.15f")

        submit_btn = st.form_submit_button(label="Get Recommendation 🚀")

    if submit_btn:
        with st.spinner("Fetching recommendations..."):
            try:
                state_id = get_state_id(state)
                crop_id = get_crop_id(crop)

                recommendation = get_recommendations(state_id, crop_id, n, p, k)
                schedule = get_schedule(recommendation, crop, total_days, sowing_date)
                df_schedule = format_schedule_response(schedule)

                time.sleep(5)

                st.success("Schedule Generated Successfully!")
                st.subheader("📋 Recommended Schedule")

                st.dataframe(df_schedule)
                # st.json(schedule)

            except Exception as err:
                st.error(f"Error: {str(err)}")

if __name__ == "__main__":
    main()
