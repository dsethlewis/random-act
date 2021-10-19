# Rate an activity in the activity list

def like(activity):
    
    rating = input("Do you want to get \""
                   + activity.title
                   + "\" more often? (Y/n) ").lower()
    return rating == "y"

def dislike(activity):

    rating = input("Do you want to get \""
                   + activity.title
                   + "\" less often? (Y/n) ").lower()
    return rating == "y"