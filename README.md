# **Mandiri Securitas – Technical Test**
### Haikal Ramadhan Usman

This is a Technical test for Mandiri Securitas. The code will install postgresql, python, Plotly Dash and Metabase for showing the dashboards.

## How to Run the Code
1. Clone the github repository 
```bash
git clone https://github.com/Khal-Ramaus/Amartek__Mandiri_Sekuritas.git
```
2. Run Docker Compose to Install all dependencies. This command will install postgresql, python, Plotly Dash and Metabase for showing the dashboards. It will also run `.\app\load_data.py` to process and load CRMCallCenterLogs.csv, CRMEvents.csv and LuxuryLoanPortfolio.csv dataframes to postgresql
```bash
docker compose up --build
```
3. Open http://localhost:3000/ in your browser. It will open metabase. 
    * Select your preferred language. 
    * Enter your credentials such as First Name, Last Name, email, Company name, and password
    * Input Connection Detail.
        - **Database type** -> PostgreSQL
        - **Display Name**
        - **Host** -> db
        - **Port** -> 5432
        - **Database Name** -> mydb
        - **username** -> user
        - **password** -> password
    * To create dashboard for task 2, click **New** button and then choose **SQL Query.** Select database name based on **Display Name** that you entered in the Connection Detail, and copy and paste sql query from folder `.\app\query\`
4. Open http://localhost:8050/ in your browser to see all dashboards for task 2
5. All my answers for all the tasks is provided in file `.\Mandiri Sekuritas - Technical Test.pdf`