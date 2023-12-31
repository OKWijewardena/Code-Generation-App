from flask import Flask, render_template, request, Response
import openai

app = Flask(__name__)

# Set your OpenAI API key here
openai.api_key = "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"

# Define a dictionary to map routes to task descriptions
task_descriptions = {
    "/": """You will receive style modifications. You must update this code to reflect the user's desired styles. 
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Magic Navigation Bar</title>
    <style>
        /* Reset some default styles */
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: Arial, sans-serif;
            height: 100vh;
            width: 100%;
            margin: 0;
            padding: 0;
            background-image: radial-gradient(circle 248px at center, #16d9e3 0%, #30c7ec 47%, #46aef7 100%);
        }

        nav {
            overflow: hidden;
            position: relative;
            transform: translateX(-300px);
            height: 100%;
            width: 400px;
            transition: all 800ms cubic-bezier(.8, 0, .33, 1);
            border-radius: 0% 0% 100% 50%;
        }

        nav.nav-open {
            transform: translateX(0px);
            border-radius: 0% 0% 0% 0%;
            background: rgba(255, 255, 255, 0.6);
        }

        nav .menu-btn {
            position: absolute;
            top: 10%;
            right: 5%;
            padding: 0;
            width: 30px;
            cursor: pointer;
            z-index: 2;
        }

        nav .menu-btn .line {
            padding: 0;
            width: 30px;
            background: #fff;
            height: 2px;
            margin: 5px 0;
            transition: all 700ms cubic-bezier(.9, 0, .33, 1);
        }

        nav .menu-btn .line.line--1 {
            width: 30px;
            transform: rotate(0) translateY(0);
        }

        nav .menu-btn .line.line--1.line-cross {
            width: 30px;
            transform: rotate(45deg) translateY(10px);
            background: rgba(0,0,0,0.6);
        }

        nav .menu-btn .line.line--2 {
            width: 28px;
            transform: translateX(0);
        }

        nav .menu-btn .line.line--2.line-fade-out {
            width: 28px;
            transform: translate(30px);
            opacity: 0;
        }

        nav .menu-btn .line.line--3 {
            width: 20px;
            transform: rotate(0) translateY(0);
        }

        nav .menu-btn .line.line--3.line-cross {
            width: 30px;
            transform: rotate(-45deg) translateY(-10px);
            background: rgba(0,0,0,0.6);
        }

        nav .nav-links {
            position: absolute;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            transform: translateX(-100px);
            opacity: 0;
            transition: all 900ms cubic-bezier(.9, 0, .33, 1);
        }

        nav .nav-links.fade-in {
            opacity: 1;
            transform: translateX(0px);
        }

        nav .nav-links .link {
            margin: 20px 0;
            text-decoration: none;
            font-family: sans-serif;
            color: rgba(0,0,0,0.9);
            font-weight: 700;
            text-transform: uppercase;
            font-size: 1.2rem;
            transition: all 300ms cubic-bezier(.9, 0, .33, 1);
        }

        nav .nav-links .link:hover {
            color: rgba(0, 0, 0, .5);
        }

        .inform {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: rgba(255, 255, 255, 0.8);
            font-size: 2rem;
            font-family: sans-serif;
            text-transform: uppercase;
            letter-spacing: 5px;
            text-shadow: 0 0 20px rgba(0,0,0,0.6);
        }

        .support {
            position: absolute;
            right: 10px;
            bottom: 10px;
            padding: 10px;
            display: flex;
        }

        a {
            margin: 0 20px;
            color: #fff;
            font-size: 2rem;
            transition: all 400ms ease;
        }

        a:hover {
            color: #222;
        }
    </style>
</head>
<body>
    <nav>
        <div class="menu-btn">
            <div class="line line--1"></div>
            <div class="line line--2"></div>
            <div class="line line--3"></div>
        </div>

        <div class="nav-links">
            <a href="" class="link">Home</a>
            <a href="" class="link">Contact</a>
            <a href="" class="link">Profile</a>
            <a href="" class="link">About</a>
        </div>
    </nav>

    <div class="inform">
        Sliding Menu
    </div>

    <div class="support">
        <a href="https://twitter.com/DevLoop01" target="_blank"><i class="fab fa-twitter-square"></i></a>
        <a href="https://codepen.io/dev_loop/" target="_blank"><i class="fab fa-codepen"></i></a>
    </div>

    <script>
        var menuBtn = document.querySelector('.menu-btn');
        var nav = document.querySelector('nav');
        var lineOne = document.querySelector('nav .menu-btn .line--1');
        var lineTwo = document.querySelector('nav .menu-btn .line--2');
        var lineThree = document.querySelector('nav .menu-btn .line--3');
        var link = document.querySelector('nav .nav-links');

        menuBtn.addEventListener('click', () => {
            nav.classList.toggle('nav-open');
            lineOne.classList.toggle('line-cross');
            lineTwo.classList.toggle('line-fade-out');
            lineThree.classList.toggle('line-cross');
            link.classList.toggle('fade-in');
        });
    </script>
</body>
</html>
"""
}

# Define functions for different routes
@app.route("/", methods=["GET", "POST"])
def table():
    task_route = "/"
    return handle_task(task_route)

# Common function to handle tasks
def handle_task(task_route):
    task_description = task_descriptions.get(task_route, "")
    conversation = []  # Initialize an empty list to store the conversation history

    if request.method == "POST":
        message = request.form["message"]

        # Add user's message to the conversation
        conversation.append({"role": "user", "content": f"User: {message}"})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": task_description},
                *conversation  # Include the entire conversation history
            ],
            max_tokens=500  # Adjust as needed
        )

        # Modify the AI's reply to preserve spacing
        ai_reply = "<pre>" + response.choices[0].message["content"] + "</pre>"

        # Append AI's reply to the conversation
        conversation.append({"role": "assistant", "content": ai_reply})

        print(ai_reply)

        return render_template("index.html", conversation=conversation, task_description=task_description, task_route=task_route)

    return render_template("index.html", conversation=conversation, task_description=task_description, task_route=task_route)

if __name__ == '__main__':
    app.run(debug=True)
