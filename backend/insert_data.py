import requests

URL = "http://127.0.0.1:3000"
IMG_URL = "http://127.0.0.1:4000"



users = [
    {
        "username": "BOB", 
        "password": "password",
        "first_name" : "BOB",
        "last_name" : "LE",
        "email" : "BOB@gmail.com",
        "phone_number" : "0556023158"
    },
    {
        "username": "john", 
        "password": "password",
        "first_name" : "Salim",
        "last_name" : "khelindi",
        "email" : "Gabriel@gmail.com",
        "phone_number" : "0556023158"
    },
    {
        "username": "James", 
        "password": "password",
        "first_name" : "Yoyo",
        "last_name" : "Drake",
        "email" : "Bridie@gmail.com",
        "phone_number" : "0556023158"
    },
    {
        "username": "David", 
        "password": "password",
        "first_name" : "ZOZ",
        "last_name" : "LE",
        "email" : "Brade@gmail.com",
        "phone_number" : "0556023158"
    }]


posts = [
        {
        "post_type": "post",
        "post_title": "prevent SQL injection",
        "post_body": """The correct way to avoid SQL injection attacks, 
no matter which database you use, is to separate the data from SQL, 
so that data stays data and will never be interpreted as commands by the SQL parser. 
It is possible to create an SQL statement with correctly formatted data parts, 
but if you don't fully understand the details, you should always use prepared statements and parameterized queries. 
These are SQL statements that are sent to and parsed by the database server separately from any parameters. 
This way it is impossible for an attacker to inject malicious SQL.""",
        "post_code" : "",
        "post_skills" : []
    },
        {
        "post_type": "post",
        "post_title": "What is the difference between 'INNER JOIN' and 'OUTER JOIN'",
        "post_body": """In simple words:
An inner join retrieve the matched rows only.
Whereas an outer join retrieve the matched rows from one table and all rows in other table ....the result depends on which one you are using:
Left: Matched rows in the right table and all rows in the left table
Right: Matched rows in the left table and all rows in the right table or
Full: All rows in all tables. It doesn't matter if there is a match or not""",
        "post_code" : "",
        "post_skills" : []
    },
    {
        "post_type": "post",
        "post_title": "HTML input pattern",
        "post_body": """The pattern attribute is an attribute of the text, tel, email, url, password, and search input types.
The pattern attribute, when specified, is a regular expression which the input's value must match for the value to pass constraint validation. It must be a valid JavaScript regular expression, as used by the RegExp type, and as documented in our guide on regular expressions; the 'u' flag is specified when compiling the regular expression so that the pattern is treated as a sequence of Unicode code points, instead of as ASCII. No forward slashes should be specified around the pattern text.""",
        "post_code" : "",
        "post_skills" : []
    },
    {
        "post_type": "post",
        "post_title": "pass-by-reference And pass-by-value",
        "post_body": """The terms "pass-by-value" and "pass-by-reference" have special, 
precisely defined meanings in computer science. These meanings differ from the intuition many people have when first hearing the terms. 
Much of the confusion in this discussion seems to come from this fact.
The terms "pass-by-value" and "pass-by-reference" are talking about variables. 
Pass-by-value means that the value of a variable is passed to a function/method. 
Pass-by-reference means that a reference to that variable is passed to the function. 
The latter gives the function a way to change the contents of the variable.""",
        "post_code" : "",
        "post_skills" : []
    },
    
]

questions = [
    {
        "post_type": "question",
        "post_title": "How do I return the response from an asynchronous call?",
        "post_body": "This is my code",
        "post_code": """
function foo() {
    var result;

    $.ajax({
        url: '...',
        success: function(response) {
            result = response;
            // return response; // <- I tried that one as well
        }
    });

    return result; // It always returns `undefined`}""",
        "post_skills" : [3]
    },
    {
        "post_type": "question",
        "post_title": "How can I remove a specific item from an array in JavaScript?",
        "post_body": "How do I remove a specific value from an array? Something like:",
        "post_code": "array.remove(value);",
        "post_skills" : [1,2,3]
    },
    {
        "post_type": "question",
        "post_title": "How can I find all files containing specific text (string) on Linux?",
        "post_body": """How do I find all files containing a specific string of text within their file contents?
        The following doesn't work. It seems to display every single file in the system.""",
        "post_code": "find / -type f -exec grep -H 'text-to-find-here' \;",
        "post_skills" : []
    },
    {
        "post_type": "question",
        "post_title": "How do I change permissions for a folder and its subfolders/files?",
        "post_body": """How do I change the permissions of a folder and all its subfolders and files?
This only applies to the /opt/lampp/htdocs folder, not its contents:""",
        "post_code": "chmod 775 /opt/lampp/htdocs",
        "post_skills" : []
    },
]

images = ["user1.jpg", "user2.jpg", "user3.jpg", "user4.jpg"]
i = 0

for user in users:
    r = requests.post(URL + "/register" ,json=user)
    print(r)

    r = requests.post(URL + "/login" ,data={"username": user["username"], "password" : user["password"]})
    print(r.json())

    user["access_token"] = r.json()["access_token"]

    r = requests.post(URL + "/posts" ,json=posts[i], headers={"Authorization": str("Bearer " + user["access_token"]) });
    print(r.json())
    posts[i]["post_id"] = r.json()

    r = requests.post(URL + "/posts" ,json=questions[i], headers={"Authorization": str("Bearer " + user["access_token"]) });
    print(r.json())
    questions[i]["post_id"] = r.json()




    # change img
    #files = {'image': open('static/img/user1.jpg','rb'), "content_type" : "image/jpeg"}
    ImageName = images[i]
    files = { 'image': (ImageName, open("static/img/" + ImageName,"rb"), "image/jpeg")  }
    r = requests.post(IMG_URL + "/user_profile_img/" ,files=files, headers={"Authorization": str("Bearer " + user["access_token"])});
    print(r.json())

    i = i + 1;

# like posts
r = requests.post(URL + "/postlike/" + str(posts[0]['post_id']) , headers={"Authorization": str("Bearer " + users[0]["access_token"]) });
print(r)
r = requests.post(URL + "/postlike/" + str(posts[0]['post_id']) , headers={"Authorization": str("Bearer " + users[1]["access_token"]) });
print(r)
r = requests.post(URL + "/postlike/" + str(posts[0]['post_id']) , headers={"Authorization": str("Bearer " + users[2]["access_token"]) });
print(r)
r = requests.post(URL + "/postlike/" + str(posts[0]['post_id']) , headers={"Authorization": str("Bearer " + users[3]["access_token"]) });
print(r)

r = requests.post(URL + "/postlike/" + str(posts[1]['post_id']) , headers={"Authorization": str("Bearer " + users[0]["access_token"]) });
print(r)
r = requests.post(URL + "/postlike/" + str(posts[2]['post_id']) , headers={"Authorization": str("Bearer " + users[0]["access_token"]) });
print(r)
r = requests.post(URL + "/postlike/" + str(posts[3]['post_id']) , headers={"Authorization": str("Bearer " + users[0]["access_token"]) });
print(r)
r = requests.post(URL + "/postlike/" + str(posts[1]['post_id']) , headers={"Authorization": str("Bearer " + users[2]["access_token"]) });
print(r)

# like questions
r = requests.post(URL + "/postlike/" + str(questions[0]['post_id']) , headers={"Authorization": str("Bearer " + users[0]["access_token"]) });
print(r)
r = requests.post(URL + "/postlike/" + str(questions[0]['post_id']) , headers={"Authorization": str("Bearer " + users[1]["access_token"]) });
print(r)
r = requests.post(URL + "/postlike/" + str(questions[0]['post_id']) , headers={"Authorization": str("Bearer " + users[2]["access_token"]) });
print(r)
r = requests.post(URL + "/postlike/" + str(questions[0]['post_id']) , headers={"Authorization": str("Bearer " + users[3]["access_token"]) });
print(r)

r = requests.post(URL + "/postlike/" + str(questions[1]['post_id']) , headers={"Authorization": str("Bearer " + users[0]["access_token"]) });
print(r)
r = requests.post(URL + "/postlike/" + str(questions[2]['post_id']) , headers={"Authorization": str("Bearer " + users[0]["access_token"]) });
print(r)
r = requests.post(URL + "/postlike/" + str(questions[3]['post_id']) , headers={"Authorization": str("Bearer " + users[0]["access_token"]) });
print(r)
r = requests.post(URL + "/postlike/" + str(questions[1]['post_id']) , headers={"Authorization": str("Bearer " + users[2]["access_token"]) });
print(r)


comments = [
    {
    "comment_body": "thanks for the the information",
    "comment_code": ""
    },
    {
    "comment_body": "preventing SQL injections is always tricky",
    "comment_code": ""
    },
    {
    "comment_body": """Let functions accept callbacks
A callback is when function 1 is passed to function 
2. Function 2 can call function 1 whenever it is ready. In the context of an asynchronous process, 
the callback will be called whenever the asynchronous process is done. Usually, the result is passed to the callback.""",
    "comment_code": """
function foo(callback) {
    $.ajax({
        // ...
        success: callback
    });
}"""
    },
    {
    "comment_body": """There are basically two ways how to solve this:
Make the AJAX call synchronous (lets call it SJAX).
Restructure your code to work properly with callbacks.""",
    "comment_code": """var request = new XMLHttpRequest();
request.open('GET', 'yourURL', false);  // `false` makes the request synchronous
request.send(null);

if (request.status === 200) {// That's HTTP for 'ok'
  console.log(request.responseText);
}"""
    }

]
# add comments for posts
r = requests.post(URL + "/posts/" + str(posts[0]['post_id']) + "/comments" , json = comments[0],headers = {"Authorization": str("Bearer " + users[0]["access_token"]) });
print(r)
r = requests.post(URL + "/posts/" + str(posts[0]['post_id']) + "/comments" , json = comments[1],headers = {"Authorization": str("Bearer " + users[1]["access_token"]) });
print(r)

# add comments for questions
r = requests.post(URL + "/posts/" + str(questions[0]['post_id']) + "/comments" , json = comments[2],headers = {"Authorization": str("Bearer " + users[2]["access_token"]) });
print(r)
r = requests.post(URL + "/posts/" + str(questions[0]['post_id']) + "/comments" , json = comments[3],headers = {"Authorization": str("Bearer " + users[3]["access_token"]) });
print(r)




projects = [
    {
        "project_name": "DevShare",
        "project_description": "DevShare" 
    },
    {
        "project_name": "Prisma",
        "project_description": "Prisma" 
    }
]




# create projects
r = requests.post(URL + "/projects" , json = projects[0],headers = {"Authorization": str("Bearer " + users[0]["access_token"]) });
print(r.json())
projects[0]["project_id"] = r.json()

r = requests.post(URL + "/projects" , json = projects[1],headers = {"Authorization": str("Bearer " + users[1]["access_token"]) });
print(r.json())
projects[1]["project_id"] = r.json()


invites = [
    {
        "username" : users[0]["username"],
        "role" : "member"
    },
    {
        "username" : users[1]["username"],
        "role" : "member"
    },
    {
        "username" : users[2]["username"],
        "role" : "member"
    },
    {
        "username" : users[3]["username"],
        "role" : "member"
    }
]

#create invite
r = requests.post(URL + "/projects/" + str(projects[1]["project_id"]) + "/invites" , json = invites[0],headers = {"Authorization": str("Bearer " + users[1]["access_token"]) });
print(r.json())
invites[0]["invite_id"] = r.json()
# user 1 invites users2 user3 user4
r = requests.post(URL + "/projects/" + str(projects[0]["project_id"]) + "/invites" , json = invites[1],headers = {"Authorization": str("Bearer " + users[0]["access_token"]) });
print(r.json())
invites[1]["invite_id"] = r.json()

r = requests.post(URL + "/projects/" + str(projects[0]["project_id"]) + "/invites" , json = invites[2],headers = {"Authorization": str("Bearer " + users[0]["access_token"]) });
print(r.json())
invites[2]["invite_id"] = r.json()

r = requests.post(URL + "/projects/" + str(projects[0]["project_id"]) + "/invites" , json = invites[3],headers = {"Authorization": str("Bearer " + users[0]["access_token"]) });
print(r.json())
invites[3]["invite_id"] = r.json()


#accept invites
r = requests.post(URL + "/user/invites/" + str(invites[1]["invite_id"]) , json = invites[0],headers = {"Authorization": str("Bearer " + users[1]["access_token"]) });
print(r)
r = requests.post(URL + "/user/invites/" + str(invites[2]["invite_id"]) , json = invites[0],headers = {"Authorization": str("Bearer " + users[2]["access_token"]) });
print(r)

# get the project members
r = requests.get(URL + "/projects/" + str(projects[0]["project_id"]) + "/members" ,headers = {"Authorization": str("Bearer " + users[0]["access_token"]) });
print(r.json())

members = r.json()


tasks = [
    {
    "task_title": "Conduct research on the project",
    "task_description": "research",
    "task_type": "test",
    "member_id" : members[0]["member_id"],
    "task_start_date": "Fri May 26 2023 11:13:35 GMT+0100 (Central European Standard Time)",
    "task_end_date": "Sat May 27 2023 23:59:59 GMT+0100 (Central European Standard Time)",
    "task_needed_time": 45084,
    "task_skills" : {}
    },
    {
    "task_title": "Define business objectives and goals",
    "task_description": "define the core objectives",
    "task_type": "test" ,
    "member_id" : members[0]["member_id"],
    "task_start_date": "Fri May 26 2023 11:13:35 GMT+0100 (Central European Standard Time)",
    "task_end_date": "Sat May 27 2023 23:59:59 GMT+0100 (Central European Standard Time)",
    "task_needed_time": 45084,
    "task_skills" : {}
    },
    {
    "task_title": "Prototyping",
    "task_description": "make prototype with the main features"  ,
    "task_type": "test" ,
    "member_id" : members[1]["member_id"],
    "task_start_date": "Fri May 26 2023 11:13:35 GMT+0100 (Central European Standard Time)",
    "task_end_date": "Sat May 27 2023 23:59:59 GMT+0100 (Central European Standard Time)",
    "task_needed_time": 45084,
    "task_skills" : { 1 : 5, 2: 5, 3: 5 }
    },
    {
    "task_title": "Test proptotype",
    "task_description": "make tasts for the proptotype"  ,
    "task_type": "test" ,
    "member_id" : members[2]["member_id"],
    "task_start_date": "Fri May 26 2023 11:13:35 GMT+0100 (Central European Standard Time)",
    "task_end_date": "Sat May 27 2023 23:59:59 GMT+0100 (Central European Standard Time)",
    "task_needed_time": 45084,
    "task_skills" : { 1 : 5, 2: 5, 3: 5 }
    }

]



# create tasks

r = requests.post(URL + "/projects/" + str(projects[0]["project_id"]) + "/task" , json = tasks[0],headers = {"Authorization": str("Bearer " + users[0]["access_token"]) });
print(r.json())
tasks[0]["task_id"] = r.json()
r = requests.post(URL + "/projects/" + str(projects[0]["project_id"]) + "/task" , json = tasks[1],headers = {"Authorization": str("Bearer " + users[0]["access_token"]) });
print(r.json())
tasks[1]["task_id"] = r.json()
r = requests.post(URL + "/projects/" + str(projects[0]["project_id"]) + "/task" , json = tasks[2],headers = {"Authorization": str("Bearer " + users[0]["access_token"]) });
print(r.json())
tasks[2]["task_id"] = r.json()
r = requests.post(URL + "/projects/" + str(projects[0]["project_id"]) + "/task" , json = tasks[3],headers = {"Authorization": str("Bearer " + users[0]["access_token"]) });
print(r.json())
tasks[3]["task_id"] = r.json()


# change state
r = requests.put(URL + "/projects/" + str(projects[0]["project_id"]) + "/task/" + str(tasks[0]["task_id"]) + "/state" + "?task_state=in-progress" , json = tasks[3],headers = {"Authorization": str("Bearer " + users[0]["access_token"]) });
print(r)
# change progress
r = requests.put(URL + "/projects/" + str(projects[0]["project_id"]) + "/task/" + str(tasks[0]["task_id"]) + "/progress" + "?task_progress=65&dif_sd_sp=18738" , json = tasks[3],headers = {"Authorization": str("Bearer " + users[0]["access_token"]) });
print(r)


