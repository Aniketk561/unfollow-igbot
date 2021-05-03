import time 
from keys_ig import *
from InstagramAPI import InstagramAPI
import csv

api = InstagramAPI(USERNAME, PASS)
api.login()
user_id = api.username_id

def getTotalFollowers():
    followers = []
    next_max_id = True
    while next_max_id:
        # first iteration hack
        if next_max_id is True:
            next_max_id = ''

        _ = api.getUserFollowers(user_id, maxid=next_max_id)
        followers.extend(api.LastJson.get('users', []))
        next_max_id = api.LastJson.get('next_max_id', '')
    return followers

def getTotalFollowing():
    followers = []
    next_max_id = True
    while next_max_id:
        # first iteration hack
        if next_max_id is True:
            next_max_id = ''

        _ = api.getUserFollowings(user_id, maxid=next_max_id)
        followers.extend(api.LastJson.get('users', []))
        next_max_id = api.LastJson.get('next_max_id', '')
    return followers

def nonFollowers(followers, following):
    nonFollowers = {}
    dictFollowers = {}
    for follower in followers:
        dictFollowers[follower['username']] = follower['pk']

    for followedUser in following:
        if followedUser['username'] not in dictFollowers:
            nonFollowers[followedUser['username']] = followedUser['pk']

    return nonFollowers

def unFollow():
    followers = getTotalFollowers()
    following = getTotalFollowing()
    nonFollow = nonFollowers(followers, following)
    i = len(nonFollow)
    print('Number of followers:', len(followers))
    time.sleep(3)
    print('Number of following:', len(following))
    time.sleep(3)
    print('Number of nonFollowers:', i)
    time.sleep(3)
    print("")

    while i!=0:
        choice2 = input("Do you want to unfollow all those who don't Follow you Back [listed in Unfollowed-log.csv] ? (y/n)")
        print("")
        time.sleep(3)
        if choice2 == 'y':
            with open('Unfollowed-log.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                while i!=0:
                    try:
                        i-=1
                        user = list(nonFollow.keys())[len(nonFollow)-1]
                        api.unfollow(nonFollow[user])
                        nonFollow.pop(user)
                        print('Unfollowed User: ', str(user))
                        writer.writerow([user])
                    except Exception as e:
                        print("Error While Unfollowing: " + str(user))
                        time.sleep(2)
                        print(str(e))

        elif choice2 == 'n':
            print("Exiting...!!")
            break

    if i == 0:
        print("")
        print("NO NON-FOLLOWERS IN ACCOUNT NOW.")
        time.sleep(3)
        print("")
        print("Everyone You are following is also following you.")
        print("")
        time.sleep(2)
        print("Exiting Now.")
        time.sleep(2)

if __name__ == "__main__":
    unFollow()    