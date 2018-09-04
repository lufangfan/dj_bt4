import os
import uuid


def get_file_path(instance, filename):
    """
    Function: common function to generate unique filename for all file resources, including courseware, homework etc

    Description:
        It will be called when file is uploaded and save the model. Once model is saved, file will be renamed
        with return value, and database will be updated.

    Args:
        instance (int): instance of the model.
        filename (str): original file name, including extension.

    Returns:
        str: filename with relative path
    """
    thumbnail = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), thumbnail)
    return os.path.join('thumbnail', filename)