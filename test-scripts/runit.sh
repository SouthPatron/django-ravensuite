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


# ----------------- TRANSACTIONS


lwp-request ${OPTIONS} -m PUT http://localhost:8000/org/13/client/13/account/13/transactions?format=json < 04001-mk.json > 04001.resp

lwp-request ${OPTIONS} -m PUT http://localhost:8000/org/13/client/13/account/15/transactions?format=json < 04001-mk.json > 04001.resp
lwp-request ${OPTIONS} -m PUT http://localhost:8000/org/13/client/13/account/15/transactions?format=json < 04002-mk.json > 04002.resp
lwp-request ${OPTIONS} -m PUT http://localhost:8000/org/13/client/13/account/15/transactions?format=json < 04003-mk.json > 04003.resp
lwp-request ${OPTIONS} -m PUT http://localhost:8000/org/13/client/13/account/15/transactions?format=json < 04004-mk.json > 04004.resp
lwp-request ${OPTIONS} -m PUT http://localhost:8000/org/13/client/13/account/15/transactions?format=json < 04005-mk.json > 04005.resp
lwp-request ${OPTIONS} -m PUT http://localhost:8000/org/13/client/13/account/15/transactions?format=json < 04006-mk.json > 04006.resp


lwp-request ${OPTIONS} -m DELETE http://localhost:8000/org/13/client/13/account/15/transaction/11?format=json > 04007.resp

lwp-request ${OPTIONS} -m POST http://localhost:8000/org/13/client/13/account/15/transaction/13?format=json < 04008-up.json > 04008.resp
lwp-request ${OPTIONS} -m POST http://localhost:8000/org/13/client/13/account/15/transaction/13?format=json < 04009-up.json > 04009.resp



# ----------------- RESERVATIONS



lwp-request ${OPTIONS} -m PUT http://localhost:8000/org/13/client/13/account/15/reservations?format=json < 05001-mk.json > 05001.resp
lwp-request ${OPTIONS} -m PUT http://localhost:8000/org/13/client/13/account/15/reservations?format=json < 05002-mk.json > 05002.resp
lwp-request ${OPTIONS} -m PUT http://localhost:8000/org/13/client/13/account/13/reservations?format=json < 05003-mk.json > 05003.resp
lwp-request ${OPTIONS} -m PUT http://localhost:8000/org/13/client/13/account/15/reservations?format=json < 05004-mk.json > 05004.resp
lwp-request ${OPTIONS} -m PUT http://localhost:8000/org/13/client/13/account/15/reservations?format=json < 05005-mk.json > 05005.resp
lwp-request ${OPTIONS} -m PUT http://localhost:8000/org/13/client/13/account/15/reservations?format=json < 05006-mk.json > 05006.resp


lwp-request ${OPTIONS} -m POST http://localhost:8000/org/13/client/13/account/15/reservation/15?format=json < 05007-up.json > 05007.resp
lwp-request ${OPTIONS} -m POST http://localhost:8000/org/13/client/13/account/15/reservation/15?format=json < 05008-up.json > 05008.resp
lwp-request ${OPTIONS} -m POST http://localhost:8000/org/13/client/13/account/15/reservation/16?format=json < 05009-up.json > 05009.resp

lwp-request ${OPTIONS} -m PUT http://localhost:8000/org/13/client/13/account/15/reservations?format=json < 05010-mk.json > 05010.resp

lwp-request ${OPTIONS} -m DELETE http://localhost:8000/org/13/client/13/account/15/reservation/17?format=json > 05011.resp
lwp-request ${OPTIONS} -m DELETE http://localhost:8000/org/13/client/13/account/15/reservation/17?format=json > 05012.resp

lwp-request ${OPTIONS} -m POST http://localhost:8000/org/13/client/13/account/15/reservation/15?format=json < 05013-up.json > 05013.resp

lwp-request ${OPTIONS} -m POST http://localhost:8000/org/13/client/13/account/15/reservation/16?format=json < 05014-up.json > 05014.resp



