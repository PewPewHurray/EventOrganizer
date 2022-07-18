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
    event.Event.add_event(request.form)
    return redirect("/dashboard")

@app.route("/events/<int:id>")
def show_event(id):
    if not "id" in session:
        return redirect("/")
    this_event = event.Event.get_event_by_id_with_participants({"id": id})
    participant = None
    if not session["id"] == this_event.coordinator.id:
        if session["id"] in this_event.participants_ids:
            participant = True
        else:
            participant = False
    this_event.date_time = this_event.date_time.strftime("%B %d, %Y at %I:%M %p")
    return render_template("show_event.html", event = this_event, participant = participant)

@app.route("/events/<int:id>/edit")
def edit_event(id):
    if not "id" in session:
        return redirect("/")
    this_event = event.Event.get_event_by_id({"id": id})
    return render_template("edit_event.html", event = this_event)

@app.route("/events/<int:id>/update", methods=["POST"])
def update_event(id):
    if not "id" in session:
        return redirect("/")
    if not event.Event.validate_event(request.form):
        this_event = event.Event.get_event_by_id({"id": id})
        return render_template("edit_event.html", event = this_event)
    event.Event.update_event(request.form)
    return redirect("/events/"+str(id))

@app.route("/events/<int:id>/destroy")
def destroy_event(id):
    if not "id" in session:
        return redirect("/")
    event.Event.destroy_event({"id": id})
    return redirect("/dashboard")

@app.route("/events/<int:id>/add_participant", methods=["POST"])
def add_participant(id):
    if not "id" in session:
        return redirect("/")
    event.Event.add_particaipant(request.form)
    return redirect("/events/"+str(id))

@app.route("/events/<int:id>/destroy_participant")
def destroy_participant(id):
    if not "id" in session:
        return redirect("/")
    data = {
        "user_id": session["id"],
        "event_id": id
    }
    event.Event.destroy_particaipant(data)
    return redirect("/events/"+str(id))