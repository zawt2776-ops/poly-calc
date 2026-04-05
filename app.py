import streamlit as st
import pandas as pd

st.set_page_config(page_title="Poly Recovery Matrix", page_icon="📊", layout="wide")

st.title("📊 Polymarket Recovery Matrix")
st.markdown("Automated calculations to turn a losing position into a profit.")

# --- 1. CURRENT POSITION ---
st.header("1. Your Current Investment")
col1, col2 = st.columns(2)

with col1:
    avg_up = st.number_input("Avg Odd (UP)", value=0.70, format="%.2f")
    shares_up = st.number_input("Shares Owned (UP)", value=285.0, step=1.0)
    spent_up = avg_up * shares_up

with col2:
    avg_down = st.number_input("Avg Odd (DOWN)", value=0.35, format="%.2f")
    shares_down = st.number_input("Shares Owned (DOWN)", value=285.0, step=1.0)
    spent_down = avg_down * shares_down

total_invested = spent_up + spent_down
st.divider()

# --- 2. CURRENT P&L STATUS ---
st.header("2. Current P&L (If Match Ended Now)")
pnl_up = shares_up - total_invested
pnl_down = shares_down - total_invested

c1, c2 = st.columns(2)
c1.metric("If UP Wins", f"${shares_up:,.2f}", f"{pnl_up:,.2f} P/L", delta_color="normal" if pnl_up >=0 else "inverse")
c2.metric("If DOWN Wins", f"${shares_down:,.2f}", f"{pnl_down:,.2f} P/L", delta_color="normal" if pnl_down >=0 else "inverse")

# --- 3. RECOVERY MATRIX ---
st.header("3. Buy-Back Strategy Matrix")
st.write("Find the current market price below to see how much more to buy to reach your profit goal.")

profit_target = st.select_slider("Target Profit Goal ($)", options=[0, 10, 20, 50, 100], value=20)

# Determine which sides need help (if shares < total_invested + profit_target)
sides_to_calc = []
if shares_up < (total_invested + profit_target): sides_to_calc.append("UP")
if shares_down < (total_invested + profit_target): sides_to_calc.append("DOWN")

if not sides_to_calc:
    st.success(f"✅ You are already in a ${profit_target} profit position for both sides!")
else:
    tabs = st.tabs([f"Recovery for {side}" for side in sides_to_calc])
    
    for i, side in enumerate(sides_to_calc):
        with tabs[i]:
            current_side_shares = shares_up if side == "UP" else shares_down
            
            data = []
            # Calculate for odds 0.05 to 0.95
            for odd_int in range(5, 100, 5):
                odd = odd_int / 100.0
                # Formula: (CurrentShares + NewShares) * 1.0 = TotalInvested + (NewShares * odd) + ProfitTarget
                # NewShares = (TotalInvested + ProfitTarget - CurrentShares) / (1 - odd)
                needed_shares = (total_invested + profit_target - current_side_shares) / (1.0 - odd)
                cost = needed_shares * odd
                
                data.append({
                    "Market Price (Odd)": f"{odd:.2f}",
                    "Shares to Buy": f"{needed_shares:,.2f}",
                    "Required Cash ($)": f"${cost:,.2f}",
                    "Total Position If Won": f"${current_side_shares + needed_shares:,.2f}"
                })
            
            df = pd.DataFrame(data)
            st.table(df)

st.caption("Note: 'Required Cash' accounts for the fact that buying more shares increases your total investment.")
