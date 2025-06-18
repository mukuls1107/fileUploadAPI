Test
Framework - Any Python Framework
Database - SQL / NoSQL Database
Create a secure file-sharing system between two different types of users. For
implementation -
You need to create REST API’s for the following action.
User 1: Operation User
Action which could be done by an Ops User

1. Login
2. Upload File*

* Only Ops User is allowed to upload pptx,docx and xlsx *
Upload file must be only of pptx,docx, and xlsx type
User 2: Client User
Action which could be done by a Client User
3. Sign Up ( Return an encrypted URL )
3. Email Verify ( Verification Email will be sent to the user on the registered email )
3. Login
3. Download File
3. List all uploaded files
Important Information
● You need to make sure when a person hits download API a secure encrypted
URL is sent in response through which the file can be downloaded.
● This URL can be accessed only by a client user.
● If any other user tries to access it the URL access would be denied to that user.

3 of 2

Example -
Client User Hits API- /download-fle/{{Assignment ID}}
Response - {

“download-link” :
“..../download-fle/moiasnciaduasnduoadosnoadaosid”,
“message” : “success”
}

Extra Points

1. Write Test Cases for the above.
2. How do you plan on deploying this to the production environment?