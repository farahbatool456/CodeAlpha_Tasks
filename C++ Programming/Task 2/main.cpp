/*
 * ============================================================
 *  Login & Registration System in C++
 *  Author  : [Your Name]
 *  Version : 1.0
 *  Purpose : Demonstrates file handling, user authentication,
 *            input validation, and modular C++ programming.
 * ============================================================
 */

#include <iostream>
#include <fstream>
#include <string>
#include <limits>
#include <algorithm>
#include <cctype>

using namespace std;

// ─── Constants ────────────────────────────────────────────────
const string DATA_FILE      = "users.dat";   // flat-file credential store
const int    MIN_USERNAME   = 4;             // minimum username length
const int    MIN_PASSWORD   = 6;             // minimum password length

// ─── Utility: trim whitespace from both ends ──────────────────
string trim(const string& s) {
    size_t start = s.find_first_not_of(" \t\r\n");
    size_t end   = s.find_last_not_of (" \t\r\n");
    return (start == string::npos) ? "" : s.substr(start, end - start + 1);
}

// ─── Utility: clear bad input state and flush the buffer ──────
void flushInput() {
    cin.clear();
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
}

// ─── Utility: print a separator line ──────────────────────────
void printLine(char ch = '-', int width = 50) {
    cout << string(width, ch) << "\n";
}

// ─── Utility: print a boxed section header ────────────────────
void printHeader(const string& title) {
    printLine('=');
    cout << "  " << title << "\n";
    printLine('=');
}

/*
 * validateUsername()
 *   Rules: length >= MIN_USERNAME, alphanumeric + underscore only,
 *          must start with a letter.
 *   Returns true if the username passes all rules.
 */
bool validateUsername(const string& username) {
    if (username.length() < static_cast<size_t>(MIN_USERNAME)) {
        cout << "[!] Username must be at least " << MIN_USERNAME
             << " characters long.\n";
        return false;
    }
    if (!isalpha(static_cast<unsigned char>(username[0]))) {
        cout << "[!] Username must start with a letter.\n";
        return false;
    }
    for (char c : username) {
        if (!isalnum(static_cast<unsigned char>(c)) && c != '_') {
            cout << "[!] Username can only contain letters, digits, and underscores.\n";
            return false;
        }
    }
    return true;
}

/*
 * validatePassword()
 *   Rules: length >= MIN_PASSWORD, at least one digit,
 *          at least one uppercase letter.
 *   Returns true if the password passes all rules.
 */
bool validatePassword(const string& password) {
    if (password.length() < static_cast<size_t>(MIN_PASSWORD)) {
        cout << "[!] Password must be at least " << MIN_PASSWORD
             << " characters long.\n";
        return false;
    }

    bool hasDigit  = false;
    bool hasUpper  = false;

    for (char c : password) {
        if (isdigit(static_cast<unsigned char>(c))) hasDigit = true;
        if (isupper(static_cast<unsigned char>(c))) hasUpper = true;
    }

    if (!hasDigit) {
        cout << "[!] Password must contain at least one digit.\n";
        return false;
    }
    if (!hasUpper) {
        cout << "[!] Password must contain at least one uppercase letter.\n";
        return false;
    }
    return true;
}

/*
 * usernameExists()
 *   Opens the data file and scans line-by-line for an exact
 *   username match (comparison is case-insensitive).
 *   Returns true if the username is already registered.
 */
bool usernameExists(const string& username) {
    ifstream file(DATA_FILE);
    if (!file.is_open()) return false;   // file doesn't exist yet → no users

    string line;
    string targetLower = username;
    transform(targetLower.begin(), targetLower.end(), targetLower.begin(), ::tolower);

    while (getline(file, line)) {
        // each line is stored as:  username|password
        size_t delimiter = line.find('|');
        if (delimiter == string::npos) continue;

        string storedUser = line.substr(0, delimiter);
        transform(storedUser.begin(), storedUser.end(), storedUser.begin(), ::tolower);

        if (storedUser == targetLower) {
            file.close();
            return true;
        }
    }
    file.close();
    return false;
}

/*
 * registerUser()
 *   Collects username + password, runs validation, checks for
 *   duplicates, then appends the credentials to DATA_FILE.
 *
 *   NOTE: Passwords are stored in plain text here so the code
 *   stays readable for learning. In a real application you would
 *   hash them with bcrypt / Argon2 before writing to disk.
 */
void registerUser() {
    printHeader("USER REGISTRATION");

    string username, password, confirmPassword;

    // ── Username ──────────────────────────────────────────────
    cout << "  Enter username : ";
    getline(cin, username);
    username = trim(username);

    if (!validateUsername(username)) return;

    if (usernameExists(username)) {
        cout << "[!] Username '" << username
             << "' is already taken. Please choose another.\n";
        return;
    }

    // ── Password ──────────────────────────────────────────────
    cout << "  Enter password : ";
    getline(cin, password);
    password = trim(password);

    if (!validatePassword(password)) return;

    // ── Confirm password ──────────────────────────────────────
    cout << "  Confirm password : ";
    getline(cin, confirmPassword);
    confirmPassword = trim(confirmPassword);

    if (password != confirmPassword) {
        cout << "[!] Passwords do not match. Please try again.\n";
        return;
    }

    // ── Write to file ─────────────────────────────────────────
    ofstream file(DATA_FILE, ios::app);  // append mode
    if (!file.is_open()) {
        cout << "[!] Error: Could not open the data file for writing.\n";
        return;
    }

    file << username << "|" << password << "\n";
    file.close();

    printLine();
    cout << "  [+] Registration successful! Welcome, " << username << ".\n";
    printLine();
}

/*
 * loginUser()
 *   Asks for username and password, then scans DATA_FILE for
 *   a matching pair. The username check is case-insensitive;
 *   the password check is case-sensitive.
 */
void loginUser() {
    printHeader("USER LOGIN");

    string username, password;

    cout << "  Enter username : ";
    getline(cin, username);
    username = trim(username);

    cout << "  Enter password : ";
    getline(cin, password);
    password = trim(password);

    // ── Search credentials ────────────────────────────────────
    ifstream file(DATA_FILE);
    if (!file.is_open()) {
        cout << "[!] No registered users found. Please register first.\n";
        return;
    }

    string line;
    bool   found = false;
    string userLower = username;
    transform(userLower.begin(), userLower.end(), userLower.begin(), ::tolower);

    while (getline(file, line)) {
        size_t delimiter = line.find('|');
        if (delimiter == string::npos) continue;

        string storedUser = line.substr(0, delimiter);
        string storedPass = line.substr(delimiter + 1);

        string storedUserLower = storedUser;
        transform(storedUserLower.begin(), storedUserLower.end(),
                  storedUserLower.begin(), ::tolower);

        if (storedUserLower == userLower && storedPass == password) {
            found = true;
            break;
        }
    }
    file.close();

    printLine();
    if (found) {
        cout << "  [+] Login successful! Welcome back, " << username << ".\n";
    } else {
        cout << "  [-] Login failed. Invalid username or password.\n";
    }
    printLine();
}

/*
 * showMainMenu()
 *   Displays the top-level menu and returns the user's choice.
 */
int showMainMenu() {
    printLine('=');
    cout << "  C++ LOGIN & REGISTRATION SYSTEM\n";
    printLine('=');
    cout << "  [1] Register\n";
    cout << "  [2] Login\n";
    cout << "  [3] Exit\n";
    printLine();
    cout << "  Your choice: ";

    int choice = 0;
    cin >> choice;
    flushInput();   // consume leftover newline so getline works next
    return choice;
}

// ─── Entry point ──────────────────────────────────────────────
int main() {
    int choice = 0;

    do {
        cout << "\n";
        choice = showMainMenu();

        switch (choice) {
            case 1:
                cout << "\n";
                registerUser();
                break;

            case 2:
                cout << "\n";
                loginUser();
                break;

            case 3:
                printLine();
                cout << "  Goodbye! Exiting the system.\n";
                printLine();
                break;

            default:
                cout << "[!] Invalid option. Please enter 1, 2, or 3.\n";
        }

    } while (choice != 3);

    return 0;
}
