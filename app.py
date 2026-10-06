"""
app.py - Streamlit Web Application for Swapi Water Tanker
Deployable directly to Streamlit Community Cloud for free.
"""

import streamlit as st
import time
from tanker_core import VALID_DENOMINATIONS, DEFAULT_TANK_CAPACITY

# Set page configuration
st.set_page_config(
    page_title="Swapi Water Tanker",
    page_icon="💧",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(135deg, #0284c7, #0369a1);
        color: white;
        padding: 24px;
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    }
    .main-header h1 {
        color: white !important;
        margin-bottom: 0px;
    }
    .tank-card {
        background-color: #f0fdf4;
        border: 1px solid #bbf7d0;
        padding: 16px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .receipt-box {
        background-color: #f8fafc;
        border: 2px dashed #0284c7;
        padding: 16px;
        border-radius: 10px;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "capacity" not in st.session_state:
    st.session_state.capacity = DEFAULT_TANK_CAPACITY
if "current_water" not in st.session_state:
    st.session_state.current_water = DEFAULT_TANK_CAPACITY
if "total_dispensed" not in st.session_state:
    st.session_state.total_dispensed = 0
if "history" not in st.session_state:
    st.session_state.history = []
if "selected_amount" not in st.session_state:
    st.session_state.selected_amount = 5

# Header
st.markdown("""
<div class="main-header">
    <h1>💧 Swapi Water Tanker</h1>
    <p style="margin: 0; font-size: 1.1rem; opacity: 0.95;">Automated Pure Water Dispensing Station</p>
</div>
""", unsafe_allow_html=True)

# Metrics Dashboard
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Tank Water Level", f"{st.session_state.current_water} L", delta=f"{st.session_state.current_water}/{st.session_state.capacity} L")
with col2:
    st.metric("Total Dispensed", f"{st.session_state.total_dispensed} L")
with col3:
    st.metric("Pricing Rate", "₹1 / Litre")

# Visual Water Level Indicator
tank_pct = max(0.0, min(1.0, st.session_state.current_water / st.session_state.capacity))
st.write(f"**Tank Storage Capacity: {int(tank_pct * 100)}% Full**")
st.progress(tank_pct)

st.divider()

# Coin Presets Section
st.subheader("🪙 Select Coin / Amount")
preset_cols = st.columns(len(VALID_DENOMINATIONS))

for i, denom in enumerate(VALID_DENOMINATIONS):
    with preset_cols[i]:
        if st.button(f"₹{denom}\n({denom}L)", key=f"btn_{denom}", use_container_width=True):
            st.session_state.selected_amount = denom

# Custom or selected amount input
selected_amt = st.number_input(
    "Or Enter Custom Litres:",
    min_value=1,
    max_value=max(1, st.session_state.current_water),
    value=min(st.session_state.selected_amount, max(1, st.session_state.current_water)),
    step=1
)

# Action Buttons: Dispense & Refill
btn_col1, btn_col2 = st.columns([3, 1])

with btn_col1:
    dispense_clicked = st.button("▶ START DISPENSING", type="primary", use_container_width=True)

with btn_col2:
    if st.button("🔄 Refill Tank", use_container_width=True):
        added = st.session_state.capacity - st.session_state.current_water
        st.session_state.current_water = st.session_state.capacity
        st.success(f"Tank refilled with {added} Litres! Now at 100% capacity.")
        st.rerun()

# Dispensing Logic
if dispense_clicked:
    if selected_amt > st.session_state.current_water:
        st.error(f"Insufficient water! Only {st.session_state.current_water}L available in tanker.")
    else:
        st.info(f"Dispensing {selected_amt} Litre(s)... Please place your container under the nozzle.")
        dispense_bar = st.progress(0)
        status_text = st.empty()

        # Dispense animation
        step_delay = 0.15 if selected_amt <= 10 else 0.05
        for litre in range(1, selected_amt + 1):
            time.sleep(step_delay)
            pct = litre / selected_amt
            dispense_bar.progress(pct)
            status_text.text(f"Dispensing: {litre} / {selected_amt} Litres ({int(pct * 100)}%)")

        # Update state
        st.session_state.current_water -= selected_amt
        st.session_state.total_dispensed += selected_amt
        st.session_state.history.append({
            "Time": time.strftime("%H:%M:%S"),
            "Amount": f"₹{selected_amt}",
            "Litres": f"{selected_amt} L",
            "Tank Left": f"{st.session_state.current_water} L"
        })

        st.balloons()
        st.success("✔ Dispensing Completed Successfully!")

        # Formatted Receipt
        st.markdown(f"""
        <div class="receipt-box">
            <h4 style="margin-top:0; color:#0284c7;">🧾 Dispense Receipt</h4>
            <p><strong>Water Dispensed:</strong> {selected_amt} Litre(s)</p>
            <p><strong>Total Paid:</strong> ₹{selected_amt}</p>
            <p><strong>Tank Remaining:</strong> {st.session_state.current_water} Litres</p>
            <p style="margin-bottom:0; color:#059669;"><em>Thanks for visiting Swapi Water Tanker! 💧</em></p>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(1)
        st.rerun()

# Transaction History Log
if st.session_state.history:
    st.divider()
    with st.expander("📋 View Transaction History", expanded=False):
        st.table(list(reversed(st.session_state.history)))
