# from subdirectory.filename import function_name
from functions.get_files_info import get_files_info

print(get_files_info("calculator", "calculator"))
print(get_files_info("calculator", "calculator/pkg"))
print(get_files_info("calculator", "/bin"))
print(get_files_info("calculator", "../"))