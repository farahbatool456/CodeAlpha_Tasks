/**
 * ============================================================
 *  CGPA Calculator — Console Application
 *  Author  : Your Name
 *  Version : 1.0
 *  Language: C++17
 * ============================================================
 *
 *  Features:
 *    - Multi-semester GPA tracking
 *    - Automatic CGPA computation
 *    - Input validation at every step
 *    - Formatted result table
 * ============================================================
 */

#include <iostream>
#include <iomanip>
#include <string>
#include <vector>
#include <limits>
#include <algorithm>

// ─────────────────────────────────────────────
//  Data Structures
// ─────────────────────────────────────────────

/**
 * Stores all details for a single course.
 */
struct Course {
    std::string name;        // e.g. "Data Structures"
    std::string letterGrade; // e.g. "A", "B+", "C"
    double      gradePoints; // numeric value mapped from letter grade
    int         creditHours; // 1 – 6
};

/**
 * Groups courses belonging to one semester.
 */
struct Semester {
    int                  number;  // semester index (1-based)
    std::vector<Course>  courses;
    double               gpa;     // computed semester GPA
};

// ─────────────────────────────────────────────
//  Grade Mapping
// ─────────────────────────────────────────────

/**
 * Converts a letter grade string to its 4.0-scale grade point.
 * Returns -1.0 if the grade is not recognised.
 *
 * Supported grades (case-insensitive):
 *   A+/A = 4.0,  A- = 3.7
 *   B+   = 3.3,  B  = 3.0,  B- = 2.7
 *   C+   = 2.3,  C  = 2.0,  C- = 1.7
 *   D+   = 1.3,  D  = 1.0
 *   F    = 0.0
 */
double gradeToPoints(const std::string& grade) {
    // Normalise to upper case
    std::string g = grade;
    std::transform(g.begin(), g.end(), g.begin(), ::toupper);

    if (g == "A+" || g == "A")  return 4.0;
    if (g == "A-")               return 3.7;
    if (g == "B+")               return 3.3;
    if (g == "B")                return 3.0;
    if (g == "B-")               return 2.7;
    if (g == "C+")               return 2.3;
    if (g == "C")                return 2.0;
    if (g == "C-")               return 1.7;
    if (g == "D+")               return 1.3;
    if (g == "D")                return 1.0;
    if (g == "F")                return 0.0;

    return -1.0; // unrecognised
}

// ─────────────────────────────────────────────
//  Input Helpers
// ─────────────────────────────────────────────

/**
 * Clears any bad state and leftover characters from std::cin.
 */
void clearInputBuffer() {
    std::cin.clear();
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

/**
 * Reads a positive integer in [min, max].
 * Keeps asking until valid input is provided.
 */
int readInt(const std::string& prompt, int minVal, int maxVal) {
    int value;
    while (true) {
        std::cout << prompt;
        if (std::cin >> value && value >= minVal && value <= maxVal) {
            clearInputBuffer();
            return value;
        }
        clearInputBuffer();
        std::cout << "  [!] Invalid input. Please enter a number between "
                  << minVal << " and " << maxVal << ".\n";
    }
}

/**
 * Reads a non-empty string from the user.
 */
std::string readString(const std::string& prompt) {
    std::string value;
    while (true) {
        std::cout << prompt;
        std::getline(std::cin, value);
        // Trim leading/trailing spaces
        size_t start = value.find_first_not_of(" \t");
        size_t end   = value.find_last_not_of(" \t");
        if (start != std::string::npos) {
            value = value.substr(start, end - start + 1);
            return value;
        }
        std::cout << "  [!] Input cannot be empty. Try again.\n";
    }
}

/**
 * Reads and validates a letter grade.
 * Loops until a recognised grade is entered.
 */
std::string readGrade(const std::string& prompt) {
    std::string grade;
    while (true) {
        std::cout << prompt;
        std::cin >> grade;
        clearInputBuffer();
        if (gradeToPoints(grade) >= 0.0) {
            // Normalise to upper case before returning
            std::transform(grade.begin(), grade.end(), grade.begin(), ::toupper);
            return grade;
        }
        std::cout << "  [!] Unrecognised grade. Valid options:\n"
                  << "      A+/A/A-  B+/B/B-  C+/C/C-  D+/D  F\n";
    }
}

// ─────────────────────────────────────────────
//  Calculation Functions
// ─────────────────────────────────────────────

/**
 * Computes the GPA for a single semester.
 *
 *   GPA = Σ(gradePoints × creditHours) / Σ(creditHours)
 */
double computeGPA(const std::vector<Course>& courses) {
    double totalPoints  = 0.0;
    int    totalCredits = 0;

    for (const auto& c : courses) {
        totalPoints  += c.gradePoints * c.creditHours;
        totalCredits += c.creditHours;
    }

    if (totalCredits == 0) return 0.0;
    return totalPoints / totalCredits;
}

/**
 * Computes the Cumulative GPA across all semesters.
 *
 *   CGPA = Σ(semesterGPA × semesterCredits) / Σ(semesterCredits)
 */
double computeCGPA(const std::vector<Semester>& semesters) {
    double totalWeightedGPA = 0.0;
    int    totalCredits     = 0;

    for (const auto& sem : semesters) {
        int semCredits = 0;
        for (const auto& c : sem.courses) semCredits += c.creditHours;

        totalWeightedGPA += sem.gpa * semCredits;
        totalCredits     += semCredits;
    }

    if (totalCredits == 0) return 0.0;
    return totalWeightedGPA / totalCredits;
}

// ─────────────────────────────────────────────
//  Display Functions
// ─────────────────────────────────────────────

/** Prints a horizontal rule of given width. */
void printRule(int width, char ch = '-') {
    std::cout << std::string(width, ch) << "\n";
}

/**
 * Displays all course details for a semester in a table,
 * followed by the semester GPA.
 */
void displaySemester(const Semester& sem) {
    const int W = 68;
    std::cout << "\n";
    printRule(W, '=');
    std::cout << "  SEMESTER " << sem.number << "\n";
    printRule(W, '=');

    // Table header
    std::cout << std::left
              << std::setw(30) << "  Course Name"
              << std::setw(10) << "Grade"
              << std::setw(14) << "Credit Hrs"
              << std::setw(14) << "Grade Pts"
              << "\n";
    printRule(W);

    int    totalCredits = 0;
    double totalPoints  = 0.0;

    for (const auto& c : sem.courses) {
        double earned = c.gradePoints * c.creditHours;
        std::cout << std::left
                  << std::setw(30) << ("  " + c.name)
                  << std::setw(10) << c.letterGrade
                  << std::setw(14) << c.creditHours
                  << std::fixed << std::setprecision(2)
                  << std::setw(14) << earned
                  << "\n";
        totalCredits += c.creditHours;
        totalPoints  += earned;
    }

    printRule(W);
    std::cout << std::left
              << std::setw(30) << "  TOTAL"
              << std::setw(10) << ""
              << std::setw(14) << totalCredits
              << std::fixed << std::setprecision(2)
              << std::setw(14) << totalPoints
              << "\n";
    printRule(W, '=');
    std::cout << "  Semester GPA : " << std::fixed << std::setprecision(2)
              << sem.gpa << " / 4.00\n";
    printRule(W, '=');
}

/**
 * Displays the final CGPA summary across all semesters.
 */
void displayCGPASummary(const std::vector<Semester>& semesters, double cgpa) {
    const int W = 68;
    std::cout << "\n\n";
    printRule(W, '*');
    // Centred title row
    std::string title = "  CGPA SUMMARY  ";
    int padding = (W - (int)title.size()) / 2;
    std::cout << std::string(padding, ' ') << title << "\n";
    printRule(W, '*');

    // Per-semester row
    std::cout << "\n"
              << std::left
              << std::setw(14) << "  Semester"
              << std::setw(22) << "Courses"
              << std::setw(16) << "Credits"
              << std::setw(16) << "GPA"
              << "\n";
    printRule(W);

    int grandCredits = 0;
    for (const auto& sem : semesters) {
        int semCredits = 0;
        for (const auto& c : sem.courses) semCredits += c.creditHours;
        grandCredits += semCredits;

        std::cout << std::left
                  << std::setw(14) << ("  " + std::to_string(sem.number))
                  << std::setw(22) << sem.courses.size()
                  << std::setw(16) << semCredits
                  << std::fixed << std::setprecision(2)
                  << std::setw(16) << sem.gpa
                  << "\n";
    }

    printRule(W);
    std::cout << "  Total Semesters : " << semesters.size()         << "\n"
              << "  Total Credits   : " << grandCredits              << "\n"
              << "  Cumulative CGPA : " << std::fixed
                                        << std::setprecision(2)
                                        << cgpa << " / 4.00\n";

    // Simple grade remark
    std::string remark;
    if      (cgpa >= 3.7) remark = "Excellent  — Dean's List quality";
    else if (cgpa >= 3.3) remark = "Very Good  — Strong academic standing";
    else if (cgpa >= 3.0) remark = "Good       — Above average";
    else if (cgpa >= 2.5) remark = "Satisfactory";
    else if (cgpa >= 2.0) remark = "Passing    — Needs improvement";
    else                  remark = "Below passing threshold";

    std::cout << "  Remarks         : " << remark << "\n";
    printRule(W, '*');
}

// ─────────────────────────────────────────────
//  Semester Input
// ─────────────────────────────────────────────

/**
 * Collects course data for one semester from the user
 * and returns a fully populated Semester object.
 */
Semester inputSemester(int semNumber) {
    Semester sem;
    sem.number = semNumber;

    std::cout << "\n--- Semester " << semNumber << " ---\n";

    int numCourses = readInt("  How many courses this semester? (1-20): ", 1, 20);

    for (int i = 1; i <= numCourses; ++i) {
        Course c;
        std::cout << "\n  Course " << i << ":\n";
        c.name        = readString("    Name        : ");
        c.letterGrade = readGrade("    Grade       : ");
        c.gradePoints = gradeToPoints(c.letterGrade);
        c.creditHours = readInt("    Credit Hrs  : ", 1, 6);
        sem.courses.push_back(c);
    }

    sem.gpa = computeGPA(sem.courses);
    return sem;
}

// ─────────────────────────────────────────────
//  Banner
// ─────────────────────────────────────────────

void printBanner() {
    std::cout << "\n";
    std::cout << "  ╔══════════════════════════════════════════════════════════╗\n";
    std::cout << "  ║           C G P A   C A L C U L A T O R                 ║\n";
    std::cout << "  ║         Console Application  —  C++17                   ║\n";
    std::cout << "  ╚══════════════════════════════════════════════════════════╝\n";
    std::cout << "\n";
    std::cout << "  Grading Scale (4.0 System)\n";
    std::cout << "  A+/A=4.0  A-=3.7  B+=3.3  B=3.0  B-=2.7\n";
    std::cout << "  C+=2.3    C=2.0   C-=1.7  D+=1.3  D=1.0  F=0.0\n";
    std::cout << "\n";
}

// ─────────────────────────────────────────────
//  Main
// ─────────────────────────────────────────────

int main() {
    printBanner();

    int numSemesters = readInt("  Enter number of semesters to calculate (1-20): ", 1, 20);

    std::vector<Semester> semesters;
    semesters.reserve(numSemesters);

    // Collect data for each semester
    for (int i = 1; i <= numSemesters; ++i) {
        semesters.push_back(inputSemester(i));
    }

    // Display each semester's result
    std::cout << "\n\n";
    std::cout << "  ══════════════════════ RESULTS ══════════════════════\n";
    for (const auto& sem : semesters) {
        displaySemester(sem);
    }

    // Compute and display overall CGPA
    double cgpa = computeCGPA(semesters);
    displayCGPASummary(semesters, cgpa);

    std::cout << "\n  Thank you for using the CGPA Calculator. Good luck!\n\n";
    return 0;
}
