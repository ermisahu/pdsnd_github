import time
import pandas as pd
import numpy as np

# loading related files
CITY_DATA = {
    'chicago':'chicago.csv',
    'new york':'new_york_city.csv',
    'washington':'washington.csv'
}

def get_city():
    '''
    The function asks the user for a city he/she wants to analyze.
    '''
    print('Let\'s explore some US bikeshare data!')
    #get user input for city (chicago, new york city, washington).
    city = input('Would you like to see data for Chicago, New York, or Washington?')
    city = city.lower()

    while True:     # I choose to use while loop to get the correct or expected city by user
            if city == 'chicago':
                return 'chicago'
            if city == 'new york':
                return 'new york'
            elif city == 'washington':
                return 'washington'
            else:
                print("\nSorry I can't get your input. Please type the below written names of cities\n")
                city = input('Chicago, New York or Washington? ')
                city = city.lower()
    return city

def get_time():
    #get user input for filtering time period (month, day or none)
    period = input('\nWould you like to filter the data by "month" or "day" of the week? Type "none" for no period filter.\n')
    period = period.lower()

    while True:
        if period == "month":
            return 'month'
        elif period == "day":
            return 'day_name'
        elif period == "none":
            return "none"
        period = input("\n Please choose a period filter option between 'month', 'day' of the week, or 'none' \n").lower()

def get_month(m):
  # get user input for month
    if m == 'month':
        month = input('\nPlease choose and type full name of the month! January, February, March, April, May, or June? \n')
        while month.strip().lower() not in ['january', 'february', 'march', 'april', 'may', 'june']:
            month = input('\nPlease do not forget to write full name. Please choose between January, February, March, April, May, or June? \n')
        return month.strip().lower()
    else:
        return 'none'

def get_day(d):
  # get user for a day
    if d == 'day_name':
        day = input('\nWhich day? Please type a day Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday \n')
        while day.lower().strip() not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            day = input('\nPlease type full name of a day as a choice from Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday. \n')
        return day.lower().strip()
    else:
        return 'none'

def load_data(city):
    # Loads data for the specified city and divide the required time from Start Time
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_name'] = df['Start Time'].dt.weekday_name
    return df

def get_time_filter(df, time, month, week_day):
    '''
    Filters the data according to the criteria specified by the user.
    Local Variables:
    df         - city dataframe
    time       - indicates the specified time (either "month" or "day_name")
    month, week_day      - brings the month or day  used to filter the data

    Result/Return:
    df - dataframe to be used for final calculation
    '''
    #Filter by month or day of week
    if time == 'month':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    elif time == 'day_name':
        days = ['Monday', 'Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        for d in days:
            if week_day.capitalize() in d:
                day_name = d
        df = df[df['day_name'] == day_name]
    return df

def pop_month(df):
    # finds the most popular month from start time for bike travelling
    print("\n In case you might be interested, please find the additional statistical results: ")
    print('\n -The most popular month for bike trips:')
    m = df.month.mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    popular_month = months[m - 1].capitalize()
    return popular_month

def pop_day(df):
    # finds the most popular day of the week for start time
    print('\n -The most popular day of the week for bike trips:')
    return df['day_name'].value_counts().reset_index()['index'][0]

def pop_hour(df):
    # finds the most popular hour of day for start time
    print('\n -The most popular hour of the day for bike trips:')
    df['hour'] = df['Start Time'].dt.hour
    return df.hour.mode()[0]

def trip_duration(df):
    # finds the total trip duration and average trip duration
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Travel Time'] = df['End Time'] - df['Start Time']
    total_trip_time = np.sum(df['Travel Time'])
    total_days = str(total_trip_time).split()[0]
    print (" \n -The total traveling time for 6 months period: " + total_days + " days \n")
    avg_trip_time = np.mean(df['Travel Time'])
    avg_days = str(avg_trip_time).split()[0]
    print(" -The average travel time for 6 months period: " + avg_days + " days \n")
    return total_trip_time, avg_trip_time

def pop_stations(df):
    # finds the most popular start station and most popular end station
    print("\n -The most popular start station:\n")
    start_station = df['Start Station'].value_counts().reset_index()['index'][0]
    print (start_station)
    print("\n -The most popular end station:\n")
    end_station = df['End Station'].value_counts().reset_index()['index'][0]
    print(end_station)
    return start_station, end_station

def pop_trip(df):
    # finds the most popular trip
    popular_trip = df[['Start Station', 'End Station']].groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('\n -The most popular trip:')
    return popular_trip

def user_stats(df):
     # finds and counts users based on user types
    print('\n -The types of users: subscribers, customers, others\n')
    return df['User Type'].value_counts()

def user_gender(df):
    # checks the user gender information
    try:
        print('\n -The gender among users:\n')
        return df['Gender'].value_counts()
    except:
        print('Sorry, there is no user gender data for this city')

def birth_years(df):
    # finds the earliest, latest, and most popular birth year
    try:
        earliest = np.min(df['Birth Year'])
        print ("\n -The earliest year of birth: " + str(earliest) + "\n")
        latest = np.max(df['Birth Year'])
        print (" -The latest year of birth: " + str(latest) + "\n")
        most_popular= df['Birth Year'].mode()[0]
        print (" -The most popular  year of birth: " + str(most_popular) + "\n")
        return earliest, latest, most_popular
    except:
        print('Sorry, there is no birth date data for this period.')

def process(f, df):
    #Calculates the time it takes to commpute a statistic
    start_time = time.time()
    statToCompute = f(df)
    print(statToCompute)
    print("Computing this stat took %s seconds." % (time.time() - start_time))

def disp_raw_data(df):
    #excludes irrelevant columns from solution table
    df = df.drop(['month'], axis = 1)
    row_index = 0
    see_data = input("\nDo you want to see 5 rows of the data from the statistic? Please write 'yes' or 'no' \n").lower()

    while True:
        if see_data == 'no':
            return
        elif see_data == 'yes':
            print(df[row_index: row_index + 5])
            row_index = row_index + 5
        see_data = input("\n Do you want to see additional 5 more rows of the data? Please write 'yes' or 'no' \n").lower()

def main():
    # calling all the functions
    city = get_city()
    period = get_time()
    month = get_month(period)
    day = get_day(period)
    df = load_data(city)
    df = get_time_filter(df, period, month, day)
    disp_raw_data(df)
    # statistic part
    stats_funcs_list = [pop_month, pop_day, pop_hour, trip_duration,
    pop_stations, pop_trip, user_stats, user_gender,birth_years]

    for x in stats_funcs_list:	# shows processing time for each function block
        process(x, df)

    # Restarting option
    restart = input("\n Would you like to try another analysis? Type \'yes\' or \'no\'.\n")

    if restart.upper() == 'YES' or restart.upper() == "Y" or restart.upper() == 'yes':
        print("OK Great! Please begin again :) \n  ")
        main()
    else:
        print("Thank you for your interest! This is the end of statistic.")

if __name__ == '__main__':
    main()