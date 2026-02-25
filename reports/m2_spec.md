# Salescope Dashboard Specifications


## Section 1: Updated Job Stories

| #   | Job Story                       | Status         | Notes                         |
| --- | ------------------------------- | -------------- | ----------------------------- |
| 1   | When I … I want to … so I can … | ✅ Implemented |                               |
| 2   | When I … I want to … so I can … | 🔄 Revised     | Changed from X to Y because … |
| 3   | When I … I want to … so I can … | ⏳ Pending M3  |                               |

For reference, these are the user stories from milestone 1:

> **User Story 1:**
> As a **Regional Sales Director**, I want to **compare basic KPIs (such as mean, median, and maximum) for customer lifetime value, average order value, and purchase frequency across different geographic regions** so that I can **identify high-performing regions to replicate best practices and underperforming regions that need intervention**.
> **User Story 2:**
> As a **Customer Success Manager**, I want to **filter customers by churn probability thresholds and analyze which retention strategies (Loyalty Program, Discount, Email Campaign) are most effective for different risk segments** so that I can **proactively intervene with at-risk customers using the most appropriate retention approach**.
> **User Story 3:**
> As an **E-commerce Product Manager**, I want to **visualize sales patterns across product categories (Electronics, Clothing, Sports, Home) and seasons, including preferred purchase times** so that I can **optimize inventory planning for peak seasons and schedule targeted marketing campaigns during high-conversion periods**. 

## Section 2: Component Inventory

TODO: Replace each row with the components outlined in issues #56, #57, #58, #59

| ID            | Type          | Shiny widget / renderer | Depends on                   | Job story  |
| ------------- | ------------- | ----------------------- | ---------------------------- | ---------- |
| `component_1` | Input         | `ui.input_slider()`     | —                            | #1, #2     |
| `component_2` | Reactive calc | `@reactive.calc`        | `input_year`, `input_region` | #1, #2, #3 |
| `component_3` | Output        | `@render.plot`          | `filtered_df`                | #1         |
| `component_4` | Output        | `@render.data_frame`    | `filtered_df`                | #2         |
| `component_5` | Input         | `ui.input_slider()`     | —                            | #1, #2     |
| `component_6` | Reactive calc | `@reactive.calc`        | `input_year`, `input_region` | #1, #2, #3 |
| `component_7` | Output        | `@render.plot`          | `filtered_df`                | #1         |
| `component_8` | Output        | `@render.data_frame`    | `filtered_df`                | #2         |


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
