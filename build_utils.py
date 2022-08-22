import shutil


def copy_datas_to_dist():
    source_dir = "LuokeCollection/assets/"
    destination_dir = "dist/LuokeCollection/assets/"
    shutil.rmtree(destination_dir)
    shutil.copytree(source_dir, destination_dir)


if __name__ == "__main__":
    copy_datas_to_dist()
