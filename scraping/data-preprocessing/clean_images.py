import os
from time import time
import shutil
import numpy as np
import pandas as pd


def read_data(path):
    """
    Read json file in dataframe

    Args:
        path (str): Path to dataset

    Returns:
        df (Pandas DataFrame) : dataframe of dataset
    """
    df = pd.read_json(path)
    return df


def copy_images(from_path, to_path):
    """
    Create a new copy of dataset to modify

    Args:
        from_path (str): path of original dataset
        to_path (str): new destination
    """
    if os.path.isdir(from_path):
        shutil.copytree(from_path, to_path)


def delete_people_with_number_of_images(df, num, path):
    """
    Delete images of people with number_of_images = num
    Drope  people with number_of_images = num from dataframe

    Args:
        df (pandas DataFrame): Information of people
        num (int): drop person with this number_of_images
        path (str): path to images
    """
    t0 = time()
    folders_num_img = df.id[df.number_of_images == num]
    df.drop(df[df.number_of_images == num].index, inplace=True)
    for i in folders_num_img:
        shutil.rmtree(f'{path}/{i}')
    t1 = time() - t0
    print(f"Delete people with nummber of images = {num} in {t1}")


def drop_duplicates(df, path):
    """
    Drop duplicates based on person name and images

    Args:
        df (pandas DataFrame): Information of people
        path (str): path to dataset
    """
    duplicates = df['name_arabic'][df['name_arabic'].duplicated()]
    df.drop(df[df['name_arabic'].duplicated()].index, inplace=True)
    for i in duplicates:
        duplicates_id = []
        img_dir = os.listdir(f'{path}/{i}')
        for j in img_dir:
            id_ = j.split('_')[-1]
            if id_ in duplicates_id:
                os.remove(f'{path}/{i}/{j}')
            else:
                duplicates_id.append(id_)


def delete_people_missing_before_year(df, year, path):
    """
    Delete missing people before specific year and delete their images

    Args:
        df (pandas DataFrame): Information of people
        year (int): year to delete people before
        path (str): path to dataset
    """
    t0 = time()
    data_before_year = df['name_arabic'][df['year'] <= year]
    df.drop(df[df['year'] <= year].index, inplace=True)
    for i in data_before_year:
        if i in os.listdir(f'{path}'):
            shutil.rmtree(f'{path}/{i}')

    t1 = time() - t0
    print(f"Delete people missing from year = {year} in {t1}")


def reset_id():
    """
    to reset id column
    """
    df.drop('id', axis=1, inplace=True)
    df.reset_index(inplace=True)
    df.rename(columns={"index": "id"}, inplace=True)


def export_json(df, path='Data/missing_people_final.json'):
    """
    Export dataframe into json file

    Args:
        df (pandas DataFrame): Information of people
        path (str): where to save json file
    """
    t0 = time()
    with open(path, 'w', encoding='utf-8') as file:
        df.to_json(file,  indent=4, orient="records",
                   force_ascii=False, date_format='iso')

    t1 = time() - t0
    print(f"Save new json file {t1}")


def rename_dir(image_path, json_path):
    """
    Rename image directory from names in arabic to their id

    Args:
        image_path (str): path to images
        json_path (str): path to json file
    """
    t0 = time()
    dir_ = os.listdir(image_path)
    df = pd.read_json(json_path)
    df.set_index('id', inplace=True)
    for i in dir_:
        os.rename(f'{image_path}/{i}',
                  f"{image_path}/{str(df[df['name_arabic']==i].index[0])}")

    t1 = time() - t0
    print(f"Rename directories to id of people in {t1}")


def train_test_split(rootDir, dataDir, test_ratio=None, one_shot=False, include=False, json_path=None, from_path=None, to_path=None, img_per_person_to_remove=None, save_path=None):
    """
    Split images into train and test set

    Args:
        rootDir (_typestr_): path to save test and train folders
        dataDir (str): path to existing data
        test_ratio (float, optional): percent   age of test set
        one_shot (int, optional): take number of image from each folder for train set
        include (bool, optional): delete people with certain number of images
        json_path (str, optional): path to missing_people_final.json
        from_path (str, optional): path where data exits
        to_path (str, optional): destination for data copy
        img_per_person_to_remove (str, optional): drop people with certain number of images
        save_path (str, optional): path of new json file
    """
    t0 = time()
    if not include:

        df = read_data(json_path)
        copy_images(from_path, to_path)
        for i in range(1, img_per_person_to_remove+1):
            delete_people_with_number_of_images(df, i, to_path)
        export_json(df, path=save_path)

    classes = os.listdir(dataDir)
    for i in classes:
        os.makedirs(rootDir + '/train/' + i)
        os.makedirs(rootDir + '/test/' + i)

        source = dataDir + '/' + i
        allFileNames = os.listdir(source)
        np.random.shuffle(allFileNames)

        train_FileNames, test_FileNames = np.split(np.array(allFileNames),
                                                   [int(len(allFileNames) * (1 - test_ratio)) if not one_shot else one_shot])

        train_FileNames = [source+'/' +
                           name for name in train_FileNames.tolist()]
        test_FileNames = [source+'/' +
                          name for name in test_FileNames.tolist()]

        for name in train_FileNames:
            shutil.copy(name, rootDir + '/train/' + i)

        for name in test_FileNames:
            shutil.copy(name, rootDir + '/test/' + i)
    print(f'training folder: {rootDir}"/train/"')
    print(f'testing folder: {rootDir}"/test/"')
    t1 = time() - t0
    way = f'{one_shot} shots' if one_shot else f'{test_ratio} test ratio'
    print(f"Split images with {way} in {t1}")


if __name__ == "__main__":
    from_path = 'data_collection/data_not_ready/images'
    to_path = 'Data/images'

    if not os.path.isdir(to_path):

        json_path = 'data_collection/data_not_ready/missing_people_without_image_columns.json'
        df = read_data(json_path)

        img_path = to_path
        copy_images(from_path, to_path)

        img_per_person_to_remove = 0
        delete_people_with_number_of_images(
            df, img_per_person_to_remove, img_path)

        drop_duplicates(df, img_path)

        delete_people_missing_before_year(df, 2010, img_path)
        reset_id()
        export_json(df)

        image_path = 'DataNotSplitted/images'
        json_path = 'DataNotSplitted/missing_people_final.json'
        rename_dir(image_path, json_path)
        if len(os.listdir(img_path)) == len(list(df.name_arabic)):
            print('Images and json file are consistant')
        print(f"number of people in directory: {len(os.listdir(img_path))}")
        print(f"number of people in json fle: {len(list(df.name_arabic))}")
    else:
        print(f'{to_path} Directory Exists.')
        print(f'To run the code again delete the created folders.')
