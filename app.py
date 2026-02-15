import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Sugar Trap | Helix CPG Market Analysis",
    layout="wide"
)

#  DATA LOADING 
@st.cache_data
def load_data():
    df = pd.read_csv("food_facts_snacks.csv")
    p99_sugar = df['sugars_100g'].quantile(0.99)
    p99_protein = df['proteins_100g'].quantile(0.99)
    df_plot = df[(df['sugars_100g'] <= p99_sugar) & (df['proteins_100g'] <= p99_protein)]
    return df, df_plot, p99_sugar, p99_protein

df, df_plot, p99_sugar, p99_protein = load_data()
ALL_CATEGORIES = sorted(df['primary_category'].unique())

CATEGORY_COLORS = {
    'Candy & Confectionery':  '#E63946',
    'Cookies & Biscuits':     '#F4A261',
    'Chips & Savory Snacks':  '#E9C46A',
    'General Snacks':         '#A8DADC',
    'Fruit & Veg Snacks':     '#52B788',
    'Nuts & Seeds':           '#2D9E6F',
    'Dairy & Yogurt Snacks':  '#58A6FF',
    'Protein & Fitness Bars': '#BF91F3',
}

#  SIDEBAR 
st.sidebar.title(" Sugar Trap")
selected_categories = st.sidebar.multiselect(
    "Filter by Category",
    ALL_CATEGORIES,
    default=ALL_CATEGORIES
)
if not selected_categories:
    selected_categories = ALL_CATEGORIES

protein_threshold = st.sidebar.slider(
    "Min Protein (g) for Blue Ocean", 5, 30, 15
)
sugar_threshold = st.sidebar.slider(
    "Max Sugar (g) for Blue Ocean", 2, 30, 10
)

df_filtered = df_plot[df_plot['primary_category'].isin(selected_categories)]
blue_ocean_n = len(df_filtered[
    (df_filtered['proteins_100g'] >= protein_threshold) &
    (df_filtered['sugars_100g'] <= sugar_threshold)
])
blue_pct = blue_ocean_n / len(df_filtered) * 100 if len(df_filtered) > 0 else 0

st.sidebar.markdown(f"**Products shown:** {len(df_filtered):,}")
st.sidebar.markdown(f"**Blue Ocean:** {blue_ocean_n:,} ({blue_pct:.1f}%)")

# HERO METRICS 
total_products = len(df)
sugar_trap_n = len(df[(df['sugars_100g'] > 20) & (df['proteins_100g'] < 5)])
blue_ocean_full = len(df[(df['proteins_100g'] >= 15) & (df['sugars_100g'] <= 10)])
bo_pct_full = blue_ocean_full / total_products * 100

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Products", f"{total_products:,}")
col2.metric("Sugar Trap Products", f"{sugar_trap_n:,}", ">20g sugar + <5g protein")
col3.metric("Blue Ocean Products", f"{blue_ocean_full:,}", "≥15g protein + ≤10g sugar")
col4.metric("Market Gap", f"{bo_pct_full:.1f}%", "of market in Blue Ocean zone")

#  TABS 
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Market Landscape",
    "Category Profiles",
    "Opportunity Score",
    "Protein Sources",
    "Reformulation Gap"
])

#  TAB 1: SCATTER 
with tab1:
    st.subheader("Sugar vs. Protein: Market Landscape")
    df_scatter = df_filtered.groupby('primary_category', group_keys=False).apply(
        lambda x: x.sample(min(len(x), 500), random_state=42)
    )
    fig1 = px.scatter(
        df_scatter,
        x='sugars_100g', y='proteins_100g',
        color='primary_category', hover_name='product_name',
        color_discrete_map=CATEGORY_COLORS,
        labels={'sugars_100g':'Sugar (g/100g)', 'proteins_100g':'Protein (g/100g)'},
        opacity=0.6, height=500
    )
    fig1.add_shape(
        type='rect',
        x0=0, x1=sugar_threshold,
        y0=protein_threshold, y1=p99_protein,
        fillcolor='rgba(88,166,255,0.07)', line=dict(color='#58A6FF', width=1.5, dash='dash')
    )
    st.plotly_chart(fig1, use_container_width=True)

#  TAB 2: CATEGORY PROFILE 
with tab2:
    st.subheader("Average Sugar vs Protein by Category")
    df_tab2 = df[df['primary_category'].isin(selected_categories)]
    summary2 = df_tab2.groupby('primary_category').agg(
        product_count=('product_name','count'),
        avg_sugar=('sugars_100g','mean'),
        avg_protein=('proteins_100g','mean')
    ).reset_index().sort_values('avg_sugar', ascending=False)
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=summary2['primary_category'], y=summary2['avg_sugar'],
        name='Avg Sugar', marker_color='#E63946'
    ))
    fig2.add_trace(go.Bar(
        x=summary2['primary_category'], y=summary2['avg_protein'],
        name='Avg Protein', marker_color='#58A6FF'
    ))
    st.plotly_chart(fig2, use_container_width=True)
    st.dataframe(summary2.set_index('primary_category'))

#  TAB 3: OPPORTUNITY SCORE 
with tab3:
    st.subheader("Market Opportunity Score")
    df_tab3 = df[df['primary_category'].isin(selected_categories)]
    summary3 = df_tab3.groupby('primary_category').agg(
        product_count=('product_name','count'),
        avg_sugar=('sugars_100g','mean'),
        avg_protein=('proteins_100g','mean')
    ).reset_index()
    summary3['ratio'] = summary3['avg_protein'] / (summary3['avg_sugar'] + 1)
    summary3['raw'] = summary3['ratio'] * np.log1p(summary3['product_count'])
    s_min, s_max = summary3['raw'].min(), summary3['raw'].max()
    summary3['score'] = ((summary3['raw'] - s_min)/(s_max - s_min + 1e-9)*100).round(1)
    bar_colors3 = ['#3FB950' if s >=60 else '#D29922' if s >=30 else '#E63946' for s in summary3['score']]
    fig3 = go.Figure(go.Bar(
        x=summary3['score'], y=summary3['primary_category'],
        orientation='h', marker_color=bar_colors3
    ))
    fig3.update_layout(height=400, xaxis_title="Opportunity Score", yaxis_title="")
    st.plotly_chart(fig3, use_container_width=True)

#  TAB 4: PROTEIN SOURCES 
with tab4:
    st.subheader("Top Protein Sources in Blue Ocean Products")
    protein_data = {
        'Protein Source':['Peanut','Soy / Soybean','Almond','Beef','Nuts','Whey','Soy Protein'],
        'Product Count':[799,669,397,135,125,111,62],
        'Type':['Plant','Plant','Plant','Animal','Plant','Animal','Plant']
    }
    prot_df = pd.DataFrame(protein_data).sort_values('Product Count', ascending=True)
    colors = ['#3FB950' if t=='Plant' else '#58A6FF' for t in prot_df['Type']]
    fig4 = go.Figure(go.Bar(
        x=prot_df['Product Count'], y=prot_df['Protein Source'], orientation='h',
        marker_color=colors
    ))
    st.plotly_chart(fig4, use_container_width=True)

#  TAB 5: REFORMULATION GAP 
with tab5:
    st.subheader("Reformulation Gap Analysis")
    df_tab5 = df[df['primary_category'].isin(selected_categories)]
    summary5 = df_tab5.groupby('primary_category').agg(
        avg_sugar=('sugars_100g','mean'),
        avg_protein=('proteins_100g','mean')
    ).reset_index()
    summary5['sugar_gap'] = (summary5['avg_sugar'] - sugar_threshold).clip(lower=0)
    summary5['protein_gap'] = (protein_threshold - summary5['avg_protein']).clip(lower=0)
    summary5['difficulty'] = summary5['sugar_gap'] + summary5['protein_gap']

    fig5 = go.Figure()
    fig5.add_trace(go.Bar(
        x=summary5['primary_category'], y=summary5['difficulty'],
        text=summary5['difficulty'].round(1), textposition='outside'
    ))
    st.plotly_chart(fig5, use_container_width=True)

st.markdown("Data: Open Food Facts · 500k rows · 54,169 snack products")
