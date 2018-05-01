import os


def resolve(directories, filename):
    """
    Searches list of `directories` and returns the full path
    of the first existing file with name `filename`
    """
    tries = []
    for search_dir in directories:
        full_name = os.sep.join([search_dir, filename])
        tries.append(full_name)
        if os.path.isfile(full_name):
            return full_name

    # Did not find the source file. Throw error
    error = (
        "Could not find {} in supplied search paths. Tried: {}. "
        "Remember to configure all search paths in the source_paths "
        "configuration option."
    ).format(filename, ', '.join(tries))
    raise FileNotFoundError(error)
