import sys
sys.path.append('/Users/David/anaconda/envs/sched/lib/python3.6/site-packages/')
import create_day
import click

@click.group()
def D20():
    pass

@D20.command()
def start():
    d = create_day.David20()
    d.reset_the_day()
    d.schedule_the_day()

@D20.command()
def clear():
    d = create_day.David20()
    d.clear_the_day()

@D20.command()
def update():
    d = create_day.David20()
    d.update_schedule()

# @D20.command()
@click.option("--many", is_flag = True)
def finish(many):
    d = create_day.David20()
    current_tasks = d.get_current_tasks()

    if len(current_tasks) == 0:
        print("No current tasks.")
        return

    for i, task_name in enumerate(current_tasks):
        print("({0}): {1}".format(i, task_name))


    value = 99
    if many:
        while value != -1:
            value = click.prompt('Enter task to delete (-1 to quit)', type=int)
            d.complete_task(current_tasks[value])
    else:
        value = click.prompt('Enter task to delete (-1 to quit)', type=int)
        d.complete_task(current_tasks[value])

    print("Drink a glass of water, take 10 deep breaths, and then get to the next one!")


# D20 add --repeat-task