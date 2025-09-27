from functions.get_files_content import get_file_content


info = get_file_content("calculator","main.py")
print("Result for current directory:")
print(info)
pkg = get_file_content("calculator","pkg/calculator.py")
print("Result for 'pkg' directory:")
print(pkg)
ll = get_file_content("calculator","/bin/cat")
print("Result for '/bin' directory:")
print(ll)
gi = get_file_content("calculator","pkg/does_not_exist.py")
print("Result for '../' directory:")
print(gi)
