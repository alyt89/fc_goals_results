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

        choice = int(filter_choice)
        if choice < 1:
            print("Please select a valid number")
            filter_user_options()
        elif choice > 2:
            print("Please select a valid number")
            filter_user_options()

        if choice == 1:
            enter_match_score()
        elif choice == 2:
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
    print("2021 / 2022 ")

    season = input("Enter your selection:\n")
    
    past_match_filter(season)


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
    print("2: Biggest Win")
    print("3: Heaviest Defeat")
    
    past_match_filter_selection = input("Enter here:\n")
    
    if past_match_filter_selection == "2":
        biggest_win(season)

    print("Select from: Fairfield, Buxton, Altrincham, Hawkes, Falcons, Lakers")
    print("Enter opposition name below:")
    opposition = input("Opposition name:\n")

    if past_match_filter_selection == "1":
        score_by_opposition(season, opposition)



def score_by_opposition(season, opposition):

    team_name = opposition.capitalize()
    print(f"Checking scores against {team_name} for season {season}\n")
    season_to_check = SHEET.worksheet(season)
    cell_results = season_to_check.findall(team_name)
    matching_cell_rows = []
    for cell in cell_results:
        matching_cell_rows.append(cell.row)

    game_data = []

    for row in matching_cell_rows:
        game_data.append(season_to_check.row_values(row))

    match_one = game_data[0]
    match_two = game_data[1]

    print("Match 1:\n")
    print(f"Date: {match_one[0]}")
    print(f"Opposition: {match_one[1]}")
    print(f"Venue: {match_one[2]}")
    print(f"Goals For: {match_one[3]}")
    print(f"Goals Against: {match_one[4]}")
    print(f"MOTM: {match_one[5]}\n")
    print("Match 2:\n")
    print(f"Date: {match_two[0]}")
    print(f"Opposition: {match_two[1]}")
    print(f"Venue: {match_two[2]}")
    print(f"Goals For: {match_two[3]}")
    print(f"Goals Against: {match_two[4]}")
    print(f"MOTM: {match_two[5]}\n")


def biggest_win(season):
    """
    Function to check the biggest win in a specified
    season. Generates list of goals scored and goals
    conceded and finds the biggest difference between the two.
    """
    season_to_check = SHEET.worksheet(season)
    goals_scored = season_to_check.col_values(4)
    goals_conceded = season_to_check.col_values(5)

    goals_scored.pop(0)
    goals_conceded.pop(0)

    print(goals_scored)
    print(goals_conceded)

    goal_difference = []

    goals_combined = zip(goals_scored, goals_conceded)
    for a, b in goals_combined:
        goal_difference.append(int(a)-int(b))
    
    print(f"Goal difference for each match is: {goal_difference}")

    filter_user_options()

def main():
    """
    Run all main functions
    """
    filter_user_options()

main()