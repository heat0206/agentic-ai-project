from functions.run_python_file import run_python_file

def run_tests():
    print("Test 1: run calculator main.py (usage instructions)")
    result = run_python_file("calculator", "main.py")
    print(result)
    print()

    print("Test 2: run calculator with expression argument")
    result = run_python_file("calculator", "main.py", ["3 + 5"])
    print(result)
    print()

    print("Test 3: run calculator tests")
    result = run_python_file("calculator", "tests.py")
    print(result)
    print()

    print("Test 4: attempt path traversal (should error)")
    result = run_python_file("calculator", "../main.py")
    print(result)
    print()

    print("Test 5: nonexistent file (should error)")
    result = run_python_file("calculator", "nonexistent.py")
    print(result)
    print()

    print("Test 6: non-Python file (should error)")
    result = run_python_file("calculator", "lorem.txt")
    print(result)
    print()


if __name__ == "__main__":
    run_tests()
