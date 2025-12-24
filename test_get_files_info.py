from functions.get_files_info import get_files_info

def run_tests():
    print("Result for current directory:")
    result = get_files_info("calculator", ".")
    print(result)
    print()

    print("Result for 'pkg' directory:")
    result = get_files_info("calculator", "pkg")
    print(result)
    print()

    print("Result for '/bin' directory:")
    result = get_files_info("calculator", "/bin")
    print(result)
    print()

    print("Result for '../' directory:")
    result = get_files_info("calculator", "../")
    print(result)
    print()


if __name__ == "__main__":
    run_tests()
