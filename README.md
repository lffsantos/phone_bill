[![Build Status](https://travis-ci.org/lffsantos/phone_bill.svg?branch=master)](https://travis-ci.org/lffsantos/phone_bill)

# API to get Phone Bill 

The purpose of this code is calculate phone calls and generate account for each client.

Based on history of calls of each month, the system get all calls from source , 
taking in consideration the last of tariff registered for calculate the phone bill.
    
You can check the api documentation [here](https://github.com/lffsantos/phone_bill/blob/master/docs/api.md).


## How the system works

Exists a scheduler that run every month on the first minute,   
this job filter search all calls for every source in the last month   
and then generate the bills  
To calculate an account is used the rates registered in the database,   
this rate can be changed, but a closed account will not be recalculated  
The values of the calls are all calculated at the end of the month.  

### Pricing rules 

The call price depends on fixed charges, call duration and the time of the day that the call was made. There are two tariff times:

Standard time call - between 6h00 and 22h00 (excluding):

Standing charge: R$ 0,36 (fixed charges that are used to pay for the cost of the connection);
Call charge/minute: R$ 0,09 (there is no fractioned charge. The charge applies to each completed 60 seconds cycle).
Reduced tariff time call - between 22h00 and 6h00 (excluding):

Standing charge: R$ 0,36
Call charge/minute: R$ 0,00 (hooray!)
It's important to notice that the price rules can change from time to time, but an already calculated call price can not change.

## How to develop?

1. Clone the repository.
2. Create a virtualenv with python 3.6.
3. Activate the virtualenv.
4. Install dependencies.
5. Configure a instance .env
6. Run tests.

```console
git clone git@github.com:lffsantos/phone_bill.git phone_bill
cd phone_bill
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp contrib/env-sample .env
python manage.py test
```

## Create Database

Before load data make a database the same name registered on you file .env and execute the migrations.

> python manage.py migrate


## Load Initial Data

The project contains a sample datas for testing the system.  
Use the command

> python manage.py loaddata core

List of registered numbers: (number with call in the months of 2017)  

- 73942315278 
- 73888758690 
- 77942589011 
- 99988526423 (02/2016, 12/2017, 03/2018)
- 11894353942 


## Create SuperUser for access admin interface

> python manage.py createsuperuser


## Run Project  

> python manage.py runserver


## How to change Tariff

If you want to change the tariff is necessary access the admin interface and change the last tariff registered or add a new.
The system automatically will consider the last.

## Test 

For test you can call the command bellow for generate the phone bill if you add a new registers

> python manage.py python manage.py process_bill -m INT -y INT 

Use the option -r if you want recalculate the account  

> python manage.py python manage.py process_bill -m INT -y INT -r True


# DOCUMENTS:

[api doc](https://github.com/lffsantos/phone_bill/blob/master/docs/api.md)
[work environment](https://github.com/lffsantos/phone_bill/blob/master/docs/system_config.md)
