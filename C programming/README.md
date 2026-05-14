## Task 1 — Basic Calculator

### Description
A menu-driven console calculator that performs the four basic arithmetic operations on two numbers entered by the user. Division by zero is caught and reported gracefully.

### Features
- Addition, Subtraction, Multiplication, Division
- `switch-case` for clean operation selection
- Division-by-zero error handling
- Modular design — one function per operation
- Formatted console output

### How to Compile and Run

```bash
gcc -Wall -o calculator task1_calculator.c
./calculator
```

### Sample Input / Output

**Addition:**
```
Enter first number  : 10.5
Enter second number : 3.5

Select operation: 1 (Addition)

Result    : 14.0000
Operation : Addition
```

**Division by zero:**
```
Enter first number  : 7
Enter second number : 0

Select operation: 4 (Division)

ERROR: Division by zero is not allowed!
```

### Functions

| Function | Purpose |
|---|---|
| `main()` | Entry point, drives menu and switch-case |
| `display_menu()` | Prints operation choices |
| `add(a, b)` | Returns a + b |
| `subtract(a, b)` | Returns a - b |
| `multiply(a, b)` | Returns a * b |
| `divide(a, b, *result)` | Divides a by b; returns -1 if b is zero |
| `print_result(op, result)` | Displays formatted result |
| `print_separator()` | Prints a divider line |

### Algorithm
1. Read two float numbers from the user
2. Display operation menu
3. Read user's choice (1–4)
4. Use `switch-case` to call the correct function
5. For division, check if divisor is zero before computing
6. Display result or error message

---

## Task 2 — Matrix Operations

### Description
A menu-driven program that performs three fundamental matrix operations on user-defined matrices stored as 2D arrays. Maximum supported size is 5×5.

### Features
- Matrix Addition
- Matrix Multiplication
- Matrix Transpose
- Input validation for matrix dimensions (1–5)
- Neat bordered grid display for all matrices
- Modular design — one function per operation

### How to Compile and Run

```bash
gcc -Wall -o matrix task2_matrix.c
./matrix
```

### Sample Input / Output

**Matrix Addition (2×2):**
```
Matrix A        Matrix B        Result (A + B)
┌────────┐      ┌────────┐      ┌────────┐
│  1   2 │  +   │  5   6 │  =   │  6   8 │
│  3   4 │      │  7   8 │      │ 10  12 │
└────────┘      └────────┘      └────────┘
```

**Matrix Multiplication (2×2 × 2×2):**
```
Matrix A        Matrix B        Result (A x B)
┌────────┐      ┌────────┐      ┌─────────┐
│  1   2 │  x   │  5   6 │  =   │  19  22 │
│  3   4 │      │  7   8 │      │  43  50 │
└────────┘      └────────┘      └─────────┘
```

**Matrix Transpose (2×3 → 3×2):**
```
Matrix A (2×3)      Transpose (3×2)
┌──────────────┐    ┌────────┐
│  1   2   3   │    │  1   4 │
│  4   5   6   │    │  2   5 │
└──────────────┘    │  3   6 │
                    └────────┘
```

### Functions

| Function | Purpose |
|---|---|
| `main()` | Entry point, drives menu and switch-case |
| `get_valid_dimension(label)` | Prompts and validates dimension input (1–5) |
| `read_matrix(mat, rows, cols, name)` | Reads matrix elements from user |
| `print_matrix(mat, rows, cols, name)` | Displays matrix in bordered grid format |
| `add_matrices(a, b, result, rows, cols)` | Element-wise addition of two matrices |
| `multiply_matrices(a, b, result, ra, ca, cb)` | Multiplies matrix A by matrix B |
| `transpose_matrix(mat, trans, rows, cols)` | Flips matrix over its diagonal |
| `print_separator()` | Prints a divider line |

### Algorithm

**Matrix Addition:**
```
For each position (i, j):
    result[i][j] = A[i][j] + B[i][j]
Time Complexity: O(rows × cols)
```

**Matrix Multiplication:**
```
Constraint: cols of A must equal rows of B

For each row i in A:
  For each col j in B:
    result[i][j] = 0
    For each k from 0 to cols_a:
      result[i][j] += A[i][k] * B[k][j]

Time Complexity: O(rows_a × cols_a × cols_b)
```

**Matrix Transpose:**
```
For each position (i, j) in original:
    trans[j][i] = mat[i][j]

Dimensions flip: (rows × cols) → (cols × rows)
Time Complexity: O(rows × cols)
```

---

## Time Complexity Summary

| Operation | Complexity |
|---|---|
| Calculator (all ops) | O(1) — constant time |
| Matrix Addition | O(r × c) |
| Matrix Transpose | O(r × c) |
| Matrix Multiplication | O(r × k × c) |

---

## Concepts Demonstrated

- Functions and modular code structure
- 2D arrays and pointer parameters
- `switch-case` for menu-driven programs
- Input validation with `do-while` loops
- Error handling (division by zero)
- Formatted console output

---

## How to Push to GitHub

```bash
# Inside your project folder
git init
git add task1_calculator.c task2_matrix.c README.md
git commit -m "Add CodeAlpha internship tasks: Calculator and Matrix Operations"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

> Replace `YOUR_USERNAME` and `YOUR_REPO_NAME` with your actual GitHub details.
