from random import sample
from typing import Dict, List

from pandas import DataFrame

from app.data import MongoDB

data: List[Dict] = MongoDB("UnderdogDevs").read("Mentors")


def rand_lib(n_matches: int) -> List[str]:
    return [match["user_id"] for match in sample(data, k=n_matches)]


def pandas_lib(n_matches: int) -> List[str]:
    return DataFrame(data).sample(n_matches)["user_id"].to_list()


if __name__ == '__main__':
    '''
    N = 3
    print(rand_lib(N))
    print(pandas_lib(N))
    print()
    print("rand_lib", end=": ")
    print("pandas_lib", end=": ")
    '''
    print(data)