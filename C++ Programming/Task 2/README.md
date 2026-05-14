# C++ Login & Registration System

A clean, modular, and beginner-friendly console-based authentication system written in C++. This project demonstrates practical use of file handling, user input validation, duplicate detection, and structured programming.

---

## Project Overview

This system lets users **register** a new account and **log in** with existing credentials. All data is persisted to a local file (`users.dat`) using C++ `fstream`. The code is organized into focused functions with clear comments, making it easy to read, extend, and submit as a portfolio or internship project.

---

## Features

| Feature | Details |
|---|---|
| **User Registration** | Collects username + password, validates both, writes to file |
| **Duplicate Detection** | Prevents two accounts with the same username (case-insensitive check) |
| **Username Validation** | Min. 4 chars, must start with a letter, alphanumeric + underscore only |
| **Password Validation** | Min. 6 chars, must include at least one digit and one uppercase letter |
| **Password Confirmation** | User must type password twice to confirm before it is saved |
| **Secure Login** | Username match is case-insensitive; password match is case-sensitive |
| **File Handling** | Credentials stored in `users.dat` using `fstream` (append + read modes) |
| **Error Messages** | Specific, actionable feedback for every failure scenario |
| **Input Sanitization** | Whitespace trimmed from all inputs; input buffer flushed after `cin >>` |
| **Modular Code** | Each responsibility is isolated in its own function |

---

## Technologies Used

- **Language:** C++ (C++11 or later)
- **File I/O:** `<fstream>` — `ifstream` for reading, `ofstream` (append mode) for writing
- **Standard Library:** `<string>`, `<cctype>`, `<algorithm>`, `<limits>`
- **Compiler:** g++ / clang++ / MSVC (any standard-compliant compiler)

---

## File Structure

```
login_system/
├── main.cpp        ← All source code (single-file for simplicity)
├── users.dat       ← Auto-created on first registration (do NOT commit this)
└── README.md       ← This file
```

---

## How the Data File Works

Each registered user occupies one line in `users.dat`:

```
username|password
alice|Secret1
bob|Hello99
```

The `|` character acts as a delimiter between the username and password fields.

> **Security note:** Passwords are stored as plain text here to keep the code readable for learning purposes. In a production application you must hash passwords before storing them (e.g., bcrypt, Argon2, or at minimum SHA-256).

---

## Compilation & Execution

### On Linux / macOS

```bash
# Compile
g++ -std=c++11 -Wall -Wextra -o login_system main.cpp

# Run
./login_system
```

### On Windows (Command Prompt with MinGW)

```bash
g++ -std=c++11 -Wall -Wextra -o login_system.exe main.cpp
login_system.exe
```

### On Windows (Visual Studio Developer Command Prompt)

```bash
cl /EHsc /W4 main.cpp /Fe:login_system.exe
login_system.exe
```

---

## Sample Usage

```
==================================================
  C++ LOGIN & REGISTRATION SYSTEM
==================================================
  [1] Register
  [2] Login
  [3] Exit
--------------------------------------------------
  Your choice: 1

==================================================
  USER REGISTRATION
==================================================
  Enter username    : alice
  Enter password    : Secret1
  Confirm password  : Secret1
--------------------------------------------------
  [+] Registration successful! Welcome, alice.
--------------------------------------------------

  Your choice: 2

==================================================
  USER LOGIN
==================================================
  Enter username : alice
  Enter password : Secret1
--------------------------------------------------
  [+] Login successful! Welcome back, alice.
--------------------------------------------------
```

---

## Validation Rules

### Username
- Minimum **4 characters**
- Must **start with a letter** (a–z, A–Z)
- Allowed characters: **letters, digits, underscore** (`_`)
- Duplicate check is **case-insensitive** (`Alice` and `alice` are the same)

### Password
- Minimum **6 characters**
- Must contain at least **one digit** (0–9)
- Must contain at least **one uppercase letter** (A–Z)
- Confirmed by typing it a second time during registration
- Case-**sensitive** during login

---

## Error Handling

| Scenario | Message |
|---|---|
| Username too short | `Username must be at least 4 characters long.` |
| Username starts with digit/symbol | `Username must start with a letter.` |
| Invalid character in username | `Username can only contain letters, digits, and underscores.` |
| Username already registered | `Username 'X' is already taken. Please choose another.` |
| Password too short | `Password must be at least 6 characters long.` |
| Password missing digit | `Password must contain at least one digit.` |
| Password missing uppercase | `Password must contain at least one uppercase letter.` |
| Passwords don't match | `Passwords do not match. Please try again.` |
| File write error | `Error: Could not open the data file for writing.` |
| No users registered yet | `No registered users found. Please register first.` |
| Wrong credentials | `Login failed. Invalid username or password.` |

---

## Possible Extensions

- **Password hashing** — integrate a library like OpenSSL or libsodium
- **Account deletion** — rewrite file excluding the target line
- **Profile display** — store additional fields (email, date registered) separated by `|`
- **Session management** — track the currently logged-in user across menu interactions
- **Admin panel** — list all users, reset passwords

---

## Author

> Replace this section with your own details before submitting.

- **Name:** FARAH BATOOL
- **Email:** farahmughal0911@email.com
- **GitHub:** github.com/farahbatool456

---

## License

This project is released for educational use. You are free to modify and redistribute it with attribution.
