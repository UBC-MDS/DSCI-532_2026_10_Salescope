# Salescope Dashboard Specifications


## Section 1: Updated Job Stories

These are the user stories from milestone 1:

> **User Story 1:**
> As a **Regional Sales Director**, I want to **compare basic KPIs (such as mean, median, and maximum) for customer lifetime value, average order value, and purchase frequency across different geographic regions** so that I can **identify high-performing regions to replicate best practices and underperforming regions that need intervention**.
> **User Story 2:**
> As a **Customer Success Manager**, I want to **filter customers by churn probability thresholds and analyze which retention strategies (Loyalty Program, Discount, Email Campaign) are most effective for different risk segments** so that I can **proactively intervene with at-risk customers using the most appropriate retention approach**.
> **User Story 3:**
> As an **E-commerce Product Manager**, I want to **visualize sales patterns across product categories (Electronics, Clothing, Sports, Home) and seasons, including preferred purchase times** so that I can **optimize inventory planning for peak seasons and schedule targeted marketing campaigns during high-conversion periods**. 

And these are the updated job stories and their progress as of Milestone 2:

| #   | Job Story                       | Status         | Notes                         |
| --- | ------------------------------- | -------------- | ----------------------------- |
| 1   | When reviewing annual sales figures, I want to identify high-performing regions, so I can learn what replicate the best practices in these regions to those requiring intervention. | Planned for M2 | Table element is planned for resolving this job story.                              |
| 2   | When investigating abnormal changes in churn rate I want to determine the customers with a high risk of churn so I can infer optimal retention strategies for mitigating this risk. | Planned for M2     |  |
| 3   | When analyzing recent product sales, I want to visualize hidden patterns across product categories, seasons, and purchase times so I can optimize inventory planning for peak seasons and schedule targeted marketing campaigns during high-conversion periods. | Planned for M2  |                               |



## Section 2: Component Inventory

TODO: Replace each row with the components outlined in issues #56, #57, #58, #59

| ID            | Type          | Shiny widget / renderer | Depends on                   | Job story  |
| ------------- | ------------- | ----------------------- | ---------------------------- | ---------- |
| `user-navigation` | Navigation| `ui.navset_bar()`, `ui.navset_panel()` | —             | #1, #2, #3 |
| `slider_*` | Input            | `ui.input_slider()`        | -                         | #1, #2, #3 |
| `check_box_group_*` | Input   | `ui.input_checkbox_group()` | -                        | #1, #2, #3 |
| `date_filter` | Input        | `ui.input_date_range()`   | -                           | #1, #2, #3 |
| `reset` | Reactive Effect     | `@reactive.effect`      | `slider_*`, `check_box_group_*`, `date_filter`                | #1, #2, #3 |
| `component_5` | Input         | `ui.input_slider()`     | —                            | #1, #2     |
| `component_6` | Reactive calc | `@reactive.calc`        | `input_year`, `input_region` | #1, #2, #3 |
| `component_7` | Output        | `@render.plot`          | `filtered_df`                | #1         |
| `component_8` | Output        | `@render.data_frame`    | `filtered_df`                | #2         |

Each of the slider and checkbox components are similar to each other and represent the following components:

```
slider_* -> slider_churn, slider_customer, slider_order, slider_freq
check_box_group_* -> check_box_group_type, check_box_group_region, check_box_group_strategy
```

## Section 3: Reactivity Diagram

Draw your planned reactive graph as a [Mermaid](https://mermaid.js.org/) flowchart using the notation from Lecture 3:

- `[/Input/]` (Parallelogram) (or `[Input]` Rectangle) = reactive input
- Hexagon `{{Name}}` = `@reactive.calc` expression
- Stadium `([Name])` (or Circle) = rendered output

Example:

````markdown
```mermaid
flowchart TD
  A[/input_year/] --> F{{filtered_df}}
  B[/input_region/] --> F
  F --> P1([plot_trend])
  F --> P2([tbl_summary])
  C[/input_color/] --> P3([plot_scatter])
```
````

## Section 4: Calculation Details

For each `@reactive.calc` in your diagram, briefly describe:

- Which inputs it depends on.
- What transformation it performs (e.g., "filters rows to the selected year range and region(s)").
- Which outputs consume it.
