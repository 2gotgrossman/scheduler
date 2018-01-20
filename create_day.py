import  google_cal
import trello_helper
import pytz

EST = pytz.timezone('US/Eastern')

from datetime import datetime, timedelta


now_board_id = "58ba055c236d1b24f3ecdd3a"
calendar_list_id = "5a62abada67a82fe63fcae9a"
backlog_list_id = "59170914545505a2f247ce6c"

scheduler_id = "hb2rb5mfqnokct3st6l0hbbiik@group.calendar.google.com"

todos = trello_helper.get_list_of_cards_from_list(backlog_list_id)
cal = google_cal.Calendar()
events = cal.get_todays_events()

print("Number of TODOS:", len(todos))
tasks = trello_helper.List(todos)
# for todo in todos:
#     print(todo['labels'])
for event in events:
    print(event)

tomorrow = datetime.now(tz=EST)
END_OF_DAY = datetime(year=tomorrow.year, month=tomorrow.month,
                            day=tomorrow.day, hour=20, minute=0, second=0, tzinfo=EST)

def get_time_from_gcal(time):
    time = time[:-3] + time[-2:]
    return datetime.strptime(time, '%Y-%m-%dT%H:%M:%S%z')

def is_dateTime(event, key):
    if 'dateTime' in event[key]:
        return True
    else:
        return False

def get_next_time_block(events, curr_time):
    for event in events:
        if is_dateTime(event, 'start'):
            start = get_time_from_gcal(event['start']['dateTime'])
            end = get_time_from_gcal(event['end']['dateTime'])
            print("Start Time:", start)
            if start > curr_time:
                return curr_time, start
            elif start <= curr_time and end > curr_time:
                curr_time = end
    # If no more events in the day
    return curr_time, END_OF_DAY


def create_day(tasks, events):
    curr_time = datetime.now(tz=EST)
    while curr_time < END_OF_DAY:
        start, end = get_next_time_block(events, curr_time)
        print("Curr Time:", curr_time)
        for task in tasks.cards:
            if task.scheduled == False:
                if task.time_for_completion() < (end - start):
                    cal.schedule_todo(task.name, start.isoformat(), (start + task.time_for_completion()).isoformat(),
                                      calendar_id = scheduler_id)
                    curr_time = start + task.time_for_completion()
                    task.scheduled = True
                    print("Start:", start, "End", curr_time, task.name)
                    break
        else:
            # If we couldn't schedule a task, either they are all scheduled already or no task fit in the time constraint
            if all(task.scheduled for task in tasks.cards):
                break
            else:
                curr_time = end

# cal.delete_today(scheduler_id)

create_day(tasks, events)

