from src.components.get_habit.view.get_habit_view import GetHabitView
from src.components.search_habit.controller.search_habit_controller import SearchHabit, HabitFactory
from itertools import groupby

class HabitAnalytics:
    def __init__(self):
        self.habit_factory = HabitFactory()
        self.habits = self.habit_factory.get_habits()
        self.habits.sort(key=lambda habit:habit[3])

    def streaks(self,habits):
        all_statuses = [record[5] for record in habits]
        # remove entries that haven't happened yet
        past_statuses = [status for status in all_statuses if status != "UPCOMING"]
        # Group consecutive 'DONE' statuses and return their lengths
        return [len(list(group)) for status, group in groupby(past_statuses) if status == "DONE"]

    def latest_streak(self,habits):
        return self.streaks(habits)[-7:]

    def longest_streak(self,habits):
        habit_streaks = self.streaks(habits)
        if len(habit_streaks)==0:
            return 0
        return max(habit_streaks)

    def shortest_streak(self,habits):
        habit_streaks = self.streaks(habits)
        if len(habit_streaks)==0:
            return 0
        return min(habit_streaks)

    def get_habit_names(self):
        return {habit[2] for habit in self.habit_factory.get_habits()}

    def completion_rate(self,habits):
        missed_sessions = list(filter(lambda habit:habit[5]=="MISSED",habits))
        done_sessions = list(filter(lambda habit:habit[5]=="DONE",habits))
        total = (len(done_sessions)+len(missed_sessions))
        if total == 0: return "0%"
        rate = (len(done_sessions)/total)*100
        return f"{rate}%, Missed={len(missed_sessions)}, Done={len(done_sessions)}"

    def habit_with_longest_streak(self):
        habit_names = self.get_habit_names()
        habit_names_long_streaks = { 
            habit_name: self.longest_streak(self.habit_factory.get_name_with_text(habit_name))
            for habit_name in habit_names
        }
        highest_streak = max(habit_names_long_streaks.values())
        habits = [name for name in habit_names_long_streaks.keys() if highest_streak==habit_names_long_streaks.get(name)]
        return habits
    
    def habit_rates(self,habit_name):
        # if 
        self.habit_factory.get_name_with_text(habit_name)

x = HabitAnalytics()
# print(habit_with_longest_streak())
print(x.habit_with_longest_streak())


# current_streak
# habit_with_most_misses
# success_rate
# average_streak