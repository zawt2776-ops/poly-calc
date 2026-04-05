import streamlit as st

st.set_page_config(page_title="Polymarket Rescue Calc", page_icon="📈")

st.title("🛡️ Polymarket Rescue Calculator")
st.markdown("Calculate how much more to buy to reach **Break Even**.")

# --- INPUT SECTION ---
st.header("Current Position")
col1, col2 = st.columns(2)

with col1:
    avg_up = st.number_input("Avg Odd (UP)", value=0.70, step=0.01)
    shares_up = st.number_input("Shares Owned (UP)", value=285.0, step=1.0)

with col2:
    avg_down = st.number_input("Avg Odd (DOWN)", value=0.35, step=0.01)
    shares_down = st.number_input("Shares Owned (DOWN)", value=285.0, step=1.0)

total_spent = (avg_up * shares_up) + (avg_down * shares_down)
st.info(f"**Total Invested So Far:** ${total_spent:,.2f}")

# --- CALCULATION SECTION ---
st.header("Rescue Plan")
target_side = st.selectbox("Which side do you think will win?", ["UP", "DOWN"])
current_market_odd = st.number_input(f"Current Market Odd for {target_side}", value=0.75 if target_side == "UP" else 0.40, step=0.01)

# Math: Total Spent = (Current Shares + New Shares) * 1.0
# New Shares = Total Spent - Current Shares
current_shares = shares_up if target_side == "UP" else shares_down
needed_shares = total_spent - current_shares

if needed_shares <= 0:
    st.success("✅ You are already in a profit position for this side!")
else:
    cost_to_buy = needed_shares * current_market_odd
    
    st.warning(f"⚠️ To break even on {target_side}:")
    st.metric(label="Additional Shares Needed", value=f"{needed_shares:,.2f}")
    st.metric(label="Estimated Cost (USD)", value=f"${cost_to_buy:,.2f}")
    
    st.write(f"**Final Result:** If you spend **${cost_to_buy:,.2f}**, your total payout will be **${total_spent + (needed_shares * (1.0 - current_market_odd)):,.2f}** which covers your total cost of **${total_spent + cost_to_buy:,.2f}**.")

st.divider()
st.caption("Note: This calculation assumes no trading fees and 1.0 payout per share.")
