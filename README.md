# FinSmart

FinSmart is a comprehensive personal finance management application designed to help users effectively manage their finances. Built using Django for the backend and React for the frontend, FinSmart offers a suite of features to track income, expenses, budgets, and financial goals.

## Features

- **Accounts Management**: Add and manage multiple financial accounts to keep track of your assets.
- **Transaction Tracking**: Record and categorize income and expenses for detailed financial insights.
- **Budgeting**: Set up budgets to monitor and control your spending habits.
- **Financial Goals**: Define and monitor savings goals to achieve your financial objectives.
- **Dashboard**: Visualize your financial data through interactive charts and summaries.
- **Data Import/Export**: Easily import transactions from external sources and export your financial data for backup or analysis.

## Installation

To set up the FinSmart application locally, follow these steps:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/WalkingStatue/finsmart.git
   cd finsmart
   ```

2. **Backend Setup**:

   - Ensure you have Python installed.
   - Create a virtual environment:

     ```bash
     python -m venv env
     source env/bin/activate  # On Windows, use 'env\Scripts\activate'
     ```

   - Install the required Python packages:

     ```bash
     pip install -r requirements.txt
     ```

   - Apply database migrations:

     ```bash
     python manage.py migrate
     ```

   - Create a superuser to access the Django admin panel:

     ```bash
     python manage.py createsuperuser
     ```

   - Start the Django development server:

     ```bash
     python manage.py runserver
     ```
   The application should now be accessible at `http://localhost:8080/`.
