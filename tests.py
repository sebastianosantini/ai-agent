from function.get_files_info import write_file

def tests():
    result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print(result)
    result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print(result)
    result = write_file("calculator", "/temp/temp.txt", "this should not be allowed")
    print(result)
    
if __name__ == "__main__":
    tests()