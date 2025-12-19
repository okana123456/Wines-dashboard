import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Nairobi Wine & Spirits Analytics",
    page_icon="🍷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Raleway:wght@300;400;600;700&display=swap');
    
    /* Main theme colors */
    :root {
        --primary: #8B1538;
        --secondary: #C7A252;
        --background: #FDF8F3;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom header */
    .main-header {
        background: linear-gradient(135deg, #8B1538 0%, #6B1028 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(139, 21, 56, 0.3);
    }
    
    .main-header h1 {
        font-family: 'Playfair Display', serif;
        color: white;
        margin: 0;
        font-size: 2.5rem;
        font-weight: 900;
    }
    
    .main-header p {
        color: #C7A252;
        margin: 0.5rem 0 0 0;
        font-size: 1rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        font-weight: 300;
    }
    
    /* Metric cards */
    div[data-testid="metric-container"] {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        border-left: 4px solid #C7A252;
    }
    
    div[data-testid="metric-container"] > label {
        color: #666 !important;
        font-size: 0.85rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    
    div[data-testid="metric-container"] > div {
        color: #8B1538 !important;
        font-family: 'Playfair Display', serif !important;
        font-weight: 700 !important;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FDF8F3 0%, #F5EDE3 100%);
    }
    
    section[data-testid="stSidebar"] > div {
        padding: 2rem 1rem;
    }
    
    /* Alerts */
    .alert-warning {
        background: linear-gradient(90deg, rgba(245, 124, 0, 0.1), white);
        border-left: 4px solid #F57C00;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    .alert-danger {
        background: linear-gradient(90deg, rgba(211, 47, 47, 0.1), white);
        border-left: 4px solid #D32F2F;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    .alert-success {
        background: linear-gradient(90deg, rgba(46, 125, 50, 0.1), white);
        border-left: 4px solid #2E7D32;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #8B1538, #6B1028);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(139, 21, 56, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Load data with caching
@st.cache_data
def load_data():
    df_sales = pd.read_csv('sales_data.csv')
    df_sales['date'] = pd.to_datetime(df_sales['date'])
    df_sales['date_only'] = pd.to_datetime(df_sales['date_only'])
    
    df_inventory = pd.read_csv('inventory_data.csv')
    df_inventory['expiry_date'] = pd.to_datetime(df_inventory['expiry_date'])
    
    return df_sales, df_inventory

# Load data
try:
    df_sales, df_inventory = load_data()
except:
    st.error("⚠️ Data files not found. Please ensure sales_data.csv and inventory_data.csv are in the same directory.")
    st.stop()

# Header
st.markdown("""
<div class="main-header">
    <h1>🍷 Nairobi Wine & Spirits</h1>
    <p>Business Intelligence Dashboard</p>
</div>
""", unsafe_allow_html=True)

# Sidebar filters
with st.sidebar:
    st.markdown("### 📊 Dashboard Controls")
    
    # Time period filter
    time_period = st.selectbox(
        "Select Time Period",
        ["Last 7 Days", "Last 30 Days", "Last 90 Days", "All Time"],
        index=1
    )
    
    # Category filter
    categories = ['All Categories'] + sorted(df_sales['category'].unique().tolist())
    category_filter = st.selectbox(
        "Select Category",
        categories
    )
    
    st.markdown("---")
    st.markdown("### 📱 Mobile Optimized")
    st.markdown("This dashboard works perfectly on phones!")
    
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
    **Features:**
    - Real-time analytics
    - Inventory alerts
    - Employee tracking
    - Mobile responsive
    """)

# Filter data based on selections
# Time filter
if time_period == "Last 7 Days":
    days = 7
elif time_period == "Last 30 Days":
    days = 30
elif time_period == "Last 90 Days":
    days = 90
else:
    days = None

if days:
    cutoff_date = datetime.now() - timedelta(days=days)
    df_filtered = df_sales[df_sales['date'] >= cutoff_date].copy()
    
    # For comparison
    prev_cutoff = datetime.now() - timedelta(days=days*2)
    prev_end = datetime.now() - timedelta(days=days)
    df_prev = df_sales[(df_sales['date'] >= prev_cutoff) & (df_sales['date'] < prev_end)].copy()
else:
    df_filtered = df_sales.copy()
    df_prev = pd.DataFrame()

# Category filter
if category_filter != 'All Categories':
    df_filtered = df_filtered[df_filtered['category'] == category_filter]
    if not df_prev.empty:
        df_prev = df_prev[df_prev['category'] == category_filter]

# Calculate metrics
total_revenue = df_filtered['total_price'].sum()
total_profit = df_filtered['profit'].sum()
profit_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0
total_transactions = len(df_filtered)

# Calculate changes
if not df_prev.empty:
    prev_revenue = df_prev['total_price'].sum()
    revenue_change = ((total_revenue - prev_revenue) / prev_revenue * 100) if prev_revenue > 0 else 0
else:
    revenue_change = 0

# Key Metrics
st.markdown("### 📈 Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Revenue",
        f"KES {total_revenue:,.0f}",
        f"{revenue_change:+.1f}%" if days else None
    )

with col2:
    st.metric(
        "Total Profit",
        f"KES {total_profit:,.0f}",
        f"{profit_margin:.1f}% margin"
    )

with col3:
    st.metric(
        "Transactions",
        f"{total_transactions:,}",
        f"KES {total_revenue/total_transactions:,.0f} avg" if total_transactions > 0 else "0"
    )

with col4:
    if len(df_filtered) > 0:
        best_seller = df_filtered.groupby('product_name')['quantity'].sum().idxmax()
        best_seller_qty = df_filtered.groupby('product_name')['quantity'].sum().max()
        st.metric(
            "Best Seller",
            best_seller[:20] + "..." if len(best_seller) > 20 else best_seller,
            f"{best_seller_qty:,.0f} units"
        )
    else:
        st.metric("Best Seller", "N/A", "0 units")

st.markdown("---")

# Revenue Trend
st.markdown("### 💰 Revenue & Profit Trend")
daily_revenue = df_filtered.groupby('date_only').agg({
    'total_price': 'sum',
    'profit': 'sum'
}).reset_index()

fig_revenue = go.Figure()
fig_revenue.add_trace(go.Scatter(
    x=daily_revenue['date_only'],
    y=daily_revenue['total_price'],
    mode='lines',
    name='Revenue',
    line=dict(color='#8B1538', width=3),
    fill='tonexty',
    fillcolor='rgba(139, 21, 56, 0.1)'
))
fig_revenue.add_trace(go.Scatter(
    x=daily_revenue['date_only'],
    y=daily_revenue['profit'],
    mode='lines',
    name='Profit',
    line=dict(color='#C7A252', width=3, dash='dot')
))
fig_revenue.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    height=400,
    hovermode='x unified',
    margin=dict(l=20, r=20, t=20, b=20),
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
)
st.plotly_chart(fig_revenue, use_container_width=True)

st.markdown("---")

# Two columns for charts
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🏆 Top Selling Products")
    top_products = df_filtered.groupby('product_name').agg({
        'total_price': 'sum',
        'quantity': 'sum'
    }).sort_values('total_price', ascending=False).head(10)
    
    fig_top_products = go.Figure(go.Bar(
        x=top_products['total_price'],
        y=top_products.index,
        orientation='h',
        marker=dict(
            color=top_products['total_price'],
            colorscale=[[0, '#5D4037'], [0.5, '#8B1538'], [1, '#C7A252']],
            showscale=False
        ),
        text=[f'KES {val:,.0f}' for val in top_products['total_price']],
        textposition='outside'
    ))
    fig_top_products.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(showgrid=False, showticklabels=False),
        yaxis=dict(showgrid=False)
    )
    st.plotly_chart(fig_top_products, use_container_width=True)

with col2:
    st.markdown("### 📊 Sales by Category")
    category_sales = df_filtered.groupby('category')['total_price'].sum().sort_values(ascending=False)
    
    fig_category = go.Figure(go.Pie(
        labels=category_sales.index,
        values=category_sales.values,
        hole=0.5,
        marker=dict(colors=['#8B1538', '#C7A252', '#5D4037', '#AD7A56', '#6B2C45', '#2C1810']),
        textinfo='label+percent',
        textfont=dict(size=12, color='white'),
        hovertemplate='<b>%{label}</b><br>Revenue: KES %{value:,.0f}<br>Share: %{percent}<extra></extra>'
    ))
    fig_category.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400,
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=True,
        legend=dict(orientation='v', yanchor='middle', y=0.5)
    )
    st.plotly_chart(fig_category, use_container_width=True)

st.markdown("---")

# Another row of charts
col1, col2 = st.columns(2)

with col1:
    st.markdown("### ⏰ Peak Hours Analysis")
    hourly_sales = df_filtered.groupby('hour')['total_price'].sum().reset_index()
    
    fig_hourly = go.Figure(go.Bar(
        x=hourly_sales['hour'],
        y=hourly_sales['total_price'],
        marker=dict(
            color=hourly_sales['total_price'],
            colorscale=[[0, '#5D4037'], [0.5, '#8B1538'], [1, '#C7A252']],
            showscale=False
        ),
        text=[f'KES {val/1000:.0f}K' for val in hourly_sales['total_price']],
        textposition='outside'
    ))
    fig_hourly.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=350,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(title='Hour of Day', showgrid=False, tickmode='linear', tick0=0, dtick=2),
        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)', showticklabels=False)
    )
    st.plotly_chart(fig_hourly, use_container_width=True)

with col2:
    st.markdown("### 👥 Employee Performance")
    employee_sales = df_filtered.groupby('employee').agg({
        'total_price': 'sum',
        'profit': 'sum'
    }).sort_values('total_price', ascending=False)
    
    fig_employee = go.Figure(go.Bar(
        x=employee_sales.index,
        y=employee_sales['total_price'],
        marker=dict(color='#8B1538'),
        text=[f'KES {val/1000:.0f}K' for val in employee_sales['total_price']],
        textposition='outside'
    ))
    fig_employee.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=350,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(showgrid=False, tickangle=-45),
        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)', showticklabels=False)
    )
    st.plotly_chart(fig_employee, use_container_width=True)

st.markdown("---")

# Inventory Alerts
st.markdown("### 🔔 Inventory Alerts")

low_stock = df_inventory[df_inventory['current_stock'] < df_inventory['reorder_level']]
expiring_soon = df_inventory[df_inventory['days_to_expiry'] <= 30]

if len(low_stock) > 0 or len(expiring_soon) > 0:
    col1, col2 = st.columns(2)
    
    with col1:
        if len(low_stock) > 0:
            st.markdown("#### ⚠️ Low Stock Items")
            for _, row in low_stock.iterrows():
                st.markdown(f"""
                <div class="alert-warning">
                    <strong>⚠️ {row['product_name']}</strong><br>
                    Current: {row['current_stock']} units | Reorder Level: {row['reorder_level']} units
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="alert-success">
                <strong>✅ All Stock Levels Healthy!</strong>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if len(expiring_soon) > 0:
            st.markdown("#### 🕒 Expiring Soon")
            for _, row in expiring_soon.iterrows():
                st.markdown(f"""
                <div class="alert-danger">
                    <strong>🕒 {row['product_name']}</strong><br>
                    Expires in {row['days_to_expiry']} days | Stock: {row['current_stock']} units
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="alert-success">
                <strong>✅ No Items Expiring Soon!</strong>
            </div>
            """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="alert-success">
        <strong>✅ All Inventory Levels Are Healthy!</strong><br>
        No low stock or expiring items detected.
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Inventory Status
st.markdown("### 📦 Current Inventory Status")
df_inv_sorted = df_inventory.sort_values('current_stock', ascending=False).head(15)

fig_inventory = go.Figure()

fig_inventory.add_trace(go.Bar(
    x=df_inv_sorted['product_name'],
    y=df_inv_sorted['current_stock'],
    name='Current Stock',
    marker=dict(color='#8B1538'),
    text=df_inv_sorted['current_stock'],
    textposition='outside'
))

fig_inventory.add_trace(go.Scatter(
    x=df_inv_sorted['product_name'],
    y=df_inv_sorted['reorder_level'],
    name='Reorder Level',
    mode='markers',
    marker=dict(color='#C7A252', size=10, symbol='diamond')
))

fig_inventory.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    height=400,
    margin=dict(l=20, r=20, t=20, b=80),
    xaxis=dict(showgrid=False, tickangle=-45),
    yaxis=dict(title='Units', showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
)
st.plotly_chart(fig_inventory, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p style='font-size: 1.2rem; font-weight: 600; color: #8B1538;'>🍷 Nairobi Wine & Spirits Dashboard</p>
    <p style='font-size: 0.9rem;'>Built with ❤️ for Business Intelligence</p>
    <p style='font-size: 0.8rem; margin-top: 1rem;'>
        📱 Mobile Optimized | 🔄 Real-time Updates | 📊 Actionable Insights
    </p>
</div>
""", unsafe_allow_html=True)
