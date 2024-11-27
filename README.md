Project Setup Guide

This repository contains an SQLite database that has already been pushed to the repository. Follow the instructions below for setup and default user credentials.
Fresh Setup Instructions

If you want to start fresh, delete the following:

    The database file:
        Locate and delete the SQLite database file (e.g., db.sqlite3 or the file named in your project).
    The migrations folders:
        Found inside each app directory, typically named migrations/.

Available Default Users
Superuser

    Username: admin
    Password: a

Test User

    Username: tst
    Password: a
    
Known Issues
CartItem Quantity Bug

    The CartItem.quantity currently has a bug where it cannot be incremented.
    Current behavior: The code hardcodes the quantity to 1, preventing users from adding a duplicate product to their cart.
