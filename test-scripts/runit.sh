#!/usr/bin/env bash

OPTIONS="-s -S -e"

cd ../website;
python manage.py sqlreset org | sqlite3 ~/db/billing.db;
cd -;

rm -f ./*.resp

lwp-request ${OPTIONS} -m PUT http://localhost:8000/org/?format=json < 00001-mkorg.json > 00001.resp

lwp-request ${OPTIONS} -m PUT http://localhost:8000/org/1/clients?format=json < 00002-mkclient.json > 00002.resp

lwp-request ${OPTIONS} -m PUT http://localhost:8000/org/1/client/1/accounts?format=json < 00003-mkaccount.json > 00003.resp


