Roshan - Django Project Submission

This repository contains an SQLite database that has already been pushed to the repository.

If you want to start fresh, delete the following:

    Database file and the migrations folders

Available Default Users

    Superuser
    Username: admin
    Password: a

    Test User
    Username: tst
    Password: a
    
Known Issues
CartItem Quantity Bug

    The CartItem.quantity currently has a bug , where it cannot be incremented.
    Current behavior: The code hardcodes the quantity to 1, preventing users from adding a duplicate product to their cart.
