import gcal
import trellz
from datetime import timedelta
import gdate


now_board_id = trellz.now_board_id
tasks_on_the_docket_id = trellz.tasks_on_the_docket_id
current_tasks_list_id = trellz.current_tasks_list_id

scheduler_calendar_id = "hb2rb5mfqnokct3st6l0hbbiik@group.calendar.google.com"

tomorrow = gdate.get_now() + timedelta(days=1)
END_OF_DAY = gdate.get_midnight(tomorrow) - timedelta(hours=0)  # 8PM


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


def create_schedule(tasks, events):
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



class David20():
    def __init__(self):
        self.cal = gcal.Calendar()

    def schedule_the_day(self):
        todos = trellz.get_list_of_cards_from_list(tasks_on_the_docket_id)
        current_tasks = trellz.get_list_of_cards_from_list(current_tasks_list_id)

        events = self.cal.get_todays_events()

        tasks = trellz.List(todos)
        tasks.add_cards(current_tasks)

        self.cal.delete_today(scheduler_calendar_id)

        tasks_to_schedule = create_schedule(tasks, events)

        for task in tasks_to_schedule:
            self.cal.schedule_task(task['name'], task['start'], task['end'], calendar_id=scheduler_calendar_id)
        for task in tasks.cards:
            if task.scheduled:
                print(task.name)
                task.move_to_list(current_tasks_list_id)

    def clear_the_day(self):
        """
        Moves all active tasks to the backlog
        :return: returns tasks that were moved to the backlog
        """
        self.cal.delete_today(scheduler_calendar_id)
        current_tasks = trellz.get_list_from_id(current_tasks_list_id)

        # If we didn't complete the task today, increase its priority
        for task in current_tasks.cards:
            task.move_to_list(tasks_on_the_docket_id)

        return current_tasks

    def reset_the_day(self):
        """
        Clears the day and increases priorities of incomplete tasks
        :return: returns tasks that were moved to the backlog
        """
        tasks_moved_to_backlog = self.clear_the_day()
        for task in tasks_moved_to_backlog.cards:
            last_priority = trellz.get_label_priority(task.labels)
            if last_priority < 4:
                task.add_label(trellz.priority_map[last_priority + 1])

    def update_schedule(self):
        self.clear_the_day()
        self.schedule_the_day()

    def get_current_tasks(self):
        current_tasks = trellz.get_list_from_id(current_tasks_list_id)
        names = []
        for task in current_tasks.cards:
            names.append(task.name)

        return names

    # TODO: Clean up task in List of cards. We remove the card from Trello, but leave it in the calendar and List object
    def complete_task(self, name):
        current_tasks = trellz.get_list_from_id(current_tasks_list_id)
        for task in current_tasks.cards:
            if task.name == name:
                task.archive_me()


if __name__ == "__main__":
    D20 =David20()
    D20.schedule_the_day()
    D20.clear_the_day()

