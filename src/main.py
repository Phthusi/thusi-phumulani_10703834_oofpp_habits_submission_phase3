from components.add_habit.controller import add_habit_controller
from components.delete_habit.controller import delete_habit_controller
from components.update_habit.controller import update_habit_controller
from components.get_habit.view import get_habit_view
from services.inputs import command_loop

add_habit = add_habit_controller.AddHabitController()
update_habit = update_habit_controller.UpdateHabitController()
get_habit = get_habit_view.GetHabitView()
delete_habit = delete_habit_controller.DeleteHabitController()

commands = {
    'create habit':add_habit.execute,
    'update habit':update_habit.execute,
    'get habits':get_habit.get_habit,
    'delete habit':delete_habit.execute
}

print(
r"""
===========================================================================================================

    ██╗  ██╗ █████╗ ██████╗ ██╗████████╗    ████████╗██████╗  █████╗  ██████╗██╗  ██╗███████╗██████╗ 
    ██║  ██║██╔══██╗██╔══██╗██║╚══██╔══╝    ╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
    ███████║███████║██████╔╝██║   ██║          ██║   ██████╔╝███████║██║     █████╔╝ █████╗  ██████╔╝
    ██╔══██║██╔══██║██╔══██╗██║   ██║          ██║   ██╔══██╗██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
    ██║  ██║██║  ██║██████╔╝██║   ██║          ██║   ██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║
    ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝   ╚═╝          ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
                                [🚀 Build consistency. Track growth.]
===========================================================================================================
"""
)

update_habit.update_statuses()
command_loop(commands,switched_to="home")

print(r"""
===========================================================================================================

    Thanks for using HABIT TRACKER 🙌

    Consistency is built one action at a time.
    See you again soon.

                                [ Exit complete. Stay disciplined. ]
===========================================================================================================
""")
update_habit.update_statuses()
