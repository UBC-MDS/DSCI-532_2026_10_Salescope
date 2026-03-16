# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2026-03-17

### Added
- Generate processed DuckDB Dataset. (#158)
- Add DuckDB/ibis data access layer. (#159)
- Pytest unit tests in `dflogic.py` (#165, renaming in PR #207)
- Playwright tests for dashboard interaction in `test_dashboard_playwright.py`. (#166)
- Documentation of logic tests in `notebooks/logic_tests.ipynb`. (#167)
- New Advanced Figure panel for metric comparisons over time. (#176)
- Querychat prompt and scope experiments notebook (`notebooks/querychat_experiments.ipynb`) documenting design decisions for M4 Option A. (#163)
- README dataset description table and written demo use case. (#184, #211)
- Help button in header linking to README usage examples. (#204, #212)

### Changed
- Replace in-memory filtering with DB-backed reactive calc. (#160)
- Refactoring of `src/app.py` to extract testable functions. (#164)
- Rename risk_value column to Value_At_Risk in generated dataframes. (#194, #208)
- Update `environment.yml` and `requirements.txt` with playwright and duckdb support. (#196)
- Manual filters moved to tab-specific layout; AI Insights tab shows only AI chat sidebar. (#200, #213)

### Fixed

**Feedback prioritization issue link:** #149

A comprehensive list of feedback issues addressed for 0.4.0 along with accreditation can be found in [issue #149](https://github.com/UBC-MDS/DSCI-532_2026_10_Salescope/issues/149#issuecomment-4027556013).

#### Critical Issues
- Set the repo so each PR requires a review before merge. (#172)
- AI chat scrollable to prevent horizontal expansion. (#174)
- Remove KPIs when AI Insights tab is chosen. (#175)
- Explicit indication of how KPI comparisons are computed. (#178)

#### Non-critical Issues
- Metric comparisons over time. (#176)
- Clean up abbreviations on dashboard. (#177)
- Add logo and colour scheme. (#179)
- Update README with usage and dataset description. (#184)
- Reorganize filter sidebar length. (#185)
- Clean up wording of helper text. (#186)
- Reduce KPI filters to single row and move Count of Datapoints. (#199)
- Replace sidebar when on AI Insights tab. (#200)
- Tooltip for churn rate reduction slider. (#203)
- Help button linking to README examples. (#204)

### Known Issues

Within `tests/test_dashboard_playwright.py`, the tests `test_retention_strategy_filter_two_values` and `test_reset_button_restores_defaults` require selecting the `Key Metrics Table` to the `Region` option even though this is technically not checked in the test. Removing these lines will result in the following error, and the cause is currently unknown as manually trying this test on the dashboard shows that the text is rendering as expected.

```
Call log:
E         - Expect "to_have_text" with timeout 15000ms
E         - waiting for locator("#kpi_note")
E           6 × locator resolved to <div id="kpi_note" aria-live="polite" class="shiny-html-output shiny-bound-output recalculating"></div>
E             - unexpected value ""
```

### Release Highlight: Querychat Customization
- **Option chosen:** A
- **Main PR:** #155
- **Supporting PRs:** Design Option A in spec (#161), AI controls and prompts (#162), experiments notebook (#163)
- **Why this option:** Gives the LLM full dataset context and user controls; persistent LLM logging would add infra without the same answer-quality gain. Feature prioritization: #155. Full description: [reports/m4_spec.md](./reports/m4_spec.md).

### Collaboration

- **CONTRIBUTING.md:** Updated with M3 retrospective and M4 norms via [PR #209](https://github.com/UBC-MDS/DSCI-532_2026_10_Salescope/pull/209). Summary: issue creation more structured (#151 + child issues), work spread across the week, `src/app.py` refactored into `dflogic.py` and `db.py`.
- **Spec and design before code.** For Option A we updated `reports/m4_spec.md` and #155 before implementing. For DuckDB/Parquet (#154) we had the pipeline and `db.py` design before wiring the app. For Playwright (#156) we added tests alongside the spec. For some feedback items we fixed first then updated CHANGELOG/spec; we aimed for spec-first on larger features. (#215)

### Reflection

The completed 0.4.0 dashboard processes sales analytics efficiently and presents them in an AI-enhanced, tested interface. DuckDB/ibis allows scaling without in-memory lag. Beyond the AI Insights tab we focused on churn risk decisions (recommendations, retention strategy comparisons). Temporal analysis is supported via the date filter and Trends Over Time figure. The repo is documented in `reports/` and `tests/`.

Most DSCI 531 visualization practices were followed. The main divergence is the scatter plot showing all 10k points (noisy when unfiltered); the box plot complements it for dense data. Full feedback prioritization and rationale: #149.

**Tests.** The Playwright tests in `test_dashboard_playwright.py` cover the dashboard UI: initial KPI count, Key Metric Tables structure and cell values, region/purchase type/retention strategy filters, row dropdown grouping, and reset button behaviour. The logic tests in `logic_tests.py` cover `normalize_range`, `create_summary_table`, and `filter_sales_data` in `dflogic.py`. If those behaviours regress, filter state and KPI summaries could be wrong or the app could show incorrect aggregates. (#214)

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
