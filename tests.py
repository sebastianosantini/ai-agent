from function.get_files_info import get_files_info, get_file_content

def tests():
    result = get_file_content("calculator", "main.py")
    print(result)
    result = get_file_content("calculator", "pkg/calculator.py")
    print(result)
    result = get_file_content("calculator", "/bin/cat")
    print(result)

if __name__ == "__main__":
    tests()