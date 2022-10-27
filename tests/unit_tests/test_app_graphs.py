import unittest

import pandas as pd

from app.graphs import title_fix, stacked_bar_chart, meeting_chart, activity_chart
from pandas import DataFrame
import numpy as np



class test_graphs(unittest.TestCase):

    def setUp(self):
        self.title_fix_text, self.title_fix_text_fixed = "This_is_text!", "This Is Text!"
        tech_stacks = ["Career Development", "iOS", "iOS", "Backend", "Android"]
        self.df_stack_by_role = DataFrame({"tech_stack": np.random.choice(tech_stacks, 45),
                                           "role": np.random.choice(["Mentee", "Mentor"], 45)}
                                          )
        self.df_meetings = pd.read_csv('test_meeting.csv')
        self.df_mentor_mentees = pd.read_csv('test_mentor_mentee.csv')

    def test_title_fix(self):
        self.assertEqual(title_fix(self.title_fix_text), self.title_fix_text_fixed)
        self.assertEqual(title_fix(self.title_fix_text_fixed), self.title_fix_text_fixed)
        self.assertEqual(title_fix(""), "")

    def test_stacked_bar_chart(self):
        test_chart = stacked_bar_chart(self.df_stack_by_role, "tech_stack", "role").to_dict()

    def test_meetings_missed_chart(self):
        test_chart = meeting_chart(self.df_meetings,
                                   "meeting_missed_by_mentee",
                                   "count(meeting_missed_by_mentee)"
                                   ).to_dict()

    def test_meetings_topics_chart(self):
        test_chart = meeting_chart(self.df_meetings,
                                   "meeting_topic",
                                   "count(meeting_topic)",
                                   ).to_dict()

    def test_is_active_chart(self):
        test_chart = activity_chart(self.df_mentor_mentees,
                                    "is_active",
                                    "role",
                                    ).to_dict()


if __name__ == '__main__':
    unittest.main()
