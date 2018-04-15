[![Build Status](https://travis-ci.org/lffsantos/phone_bill.svg?branch=master)](https://travis-ci.org/lffsantos/phone_bill)

# Phone Bill

The purpose of this code is calculate phone calls and generate account for each client.

Based on history of calls of each month, the system get all calls from source , 
taking in consideration the last of tariff registered for calculate the phone bill.


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