import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('fc_goals_results')

TWENTY_ONE = SHEET.worksheet('2021')
TWENTY_TWO = SHEET.worksheet('2022')

data = TWENTY_ONE.get_all_values()

def filter_user_options():
    print("Choose from one of the following options:")
    print("1: Enter new match score")
    print("2: Check past match data")

    filter_choice = input("Enter your selection here:\n")

    filter_choice_value = int(filter_choice)

    if filter_choice_value == 1:
        enter_match_score()
    elif filter_choice_value == 2:
        check_past_match()


def enter_match_score():
    """
    Function to filter user option and enter a new match score
    to be updated on the worksheet.
    """
    print("Ready to enter new match score")

    while True:
        print("Enter match data here")
        print("Please enter in following format:")
        print("Date (DD-MMM), Opposition name, Venue (H or A), Goals For, Goals Against, MOTM")
        print("Example: 01-Jan, Man U, H, 3, 0, Smith")
        score_data_string = input("Enter here:\n")
        score_data = score_data_string.split(",")
        print(score_data)

        if validate_scores_data(score_data) == 6:
            break


def validate_scores_data(data):
    date = data[0]
    print(date)
    return len(data)
  

def check_past_match():
    """
    Function to analyse the existing data on worksheet and provide
    data dependent on options provided.
    """
    print("Ready to check match score")

def main():
    """
    Run all main functions
    """
    filter_user_options()

main()