# Reddit Purger

This is a script to delete any Reddit comments and submissions associated with a given Reddit account. This is achieved through use of the Pushshift API to retrieve all the comment/submission ids associated with said account and passing those ids to PRAW (The Python Reddit API Wrapper) for deletion. Pushshift was necessary to accomplish this goal because Reddit's API limits the maximum amount of data that can be retrieved to the most recently posted 1000, with no means of retrieving older data even if those initial 1000 comments and submissions are deleted.

Pushshift is a separate database which stores a copy of everything posted on Reddit: every comment, and every submission. Using this database, all data about a particular account can be retrieved and passed to PRAW, bypassing Reddit's 1000 post retrieval limit.

##### Those interested in completely deleting their Reddit data be warned, as this process only deletes your data from Reddit's (public) servers and not Pushshifts, the copy will remain to be read by websites such as removeddit.com, which displays information fetched from the Pushshift database. Luckily, the maintainers of Pushshift will fulfill any requests for data deletion from Pushshift if the owner of the account requests that they do so. Find out more at https://www.reddit.com/r/pushshift/

##### WARNING! Remember that because this script uses Pushshift's database to delete your data from Reddit's database, requesting that Pushshift's maintainers delete your data will strip you of the ability to use their database in conjunction with this script to delete your information from Reddit in the first place. Be certain that all the data you want deleted from Reddit has been deleted before making any requests for data deletion at Pushshift.

## Install

Install pip: https://github.com/pypa/pip

Using pip, install PRAW and the PushshiftAPI.

## Usage

Supply your Reddit account's username, password, application client id and application secret. The program will do the rest and delete every Reddit comment and submission accessible via the PushShift API associated with the given account. Note that "accessible" in this context means posted in a public Subreddit, as private Subreddits are inaccessible to the Pushshift API and were therefore unable to be stored for later retrieval.

## What is PRAW?

https://github.com/praw-dev/praw

"PRAW, an acronym for "Python Reddit API Wrapper", is a Python package that allows for simple access to Reddit's API. PRAW aims to be easy to use and internally follows all of Reddit's API rules. With PRAW there's no need to introduce sleep calls in your code. Give your client an appropriate user agent and you're set."

More information can be found at the following URL: https://praw.readthedocs.io/en/latest/

## What is Pushshift?

https://www.reddit.com/r/pushshift/comments/bcxguf/new_to_pushshift_read_this_faq/

"Pushshift is a big-data storage and analytics project started and maintained by Jason Baumgartner (reddit.com/u/Stuck_In_the_Matrix). Most people know it for its copy of reddit comments and submissions."

More information can be found at the following URLs:

https://github.com/pushshift/api
https://github.com/dmarx/psaw
https://arxiv.org/pdf/2001.08435.pdf#:~:text=Specifically%2C%20because%2C%20at%20the%20time,ingest%20large%20amounts%20of%20data.
https://www.reddit.com/r/pushshift/

## License

MIT
