# Mentee/Mentor Generator

## Objective:
* The objective of this notebook is to share a random user generator for both the mentee and mentor.
* This data can then be used in machine learning models to imitate an actual pairing process.
* I think that it's worth exploring a K-Means clustering model for automating the matching process.
    * It was discussed that the process shouldn't be fully autonimus, but each pair should include a top five matches.
        * This information will be futher processed by a member at Underdog-devs.
        * The process should be flexable enough though to support major growth too.

## Imports:
* import datetime
* import random
* from random import randint, choice, choices
* import pandas as pd

## Helper Functions:
* The helper functions below will be used in generating data for the mentee/mentor classes.
    * The **random_date** function will be for aiding in generating random timeframes of application submissions.
    * The **percent_true** function will be used in generating boolian outputs from the hypethetical user, or helping other functions.
    * The **random_first_name** function will be purposed for generating either a female, or male name for the hypethetical user.
    * The **random_mentee_language** function will help generate possibly known languages from a mentee.
    * The **random_profile_id** function will be used for generating random profile id's using a hash of the randomly generated email.

## Mentee Class:
* The "__init__"s - below will be the methods in generating data for the mentee class.
    * mentee_intake_id = When the mentee submits an application this identifier will be assigned for tracking said application.
    * first_name = This represents the first name of the hypethetical user.
    * last_name = This represents the last name of the hypethetical user.
    * email = This represents a email of the hypethetical user.
    * profile_id = This will be generated for the user when the user registers.
    * gender = This is a field that represents the gender of a user. This could be helpful in matching a mentee to mentor since it would provide more middle ground between the two.
    * formerly_incarcerated = This is a field that represents if the user has been previously incarcerated. 
    * convictions_list = This is a field that will be randomized of a few possible convictions. I've included logic to input "None" if the user specifies they haven't been incarcerated.
    * street_address = This is a random real street address from a medium to large sized city.
    * city = This is a random real city assicoated to the street address.
    * state = This is a random real state assicoated to the street address.
    * zip = This is a random real zip assicoated to the street address.
    * veteran_stauts = This is a field that represents if our hypethetical user has served in the military. This could be helpful in matching a mentor or mentee since it would provide more middle ground between the two.
    * intention = This is a field that represents what the user is after. This includes: Life coaching, programming development, and career readiness.
        * Depending on what selection is randomized will determine the next few data points.
    * tech_stack = This is a field to represent the mentee's desired programming development path. If they weren't randomized programming development, they will have "None" in this field.
    * career_development = This is a field to represent the mentee's desired career help. If they weren't randomized programming development, they will have "None" in this field.
    * known_languages = This is a field that represents if the mentee has any known languages. I've included this field with a majority bias of "None", but I wanted to include a couple of small chances they may share a potential known langauge in common with a mentor. If they weren't randomized programming development, they will have "None" in this field.
    * date_submitted - This is a field that is a randomizd date between the last two years to simulate a potential application.
* The Class methods - below will be the functions used in generating data for the mentee class.
    * increment_intake_counter = This function will be used to generate a sequential intake_id.
    * to_df = This function will be used to generate a dataframe based on the generated users and input will be the number of mentees.

## Mentor Class:
* The "__init__"s - below will be the methods in generating data for the mentor class.
    * mentor_intake_id = When the mentor submits an application this identifier will be assigned for tracking said application.
    * first_name = This represents the first name of the hypethetical user.
    * last_name = This represents the last name of the hypethetical user.
    * email = This represents a email of the hypethetical user.
    * profile_id = This will be generated for the user when the user registers.
    * gender = This is a field that represents the gender of a user. This could be helpful in matching a mentee to mentor since it would provide more middle ground between the two.
    * street_address = This is a random real street address from a medium to large sized city.
    * city = This is a random real city assicoated to the street address.
    * state = This is a random real state assicoated to the street address.
    * zip = This is a random real zip assicoated to the street address.
    * veteran_stauts = This is a field that represents if our hypethetical user has served in the military. This could be helpful in matching a mentor or mentee since it would provide more middle ground between the two.
    * intention = This is a field that represents what the user is after. This includes: Life coaching, programming development, and career readiness.
        * Depending on what selection is randomized will determine the next few data points.
    * tech_stack = This is a field to represent the mentor's known programming development stack. If they weren't randomized programming development, they will have "None" in this field.
    * career_development = This is a field to represent the mentor's known career skills. If they weren't randomized programming development, they will have "None" in this field.
    * known_languages = This is a field that represents if the mentor's known languages. If they weren't randomized programming development, they will have "None" in this field.
    * years_programming = This is a field that represents how long the mentor has been programming.
    * date_submitted - This is a field that is a randomizd date between the last two years to simulate a potential application.
* The Class methods - below will be the functions used in generating data for the mentee class.
    * increment_intake_counter = This function will be used to generate a sequential intake_id.
    * to_df = This function will be used to generate a dataframe based on the generated users and input will be the number of mentees.

## Thoughts:
* I think that a K-Means clustering model would be a great choice for automating some of the matching process.
* KNN might be another good choice. It's worth looking into depending on the approach.
* I think that drop downs and multi-selects will increase the effiency of all models. It's worth looking into ironing out the detials for what questions should be asked to the user on signup. I've included some options for datapoints in the flow, but there's room for improvement.