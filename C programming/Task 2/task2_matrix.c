#include <stdio.h>   /* printf, scanf */

/* ── Compile-time constant for max matrix size ── */
#define MAX 5

/* ──────────────────────────────────────────────
   FUNCTION PROTOTYPES
   ────────────────────────────────────────────── */
void read_matrix  (int mat[MAX][MAX], int rows, int cols, char *name);
void print_matrix (int mat[MAX][MAX], int rows, int cols, char *name);
void add_matrices (int a[MAX][MAX], int b[MAX][MAX],
                   int result[MAX][MAX], int rows, int cols);
void multiply_matrices(int a[MAX][MAX], int b[MAX][MAX],
                       int result[MAX][MAX],
                       int rows_a, int cols_a, int cols_b);
void transpose_matrix (int mat[MAX][MAX], int trans[MAX][MAX],
                       int rows, int cols);
void print_separator(void);
int  get_valid_dimension(char *label);

/* ──────────────────────────────────────────────
   MAIN FUNCTION
   Drives a menu that lets the user pick which
   matrix operation to perform.
   ────────────────────────────────────────────── */
int main(void)
{
    /* ── Declare all matrices we might need ── */
    int matA[MAX][MAX], matB[MAX][MAX], result[MAX][MAX];
    int rows, cols, choice;

    print_separator();
    printf("         MATRIX OPERATIONS PROGRAM\n");
    printf("         CodeAlpha C Internship — Task 2\n");
    print_separator();

    /* ── Operation selection menu ── */
    printf("\n Select an operation:\n");
    printf("  1. Matrix Addition\n");
    printf("  2. Matrix Multiplication\n");
    printf("  3. Matrix Transpose\n");
    printf("\n Enter choice (1-3): ");
    scanf("%d", &choice);

    /* ──────────────────────────────────────────
       SWITCH: Route to the chosen operation.
       Each case handles its own dimension logic
       because the rules differ:
         Add/Subtract  → both matrices SAME size
         Multiply      → A is (m×k), B is (k×n)
         Transpose     → just one matrix
       ────────────────────────────────────────── */
    switch (choice)
    {

        /* ════════════════════════════════════
           CASE 1 — MATRIX ADDITION
           Rule: A and B must have identical
                 dimensions (same rows, same cols).
           Result[i][j] = A[i][j] + B[i][j]
           ════════════════════════════════════ */
        case 1:
            printf("\n── Matrix Addition ──\n");
            rows = get_valid_dimension("rows");
            cols = get_valid_dimension("cols");

            read_matrix(matA, rows, cols, "A");
            read_matrix(matB, rows, cols, "B");

            add_matrices(matA, matB, result, rows, cols);

            print_matrix(matA, rows, cols, "Matrix A");
            print_matrix(matB, rows, cols, "Matrix B");
            print_matrix(result, rows, cols, "Result (A + B)");
            break;

        /* ════════════════════════════════════
           CASE 2 — MATRIX MULTIPLICATION
           Rule: A is (rows_a × cols_a)
                 B is (cols_a × cols_b)
                 Result is (rows_a × cols_b)

           ALGORITHM EXPLANATION:
           To get result[i][j], we take the
           i-th ROW of A and the j-th COLUMN
           of B, multiply element by element,
           then sum all those products.

           Example (2×2 × 2×2):
             result[0][0] = A[0][0]*B[0][0]
                          + A[0][1]*B[1][0]
           ════════════════════════════════════ */
        case 2:
            printf("\n── Matrix Multiplication ──\n");
            printf("\n Matrix A dimensions:\n");
            int rows_a = get_valid_dimension("rows of A");
            int cols_a = get_valid_dimension("cols of A");

            printf("\n Matrix B dimensions:\n");
            printf(" (rows of B must equal cols of A = %d)\n", cols_a);
            int cols_b = get_valid_dimension("cols of B");

            read_matrix(matA, rows_a, cols_a, "A");
            read_matrix(matB, cols_a, cols_b, "B");

            multiply_matrices(matA, matB, result, rows_a, cols_a, cols_b);

            print_matrix(matA, rows_a, cols_a, "Matrix A");
            print_matrix(matB, cols_a, cols_b, "Matrix B");
            print_matrix(result, rows_a, cols_b, "Result (A x B)");
            break;

        /* ════════════════════════════════════
           CASE 3 — MATRIX TRANSPOSE
           Rule: If A is (rows × cols),
                 Transpose is (cols × rows).
           trans[j][i] = A[i][j]
           (rows become columns, columns become rows)
           ════════════════════════════════════ */
        case 3:
            printf("\n── Matrix Transpose ──\n");
            rows = get_valid_dimension("rows");
            cols = get_valid_dimension("cols");

            read_matrix(matA, rows, cols, "A");
            transpose_matrix(matA, result, rows, cols);

            print_matrix(matA, rows, cols, "Matrix A (original)");
            print_matrix(result, cols, rows, "Transpose of A");
            break;

        default:
            printf("\n ERROR: Invalid choice. Please enter 1, 2, or 3.\n");
            break;
    }

    print_separator();
    printf("\n Program ended. Goodbye!\n\n");
    return 0;
}

/* ──────────────────────────────────────────────
   FUNCTION: get_valid_dimension
   Purpose : Ask the user for a matrix dimension
             (rows or cols). Keeps asking until a
             value between 1 and MAX is entered.
   Params  : label — string shown in the prompt
   Returns : valid integer between 1 and MAX
   ────────────────────────────────────────────── */
int get_valid_dimension(char *label)
{
    int value;
    do {
        printf(" Enter %s (1 to %d): ", label, MAX);
        scanf("%d", &value);
        if (value < 1 || value > MAX)
        {
            printf(" ERROR: Must be between 1 and %d. Try again.\n", MAX);
        }
    } while (value < 1 || value > MAX);
    return value;
}

/* ──────────────────────────────────────────────
   FUNCTION: read_matrix
   Purpose : Read matrix values from user input.
             Loops row by row, column by column.
   Params  : mat  — 2D array to fill
             rows — number of rows
             cols — number of columns
             name — label shown in prompt ("A" or "B")
   ────────────────────────────────────────────── */
void read_matrix(int mat[MAX][MAX], int rows, int cols, char *name)
{
    int i, j;

    printf("\n Enter elements of Matrix %s (%dx%d):\n", name, rows, cols);

    for (i = 0; i < rows; i++)
    {
        for (j = 0; j < cols; j++)
        {
            printf("  [%d][%d] = ", i, j);
            scanf("%d", &mat[i][j]);
        }
    }
}

/* ──────────────────────────────────────────────
   FUNCTION: print_matrix
   Purpose : Display a 2D matrix in grid format
             with proper row/column spacing.
   Params  : mat  — 2D array to display
             rows — number of rows
             cols — number of columns
             name — heading label for the matrix
   ────────────────────────────────────────────── */
void print_matrix(int mat[MAX][MAX], int rows, int cols, char *name)
{
    int i, j;

    printf("\n %s (%dx%d):\n", name, rows, cols);
    printf(" ┌");

    /* ── Draw top border (rough width estimate) ── */
    for (j = 0; j < cols; j++) printf("──────");
    printf("┐\n");

    /* ── Print each row ── */
    for (i = 0; i < rows; i++)
    {
        printf(" │");
        for (j = 0; j < cols; j++)
        {
            printf(" %4d ", mat[i][j]);
        }
        printf("│\n");
    }

    /* ── Draw bottom border ── */
    printf(" └");
    for (j = 0; j < cols; j++) printf("──────");
    printf("┘\n");
}

/* ──────────────────────────────────────────────
   FUNCTION: add_matrices
   Purpose : Add two matrices element by element.

   LOGIC:
   For every position (i, j), simply add the
   values from the same position in A and B.
   result[i][j] = a[i][j] + b[i][j]

   Time Complexity: O(rows × cols)
   ────────────────────────────────────────────── */
void add_matrices(int a[MAX][MAX], int b[MAX][MAX],
                  int result[MAX][MAX], int rows, int cols)
{
    int i, j;

    for (i = 0; i < rows; i++)
    {
        for (j = 0; j < cols; j++)
        {
            result[i][j] = a[i][j] + b[i][j];
        }
    }
}

/* ──────────────────────────────────────────────
   FUNCTION: multiply_matrices
   Purpose : Multiply matrix A (rows_a × cols_a)
             by matrix B (cols_a × cols_b).
             Stores result in result (rows_a × cols_b).

   LOGIC — Step by step:
   1. For each row i in A:
   2.   For each column j in B:
   3.     Start with sum = 0
   4.     Loop through k from 0 to cols_a:
   5.       sum += A[i][k] * B[k][j]
            (row of A dotted with column of B)
   6.     result[i][j] = sum

   WHY?
   Matrix multiplication is a "dot product" of
   each row of A with each column of B.

   VISUAL EXAMPLE — 2×2:
     A = | 1 2 |    B = | 5 6 |
         | 3 4 |        | 7 8 |

     result[0][0] = 1*5 + 2*7 = 5 + 14 = 19
     result[0][1] = 1*6 + 2*8 = 6 + 16 = 22
     result[1][0] = 3*5 + 4*7 = 15 + 28 = 43
     result[1][1] = 3*6 + 4*8 = 18 + 32 = 50

   Time Complexity: O(rows_a × cols_a × cols_b)
   ────────────────────────────────────────────── */
void multiply_matrices(int a[MAX][MAX], int b[MAX][MAX],
                       int result[MAX][MAX],
                       int rows_a, int cols_a, int cols_b)
{
    int i, j, k;

    /* ── Initialize result to zero first ── */
    for (i = 0; i < rows_a; i++)
        for (j = 0; j < cols_b; j++)
            result[i][j] = 0;

    /* ── Triple nested loop: the core of matrix multiply ── */
    for (i = 0; i < rows_a; i++)           /* each row of A    */
    {
        for (j = 0; j < cols_b; j++)       /* each col of B    */
        {
            for (k = 0; k < cols_a; k++)   /* dot product loop */
            {
                result[i][j] += a[i][k] * b[k][j];
            }
        }
    }
}

/* ──────────────────────────────────────────────
   FUNCTION: transpose_matrix
   Purpose : Flip a matrix over its diagonal.
             Rows become columns, columns become rows.

   LOGIC:
   trans[j][i] = mat[i][j]

   If original is:
     1 2 3
     4 5 6

   Transpose is:
     1 4
     2 5
     3 6

   Time Complexity: O(rows × cols)
   ────────────────────────────────────────────── */
void transpose_matrix(int mat[MAX][MAX], int trans[MAX][MAX],
                      int rows, int cols)
{
    int i, j;

    for (i = 0; i < rows; i++)
    {
        for (j = 0; j < cols; j++)
        {
            trans[j][i] = mat[i][j];   /* swap row↔col index */
        }
    }
}

/* ──────────────────────────────────────────────
   FUNCTION: print_separator
   Purpose : Print a visual divider line for
             cleaner console output formatting.
   ────────────────────────────────────────────── */
void print_separator(void)
{
    printf("\n =============================================\n");
}
