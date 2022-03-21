import os

def get_user_public_key(key_or_path: str = None, secrets_config=None):
    """
        Return the ssh key.
        It will first check if the given argument is a ssh key or a path to one
        otherwise will check the configuration file.
    """
    if not key_or_path:
        if secrets_config.ssh_pub_key:
            key_or_path = secrets_config.ssh_pub_key

        else:
            return None

    if not key_or_path:
        return None

    key = None
    if os.path.isfile(os.path.expanduser(key_or_path)):
        return __read_ssh_key_from_file(key_or_path)
    else:
        return key_or_path


def __read_ssh_key_from_file(path: str) -> str:
    """
        Read the content of the given file
    """
    with open(os.path.expanduser(path), 'r') as content_file:
        return content_file.read()
