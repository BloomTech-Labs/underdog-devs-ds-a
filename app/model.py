from typing import Dict, List, Optional, Tuple

from app.data import MongoDB


class MenteeMatcherSearch:
    """Callable matching class implementing sorted search algorithm."""
    db = MongoDB()

    def __call__(self, profile_id: str, n_matches: Optional[int] = None) -> List[str]:
        """Return a list of profile_id for matched mentors."""
        mentee = self.db.first("Mentees", {"profile_id": profile_id})

        def sort_mentors(mentor: Dict) -> Tuple:
            return (
                mentee["pair_programming"] != mentor["pair_programming"],
                mentee["job_help"] != mentor["job_help"],
                not mentor["industry_knowledge"],
            )

        results = sorted(
            self.db.read("Mentors", {
                "tech_stack": mentee["tech_stack"],
                "is_active": True,
                "accepting_new_mentees": True,
                "validate_status": "approved",
                "profile_id": {"$nin": mentee["matches"]},
            }),
            key=sort_mentors,
        )[:n_matches]
        return [mentor["profile_id"] for mentor in results]


class MentorMatcherSearch:
    """Callable matching class implementing sorted search algorithm."""
    db = MongoDB()

    def __call__(self, profile_id: str, n_matches: Optional[int] = None) -> List[str]:
        """Return a list of profile_id for matched mentees."""
        mentor = self.db.first("Mentors", {"profile_id": profile_id})
        print(mentor)

        def sort_mentees(mentee: Dict) -> Tuple:
            return (
                mentor["pair_programming"] != mentee["pair_programming"],
                mentor["job_help"] != mentee["job_help"],
            )

        results = sorted(
            self.db.read("Mentees", {
                "tech_stack": {"$in": mentor["tech_stack"]},
                "is_active": True,
                "validate_status": "approved",
                "profile_id": {"$nin": mentor["matches"]},
            }),
            key=sort_mentees,
        )[:n_matches]
        return [mentee["profile_id"] for mentee in results]
