# Personal Finance Tracker

![Personal Finance Tracker](https://via.placeholder.com/728x90.png)

## Overview

The **Personal Finance Tracker** is a web-based application designed to help users track, manage, and analyze their personal finances. This app offers features like income/expense tracking, budgeting tools, savings goals, and various financial reports, all while providing a user-friendly interface.

The project is built using **Django**, with secure authentication and a responsive design to ensure seamless use across devices. The goal of this application is to help users make informed financial decisions through detailed tracking and visual representation of their finances.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Technologies](#technologies)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

---

## Features

### 1. User Authentication
- **User Sign-Up/Login**: Secure user authentication using Django’s built-in system.
- **Google Sign-In**: (Pending) OAuth integration for users to sign in via Google.
- **Password Reset**: Reset passwords securely via email.
- **Profile Management**: Update personal details and account settings.

### 2. Dashboard
- **Overview of Finances**: Summary of total income, expenses, and balance.
- **Recent Transactions**: Display the latest income/expense entries.
- **Budget Progress Bars**: Visual representation of category-based spending against the budget.

### 3. Income and Expense Tracking
- **Add Income/Expense**: Categorize and add financial entries.
- **Recurring Transactions**: (Pending) Set up recurring income/expense entries (e.g., monthly rent, salary).
- **Custom Categories**: Define personalized categories for both income and expenses.
- **Date-Based Filtering**: Filter transactions by custom date ranges (daily, weekly, monthly).

### 4. Budgeting Tools
- **Create Budgets**: Set budgets for various spending categories.
- **Budget Tracking**: Monitor budget consumption and receive alerts when nearing limits.
- **Savings Goals**: Track progress toward financial goals (e.g., saving for a vacation).

### 5. Alerts and Notifications
- **Budget Alerts**: Notifications when approaching or exceeding a budget.
- **Savings Reminders**: Reminders to contribute toward savings goals.
- **Recurring Transaction Reminders**: Alerts for upcoming recurring payments or income.

### 6. Data Visualizations
- **Spending Breakdown**: Pie charts for expense distribution across categories.
- **Income vs. Expenses**: Line and bar charts comparing income to expenses.
- **Budget Utilization**: Progress bars for budget usage.
- **Savings Goal Progress**: Visual tracker of savings goal progress.

### 7. Transaction History and Search
- **Transaction History**: Detailed transaction records with filters.
- **Search Functionality**: Search for transactions by category, amount, or keywords.

### 8. Export Data
- **Export to CSV/Excel**: Export transaction history and reports to CSV/Excel for further analysis.

### 9. Settings and Customization
- **Currency and Locale Settings**: Customize the preferred currency and locale for date formats.
- **Category Management**: Add, edit, or delete custom categories for income/expenses.

### 10. Security
- **User Data Encryption**: Encryption for sensitive user data, including passwords.
- **Two-Factor Authentication**: (Optional) Implemented for added security.
- **Data Backup and Recovery**: Mechanism to back up and recover user data.

### 11. Mobile Responsiveness
- Fully responsive design to ensure usability across mobile and desktop devices.

### 12. Reports and Analytics
- **Monthly/Yearly Reports**: Summarize income, expenses, and savings for selected time periods.
- **Custom Reports**: Generate custom financial reports based on user criteria.

---

## Installation

### Prerequisites
- **Python 3.x**
- **Django Framework**
- **SQLite/PostgreSQL** (for database)
- **Virtual Environment** (Recommended)

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/personal-finance-tracker.git
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv env
   source env/bin/activate  # For Windows: env\Scripts\activate
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure the database in `settings.py` and run migrations:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create a superuser for admin access:

   ```bash
   python manage.py createsuperuser
   ```

6. Start the development server:

   ```bash
   python manage.py runserver
   ```

---

## Usage

1. **Sign Up**: Create a new account and log in.
2. **Add Transactions**: Add income or expense entries categorized by type and date.
3. **Create Budgets**: Set budget limits for different categories.
4. **Track Progress**: Monitor your financial health via charts and progress bars.
5. **Export Data**: Export transaction history and reports to CSV/Excel.

---

## Screenshots

| Feature      | Screenshot |
|--------------|------------|
| **Dashboard** | ![Dashboard](https://via.placeholder.com/300x200) |
| **Budgeting Tools** | ![Budgets](https://via.placeholder.com/300x200) |
| **Reports** | ![Reports](https://via.placeholder.com/300x200) |

---

## Technologies

- **Backend**: Django, Python
- **Frontend**: HTML5, CSS3, JavaScript (with Bootstrap)
- **Database**: SQLite/PostgreSQL
- **Authentication**: Django’s Authentication System, Google OAuth (Pending)
- **Data Visualization**: Chart.js

---

## Roadmap

- [x] User Registration and Authentication
- [x] Income/Expense Tracking
- [x] Dashboard and Reports
- [ ] Google OAuth Integration
- [ ] Recurring Transactions
- [ ] Two-Factor Authentication
- [ ] Mobile App (PWA or React Native)

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the project.
2. Create your feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Open a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contact

For any questions or suggestions, please feel free to reach out:

- **Email**: arjunsridhar445@gmail.com
- **GitHub**: [@smooth-glitch](https://github.com/smooth-glitch)
