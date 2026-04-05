import streamlit as st
import pandas as pd

st.set_page_config(page_title="Poly Recovery Pro", page_icon="📈", layout="wide")

st.title("📊 Polymarket Recovery & Profit Matrix")

# --- 1. CURRENT POSITION ---
st.header("1. Your Current Investment")
col1, col2 = st.columns(2)

with col1:
    avg_up = st.number_input("Avg Odd (UP)", value=0.70, format="%.2f")
    shares_up = st.number_input("Shares Owned (UP)", value=285.0, step=1.0)
    spent_up = avg_up * shares_up
    st.write(f"Invested in UP: **${spent_up:,.2f}**")

with col2:
    avg_down = st.number_input("Avg Odd (DOWN)", value=0.35, format="%.2f")
    shares_down = st.number_input("Shares Owned (DOWN)", value=285.0, step=1.0)
    spent_down = avg_down * shares_down
    st.write(f"Invested in DOWN: **${spent_down:,.2f}**")

total_invested_prev = spent_up + spent_down
st.info(f"**Total Invested (Previous):** ${total_invested_prev:,.2f}")
st.divider()

# --- 2. STATUS CHECK ---
st.header("2. Current P&L (Before Buying More)")
pnl_up = shares_up - total_invested_prev
pnl_down = shares_down - total_invested_prev

c1, c2 = st.columns(2)
c1.metric("If UP Wins", f"${shares_up:,.2f}", f"{pnl_up:,.2f} P/L", delta_color="normal" if pnl_up >=0 else "inverse")
c2.metric("If DOWN Wins", f"${shares_down:,.2f}", f"{pnl_down:,.2f} P/L", delta_color="normal" if pnl_down >=0 else "inverse")

# --- 3. RECOVERY MATRIX ---
st.header("3. Strategy Matrix")
profit_target = st.select_slider("Target Profit Goal ($)", options=[0, 10, 20, 50, 100], value=20)

# Check which sides are below target
sides_to_calc = []
if shares_up < (total_invested_prev + profit_target): sides_to_calc.append("UP")
if shares_down < (total_invested_prev + profit_target): sides_to_calc.append("DOWN")

if not sides_to_calc:
    st.success(f"✅ You already have at least ${profit_target} profit on both sides!")
else:
    tabs = st.tabs([f"Buy for {side}" for side in sides_to_calc])
    
    for i, side in enumerate(sides_to_calc):
        with tabs[i]:
            current_shares = shares_up if side == "UP" else shares_down
            matrix_data = []
            
            for odd_int in range(5, 100, 5):
                odd = odd_int / 100.0
                # Formula: NewShares = (TotalInvestedPrev + ProfitTarget - CurrentShares) / (1.0 - odd)
                needed_shares = (total_invested_prev + profit_target - current_shares) / (1.0 - odd)
                cost = needed_shares * odd
                total_invested_new = total_invested_prev + cost
                total_shares_new = current_shares + needed_shares
                final_profit = total_shares_new - total_invested_new
                
                matrix_data.append({
                    "Market Price (Odd)": f"{odd:.2f}",
                    "Shares to Buy (Total)": f"{needed_shares:,.2f} ({total_shares_new:,.2f})",
                    "Required Cash (Total Inv)": f"${cost:,.2f} (${total_invested_new:,.2f})",
                    "Profit Equation (Payout - Total Inv)": f"${total_shares_new:,.2f} - ${total_invested_new:,.2f} = ${final_profit:,.2f}"
                })
            
            st.table(pd.DataFrame(matrix_data))

st.caption("Calculation Logic: The equation shows your Total Payout (1:1) minus your Total cumulative investment to verify the profit.")
