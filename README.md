# DSCI-532_2026_10_Salescope

## Overview

Salescope is an interactive dashboard that helps e-commerce businesses understand their customers better and reduce churn. Regional sales directors can compare performance across different territories, while customer success managers can identify at-risk customers and evaluate which retention strategies work best. The dashboard visualizes purchasing patterns by product category, season, and customer segment to support data-driven decisions about inventory planning and marketing campaigns.

## Deployments

A stable deployment from the `main` branch can be viewed at [https://019c8d13-5610-dd58-6134-331453179c0e.share.connect.posit.cloud](https://019c8d13-5610-dd58-6134-331453179c0e.share.connect.posit.cloud)

An updating deployment from the `dev` branch can be viewed at [https://019c8d16-a100-6bb9-8eb5-58c6097addfa.share.connect.posit.cloud](https://019c8d16-a100-6bb9-8eb5-58c6097addfa.share.connect.posit.cloud)

## Dataset

We use the [Sales and Customer Insights](https://www.kaggle.com/datasets/imranalishahh/sales-and-customer-insights) dataset from Kaggle, which contains 10,000 customer records with purchasing behavior and engagement metrics.

## Team

This dashboard is developed by Group 10 for DSCI 532:
- Alexander Wen ([@alxwen711](https://github.com/alxwen711))
- Tirth Joshi ([@tirthjoship](https://github.com/tirthjoship))
- Songyang Yu ([@Spanorti08](https://github.com/Spanorti08))
- Raghav Gupta ([@raghav9048](https://github.com/raghav9048))

## Demo

<video controls>
  <source src="img/demo.mp4" type="video/mp4">
</video>

## How to Run Locally

Follow these steps to set up and run the Salescope dashboard on your local machine:

### 1. Clone the Repository

```bash
git clone https://github.com/UBC-MDS/DSCI-532_2026_10_Salescope.git
cd DSCI-532_2026_10_Salescope
```

### 2. Create the Environment

Create a conda environment using the provided `environment.yml` file:

```bash
conda env create -f environment.yml
conda activate Salescope
```

### 3. Verify the Data

The dataset is already included in the repository at `data/raw/sales_and_customer_insights.csv`. You can verify it exists by checking:

```bash
ls data/raw/
```

### 4. Run the Dashboard

Start the Shiny dashboard application:

```bash
shiny run --reload --launch-browser src/app.py
```

The dashboard will automatically open in your default web browser. If it does not open automatically, navigate to the URL shown in the terminal (typically `http://127.0.0.1:8000`).

## License

Licensed under the MIT License. See [LICENSE](LICENSE) for details.
