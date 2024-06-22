import sys
import os
import zlib
import hashlib

def init():
    os.mkdir(".git")
    os.mkdir(".git/objects")
    os.mkdir(".git/refs")
    with open(".git/HEAD", "w") as f:
        f.write("ref: refs/heads/main\n")
    print("Repositorio de git inicializado")

def cat_file(blob_sha):
    try:
        with open(f".git/objects/{blob_sha[:2]}/{blob_sha[2:]}", "rb") as f:
            raw = zlib.decompress(f.read())
            header, content = raw.split(b"\0", maxsplit=1)
            print(content.decode("utf-8"), end="")
    except FileNotFoundError:
        raise RuntimeError("Blob no encontrado")
    except zlib.error:
        raise RuntimeError("Error al descomprimir el blob")

def hash_object(file_path):
    try:
        with open(f"./{file_path}", "rb") as f:
            file_content = f.read()
            file_size = len(file_content)
            blob_header = f"blob {file_size}\0"
            blob_data = blob_header.encode("utf-8") + file_content
            sha1 = hashlib.sha1(blob_data).hexdigest()
        
            object_dir = f".git/objects/{sha1[:2]}"
            os.makedirs(object_dir, exist_ok=True)
            compressed_blob = zlib.compress(blob_data)

            with open(f"{object_dir}/{sha1[2:]}", "wb") as f:
                f.write(compressed_blob)

        print(f"Blob creado satisfactoriamente con SHA1: {sha1}")
    except FileNotFoundError:
        raise RuntimeError(f"Archivo no encontrado: {file_path}")
    except zlib.error:
        raise RuntimeError("Error al comprimir el blob")
    except Exception as e:
        raise RuntimeError(f"Error inesperado: {e}")

def main():
    command = sys.argv[1]
    if command == "init":
        init()
    elif command == "cat-file":
        if sys.argv[2] == "-p":
            blob_sha = sys.argv[3]
            cat_file(blob_sha)
    elif command == "hash-object":
        if sys.argv[2] == "-w":
            file_path = sys.argv[3]
            hash_object(file_path)
    else:
        raise RuntimeError(f"Comando desconocido: {command}")

if __name__ == "__main__":
    main()
