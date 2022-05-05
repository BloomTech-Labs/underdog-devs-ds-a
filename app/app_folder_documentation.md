# app folder documentation

If this list of endpoints or files ever change (order/add/delete) please correct this readme to reflect the changes, so the current and next cohorts can have the most up to date documentation. Tips for future documentation:
1. Be quick and easy both to create and update. Information that is out of date can be worse than no information at all.
2. Easily provide correct answers. If it’s not easy to find no one will use it anyway.
3. Not replace human interaction. Individuals and interaction over processes and tools, right?

## api.py

This api contains all of our current endpoints that connect backend to ds. Backend uses these endpoints to send and receive data from the data science team. For more detail on each endpoint visit our [elasticbeanstalk API URL](http://underdog-devs-ds-a-dev.us-east-1.elasticbeanstalk.com) or open the file and look at doc strings.

## data.py

Not 100% sure what this file contains, but it seems important to working mongodb 

## graphs.py

This file current contains the function that is used in the /graphs/tech-stack-by-role endpoint.

## model.py

Here is where our matching classes are located. There are a few matching features implemented and they are stored here. Here is a list of the current classes that we have and what they do. For more detail on each class please open the file and look at doc strings. 

MatcherSortSearch

MatcherSortSearchResource

## utilities.py

This file current contains the function that is used in the /financial_aid/{profile_id} endpoint.

## vader_sentiment.py

This file currently contains the function that is used in the /sentiment endpoint.
