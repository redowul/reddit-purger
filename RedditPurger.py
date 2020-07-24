import praw, prawcore
from psaw import PushshiftAPI
import datetime as dt
import time

api = PushshiftAPI()

# Reddit account information; you cannot delete data for an account you do not have access to.
username = "" # Your Reddit username
password = "" # Your Reddit password

# These two values are needed to access Reddit’s API as a script application (see Authenticating via OAuth for other application types). 
# If you don’t already have a client ID and client secret, follow Reddit’s First Steps Guide to create them.
# https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps
client_id     = ""  # Reddit app client id
client_secret = ""  # Reddit app secret

# A user agent is a unique identifier that helps Reddit determine the source of network requests. 
# https://github.com/reddit-archive/reddit/wiki/API
user_agent = "" 

# Edit comment first before deleting it. Leave blank to leave comment unedited at time of deletion.
# Likely an unnecessary feature as the data would still be retained by Pushshift at time of deletion, but I included it for peace of mind anyway.  
edit_value = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
ask_before_deleting = True  # Ask before deleting every comment. False = auto delete.

start_epoch = dt.datetime(2005, 6, 25) # Year, Month, Day. Only comments / submissions created after the given datetime will be fetched and deleted.
end_epoch = dt.datetime(2020, 7, 24) # Year, Month, Day. Only comments / submissions created before the given datetime will be fetched and deleted.

# Updated as the algorithm progresses so that new items are continuously fetched, shrinking the time between the start and end epochs over time.
# Since the items in the pushshift database remain even after any comments or submissions are deleted from reddit, without this variable
# the algorithm would continuously fetch the same X comments/submissions (where x = batch_size) every run.
last_item_timestamp = None 

batch_size = 100 # Number of comments / submissions to delete at once. Maximum value accepted by the pushshift api is 100. 

def delete_comments(reddit, api):
    print("Deleting comments")
    count = 0
 
    comments = list(api.search_comments(
        before  = int(end_epoch.timestamp()),
        after   = int(start_epoch.timestamp()),
        author  = username,
        limit   = batch_size,
        sort    = "asc")) # sort results ascended order; needed to update the last_item_timestamp variable accurately.

    while(len(comments) > 0):
        for id in comments:
            comment = reddit.comment(id)
            last_item_timestamp = dt.datetime.fromtimestamp(comment.created_utc)
            if comment.body != "[deleted]":
                if ask_before_deleting:
                    print("https://www.reddit.com" + comment.permalink)
                    response = input("Are you sure you want to delete this comment? [Y/N]")
                    if response.lower() == "y":
                        print("Deleting: https://www.reddit.com" + comment.permalink)
                        if len(edit_value) > 0: 
                            if comment.body != "[deleted]":
                                try:
                                    comment.edit(edit_value)
                                except prawcore.exceptions.Forbidden as exception: # Checks if the subreddit is accessable, quarantined or banned subreddits will return a 403 error
                                    print(exception)
                            comment.delete()
                            count = count + 1
                            print("Deleted " + str(count) + " comments")
                    else:
                        print("Comment skipped")
                else:
                    if len(edit_value) > 0: 
                        if comment.body != "[deleted]": 
                            try:
                                comment.edit(edit_value)
                            except prawcore.exceptions.Forbidden as exception: # Checks if the subreddit is accessable, quarantined or banned subreddits will return a 403 error
                                print(exception)
                    comment.delete()
                    count = count + 1
                    print("Deleted " + str(count) + " comments")

        time.sleep(1) # Pushshift has a rate limit, if we send requests too fast it will start returning error messages.
        comments = list(api.search_comments(
            before  = int(end_epoch.timestamp()),
            after   = int(last_item_timestamp.timestamp()),
            author  = username,
            size    = batch_size,
            sort    = "asc")) # sort results ascended order; needed to update the last_item_timestamp variable accurately

    print("Deleted " + str(count) + " comments total")

def delete_submissions(reddit, api):
    print("Deleting submissions")
    count = 0
 
    submissions = list(api.search_submissions(
        before  = int(end_epoch.timestamp()),
        after   = int(start_epoch.timestamp()),
        author  = username,
        limit   = batch_size,
        sort    = "asc")) # sort results ascended order; needed to update the last_item_timestamp variable accurately.
    
    while(len(submissions) > 0):
        for id in submissions:
            submission = reddit.submission(id)
            last_item_timestamp = dt.datetime.fromtimestamp(submission.created_utc)
            if submission.title != "[deleted]":
                if ask_before_deleting:
                    print("https://www.reddit.com" + submission.permalink)
                    response = input("Are you sure you want to delete this submission? [Y/N]")
                    if response.lower() == "y":
                        if submission.is_self:
                            if len(edit_value) > 0: 
                                if submission.selftext != "[deleted]":
                                    submission.edit(edit_value)
                        print("Deleting: https://www.reddit.com" + submission.permalink)
                        submission.delete()
                        count = count + 1
                    else:
                        print("Submission skipped")
                else:
                    print("Deleting: " + submission.shortlink)
                    if submission.is_self:
                        if len(edit_value) > 0: 
                            if submission.selftext != "[deleted]":
                                submission.edit(edit_value)
                    submission.delete()
                    count = count + 1
                    print("Deleted " + str(count) + " submissions")
        
        time.sleep(1) # Pushshift has a rate limit, if we send requests too fast it will start returning error messages.
        submissions = list(api.search_submissions(
            before  = int(end_epoch.timestamp()),
            after   = int(last_item_timestamp.timestamp()),
            author  = username,
            limit   = batch_size,
            sort    = "asc")) # sort results ascended order; needed to update the last_item_timestamp variable accurately.

    print("Deleted " + str(count) + " submission total")

if __name__ == "__main__":
    print("Logging on")
    reddit = praw.Reddit(
        username = username,
        password = password,
        client_id = client_id,
        client_secret = client_secret,
        user_agent = username
    )

    print(reddit.user.me())
    api = PushshiftAPI(reddit)   
  
    delete_comments(reddit, api) 
    delete_submissions(reddit, api)

    print("Done!")