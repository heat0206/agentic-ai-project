from functions.get_file_content import get_file_content
from config import MAX_CHARS


def run_tests():
    # # ---- TEST 1: lorem.txt (truncation expected) ----
    # print("Result for 'lorem.txt':")
    # result = get_file_content("calculator", "lorem.txt")

    # print("Length of returned content:", len(result))

    # if len(result) <= MAX_CHARS:
    #     print("✅ Content length is within limit")
    # else:
    #     print("❌ Content exceeds MAX_CHARS")

    # if "truncated" in result.lower():
    #     print("✅ Truncation message present")
    # else:
    #     print("❌ Truncation message missing")

    #print()

    # ---- TEST 2: main.py ----
    print("Result for 'main.py':")
    result = get_file_content("calculator", "main.py")
    print(result)  # partial preview only

    # ---- TEST 3: pkg/calculator.py ----
    print("Result for 'pkg/calculator.py':")
    result = get_file_content("calculator", "pkg/calculator.py")
    print(result)

    # ---- TEST 4: /bin/cat (ERROR EXPECTED) ----
    print("Result for '/bin/cat':")
    result = get_file_content("calculator", "/bin/cat")
    print(result)

    if "error" in result.lower():
        print("✅ Proper error returned")
    else:
        print("❌ Expected an error message")

    print()

    # ---- TEST 5: pkg/does_not_exist.py (ERROR EXPECTED) ----
    print("Result for 'pkg/does_not_exist.py':")
    result = get_file_content("calculator", "pkg/does_not_exist.py")
    print(result)

    if "error" in result.lower():
        print("✅ Proper error returned")
    else:
        print("❌ Expected an error message")

    print()


if __name__ == "__main__":
    run_tests()
