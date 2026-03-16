# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2026-03-17


### Added
<!-- New features, components, tests - one line each. Reference PRs where relevant (e.g. #12). -->

- Generate processed DuckDB Dataset. (#158)
- Add DuckDB/ibis data access layer. (#159)
- Pytest unit tests located in `dflogic.py` for #164. (#165, renaming in PR #207)
- Playwright tests for dashboard interaction in `test_dashboard_playwright.py`. (#166)
- Documentation of logic tests in `notebooks/logic_tests.ipynb`. (#167)
- New Advanced Figure panel for metric comparisons over time. (#176)
- Querychat prompt and scope experiments notebook (`notebooks/querychat_experiments.ipynb`) documenting design decisions for M4 Option A. (#163)
- README dataset description table and written demo use case. (#184, #211)
- Help button in header linking to README usage examples. (#204, #212)

### Changed

<!-- Spec or design deviations, and motivation. -->
<!-- Feedback items you addressed: "Addressed: <item description> (#<prioritization issue>) via #<PR>" -->
- Replace in‑memory filtering with DB‑backed reactive calc. (#160)
- Refactoring of `src/app.py` to extract testable functions. (#164)
- Rename risk_value column to Value_At_Risk in generated dataframes. (#194, #208)
- Update `environment.yml` and `requirements.txt` with playwright and duckdb support. (#196)
- Manual filters moved to tab-specific layout; AI Insights tab shows only AI chat sidebar. (#200, #213)

### Fixed

**Feedback prioritization issue link:** #149

A comprehensive list of feedback issues addressed for 0.4.0 along with accreditation can be found in [https://github.com/UBC-MDS/DSCI-532_2026_10_Salescope/issues/149#issuecomment-4027556013](https://github.com/UBC-MDS/DSCI-532_2026_10_Salescope/issues/149#issuecomment-4027556013).

#### Critical Issues

- Set the repo up so that each PR requires a review before merge. (#172) 
- AI chat is not scrollable yet, add this in to prevent horizontal expansion of this box. (#174)
- Remove the KPIs when the `AI Insights` tab is chosen, currently when viewing the dashboard it is difficult to see visual change between the tabs. (#175)
- Explicit indication of how the comparisons in KPIs are computed. (#178)
 

#### Non-critical Issues
- Metric comparisons over time. (#176)
- Clean up abbreviations on dashboard.  (#177)
- Add logo and colour scheme. (#179)
- Update README with more concrete usage and dataset description. (#184)
- Reorganize filter sidebar length. (#185)
- Clean up wording of helper text. (#186)
- Reduce KPI filters to single row and move Count of Datapoints. (#199)
- Replace sidebar when on AI Insights tab. (#200)
- Tooltip for churn rate reduction slider. (#203)
- Help button linking to README examples. (#204)

### Known Issues

<!-- Anything incomplete or broken TAs should be aware of (so it isn't mistaken for unfinished work). -->
When testing the app locally using the command `shiny run --reload --launch-browser src/app.py`, there is a possibility of the following error appearing:

```
File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 999, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/.../532/DSCI-532_2026_10_Salescope/src/app.py", line 17, in <module>
    from .dflogic import create_summary_table, filter_sales_data
ImportError: attempted relative import with no known parent package
```

This is a local import bug that does not affect the posit deployments. To workaround this you can either create your own posit deployment using the `main` branch of this repo or temporarily replace lines 17 and 18 in `src/app.py` with the following:

```
from dflogic import create_summary_table, filter_sales_data
from db import get_base_dataframe, execute_filtered_query
```


### Release Highlight: Querychat Customization

- **Option chosen:** A
- **Main PR:** #155
- **Supporting PRs:**
    - Design Option A (Querychat customization) in spec. (#161)
    - Implement AI behavior controls + querychat prompts. (#162)
    - Querychat prompt and scope experiments notebook (`notebooks/querychat_experiments.ipynb`) documenting design decisions for M4 Option A. (#163)
- **Why this option over the others:** This new feature provides the LLM additional context over the dataset enabling the ability to respond to more specialized queries. Persistent LLM Logging was considered for this task but would have lacked the improvement in AI answer quality and would also have added additional complexity in maintenance of an additional database. 
- **Feature prioritization issue link:** #155

A complete description for our decision to create this advanced feature and the technical functionality can be found as part of our [Milestone 4 Report](./reports/m4_spec.md).


### Collaboration

<!-- Summary of workflow or collaboration improvements made since M3. -->

- **CONTRIBUTING.md:** Updated with our M3 retrospective and M4 collaboration norms via [PR #209](https://github.com/UBC-MDS/DSCI-532_2026_10_Salescope/pull/209). The full reflection (what went well in M3, what we improved, and norms we committed to for M4) is in [CONTRIBUTING.md](CONTRIBUTING.md) under the `M3 Reflection` section. Summary of what we did in M4:

- Issue creation was more structured than in M3; a main issue in #151 was reintroduced with child issues being setup for each requirement. This resulted in far fewer additional issues having to be created as work proceeded through M4. The specific issues created exclusively as children to #151 for tracking requirements are listed below:
    - Submission setup for M4. (#152)
    - Transfer database setup to DuckDB + Parquet. (#154)
    - Implement advanced feature Querychat Customization. (#155)
    - Setup automated dashboard tests using playwright. (#156)
    - Prioritize and resolve M4 TA/Instructor/Peer Feedback. (#149)
    - Utilize this exact format for CHANGELOG and Reflection. (#157)

- We spread work across the week instead of leaving it to the last day, so we could finish before the deadline without a repeat of M3’s deadline-eve crunch.
- We refactored `src/app.py` into helper modules (`dflogic.py`, `db.py`) for maintainability and testability; see the Changed section above for details.


### Reflection

<!-- Standard (see General Guidelines): what the dashboard does well, current limitations,
     any intentional deviations from DSCI 531 visualization best practices. -->

The completed 0.4.0 version of the Salescope dashboard processes sales analytics queries efficiently and presents them in an AI-enhanced user-tested interface. Usage of a DuckDB/ibis infrastructure means that further scaling of the dataset can be handled effectively without lag typically associated with processing data entirely in the browser or app memory. Asides from the `AI Insights` tab, additional focus has been made on decisional aspects for churn risk analysis through computed recommendations and more case specific comparisons between retention strategies. Rudimentary temporal analysis is also possible with this dashboard through the date filter and the `Trends Over Time` Advanced figure, and with further time additions in time analysis would be considered. Lastly, the dashboard has been extensively documented and automatically tested in the `reports` and `tests` folders of our repository respectively.

Most visualization practices in DSCI 531 were followed. Interactivity was kept to mainly the base `plotly` functionality as there was already a high degree of complexity in the dashboard as a whole and most of the user stories could be resolved through simpler radio buttons and dropdown filters. The only significant divergence from DSCI 531 guidelines was in the scatter plot being able to show all 10000 points, creating a cluttered and noisy plot. The scatter plot in this sense works best when the data is significantly filtered, which is why the box plot was created as an accompanying plot as it can represent more data points in a more effective manner.


<!-- Trade-offs: one sentence on feedback prioritization - full rationale is in #<issue> and ### Changed above. -->
Full feedback prioritization and rationale is stored in #149. For peer feedback issues #168, #173, and #201, child issues directly addressing the feedback have been linked accordingly.

<!-- Most useful: which lecture, material, or feedback shaped your work most this milestone,
     and anything you wish had been covered. -->
In terms of feedback shaping the work on M4, many of the issues stored under #149 followed a process of referring to the relevant lecture material, then utilizing the [Shiny Python Documentation](https://shiny.posit.co/py/docs/overview.html) for more specific `ui` functions and interactions necessary. With further time, there could be more work put into the visually compact setup of the dashboard and further emphasis on how to balance the necessity for presenting key stats without overwhelming the user and including the features to go into extensive depth with our dataset.






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
