
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="TrustFarm AI",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 TrustFarm AI")
st.subheader(
    "Intelligent and Reliable Agriculture "
    "Decision Support System"
)

st.write(
    "Make informed farming decisions with crop "
    "comparisons, transparent reasoning, and risk checks."
)

st.warning(
    "Demo mode: scores use illustrative rules and are "
    "not validated probabilities of crop success."
)

st.header("1. Enter Farm Details")

left, right = st.columns(2)

with left:
    location = st.text_input("Farm location", "Tamil Nadu")
    soil = st.selectbox(
        "Soil type",
        ["Clay loam", "Loamy", "Clay", "Sandy"]
    )
    ph = st.slider("Soil pH", 3.0, 10.0, 6.5, 0.1)

with right:
    temp = st.slider("Temperature (°C)", 10, 45, 30)
    rain = st.selectbox(
        "Expected rainfall",
        ["Low", "Moderate", "High"]
    )
    water = st.selectbox(
        "Water availability",
        ["Low", "Moderate", "High"]
    )

if st.button("Analyze My Farm", type="primary"):

    # Illustrative demo rules only.
    crops = {
        "Paddy": 0,
        "Millet": 0,
        "Groundnut": 0
    }

    explanations = {
        "Paddy": [],
        "Millet": [],
        "Groundnut": []
    }

    if water == "High":
        crops["Paddy"] += 3
        explanations["Paddy"].append(
            "High water availability supports consideration "
            "of water-demanding crops."
        )
    else:
        crops["Millet"] += 2
        explanations["Millet"].append(
            "Lower water availability makes drought-tolerant "
            "crop options worth evaluating."
        )

    if rain == "Low":
        crops["Millet"] += 2
        crops["Groundnut"] += 1
    elif rain == "High":
        crops["Paddy"] += 2

    if soil in ["Loamy", "Sandy"]:
        crops["Groundnut"] += 2
    elif soil == "Clay":
        crops["Paddy"] += 1

    if 20 <= temp <= 35:
        crops["Millet"] += 1
        crops["Groundnut"] += 1

    if 5.5 <= ph <= 7.0:
        crops["Paddy"] += 1
        crops["Millet"] += 1
        crops["Groundnut"] += 1

    ranked = sorted(
        crops.items(),
        key=lambda item: item[1],
        reverse=True
    )

    st.header("2. Crop Recommendations")

    cols = st.columns(3)

    for col, (crop, score) in zip(cols, ranked):
        with col:
            st.metric(crop, f"{score} demo points")
            if score == ranked[0][1]:
                st.success("Highest rule match")

    chart_data = pd.DataFrame(
        ranked, columns=["Crop", "Demo points"]
    ).set_index("Crop")

    st.subheader("Crop Comparison")
    st.bar_chart(chart_data)

    st.header("3. Trust Analysis")

    missing = []

    if not location.strip():
        missing.append("Farm location")
    if ph == 6.5:
        missing.append(
            "A measured soil pH value should be confirmed"
        )

    st.write("**Evidence currently available:**")
    st.write(
        "User-entered soil type, pH, temperature, rainfall "
        "expectation, and water availability."
    )

    st.write("**Information still needed:**")
    st.write(
        "- Verified local crop suitability data\n"
        "- Actual weather forecast and planting season\n"
        "- Soil nutrient test (N, P, K)\n"
        "- Crop variety and irrigation details"
    )

    st.info(
        "No statistically calibrated confidence percentage "
        "is provided because the demo rules have not been "
        "validated against real farming outcomes."
    )

    st.header("4. Risk Warnings")

    if water == "Low" and ranked[0][0] == "Paddy":
        st.warning(
            "Water shortage may conflict with paddy's "
            "water needs. Check local irrigation conditions."
        )
    else:
        st.write(
            "Review the selected crop's local water, soil, "
            "weather, and seasonal requirements before planting."
        )

    if ph < 5.0 or ph > 8.0:
        st.warning(
            "This pH may restrict some crop options. "
            "Seek a soil test and local agricultural advice."
        )

    st.caption(
        "TrustFarm AI prototype | Recommendations are "
        "demonstrations, not professional agricultural advice."
    )
