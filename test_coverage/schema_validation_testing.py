from app.schema import Mentor
from data_generators.generators import RandomMentor
# doctest

mentor = RandomMentor()
mentor_dict = vars(mentor)
print(mentor_dict)
created = mentor_dict.pop("created_at")
Mentor(**mentor_dict)

