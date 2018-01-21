import gcal
import trellz
from datetime import timedelta
import gdate


now_board_id = trellz.now_board_id
tasks_on_the_docket_id = trellz.tasks_on_the_docket_id
current_tasks_list_id = trellz.tasks_on_the_docket_id

scheduler_calendar_id = "hb2rb5mfqnokct3st6l0hbbiik@group.calendar.google.com"

tomorrow = gdate.get_now() + timedelta(days=1)
END_OF_DAY = gdate.get_midnight(tomorrow) - timedelta(hours=1)  # 8PM


def is_dateTime(event, key):
    if 'dateTime' in event[key]:
        return True
    else:
        return False

def get_next_time_block(events, curr_time):
    for event in events:
        if is_dateTime(event, 'start'):
            start = gdate.gdate_to_datetime(event['start']['dateTime'])
            end = gdate.gdate_to_datetime(event['end']['dateTime'])

            if start > curr_time:
                return curr_time, start
            elif start <= curr_time < end:
                curr_time = end
    # If no more events in the day
    return curr_time, END_OF_DAY


def create_day(tasks, events):
    tasks_to_schedule = []
    curr_time = gdate.get_now()
    while curr_time < END_OF_DAY:
        start, end = get_next_time_block(events, curr_time)

        for task in tasks.prioritize():
            if not task.scheduled:
                completion_time = start + task.time_for_completion()

                if completion_time < end:
                    tasks_to_schedule.append({'name': task.name, 'start': gdate.datetime_to_gdate(start),
                                              'end': gdate.datetime_to_gdate(completion_time)})
                    curr_time = completion_time
                    task.scheduled = True
                    print("Start:", start, "End", curr_time, task.name)
                    break
        else:
            # If we couldn't schedule a task, either they are all scheduled
            # already or no task fit in the time constraint
            if all(task.scheduled for task in tasks.cards):
                break
            else:
                curr_time = end
    return tasks_to_schedule


def main():
    todos = trellz.get_list_of_cards_from_list(tasks_on_the_docket_id)
    cal = gcal.Calendar()
    events = cal.get_todays_events()

    tasks = trellz.List(todos)

    cal.delete_today(scheduler_calendar_id)

    tasks_to_schedule = create_day(tasks, events)

    for task in tasks_to_schedule:
        cal.schedule_task(task['name'], task['start'], task['end'], calendar_id=scheduler_calendar_id)


main()