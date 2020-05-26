#commands

import time
import datetime

class classStuff:

    def getDateTime(DateOrTime):
        tim = time.localtime()
        day = tim.tm_mday
        month = tim.tm_mon
        year = tim.tm_year
        date = '{}/{}/{}'. format(month, day, year)
        hour = tim.tm_hour
        minute = tim.tm_min
        second = tim.tm_sec
        realTime = (hour, minute)
        if DateOrTime == 'Time':
            if realTime[0] > 12:
                hour = realTime[0]-12
                minute = realTime[1]
                if minute < 10:
                    minute = '0{}'. format(minute)
                ampm = 'PM'
            else:
                hour = realTime[0]
                minute = realTime[1]
                if minute < 10:
                    minute = '0{}'. format(minute)
                ampm = 'AM'
            return '{}:{} {}'. format(hour,minute,ampm)
        elif DateOrTime == 'Date':
            return date
        elif DateOrTime == 'DateTime':
            full = '{} - {}'. format(date,realTime)

    def findDayType():
        day = time.strftime('%A', time.localtime())
        if day == 'Monday':
            dayType = 'A'
        elif day == 'Tuesday':
            dayType = 'B'
        elif day == 'Wednesday':
            dayType = 'C'
        elif day == 'Thursday':
            dayType = 'D'
        elif day == 'Friday':
            dayType = 'E'
        else:
            dayType = 'No School'
        return dayType

    def findSchedule():
        dayType = classStuff.findDayType()
##        dayType = 'E'
        if dayType == 'A':
            schedule = [1,2,3,4,5,6,7,8]
        elif dayType == 'B':
            schedule = [1,2,3,4,5,6]
        elif dayType == 'C':
            schedule = [7,8,3,4,2,1]
        elif dayType == 'D':
            schedule = [8,7,5,6,2,1]
        elif dayType == 'E':
            schedule = [5,6,3,4,7,8]
        return schedule
    
    def makeSchedule():
        dayType = classStuff.findDayType()
##        dayType = 'E'
        if dayType == 'A':
            schedule = classStuff.findSchedule()
            output = 'A day, hours in order: \n {} \n {} \n {} \n {} \n {} \n {} \n {} \n {}'. format(schedule[0],schedule[1],schedule[2],schedule[3],schedule[4],schedule[5],schedule[6],schedule[7])
        elif dayType == 'B' or 'C' or 'D' or 'E':
            schedule = classStuff.findSchedule()
            output = '{} day, hours in order: \n {} \n {} \n {} \n {} \n {} \n {}'. format(dayType,schedule[0],schedule[1],schedule[2],schedule[3],schedule[4],schedule[5])
        return output
    
    def getTimes():
        day = time.localtime().tm_mday
        month = time.localtime().tm_mon
        year = time.localtime().tm_year
        hour = time.localtime().tm_hour
        minute = time.localtime().tm_min

        Class1A = datetime.datetime(year,month,day,8,0)
        Class2A = datetime.datetime(year,month,day,8,46)
        Class3A = datetime.datetime(year,month,day,9,45)
        Class4A = datetime.datetime(year,month,day,10,59)
        Class5A = datetime.datetime(year,month,day,11,45)
        Class6A = datetime.datetime(year,month,day,13,0)
        Class7A = datetime.datetime(year,month,day,13,46)
        Class8A = datetime.datetime(year,month,day,14,32)

        ADayTimes = [(1,Class1A),(2,Class2A),(3,Class3A),(4,Class4A),(5,Class5A),(6,Class6A),(7,Class7A),(8,Class8A)]

        Class1 = datetime.datetime(year,month,day,8,0)
        Class2 = datetime.datetime(year,month,day,9,0)
        Class3 = datetime.datetime(year,month,day,10,15)
        Class4 = datetime.datetime(year,month,day,11,50)
        Class5 = datetime.datetime(year,month,day,13,20)
        Class6 = datetime.datetime(year,month,day,14,20)

        NormalTimes = [(1,Class1),(2,Class2),(3,Class3),(4,Class4),(5,Class5),(6,Class6)]
        return ADayTimes,NormalTimes
    
    
    def timeCheck(buffer, ADayTimes, NormalTimes):
        global time
        schedule = classStuff.findSchedule()
        dayType = classStuff.findDayType()
        day = time.localtime().tm_mday
        month = time.localtime().tm_mon
        year = time.localtime().tm_year
        hour = time.localtime().tm_hour
        minute = time.localtime().tm_min
        currentTime = datetime.datetime(year,month,day,hour,minute)
        if dayType == 'A':
            for times in ADayTimes:
                timeLeft = times[1] - currentTime
                #timeLeft = 5
                #print(timeLeft)
                if abs(timeLeft) == timeLeft and timeLeft.seconds/60 <= buffer:
                    return True, classStuff.matchPeriod(times[0]), times[1]
        else:
            for times in NormalTimes:
                timeLeft = times[1] - currentTime
                #timeLeft = 5
                #print(timeLeft)
                if abs(timeLeft) == timeLeft and timeLeft.seconds/60 <= buffer:
                    return True, classStuff.matchPeriod(times[0]), times[1]
        return False, 'No Period within {} minutes'. format(buffer*60)

    def convertMins(time):
        hours = time.hour
        minutes = time.minute
        newTime = hours*60+minutes

    def timeTillNextClass(ADayTimes, NormalTimes):
        now = datetime.datetime.now()
        dayType = classStuff.findDayType()

        if dayType == 'A':
            timeList = ADayTimes
        else:
            timeList = NormalTimes

        closestTimeTill = 100000000000
        for times in timeList:
            time = times[1]
            period = times[0]
            if time > now:
                timeTill = time - now
                timeTill = timeTill.seconds
                if timeTill<closestTimeTill:
                    closestTime=time
                    closestTimeTill = timeTill
                    closestPeriod = period
        return int(closestTimeTill/60), classStuff.matchPeriod(closestPeriod), closestTime


    def matchPeriod(item):
        listPlace = item
        schedule = classStuff.findSchedule()
        period = schedule[listPlace-1]
        if period > 3:
            return '{}th hour'. format(period)
        elif period == 1:
            return '1st hour'
        elif period == 2:
            return '2nd hour'
        elif period == 3:
            return '3rd hour'

                
                
#print(classStuff.timeTillNextClass(classStuff.ADayTimes,classStuff.NormalTimes))

        
    

        









    
    


    
