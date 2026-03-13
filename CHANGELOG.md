# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2026-03-XX

### Added
- Querychat prompt and scope experiments notebook (`notebooks/querychat_experiments.ipynb`) documenting design decisions for M4 Option A. (#163)

## [0.3.0] - 2026-03-08

### Added
- New 'AI Insights' page for filtering supported by `querychat` (#91, #96), alongside accompanying specialized AI plots. (#135, #137) 
- Option to use the AI filtered dataframe in Advanced Figures. (#92, #93, #94, #95)
- Added `docs/AI_INTEGRATION_TESTING.md` containing manual AI checklist evaluation protocols (#97).
- Replaced the previous churn rate range slider with two independent numerical inputs and a new "Churn rate decrease (%)" slider to directly simulate churn reduction models (#98).
- Added a quartile box plot alongside the scatter plot in the Churn Risk Plot tab to show churn probability distributions across retention strategies (#99).
- Added comparison subtext to the main KPIs indicating the metric delta (amount and direction) when the churn decrease slider is active (#103).
- Default filter view set to most recent quarter; reset button restores to this default (#104).
- Added Q1–Q4 quarter bubbles visualization to track dynamic performance clusters by season (#127).
- Added decision-making `Recommendations` section. (#130) 
- Added scatter plot in AI Insights tab using querychat filtered dataframe (#135).
- Added heatmap (Season × Category, mean LTV) in AI Insights tab using querychat filtered dataframe (#137).


### Changed
- Environment update to support the AI integration. (#90)
- Reduced size of the `Count Datapoints` KPI and added low sample size warnings. (#100)
- Restored default text size for improved readability across dashboard text and KPI labels (#101, #124).
- Clarified KPI labels and chart titles to reflect filtered segments and units (#102).
- Reworked the Churn Risk Plot to color points by their status ("In Range" vs "Excluded") whenever the churn decrease slider is active, making it easier to see which customers are impacted by the simulated churn reduction (#105).
- De-emphasized the "Count of Datapoints" KPI to keep main analytics prominent (#125).
- Replaced CLV, AOV, and Purchase Frequency sliders with numeric input pairs for consistency with churn controls (#126).
- Added "Customer Retention & Churn Insights" to the primary app title parameter and injected a markdown subheading to immediately convey dashboard context without necessitating sidebar reference (#128).
- Added red/green color coding to the KPI comparison delta subtext to quickly indicate positive or negative performance changes (#129).

## [0.2.0] - 2026-02-28

### Added
- Interactive Plotly scatterplot for the Churn Risk Plot tab showing customer Lifetime Value vs Days Between Purchases, colored by Retention Strategy and sized by Churn Probability
- Central `filtered_df()` reactive function that applies all sidebar filters and feeds every output in the dashboard
- Numeric slider filters for Churn Rate, Customer Lifetime Value, Average Order Value, and Purchase Frequency
- Categorical checkbox filters for Region, Retention Strategy, and Most Common Purchase Type
- Interactive heatmap showing average customer value by Season and Product Category
- Multi-tab summary table with grouping by Region, Retention Strategy, or Most Frequent Category
- KPI value boxes showing live counts of filtered datapoints
- Two Posit Connect Cloud deployments: stable on `main` and auto-updating on `dev`

### Changed
- Replaced single-page layout from the M1 sketch with a tabbed navigation system (`ui.navset_bar()` with three `ui.nav_panel()` views: KPI/Tables, Churn Risk Plot, Seasonal Product Heatmap) to reduce cognitive load and give each complex visual adequate screen real estate.
- Removed `ridgeplot` dependency; ridge plot was dropped in favour of the interactive Plotly scatterplot which better serves the churn-risk job story.

### Known Issues
- The app layout may look slightly cramped on very mobile-sized screens due to the multi-column configurations.

### Reflection
**1. Implementation Status:** We have successfully implemented all core components planned for the M2 proposal. Job Story 1 is fulfilled by the multi-tab interactive summary table. Job Story 2 is fulfilled by the interactive plotly scatterplot and a combination of numeric sliders (ex. Churn Rate). Job Story 3 is fulfilled by the seasonal heatmap that toggles between metric aggregations. All global filters safely push state downwards to these components through the central `filtered_df` reactive calculation. 

**2. Deviations:** We primarily deviated from our M1 Sketch layout. Instead of cramming all charts onto a single dashboard view, we adopted a tabbed navigation system (`ui.navset_bar`) with three distinct views (KPI/Tables, Churn Risk Plot, Seasonal Product Heatmap). We made this change to heavily reduce cognitive load on the user and give the complex visual components (like the heatmap and side-by-side tables) adequate screen real estate.

**3. Known Issues:** When users rapidly change multiple checkbox filters, the app may briefly stutter while recalculating the `filtered_df`. Additionally, edge cases exist where filtering leaves zero rows, but the Plotly charts now handle this gracefully with empty state titles instead of crashing.

**4. Best Practices:** We consciously deviated from standard monochromatic color scales in our scatterplot, utilizing a categorical color mapping (`Retention_Strategy`) alongside varying marker sizes (`Churn_Probability`). While multiple encodings can sometimes clutter a plot according to standard visualization rules, we justified this to ensure stakeholders could spot high-risk outliers across disparate retention campaigns immediately at a glance. We adhered strictly to DSCI-531 guidelines regarding clear axis labeling.

**5. Self-Assessment:** Our current technical strength lies in the robust, centralized reactivity pipeline which ensures flawless state management across the app. Our primary limitation is the somewhat generic aesthetic styling; the app currently relies mostly on default Shiny themes. For future improvements in M3, we plan to implement custom CSS to refine the user interface and add actionable UX components like a "Reset Filters" button, directly addressing recent TA feedback.
