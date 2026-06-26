#for testing 
from datetime import timedelta
import datetime as dt
import math

class Scheduler:
    def __init__(self, recurrings = None, commitments= None, dailies= None, deadlineds= None, hobbies= None, length = 14): 
        rows, cols = length, 96  # Example dimensions: 14 rows and 96 columns
        self.schedule= [[None for _ in range(cols)] for _ in range(rows)]

        # self.recurrings = [{"type":"re", "name": "Comp Sci Lecture" , "week_days": " 0 2 4", "time_pairs": "07:00-10:00 08:00-10:30 14:00-16:15"}, 
        #               {"type":"re","name": "History Lecture" , "week_days": " 0 1 ", "time_pairs": "10:00-12:00 08:00-10:30"}]
        # self.commitments = [{"type":"co","name": "birthday party", "date": "2024-07-28", "start": "19:00", "end": "24:00", "also_accomplishes":"dinner" }]
        # #end slot for dailies is the time at which you will finish the activity at the latest
        # self.dailies = [{"type":"da","name": "Sleep", "start": "23:30", "end": "10:30", "min_hours": "8", "max_hours": "9"}, 
        #                 {"type":"da","name": "Lunch", "start": "12:00", "end": "15:00", "min_hours": "0.5", "max_hours": "1"}, 
        #                 {"type":"da","name": "Teeth/ Shave/ Get Dressed", "start": "7:00", "end": "10:30", "min_hours": "0.25", "max_hours": "0.25"}, 
        #                 {"type":"da","name": "Dinner", "start": "19:00", "end": "22:00", "min_hours": "0.5", "max_hours": "1.5"}, 
        #                 {"type":"da","name": "Shower", "start": "8:00", "end": "23:00", "min_hours": "0.25", "max_hours": "0.25"}, 
        #                 {"type":"da","name": "Reading", "start": "07:15", "end": "11:00", "min_hours": "0.5", "max_hours": "1"}]
        # self.deadlineds = [{"type":"de", "name": "homework 1", "date": "2024-08-30", "hours_left": "5", "min_hours": "1", "max_hours": "2.0"}]

        # #also chores
        # #start and end times are for when you are okay with doing this hobby. Like if you only like watching old movies after 8, or at least its a night specific hobby
        # #the end would be used for if you didnt want to practice french after the morning or ealry afternoon
        # #date is for the date you last performed it in Y-m-d format
        # self.hobbies = [{"type":"ho", "name": "Painting", "frequency": "2", "date": "2024-08-20", "min_hours": "1", "max_hours": "5", "start": "04:00", "end": "11:00"},
        #                 {"type":"ho", "name": "Workout", "frequency": "2", "date": "2024-08-26", "min_hours": "1.5", "max_hours": "2", "start": "04:00", "end": "18:00"},  
        #                 {"type":"ho", "name": "French ", "frequency": "1", "date": "2024-08-20", "min_hours": "0.5", "max_hours": "1.5", "start": "04:00", "end": "04:00"}, 
        #                 {"type":"ho", "name": "Clay/Embroidery", "frequency": "4", "date": "2024-08-20", "min_hours": "0.5", "max_hours": "2", "start": "10:30", "end": "24:00"},
        #                 {"type":"ho", "name": "Drawing", "frequency": "1", "date": "2024-08-25", "min_hours": "0.5", "max_hours": "2", "start": "04:00", "end": "24:00"}, 
        #                 {"type":"ho", "name": "Baking", "frequency": "7", "date": "2024-08-01", "min_hours": "1.5", "max_hours": "2", "start": "12:00", "end": "11:00"}, 
        #                 {"type":"ho", "name": "Fancy Cooking", "frequency": "7", "date": "2024-08-03", "min_hours": "1", "max_hours": "2", "start": "12:00", "end": "22:00"}, 
        #                 {"type":"ho", "name": "Old Movies", "frequency": "5", "date": "2024-08-02", "min_hours": " 2", "max_hours": "2.5", "start": "18:00", "end": "24:00"}]
        self.recurrings =recurrings
        self.commitments = commitments
        print("**************7")
        self.dailies = dailies
        self.deadlineds = deadlineds
        self.hobbies = hobbies
        self.today = dt.datetime.today()
        self.today_string = self.today.strftime(r'%Y-%m-%d')
        self.events = []        
        self.length = length
        
        self.add_recurrings()
        self.add_commitments()
        self.add_dailies()
        self.add_deadlineds()
        print("**************8")
        self.add_hobbies()
        print("**************9")
        #self.review_fill() #only do this later
        self.view()
        self.convert_to_events()
        

    def add_recurrings(self):
        if self.recurrings == None:
            return
        #monday is 0, sunday is 1
        weekday_int = (dt.datetime.now().weekday() +1) %7 #tomorrows day int to start
        recurrings = self.recurrings
        for i in range(len(self.schedule)):
            for recurring in recurrings:
                weekday_ints = recurring['week_days'].split()
                time_ints = recurring['time_pairs'].split()
                #if the recurring is occuring on the current weekday_int
                if (str(weekday_int) in weekday_ints):
                    index = weekday_ints.index(str(weekday_int))
                    start = time_ints[index].split("-")[0]
                    end = time_ints[index].split("-")[1]
                    self.schedule_activity(i, recurring, start, end )
            weekday_int = (weekday_int +1) % 7

    def add_commitments(self):
        if self.commitments == None:
            return
        commitments = self.commitments
        current_day = dt.datetime.today().date() + timedelta(days= 1)    
        
        for i in range (len(self.schedule)):
            formatted_date = current_day.strftime(r'%Y-%m-%d')
            for commitment in commitments:
                print(formatted_date)
                if commitment['date'] == formatted_date:
                    #if the commmitment goes from night until next morning
                    if(self.get_index(commitment['start']) > self.get_index(commitment['end'])):
                        self.schedule_activity(i, commitment, commitment['start'], "24:00")
                        self.schedule_activity(i+1, commitment,"00:00", commitment['end'])
                    self.schedule_activity(i, commitment, commitment['start'], commitment['end'])
                    continue
            current_day = current_day + timedelta(days=1)
    
    def add_dailies(self):
        if self.dailies == None:
            return
        dailies  = self.order_by_start(self.dailies)
        
        #dailies = [daily for daily in dailies if daily["name"] != "Sleep"]
        #each current day is responsible for scheduling sleep starting at night through till tomorrow morning 
        
        #remove dailies from ordered list that are also_accomplished by commitments
        ##does one day then moves to the next
        for i in range (len(self.schedule)):
            for daily in dailies:
                name = daily["name"]
                print(f"Starting {name} on the {i}th day")
                if(daily["name"].lower() == "sleep"):
                    self.schedule_sleep(i, daily)
                    continue
                if self.already_accomplished(i, daily) == True:
                    continue
                slots = self.get_open_indexes(daily, i)
                if len(slots) == 0:
                    continue

                dailys_slots = self.trim_slots(daily, slots)
                if len(dailys_slots) == 0:
                    continue
                print(f"Ending {name}")
                

                self.schedule_activity(i, daily, dailys_slots[0], dailys_slots[len(dailys_slots) -1], "indexes")



    #version 1: plans for each deadlined activity will be created for the next two weeks
    #for those activities that will be completed in 2 weeks:
        # create plans and schedule them in. if there is a day when there is not enough time, then time will be added to another day   

        #if you wish to update your schedule or create a new schedule after adding some new commitments a few days later, just update the info for your current deadlined projects and hit submit
    #for those activities that will not be completed in two weeks
        # it will do the proper mah to figure out how many hours you should be working on stuff, but will only schedule in anything that you should do over the next few days

    #also- the deadline means the date that you are handing something in, so it should always be done by at least the day before, not on the deadline. You finish homework the night before, you finish studying for a test the night before a test, etc. 
    def add_deadlineds(self):
        if self.deadlineds == None:
            return
        deadlineds = self.order_by_deadline(self.deadlineds)
        for deadlined in deadlineds:
            two_week_plan= self.create_plan(deadlined)
            for i in range(len(two_week_plan)):
                #schedules the deadlined activity for each day according to the plan
                self.schedule_deadlined(i, deadlined, two_week_plan[i])     

    def add_hobbies(self):
        if self.hobbies == None:
            return
        date = self.today
        hobbies = self.hobbies
        for i in range(len(self.schedule)):
            date = date + timedelta(days=1)
            hobbies = self.order_by_priority(hobbies, date) #so date should start as tommorow, since thats the first day that the scheduler will make
            hobbies = self.schedule_hobbies(hobbies, date, i) # updates each hobbies' last performed date
        
        self.hobbies = hobbies

        


    def order_by_deadline(self, deadlineds):
        for i in range(len(deadlineds)):
            cur_soonest_deadline = deadlineds[i]
            days_till_soonest = 365
            soonest_deadline_index = -1
            for j in range(i+1, len(deadlineds)):
                if (days_till_soonest > self.days_between_date_strings(deadlineds[j]["date"], self.today_string)):
                    cur_soonest_deadline= deadlineds[j]
                    days_till_soonest = self.days_between_date_strings(deadlineds[j]["date"], self.today_string)
                    soonest_deadline_index = j  

            temp = deadlineds[i]
            deadlineds[i] = cur_soonest_deadline
            deadlineds[soonest_deadline_index] = temp        

        return deadlineds
    
    def order_by_priority(self, hobbies, date):        
        for i in range(len(hobbies)):
            cur_max_priority = self.find_priority(hobbies[i], date)
            cur_prioritized = hobbies[i]
            prioritized_index = i
            #goes through each hobby after i and finds the biggest prioritied one
            for j in range(i+1, len(hobbies)):
                temp_priority = self.find_priority(hobbies[j], date)
                temp_prioritized = hobbies[j]
                if (temp_priority > cur_max_priority):
                    cur_max_priority = temp_priority
                    cur_prioritized = temp_prioritized
                    prioritized_index = j

            temp = hobbies[i]
            hobbies[i] = cur_prioritized
            hobbies[prioritized_index] = temp

        return hobbies
    
    def schedule_hobbies(self, hobbies, date, day_int):
        date_string = date.strftime(r'%Y-%m-%d')

        hours_of_hobbies= 0
        counter = 0
        while hours_of_hobbies <= 6 and counter < 10:
            counter +=1
            for hobby in hobbies:
                open_indexes = self.get_open_indexes(hobby, day_int, "hobby")
                #maybe just add condition that if the length of open_indexes or if the length of trimmed indexes 
                # is less than min time, dont schedule
                if (len(open_indexes)==0):
                    continue
                trimmed_indexes = self.trim_slots(hobby, open_indexes)

                #if there is an available space in the day long enough to fit the hobby
                if len(trimmed_indexes) != 0:
                    self.schedule_activity_by_slots(day_int, hobby, trimmed_indexes)
                    hobby["date"] = date_string
                    hours_of_hobbies += len(trimmed_indexes)/4

        return hobbies

        #update hobbies with the date it is being scheduled for





    def find_priority(self, hobby, date = dt.datetime.now()):
        date_string = date.strftime(r'%Y-%m-%d')
        days_since = self.days_between_date_strings(date_string, hobby["date"])
        frequency = int(hobby["frequency"])

        # multiplier = frequency *7
        base_priority = days_since-frequency
        return base_priority *frequency


    
    def days_between_date_strings(self, date_string_1, date_string_2):
        date_1 = dt.datetime.strptime(date_string_1, r'%Y-%m-%d')
        date_2 = dt.datetime.strptime(date_string_2, r'%Y-%m-%d')
        return abs(date_2- date_1).days




    def create_plan(self, deadlined):
        #max_hours is only useful when scheduling so you know to put a small break after that amount of hours. 
        plan = [0] *56
        days_to_deadline = self.days_between_date_strings(deadlined["date"], self.today_string)
        min_daily_hours = float(deadlined["min_hours"])
        required_hours_left = float(deadlined["hours_left"])
        i = 0
        #schedules in minimum workoing hours for either enough days to finish, or until one day before the deadline
        while(required_hours_left>0 and i < days_to_deadline - 1):
            plan[i] = min(min_daily_hours, required_hours_left)
            required_hours_left -= min_daily_hours
            i+=1


        if (required_hours_left ==0):
            return plan
        
        #if still time left, add a half hour to each plan slot 
        while(required_hours_left>0):
            for j in range(min(days_to_deadline-1, len(plan)-1)):
                more_work = min(0.5, required_hours_left)
                plan[j] += more_work
                required_hours_left -= more_work
        
        return plan[0:self.length]

    def already_accomplished(self,schedule_day_index, daily):
        for i in range(96):
            if (self.schedule[schedule_day_index][i] != None):
                if (self.schedule[schedule_day_index][i]["type"] == "co"):
                    if(self.schedule[schedule_day_index][i]["also_accomplishes"] == daily["name"]):
                        return True
        return False

    #orders daily activities by their earliest starting time
    def order_by_start(self, dailies):

        for i in range (len(dailies)):
            cur_earliest_daily = dailies[i]
            cur_earliest_time_index = self.get_index(cur_earliest_daily["start"])
            earliest_daily_index = i
            for j in range(i+1, len(dailies)):
                if (cur_earliest_time_index > self.get_index(dailies[j]["start"])): #if the current daily starts after the temp one
                    cur_earliest_daily = dailies[j]                                 #the current daily becomes the temp one
                    cur_earliest_time_index = self.get_index(cur_earliest_daily["start"]) 
                    earliest_daily_index = j  

            temp = dailies[i]
            dailies[i] = cur_earliest_daily
            dailies[earliest_daily_index] = temp

        return dailies



    #accepts a daily activity or hobby activity, 'activity' and a list of indexes,'slots', of all the available timeslots within the dailies range
    #returns a list of the first slots that fit the minimum length of that daily activity
    def trim_slots(self, activity, slots):
        min_slots = self.convert_length(activity["min_hours"]) 
        trimmed = [slots[0]]
        in_a_row = 1
        
        for i in range(1, len(slots)):
            if (slots[i] == (slots[i-1] +1)):
                in_a_row +=1
                trimmed.append(slots[i])
            else:
                in_a_row = 1
                trimmed = [slots[i]]
            if in_a_row >= min_slots:
                trimmed = trimmed[0:min_slots]
                break
        if (in_a_row < min_slots):
            return []
        return trimmed

    

    def get_open_indexes(self, activity, i, type = "daily"):
        ##get all available indexes for day i in the 14 day schedule, between the dailies or hobbies starting and ending indexes. returns all available indexes for other activities
        available_indexes = []
        start_index = 0
        end_index = 96
        if (type == "daily" or type =="hobby"):
            start_index = self.get_index(activity["start"])
            end_index = self.get_index(activity["end"])          
        
        for j in range(start_index, end_index):
            if self.schedule[i][j] == None:
                available_indexes.append(j)
        
        return available_indexes
    
    #this method is responsible for scheduling in the nights sleep and the following morning  for the minimum required hours
    #on the first day it will fill sleep up to when the first daily activity occurs
    #on the last day it will only schedule in for the night
    #assumes that any activity you are doing that might go into the early morning will be connected to an activity from the previous night. for example its fine to be at a party from 10-pm to 1-am but not to just be 
    #somewhere from 1:30-am to 3-am
    def schedule_sleep(self, day_int, sleep):
        if (day_int == 0 ):
            for i in range(len(self.schedule[0])):
                if (self.schedule[0][i] == None):
                    self.schedule[0][i] = sleep
                else:
                    break
        
        ##get all available indexes for day i in the 14 day schedule, between the dailies starting and ending indexes. returns all available indexes for other activities
        night_sleep_indexes = []
        
        sleep_index = self.get_index(sleep["start"])
        wakeup_index = self.get_index(sleep["end"])

        #schedules sleep at night
        for j in range(sleep_index, 96):
            if self.schedule[day_int][j] == None:
                night_sleep_indexes.append(j)
        if len(night_sleep_indexes) !=0:
            night_sleep_indexes = self.trim_night_sleep(night_sleep_indexes)
            self.schedule_activity_by_slots(day_int, sleep, night_sleep_indexes)

        if day_int == len(self.schedule)-1:
            return

        #schedules sleep for next morning, filling in until youve gotten enogh sleep. Will wakeup before any commitments, but schedules morning sleep before any dailies have the opportunity to be 
        # scheduled in, so you will otherwise get your minimum sleep ours
        hours_of_sleep = len(night_sleep_indexes)/4
        sleep_still_needed = float(sleep["min_hours"]) - hours_of_sleep
        morning_sleep_indexes = []
        for j in range(0, wakeup_index):
            #this will end sleep a half hour before any commitmeents at the very latest
            if(self.schedule[day_int +1][j+2] != None):
                break
            if self.schedule[day_int +1][j] == None:
                morning_sleep_indexes.append(j)
                sleep_still_needed -=0.25
                if(sleep_still_needed <=0):
                    break
        #if sleep_still_needed > 0:
        #   add sleep still needed to previous night

        self.schedule_activity_by_slots(day_int+1, sleep, morning_sleep_indexes)
    

    def trim_night_sleep(self, night_sleep_indexes):
        trimmed = []
        if(night_sleep_indexes[len(night_sleep_indexes)-1] != 95):
            return trimmed
        trimmed= [night_sleep_indexes[len(night_sleep_indexes)-1]]
        for i in range (len(night_sleep_indexes)-2, -1, -1):
            if (night_sleep_indexes[i] +1 == night_sleep_indexes[i+1] ):
                trimmed.insert(0, night_sleep_indexes[i])
            else: 
                return trimmed
        return trimmed
                

    
    
    def schedule_deadlined(self, day_int, deadlined, planned_hours):
        if planned_hours ==0:
            return
        max_hours = float(deadlined["max_hours"])
        planned_slots_required = int(planned_hours *4)
        open_indexes = self.get_open_indexes(deadlined, day_int, "deadlined" )
        #continually shortens the available slots until the largest groups are left that allow for the required time 
        min_slots = 2
        temp_indexes = self.remove_small_segments(open_indexes,  min_slots)
        while(planned_slots_required<= len(temp_indexes) and planned_slots_required >= min_slots):
            open_indexes = temp_indexes
            min_slots+=1
            temp_indexes = self.remove_small_segments(open_indexes, min_slots)

        #schedules regarless of breaks
        self.schedule_activity_by_slots(day_int, deadlined, open_indexes[0:planned_slots_required])

        #check if break is necessary, and if it is, and there is room to add a break, then add a break


    def remove_small_segments(self, slots, min_slots):
        trimmed = []
        in_a_row = 1
        cur_row = [slots[0]]
        
        for i in range(1, len(slots)):
            if (slots[i] == (slots[i-1] +1)):
                cur_row.append(slots[i])
                if (i +1 == len(slots)):
                    trimmed.extend(cur_row)
                    return trimmed
            #when the cur_row streak ends, add the previous streak to trimmed if its long enough, and then reset cur_row 
            else:
                if (len(cur_row) >= min_slots):
                    trimmed.extend(cur_row)
                cur_row = [slots[i]]
        return trimmed




    #takes start and end as time strings like "08:30", and fills in the schedule wiht the activity for between those times
    def schedule_activity(self, day_int, activity, start, end, type = "strings"):
        if day_int > len(self.schedule):
            return
        
        if type == "strings":
            start_index = self.get_index(start)
            end_index = self.get_index(end)

            for i in range(start_index, end_index):
                self.schedule[day_int][i] = activity
        elif (type == "indexes"):
            for i in range(start, end + 1):
                self.schedule[day_int][i] = activity

    def schedule_activity_by_slots(self, day_int, activity, slots):
        for slot in slots:
            if self.schedule[day_int][slot] == None:
                self.schedule[day_int][slot] = activity
        
    
    def convert_length(self, hours):
        return int(float(hours) * 4)

    

    #takes time as "08:00" or "13:30"
    def get_index(self, time):
        hours = int(time.split(":")[0])
        minutes = int(time.split(":")[1])


        return ( int(hours*4) + int(minutes/15))
    
    # def get_end_minutes(self, index):
    #     hours = str((int(index/4)))
    #     minutes = str((int(index%4) *15))

    #     return(f"{hours:02}:{minutes:02}")
    
    # def get_start_time(self, index):
    #     hours = str((int(index/4)))
    #     minutes = str((int(index%4) *15) +14)

    #     return(f"{hours:02}:{minutes:02}")
    
    def convert_to_events(self):
        #for each day in the schedule
        date = dt.datetime.strptime(self.today_string, r'%Y-%m-%d')
        for i in range(len(self.schedule)):
            #convert each day to an eventlist
            cur_event = None
            date += timedelta(days = 1)
            todays_events = []
            #for each slot in the day
            for j in range(0,  len(self.schedule[0])):   
                temp_event = self.schedule[i][j]
                if temp_event == None:
                    continue
                #if the slot before didnt exist or was empty
                if cur_event == None:
                    cur_event = temp_event
                #if the current slot is not empty
                    if temp_event != None:
                        todays_events.append({'summary': cur_event["name"], 
                                "description": "****",
                                "start": {"dateTime": (date + timedelta(hours = (int((j)/4)), minutes = ((j%4)*15))).isoformat(), "timeZone": "America/New_York"}, 
                                "end":{"dateTime": (date + timedelta(hours = (int((j)/4)), minutes = ((j%4)*15)+14)).isoformat() , "timeZone": "America/New_York"}})
                        continue
                    

                #if the event as the same that came before it, 
                if (temp_event["name"].lower() == cur_event["name"].lower()):
                    todays_events[len(todays_events) -1 ]["end"]["dateTime"] = (date + timedelta(hours = (int((j)/4)), minutes = ((j%4)*15)+14)).isoformat()
                else:
                    new_event = {'summary': temp_event["name"], 
                              "description": "****",
                              "start": {"dateTime": (date + timedelta(hours = (int((j)/4)), minutes = ((j%4)*15) )).isoformat(), "timeZone": "America/New_York"}, 
                              "end":{"dateTime": (date + timedelta(hours = (int((j)/4)), minutes = ((j%4)*15)+14)).isoformat() , "timeZone": "America/New_York"}}
                    cur_event = temp_event
                    todays_events.append(new_event)

               

            self.events += todays_events

        
    



    #change from just the name to print the name of each daily
    def view(self):

        slots = []
        hours = 0
        minutes = 0
        for i in range(96):
            hours = int(i/4)  
            minutes = (i * 15)  %60
            slots.append(str(hours) + ":" + str(minutes))

        #for each timeslot in the day
        for i in range(len(slots)):
            # Extract the column from schedule
            #column_names = [self.schedule[row][i] for row in range(len(self.schedule))]
            at_this_index = []
            #for each day
            #get just the names
            for j in range(len(self.schedule)):
                name = "N/A"
                if (self.schedule[j][i] != None ):                    
                    name = self.schedule[j][i]["name"]

                at_this_index.append(name)
            formatted_schedule_line = '| '.join(at_this_index)

            print(f"{slots[i]} -> [{formatted_schedule_line}]")



if __name__ == '__main__':
    scheduler = Scheduler()