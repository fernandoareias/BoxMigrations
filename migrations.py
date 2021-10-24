import argparse
import pyfiglet
import pathlib
import os
import shutil
import logging



def banner():
    ascii_banner = pyfiglet.figlet_format("Box Migrations")
    
    print(ascii_banner)

def help():

    parser = argparse.ArgumentParser(description='This is a simples migrations organizer')

    parser.add_argument('--path',action='store', dest='path_project', type=str, help="set your project path")

    args = parser.parse_args()
    
    return args



def start_script(path:str):
    # Procura as pastas Migrations no projeto informado
    migrations_path = search_migrations(path)
    
    # Lista e divide os Paths e nome dos arquivos de Migration encontrado
    paths_lits, paths_filenames_list, filenames_list  = sorted(get_filenames_list(migrations_path))

    # Obtem uma lista de anos das migrations
    years = get_list_years(filenames_list)

    # Cria novas pastas para cada ano de migrations
    list_new_paths = create_paths(paths_lits, years)

    # Move as migrations para suas respectivas pastas
    moved_for_new_path(paths_lits)

    # Compacta as pastas em .RAR e deleta a pasta antiga
    compact_paths(paths_lits)

def main():

    banner()
    
    start_script(help().path_project)
    


def compact_paths(paths_lits):
    for path in paths_lits:
        for directory, subfolders, files in os.walk(path):
            for file in files:
                if(file.endswith('.cs') and file[0].isdigit()):
                    name_arch = path + '/Migrations_' + directory[-4::] + '_compact'
                    logging.basicConfig(level=0)
                    if(os.path.exists(name_arch + '.zip') == False):
                        try:
                            shutil.make_archive(name_arch, 'zip', directory, logger=logging)
                        except IsADirectoryError:
                            print("[-] Unable to compress file.")
                            exit(1)
                        except FileNotFoundError:
                            print("[-] Could not find folder")
                            exit(1)
                        else:
                            print("")
                            print("[+] Total compressed files: " + str(len(files)))
                            shutil.rmtree(directory)
                            print("[-] Folders removed: " + directory[-15::])
                            print("")


def moved_for_new_path(lista_paths ):
    for path in lista_paths:
        for directory, subfolders, files in os.walk(path):
            for file in files:
                if(file.endswith('.cs') and file[0].isdigit()):
                    new_path = path + "/Migrations_" + file[0:4] 
                    if(os.path.exists(path + '/' + file) == True):
                        if(pathlib.Path(new_path).exists() == True):
                            shutil.move(path + '/' + file, new_path + '/' + file)


def create_paths(lista_paths:str, years:str):
    list_new_paths = []
    for path in lista_paths:
        for year in years:
            new_path = path + "/Migrations_" + year + "/"
            if(pathlib.Path(new_path).exists() == False and path.count("/Migrations_" + year) == 0):
                os.makedirs(new_path)
                list_new_paths.append(new_path)
    
    return list_new_paths

def get_list_years(lista_files:str):
    lista_anos = []
    for file in lista_files:
        lista_anos.append(file[0:4])    

    # Remove valores repetidos e retorna a lista
    return list(dict.fromkeys(lista_anos))

def get_filenames_list(migrations_paths:str):
    filenames_list = []
    paths_lits = []
    paths_filenames_list = []

    for migration in migrations_paths:
        for directory, subfolders, files in os.walk(migration):
            for file in files:
                if(file.endswith('.cs') and file[0].isdigit()):
                    paths_filenames_list.append(directory + "/" + file)
                    filenames_list.append(file)
                    paths_lits.append(directory)

    if(len(filenames_list) < 1):
        print("[-] Could not find files of migrations!")
        exit(1)

    return list(dict.fromkeys(filenames_list)), list(dict.fromkeys(paths_lits)), list(dict.fromkeys(paths_filenames_list))

def search_migrations(path:str):
  
    # Procura a pasta informada
    directory = pathlib.Path(path)

    if(directory.exists() == False):
        print("[-] Could not find migration path!")

    # Dentro da pasta infromada procura o path de todas as pastas Migrations encontrada
    migrations_paths = directory.glob('**/Migrations')

    return list(dict.fromkeys(migrations_paths))




if __name__ == "__main__":   
    main()








