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


def filter_user_options():

    while True:
        print("Choose from one of the following options:")
        print("1: Enter new match score")
        print("2: Check past match data")

        filter_choice = input("Enter your selection here:\n")

        

        try:
            choice = int(filter_choice)
            choice += 1
        except ValueError:
            print("Please enter valid number")
            filter_user_options()

        try:
            choice = int(filter_choice)
            if choice < 1:
                print("Please select a valid number")
                filter_user_options()
            elif choice > 2:
                print("Please select a valid number")
                filter_user_options()
        except:
            print("Please select a valid option")    

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
    print("Enter match data here")
    print("Please enter in following format:")
    print("Date, Opposition, Venue, Goals For, Goals Against, MOTM")
    print("Example: 01-Jan, Man U, H, 3, 0, Smith\n")
    print("To go to main menu enter 'main'\n")
    score_data_string = input("Enter here:\n")
    score_data = score_data_string.split(",")
    print(score_data)

    if score_data[0] == "main":
        filter_user_options()

    if validate_scores_data(score_data):
        print("data valid")
        update_score(score_data)

    return score_data        


def validate_scores_data(data):

    try:
        if len(data) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(data)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
    
    return True


def check_past_match():
    """
    Function to analyse the existing data on worksheet and provide
    data dependent on options provided.
    """
    print("Ready to check match score\n")
    print("Enter season you wish to check")
    print("2021 / 2022 / all")

    past_match_year = input("Enter your selection:\n")
    
    past_match_filter(past_match_year)


def update_score(score):
    """
    Uses the score data input by user to update spreadsheet.
    """
    print("Select which season you want to update (2021 or 2022)")
    year = input("Enter Season:\n")
    print(f"Year selected is {year}")
    
    season_to_update = SHEET.worksheet(year)
    season_to_update.append_row(score)
    print("score successfully updated")
    filter_user_options()


def past_match_filter(season):
    print(f"season option selected is {season}")
    print("Select from one of the following options")
    print("1: Check result by opposition")
    
    past_match_filter_selection = input("Enter here:\n")
    print("Enter opposition name below:")
    opposition = input("Opposition name:\n")
    
    if past_match_filter_selection == "1":
        score_by_opposition(season, opposition)


def score_by_opposition(season, opposition):
    print(f"Checking scores against {opposition} for season {season}")
    season_to_check = SHEET.worksheet(season)
    cell_results = season_to_check.findall(opposition)
    matching_cell_rows = []
    for cell in cell_results:
        matching_cell_rows.append(cell.row)
    print(matching_cell_rows)

    for row in matching_cell_rows:
        print(season_to_check.row_values(row))

def main():
    """
    Run all main functions
    """
    filter_user_options()

main()