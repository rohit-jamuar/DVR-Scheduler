#DVR - Scheduler

A terminal based scheduler for programming a DVR. It allows one to choose number of tuners that is expected from the DVR system.

##Functions supported:
  * **add( sched )** - To add a new channel for recording. Variable `sched` needs to have the following format `mm/dd/yyyy hh:mm[am|pm]-hh:mm[am|pm] channel_number`.
  * **get( sched )** - To check if something is scheduled at time-frame `sched`. If somethig is scheduled at any of the tuners, the function prints the list of scheduled channels on **STDOUT**. `sched` needs to be fed in the following format `mm/dd/yyyy hh:mm[am|pm]`.
  * **remove( sched )** - To remove an existing `sched` from the scheduler. It checks if `sched` is scheduled to be recorded by one of the tuners. If so, it removes the `sched` from its internal data-store. Variable `sched` needs to have the following format `mm/dd/yyyy hh:mm[am|pm]-hh:mm[am|pm] channel_number`.
  * **view_scheduled()** - To view all the channels which have been scheduled by the user. The method prints all the scheduled channels in a chronological manner to **STDOUT**.
  
###Run: 
`python dvr_scheduler.py`

###Requirements:
  * Python 2.7

