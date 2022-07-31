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


def filter_user_options():
    """
    Initial function to give user the filter to choose between
    entering a new match score or checking past match data
    """

    while True:
        print("----------------------------")
        print("Welcome to FC Goals Database")
        print("----------------------------")
        print("Choose from one of the following options:")
        print("1: Enter new match score")
        print("2: Check past match data")
        filter_choice = input("Enter your selection here:\n")

        try:
            choice = int(filter_choice)
            choice += 1
        except ValueError:
            print("Please enter a valid number")
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
    print("----------------------------")
    print("Ready to enter new match score")
    print("Enter match data here")
    print("Please enter in following format:")
    print("Date, Opposition, Venue, Goals For, Goals Against, MOTM")
    print("Example: 01-Jan, Man U, H, 3, 0, Smith\n")
    print("To go to main menu enter 'main'\n")
    score_data_string = input("Enter here:\n")
    score_data = score_data_string.split(",")

    if score_data[0] == "main":
        filter_user_options()

    if validate_scores_data(score_data):
        print("Data valid")
        update_score(score_data)

    return score_data


def validate_scores_data(data):
    """
    Function to validate the data entered by the user when
    entering a new match score
    """

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

    year = input("Enter your selection:\n")

    try:
        season = int(year)
        season += 1
    except ValueError:
        print("Please enter a valid season, either 2021 or 2022")
        filter_user_options()

    season = int(year)        
    if season < 2021:
        print("Please select a valid season")
        filter_user_options()
    elif season > 2022:
        print("Please select a valid season")
        filter_user_options()

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
    print("Score successfully updated")
    print("----------------------------")
    filter_user_options()


def past_match_filter(season):
    """
    Function to filter the users selection for past match data
    and determine which following function to run.
    """

    print(f"season option selected is {season}")
    print("Select from one of the following options")
    print("1: Check result by opposition")
    print("2: Biggest Win")
    print("3: Heaviest Defeat")

    past_match_filter_selection = input("Enter here:\n")

    if past_match_filter_selection == "2":
        biggest_win(season)

    if past_match_filter_selection == "3":
        heaviest_defeat(season)

    print("----------------------------")
    print("Select from: Fairfield, Buxton,"
          " Altrincham, Hawkes, Falcons, Lakers")
    print("Enter opposition name below:")
    opposition = input("Opposition name:\n")

    if past_match_filter_selection == "1":
        score_by_opposition(season, opposition)


def check_opposition(season, opposition):
    worksheet = SHEET.worksheet(season)
    cell = worksheet.find(opposition.capitalize())

    if cell is None:
        print("Opposition name not found")
        past_match_filter(season)


def score_by_opposition(season, opposition):
    """
    Function collects the opposition name specified by
    the user and finds all matches from the relevant
    worksheet.
    """

    check_opposition(season, opposition)
    team_name = opposition.capitalize()
    print("----------------------------")
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

    filter_user_options()


def heaviest_defeat(season):
    """
    Function to check the heaviest defeat in a specified
    season. Generates list of goals scored and goals
    conceded and finds the biggest difference between the two.
    """
    year = SHEET.worksheet(season)
    goals_scored = year.col_values(4)
    goals_conceded = year.col_values(5)

    goals_scored.pop(0)
    goals_conceded.pop(0)

    goal_difference = []

    goals_combined = zip(goals_conceded, goals_scored)
    for a, b in goals_combined:
        goal_difference.append(int(a)-int(b))

    max_goal_difference = max(goal_difference)
    max_goal_difference_index = goal_difference.index(max_goal_difference)
    max_goal_difference_row = (max_goal_difference_index + 2)

    print(f"Heaviest defeat in {season} against"
          f" {year.cell(max_goal_difference_row, 2).value}"
          )

    print(f"Score {year.cell(max_goal_difference_row, 4).value}"
          f" - {year.cell(max_goal_difference_row, 5).value}")

    filter_user_options()


def biggest_win(season):
    """
    Function to check the biggest win in a specified
    season. Generates list of goals scored and goals
    conceded and finds the biggest difference between the two.
    """
    year = SHEET.worksheet(season)
    goals_scored = year.col_values(4)
    goals_conceded = year.col_values(5)

    goals_scored.pop(0)
    goals_conceded.pop(0)

    goal_difference = []

    goals_combined = zip(goals_scored, goals_conceded)
    for a, b in goals_combined:
        goal_difference.append(int(a)-int(b))

    max_goal_difference = max(goal_difference)
    max_goal_difference_index = goal_difference.index(max_goal_difference)
    max_goal_difference_row = (max_goal_difference_index + 2)

    print(f"Biggest win in {season} against"
          f" {year.cell(max_goal_difference_row, 2).value}"
          )

    print(f"Score {year.cell(max_goal_difference_row, 4).value}"
          f" - {year.cell(max_goal_difference_row, 5).value}")

    filter_user_options()


filter_user_options()
