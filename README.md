# 💸 Personal Budget App

A streamlined, multi-currency personal finance dashboard built with **Streamlit** and **SQLAlchemy**. This application helps you track your net worth across different currencies (USD & PKR), manage multiple wallets, categorise transactions, and visualize your financial health in a simple, responsive interface.

## 🚀 Features

- **Multi-Currency Support**: Native support for tracking balances in **USD** and **PKR**.
- **Dashboard Overview**: 
  - Real-time Total Net Worth calculation.
  - Individual breakdowns for different currency holdings.
  - Visual cards for each wallet/account.
- **Wallet Management**: Create and manage multiple accounts (e.g., Cash, Bank, Savings) with specific currencies.
- **Transaction Tracking**: 
  - Record **Income**, **Expenses**, and **Transfers** between accounts.
  - Support for custom exchange rates during transfers.
- **Category System**: Organize transactions with a hierarchical category system (Parent/Child categories).
- **Responsive Design**: Custom CSS styling for a polished look on desktop and mobile.
- **Docker Ready**: Fully containerized for easy deployment.

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Backend & ORM**: Python, [SQLAlchemy](https://www.sqlalchemy.org/)
- **Database**: SQLite (Default) / Postgres (Supported via dependencies)
- **Data Manipulation**: Pandas

## 📂 Project Structure

```bash
personal_budget_app/
├── app.py                  # Main entry point (Dashboard)
├── pages/                  # Streamlit multi-page routes
│   ├── 1_Add_Transaction.py
│   ├── 2_Manage_Wallets.py
│   └── 3_Manage_Categories.py
├── database.py             # Database connection setup
├── models.py               # SQLAlchemy Database Models
├── crud.py                 # DB Create, Read, Update, Delete functions
├── styles.py               # Custom CSS styles
├── backup_to_gcs.sh        # Backup script
├── Dockerfile              # Container configuration
└── requirements.txt        # Python dependencies
```

## ⚡ Getting Started

### Option 1: Run Locally

1.  **Clone the repository**
    ```bash
    git clone <repository-url>
    cd personal_budget_app
    ```

2.  **Set up a virtual environment** (Recommended)
    ```bash
    # Windows
    python -m venv .venv
    .venv\Scripts\activate

    # macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Initialize the Database**
    ```bash
    python init_db.py
    ```

5.  **Run the Application**
    ```bash
    streamlit run app.py
    ```
    The app will open automatically in your browser at `http://localhost:8501`.

### Option 2: Run with Docker

1.  **Initialize the Database Locally**
    Ensure you have a `budget.db` file by running:
    ```bash
    python init_db.py
    ```

2.  **Build the Docker Image**
    ```bash
    docker build -t budget-app .
    ```

3.  **Run the Container**
    To ensure your data is saved and the app finds the database, mount the `budget.db` file:
    ```bash
    # PowerShell / Linux / Mac
    docker run -p 8080:8080 -v ${PWD}/budget.db:/app/budget.db budget-app
    ```
    Access the app at `http://localhost:8080`.

    > **Note**: Without volume mounting (`-v`), the database inside the container will be empty and erased every time the container stops.

## 📖 Usage

1.  **Dashboard**: The landing page (`app.py`) provides a high-level view of your finances.
2.  **Manage Wallets**: Navigate to the "Manage Wallets" page to create your initial accounts (e.g., "Chase Bank (USD)", "Cash (PKR)").
3.  **Manage Categories**: Set up income and expense categories to keep your transactions organized.
4.  **Add Transaction**: Log your daily spending, income, or move money between accounts using the "Add Transaction" page.

## 🗄️ Database

By default, the application uses a local **SQLite** database (`budget.db`) which is automatically created upon the first run. 

To use **PostgreSQL**:
1.  Ensure you have a Postgres database running.
2.  Modify `database.py` (or environment configuration) to point to your Postgres connection string.
3.  The `psycopg2-binary` dependency is already included in `requirements.txt`.

## 📄 License

[MIT License](LICENSE)
