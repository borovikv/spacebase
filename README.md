# Installation

Download and unpack project.
From source directory execute
```
pip install -r requirements.txt
```

# Run Tests

```
./manage.py test
```

# Run server.
```
python manage.py runserver
```

# Task 1

Open [http://localhost:8000/admin](http://localhost:8000/admin).
Log in with credentials:

- Username: user
- Password: password

Add IBAN record. Check representation.

Log out then log in as superuser

- Username: admin
- Password: password

Check representation for the record.


# Task 2
Open [http://localhost:8000/admin/addresses/useraddress/](http://localhost:8000/admin/addresses/useraddress/).
Add UserAddress to check deduplication.

