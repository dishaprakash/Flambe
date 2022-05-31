def new_user(username, pw):
	file_obj = open("Users.txt", "a")
	file_obj.write("{} {}\n".format(username, pw))
	file_obj.close()

	file_obj = open("{}.txt".format(username), "a")
	file_obj.close()


def check_pw(username, pw):
	file_obj = open("Users.txt", "r")
	details = file_obj.readlines()
	final = 0

	for i in range(len(details)):
		if details[i] == (username + " " + pw + "\n") :
			final = 1

	if final == 1:
		return True

	if final == 0:
		return False


def check_existing_user(username, pw):
	file_obj = open("Users.txt", "r")
	details = file_obj.readlines()

	final = 0

	for i in range(len(details)):
		if details[i].startswith(username):
			final = 1

	if final == 1:
		return True

	if final == 0:
		return False


def username_criteria(username):
	if " " in username:
		return False
	else:
		for letter in username:
			if not letter.isalnum():
				return False
		return True


def password_len(pw):
	if len(pw) <= 13:
		return True
	else:
		return False
