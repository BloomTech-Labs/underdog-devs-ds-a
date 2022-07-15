import math as m
import numpy as np
import pandas as pd


def add_computer_assignment_rating(adict):
    """Adds the computer matching rating to the dictionary
    and sets the already matched flag to false.
    It sets the already matched flag after instead of being
    in the default schema for organizational purposes of
    all numbers being next to each other in the collection.
    Requires a dictionary with the following schema:
    {
    "profile_id": '00u13oned0U8XP8Mb4x7',
    "first_name": 'Exam',
    "last_name": 'Pull',
    "need_new_comp": 2,
    "need_help_acquiring": 1,
    }
    """

    x = adict['need_help_acquiring']
    y = adict['need_new_comp']
    rating_unfiltered = (x ** 2 - m.floor((.7 * x))) * (abs(y ** 3 - y ** 2 - y))
    rating_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    sortvals = [0, 1, 2, 3, 6, 7, 14, 15, 45, 105]
    rating_filtered = int(
        np.interp(rating_unfiltered, sortvals, rating_numbers))
    adict['rating'] = rating_filtered
    adict['already_matched'] = False
    return adict


def computer_assignment_visualizer(mongodb_class_instance):
    """
    Constructs a visual for the computer assignment
    rating.  Requires the database connection, this
    function automatically calls the collection.
    Returns a pandas dataframe.
    """

    collection = 'computer_assignment'
    search_query = {'already_matched': False}
    data = mongodb_class_instance.read(collection, search_query)
    dataframe = pd.DataFrame(data)
    dataframe.drop(columns=[
        'need_new_comp',
        'need_help_acquiring',
        'already_matched',
    ], inplace=True)
    # V Prevents false error popup for next step V
    pd.set_option('mode.chained_assignment', None)
    for x in dataframe.index:
        dataframe['rating'][x] = '⭐️' * dataframe['rating'][x]
    dataframe.set_index('profile_id', inplace=True)
    return dataframe.sort_values('rating', ascending=False).to_html()
