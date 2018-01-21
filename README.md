# Scheduler 1.0

## The need / story

Self control is hard to come by. Sometimes, there's a lot of things to do and I can't decide what to do / what's the order to do it in. Many times, I spend more time thinking about what I need to do than I spend doing things.

Also, I at times can make a perfect schedule, but then things happen. Something really interesting in the moment comes up (hanging out with friends, a good conversation, etc), but my day does not adapt. I want my schedule to adapt to changes in how I complete my schedule.

## Minimum requirements for the solution

1. User inputs TODO items - DONE
2. Scheduler schedules items in calendar - DONE
3. If task complete, it is removed (by user or scheduler) from TODOs. -DONE
4. If task is incomplete in the time period and user needs a new calendar, user can refresh the calendar.

## Cool features
1. TODO items input into Trello
2. Calendar updated on Google  Calendar - DONE
3. Priority of tasks 
4. Due dates of tasks
5. Types of tasks

## Big things to implement
1. INPUT EVENT
2. STORE EVENT (can probably be done just with Trello)
3. CREATE DAY
4. COMPLETE EVENT 
5. REFRESH CALENDAR

# Time for a Rewrite
The bare bones have been implemented. It's time to do a rewrite of the design. The high level works, but we need to get beyond spaghetti code. There are plenty of features to add, but we have to work with something a bit cleaner. So here's the next set of TODOs:
1. Create timedate functions -- to and from datetime and GCal
2. Extract the parameter specific parts of the code from the Object Oriented structure -- Use a separate module that will have the parameters

## Let's Get Them Features Done!
1. Priority of tasks - take labels into account
2. Figure out where to host code
3. If I don't have plans for lunch or dinner, leave space open
4. For repeating tasks, add them to the backlog
5. Move tasks that are booked to a Sprint list
6. At the beginning of every day, delete all repeat tasks, add new repeat tasks, and give priority to the missed tasks from yesterday


