"""
Chatting traders

Conor Reynolds and Elias Tamagni

4/3/18
"""

import matplotlib.pyplot as plt
import pandas as pd

# Convert TSV files to pandas

users = pd.read_table("/Users/elitamagni 1/Desktop/traders/users.tsv")
# user ids, account creation dates
messages = pd.read_table("/Users/elitamagni 1/Desktop/traders/messages.tsv")
# message ids, send dates, sender ids, message types
discussions = pd.read_table("/Users/elitamagni 1/Desktop/traders/discussions.tsv")
# discussion ids, creation dates, creator ids, discussion categories
discussionPosts = pd.read_table("/Users/elitamagni 1/Desktop/traders/discussion_posts.tsv")
# post ids, discussion ids, creator ids
CONST_TIME = (1000*60*60*24) #time conversion constant

# Part 1: Simple Descriptive Statistics

# Number of users in database
print("Users: ", len(users)) # all users

# Time span of database
timeData = pd.concat([discussionPosts["createDate"], discussions["createDate"], messages["sendDate"], users["memberSince"]] ,ignore_index=True)
print("Time: ", (timeData.max() - timeData.min())/(CONST_TIME)) # time span

# Number of messages by type
messageType = messages['type'].unique()
messData = messages['type'].value_counts()
plt.pie(messData, labels = messageType, autopct = '%1.1f%%')
plt.title('Message Type')
plt.axis('equal')
plt.show()
plt.close()

# Number of discussions by type
discussionType = discussions['discussionCategory'].unique()
disData = discussions['discussionCategory'].value_counts()
plt.pie(disData, labels = discussionType, autopct = '%1.1f%%')
plt.title('Discussion Type')
plt.axis('equal')
plt.show()
plt.close()

# Number of discussion posts
print("Discussion Posts: ", len(discussionPosts)) # all discussion posts

# Part 2: Distribution of Activity Ranges

# Activity range is the time between first and last messages sent (in any category)

userActivity = messages.groupby(["sender_id"]) # group by user
activityRange = (userActivity.sendDate.max() - userActivity.sendDate.min())/(CONST_TIME) # get range
plt.figure(2, figsize=(5,5))
plt.title("Activity range of messages")
plt.xlabel("Activity range")
plt.ylabel("User count")
plt.hist(activityRange, bins = 20, log = True)

# Part 3: Distribution of Message Activity Delays

# Message activity delay is the time between user account creation and sending the first user message in a specific category

mergedMessageFrame = pd.merge(users, messages, left_on = "id", right_on = "sender_id")
mergedMessageFrame = mergedMessageFrame.groupby("id_x") # group by user
delay = mergedMessageFrame.min() # first message
flr = delay.loc[delay["type"] == "FRIEND_LINK_REQUEST"] # friend link request
flr = (flr.sendDate - flr.memberSince)/(CONST_TIME)
dm = delay.loc[delay["type"] == "DIRECT_MESSAGE"] # direct message
dm = (dm.sendDate - dm.memberSince)/(CONST_TIME)
plt.figure(3, figsize = (5, 5))
plt.title("Message activity delay")
plt.xlabel("Activity delay")
plt.ylabel("User count")
plt.hist(flr, bins = 20, log = True, alpha = 0.5, label = "Friend link request")
plt.hist(dm, bins = 20, log = True, alpha = 0.5, label = "Direct message")
plt.legend(loc = "upper right")

# Part 4: Distribution of Discussion Categories

# Calculated by number of posts

plt.figure(4, figsize=(10,10))
disc = pd.merge(discussions, discussionPosts, left_on= 'id', right_on='discussion_id')
discPie = disc.discussionCategory.value_counts()
discPie.plot.pie(labeldistance=1.2, shadow=True, autopct='%1.1f%%', pctdistance=1.1, explode = (0.15, 0, 0,0,0,0,0,0,0), legend = True).set_ylabel("")
plt.title("Discussion categories")
plt.show()
plt.close()

# Part 5: Post Activity Delay

# Post activity delay is the time between user account creation and posting the first discussion message
# This shows the post activity delays in the most popular category, which is QUESTION

mergedPostFrame = pd.merge(users, disc, left_on = "id", right_on = "id_x")
mergedPostFrame = mergedPostFrame.groupby("id") # group by user
postDelay = mergedPostFrame.min() # first post
data = postDelay.loc[postDelay["discussionCategory"] == "QUESTION"] # most popular
data = (data.createDate_x - data.memberSince)/(CONST_TIME) # range
plt.figure(5, figsize = (5, 5))
plt.title("Post activity delay")
plt.xlabel("Activity delay")
plt.ylabel("User count")
plt.hist(data, bins = 20, log = True)

# Part 6: Box and Whisker Plots

# Demonstrating statistics for message activity delays in each category, post activity delays, and activity ranges

# size of the boxplot
plt.figure(6, figsize=(10,20))
# size of each subplot
plt.subplot(1, 4, 1)
# title of each subplot 1
plt.title("Friend Request")
# make the each subplot
flr.plot.box(label="", showmeans=True).set_ylabel("Box plot")
# set the scale for each bin
plt.yscale('log')
plt.subplot(1, 4, 2)
plt.title("Direct Message")
dm.plot.box(label="", showmeans=True)
plt.yscale('log')
plt.subplot(1, 4, 3)
plt.title("Post Activity")
data.plot.box(label="", showmeans=True)
plt.yscale('log')
plt.subplot(1, 4, 4)
plt.title("Activity")
activityRange.plot.box(label="", showmeans=True)
plt.yscale('log')
plt.show()
plt.close()
