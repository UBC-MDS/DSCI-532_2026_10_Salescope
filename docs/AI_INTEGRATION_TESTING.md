# AI Integration Document (M3 + M4)

This document covers the AI-assisted filtering tab introduced in M3 and the querychat customizations added in M4 (Option A).

---

## M4 Option A: Querychat Customization

We chose Option A (Querychat Customization) over the other three options because we already had a working querychat integration from M3 and wanted to go deeper on making the AI more context-aware and controllable, rather than adding a separate logging backend or knowledge base.

### What we changed

**1. System prompt — `extra_instructions`**

The M3 `data_description` only listed 5 of the 16 dataset columns, had no business framing, and didn't mention `Value_At_Risk` at all (even though it's a key derived column in the dashboard). We added `SALESCOPE_EXTRA_INSTRUCTIONS` in `src/app.py` that gives the model:

- A definition of `Value_At_Risk = Lifetime_Value × Churn_Probability` as the primary intervention metric
- Rough churn risk thresholds (>0.7 = high)
- Instructions to frame answers in business terms (revenue at risk, not just probability values)
- The full column list so it stops hallucinating on columns like `Preferred_Purchase_Times`

Experiments in `notebooks/querychat_customization.ipynb` show the enhanced prompt produces more actionable, business-framed answers with consistent churn threshold language.

**2. `on_tool_request` hook**

Added `_handle_tool_request` in the server function (registered via `qc_vals.client.on_tool_request`). It:
- Logs every tool call (tool name + first 80 chars of SQL) to the console
- Raises `ToolRejectError` when a query doesn't match the current scope mode

The `ToolRejectError` propagates back to the model as a tool failure message, so the model tells the user it can't answer rather than silently failing or crashing.

**3. Analysis Scope dropdown (user-facing control)**

Added `ui.input_select("ai_scope_mode", ...)` to the AI Insights panel with three options:
- **Full Analysis** — no restrictions, same as M3
- **Churn Focus Only** — blocks SQL that doesn't reference churn/retention columns
- **Revenue & LTV Focus Only** — blocks SQL that doesn't reference LTV/order value columns

The scope is stored in a `_scope` dict that gets updated by a `@reactive.effect` whenever the dropdown changes. The `on_tool_request` callback reads from this dict directly, which bridges Shiny's reactive world with chatlas's synchronous callback.

*Note on table updates:* `qc_vals.df()` (and `ai_data_table`) only change when the model runs a filter/update tool. Aggregate/summary queries can answer via SQL without changing the filtered dataset.

### Design decisions and alternatives considered

See `notebooks/querychat_customization.ipynb` for the full experiment log. Key choices:

- We tried a verbosity slider first but there's no clean way to inject per-message prompt changes into querychat's existing flow without reinitializing the client.
- The scope dropdown maps naturally to real user roles (churn analyst vs. revenue manager) and uses the `on_tool_request` mechanism the assignment asks for.
- We kept the scope guard lightweight — it just checks whether the SQL string contains relevant column names, which is fast and doesn't add latency.

---

## M3 Testing Protocols

*Original M3 testing checklist below.*

This document outlines the testing protocols for the AI-assisted filtering tab introduced in Milestone 3, ensuring all LLM boundaries operate seamlessly with legacy components alongside edge-casing failure states.

**Note on Models:** 
Because output interpretation varies largely between free-tier models (like `gpt-4.1-mini`) and paid tiers (like `claude-sonnet-4-0`), ensure you accurately record the active model mapping the test to help narrow down interpretation bugs.

---

## Testing Checklist

### 1. QueryChat Interaction
- [ ] **Prompt Logging:** Test the chat interface by submitting natural language queries.
- [ ] **DF Target Logic:** Ensure the AI comprehends bounds (e.g. "Customers with Lifetime Value over 5000") and executes filter modifications across the `ai_data_table` output.

### 2. AI Filtered Data Display
- [ ] **Render:** Validate the right-hand Datagrid successfully populates the subset parsed by the LLM without throwing index errors.
- [ ] **Column Parity:** Ensure the table still contains all primary categorical markers and expected integers matching the baseline data.

### 3. File Download 
- [ ] **Export Integrity:** Use the Download button over the AI filters. Open the `.csv` and confirm the row count explicitly matches the exact parsed volume from the datatable above it rather than the full, unfiltered 10,000 row raw set.

### 4. Global Override Mapping ("Use AI filtered data for dashboard")
- [ ] **Checkbox State:** Toggle the AI override boundary checkbox on the central app logic.
- [ ] **KPI Recalibration:** Verify that checking the box aggressively hijacks the global application dataset binding (`kpi_count`, heatmap aggregates) and ignores sidebar inputs. 
- [ ] **Undo Function:** Verify that unchecking the box reverts the system back to normal sidebar manual overrides flawlessly without needing a browser refresh.

### 5. AI Empty States (Edge Cases)
- [ ] **Null Filters:** Ask the LLM to filter impossible parameters (e.g. "Find me customers with over $900,000,000 LTV"). Verify the AI successfully renders a 0-row empty dataframe instead of crashing the core `app.py` process.

### 6. Automated Evals (Future Work)
- [ ] *Optional:* If `inspect_ai` framework gets initialized, build out Python assertions tracing conversational memory mappings directly to the model container endpoint as documented in the course's automated eval syllabus block.

---

## Test Record

*Copy and paste this section per test run.*

**Date:** YYYY-MM-DD
**Model Selected:** `e.g. claude-sonnet-4-0`
**Result:** [ PASS / FAIL / BUG ]
**Tester Notes:**
> *Record any crashes or specific logic the LLM struggled to filter correctly...*
