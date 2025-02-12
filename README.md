 # Pedmonie Django Backend API

## Project Overview

The Pedmonie Django Backend API is a Django-based analytics service designed to provide insights into critical business areas, including:

- **Sales Performance Analytics**  
  - **Revenue Trends:** Track overall sales performance over time (e.g., daily, weekly, monthly, quarterly). Show revenue growth or decline trends to help vendors understand performance.  
  - **Sales by Product:** Display which renewable energy products (solar panels, wind turbines, batteries, etc.) are generating the most revenue.  
  - **Sales by Region/Location:** Identify which geographic areas or markets are generating the most sales, useful for targeting specific regions.  
  - **Sales by Time of Year:** Renewable energy products may have seasonal trends (e.g., increased sales in summer for solar products). Track sales spikes or dips during different times of the year.  

- **Product Performance Analytics**  
  - **Top-Selling Products:** List products that are selling the most, helping vendors understand demand patterns.  
  - **Product Views and Engagement:** Track how many views or interactions a product page receives, which can help understand customer interest even if sales haven’t been made yet.  
  - **Profit Margin by Product:** Show how profitable each product is by calculating the margin between cost and sales price.  

- **Marketing & Conversion Analytics**  
  - **Cart Abandonment Rate:** Track how many customers add products to the cart but leave without purchasing.  

- **Profitability & Financial Analytics**  
  - **Gross Profit and Net Profit:** Track gross and net profits over time, showing how operational costs are affecting profitability.  

It empowers businesses with advanced features such as filtering, data aggregation, and reporting to optimize strategies and monitor key metrics effectively.


## Live Link

[API Live Demo](https://codebrewmaster.pythonanywhere.com/api/v1)

## Documentation Link

[Postman API Documentation](https://documenter.getpostman.com/view/36548151/2sAYBPmZm1)

---

## Installation Instructions

### Prerequisites

Ensure the following tools are installed:

- Python (>= 3.9 recommended)
- pip (Python package manager)
- Git
- Virtual environment tool (e.g., `venv` or `virtualenv`)
- MySQL

### How to Run the API Locally

1. **Clone the repository:**

    ```bash
    git clone https://github.com/InternPulse/pedmonie-django-backend.git
    cd pedmonie-django-backend
    ```

2. **Set up a virtual environment:**

    **Windows:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

    **macOS/Linux:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database:**

    ```bash
    python manage.py migrate
    ```

5. **Start the server:**

    ```bash
    python manage.py runserver
    ```

    The API will be available at `http://127.0.0.1:8000/`.

---

## Features

- **Advanced Analytics:** Provides insights into key performance metrics.
- **REST API:** Enables querying and managing analytics data.
- **Filters:** Supports filtering by dates, products, and profitability.
- **Data Aggregation:** Converts raw data into actionable insights.
- **Reporting:** Offers downloadable and visual reports.

---

## Usage

- Access the API locally at `http://127.0.0.1:8000/` or via the [Live Link](https://codebrewmaster.pythonanywhere.com/api/v1).
- Test endpoints using tools like Postman, cURL, or other API testing utilities.
- Refer to the [API Documentation](https://documenter.getpostman.com/view/36548151/2sAYBPmZm1) for detailed instructions.

---

## API Endpoints

**Base URL:** `http://127.0.0.1:8000/api/v1/`

| Endpoint                                    | Method | Description                           |
|---------------------------------------------|--------|---------------------------------------|
| `/financial/analytics/`                     | GET    | Fetch all financial analytics records.|
| `/financial/analytics/top_products/`        | GET    | Get top products by profitability.    |
| `/financial/analytics/?year=2022`           | GET    | Filter analytics by year.             |
| `/financial/analytics/?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD` | GET | Filter analytics by date range.       |
| `/financial/analytics/profit_records/`      | GET    | Fetch records with profit only.       |
| `/financial/analytics/selling_at_loss/`     | GET    | Fetch records with losses only.       |

For a comprehensive list, refer to the [API Documentation](https://documenter.getpostman.com/view/36548151/2sAYBPmZm1).

---

## Project Structure

```plaintext
renergy-hub-django-backend/
├── analytics_service/
│   ├── sales_performance/      # Sales Performance Analytics
│   ├── product_performance/    # Product Performance Analytics
│   ├── marketing_conversion/   # Marketing Analytics
│   ├── profitability_financial/ # Financial Analytics
│   ├── shared/                 # Shared utilities and helpers
├── manage.py                   # Django entry point
├── requirements.txt            # Python dependencies
└── ...
```

---

## Environment Variables

Create a `.env` file in the root directory with the following keys:

```bash
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# MySQL
DB_NAME=your-database-name
DB_USER=your-database-user
DB_PASSWORD=your-database-password
DB_HOST=localhost
DB_PORT=5432
```

---

## Contributions

Contributions are welcome! If you’re interested:

1. Create an issue or comment on the repository to let others know what you're working on to avoid overlapping efforts.
2. Follow the steps outlined below to contribute.

### Contribution Guidelines

1. **Clone the repository:**

    ```bash
    git clone https://github.com/InternPulse/renergy-hub-django-backend.git
    ```

2. **Set the origin branch:**

    ```bash
    git remote add origin https://github.com/InternPulse/renergy-hub-django-backend.git
    git pull origin dev
    ```

3. **Create a new branch for your task:**

    ```bash
    git checkout -b BA-001/Feat/Sign-Up-Form
    ```

4. **Make your changes and commit:**

    ```bash
    git add .
    git commit -m "your commit message"
    ```

5. **Sync with the dev branch to avoid conflicts:**

    ```bash
    git pull origin dev
    ```

6. **Push your branch:**

    ```bash
    git push -u origin BA-001/Feat/Sign-Up-Form
    ```

7. **Create a pull request to the dev branch.** Ensure the PR description is clear and includes test instructions.

---

## Commit Standards and Guidelines

### Commit Cheat Sheet

| Type      | Description                                  |
|-----------|----------------------------------------------|
| `feat`    | Features: A new feature                     |
| `fix`     | Bug Fixes: A bug fix                        |
| `docs`    | Documentation: Documentation-only changes   |
| `style`   | Styles: Formatting or cosmetic changes      |
| `refactor`| Code Refactoring: Neither fixes a bug nor adds a feature |
| `perf`    | Performance: Optimizes performance          |
| `test`    | Tests: Adding or updating tests             |
| `build`   | Builds: Changes to build tools or dependencies |
| `ci`      | CI: Updates to CI configurations            |
| `chore`   | Chores: Maintenance or configuration tasks  |
| `revert`  | Reverts: Reverts a previous commit          |

### Sample Commit Messages

- `chore: Update README file – Maintenance task.`
- `feat: Add user registration endpoint – New feature added.`

---

## License

This project is licensed under the MIT License.
