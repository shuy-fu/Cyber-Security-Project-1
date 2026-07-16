# Cyber-Security-Project-1
I will be using the OWASP Top 10:2021 list. 

LINK: https://github.com/shuy-fu/Cyber-Security-Project-1 


FLAW1: 
https://github.com/shuy-fu/Cyber-Security-Project-1/blob/d1400db68f78ab322e9c828bd449996896506a2e/readingjournal/views.py#L72 
A01 Broken Access Control:
OWASP describes this flaw as users being able to act outside of their intended permissions. In the vulnerable version of my app, anyone could delete any book by altering the URL. When the delete URL of a book is accessed, the app doesn’t require a user to be logged in, nor does it check if the user matches the book’s owner. As an example, in screenshot ‘flaw-1-before-1.png’, I have accessed the delete page of the book with an ID 6 without logging in. 

To fix this issue, I added a line that requires users to log in to be able to delete a book. To ensure a user only deletes one’s own books, the fixed version also checks if the user matches the book’s owner. In the screenshot ‘flaw-1-after-1.png’, if someone tries to access a book delete URL, they will be prompted to log in instead of allowing the deletion. 


FLAW2: 
https://github.com/shuy-fu/Cyber-Security-Project-1/blob/d1400db68f78ab322e9c828bd449996896506a2e/readingjournal/views.py#L96 
A03 Injection: 
In the vulnerable version of my app, the commenting feature allows user-supplied input to be interpreted as part of a SQL command instead of treating it as regular comment data. A raw SQL query that uses f-strings will allow a user to insert malicious code straight into the SQL command without it being validated. To demonstrate this vulnerability, I tested whether a single quotation mark in the comment text field cause a SQL query. As shown in screenshot ‘flaw-2-before-1.png’, a SQL operational error was generated. This shows that the single quotation mark was interpreted as part of the SQL command instead of a regular text line for a comment. This would allow SQL injection attacks. 

To fix this vulnerability, I would not use a raw SQL query. Instead, Django ORM provides a tool to make queries without writing raw SQL.  The method ‘create()’ will ensure that a user’s input will not be treated as an executable SQL command. Now even when I test this with a single quotation mark, it will be treated as regular data and the SQL operational error will not show. This is shown in screenshot ‘flaw-2-after-1.png’, where we can observe a comment of a single quotation mark. 

 
FLAW3:  
https://github.com/shuy-fu/Cyber-Security-Project-1/blob/d1400db68f78ab322e9c828bd449996896506a2e/readingjournal/views.py#L103 
https://github.com/shuy-fu/Cyber-Security-Project-1/blob/d1400db68f78ab322e9c828bd449996896506a2e/readingjournal/models.py#L18 
https://github.com/shuy-fu/Cyber-Security-Project-1/blob/d1400db68f78ab322e9c828bd449996896506a2e/readingjournal/templates/readingjournal/detail.html#L27 
A04 Insecure Design: 
The third flaw is also related to user input and limiting what one is able to insert into the comment field. In the vulnerable version, a user is able to submit an empty comment or a comment without maximum length. An extremely long comment could for example, lead to a Denial of Service attack. In the screenshot ‘flaw-3-before-1.png’ we can see both an empty comment and part of a massively long comment. 

The OWASP list states that an insecure design vulnerability shoul be prevented by integrating plausibility checks at each tier of your application (from frontend to backend). To fix this flaw in my app, I have spesified that a max_lenght of 1000 characters is the intended limit. To validate the input, I implemented a plausibility check in views.py. If a user tried to submit an empty comment, the server would return a HTTPResponse saying that ‘The comment cannot be empty’. Then if the comment exceeds maximum lenght, the HTTPResponse would say ‘Comment is too long’. To ensure that plausibility checks are intact also in the frontend, I implemented a comment validating function in the html file. Now the user will get a pop-up notification if their comment is empty or exceeds max_lenght. These are demonstrated in ‘flaw-3-after-1.png’ and ‘flaw-3-after-2.png’. 


FLAW4:  
https://github.com/shuy-fu/Cyber-Security-Project-1/blob/d1400db68f78ab322e9c828bd449996896506a2e/mysite/settings.py#L26 
https://github.com/shuy-fu/Cyber-Security-Project-1/blob/d1400db68f78ab322e9c828bd449996896506a2e/readingjournal/views.py#L50 
A05 Security Misconfiguration: 
This vulnerability has to do with revealing overly informative error messages to users.  In the vulnerable version of my app, if a user were to change the book ID of the URL to a non-existing book ID number, an error page will be generated. Because my app contains ‘DEBUG = True’, a detailed error page will be displayed. This page would reveal the app’s internal structure and possibly allow an attacker to use this information for malicious intent. In screenshot ‘flaw-4-before-1.png’, we can see part of the error page. 

In order to fix this, we need to change ‘DEBUG’ INTO ‘False’ and I have added a HTTPResponse that states ‘Book does not exist’ that will be displayed after the app tries to retrieve a book and notices that it does not exist. This is shown in screenshot ‘flaw-4-after-1.png’. 


FLAW5: 
https://github.com/shuy-fu/Cyber-Security-Project-1/blob/d1400db68f78ab322e9c828bd449996896506a2e/mysite/settings.py#L89 
A07 Identification and Authentication Failures: 
Finally, we have a vulnerable feature that OWASP describes as an app permitting default, weak, or well-known passwords, such as ‘Password1’ or ‘admin/admin’. In my app, the registration form is generated using Django’s ‘UserCreationForm()’. This form follows the validation rules that are set in settings.py ‘AUTH_PASSWORD_VALIDATORS’. In this vulnerable version, norules were set, so this allows users to register with weak passwords. The screenshot ‘flaw-5-before-1.png’ shows the registration form without rules. 

To address this vulnerability, I have added password validators in settings.py. These requirements will be displayed to users in the registration process. Screenshot ‘flaw-5-after-1.png’ shows the fixed form and ‘flaw-5-after-2.png’ shows a failed attempt to register. 
