# French-and-Non-French-Wine-Selection-in-BC-Liquor-Regression-Analysis
OLS linear regression analysis quantifying country-of-origin price premiums using retail observations.

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Methodology](#methodology)
3. [Key Findings and Data Analysis](#key-findings-and-data-analysis)
4. [Conclusions and Next Steps](#conclusions-and-next-steps)

---
## Executive Summary
This project explores the varieties of liquor in BC Liquor Stores and analyzes their countries of origin. The data shows that Wine is the dominant product category, with the majority of these wines originating from France. Our statistical analysis confirmed that France commands a statistically significant price premium compared to wines from other countries, with an average associated price difference of CAD 124 per litre. Beyond wine, the data reveals strong regional specializations: Canada excels as the primary producer of beer and refreshment beverages, while the United Kingdom leads the market in spirit production.

## Methodology
We utilized a linear regression model with one dummy variable, where the dummy variable is assigned a value of 1 if the wine is from France and 0 if it originates from any other country. 

To ensure the statistical validity of the model, we conducted several diagnostic evaluations:
* **Normality:** A normality test showed that the residuals are not normally distributed; however, the model remains robust due to a large sample size of 4,528 observations.
* **Homoskedasticity:** A test for homoskedasticity indicated the presence of heteroskedasticity. To correct for this, heteroskedasticity-consistent standard errors (HC3) were calculated.
* **Independence:** A test of autocorrelation was performed, confirming that the observations are independent of each other.

## Key Findings and Data Analysis
To understand the inventory at BC Liquor Stores, we first analyzed where products come from and what categories dominate the market. As shown below, wine is the dominant product category across major exporting countries. Canada specializes heavily in beer, while the United Kingdom leads the market in spirit production.

![Category Breakdown by Top 10 Countries](Product%20Breakdown.png)
![Category Breakdown by Top 10 Countries](Wine%20Breakdown.png)

The regression results indicate that both coefficients are statistically significant, meaning that French origin is confidently associated with a premium wine price. 

However, the $R^2$ and adjusted $R^2$ values indicate that there are significant lurking variables not accounted for in the current model. We propose two primary explanations for this unaccounted variance:
1. **Product Type:** A disproportionate number of French products available at BC Liquor Stores may be sparkling wines (Champagne), which naturally command a higher premium.
2. **Product Maturity:** The vintage or age of the wine is not tracked in this baseline model, which perspective-wise contributes heavily to premium pricing.

## Conclusions and Next Steps
On average, French wine is associated with a higher selling price at BC Liquor Stores, validating the market assumption of a French price premium. 

Moving forward, our next steps will be to expand the regression model to control for the missing lurking variables identified in our analysis. Specifically, we aim to source and integrate data regarding product sub-categories (e.g., sparkling vs. still wine) and product age to improve the model's overall explanatory power ($R^2$).
