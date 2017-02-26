from django.shortcuts import render, redirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import User

# Project Views
def index(request):
	return render(request, 'login_reg_app/index.html')

def process(request):
	postType = request.POST
	if request.method == 'POST':
		if request.POST['submit'] == 'Register':
			# Get registration information
			first_name = request.POST['first_name']
			last_name = request.POST['last_name']
			email = request.POST['email']

			validateInfo = {
				'first_name': first_name,
				'last_name': last_name,
				'email': email
			}

			# Checking validity of the user-entered info.
			checkInfo = User.userManager.validate(validateInfo)
			if checkInfo:
				for idx in range(len(checkInfo)):
					messages.error(request, checkInfo[idx])
				return redirect(reverse('login_reg:login_reg_index'))

			#Verify that user is not already in the Db
			userCheck = User.userManager.getUserByEmail(email)
			if userCheck:
				messages.error(request, 'This email is already in the database. Please register with a different email.')
				return redirect(reverse('login_reg:login_reg_index'))
			else:
				# Check the length of the entered password and that password and confirm password match. If both are true then secure the password using bcrypt.
				pwCheck = User.userManager.pwSecure(request.POST['password'], request.POST['pwConfirm'])
				if pwCheck[0] == True:
					# Adding new user to Db
					userAdd = User.userManager.addUser(validateInfo, pwCheck[1])

					# Get user info and redirect to success page
					newUserGet = User.userManager.getUserByEmail(email)
					for user in newUserGet:
						idNew = str(user.id)
					messages.success(request, 'Successfully logged in!')
					return redirect('/process/login/'+ idNew)
				else:
					for idx in range(len(pwCheck[1])):
						messages.error(request, pwCheck[1][idx])
					return redirect(reverse('login_reg:login_reg_index'))

		elif request.POST['submit'] == 'Login':
			# Get entered login information
			email = request.POST['email']
			password = request.POST['password']

			# Query Db for user based on entered email
			findUser = User.userManager.getUserByEmail(email)

			# If verify user exists in Db. If yes, send to success page. if no tell user to register
			if findUser:
				for user in findUser:
					pwUser = user.password
					idLogin = str(user.id)

				# Verify that pw matches what's in the Db
				confirmPW = User.userManager.pwVerifyLogin(password, pwUser)

				if confirmPW[0] == True:
					messages.success(request, confirmPW[1])
					return redirect('/process/login/'+ idLogin)
				else:
					messages.error(request, confirmPW[1])
					return redirect(reverse('login_reg:login_reg_index'))
			else:
				messages.error(request, 'User not found. Please Register above.')
				return redirect(reverse('login_reg:login_reg_index'))

def success(request, id):

	userID = id
	getUserInfo = User.userManager.getUserByID(userID)

	userContext = {
		'userInfo': getUserInfo
	}
	return render(request, 'login_reg_app/success.html', userContext)
