"""
Classes for picture information for the
social network project
"""
# pylint: disable=R0903
# pylint: disable=C0115 (missing-class-docstring)
# pylint: disable=C0116 (missing-function-docstring)
# pylint: disable=C0301 (line-too-long)
# pylint: disable=W0401, E0401, W0150, W0614, R0801, R1705, W0703, C0103, W0120, W1309, R1705, R0801, C0305

from pathlib import Path
import re
from loguru import logger



def check_image_constraints(user_id, tags, user_collection):
    '''
    Checks picture constraints
    '''
    if user_collection.find_one(user_id = user_id):
        if len(tags) > 100:
            logger.debug(f"Tags cannot be longer than 100 characters.")
            return False
        if check_tag_constraints(tags) is False:
            logger.debug(f"Tags can only contain upper and lower case letters and underscore")
            return False
        return True
    else:
        logger.debug(f"user_id:{user_id} doesn't exist and image cannot be added.")
        return False


def check_tag_constraints(list_of_tags):
    pattern = '^[a-zA-Z_]*$'
    text_list = list_of_tags.replace('#','').split(' ')
    for text in text_list:
        if bool(re.search(pattern, text)) is False:
            return False
    else:
        return True


def add_image(user_id, tags, user_collection, image_collection):
    if check_image_constraints(user_id, tags, user_collection) is False:
        return False
    else:
        try:
            picture_id = image_collection.insert(user_id = user_id,
                                                 tags = tags)
            file_created = create_picture_file(user_id, picture_id, tags)
            logger.info(f"New Image added: ({picture_id}, {user_id}, {tags} at {file_created})")
            return True
        except Exception as e:
            logger.debug(f'Error: {e}')
            return False


def create_picture_file(user_id, picture_id, tags):
    file_path = user_id/create_tag_path(tags)
    picture_name = str(picture_id).zfill(6) + '.png'
    if not file_path.exists():
        file_path.mkdir(parents = True)
    with open(file_path / picture_name, 'w'):
        pass
    return file_path


def create_tag_path(tags):
    list_of_tags = tags.replace('#','').split(' ')
    list_of_tags.sort()
    return Path('/'.join(list_of_tags))


def list_of_user_images(user_id):
    result = []
    list_of_images = get_file_list(Path(user_id))
    if list_of_images is None:
        logger.debug(f"user_id:{user_id} doesn't have any images")
        return None
    else:
        for image in list_of_images:
            result.append((user_id, str(image.parent), image.name))
        logger.info(f"{len(list_of_images)} images found for user {user_id}")
        return result


def get_file_list(path):
    list_of_files = []
    if not path.is_dir():
        return None
    for child in path.iterdir():
        if child.is_file():
            if child.stem != '.DS_Store':
                list_of_files.append(child)
        else:
            list_of_files.extend(get_file_list(child))
    return list_of_files


def reconcile_images(user_id, user_collection, image_collection):
    if user_collection.find_one(user_id = user_id):
        images_on_drive = [result[2] for result in list_of_user_images(user_id)]

        images_on_db = []
        for result in image_collection.find(user_id = user_id):
            db_picture_name = str(result['id']).zfill(6) + '.png'
            images_on_db.append(db_picture_name)

        unique_on_db = [image for image in images_on_db if image not in images_on_drive]
        unique_on_drive = [image for image in images_on_drive if image not in images_on_db]
        return unique_on_db, unique_on_drive
    else:
        logger.debug(f"user_id:{user_id} doesn't exist and images cannot be reconciled.")
        return None

