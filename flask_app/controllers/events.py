from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import event, user

@app.route("/events/create")
def create_event():
    if not "id" in session:
        return redirect("/")
    return render_template("new_event.html")

@app.route("/events/add", methods=["POST"])
def add_event():
    if not "id" in session:
        return redirect("/")
    if not event.Event.validate_event(request.form):
        return redirect("/events/create")
    event.Event.create_event(request.form)
    return redirect("/dashboard")

@app.route("/events/<int:id>")
def show_event(id):
    if not "id" in session:
        return redirect("/")
    data = {"id": id}
    this_event = event.Event.get_event_by_id(data)
    return render_template("show_event.html", event = this_event)

@app.route("/events/<int:id>/edit")
def edit_event(id):
    if not "id" in session:
        return redirect("/")
    data = {"id": id}
    this_event = event.Event.get_event_by_id(data)
    return render_template("edit_event.html", event = this_event)