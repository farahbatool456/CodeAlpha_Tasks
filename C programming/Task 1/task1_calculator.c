/*
 * ============================================================
 *  Project    : Basic Calculator
 *  Task       : 1 of 2 — CodeAlpha C Programming Internship
 *  Author     : FARAH BATOOL
 *  Date       : 2025
 *  Description: A menu-driven calculator that performs addition,
 *               subtraction, multiplication, and division on two
 *               numbers entered by the user. Division by zero is
 *               handled gracefully. Uses switch-case for clean
 *               operation selection.
 * ============================================================
 */

#include <stdio.h>   /* printf, scanf */

/* ──────────────────────────────────────────────
   FUNCTION PROTOTYPES
   Declaring all functions before main() so the
   compiler knows their signatures in advance.
   ────────────────────────────────────────────── */
void  display_menu(void);
float add(float a, float b);
float subtract(float a, float b);
float multiply(float a, float b);
int   divide(float a, float b, float *result);   /* returns 0 on success, -1 on div-by-zero */
void  print_result(char *operation, float result);
void  print_separator(void);

/* ──────────────────────────────────────────────
   MAIN FUNCTION
   Entry point. Drives the menu → input → compute
   → output loop.
   ────────────────────────────────────────────── */
int main(void)
{
    float num1, num2, result;
    int   choice;

    print_separator();
    printf("       BASIC CALCULATOR PROGRAM\n");
    printf("       CodeAlpha C Internship — Task 1\n");
    print_separator();

    /* ── Get first number ── */
    printf("\n Enter first number  : ");
    scanf("%f", &num1);

    /* ── Get second number ── */
    printf(" Enter second number : ");
    scanf("%f", &num2);

    /* ── Show operation menu ── */
    display_menu();

    printf("\n Enter your choice (1-4) : ");
    scanf("%d", &choice);

    print_separator();

    /* ── Select and execute operation ── */
    switch (choice)
    {
        case 1:   /* Addition */
            result = add(num1, num2);
            print_result("Addition", result);
            break;

        case 2:   /* Subtraction */
            result = subtract(num1, num2);
            print_result("Subtraction", result);
            break;

        case 3:   /* Multiplication */
            result = multiply(num1, num2);
            print_result("Multiplication", result);
            break;

        case 4:   /* Division — needs zero-check */
            if (divide(num1, num2, &result) == 0)
            {
                print_result("Division", result);
            }
            else
            {
                printf(" ERROR: Division by zero is not allowed!\n");
            }
            break;

        default:
            printf(" ERROR: Invalid choice. Please enter 1 to 4.\n");
            break;
    }

    print_separator();
    printf("\n Program ended. Goodbye!\n\n");
    return 0;
}

/* ──────────────────────────────────────────────
   FUNCTION: display_menu
   Purpose : Print the list of available operations
             so the user can choose one.
   ────────────────────────────────────────────── */
void display_menu(void)
{
    printf("\n ┌────────────────────────┐\n");
    printf(" │   SELECT OPERATION     │\n");
    printf(" ├────────────────────────┤\n");
    printf(" │  1. Addition  (+)      │\n");
    printf(" │  2. Subtraction  (-)   │\n");
    printf(" │  3. Multiplication (*) │\n");
    printf(" │  4. Division  (/)      │\n");
    printf(" └────────────────────────┘\n");
}

/* ──────────────────────────────────────────────
   FUNCTION: add
   Purpose : Return the sum of two floats.
   Params  : a, b — the two operands
   Returns : a + b
   ────────────────────────────────────────────── */
float add(float a, float b)
{
    return a + b;
}

/* ──────────────────────────────────────────────
   FUNCTION: subtract
   Purpose : Return the difference of two floats.
   Params  : a, b — the two operands
   Returns : a - b
   ────────────────────────────────────────────── */
float subtract(float a, float b)
{
    return a - b;
}

/* ──────────────────────────────────────────────
   FUNCTION: multiply
   Purpose : Return the product of two floats.
   Params  : a, b — the two operands
   Returns : a * b
   ────────────────────────────────────────────── */
float multiply(float a, float b)
{
    return a * b;
}

/* ──────────────────────────────────────────────
   FUNCTION: divide
   Purpose : Divide a by b, storing result in the
             pointer *result.
   Params  : a       — dividend
             b       — divisor
             *result — pointer to store the answer
   Returns :  0 on success
             -1 if b is zero (division not possible)

   WHY POINTER?
   A function can only return one value. We need
   to return BOTH the result AND a success/error
   flag. So the result goes via pointer, and the
   return value is the status code.
   ────────────────────────────────────────────── */
int divide(float a, float b, float *result)
{
    if (b == 0.0f)
    {
        return -1;   /* signal error to caller */
    }

    *result = a / b;
    return 0;        /* signal success */
}

/* ──────────────────────────────────────────────
   FUNCTION: print_result
   Purpose : Display the operation name and its
             computed result in a formatted way.
   Params  : operation — string label (e.g. "Addition")
             result    — the computed float value
   ────────────────────────────────────────────── */
void print_result(char *operation, float result)
{
    printf("\n Result  : %.4f\n", result);
    printf(" Operation: %s\n", operation);
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
