# Salescope M4 Specification — AI Feature (Option A)

This document specifies the M4 advanced feature decision for Salescope. For testing protocols see `docs/AI_INTEGRATION_TESTING.md`. For experiment logs see `notebooks/querychat_customization.ipynb` and `notebooks/querychat_experiments.ipynb`.

---

## Why Option A (Querychat Customization)

We already had a working querychat integration from M3 — the AI Insights tab was functional but the LLM had minimal context about the dataset and no user controls over its behavior. Option A lets us go deeper on what we already built instead of adding a separate logging backend (B), a RAG pipeline (C), or a click-event handler (D).

The specific gaps in M3 that Option A fixes:
- The data_description only listed 5 of 16 columns — the LLM didn't know about `risk_value`, `Preferred_Purchase_Times`, or `Peak_Sales_Date`
- No business framing — answers were technically correct but not business-actionable
- No way for users to focus the AI on a specific area of analysis

Option B (logging) would have added value but requires setting up an external DB, which adds infra complexity without improving the actual answer quality. Option A's scope control accomplishes a similar goal (keeping the AI on topic) with less moving parts.

---

## Personas and AI Questions

These are the three main user types who would use the AI Insights tab:

**Sales Leader**
Cares about high-level revenue exposure and regional trends. Doesn't want to read through data tables — wants the AI to surface the top priorities.

Example questions:
- "Which region has the highest revenue at risk right now?"
- "Where should we focus retention spend this quarter?"

**Customer Success Lead**
Manages the retention strategies day-to-day. Wants to know which cohorts are highest churn risk and whether the current strategy is working.

Example questions:
- "Show me customers with Churn_Probability above 0.8 in North America"
- "Which retention strategy has the best average LTV for high-churn segments?"

**Data-savvy Analyst**
Comfortable with the raw data. Uses the AI tab to run quick slice-and-dice queries without writing SQL manually.

Example questions:
- "What's the average risk_value by season and region?"
- "Compare churn probability distributions across product categories"

---

## AI Controls Added (M4)

### Analysis Scope dropdown (`ai_scope_mode`)

Location: AI Insights tab, "AI Analysis Settings" card above the data table.

| Option | What it allows | Blocked | Mainly for |
|--------|---------------|---------|------------|
| Full Analysis | All questions | Nothing | Analyst |
| Churn Focus Only | Questions referencing `Churn_Probability`, `Retention_Strategy`, or `churn` | Queries on revenue/LTV/category that don't touch churn columns | Customer Success Lead |
| Revenue & LTV Focus Only | Questions referencing `Lifetime_Value`, `Average_Order_Value`, or `risk_value` | Queries on churn/retention that don't touch revenue columns | Sales Leader |

Enforcement happens via `on_tool_request` in the Shiny server — the callback checks the SQL the LLM generates and raises `ToolRejectError` if the query doesn't mention the right columns. The model then tells the user it's outside the current scope. App does not crash.

### Use AI filtered data for dashboard (existing M3 toggle)

Still present on the main sidebar. When checked, the `dashboard_df` reactive uses `ai_filtered_df()` instead of `filtered_df()`. This connects the AI's filtering to the KPI cards, heatmap, and tables on the Advanced Figures tab.

Together, the two controls give users:
1. Scope the AI's question range (new)
2. Push the AI filter into the broader dashboard (M3)

---

## Desired AI Response Format

Based on the experiment results in `notebooks/querychat_customization.ipynb`, the enhanced system prompt pushes the model toward this structure:

1. **Filter context** — what slice the query is looking at (e.g., "Looking at high-churn customers in Asia...")
2. **Key metric** — the number, usually framed in dollars or percentage (e.g., "Average risk_value is $3,241")
3. **Business takeaway** — one sentence on what to do about it (e.g., "Loyalty Program customers here have the lowest average churn — consider shifting budget toward that strategy")

The model doesn't always follow this exactly, but the `extra_instructions` constant in `app.py` pushes it in that direction by telling it users are "sales managers, not data scientists" and to frame results in terms of revenue at risk.

---

## Component Changes (M4 AI additions)

| ID | Type | Shiny widget / renderer | Depends on | Purpose |
|----|------|------------------------|------------|---------|
| `ai_scope_mode` | Input | `ui.input_select()` | — | User selects analysis scope |
| `scope_mode_info` | Output | `@render.ui` | `ai_scope_mode` | Shows current scope restriction in UI |
| `_scope` | Internal | `dict` (mutable) | `_sync_scope` effect | Carries scope value into on_tool_request callback |
| `_sync_scope` | Effect | `@reactive.effect` | `ai_scope_mode` | Keeps `_scope` in sync with dropdown |
| `_handle_tool_request` | Callback | `on_tool_request` | `_scope` | Logs + enforces scope on every LLM tool call |

The rest of the AI tab components (`ai_data_table`, `ai_tab_scatter`, `ai_tab_heatmap`, `download_ai_filtered`, `use_ai_filter`) are unchanged from M3.
