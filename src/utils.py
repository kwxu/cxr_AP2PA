import os
import errno


def read_file_contents_list(file_name):
    print(f'Reading from file list txt {file_name}')
    with open(file_name) as file:
        lines = [line.rstrip('\n') for line in file]
        return lines


def mkdir_p(path):
    print(f'mkdir: {path}')
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

