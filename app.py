import streamlit as st

st.set_page_config(page_title="Poly Rescue & Profit", page_icon="💰")

st.title("💰 Poly Profit & Rescue Pro")
st.markdown("Calculate how much to buy to hit a **specific profit target**.")

# --- INPUT SECTION ---
st.header("1. Current Position")
col1, col2 = st.columns(2)

with col1:
    avg_up = st.number_input("Avg Odd (UP)", value=0.70, format="%.2f")
    shares_up = st.number_input("Shares Owned (UP)", value=285.0, step=1.0)

with col2:
    avg_down = st.number_input("Avg Odd (DOWN)", value=0.35, format="%.2f")
    shares_down = st.number_input("Shares Owned (DOWN)", value=285.0, step=1.0)

total_spent = (avg_up * shares_up) + (avg_down * shares_down)
st.metric("Total Invested", f"${total_spent:,.2f}")

# --- PROFIT TARGET ---
st.header("2. Set Your Goal")
target_side = st.radio("Which side are you backing?", ["UP", "DOWN"], horizontal=True)
current_market_odd = st.number_input(f"Current {target_side} Price (Odd)", value=0.75 if target_side == "UP" else 0.40, format="%.2f")
profit_goal = st.number_input("Desired Profit ($)", value=20.0, step=5.0)

# --- CALCULATION ---
# Total Payout Needed = Total Spent + New Cost + Profit Goal
# Shares * 1.0 = Total Spent + (New Shares * Price) + Profit Goal
# New Shares = (Total Spent + Profit Goal - Current Shares) / (1 - Price)

current_shares = shares_up if target_side == "UP" else shares_down
numerator = total_spent + profit_goal - current_shares
denominator = 1.0 - current_market_odd

if denominator <= 0:
    st.error("Price cannot be 1.0 or higher!")
else:
    shares_to_buy = numerator / denominator
    
    if shares_to_buy <= 0:
        actual_profit = current_shares - total_spent
        st.success(f"✅ You are already on track for ${actual_profit:,.2f} profit!")
    else:
        cost = shares_to_buy * current_market_odd
        st.subheader("🚀 Action Plan")
        st.write(f"To finish with **${profit_goal:,.2f} profit**:")
        st.warning(f"Buy **{shares_to_buy:,.2f}** more shares of **{target_side}**")
        st.info(f"**Total Cost to Buy:** ${cost:,.2f}")

# --- MERGE CALCULATOR ---
st.divider()
st.header("🧮 Merge Preview")
mergeable = min(shares_up, shares_down)
if st.button(f"Calculate Merge for {mergeable} pairs"):
    st.write(f"If you merge now, you get **${mergeable:,.2f}** cash back.")
    st.write(f"Remaining: **{shares_up - mergeable} UP** and **{shares_down - mergeable} DOWN**.")
