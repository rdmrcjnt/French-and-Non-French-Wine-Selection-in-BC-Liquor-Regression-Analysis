import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import statsmodels.api as sm
import scipy.stats as stats


###to get data from local
current_dir = os.path.dirname(__file__) if '__file__' in locals() else '.'
csv_path = os.path.join(current_dir, "..", "Data", "bc_liquor_store_product_price_list_january_2026.csv")
df = pd.read_csv(csv_path)

###to drop duplicate values from table df
df = df.drop_duplicates(subset=['PRODUCT_LONG_NAME'], keep='first') 
###to create a new column where value is Price Per Litre
df["PRICE PER LITRE"] = df["PRODUCT_PRICE"] / df["PRODUCT_LITRES_PER_CONTAINER"] 
###Add a new column where value is count
df['COUNTRY COUNT'] = df.groupby('PRODUCT_COUNTRY_ORIGIN_NAME')['PRODUCT_COUNTRY_ORIGIN_NAME'].transform('count') 


###to create stacked column graph with top 10 countries with the most products
top_10_countries = df['PRODUCT_COUNTRY_ORIGIN_NAME'].value_counts().head(10).index
df_top_10 = df[df['PRODUCT_COUNTRY_ORIGIN_NAME'].isin(top_10_countries)]
category_order = df_top_10['ITEM_CATEGORY_NAME'].value_counts(ascending=True).index.tolist()
fig1 = px.histogram(
    df_top_10,
    x='PRODUCT_COUNTRY_ORIGIN_NAME',
    color='ITEM_CATEGORY_NAME',
    title="Percentage of Categories for Top 10 Countries",
    barnorm="percent"
)
fig1.update_layout(
    barmode="stack",
    yaxis_ticksuffix="%",
    xaxis_title="Country",
    yaxis_title="Percentage (%)",
    # to sort the country text labels from A to Z
    xaxis={'categoryorder': 'category ascending'},
    yaxis={'categoryorder': 'array', 'categoryarray': category_order}
)
fig1.show()

###to create pie chart with drill down button
fig2 = go.Figure()
categories = df_top_10['ITEM_CATEGORY_NAME'].unique()


#add the default "All Categories" trace (Index 0)
cat_counts = df_top_10['ITEM_CATEGORY_NAME'].value_counts()
fig2.add_trace(go.Pie(
    labels=cat_counts.index, 
    values=cat_counts.values, 
    name="All Categories",
    visible=True
))

#add hidden country-breakdown traces for each category
for cat in categories:
    sub_df = df_top_10[df_top_10['ITEM_CATEGORY_NAME'] == cat]
    country_counts = sub_df['PRODUCT_COUNTRY_ORIGIN_NAME'].value_counts()
    
    fig2.add_trace(go.Pie(
        labels=country_counts.index, 
        values=country_counts.values, 
        name=cat,
        visible=False  
    ))

#create the dropdown menu buttons
buttons = []

#Button for the default view
buttons.append(dict(
    method="update",
    label="All Categories Summary",
    args=[{"visible": [True] + [False] * len(categories)},
          {"title": "Overall Item Category Breakdown"}]
))

#buttons for each individual category drill-down
for i, cat in enumerate(categories):
    # Create a visibility list where only the current category's trace is True
    visibility = [False] * (len(categories) + 1)
    visibility[i + 1] = True
    
    buttons.append(dict(
        method="update",
        label=f"Drill: {cat}",
        args=[{"visible": visibility},
              {"title": f"Country Breakdown for Category: {cat}"}]
    ))

#add dropdown menu to layout and display
fig2.update_layout(
    # Chart Title Configuration
    title={
        'text': "Overall Item Category Breakdown",
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {'size': 20}
    },
    # Dropdown Filter Placement (Positioned below the chart)
    updatemenus=[dict(
        active=0,
        buttons=buttons,
        direction="up",
        pad={"r": 10, "t": 10},
        showactive=True,
        x=0.5,
        xanchor="center",
        y=-0.15,
        yanchor="top"
    )],
    # Extra margin at bottom to ensure dropdown is fully visible
    margin=dict(b=100)
)

fig2.show()



###to build Linear Regression analysis with a dummy variable
#to convert price per litre to log
df = df_top_10 
df['LN PRICE PER LITRE'] = np.log(df['PRICE PER LITRE'])
df = df.loc[df['ITEM_CATEGORY_NAME'] == 'Wine']
X = sm.add_constant((df['PRODUCT_COUNTRY_ORIGIN_NAME'] == 'FRANCE').astype(int))
y = df['LN PRICE PER LITRE']
model = sm.OLS(y, X).fit()
residuals = model.resid
print(model.summary())
print("\n" + "="*50 + "\nASSUMPTION CHECKS (LOG MODEL)\n" + "="*50)


#to test Residual normality
shapiro_stat, shapiro_p = stats.shapiro(residuals)
print(f"Shapiro-Wilk Test: Stat={shapiro_stat:.4f}, p-value={shapiro_p:.4f}")
if shapiro_p > 0.05:
    print("-> Result: Fail to reject H0. Residuals of log prices appear normally distributed.")
else:
    print("-> Result: Reject H0. Residuals of log prices are NOT normally distributed.")

#to test residual homoskedasticity
#filter for France prices
group_paris = df[df['PRODUCT_COUNTRY_ORIGIN_NAME'] == 'FRANCE']['LN PRICE PER LITRE']
#filter for Non-France prices (using !=)
group_others = df[df['PRODUCT_COUNTRY_ORIGIN_NAME'] != 'FRANCE']['LN PRICE PER LITRE']
#run Levene's Test
levene_stat, levene_p = stats.levene(group_paris, group_others)
print(f"\nLevene's Test: Stat={levene_stat:.4f}, p-value={levene_p:.4f}")
if levene_p > 0.05:
    print("-> Result: Fail to reject H0. Variances of log prices are equal (Homoscedasticity holds).")
else:
    print("-> Result: Reject H0. Variances of log prices are unequal (Heteroscedasticity detected).")

#to check the homoskedasticity/heteroskedasticity plot
import matplotlib.pyplot as plt
import seaborn as sns
#extract the predicted values and residuals from fitted model
predicted_values = model.fittedvalues
residuals = model.resid
#Create the scatter plot
plt.figure(figsize=(8, 5))
sns.scatterplot(x=predicted_values, y=residuals, alpha=0.5, color='royalblue')
#Add a horizontal line at 0 to represent perfect prediction
plt.axhline(y=0, color='red', linestyle='--', linewidth=1.5)
#Label the plot
plt.title('Residuals vs Predicted Values (Checking for Heteroskedasticity)')
plt.xlabel('Predicted LN PRICE PER LITRE')
plt.ylabel('Residuals (Errors)')
#Display the plot
plt.show()

#to correct heteroskedasticity
#Prepare variables (ensuring X is an integer 0 or 1)
df['is_france'] = (df['PRODUCT_COUNTRY_ORIGIN_NAME'] == 'FRANCE').astype(int)
X = sm.add_constant(df['is_france'])
y = df['LN PRICE PER LITRE']
#Fit the model using HC3 Robust Standard Errors
model = sm.OLS(y, X).fit(cov_type='HC3')
#View the corrected summary
print(model.summary())


