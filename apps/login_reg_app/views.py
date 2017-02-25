from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User
import bcrypt
import re

emailValidate = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Project Views
def index(request):
	return render(request, 'login_reg_app/index.html')

def process(request):
	if request.method == 'POST':
		if request.POST['register']:
			# Get registration information
			first_name = request.POST['first_name']
			last_name = request.POST['last_name']
			email = request.POST['email']
			password = request.POST['password']
			pwConfirm = request.POST['pwConfirm']

			# Validity checks
			# Checking that length of first_name and last_name is 2 char or more
			if len(first_name) < 2 or len(last_name) < 2:
				messages.error(request, 'First name and last name must be at least 2 characters in length.')
				return redirect('/')

			# Checking that email fits valid email format
			if len(email) < 1 or not emailValidate.match(email):
				messages.error(request, 'Your email is not valid!')
				return redirect('/')

			# Checking that password and pwConfirm match and that password is at least 8 characters
			if len(password) < 8:
				messages.error(request, 'Your password must be at least 8 characters')
			if password != pwConfirm:
				messages.error(request, 'Your password and Confirm Password must match')
				return redirect('/')
			# Encrypt PW using bcrypt and check validity
			password = password.encode()
			pwHashSalt = bcrypt.hashpw(password, bcrypt.gensalt())

			#Verify that user is not already in the Db
			userCheck = User.objects.filter(email=email)
			if userCheck:
				messages.error(request, 'This email is already in the database. Please register with a different email.')
				return redirect('/')
			else:
				# Adding new user to Db
				userAdd = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=pwHashSalt)

				newUserGet = User.objects.filter(email=email)
				for user in newUserGet:
					print str(newUserGet['id'])
					idNew = str(newUserGet['id'])
				return redirect('/process/login/'+ idNew)
		elif request.POST['login']:
			# Get entered login information
			email = request.POST['email']
			password = request.POST['password']

			# Query Db for user based on entered email
			findUser = User.objects.filter(email = email)

			# If verify user exists in Db. If yes, send to success page. if no tell user to register
			if findUser:
				if bcrypt.check_password_hash(findUser['password'], password):
					return render(request, 'login_reg_app/success.html')
			else:
				messages.error(request, 'User not found. Please Register above.')
				return redirect('/')

def success(request, id):
	return render(request, 'login_reg_app/success.html')
