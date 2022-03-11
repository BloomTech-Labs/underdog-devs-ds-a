from random import sample
from typing import Dict, List
import pandas

from pandas import DataFrame

from app.data import MongoDB

data: List[Dict] = MongoDB("UnderdogDevs").read("Mentors")


def rand_lib(n_matches: int) -> List[str]:
    return [match["profile_id"] for match in sample(data, k=n_matches)]


def pandas_lib(n_matches: int) -> List[str]:
    return DataFrame(data).sample(n_matches)["profile_id"].to_list()


if __name__ == '__main__':
    from MonkeyScope import timer

    N = 3
    print(rand_lib(N))
    print(pandas_lib(N))
    print()
    print("rand_lib", end=": ")
    timer(rand_lib, N)
    print("pandas_lib", end=": ")
    timer(pandas_lib, N)
