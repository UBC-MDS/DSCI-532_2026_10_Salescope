# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - Unreleased

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

### Known Issues

### Reflection
Job Story 1 is done through the multi-tab summary table with grouping by Region, Retention Strategy, or Most Frequent Category. Job Story 2 is done with the scatterplot and sidebar filters. Job Story 3 is done with the heatmap. Layout changed from the M1 sketch to three nav panels (KPI Tables, Churn Risk Plot, Seasonal Product Heatmap) so each user story has its own view.
