# Phone Bill



[![Build Status](https://travis-ci.org/lffsantos/phone_bill.svg?branch=master)](https://travis-ci.org/lffsantos/phone_bill)


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
