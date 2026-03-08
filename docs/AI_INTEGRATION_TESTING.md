# AI Integration Testing Document (M3)

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
