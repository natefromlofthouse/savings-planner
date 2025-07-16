import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page config for dark mode aesthetic
st.set_page_config(
    page_title="Savings Planner",
    layout="centered",
    page_icon="💸"
)

# Custom dark theme tweaks
st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        background-color: #111111;
        color: #EEEEEE;
        font-family: 'Segoe UI', sans-serif;
        font-size: 16px;
    }
    .stSlider > div {
        background-color: #222222;
        padding: 10px;
        border-radius: 8px;
    }
    .stButton button {
        background-color: #444444;
        color: #ffffff;
        border-radius: 8px;
    }
    .stMarkdown {
        padding-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Saving for Sciences Po")

# --- Inputs ---
annual_income = st.slider("Annual Income (USD)", 20000, 100000, 50000, step=1000)
tax_rate = st.slider("Estimated Tax Rate (%)", 0, 40, 20, step=1)

monthly_rent = st.slider("Monthly Rent (USD)", 300, 3000, 1000, step=50)
monthly_needs = st.slider("Monthly Needs (Groceries, Transport, etc.) (USD)", 100, 2000, 600, step=50)

# Post-tax income calculation
post_tax_income = annual_income * (1 - tax_rate / 100)
monthly_post_tax_income = post_tax_income / 12

# Discretionary and savings
discretionary_income = max(monthly_post_tax_income - monthly_rent - monthly_needs, 0)
savings_percent = st.slider("Percentage of Discretionary Income to Save (%)", 0, 100, 50, step=1)
actual_monthly_savings = discretionary_income * (savings_percent / 100)
total_savings = actual_monthly_savings * 12
wants = max(monthly_post_tax_income - (monthly_rent + monthly_needs + actual_monthly_savings), 0)

# Rating logic
def savings_emoji(savings):
    if savings < 8581:
        return "❌"
    elif 8581 <= savings < 10000:
        return "⭐"
    elif 10000 <= savings < 15000:
        return "⭐⭐"
    elif 15000 <= savings < 20000:
        return "⭐⭐⭐"
    elif 20000 <= savings <= 32200:
        return "⭐⭐⭐⭐"
    else:
        return "👑"

rating = savings_emoji(total_savings)

# --- Results Display ---
st.markdown("### Results")
st.write(f"**Post-Tax Monthly Income**: ${monthly_post_tax_income:,.2f}")
st.write(f"**Discretionary Income (after Rent & Needs)**: ${discretionary_income:,.2f}")
st.write(f"**Estimated Monthly Savings**: ${actual_monthly_savings:,.2f}")
st.success(f" **Estimated Total Savings in One Year**: ${total_savings:,.2f} {rating}")

if discretionary_income <= 0:
    st.warning("⚠️ You have no discretionary income left after rent and needs.")
elif total_savings < 8581:
    st.info("📌 Note: You may need at least $8,581 saved to qualify for your French student visa.")

# --- Pie Chart ---
labels = ['Rent', 'Needs', 'Savings', 'Wants']
amounts = [monthly_rent, monthly_needs, actual_monthly_savings, wants]
colors = ['#e7ecef', '#274c77', '#6096ba', '#a3cef1']

fig, ax = plt.subplots()
ax.pie(amounts, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors, textprops={'color': 'white'})
ax.axis('equal')
fig.patch.set_facecolor('#111111')
st.markdown("### 🧾 Monthly Spending Breakdown")
st.pyplot(fig)

st.markdown(f"**Wants (unallocated leftover): ${wants:,.2f}**")
