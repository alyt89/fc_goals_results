# FC Goals

FC Goals is a fictional football (soccer) team with its results stored in a Google Sheets worksheet. This is a Python terminal app to analyse the results and add new match results also.

[Click here for the link to my live project](https://fc-goals.herokuapp.com/)

![Responsive screenshot](/images/fcgoals_responsive.png)

## How to Use

Users are presented with various filters through the app to guide them to the option they would like to use.

The primary filter allows the user to either enter new match data or check past match data.

Depending on their selection they will be taken to the next relevant option with further sub-filters available on the 'past match data' filter.

## Features

![Responsive screenshot](/images/fcgoals_intro.png)

- Enter new details for FC Goals which are updated in real time on the Google Sheets linked.

![Responsive screenshot](/images/fcgoals_match_score.png)

- Validates new data entered is of sufficient length.

- Offers various filters to check past match results.

![Responsive screenshot](/images/fcgoals_pastmatch_filter.png)

- Set up to work if further seasons are added later and if further results are added to the sheet.

- Prints results of past match data to the user depending on their input.

![Responsive screenshot](/images/fcgoals_result_by_opp.png)

## Future Features

The app could be further enhanced in the future by implementing:

- Score predictor 

    - Analyse past results against an opposition and get average goals scored/conceded.
    - Analyse recent form and average goals scored/conceded again.
    - Combine a mean of these averages and round suitably to create a score prediction. 

- Top Scorer 

    - Add 'Goalscorer(s)' column to the sheet and use this data to analyse the top scorer for a particular season.

## Language and model used

The app uses only Python language and is primarily a chain of user inputs that lead to relevant functions depending on the user's selection.

Gspread API is used for the linking of the app and to the Google Sheets data for FC Goals as well as Gspread methods. The Google Sheets data can be found on the following link:

[Click here](https://docs.google.com/spreadsheets/d/1oxZT51qHpiZh39yspIBTBg7NI4O8NV3WUB0Umf_VutE/edit?usp=sharing)


The Credentials from google.oauth2.service.account is also required in the run.py file to ensure relevant credentials can allow the pull and push of data between the app and the google sheets

Within the past match data filter there are gspread methods used to access and filter the data appropriately to return the correct results.

For loops and if statements are used to check against the user's selections and return the correct data to printed to the terminal.

## Testing

- Testing was done throughout building the app on the built in terminal on gitpod through various print statements.

- Official validation done through PEP8 which showed code was correct.

- App has been tested in the builtin terminal on gitpod and also on Heroku.

## Debugging

- The validate_scores function was looping back to the wrong part of code initially, once code was reordered this was resolved.

- Upon initial Heroku deployment tested the app and biggest_win function was not working due to partial renaming of a variable. Renamed variable throughout and tested this was now working.

- Various errors in PEP8 validation initially regarding whitespace and lines after methods. Cleaned up and all passed through.


## Deployment

- The project was deployed via Heroku using the following steps:

    - Open Heroku account.
    - Select 'Create new app'.
    - Under 'Settings' section update relevant PORT and CREDS settings. 
    - Still in 'Settings' section add Python and NodeJS buildpacks.
    - Under 'Deploy' section choose to connect with 'GitHub' and ensure logged in correctly.
    - Type in workspace name and select suitable project to connect
    - Select 'Manual Deploy' and wait for app to build.
    - Click 'view' to open app in new tab.

## Credits

- W3 Schools for refreshers on for loops and zip

- Gspread documentation for max() and findall() method usage.

