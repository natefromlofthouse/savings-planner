import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Savings Planner", layout="centered")
st.title("📊 Savings Calculator for Studying Abroad")

# Inputs
annual_income = st.slider("Annual Income (USD)", min_value=20000, max_value=100000, value=50000, step=1000)
monthly_expenses = st.slider("Total Monthly Expenses (USD)", min_value=500, max_value=5000, value=1500, step=100)
save_percent = st.slider("Percentage of Post-Tax Income to Save (%)", min_value=0, max_value=100, value=20, step=1)

# Tax estimate
estimated_tax_rate = 0.20
post_tax_income = annual_income * (1 - estimated_tax_rate)
monthly_post_tax_income = post_tax_income / 12

# Monthly savings calculations
monthly_savings_from_percent = monthly_post_tax_income * (save_percent / 100)
monthly_net_savings = monthly_post_tax_income - monthly_expenses
actual_monthly_savings = min(monthly_net_savings, monthly_savings_from_percent)
total_savings = actual_monthly_savings * 12

# Emoji logic
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

# Results
st.markdown("### 💰 Results")
st.write(f"**Post-Tax Monthly Income**: ${monthly_post_tax_income:,.2f}")
st.write(f"**Estimated Monthly Savings**: ${actual_monthly_savings:,.2f}")
st.success(f"🎯 **Estimated Total Savings in One Year**: ${total_savings:,.2f} {rating}")

if monthly_net_savings <= 0:
    st.warning("⚠️ Your expenses exceed or match your income. Consider reducing your costs.")
elif total_savings < 8581:
    st.info("📌 Note: You may need at least $8,581 saved to qualify for your French student visa.")

# Visualization
months = [f"Month {i+1}" for i in range(12)]
monthly_savings_data = [actual_monthly_savings for _ in range(12)]
cumulative_savings = pd.DataFrame({
    "Month": months,
    "Cumulative Savings ($)": [actual_monthly_savings * (i + 1) for i in range(12)]
})

st.markdown("### 📈 Savings Growth Over the Year")
fig, ax = plt.subplots()
ax.plot(cumulative_savings["Month"], cumulative_savings["Cumulative Savings ($)"], marker='o')
ax.set_ylabel("USD")
ax.set_xlabel("Month")
ax.set_title("Cumulative Savings Over 12 Months")
plt.xticks(rotation=45)
plt.grid(True)
st.pyplot(fig)
