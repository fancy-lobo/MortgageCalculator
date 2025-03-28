# Adjustable parameters
num_children = 1  # Number of children

# Tuition inputs:
# Set the annual tuition for the highest grade (per child, in USD)
highest_grade_tuition = 27950   # Default average; update as needed (e.g., 37300 for premium schools)
# Multiplier to infer average elementary tuition from highest-grade tuition.
# (Default ratio based on rough averages: 8276/14596 ≈ 0.57)
elementary_ratio = 0.57  
elementary_tuition = highest_grade_tuition * elementary_ratio

# --- Worst-Case Scenario Housing Assumptions ---
# Modest Home (Average District)
modest_home_price = 450000
modest_closing_rate = 0.04
modest_closing_cost = modest_home_price * modest_closing_rate
worst_case_modest_interest = 69000  # Interest paid over 5-6 years (worst-case)
worst_case_modest_total_housing = modest_home_price + modest_closing_cost + worst_case_modest_interest

# Upscale Home (Wayzata)
upscale_home_price = 700000
credit = 20000
upscale_effective_price = upscale_home_price - credit
upscale_closing_rate = 0.04
upscale_closing_cost = upscale_home_price * upscale_closing_rate
worst_case_upscale_interest = 158000  # Interest paid over ~8 years (worst-case)
worst_case_upscale_total_housing = upscale_effective_price + upscale_closing_cost + worst_case_upscale_interest

# --- Best-Case Scenario Housing Assumptions ---
# Assume best-case interest is much lower due to early payoff.
best_case_modest_interest = 23000  # Modest home paid off in 1-2 years
best_case_modest_total_housing = modest_home_price + modest_closing_cost + best_case_modest_interest

best_case_upscale_interest = 70000  # Upscale home paid off in 3-4 years
best_case_upscale_total_housing = upscale_effective_price + upscale_closing_cost + best_case_upscale_interest

# --- Tuition Calculations (These remain the same in both scenarios) ---
# Option 1: Full Private K–12
tuition_elem_full = 9 * elementary_tuition * num_children  # 9 years (K–8)
tuition_high_full = 4 * highest_grade_tuition * num_children   # 4 years (9–12)
tuition_full_private = tuition_elem_full + tuition_high_full

# Option 2A: Hybrid – Private K–5 then Public (6 years private elementary)
tuition_private_K5 = 6 * elementary_tuition * num_children

# Option 2B: Hybrid – Private K–8 then Public (9 years private elementary)
tuition_private_K8 = 9 * elementary_tuition * num_children

# Option 3: Full Public Schooling in Wayzata (no tuition)
tuition_public = 0

# --- Combined Total Outlays (Housing + Tuition) ---
# Worst-case:
option1_total_worst = worst_case_modest_total_housing + tuition_full_private
option2A_total_worst = worst_case_modest_total_housing + tuition_private_K5
option2B_total_worst = worst_case_modest_total_housing + tuition_private_K8
option3_total_worst = worst_case_upscale_total_housing  # No tuition for public option

# Best-case:
option1_total_best = best_case_modest_total_housing + tuition_full_private
option2A_total_best = best_case_modest_total_housing + tuition_private_K5
option2B_total_best = best_case_modest_total_housing + tuition_private_K8
option3_total_best = best_case_upscale_total_housing  # No tuition for public option

# --- Future Home Value Projections (15-Year Horizon) ---
annual_growth_rate = 0.035  # 3.5% annual growth rate
years = 15

# Future sale value is based on the original purchase prices:
modest_future_value = modest_home_price * ((1 + annual_growth_rate) ** years)
upscale_future_value = upscale_effective_price * ((1 + annual_growth_rate) ** years)

# --- Net Asset ("Remaining Equity") Calculation ---
# Defined as the projected future sale value minus total outlays.
net_asset_option1_worst = modest_future_value - option1_total_worst
net_asset_option2A_worst = modest_future_value - option2A_total_worst
net_asset_option2B_worst = modest_future_value - option2B_total_worst
net_asset_option3_worst = upscale_future_value - option3_total_worst

net_asset_option1_best = modest_future_value - option1_total_best
net_asset_option2A_best = modest_future_value - option2A_total_best
net_asset_option2B_best = modest_future_value - option2B_total_best
net_asset_option3_best = upscale_future_value - option3_total_best

# --- Markdown Output ---
markdown_output = f"""
## Cost-Benefit Analysis Over 15 Years: Worst-Case vs. Best-Case

### Tuition Inputs:
- **Highest Grade Tuition:** \$**{highest_grade_tuition:,.0f}** per year (per child)
- **Inferred Average Elementary Tuition:** \$**{elementary_tuition:,.0f}** per year (per child)  
  *(Using a multiplier of {elementary_ratio:.2f} applied to highest-grade tuition)*

---

## Worst-Case Scenario
### Housing Outlays:
- **Modest Home (Average District):**  
  - Purchase Price: \$450,000  
  - Closing Costs (4%): \$**{modest_closing_cost:,.0f}**  
  - Interest (over 5–6 yrs): \$**{worst_case_modest_interest:,.0f}**  
  - **Total Outlay:** \$**{worst_case_modest_total_housing:,.0f}**

- **Upscale Home (Wayzata):**  
  - Effective Purchase Price: \$**{upscale_effective_price:,.0f}**  
  - Closing Costs (4% of \$700K): \$**{upscale_closing_cost:,.0f}**  
  - Interest (over ~8 yrs): \$**{worst_case_upscale_interest:,.0f}**  
  - **Total Outlay:** \$**{worst_case_upscale_total_housing:,.0f}**

### Tuition Costs (for {num_children} child(ren)):
- **Option 1: Full Private K–12:**  
  - Elementary (K–8 for 9 yrs): \$**{tuition_elem_full:,.0f}**  
  - High School (9–12 for 4 yrs): \$**{tuition_high_full:,.0f}**  
  - **Total Tuition:** \$**{tuition_full_private:,.0f}**

- **Option 2A: Hybrid – Private K–5 then Public:**  
  - Private Elementary (K–5 for 6 yrs): \$**{tuition_private_K5:,.0f}**

- **Option 2B: Hybrid – Private K–8 then Public:**  
  - Private Elementary/Middle (K–8 for 9 yrs): \$**{tuition_private_K8:,.0f}**

- **Option 3: Full Public (Wayzata):**  
  - **Total Tuition:** \$0

### Combined Total Outlays (Housing + Tuition) - Worst-Case:
| Option                                  | Housing Outlay       | Tuition Outlay       | **Total Outlay**     |
|-----------------------------------------|----------------------|----------------------|----------------------|
| **1. Full Private K–12**                | \${worst_case_modest_total_housing:,.0f}      | \${tuition_full_private:,.0f}      | \${option1_total_worst:,.0f}      |
| **2A. Hybrid: Private K–5 then Public**   | \${worst_case_modest_total_housing:,.0f}      | \${tuition_private_K5:,.0f}         | \${option2A_total_worst:,.0f}      |
| **2B. Hybrid: Private K–8 then Public**   | \${worst_case_modest_total_housing:,.0f}      | \${tuition_private_K8:,.0f}         | \${option2B_total_worst:,.0f}      |
| **3. Full Public (Wayzata)**             | \${worst_case_upscale_total_housing:,.0f}     | \$0                     | \${option3_total_worst:,.0f}     |

### Projected Future Home Values (after 15 years):
- **Modest Home Future Value:** \$**{modest_future_value:,.0f}**
- **Upscale Home Future Value:** \$**{upscale_future_value:,.0f}**

### Net Asset ("Remaining Equity") - Worst-Case:
| Option                                  | Future Value         | Total Outlay         | **Net Asset**        |
|-----------------------------------------|----------------------|----------------------|----------------------|
| **1. Full Private K–12**                | \${modest_future_value:,.0f}         | \${option1_total_worst:,.0f}      | \${net_asset_option1_worst:,.0f}      |
| **2A. Hybrid: Private K–5 then Public**   | \${modest_future_value:,.0f}         | \${option2A_total_worst:,.0f}      | \${net_asset_option2A_worst:,.0f}      |
| **2B. Hybrid: Private K–8 then Public**   | \${modest_future_value:,.0f}         | \${option2B_total_worst:,.0f}      | \${net_asset_option2B_worst:,.0f}      |
| **3. Full Public (Wayzata)**             | \${upscale_future_value:,.0f}        | \${option3_total_worst:,.0f}      | \${net_asset_option3_worst:,.0f}      |

---

## Best-Case Scenario
### Housing Outlays:
- **Modest Home (Average District):**  
  - Purchase Price: \$450,000  
  - Closing Costs (4%): \$**{modest_closing_cost:,.0f}**  
  - Interest (over 1–2 yrs): \$**{best_case_modest_interest:,.0f}**  
  - **Total Outlay:** \$**{best_case_modest_total_housing:,.0f}**

- **Upscale Home (Wayzata):**  
  - Effective Purchase Price: \$**{upscale_effective_price:,.0f}**  
  - Closing Costs (4% of \$700K): \$**{upscale_closing_cost:,.0f}**  
  - Interest (over 3–4 yrs): \$**{best_case_upscale_interest:,.0f}**  
  - **Total Outlay:** \$**{best_case_upscale_total_housing:,.0f}**

### Combined Total Outlays (Housing + Tuition) - Best-Case:
| Option                                  | Housing Outlay       | Tuition Outlay       | **Total Outlay**     |
|-----------------------------------------|----------------------|----------------------|----------------------|
| **1. Full Private K–12**                | \${best_case_modest_total_housing:,.0f}      | \${tuition_full_private:,.0f}      | \${option1_total_best:,.0f}      |
| **2A. Hybrid: Private K–5 then Public**   | \${best_case_modest_total_housing:,.0f}      | \${tuition_private_K5:,.0f}         | \${option2A_total_best:,.0f}      |
| **2B. Hybrid: Private K–8 then Public**   | \${best_case_modest_total_housing:,.0f}      | \${tuition_private_K8:,.0f}         | \${option2B_total_best:,.0f}      |
| **3. Full Public (Wayzata)**             | \${best_case_upscale_total_housing:,.0f}     | \$0                     | \${option3_total_best:,.0f}     |

### Net Asset ("Remaining Equity") - Best-Case:
| Option                                  | Future Value         | Total Outlay         | **Net Asset**        |
|-----------------------------------------|----------------------|----------------------|----------------------|
| **1. Full Private K–12**                | \${modest_future_value:,.0f}         | \${option1_total_best:,.0f}      | \${net_asset_option1_best:,.0f}      |
| **2A. Hybrid: Private K–5 then Public**   | \${modest_future_value:,.0f}         | \${option2A_total_best:,.0f}      | \${net_asset_option2A_best:,.0f}      |
| **2B. Hybrid: Private K–8 then Public**   | \${modest_future_value:,.0f}         | \${option2B_total_best:,.0f}      | \${net_asset_option2B_best:,.0f}      |
| **3. Full Public (Wayzata)**             | \${upscale_future_value:,.0f}        | \${option3_total_best:,.0f}      | \${net_asset_option3_best:,.0f}      |

---

### Note:
- The projected future home values assume a 15-year horizon with an annual appreciation rate of {annual_growth_rate*100:.1f}%.
- “Net Asset” here is a rudimentary measure: it’s the projected future sale value minus your total cash outlays (housing plus tuition).
- Worst-case scenarios use higher interest costs (reflecting gradual prepayment), whereas best-case scenarios assume early payoff and lower interest.
- You can adjust the interest figures, growth rate, or tuition multiplier as needed to better reflect your situation.
"""

print(markdown_output)
