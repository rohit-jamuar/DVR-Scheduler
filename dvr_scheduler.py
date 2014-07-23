#!/usr/bin/python

from datetime import datetime

class Scheduler:
    '''
    DVR Scheduler v0.1
    '''

    def __init__(self, k):
        '''
        data-layout : 
        { tuner_i : { date_j : [ { (start_k, end_k) : channel_l }, ... ] }, ... }
        '''
        self.tuners = [ 't'+str(i+1) for i in range(k) ]
        self.data = { elem : {} for elem in self.tuners }
        self.recordings_on = set()

    @staticmethod
    def __get_time(time_var, convert):
        '''
        If convert == 'to':
        Returns the integral representation of time passed as string. If the passed
        argument is an invalid representation, False is returned.
        The argument has to be passed in this format - hh:mm[am|pm|AM|PM]
        
        If convert == 'from':
        Returns time as string in the following format hh:mm[am|pm]
        If the passed argument ('time_var') is improper, False is returned.
        '''
        try:
            if convert == 'to':
                time_var = time_var.upper()
                date_object = datetime.strptime(time_var, '%I:%M%p')
                return (date_object.hour * 100) + date_object.minute
            elif convert == 'from':
                if type(time_var) == int and 0 <= time_var <= 2359:
                    hrs = time_var / 100
                    mins = str(time_var % 100)
                    is_pm = False
                    
                    if hrs > 12:
                        hrs -= 12
                        is_pm = True
                    hrs = str(hrs)
                    if len(hrs) == 1:
                        hrs = '0' + hrs
                            
                    if len(mins) == 1:
                        mins = '0' + mins
                    
                    if is_pm:
                        return hrs+":"+mins+'pm'
                    else:
                        return hrs+":"+mins+'am'
                else:
                    raise ValueError
            return False
        except ValueError:
            return False

    @staticmethod
    def __get_datetime_obj(date_str):
        '''
        A Datetime object for the 'date_str' string is returned. The validity of the
        presented string is checked against the following pattern - mm/dd/YYYY
        '''
        try:
            return datetime.strptime(date_str, '%m/%d/%Y')
        except ValueError:
            return False

    @staticmethod
    def __process_input(schedule_input, action):
        '''
        Process the input entered by user; depending on the 'action', values are 
        appropriately returned. If there is an error in user-input, the function
        returns False.
        '''
        if action in ['add', 'remove']:
            if schedule_input.count(' ') == 2:
                date, slot, channel = schedule_input.split()
                
                if '-' in slot:
                    start, end = slot.split('-')
                
                    start = Scheduler.__get_time(start, 'to')
                    end = Scheduler.__get_time(end, 'to')
                    date = Scheduler.__get_datetime_obj(date)

                    if start and end and date and start < end:
                        return (start, end, date, channel)
            return False
        
        elif action == 'get':
            if schedule_input.count(' ') == 1:
                date, time_var = schedule_input.split()
                
                date = Scheduler.__get_datetime_obj(date)
                time = Scheduler.__get_time(time_var, 'to')

                if date and time:
                    return (date, time)
        return False

    def add(self, schedule_input):
        '''
        This function tries to add {date, time-slot, channel} (provided as 'l') to the
        existing data-structure ('self.data'). The function, primarily, tries to
        add the request to first tuner's internal data-structure. If there is a 
        schedule-conflict, second tuner is searched into, and so on. If there is a conflict
        there in all the tuners, the user is notified of the conflict and the request is 
        dropped. All the insertions are made in an non-decreasing order.
        '''
        processed_input = Scheduler.__process_input(schedule_input, 'add')

        if processed_input:
            start = processed_input[0]
            end = processed_input[1]
            date = processed_input[2]
            channel = processed_input[3]

            data_to_insert = {(start, end) : channel}
            self.recordings_on.add(date)
            
            for tuner in self.tuners:
                if date in self.data[tuner]:
                    temp = self.data[tuner][date]

                    s_i = temp[0].keys()[0][0]
                    if end <= s_i:
                        self.data[tuner][date].insert(0, data_to_insert)
                        return

                    index = 0
                    while index < len(temp)-1:
                        e_1 = temp[index].keys()[0][1]
                        s_2 = temp[index+1].keys()[0][0]
                        if start >= e_1 and end <= s_2 :
                            temp.insert(index+1, data_to_insert)  
                            self.data[tuner][date] = temp
                            return
                        index += 1

                    e_i = temp[-1].keys()[0][1]
                    if start >= e_i:
                        self.data[tuner][date].append(data_to_insert)
                        return
                else:
                    self.data[tuner][date] = [data_to_insert]
                    return

            print "All the tuners are busy! This request cannot be completed."
        
        else:
            print "The time-slot has to be entered in H:MM[AM|PM] format",
            print "and / or the date has to be entered in H:MM[am|pm] !"

    def get(self, schedule_input):
        '''
        This function checks if any of the tuners have a channel scheduled at the 
        {date, time} provided by user.
        '''
        processed_input = Scheduler.__process_input(schedule_input, 'get')
        
        if processed_input:
            date = processed_input[0]
            time = processed_input[1]
            active_channels = []

            for tuner in self.tuners:
                if date in self.data[tuner]:
                    for slots in self.data[tuner][date]:
                        s_0, e_0 = slots.keys()[0][0], slots.keys()[0][1]
                        if s_0 <= time <= e_0:
                            for elem in slots.values():
                                active_channels.append( elem )
            if active_channels:
                print "The channel(s) being recorded is / are -",
                print ', '.join( [elem for elem in active_channels] )
            else:
                print "No channel has been scheduled at the time specified !"
        else:
            print "The time-slot has to be entered in H:MM[AM|PM] format",
            print "and / or the date has to be entered in H:MM[am|pm] !"

    def remove(self, schedule_input):
        '''
        This function removes a schedule (represented by 'schedule_input') from DVR.
        '''
        processed_input = Scheduler.__process_input(schedule_input, 'remove')

        if processed_input:
            start = processed_input[0]
            end = processed_input[1]
            date = processed_input[2]
            channel = processed_input[3]

            for tuner in self.tuners:
                if date in self.data[tuner]:
                    temp = self.data[tuner][date]
                    for index in range(len(temp)):
                        s_0 = temp[index].keys()[0][0]
                        e_0 = temp[index].keys()[0][1]
                        if s_0 == start and e_0 == end:
                            for elem in temp[index].values():
                                if elem ==  channel:
                                    temp = temp[:index] + temp[index+1:]
                                    if not temp:
                                        del self.data[tuner][date]
                                    else:
                                        self.data[tuner][date] = temp
                                    print "Removed '%s' !" % schedule_input
                                    return
            print "Could not find '%s' !" % schedule_input
        else:
            print "The time-slot has to be entered in H:MM[AM|PM] format",
            print "and / or the date has to be entered in H:MM[am|pm] !"

    def view_scheduled(self):
        '''
        Shows all the scheduled recordings on STDOUT
        '''
        for date in sorted(self.recordings_on):
            sched = []
            for tuner in self.tuners:
                if date in self.data[tuner]:
                    for item in self.data[tuner][date]:
                        sched.append(item)
            if sched:
                sched.sort(key = lambda x : x.keys()[0][0])
                current_date = date.date()
                print "\nDate : %d/%d/%d" \
                % (current_date.month, current_date.day, current_date.year)
                
                for elem in sched:
                    s_0 = Scheduler.__get_time(elem.keys()[0][0], 'from')
                    e_0 = Scheduler.__get_time(elem.keys()[0][1], 'from')
                    print "From %s to %s -- %s" % (s_0, e_0, elem.values())

if __name__ == '__main__':
        
    TUNER_COUNT = int(raw_input("Enter # of tuners - "))
    if TUNER_COUNT >= 1:
        SCHED = Scheduler(TUNER_COUNT)
        
        print "\nEnter -"
        print "S : to enter a schedule\nQ : to query using time"
        print "R : to remove a schedule\nV : to view entire schedule"
        print "X : to quit\n"
        
        while True:
            USER_INPUT = raw_input("\nCommand - ")
            if USER_INPUT in ['X', 'x']:
                break
            elif USER_INPUT in ['S', 's']:
                SCHEDULE = raw_input("Enter schedule: ")
                SCHED.add(SCHEDULE.strip())
            elif USER_INPUT in ['Q', 'q']:
                QUERY = raw_input("Enter query: ")
                SCHED.get(QUERY.strip())
            elif USER_INPUT in ['R', 'r']:
                SCHEDULE_R = raw_input("Enter schedule to remove: ")
                SCHED.remove(SCHEDULE_R.strip())
            elif USER_INPUT in ['v', 'V']:
                SCHED.view_scheduled()
