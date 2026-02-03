import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt

FILE_NAME = "expense.txt"

# ============================
# Page config
# ============================
st.set_page_config(
    page_title="🧚🏻 Expense Tracker",
    page_icon="💰",
    layout="centered"
)

# ============================
# CSS (ALL UI FIXED & UNIFORM)
# ============================
st.markdown("""
<style>
/* ===== Background ===== */
.stApp {
  background: #fff7fa;
}

/* ===== Typography ===== */
h1, h2, h3 {
  color: #d81b60 !important;
  font-weight: 800 !important;
}
p, label, span {
  color: #333333 !important;
}

/* ===== Variables ===== */
:root{
  --border: #f2a1c2;     /* pink border */
  --border_focus: #ec407a;
  --bg: #ffffff;         /* box background */
  --txt: #000000;        /* text color */
  --radius: 14px;
  --height: 46px;
  --font: 16px;
  --padx: 14px;
}

/* ==================================================
   ONE STYLE FOR ALL INPUT BOXES (TEXT / DATE / SELECT)
   ================================================== */

/* Text + Date input */
.stTextInput input,
.stDateInput input {
  height: var(--height) !important;
  background: var(--bg) !important;
  color: var(--txt) !important;
  caret-color: var(--txt) !important;

  border: 2px solid var(--border) !important;
  border-radius: var(--radius) !important;

  padding: 0 var(--padx) !important;
  font-size: var(--font) !important;

  box-shadow: none !important;
}

/* Placeholder */
.stTextInput input::placeholder,
.stDateInput input::placeholder {
  color: #888888 !important;
  opacity: 1 !important;
}

/* Selectbox main box */
.stSelectbox div[data-baseweb="select"] > div {
  height: var(--height) !important;
  background: var(--bg) !important;

  border: 2px solid var(--border) !important;
  border-radius: var(--radius) !important;

  padding: 0 var(--padx) !important;
  font-size: var(--font) !important;

  display: flex !important;
  align-items: center !important;

  box-shadow: none !important;
}

/* Selectbox text (selected value + placeholder) */
.stSelectbox div[data-baseweb="select"] span,
.stSelectbox div[data-baseweb="select"] div {
  color: var(--txt) !important;
  font-size: var(--font) !important;
}

/* ===== Focus glow ===== */
.stTextInput input:focus,
.stDateInput input:focus,
.stSelectbox div[data-baseweb="select"] > div:focus-within {
  border-color: var(--border_focus) !important;
  box-shadow: 0 0 0 3px rgba(236, 64, 122, 0.15) !important;
  outline: none !important;
}

/* ==========================
   Selectbox dropdown (popup)
   ========================== */
.stSelectbox div[data-baseweb="popover"] > div {
  background: #ffffff !important;
  border: 2px solid var(--border) !important;
  border-radius: 12px !important;
  box-shadow: 0 14px 34px rgba(244,143,177,0.25) !important;
}

/* Menu list */
.stSelectbox div[data-baseweb="menu"] {
  background: #ffffff !important;
}

/* Options */
.stSelectbox div[data-baseweb="option"] {
  background: #ffffff !important;
  color: #000000 !important;
}

/* Hover */
.stSelectbox div[data-baseweb="option"]:hover {
  background: #fff0f6 !important;
}

/* Selected row */
.stSelectbox div[aria-selected="true"] {
  background: #f8bbd0 !important;
  color: #000000 !important;
}

/* ==========================
   Button (pink)
   ========================== */
.stButton > button,
div[data-testid="stFormSubmitButton"] > button {
  background: #f48fb1 !important;
  color: #000000 !important;
  border: none !important;
  border-radius: 14px !important;
  font-weight: 800 !important;
  padding: 10px 22px !important;
  box-shadow: 0 10px 22px rgba(244,143,177,0.22) !important;
}

.stButton > button:hover,
div[data-testid="stFormSubmitButton"] > button:hover {
  background: #ec407a !important;
  color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)


# ============================
# Helpers
# ============================
def ensure_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w"):
            pass

def load_expenses():
    if not os.path.exists(FILE_NAME):
        return pd.DataFrame(columns=["Amount", "Category", "Date"])

    rows = []
    with open(FILE_NAME, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) != 3:
                continue
            amount_str, cat, date_str = parts
            try:
                amount = float(amount_str)
            except ValueError:
                continue
            date = pd.to_datetime(date_str, errors="coerce")
            if pd.isna(date):
                continue
            rows.append({"Amount": amount, "Category": cat, "Date": date})

    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.sort_values("Date", ascending=False)
    return df

def get_categories(df):
    if df.empty:
        return []
    return sorted(df["Category"].unique().tolist())

def save_expense(amount, category, date):
    ensure_file()
    with open(FILE_NAME, "a") as f:
        f.write(f"{amount},{category},{date}\n")

# ============================
# UI
# ============================
st.title("Expense Tracker 💕")
st.write("Let’s track your daily expenses nicely ✨")

df = load_expenses()

# ============================
# Add Expense
# ============================
st.header("➕ Add New Expense")

with st.form("add_expense_form"):
    amount_text = st.text_input("Enter amount", placeholder="e.g. 10000")

    category_choice = st.selectbox(
        "Choose an existing category",
        ["-- Select --"] + get_categories(df)
    )

    new_category = st.text_input(
        "Or add a new category",
        placeholder="e.g. Rent, Cafe"
    )

    date_value = st.date_input("Date")

    submitted = st.form_submit_button("Add New Expense")

if submitted:
    category_final = new_category.strip() if new_category.strip() else category_choice

    if not amount_text.strip():
        st.warning("Please enter an amount.")
    elif not category_final or category_final == "-- Select --":
        st.warning("Please select or type a category.")
    else:
        try:
            amount = float(amount_text)
            if amount <= 0:
                st.warning("Amount must be greater than 0.")
            else:
                save_expense(amount, category_final, date_value)
                st.success("Expense successfully added! 💖")
                st.rerun()
        except ValueError:
            st.error("Amount must be a number.")

st.markdown("---")

df = load_expenses()

# ============================
# View All Expenses (Table)
# ============================
st.header("📜 View All Expenses")

if df.empty:
    st.info("No expenses yet!")
else:
    filter_cat = st.selectbox(
        "Filter by category",
        ["All"] + get_categories(df)
    )

    view_df = df if filter_cat == "All" else df[df["Category"] == filter_cat]

    view_df = view_df.copy()
    view_df["Date"] = view_df["Date"].dt.strftime("%Y-%m-%d")
    view_df["Amount (₩)"] = view_df["Amount"].map(lambda x: f"{x:,.0f}")

    st.dataframe(
        view_df[["Date", "Category", "Amount (₩)"]],
        use_container_width=True,
        hide_index=True
    )

st.markdown("---")

# ============================
# Total Spent
# ============================
st.header("🧾 Total Spent")

if df.empty:
    st.info("No data to calculate.")
else:
    st.success(f"Total Spent: **{df['Amount'].sum():,.0f}₩**")

st.markdown("---")

# ============================
# Pie Chart (Pastel)
# ============================
st.header("📊 Spending by Category")

if df.empty:
    st.info("No expenses found.")
else:
    totals = df.groupby("Category")["Amount"].sum().sort_values(ascending=False)

    pastel_colors = [
        "#f8bbd0", "#f48fb1", "#ce93d8",
        "#b39ddb", "#9fa8da", "#90caf9",
        "#a5d6a7", "#ffe082"
    ]

    fig, ax = plt.subplots()
    ax.pie(
        totals.values,
        labels=totals.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=pastel_colors[:len(totals)]
    )
    ax.axis("equal")
    st.pyplot(fig)

st.markdown("____")
st.caption("Made with love by Yuri 💌")
