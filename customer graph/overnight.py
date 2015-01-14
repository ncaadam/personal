import frequent_functions as ff
import twitter_functions as tf
import time


def main():
    cursor = -1
    users = []
    for i in range(0, 500000, 5000):
    	print "Iteration #" + str((i/5000) + 1)
    	print "There are", str(len(users)), "users in the list."
    	new_users,cursor = tf.grab_twitter_followers('Starbucks',cursor)
    	for user in new_users:
    		users.append(user)
    	print "Next cursor:", cursor
    	if len(new_users) < 5000:
    		break
    	print "Sleeping..."
    	time.sleep(61)
    	print "Awake..."
    
    with open('test.txt', 'wb') as f:
    	for item in users:
    		f.write(item + "\n")


    

if __name__ == "__main__":
    main()

