import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
cities=['chicago','new york city','washington']
months=['january', 'february', 'march', 'aprill', 'may', 'june','all']
days=['sunday','monday','tuesday','wednesday','thursday','friday','saturday','all']
choice = ['yes','no']



def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        
        city = str(input("\nwhich city would you like to see data for chicago, new york city or washington?\n")).lower()
        if city not in cities:
            print('invalid input, enter a valid city name (chicago, new york city, washington)')
        else:
            break
    
    # get user input for month (all, january, february, ... , june)
    while True:
        month = str(input("\nwhich month you would like to filter the data with?[January, February, March, Aprill, May or June]?or type all for no filter\n ")).lower()
        if month not in months:
            print('invalid input, enter a valid month name or all for no filter[january, february, march, april, may or june]')
        else:
            break
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("\nwhich day you would like to filter the data with?or type all for no filter\n").lower()
        if day not in days:
            print('invalid input, enter a valid day or all for no filter [sunday, monday, tuesday, wednesday, thursday, friday, saturday]')
        else:
            break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month']==month]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    #cleaning data 
    #first removing (Dependent) from user type as the data set showed that User Type (Subscriber or Customer) only
    df.drop(df.index[(df["User Type"] == "Dependent")],axis=0,inplace=True)
    #second removing the earliest year of birth as it is unrealistic, to let the data more relvant[the earliest year of birthe was 1885,1889,1890. so it is unrealstic that someone who has more than 110 years to ride a bike]
    if "Birth Year" in df.columns:
        df.drop(df.index[(df["Birth Year"] < 1920)],axis=0,inplace=True)
    

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    popular_month = df['month'].mode()[0]
    print('Most Frequent month:', popular_month)

    # display the most common day of week

    popular_day = df['day_of_week'].mode()[0]
    print('Most Frequent day of the week:', popular_day)

    # display the most common start hour

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most common hour (from 0 to 23)
    popular_hour = df['hour'].mode()[0]
    
    print('Most Frequent Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_start_station = df['Start Station'] .mode()[0]

    print('most commonly start station:',most_start_station)

    # display most commonly used end station
    most_end_station = df['End Station'] .mode()[0]

    print('most commonly end station:',most_end_station)    


    # display most frequent combination of start station and end station trip
    df["start_end_stations"] = 'From: '+df["Start Station"]+' To: '+ df["End Station"]
    start_end = df["start_end_stations"].mode()[0]
    print('The most frequent combination of start station and end station trip:',start_end)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['Trip Duration']= df['Trip Duration'].astype(int)
    total_travel_time = (df['Trip Duration'].sum())/(60*60)
    print('total travel time:',"%.2f" % round(total_travel_time, 2),'Hours')


    # display mean travel time
    mean_travel_time = (df['Trip Duration'].mean())/60
    print('mean travel time:',"%.2f" % round(mean_travel_time, 2),'minutes')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'] .value_counts()
    print(user_types)


    # Display counts of gender
    if('Gender' not in df):
        print('No Gender data avaialble for Washington')
    else:
        
        Gender_types = df['Gender'] .value_counts()
        print(Gender_types)

    # Display earliest, most recent, and most common year of birth
    if ('Birth Year' not in df):
        print('No Birth year data available for Washington')
    else:    
        birth = df['Birth Year'] .mode()[0]
        print('the most common year of birth:',birth)
        birth_max = df['Birth Year'] .max()
        print('the most recent year of birth:',birth_max)    
        birth_min = df['Birth Year'] .min()     
        print('the earliest year of birth:',birth_min)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# to display raw data
def display_raw_data(df):
    start=0
    while True:
        view_data =(input('\nDo you want to view raw data? type(yes or no).\n')).lower()
        if view_data not in choice:
            print('invalid input, please enter yes to view  data or no to quit')
        else:
            break                
    while view_data == 'yes':
        n=start+5
        if n > df.shape[0]:
            print(' there is no more raw data to display.')
            n -= 5
            break

        print(df[start:n])
        while True:
            view_data=input('do you want to view more data? type(yes or no).\n').lower()
            if view_data not in choice:
                print('invalid input, please enter yes to view  data or no to quit')
            else:
                break
            
        start=n


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)
        while True:
            restart = (input('\nWould you like to restart? Enter yes or no.\n')).lower()
            if restart not in choice:
                print('invalid input, please enter yes to restart or no to quit')
            else:
                break    
        if restart.lower() != 'yes':
            break

            
                  
            
if __name__ == "__main__":
	main()
