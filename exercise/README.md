# Family budget application

Django application that allows managing budgets consisting of incomes and expenses. 
Owner of the budget can share it with other users. 

Made with DRF.

### How to run?
* Rename .env_example file to .env and provide the secrets

* Create docker container
```bash
docker-compose build
```
* Run the container
```bash
docker-compose up -d
```
* Migrate database 
```bash
docker-compose run --rm web python manage.py migrate
```
* Create superuser for access to admin panel 
```bash
docker-compose run --rm web python manage.py createsuperuser
```
To run tests:
```bash
docker-compose run --rm web pytest
```

## API endpoints usages
Use `/register/` endpoint to create a new user.

Use `/budgets/` endpoint to list the budgets you have access to and to create a new budget.

Use `/budgets/{budgetId}` endpoint to see the  details for the specific budget and to share it with another user.

Use `/incomes/` and `/expenses/` endpoints to list the incomes or expenses of the budgets that you have access to 
or to create new incomes or expenses.  You can filter the list by `category` or `budgetId` by providing them as url kwargs.

Use `/incomes/{incomeId}` and `/expenses/{expenseId}` to see the details for the specific income/expense.

