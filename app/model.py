from random import sample, choice
from typing import List, Tuple, Dict

from app.data import MongoDB
from app.utilities import dict_to_str


class MatcherSort:
    db = MongoDB("UnderdogDevs")

    def __call__(self, n_matches: int, mentee_id: int) -> List[int]:
        mentee = self.db.first("Mentees", {"user_id": mentee_id})

        def sort_mentors(mentor: Dict) -> Tuple:
            return (
                mentee["subject"] != mentor["subject"],
                mentee["skill_level"] != mentor["skill_level"],
            )

        results = sorted(self.db.read("Mentors"), key=sort_mentors)[:n_matches]
        return [mentor["user_id"] for mentor in results]


class MatcherSearch:
    db = MongoDB("UnderdogDevs")

    def __call__(self, n_matches: int, mentee_id: int) -> List[int]:
        mentee = self.db.first("Mentees", {"user_id": mentee_id})
        results = self.db.search("Mentors", mentee["subject"])[:n_matches]
        return [mentor["user_id"] for mentor in results]


class MatcherSortSearch:
    db = MongoDB("UnderdogDevs")

    def __call__(self, n_matches: int, mentee_id: int) -> List[int]:
        mentee = self.db.first("Mentees", {"user_id": mentee_id})

        def sort_mentors(mentor: Dict) -> Tuple:
            return (
                mentee["subject"] != mentor["subject"],
                mentee["skill_level"] != mentor["skill_level"],
            )

        results = sorted(
            self.db.search("Mentors", mentee["subject"]),
            key=sort_mentors,
        )[:n_matches]
        return [mentor["user_id"] for mentor in results]


class MatcherRandom:
    db = MongoDB("UnderdogDevs")

    def __call__(self, n_matches: int, mentee_id: int) -> List[int]:
        results = sample(self.db.read("Mentors"), k=n_matches)
        return [mentor["user_id"] for mentor in results]


if __name__ == '__main__':
    matcher = MatcherSortSearch()

    db = matcher.db
    mentees = db.read("Mentees")
    test_user_id = choice(mentees)["user_id"]
    matches = matcher(3, test_user_id)

    print(f"Mentee: {test_user_id}")
    print(f"Matches: {matches}")

    print(dict_to_str(db.first("Mentees", {"user_id": test_user_id})))
    for mentor_id in matches:
        print(dict_to_str(db.first("Mentors", {"user_id": mentor_id})))
