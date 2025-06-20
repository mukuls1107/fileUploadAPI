# File Sharing API using Flask, Cloudinary and MongoDB

This is a simple file sharing backend system built using Flask, MongoDB and Cloudinary. Supports user and admin sign up/ sign in for a secured system and allow admins to upload the files and let users download them with a unique link.

## Stack 
- Flask
- MongoDB
- Cloudinary
- SMTP

## Routes
- User Authentication
    - POST `/api/users/signup` - Register a new user
    - GET `/api/users/verify/<token>` - Email Verification with unique token
    - POST `/api/users/login` - Login using email and password
    - Auto resend verification link on email if not verified during the time limit

- File Upload/Download 
    - POST `/api/file/upload` - Allow only admin to upload the files
    - GET `/api/file/uploads` - List all the uploaded files on the cloud
    - GET `/api/file/download?file=<file_id>` - Download the specific file using the unique id


## Run Locally
1. Clone this repository
2. create a `.env` file in the root with the following template
    ```ini
    DB_USERNAME=<mongoDB username>
    DB_PASS=<db password>
    DB_URL=<connection url>

    MY_EMAIL=<your email from where you going to send the verification token to the user>
    MY_EMAILPASS=<generate app password for your email>


    JWT_KEY=<your jwt secret key>

    CLOUDINARY_CNAME=<cloudinary cloud name>
    API_KEY=<cloudinary api key>
    API_SECRET=<clodinary api secret>

    CLOUDINARY_URL=<your cloudinary url from the dashboard>

    ```
3. Run `pip install -r requirements.txt`
4. Finally run `python main.py`


# Made with intent.
This project was built in limited time but with clear structure and purpose.
I’ll keep improving and adding features when I get a chance.