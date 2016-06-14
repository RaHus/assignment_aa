assignment_aa README
====================
A form web application in Python Pyramid framework where the customer fills in the following fields:

- Type of Customer - One of Affiliate/Direct
- Type of Contract - One Time/Monthly Retainer / Yearly Retainer
- Name
- Contact Phone

Upon Submission of the form, send emails to address X. The emails sent out have different templates per Contract Type
and Customer Type. For the templates, the system has the different templates as jinja2 files in one directory.

Additional features:

* X is configurable via 'report.recipient' configuration key .
* Mail Templates include:
    {{Contract-type }}{{customer-type}}
    Also includes all other dynamic info from the Submitted form including the db generated id.

* Showcases as many relevant pyramid features as possible
* Structured as a mid-sized pyramid app
* Full blown validation with Colander
* Mail system using pyramid_mailer
* Sample unit and functional tests
* Coverage > 95%

Getting Started
---------------
- Activate your environment

- git clone git@github.com:RaHus/assignment_aa.git

- cd assignment_aa

- $VENV/bin/pip install -e .[dev,testing]

- $VENV/bin/initialize_assignment_aa_db development.ini

- $VENV/bin/pserve development.ini

development.ini vs production.ini
---------------------------------
When serving with `development.ini` the resulting mail reports will be present under `./mail`. If you want to actually 
send the mails use `production.ini` and substitute all relevant `mail.` options (tested for gmail accounts)

