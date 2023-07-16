import os, shutil, subprocess

def gether_deps(path, dependencies):
    with  subprocess.Popen(f"/usr/bin/ldd {path} | awk '{{print $3}}'", stdout=subprocess.PIPE, shell=True, stderr=subprocess.DEVNULL) as proc:
        for path in proc.stdout.readlines():
            path = path.decode("utf-8").replace("\n", "")
            if not os.path.exists(path) or path in dependencies:
                continue
            print(path)
            dependencies.append(path)
            dependencies = gether_deps(path, dependencies)


    return dependencies

def copy_all(source, target):
    shutil.copy2(source, target)
    st = os.stat(source)
    os.chown(target, st.st_uid, st.st_gid)

def copy_results(main_lib, dependencies):
    tmp_dir = "/tmp/dest"
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    main_lib_dir_name = f"{tmp_dir}{os.path.dirname(main_lib)}"
    if not os.path.exists(main_lib_dir_name):
        os.makedirs(main_lib_dir_name)
    copy_all(main_lib, main_lib_dir_name)

    for dependency in dependencies:
        dest_path = f"{tmp_dir}{dependency}"
        dep_dir = os.path.dirname(dependency)
        dest_dir = f"{tmp_dir}{dep_dir}"
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        copy_all(dependency, dest_path)

if __name__ == "__main__":

    php_cli_path = "/usr/local/sbin/php-fpm"
    dependencies = gether_deps(php_cli_path,  [])
    copy_results(php_cli_path, dependencies)

    
    extensions = ["opcache.so", "redis.so", "sodium.so"]
    for extension in extensions:
        extension_path = f"/usr/local/lib/php/extensions/no-debug-non-zts-20220829/{extension}"
        dependencies = gether_deps(extension_path,  [])
        copy_results(extension_path, dependencies)
