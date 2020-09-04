"""
v0.8
This script creates folders inside a directory, one for each non-folder element,
as many as n files in the directory it was executed from, whatever the extension, and names each
as the name of each file listed (minus "desktop.ini" and the name of the script itself).
On the completion of that task, moves each file found to its name-corresponding new folder.
"""
"""
TODO:   1) Write a log to a .txt so it can be read in case of wanting to undo past executions
        2) Hability to select if run normally or load past log  
FIXES:  A) Catch exceptions to name conflicts

"""
import os
import re
import sys  # For halting execution if not valid files are found

entire_dir = os.listdir()
print("Current directory path found...")
# Los nombres de los archivos en el directorio

scriptname = os.path.basename(__file__)
print("Script filename found")
# Nombre del script para retirarlo de la lista de directorios a crear

# String comprehension "desktop.ini" removal
notwant = "desktop.ini"
notwant2 = scriptname
entire_dir_1 = [i for i in entire_dir if i != notwant]
entire_dir_n = [i for i in entire_dir_1 if i != notwant2]
print("The script filename and 'desktop.ini' filenames are omited from the list.")

siz2 = len(entire_dir_n)
# Cuántos son

# Listar cuáles son directorio
fileordir = []
for i in range(0, siz2-1):
    fileordir.append(os.path.isdir(entire_dir_n[i]))
    # True: Folder / False: File

# Remover extensiones a los nombres y saltar los directorios
pattern = ".*(?=\.)"
no_extension = []
for i in range(0, siz2-1):
    if not fileordir[i]:
        no_extension.append(re.match(pattern, entire_dir_n[i]).group())

# Halt script if the non-directory file list is less than 1 element
if len(no_extension) < 1:
    print("No files have found in current directory, stopping execution.")
    sys.exit()

# Agregar una seña particular al nombre para identificar el directorio
no_extension_custom = [s + "_folderer" for s in no_extension]
# ... this is also list comprehension
print("The directories created are named without filename's extensions and with \"_folderer\" at the end so they're identifiable.")

# Crear directorios
for i in range(0, len(no_extension)):
    try:
        os.mkdir(no_extension_custom[i])
    except OSError:
        print("Creation of the directory \"'%s\" not needed" % no_extension[i])
    else:
        print("Successfully created the directory \"%s\" " % no_extension[i])

# Crear lista de nombres de archivos con extensiones
# Se les quitó la extensión junto cuando se seleccionó cuáles eran directorio
print("Files are going into the directories created...")
yes_extension = []
for i in range(0, len(entire_dir_n)-1):
    if not fileordir[i]:  # To skip the folders without making yet another step-list
        yes_extension.append(entire_dir_n[i])
        # entire_dir_n : complete list without desktop.ini and script name, yet with extensions

# Make the list of source filenames
source_paths = []
for i in range(0, len(yes_extension)):
    source_paths.append(os.getcwd() + '\\' + yes_extension[i])

# Make the list of destination directories
target_path = []
for i in range(0, len(no_extension)):
    target_path.append(os.getcwd() + '\\' + no_extension_custom[i] + '\\' + yes_extension[i])

# Mover archivos hacia su correspondiente carpeta
for i in range(0, len(source_paths)):
    os.replace(source_paths[i], target_path[i])
# Apparently 'os.replace()' doesn't throw an exception if paths arenot found
print("Files moved successfully.")

# Give the option to undo changes:
undo_changes = input("\n Do you want to undo changes?: Y: Yes | Other: No")
if undo_changes == 'Y' or undo_changes == 'y':
    print("Replacing files to original location and deleting created folders...")
    for i in range(0, len(source_paths)):
        os.replace(target_path[i], source_paths[i])
    for i in range(0, len(no_extension)):
        os.rmdir(os.getcwd() + '\\' + no_extension_custom[i])
else:
    print("Execution ended successfully !")

# print("hey") # Break for debugging
