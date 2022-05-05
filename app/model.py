from random import sample, choice
from typing import List, Tuple, Dict

from app.data import MongoDB
from app.utilities import dict_to_str


class MatcherSortSearch:
    """Callable matching class implementing simple sort-search algorithm.

    Searches for mentors in database that match the given mentee's
    subject, and then organizes subsequent mentors based on
    mentee's subject of interest and their self-defined skill
    level, corresponding to mentors' teachable tech_stack and desired
    skill level(s) to teach.
    """
    db = MongoDB("UnderdogDevs")

    def __call__(self, n_matches: int, profile_id: str) -> List[str]:
        """Return a list of matched mentor id string.
        Args:
            n_matches (int): Number of mentor matches desired
            profile_id (str): ID strings of mentee that needs mentor

        Returns:
            List of mentor ID strings
        """
        mentee = self.db.first("Mentees", {"profile_id": profile_id})

        def sort_mentors(mentor: Dict) -> Tuple:
            return (
                mentee["experience_level"] != mentor["experience_level"],
                mentee["pair_programming"] != mentor["pair_programming"],
                mentor["industry_knowledge"],
            )

        results = sorted(
            self.db.search("Mentors", mentee["tech_stack"]),
            key=sort_mentors,
        )[:n_matches]
        return [mentor["profile_id"] for mentor in results]


class MatcherSortSearchResource:
    db = MongoDB("UnderdogDevs")

    def __call__(self, n_matches: int, item_id: str) -> List[str]:
        item = self.db.first("Resources", {"item_id": item_id})

        def sort_mentees(mentee: Dict) -> Tuple:

            # need to know which parameters the stakeholder wants to consider for resource matching
            return (
                mentee["need"] != item["name"],
                not mentee["parole_restriction"],
                not mentee["disability"],
                mentee["assistance"],
                mentee["work_status"],
            )

        results = sorted(
            self.db.search("Mentees", item["name"]),
            key=sort_mentees
        )[:n_matches]
        return [mentee["profile_id"] for mentee in results]


if __name__ == '__main__':
    matcher = MatcherSortSearch()

    db = matcher.db
    mentees = db.read("Mentees")
    test_user_id = choice(mentees)["profile_id"]
    matches = matcher(3, test_user_id)

    print(f"Mentee: {test_user_id}")
    print(f"Matches: {matches}")

    print(dict_to_str(db.first("Mentees", {"profile_id": test_user_id})))
    for mentor_id in matches:
        print(dict_to_str(db.first("Mentors", {"profile_id": mentor_id})))
