import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        userQuestion = request.form["userQ"]
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=generate_prompt(userQuestion),
            temperature=0.6,
            max_tokens=60,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(userQuestion):
    return """Suggest time spot and phone number for an appointment.

schedule: morning
available time: 9AM on September 3 and what is your call back phone number?

schedule: afternoon
available time: 1pm on September 3 and what is your call back phone number?


as soon as possible: call back
what is your phone number?

appointment: I want to book an appointment
The nurse can call you back at 1 pm on September 3, Monday.

appointment: can I book an appointment?
what is your call back phone number and your name?

ok:that works for me
thank you


Phone:{}
""".format(
        userQuestion.capitalize()
    )
