# Scheduler 1.0

## The need / story

Self control is hard to come by. Sometimes, there's a lot of things to do and I can't decide what to do / what's the order to do it in. Many times, I spend more time thinking about what I need to do than I spend doing things.

Also, I at times can make a perfect schedule, but then things happen. Something really interesting in the moment comes up (hanging out with friends, a good conversation, etc), but my day does not adapt. I want my schedule to adapt to changes in how I complete my schedule.

## Minimum requirements for the solution

1. User inputs TODO items - DONE
2. Scheduler schedules items in calendar - DONE
3. If task complete, it is removed (by user or scheduler) from TODOs. -DONE
4. If task is incomplete in the time period and user needs a new calendar, user can refresh the calendar.

## Let's Get Them Features Done!
2. Figure out where to host code
3. If I don't have plans for lunch or dinner, leave space open
4. For repeating tasks, add them to the backlog
6. At the beginning of every day, delete all repeat tasks, add new repeat tasks, and give priority to the missed tasks from yesterday
7. When increasing the priority for a task that I did not complete today, remove its last priority.
8. Write multiple priority algorithms: random, choose a task from each tier, wait 15 minutes between tasks, prioritize longer or shorter tasks
9. Google Auth - Figure out how to only approve credentials only once or also from the command line
10. Mobility - Build a simple PowerUp with Webhook
11. Repeat Tasks - Daily TODOs that are scheduled either at a certain time or time range
12. Meal Time - Implement breaks for lunch and dinner
13. D20 Secure - Increase security of system. Nothing on GitHub should have personal info.
14. Click Input - Implement ability to create new task from command line.
15. Cap the amount of time for work in the day: start and end, total time.
16. Create task categories: Classwork, Coding, Health, Learning, Friends
17. Implement Due Dates
