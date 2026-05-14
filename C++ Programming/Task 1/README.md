# 📊 CGPA Calculator

A console-based C++ application that helps students calculate their semester GPA and cumulative CGPA accurately — with clean input validation, formatted output tables, and support for multiple semesters.

---

## 📌 Project Overview

Managing academic performance manually is error-prone. This tool automates GPA and CGPA calculations using the standard 4.0 grading scale. Students enter their course name, grade, and credit hours; the program handles all the math and displays results in a structured, easy-to-read format.

The project is intentionally written to be beginner-friendly — every function has a clear purpose, every block of logic is commented, and no external libraries are required.

---

## ✅ Features

| Feature | Description |
|---|---|
| Multi-semester support | Track GPA across 1–20 semesters in one session |
| Full grade scale | Supports A+, A, A−, B+, B, B−, C+, C, C−, D+, D, F |
| Automatic GPA calculation | Computes weighted GPA per semester |
| Cumulative CGPA | Accurately aggregates GPA across all semesters |
| Input validation | Rejects invalid grades, empty names, and out-of-range numbers |
| Formatted result table | Aligned columns for course name, grade, credits, and grade points |
| Academic remarks | Provides a qualitative label (Excellent / Good / Passing, etc.) |
| Clean console UI | Professional banner and separator lines |

---

## 🛠️ Technologies Used

- **Language:** C++17
- **Standard Library:** `<iostream>`, `<iomanip>`, `<string>`, `<vector>`, `<limits>`, `<algorithm>`
- **Paradigm:** Structured / procedural with `struct`-based data modelling
- **Build tool:** `g++` (GCC) or any C++17-compatible compiler

No third-party libraries. No frameworks. Just standard C++.

---

## 📐 Grading Scale (4.0 System)

| Letter Grade | Grade Points |
|---|---|
| A+ / A | 4.0 |
| A− | 3.7 |
| B+ | 3.3 |
| B | 3.0 |
| B− | 2.7 |
| C+ | 2.3 |
| C | 2.0 |
| C− | 1.7 |
| D+ | 1.3 |
| D | 1.0 |
| F | 0.0 |

**GPA Formula:**
```
GPA = Σ(Grade Points × Credit Hours) / Σ(Credit Hours)
```

**CGPA Formula:**
```
CGPA = Σ(Semester GPA × Semester Credits) / Σ(All Credits)
```

---

## 📁 Project Structure

```
cgpa_calculator/
├── cgpa_calculator.cpp   # Full source code (single file)
└── README.md             # This file
```

---

## ⚙️ How to Compile and Run

### Prerequisites
- A C++17 compatible compiler:
  - **Linux/macOS:** GCC (`g++`) or Clang
  - **Windows:** MinGW, MSVC (Visual Studio), or WSL

### Linux / macOS

```bash
# 1. Clone or download the project
git clone https://github.com/your-username/cgpa-calculator.git
cd cgpa-calculator

# 2. Compile
g++ -std=c++17 -Wall -o cgpa_calculator cgpa_calculator.cpp

# 3. Run
./cgpa_calculator
```

### Windows (MinGW)

```bash
g++ -std=c++17 -Wall -o cgpa_calculator.exe cgpa_calculator.cpp
cgpa_calculator.exe
```

### Windows (Visual Studio)
1. Open Visual Studio → Create a new **Console Application** project.
2. Replace the default `main.cpp` content with `cgpa_calculator.cpp`.
3. Build and run with `Ctrl+F5`.

---

## 🖥️ Sample Run

```
  ╔══════════════════════════════════════════════════════════╗
  ║           C G P A   C A L C U L A T O R                 ║
  ║         Console Application  —  C++17                   ║
  ╚══════════════════════════════════════════════════════════╝

  Grading Scale (4.0 System)
  A+/A=4.0  A-=3.7  B+=3.3  B=3.0  B-=2.7
  C+=2.3    C=2.0   C-=1.7  D+=1.3  D=1.0  F=0.0

  Enter number of semesters to calculate (1-20): 1

--- Semester 1 ---
  How many courses this semester? (1-20): 3

  Course 1:
    Name        : Data Structures
    Grade       : A
    Credit Hrs  : 3

  Course 2:
    Name        : Calculus II
    Grade       : B+
    Credit Hrs  : 3

  Course 3:
    Name        : English Writing
    Grade       : A-
    Credit Hrs  : 2

====================================================================
  SEMESTER 1
====================================================================
  Course Name                   Grade     Credit Hrs    Grade Pts
--------------------------------------------------------------------
  Data Structures               A         3             12.00
  Calculus II                   B+        3             9.90
  English Writing               A-        2             7.40
--------------------------------------------------------------------
  TOTAL                                   8             29.30
====================================================================
  Semester GPA : 3.66 / 4.00
====================================================================

************************************************************
*                    CGPA SUMMARY                         *
************************************************************

  Semester      Courses               Credits         GPA
--------------------------------------------------------------------
  1             3                     8               3.66

--------------------------------------------------------------------
  Total Semesters : 1
  Total Credits   : 8
  Cumulative CGPA : 3.66 / 4.00
  Remarks         : Very Good  — Strong academic standing
************************************************************
```

---

## 🧠 Code Design Decisions

**Why a single `.cpp` file?**
For a beginner-portfolio project, one file is easier to review, submit, and understand. A multi-file split (`.h` + `.cpp`) would add noise without adding value at this scope.

**Why `struct` instead of `class`?**
`Course` and `Semester` are plain data containers with no behaviour. `struct` is the correct C++ tool for that — `class` with public members would be equivalent but misleading.

**Why `std::vector` instead of raw arrays?**
Vectors handle dynamic sizing, bounds safety, and range-based loops cleanly. Raw arrays at this level are a common source of bugs (off-by-one, buffer overflows).

**Why no global variables?**
Every value flows through function parameters and return values. This makes the code testable and the data flow explicit.

---

## 🚀 Possible Extensions

- Save results to a `.txt` or `.csv` file
- Load previous semester data from a file
- Add a GPA predictor ("what grade do I need in Course X to reach CGPA Y?")
- Port to a simple GUI using Qt or Dear ImGui

---

## 👤 Author

**Your Name**
- GitHub: [@your-username](https://github.com/your-username)
- LinkedIn: [your-linkedin](https://linkedin.com/in/your-linkedin)

---

## 📄 License

This project is open source under the [MIT License](LICENSE).
