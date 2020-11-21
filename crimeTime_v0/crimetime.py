"""
Implementation requirements:
1) -> specifying return types in function declaration
2) Crime object
    attrs:
        crime_id as read from crimes.tsv
        category as read from crimes.tsv
        day_of_week as read from times.tsv
        month modified from times.tsv to be a full word
        hour modified from times.tsv to be in AM/PM format
    __init__(self,crime_id, category):
        other attrs initialize to None
    __eq__(self,other):
        True if id of 2 crime objects is the same, false otherwise
    __repr__(self):
        tab between attributes with a newline character at the end
3) create_crimes(lines) -> list
4) sort_crimes(crimes) -> list
5) set_crimetime(crime, day_of_week, month, hour)
6) update_crimes(crimes, lines)
7) find_crime(crimes, crime_id) -> Crime

Output
1) robberies.tsv
2) print the following stats:
    NUMBER OF PROCESSED ROBERIES: _
    DAY WITH MOST ROBBERIES: _
    MONTH WITH MOST ROBBERIES: _
    HOUR WITH MOST ROBBERIES: _
"""
# 0) Imports
from sys import argv
from copy import copy
from calendar import month_name

# 1) Initialize variables
crimeFile = argv[1]
timeFile = argv[2]

# 3) Implementation Requirements
class Crime:
    def __init__(self, crime_id, category):
        self.crime_id = int(crime_id)
        self.category = category
        self.day_of_week = None
        self.month = None
        self.hour = None
    def __eq__(self,other):
        """
        the try/ except block here was added to mitigate Attribute error that was 
        raised when comparing Crime's with None
        """
        try: 
            return self.crime_id == other.crime_id
        except AttributeError as e:
            if "NoneType" in str(e):
                return False
            else:
                raise AttributeError(e)
    def __repr__(self):
        return f"{self.crime_id}\t{self.category}\t{self.day_of_week}\t{self.month}\t{self.hour}\n"

def create_crimes(lines)->list:
    """
    input: 
        lines <- list of strings, each being a line from crimes.tsv
    output: 
        list of Crime objects with unique IDs
    improvements:
        a more robust function might include another parameter "crimeType" 
        which would allow for analysis of other crimes.
    """
    crimes = []
    IDS = set()
    for line in lines[1:]:
        crime_id, category, _  = line.split("\t")
        if crime_id not in IDS and category == "ROBBERY":
            crimes.append(Crime(crime_id, category))
            IDS.add(crime_id)
    return crimes
    
def sort_crimes(crimes)->list:
    """
    input: 
        crimes <- list of Crime objects
    requirements: 
        Use copy function from copy module to shallow copy input list into a new list.
        Use selection sort or insertion sort to sort the new list by ID
    output: 
        return the new list of crimes sorted by ID
    improvements:
        selection sort should pretty much never be used in practice, insertion sort
        can be effective for very small datasets.  Use a better sorting algorithm 
        "quick sort" or "timsort (used by Python's default sort method)"
    """
    # SELECTION SORT
    # 1) set location = 0, 
    # 2) search for min in sublist location:length(list)
    # 3) swap min & element at location
    # 4) increment location
    # 5) repeat until list sorted
    sorted_crimes = copy(crimes)
    i = 0
    while i < len(sorted_crimes) - 1:
        j, _min = i , i 
        while j < len(sorted_crimes):
            _min = _min if sorted_crimes[j].crime_id >= sorted_crimes[_min].crime_id else j 
            j += 1
        sorted_crimes[i], sorted_crimes[_min] = sorted_crimes[_min], sorted_crimes[i]
        i += 1
    return sorted_crimes

def set_crimetime(crime, day_of_week, month, hour):
    """
    input: 
        crime:
        day_of_week:
        month:
        hour:
    functionality:
        updates crime object.
        crime.month
            uses the month_name object from the calendar module, to avoid ugly/ time 
            consuming hard-coding month names.
            if this is not allowed:
            hard code the month names into a list, the intger corresponding to the month name - 1
            will be the index of the correct month name.
        crime.hour


    output:
        None
    """
    crime.day_of_week = day_of_week
    crime.month = month_name[int(month)]
    crime.hour = convert_time(hour)

def update_crimes(crimes, lines):
    """
        input:
            crimes <- list of sorted crime objects
            lines <-  lines from "times.tsv"
        requirements:
            calls set_crimetime to update crimes where
            crime_id matches times_id.
            calls find_crime to get find the appropriate crime
            to update.
        output:
            None
    """
    for line in lines[1:]:
        crime_id, day_of_week, date, time  = line.split("\t")
        crime = find_crime(crimes, int(crime_id))
        if crime != None:
            month = date.split("/")[0].strip()
            hour = time.split(":")[0].strip()
            set_crimetime(crime, day_of_week.strip(), month, hour)
    
def find_crime(crimes, crime_id)->Crime:
    """
    input:
        crimes <- sorted list of crimes
        crime_id <- integer crime_id
    requirements:
        use binary search to find the crime_id
    output:
        crime object with crime_id matching the input crime_id
    improvements:
        -why return the crime object, waste of memory.  Return a pointer 
        to the crime object instead.
    """
    # Binary search
    i, j = 0, len(crimes)
    while i < j:
        m = (i + j)//2
        if crimes[m].crime_id > crime_id:
            j = m
        elif crimes[m].crime_id < crime_id:
            i = m + 1
        else:
            return crimes[m]

# 4) Additional functions
def convert_time(time_24)->str:
    """
    input:
        an hour in 24 time format
    output:
        a string, the twelve hour format of the input time with the correct [AM,PM] suffix
    """
    time_24 = int(time_24)
    if -1 < time_24 < 25:
        suffix = "PM" if time_24 > 11 else "AM" 
        time_12 = time_24 % 12 if time_24 % 12 != 0 else 12
        return f"{time_12}{suffix}"
    else:
        return None

def gen_output_file(crimes, fname = "robberies.tsv"):
    """
    input:
        fname:
        crimes:
    output:
        None
    """
    with open(fname,"w+") as out:
        out.writelines(["ID\tCategory\tDayOfWeek\tMonth\tHour\n"]+[c.__repr__() for c in crimes])

def align_right(str_list, padding = " "):
    """
    input:
        str_list: list of strings
        padding (optional): pad the strings in str_list with this character
    output:
        None
    """
    r_length = max([len(r) for r in str_list])
    for i in range(len(str_list)):
        str_list[i] = padding * (r_length - len(str_list[i])) + str_list[i]

def maxRobberiesByAttribute(crimes,attribute)->str:
    """
    input:
        crimes: list of crime objects
        attribute: "day_of_week", "hour", "month"
    output:
        string corresponding to the attribute key with the most robberies
    """
    cache = {}
    for crime in crimes:
        cache[getattr(crime,attribute)] = cache[getattr(crime,attribute)] + 1 if getattr(crime,attribute) in cache else 1
    return max(cache, key=cache.get)

def get_crime_stats(crimes):
    question = [
        "NUMBER OF PROCESSED ROBBERIES: ",
        "DAY WITH MOST ROBBERIES: ",
        "MONTH WITH MOST ROBBERIES: ",
        "HOUR WITH MOST ROBBERIES: "
    ]
    answer = [
        len(crimes),
        maxRobberiesByAttribute(crimes, 'day_of_week'),
        maxRobberiesByAttribute(crimes, 'month'),
        maxRobberiesByAttribute(crimes, 'hour')
    ]
    align_right(question)
    for i in range(len(question)):
        print(f"{question[i]}{answer[i]}")

if __name__ == "__main__":
    crimeLines, timeLines = [], []
    with open(crimeFile,"r+") as crimeFileOpen:
        crimeLines = crimeFileOpen.readlines()
    with open(timeFile,"r+") as timeFileOpen:
        timeLines = timeFileOpen.readlines()
    robberies = create_crimes(crimeLines)
    sorted_robberies = sort_crimes(robberies)
    update_crimes(sorted_robberies, timeLines)
    get_crime_stats(sorted_robberies)
    gen_output_file(sorted_robberies)