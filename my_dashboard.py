import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
# Set random seed
np.random.seed(42)

# Load the dataset
data = pd.read_csv('supermarket_sales.csv')
df = pd.DataFrame(data)
df['Date'] = pd.to_datetime(df['Date'])  # Convert Date column to datetime format

# Custom CSS for color styling with new palette
st.markdown("""
    <style>
        /* Increase table font size */
    .dataframe {
        font-size: 18px !important;
    }
    /* Set background colors for main container and sidebar */
    .main .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
        height: 100vw;
        width: 100rem;
        overflow: hidden; 
        background-color: #070F2B; /* Dark blue for main background */
        color: #9290C3; /* Light lavender blue for general text */
    }
    .css-1d391kg {
        background-color: #1B1A55 !important; /* Navy blue for sidebar */
    }

    /* Header and title styles */
    h1, h2, h3, .css-12oz5g7 {
        color: #9290C3 !important; /* Lavender blue for headers */
    }

    /* Key Metric styling */
    .stMetric {
        color: #070F2B; /* Dark font on metrics */
        font-size: 24px;
        background: linear-gradient(to right, #512B81, #535C91, #4477CE);   /* Slate blue for metric background */
        padding: 10px;
        border-radius: 5px;
    }

    /* Customize columns within the main content area */
    .css-1lcbmhc {
        margin: 0 auto !important;
        width: 100rem;
    }
    .st-emotion-cache-13ln4jf{
        width:100rem;
        max-width:100%;
    }
    .st-bn{
        background: linear-gradient(to right, #8CABFF, #6A8BFF, #4C70FF);
    }
    .st-dj {
        cursor: pointer;
    }
    .st-dp {
        cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar for filters and navigation
st.sidebar.header("Filter Options")
selected_branch = st.sidebar.multiselect("Select Branch", options=df['Branch'].unique(), default=df['Branch'].unique())
selected_city = st.sidebar.multiselect("Select City", options=df['City'].unique(), default=df['City'].unique())
selected_customer_type = st.sidebar.multiselect("Select Customer Type", options=df['Customer type'].unique(), default=df['Customer type'].unique())
selected_gender = st.sidebar.multiselect("Select Gender", options=df['Gender'].unique(), default=df['Gender'].unique())

# Dropdown for page redirection
page = st.sidebar.selectbox("Navigate to Page", ["Overview", "Research Question 1", "Research Question 2", 
                                                 "Research Question 3", "Research Question 4", 
                                                 "Research Question 5", "Research Question 6"])

    # Filter data based on sidebar selections
df_filtered = df[
    (df['Branch'].isin(selected_branch)) & 
    (df['City'].isin(selected_city)) & 
    (df['Customer type'].isin(selected_customer_type)) & 
    (df['Gender'].isin(selected_gender))
]

if page == "Overview":


    # Set up the dashboard title
    st.title("Superstore Sales Dashboard")

    # Key Metrics
    st.markdown("### Key Metrics")
    total_customers = df_filtered['Invoice ID'].nunique()
    total_profit = df_filtered['gross income'].sum()
    total_cogs = df_filtered['cogs'].sum()
    kpi1, kpi2, kpi3 = st.columns([1, 1, 1])
    kpi1.metric("No. of Customers:", total_customers)
    kpi2.metric("Total COGS/Expenses", "22K")
    kpi3.metric("Sum of Profit", total_profit)

    # Display sample data
    st.subheader("Sample Data Table")
    st.write(df_filtered.head())
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Sales Analysis by Product Line")
        product_sales = df_filtered.groupby('Product line').agg(
            Total_Revenue=('Total', 'sum'),
            Average_Quantity=('Quantity', 'mean'),
            Average_Unit_Price=('Unit price', 'mean')
        ).sort_values(by='Total_Revenue', ascending=False)
        st.write(product_sales)  # Larger text applied via CSS

    with col2:
        st.subheader("Branch and City Performance")
        branch_city_sales = df_filtered.groupby(['Branch', 'City']).agg(Total_Revenue=('Total', 'sum')).unstack().fillna(0)
        st.write(branch_city_sales)  # Larger text applied via CSS

    # Main charts with increased font size for labels
    col3, col4 = st.columns([2, 2])

    with col3:
        product_sales = df_filtered.groupby('Product line').agg(
            Total_Revenue=('Total', 'sum')
        ).reset_index()
        
        fig_product_sales = px.pie(
            product_sales, 
            values='Total_Revenue', 
            names='Product line', 
            title="Sales by Product Line",
            color_discrete_sequence=["#535C91", "#1B1A55", "#9290C3", "#070F2B"]
        )
        fig_product_sales.update_layout(
            title_font_size=24,
            legend_font_size=16,
        )
        st.plotly_chart(fig_product_sales, use_container_width=True)

    with col4:
        customer_type_gender = df_filtered.groupby(['Customer type', 'Gender']).size().reset_index(name='Count')

        fig_customer_demographics = px.pie(
            customer_type_gender,
            values='Count', 
            names='Customer type', 
            title="Customer Type by Gender",
            color='Customer type', 
            color_discrete_sequence=["rgb(52, 50, 163)", "rgb(141, 148, 189)"]  # Updated color scheme
        )

        fig_customer_demographics.update_layout(
            title_font_size=24,
            legend_font_size=16,
        )

        st.plotly_chart(fig_customer_demographics, use_container_width=True)


    branch_city_sales = df_filtered.groupby(['Branch', 'City']).agg(Total_Revenue=('Total', 'sum')).reset_index()
    fig_branch_city = px.bar(
        branch_city_sales, 
        x='Branch', 
        y='Total_Revenue', 
        color='City', 
        title="Total Revenue by Branch and City",
        barmode='stack',
        color_continuous_scale=px.colors.sequential.Purples,
        labels={'Total_Revenue': 'Total Revenue', 'Branch': 'Branch'}
    )
    fig_branch_city.update_layout(
        title_font_size=24,
        xaxis_title_font_size=18,
        yaxis_title_font_size=18,
        legend_font_size=16
    )
    st.plotly_chart(fig_branch_city, use_container_width=True)


    daily_sales = df_filtered.groupby(df_filtered['Date'].dt.date).agg(Total_Revenue=('Total', 'sum')).reset_index()
    fig_daily_sales = px.line(
    daily_sales, 
        x='Date', 
        y='Total_Revenue', 
        title="Sales Trends", 
        labels={'Date': 'Date', 'Total_Revenue': 'Total Revenue'},
        color_discrete_sequence=["#9290C3"]
    )
    fig_daily_sales.update_layout(
        title_font_size=24,
        xaxis_tickangle=-45,
        xaxis_title="Date",
        yaxis_title="Total Revenue",
        xaxis_title_font_size=18,
        yaxis_title_font_size=18,
        legend_font_size=16
    )
    st.plotly_chart(fig_daily_sales, use_container_width=True)
elif page == "Research Question 1":
    st.title("Research Question 1")
    st.markdown("**What are the key sales trends and seasonal patterns in supermarket sales data?**")
    
    # Resample data by month to calculate monthly sales
    monthly_sales = df_filtered.resample('M', on='Date').sum(numeric_only=True)['Total'].reset_index()
    
    # Plotting with Plotly
    fig_q1 = px.line(
        monthly_sales,
        x='Date',
        y='Total',
        title="Monthly Total Sales Over Time",
        labels={'Date': 'Date', 'Total': 'Total Sales'}
    )
    
    fig_q1.update_layout(
        title_font_size=24,
        xaxis_title="Date",
        yaxis_title="Total Sales",
        xaxis_tickangle=-45,
        xaxis_title_font_size=18,
        yaxis_title_font_size=18,
        legend_font_size=16,
        template="plotly_dark"
    )
    
    st.plotly_chart(fig_q1, use_container_width=True)
    st.markdown("### Conclusion")
    st.write("""
    The supermarket sales data indicates a seasonal pattern with a decline in both total sales and gross income during mid to late February, followed by a rebound in March. This suggests that there might be a typical lull in sales activity during February, possibly due to fewer promotional events or lower consumer demand. However, the upward trend in March signals a recovery, potentially driven by increased demand or seasonal events as the spring season approaches.

    Supermarkets may want to take advantage of this pattern by launching promotions or marketing campaigns during the slower February period to mitigate the drop in sales, and capitalize on the natural increase in March by reinforcing their efforts.
    """)
elif page == "Research Question 2":
    st.title("Research Question 2")
    st.markdown("**How do customer demographics (e.g., gender, membership status) influence purchasing behavior and sales volume?**")
        
    # --- Total Sales by Gender ---
    sales_by_gender = df_filtered.groupby('Gender')['Total'].sum().reset_index()
    fig_sales_gender = px.bar(
        sales_by_gender,
        x='Gender',
        y='Total',
        title="Total Sales by Gender",
        color='Gender',
        labels={'Total': 'Total Sales'},
        color_discrete_map={
            'Male': 'rgb(52, 50, 163)',
            'Female': 'rgb(141, 148, 189)'
        }
    )
    fig_sales_gender.update_layout(
        title_font_size=24,
        xaxis_title="Gender",
        yaxis_title="Total Sales",
        xaxis_tickangle=0,
        xaxis_title_font_size=18,
        yaxis_title_font_size=18,
        legend_font_size=16,
        plot_bgcolor='rgb(245, 245, 245)'  # Light background for contrast
    )
    st.plotly_chart(fig_sales_gender, use_container_width=True)
    # --- Product Line Preferences by Gender ---
    product_line_gender = df_filtered.groupby(['Product line', 'Gender']).size().reset_index(name='Count')
    fig_product_line_gender = px.bar(
        product_line_gender,
        x='Product line',
        y='Count',
        color='Gender',
        barmode='group',
        title="Product Line Preferences by Gender",
        labels={'Product line': 'Product Line', 'Count': 'Number of Purchases'},
        color_discrete_map={
            'Male': 'rgb(52, 50, 163)',
            'Female': 'rgb(141, 148, 189)'
        }
    )
    fig_product_line_gender.update_layout(
        title_font_size=24,
        xaxis_tickangle=-45,
        xaxis_title="Product Line",
        yaxis_title="Number of Purchases",
        xaxis_title_font_size=18,
        yaxis_title_font_size=18,
        legend_font_size=16,
        plot_bgcolor='rgb(245, 245, 245)'
    )
    st.plotly_chart(fig_product_line_gender, use_container_width=True)

    # --- Product Line Preferences by Customer Type ---
    product_line_customer_type = df_filtered.groupby(['Product line', 'Customer type']).size().reset_index(name='Count')
    fig_product_line_customer_type = px.bar(
        product_line_customer_type,
        x='Product line',
        y='Count',
        color='Customer type',
        barmode='group',
        title="Product Line Preferences by Customer Type",
        labels={'Product line': 'Product Line', 'Count': 'Number of Purchases'},
        color_discrete_map={
            'Member': 'rgb(83, 92, 145)',
            'Normal': 'rgb(68, 68, 68)'
        }
    )
    fig_product_line_customer_type.update_layout(
        title_font_size=24,
        xaxis_tickangle=-45,
        xaxis_title="Product Line",
        yaxis_title="Number of Purchases",
        xaxis_title_font_size=18,
        yaxis_title_font_size=18,
        legend_font_size=16,
        plot_bgcolor='rgb(245, 245, 245)'
    )
    st.plotly_chart(fig_product_line_customer_type, use_container_width=True)
    # Conclusion
    st.markdown("### Conclusion")
    st.write("""
        The graphs suggest that gender plays a notable role in influencing purchasing behavior and sales volume. 
        While both male and female customers contribute significantly to total sales, females tend to generate slightly higher sales overall. 
        Product preferences also vary by gender, with females showing a stronger inclination towards categories like home and lifestyle, as well as fashion accessories, while males prefer sports and travel, along with health and beauty products. 
        Although both genders exhibit similar interest in categories like electronic accessories and food and beverages, these differences highlight the impact of gender on shopping patterns.
        """)

elif page == "Research Question 3":
    st.title("Research Question 3")
    st.markdown("**Which product lines contribute the most to overall revenue, and which ones are underperforming?**")

    # --- Total Sales by Product Line ---
    sales_by_product = df_filtered.groupby('Product line')['Total'].sum().reset_index()
    fig_sales_product = px.bar(
        sales_by_product,
        x='Product line',
        y='Total',
        title="Total Sales by Product Line",
        color='Product line',
        color_discrete_sequence=[
            'rgb(52, 50, 163)', 'rgb(141, 148, 189)', 'rgb(83, 92, 145)', 'rgb(68, 68, 68)',
            'rgb(111, 115, 178)', 'rgb(75, 73, 165)'
        ]
    )
    fig_sales_product.update_layout(
        title_font_size=24,
        xaxis_title="Product Line",
        yaxis_title="Total Sales",
        xaxis_tickangle=-45,
        xaxis_title_font_size=18,
        yaxis_title_font_size=18,
        legend_title_text="Product Line",
        plot_bgcolor='rgb(245, 245, 245)'
    )
    st.plotly_chart(fig_sales_product, use_container_width=True)

    # --- Revenue Contribution by Product Line (Pie Chart) ---
    fig_revenue_contribution = px.pie(
    sales_by_product,
    names='Product line',
    values='Total',
    title="Revenue Contribution by Product Line",
    color_discrete_sequence=[
        'rgb(52, 50, 163)', 'rgb(141, 148, 189)', 'rgb(83, 92, 145)', 'rgb(68, 68, 68)',
        'rgb(111, 115, 178)', 'rgb(75, 73, 165)'
    ]
)

    # Update traces to ensure all labels are placed inside
    fig_revenue_contribution.update_traces(
        textinfo='percent+label', 
        textposition='inside',  # Place all labels inside the chart
        insidetextorientation='radial'  # Orient text radially for better fit
    )

    # Update layout
    fig_revenue_contribution.update_layout(
        title_font_size=24,
        legend_font_size=16,
        plot_bgcolor='rgb(245, 245, 245)'
    )

    # Display in Streamlit
    st.plotly_chart(fig_revenue_contribution, use_container_width=True)

    # Conclusion
    st.markdown("### Conclusion")
    st.write("""
    The product lines contributing the most to revenue are **Food and Beverages**, **Electronic Accessories**, 
    and **Fashion Accessories**, with **Food and Beverages** leading at 17.4%. On the other hand, **Health and Beauty** 
    is underperforming, contributing the least to both total sales and revenue at 15.2%. **Home and Lifestyle** 
    also lags slightly, with a lower contribution of 16.7% in revenue compared to the top performers.
    """)

elif page == "Research Question 4":
    st.title("Research Question 4")
    st.markdown("**How do sales performance and product preferences vary across different branches and cities?**")

    # --- Sales by Branch ---
    branch_sales = df_filtered.groupby('Branch')['Total'].sum().reset_index()
    fig_branch_sales = px.bar(
        branch_sales,
        x='Branch',
        y='Total',
        title="Sales by Branch",
        color='Branch',
        color_discrete_sequence=['rgb(141, 148, 189)', 'rgb(83, 92, 145)', 'rgb(68, 68, 68)']
    )
    fig_branch_sales.update_layout(
        title_font_size=24,
        xaxis_title="Branch",
        yaxis_title="Total Sales",
        xaxis_tickangle=0,
        plot_bgcolor='rgb(245, 245, 245)'
    )
    st.plotly_chart(fig_branch_sales, use_container_width=True)

    # --- Product Preferences by City (Heatmap) ---
   # Create the pivot table
    product_city_sales = df_filtered.pivot_table(values='Total', index='Product line', columns='City', aggfunc='sum').fillna(0)

    # Convert the pivot table values to formatted strings for display in each cell
    text_values = product_city_sales.applymap(lambda x: f'{x:,.0f}')  # Format values as comma-separated integers

    # Create the heatmap with annotations
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=product_city_sales.values,
        x=product_city_sales.columns,
        y=product_city_sales.index,
        text=text_values.values,  # Add text values
        hovertemplate="%{text}",  # Display text values
        colorscale='Blues',
        colorbar=dict(title="Sales")
    ))

    # Update layout for title, axis titles, and background color
    fig_heatmap.update_layout(
        title="Product Sales by City and Product Line",
        xaxis_title="City",
        yaxis_title="Product Line",
        plot_bgcolor='rgb(245, 245, 245)'
    )

# Display in Streamlit
    st.plotly_chart(fig_heatmap, use_container_width=True)
    # Conclusion
    st.markdown("### Conclusion")
    st.write("""
    Sales performance is relatively balanced across branches, but product preferences vary significantly by city. Naypyitaw leads in food and fashion, Yangon excels in home goods, and Mandalay is strong in health and travel-related products.
    """)

elif page == "Research Question 5":
    st.title("Research Question 5")
    st.markdown("**What is the relationship between customer satisfaction ratings and sales volume across different product categories?**")

    # --- Satisfaction Rating vs Sales by Product Line (Scatter Plot) ---
    # Create the scatter plot based on filtered data
    fig_scatter_satisfaction_sales = px.scatter(
        df_filtered,
        x='Rating',
        y='Total',
        color='Gender',
        facet_col='Product line',
        facet_col_wrap=3,
        title="Customer Satisfaction Rating vs. Sales Volume by Product Line",
        color_discrete_sequence=['rgb(52, 50, 163)', 'rgb(83, 92, 145)'],
        opacity=0.7,
        facet_col_spacing=0.08,  # Adjust column spacing
        facet_row_spacing=0.15   # Adjust row spacing
    )

    # Update layout for improved spacing and appearance
    fig_scatter_satisfaction_sales.update_layout(
        title_font_size=24,
        xaxis_title="Customer Satisfaction Rating",
        yaxis_title="Total Sales",
        legend_title_text="Gender",
        plot_bgcolor='rgb(245, 245, 245)',
        margin=dict(t=80, b=50, l=50, r=50)  # Add margins around the entire plot
    )

    # Adjust subplot titles to give more space between title and the graph
    for annotation in fig_scatter_satisfaction_sales.layout.annotations:
        annotation['yshift'] = 10  # Move titles slightly higher to increase spacing

    # Display the updated plot in Streamlit
    st.plotly_chart(fig_scatter_satisfaction_sales, use_container_width=True)
    # --- Customer Satisfaction Ratings by Product Line (Box Plot) ---
    fig_boxplot_satisfaction = px.box(
        df_filtered,
        x='Product line',
        y='Rating',
        title="Customer Satisfaction Ratings by Product Line",
        color_discrete_sequence=['rgb(68, 68, 68)']
    )
    fig_boxplot_satisfaction.update_layout(
        title_font_size=24,
        xaxis_title="Product Line",
        yaxis_title="Satisfaction Rating",
        xaxis_tickangle=-45,
        plot_bgcolor='rgb(245, 245, 245)'
    )
    st.plotly_chart(fig_boxplot_satisfaction, use_container_width=True)

    # Conclusion
    st.markdown("### Conclusion")
    st.write("""
    While customer satisfaction ratings are relatively similar across product categories, the scatter plot suggests no strong correlation between customer satisfaction and sales volume. Products with high sales can have varying satisfaction ratings, and vice versa.
    """)

elif page == "Research Question 6":
    st.title("Research Question 6")
    st.markdown("**How do different payment methods (e.g., cash, credit card, mobile payment) impact sales volume and customer satisfaction?**")

    # --- Sales by Payment Method ---
    payment_sales = df_filtered.groupby('Payment')['Total'].sum().reset_index()
    fig_payment_sales = px.bar(
        payment_sales,
        x='Payment',
        y='Total',
        title="Sales by Payment Method",
        color='Payment',
        color_discrete_sequence=['rgb(52, 50, 163)', 'rgb(141, 148, 189)', 'rgb(83, 92, 145)']
    )
    fig_payment_sales.update_layout(
        title_font_size=24,
        xaxis_title="Payment Method",
        yaxis_title="Total Sales",
        xaxis_tickangle=0,
        plot_bgcolor='rgb(245, 245, 245)'
    )
    st.plotly_chart(fig_payment_sales, use_container_width=True)

    # --- Customer Satisfaction Ratings by Payment Method (Box Plot) ---
    fig_boxplot_payment = px.box(
        df_filtered,
        x='Payment',
        y='Rating',
        title="Customer Satisfaction Ratings by Payment Method",
        color_discrete_sequence=['rgb(68, 68, 68)']
    )
    fig_boxplot_payment.update_layout(
        title_font_size=24,
        xaxis_title="Payment Method",
        yaxis_title="Satisfaction Rating",
        plot_bgcolor='rgb(245, 245, 245)'
    )
    st.plotly_chart(fig_boxplot_payment, use_container_width=True)

    # Conclusion
    st.markdown("### Conclusion")
    st.write("""
    Sales Volume Impact: Cash payments drive the highest sales, followed closely by Ewallets, with credit cards generating slightly lower sales.
    
    Customer Satisfaction Impact: Ewallet users generally report the highest satisfaction, followed by credit card users. Cash payments have slightly lower satisfaction ratings on average but maintain a more consistent distribution across the range.
    
    This indicates that while cash drives more sales, Ewallet tends to yield higher customer satisfaction on average.
    """)
