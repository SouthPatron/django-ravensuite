#!/usr/bin/env bash

OPTIONS="-s -S -e"

cd ../website;
python manage.py sqlreset org | sqlite3 ~/db/billing.db;
cd -;

rm -f ./*.resp

# ----------------- ORGANIZATION

lwp-request ${OPTIONS} -m PUT http://localhost:8000/org/?format=json < 01001-mk.json > 01001.resp
lwp-request ${OPTIONS} -m PUT http://localhost:8000/org/?format=json < 01002-mk.json > 01002.resp
lwp-request ${OPTIONS} -m PUT http://localhost:8000/org/?format=json < 01003-mk.json > 01003.resp

lwp-request ${OPTIONS} -m DELETE http://localhost:8000/org/12?format=json > 01004.resp

lwp-request ${OPTIONS} -m POST http://localhost:8000/org/11?format=json < 01005-up.json > 01005.resp
lwp-request ${OPTIONS} -m POST http://localhost:8000/org/13?format=json < 01006-up.json > 01006.resp


# ----------------- CLIENT

lwp-request ${OPTIONS} -m PUT http://localhost:8000/org/13/clients?format=json < 02001-mk.json > 02001.resp
lwp-request ${OPTIONS} -m PUT http://localhost:8000/org/13/clients?format=json < 02002-mk.json > 02002.resp
lwp-request ${OPTIONS} -m PUT http://localhost:8000/org/13/clients?format=json < 02003-mk.json > 02003.resp

lwp-request ${OPTIONS} -m DELETE http://localhost:8000/org/13/client/12?format=json > 02004.resp

lwp-request ${OPTIONS} -m POST http://localhost:8000/org/13/client/11?format=json < 02005-up.json > 02005.resp
lwp-request ${OPTIONS} -m POST http://localhost:8000/org/13/client/13?format=json < 02006-up.json > 02006.resp

lwp-request ${OPTIONS} -m PUT http://localhost:8000/org/11/clients?format=json < 02007-mk.json > 02007.resp


# ----------------- ACCOUNTS


lwp-request ${OPTIONS} -m PUT http://localhost:8000/org/11/client/11/accounts?format=json < 03001-mk.json > 03001.resp
lwp-request ${OPTIONS} -m PUT http://localhost:8000/org/11/client/11/accounts?format=json < 03002-mk.json > 03002.resp
lwp-request ${OPTIONS} -m PUT http://localhost:8000/org/13/client/13/accounts?format=json < 03003-mk.json > 03003.resp
lwp-request ${OPTIONS} -m PUT http://localhost:8000/org/13/client/13/accounts?format=json < 03004-mk.json > 03004.resp
lwp-request ${OPTIONS} -m PUT http://localhost:8000/org/13/client/13/accounts?format=json < 03005-mk.json > 03005.resp


lwp-request ${OPTIONS} -m DELETE http://localhost:8000/org/13/client/13/account/14?format=json > 03006.resp
lwp-request ${OPTIONS} -m DELETE http://localhost:8000/org/11/client/11/account/11?format=json > 03007.resp
lwp-request ${OPTIONS} -m DELETE http://localhost:8000/org/11/client/11/account/11?format=json > 03008.resp


lwp-request ${OPTIONS} -m POST http://localhost:8000/org/13/client/13/account/13?format=json < 03009-up.json > 03009.resp
lwp-request ${OPTIONS} -m POST http://localhost:8000/org/13/client/13/account/15?format=json < 03010-up.json > 03010.resp

exit 0



lwp-request ${OPTIONS} -m PUT http://localhost:8000/org/1/clients?format=json < 00002-mkclient.json > 00002.resp

lwp-request ${OPTIONS} -m PUT http://localhost:8000/org/1/client/1/accounts?format=json < 00003-mkaccount.json > 00003.resp

lwp-request ${OPTIONS} -m PUT http://localhost:8000/org/1/client/1/account/1/transactions?format=json < 00004-mktrans.json > 00004.resp

lwp-request ${OPTIONS} -m PUT http://localhost:8000/org/1/client/1/account/1/transactions?format=json < 00005-mktrans.json > 00005.resp

lwp-request ${OPTIONS} -m PUT http://localhost:8000/org/1/client/1/account/1/transactions?format=json < 00006-mktrans.json > 00006.resp

lwp-request ${OPTIONS} -m PUT http://localhost:8000/org/1/client/1/account/1/reservations?format=json < 00007-mkres.json > 00007.resp

lwp-request ${OPTIONS} -m PUT http://localhost:8000/org/1/client/1/account/1/reservations?format=json < 00008-mkres.json > 00008.resp

lwp-request ${OPTIONS} -m PUT http://localhost:8000/org/1/client/1/account/1/reservations?format=json < 00009-mkres.json > 00009.resp


