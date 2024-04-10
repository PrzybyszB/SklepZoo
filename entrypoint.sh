#!/bin/bash

# We invoke a Python script and save the result to a variable
result=$(python3 src/check_db.py)

# We check the result returned by the Python script
if [[ "$result" == "Database exist" ]]; then
    echo "Database exist"
else
    echo "Database doeasn't exist. Initialize db"
    python src/init_db.py
    flask db init
    flask db migrate -m 'Initial migration.'
    flask db upgrade
fi

exec gunicorn -w 6 -b 0.0.0.0 --access-logfile=- 'src:create_app()'
