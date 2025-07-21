import streamlit as st
import pandas as pd
import numpy as np
from data_simulation import simulate_data
from utils import calculate_roas, get_top_influencers
import plotly.express as px
import random

# Inject ultra-modern CSS and variables
st.markdown('''
    <style>
    :root {
      --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      --success-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
      --warning-gradient: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
      --glass-primary: rgba(255, 255, 255, 0.08);
      --glass-secondary: rgba(255, 255, 255, 0.04);
      --glass-border: rgba(255, 255, 255, 0.12);
      --bg-primary: #0a0b0d;
      --bg-secondary: #1a1d21;
      --bg-tertiary: #2a2d35;
      --neon-blue: #00d4ff;
      --neon-purple: #b794f6;
      --neon-green: #68d391;
      --neon-pink: #f093fb;
    }
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: var(--bg-primary);
        color: #f8fafc;
        line-height: 1.6;
    }
    header {
      position: fixed;
      top: 16px;
      left: 50%;
      transform: translateX(-50%);
      width: calc(100% - 32px);
      max-width: 1400px;
      height: 72px;
      background: rgba(10, 11, 13, 0.8);
      backdrop-filter: blur(24px) saturate(180%);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 20px;
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(255, 255, 255, 0.05) inset;
      z-index: 1000;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 2rem;
    }
    .logo {
      background: linear-gradient(135deg, #667eea, #764ba2);
      background-clip: text;
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      filter: drop-shadow(0 0 8px rgba(102, 126, 234, 0.3));
      animation: logoGlow 3s ease-in-out infinite;
      font-size: 2rem;
      font-weight: 700;
      letter-spacing: -0.01em;
    }
    @keyframes logoGlow {
      0%, 100% { filter: drop-shadow(0 0 8px rgba(102, 126, 234, 0.3)); }
      50% { filter: drop-shadow(0 0 16px rgba(102, 126, 234, 0.6)); }
    }
    .search-bar {
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 12px;
      backdrop-filter: blur(12px);
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      padding: 0.5rem 1rem;
      color: #fff;
      font-size: 1rem;
      width: 220px;
      margin-right: 1rem;
    }
    .search-bar:focus-within {
      background: rgba(255, 255, 255, 0.08);
      border-color: var(--neon-blue);
      box-shadow: 0 0 24px rgba(0, 212, 255, 0.2);
      transform: scale(1.02);
    }
    .avatar {
      width: 68px;
      height: 68px;
      border-radius: 20px;
      border: 2px solid transparent;
      background: linear-gradient(145deg, rgba(255,255,255,0.1), transparent);
      padding: 2px;
      position: relative;
      transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    .avatar:hover {
      transform: rotateY(15deg) rotateX(5deg) scale(1.05);
      box-shadow: 0 16px 32px rgba(0, 212, 255, 0.2);
    }
    .dashboard-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
      gap: 24px;
      padding: 120px 32px 32px;
      max-width: 1400px;
      margin: 0 auto;
    }
    .influencer-card {
      background: linear-gradient(145deg, rgba(255, 255, 255, 0.06) 0%, rgba(255, 255, 255, 0.02) 100%);
      backdrop-filter: blur(16px) saturate(180%);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 24px;
      padding: 24px;
      position: relative;
      overflow: hidden;
      transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12), 0 0 0 1px rgba(255, 255, 255, 0.05) inset;
      opacity: 0;
      transform: translateY(40px);
      animation: slideInUp 0.6s cubic-bezier(0.4, 0, 0.2, 1) forwards;
    }
    .influencer-card:nth-child(1) { animation-delay: 0.1s; }
    .influencer-card:nth-child(2) { animation-delay: 0.2s; }
    .influencer-card:nth-child(3) { animation-delay: 0.3s; }
    @keyframes slideInUp {
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }
    .influencer-card:hover {
      transform: translateY(-8px) scale(1.02);
      box-shadow: 0 24px 48px rgba(0, 0, 0, 0.2), 0 0 32px rgba(102, 126, 234, 0.1), 0 0 0 1px rgba(255, 255, 255, 0.1) inset;
      border-color: rgba(102, 126, 234, 0.3);
    }
    .platform-badge {
      background: rgba(0, 0, 0, 0.6);
      backdrop-filter: blur(8px);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 8px;
      padding: 4px 8px;
      font-size: 11px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-left: 8px;
    }
    .platform-badge.twitter { color: var(--neon-blue); border-color: rgba(0, 212, 255, 0.3); }
    .platform-badge.instagram { color: var(--neon-pink); border-color: rgba(240, 147, 251, 0.3); }
    .platform-badge.youtube { color: #fa709a; border-color: rgba(250, 112, 154, 0.3); }
    .roas-progress {
      width: 100%;
      height: 8px;
      background: rgba(255, 255, 255, 0.05);
      border-radius: 12px;
      overflow: hidden;
      position: relative;
      margin-top: 8px;
    }
    .roas-fill {
      height: 100%;
      background: linear-gradient(135deg, var(--neon-blue) 0%, var(--neon-purple) 100%);
      border-radius: 12px;
      position: relative;
      transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
      box-shadow: 0 0 12px rgba(0, 212, 255, 0.3), 0 0 24px rgba(0, 212, 255, 0.1);
    }
    .roas-value {
      font-size: 32px;
      font-weight: 700;
      background: linear-gradient(135deg, var(--neon-blue), var(--neon-purple));
      background-clip: text;
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      filter: drop-shadow(0 0 8px rgba(0, 212, 255, 0.3));
    }
    .action-button {
      background: rgba(255, 255, 255, 0.05);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 12px;
      padding: 12px 20px;
      font-weight: 600;
      color: white;
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      position: relative;
      overflow: hidden;
      margin-right: 8px;
    }
    .action-button:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 24px rgba(0, 212, 255, 0.2);
      border-color: var(--neon-blue);
    }
    .section-title {
      font-size: 32px;
      font-weight: 700;
      margin-bottom: 32px;
      display: flex;
      align-items: center;
      gap: 12px;
      background: linear-gradient(135deg, #ffffff, #a0aec0);
      background-clip: text;
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .section-title::before {
      content: '';
      width: 4px;
      height: 32px;
      background: linear-gradient(135deg, var(--neon-blue), var(--neon-purple));
      border-radius: 2px;
      box-shadow: 0 0 12px rgba(0, 212, 255, 0.4);
    }
    @media (max-width: 768px) {
      .dashboard-grid {
        grid-template-columns: 1fr;
        padding: 100px 16px 16px;
        gap: 16px;
      }
      .influencer-card {
        border-radius: 20px;
        padding: 20px;
      }
      header {
        top: 8px;
        width: calc(100% - 16px);
        height: 64px;
        border-radius: 16px;
      }
    }
    </style>
''', unsafe_allow_html=True)

# --- Responsive and perfectly aligned header with premium font ---
st.markdown('''
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
<style>
body, html, [class*="css"] {
  font-family: 'Inter', 'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}
@media (max-width: 900px) {
  .header-row { flex-direction: column !important; align-items: stretch !important; gap: 10px !important; }
  .header-logo { justify-content: center !important; font-size: 1.3rem !important; }
  .header-search { width: 100% !important; }
  .header-avatar { margin: 0 auto !important; }
}
.header-row { display: flex; align-items: center; justify-content: space-between; gap: 24px; margin-bottom: 0; }
.header-logo { font-size: 2.1rem; font-weight: 700; letter-spacing: -0.02em; background: linear-gradient(135deg,#667eea,#764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; display: flex; align-items: center; font-family: 'Poppins', 'Inter', sans-serif; }
.header-search { flex: 1; display: flex; align-items: center; }
.header-search input { width: 100%; min-width: 0; }
.header-avatar { width: 48px; height: 48px; border-radius: 50%; background: linear-gradient(135deg,#667eea,#764ba2); display: flex; align-items: center; justify-content: center; font-size: 1.7rem; font-weight: 700; color: #fff; }
.section-title { margin-top: 0px !important; margin-bottom: 18px !important; font-family: 'Poppins', 'Inter', sans-serif; font-size: 2rem; font-weight: 700; letter-spacing: -0.01em; background: linear-gradient(135deg,#667eea,#764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; display: flex; align-items: center; }
</style>
<div class="header-row">
  <div class="header-logo">HealthKart</div>
  <div class="header-search"></div>
  <div class="header-avatar">H</div>
</div>
''', unsafe_allow_html=True)

# Render the search bar in the header using Streamlit (directly below header for now)
search_query = st.text_input(
    label="",
    value="",
    key="search_bar",
    placeholder="Search by name, platform, or category...",
    help="Search by name, platform, or category"
)

# Remove extra vertical space
st.markdown('<div style="height:5px"></div>', unsafe_allow_html=True)

# --- Loading skeleton for data (simulate async load) ---
import time
with st.spinner('Loading dashboard...'):
    time.sleep(0.7)

# Cache the simulated data so it doesn't change on every rerun
@st.cache_data
def load_data():
    return simulate_data()

def filter_influencers(df, query):
    if not query:
        return df
    query = query.lower()
    return df[df.apply(lambda row: query in str(row['name']).lower() or query in str(row['platform']).lower() or query in str(row['category']).lower(), axis=1)]

influencers, posts, tracking, payouts = load_data()
roas_df = calculate_roas(tracking, payouts)
merged = pd.merge(roas_df, influencers, on='influencer_id')

# Apply search filter to merged influencer data
filtered_merged = filter_influencers(merged, search_query)
filtered_influencers = filter_influencers(influencers, search_query)

# Tabs with modern nav
selected_tab = st.selectbox("", ["Campaign Performance", "Influencer Insights", "Payouts"], key="tabnav")

def random_contact(name):
    domains = ["gmail.com", "yahoo.com", "outlook.com", "healthkart.com"]
    email = f"{name.split()[0].lower()}.{name.split()[-1].lower()}@{random.choice(domains)}"
    phone = f"+91-{random.randint(70000,99999)}-{random.randint(10000,99999)}"
    return email, phone

if selected_tab == "Campaign Performance":
    st.markdown('<div class="section-title">Campaign Performance Overview</div>', unsafe_allow_html=True)
    if filtered_merged.empty:
        st.markdown('<div style="text-align:center; margin-top:20px; color:#b794f6; font-size:1.3rem;"><span style="font-size:2.5rem;">🔍</span><br>No results found for your search.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="dashboard-grid">', unsafe_allow_html=True)
        for idx, row in filtered_merged.sort_values(by='roas', ascending=False).iterrows():
            platform_class = row['platform'].lower()
            email, phone = random_contact(row['name'])
            with st.container():
                st.markdown(f'''
                <div class="influencer-card">
                    <div style="display:flex;align-items:center;gap:1.5rem;">
                        <img src="https://api.dicebear.com/7.x/avataaars/svg?seed={row['name'].replace(' ','')}" class="avatar" />
                        <div style="flex:1;">
                            <div style="font-size:1.2rem;font-weight:600;">{row['name']} <span class="platform-badge {platform_class}">{row['platform']}</span></div>
                            <div style="color:#9CA3AF;">Followers: {int(row['followers']):,}</div>
                            <div style="margin-top:0.3rem;">ROAS: <span class="roas-value">{row['roas']:.2f}</span></div>
                            <div class="roas-progress"><div class="roas-fill" style="width:{min(row['roas']*20,100)}%"></div></div>
                        </div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Contact {row['influencer_id']}", key=f"contact_{row['influencer_id']}"):
                        st.info(f"**Email:** {email}\n\n**Phone:** {phone}")
                with col2:
                    with st.expander("Analytics", expanded=False):
                        st.write(f"**Platform:** {row['platform']}")
                        st.write(f"**Followers:** {int(row['followers']):,}")
                        st.write(f"**ROAS:** {row['roas']:.2f}")
                        st.write(f"**Category:** {row['category']}")
        st.markdown('</div>', unsafe_allow_html=True)
        # Modern, clean bar chart
        fig = px.bar(filtered_merged, x='name', y='roas', color='platform', color_discrete_sequence=['#667eea','#764ba2','#4facfe'])
        fig.update_layout(
            plot_bgcolor='rgba(10,11,13,0.0)',
            paper_bgcolor='rgba(10,11,13,0.0)',
            font_family='Inter',
            font_color='#f8fafc',
            xaxis=dict(showgrid=False, tickangle=-30, title=''),
            yaxis=dict(showgrid=False, title='ROAS'),
            margin=dict(l=20, r=20, t=10, b=40),
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
        )
        fig.update_traces(marker_line_width=0, opacity=0.92)
        st.plotly_chart(fig, use_container_width=True)

elif selected_tab == "Influencer Insights":
    st.markdown('<div class="section-title">🌟 Top Influencers by Revenue</div>', unsafe_allow_html=True)
    top = get_top_influencers(tracking, filtered_influencers)
    if top.empty:
        st.markdown('<div style="text-align:center; margin-top:40px; color:#b794f6; font-size:1.3rem;"><span style="font-size:2.5rem;">🔍</span><br>No results found for your search.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="dashboard-grid">', unsafe_allow_html=True)
        for idx, row in top.iterrows():
            platform_class = row['platform'].lower()
            email, phone = random_contact(row['name'])
            with st.container():
                st.markdown(f'''
                <div class="influencer-card">
                    <div style="display:flex;align-items:center;gap:1.5rem;">
                        <img src="https://api.dicebear.com/7.x/avataaars/svg?seed={row['name'].replace(' ','')}" class="avatar" />
                        <div style="flex:1;">
                            <div style="font-size:1.2rem;font-weight:600;">{row['name']} <span class="platform-badge {platform_class}">{row['platform']}</span></div>
                            <div style="color:#9CA3AF;">Category: {row['category']} | Followers: {int(row['followers']):,}</div>
                        </div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Contact {row['influencer_id']}", key=f"contact2_{row['influencer_id']}"):
                        st.info(f"**Email:** {email}\n\n**Phone:** {phone}")
                with col2:
                    with st.expander("Analytics", expanded=False):
                        st.write(f"**Platform:** {row['platform']}")
                        st.write(f"**Followers:** {int(row['followers']):,}")
                        st.write(f"**Category:** {row['category']}")
        st.markdown('</div>', unsafe_allow_html=True)
        # Neon pie chart
        fig2 = px.pie(filtered_influencers, names='platform', title='Platform Distribution', color_discrete_sequence=['#00d4ff','#b794f6','#f093fb'])
        fig2.update_layout(
            plot_bgcolor='rgba(10,11,13,0.8)',
            paper_bgcolor='rgba(10,11,13,0.8)',
            font_color='#f8fafc',
            title_font_color='#b794f6',
        )
        st.plotly_chart(fig2, use_container_width=True)

elif selected_tab == "Payouts":
    st.markdown('<div class="section-title">💰 Payout Summary</div>', unsafe_allow_html=True)
    st.markdown('<div class="dashboard-grid">', unsafe_allow_html=True)
    for idx, row in payouts.iterrows():
        st.markdown(f'''
        <div class="influencer-card">
            <div style="display:flex;align-items:center;gap:1.5rem;">
                <img src="https://api.dicebear.com/7.x/avataaars/svg?seed={row['influencer_id']}" class="avatar" />
                <div style="flex:1;">
                    <div style="font-size:1.1rem;font-weight:600;">Influencer ID: {row['influencer_id']}</div>
                    <div style="color:#9CA3AF;">Basis: {row['basis']} | Rate: ₹{row['rate']} | Orders: {row['orders']}</div>
                    <div style="margin-top:0.3rem;">Total Payout: <b style="color:#f093fb;">₹{row['total_payout']:,}</b></div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("### Export:")
    st.download_button("Download Payouts CSV", payouts.to_csv(index=False), "payouts.csv") 