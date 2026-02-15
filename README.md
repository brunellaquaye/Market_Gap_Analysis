# The Sugar Trap — Snack Market Gap Analysis
### Helix CPG Partners · Strategic Food & Beverage Consultancy

## A. Executive Summary

Out of 54,169 snack products analyzed from the Open Food Facts dataset, only 5.9% fall into the “Blue Ocean” zone — products with ≥15g protein and ≤10g sugar per 100g. Most products are high in sugar and low in protein.

The clearest opportunity is in Chips & Savory Snacks, a large category of 7,620 products. Only 1.5% currently meet the high-protein, low-sugar target. The category averages just 8.2g sugar, meaning a protein boost would create a high-demand product with minimal competition.

Top protein sources driving success in Blue Ocean products are Peanuts (26%), Soy/Soybean (22%), and Almonds (13%), plant-based, cost-effective, and ideal for savory snacks. The recommendation: launch a high-protein savory snack (≥15g protein, ≤5g sugar) using peanut or soy protein to capture a market with near-zero direct competition.

## B. Project Links

| Deliverable | Link |
|---|---|
| Notebook (Google Colab) | https://colab.research.google.com/drive/1-g8Om1Q3m-_T_PAFPqhPH_4z7lu8UGgy?usp=sharing |
| Live Dashboard (Streamlit) | https://marketgap.streamlit.app |
| Slide Deck | https://docs.google.com/presentation/d/1dlb6ABs1_Hdzejg47mS84_JQx5OHJcJeEu0MHGSBRxA/edit?usp=sharing |


## C. Technical Explanation

### Data Cleaning (Story 1)

**Selective loading.** I loaded only the first 500,000 rows and only 8 columns (`product_name`, `categories_tags`, `ingredients_text`, `sugars_100g`, `proteins_100g`, `fat_100g`, `fiber_100g`, `energy_100g`). This kept memory usage under control.

**Handling missing values.** Dropped rows missing `product_name`, `sugars_100g`, or `proteins_100g`. Supplementary columns like `fat_100g` or `fiber_100g` were kept even if missing.

**Filtering impossible values.** Every nutritional value is measured per 100g of product. That means no single nutrient can exceed 100g/100g — it's physically impossible. Any row with sugar, protein, fat, or fiber outside the 0–100 range was removed. 

**Snack filtering.** After cleaning, I parsed the `categories_tags` column (a messy comma-separated string of Open Food Facts tags like `en:sweet-snacks,en:biscuits-and-cakes`) and applied a two-step classification: first exclude non-snack products (beverages, frozen desserts, soups, meals, etc.), then match remaining products to one of 8 clean category buckets using priority-ordered keyword rules. This reduced 391,528 clean rows down to 54,169 snack products.

The final cleaned and classified dataset was saved as `food_facts_snacks.csv` for use in the dashboard.


### Candidate's Choice — The Reformulation Gap Analysis

**What it is:** A two-panel chart showing, for each snack category, exactly how many grams of sugar need to be cut and how many grams of protein need to be added to reach the Blue Ocean target (≥15g protein, ≤10g sugar). A combined "difficulty score" (total gap in grams) ranks categories from easiest to hardest to reformulate.

**Why I added it:** The scatter plot shows *where* products currently are. The opportunity score shows *which category* to target. But neither answers the question an R&D director asks immediately after: *"How hard is it to actually get there?"*

There are two routes to entering a new market, launching a brand-new product from scratch, or reformulating an existing product. Option two is faster, cheaper, and lower risk, but only if the gap is closeable. This chart makes that call instantly visible.

The result is striking:Chips & Savory Snacks already meets the sugar target (avg 8.2g, shown as in the chart). It only needs +10g of protein. Compare that to Candy & Confectionery, which needs to cut 44g of sugar, that's not a reformulation, that's a completely different product. 



## F. Key Numbers at a Glance

| Metric | Value |
|---|---|
| Total snack products analysed | 54,169 |
| Products in the Sugar Trap (>20g sugar, <5g protein) | 24,521 |
| Products in the Blue Ocean zone (≥15g protein, ≤10g sugar) | 3,176 |
| Blue Ocean share of total market | 5.9% |
| Target category | Chips & Savory Snacks |
| Products in target category | 7,620 |
| Blue Ocean products in target category | 111 (1.5%) |
| Recommended protein target | ≥15g per 100g |
| Recommended sugar ceiling | <5g per 100g |
| Top protein source (#1) | Peanut (26% of Blue Ocean products) |
| Top protein source (#2) | Soy / Soybean (22%) |
| Top protein source (#3) | Almond (13%) |


*Data source: [Open Food Facts](https://world.openfoodfacts.org/) — open database of food products worldwide.*
*Analysis: 500,000 row subset · Cleaned to 391,528 rows · Filtered to 54,169 snack products*