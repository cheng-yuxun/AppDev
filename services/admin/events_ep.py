from datetime import datetime
from PIL import Image
from flask import (
    Blueprint,
    Response,
    flash,
    url_for,
    render_template,
    redirect,
    request,
)
import os
import os.path
import shelve
from data.db_ep import get_db
from data.Events import Onsite, Livestream
from services.forms import form_events
from services.forms.form_search import EventFilter

endpoint = Blueprint("events", __name__)
basedir = os.getcwd()


@endpoint.route("/events", methods=["GET", "POST"])
def events():
    db = shelve.open(get_db(), flag="c")
    events_dict: dict = db["Events"]
    db["Filter_Event"] = {}
    current_dict: dict = db["Filter_Event"]
    db.close()
    events_list = []
    eventfilter = EventFilter(request.form)
    if request.method == "GET":
        if current_dict == {}:
            for key in events_dict:
                events = events_dict.get(key)
                events_list.append(events)
    elif request.method == "POST":
        if (
            request.form.get("onsitecheck") is None
            and request.form.get("livestreamcheck") is None
            and eventfilter.start_date.data is None
            and eventfilter.end_date.data is None
            and eventfilter.status.data == ""
        ):
            return redirect(url_for("events.events"))

        def filter(events):
            if events not in events_list:
                events_list.append(events)

        for key in events_dict:
            events = events_dict.get(key)

            if request.form.get("onsitecheck") is not None or request.form.get("livestreamcheck") is not None:
                if events.get_category() == request.form.get("onsitecheck") or events.get_category() == request.form.get("livestreamcheck"):
                    if eventfilter.start_date.data is not None and eventfilter.end_date.data is not None:
                        if eventfilter.start_date.data <= events.get_date() <= eventfilter.end_date.data:
                            if eventfilter.status.data != '':
                                if events.get_status() == eventfilter.status.data:
                                    filter(events)
                            else:
                                filter(events)
                    else:
                        filter(events)
            else:
                if eventfilter.start_date.data is not None and eventfilter.end_date.data is not None:
                    if eventfilter.start_date.data <= events.get_date() <= eventfilter.end_date.data:
                        if eventfilter.status.data != '':
                            if events.get_status() == eventfilter.status.data:
                                filter(events)
                        else:
                            filter(events)
                else:
                    if eventfilter.status.data != '':
                            if events.get_status() == eventfilter.status.data:
                                filter(events)
                    else:
                        filter(events)

        print(events_list)
    return render_template(
        "admin/events/events.html",
        events_list=events_list,
        count=len(events_list),
        eventfilter=eventfilter,
    )


@endpoint.route("/events/add/onsite", methods=["GET", "POST"])
def onsite_add():
    form = form_events.OnsiteEvents(request.form)
    if request.method == "POST" and form.validate():
        db = shelve.open(get_db(), "w")
        events_dict: dict = db["Events"]
        onsite = Onsite(
            name=form.name.data,
            desc=form.desc.data,
            date=form.date.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            location=form.location.data,
            quantity=form.quantity.data,
            price=form.price.data,
        )
        img = Image.open(request.files["image"])
        img.load()
        img.resize((1200, 600))
        img.convert("RGB")
        img.save(f"{basedir}/static/media/event_img/{onsite.get_uuid()}.png")
        events_dict[onsite.get_uuid()] = onsite
        db["Events"] = events_dict
        db.close()
        flash(
            f"Onsite Event {onsite.get_name()} has been added successfully!",
            category="success",
        )
        return redirect(url_for("events.events"))
    return render_template("admin/events/form_onsite.html", form=form)


@endpoint.route("/events/add/livestream", methods=["GET", "POST"])
def livestream_add():
    form = form_events.LivestreamEvents(request.form)
    if request.method == "POST" and form.validate():
        db = shelve.open(get_db(), "w")
        events_dict: dict = db["Events"]
        livestream = Livestream(
            name=form.name.data,
            desc=form.desc.data,
            date=form.date.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            link=form.link.data,
        )
        img = Image.open(request.files["image"])
        img.load()
        img.resize((1200, 600))
        img.convert("RGB")
        img.save(f"{basedir}/static/media/event_img/{livestream.get_uuid()}.png")
        events_dict[livestream.get_uuid()] = livestream
        db["Events"] = events_dict
        db.close()
        print(f"Livestream Key {livestream.get_uuid()} has been added successfully!")
        return redirect(url_for("events.events"))
    return render_template("admin/events/form_livestream.html", form=form)


@endpoint.route("/admin_events_detail/<id>/", methods=["GET", "POST"])
def events_details(id):
    db = shelve.open(get_db(), "r")
    events_dict: dict = db["Events"]
    db.close()
    events_id = events_dict.get(id)
    print(f"--- Retrieving Event Key {events_id.get_uuid()} Data ---")
    return render_template("admin/admin_eventdetails.html", events_id=events_id)


@endpoint.route("/update/<id>/onsite", methods=["GET", "POST"])
def update_onsiteevents(id):

    form = form_events.UpdateOnsiteEvents(request.form)
    if request.method == "POST" and form.validate():
        db = shelve.open(get_db(), "w")
        events_dict: dict = db["Events"]
        events_id = events_dict.get(id)
        data = {
            "name": form.name.data,
            "desc": form.desc.data,
            "date": form.date.data,
            "start_time": form.start_time.data,
            "end_time": form.end_time.data,
            "quantity": form.quantity.data,
            "price": form.price.data,
        }

        for key, value in data.items():
            if value is not None:
                setattr(events_id, key, value)

        if form.location.data != "empty":
            setattr(events_id, "location", form.location.data)

        if request.files["image"].filename != "":
            img = Image.open(request.files["image"])
            img.load()
            img.resize((1200, 600))
            img.convert("RGB")
            img.save(f"{basedir}/static/media/event_img/{events_id.get_uuid()}.png")
            print("image has been replaced")
        db["Events"] = events_dict
        db.close()
        print(f"Onsite Event Key {events_id.get_uuid()} has been updated successfully!")
    else:
        db = shelve.open(get_db(), "r")
        events_dict: dict = db["Events"]
        db.close()
        events_id = events_dict.get(id)
        form.name.data = events_id.get_name()
        form.desc.data = events_id.get_desc()
        form.date.data = events_id.get_date()
        form.start_time.data = events_id.get_start_time()
        form.end_time.data = events_id.get_end_time()
        form.quantity.data = events_id.get_quantity()
        form.price.data = events_id.get_price()
    return render_template(
        "admin/events/update/update_onsite.html", form=form, events_id=events_id
    )


@endpoint.route("/update/<id>/livestream", methods=["GET", "POST"])
def update_livestreamevents(id):
    db = shelve.open(get_db(), "r")
    events_dict: dict = db["Events"]
    db.close()
    events_id = events_dict.get(id)

    form = form_events.UpdateLivestreamEvents(request.form)
    if request.method == "POST" and form.validate():
        db = shelve.open(get_db(), "w")
        events_dict: dict = db["Events"]
        events_id = events_dict.get(id)
        data = {
            "name": form.name.data,
            "desc": form.desc.data,
            "date": form.date.data,
            "start_time": form.start_time.data,
            "end_time": form.end_time.data,
            "link": form.link.data,
        }

        for key, value in data.items():
            setattr(events_id, key, value)

        if request.files["image"].filename != "":
            img = Image.open(request.files["image"])
            img.load()
            img.resize((1200, 600))
            img.convert("RGB")
            img.save(f"{basedir}/static/media/event_img/{events_id.get_uuid()}.png")
            print("image has been replaced")
        db["Events"] = events_dict
        db.close()
        print(
            f"Livestream Event Key {events_id.get_uuid()} has been updated successfully!"
        )
    else:
        db = shelve.open(get_db(), "r")
        events_dict: dict = db["Events"]
        db.close()
        events = events_dict.get(id)
        form.name.data = events.get_name()
        form.desc.data = events.get_desc()
        form.date.data = events.get_date()
        form.start_time.data = events.get_start_time()
        form.end_time.data = events.get_end_time()
        form.link.data = events.get_link()
    return render_template(
        "admin/events/update/update_livestream.html", form=form, events_id=events_id
    )


@endpoint.route("/delete_event/<id>", methods=["POST"])
def delete_event(id):
    db = shelve.open(get_db(), "w")
    events_dict: dict = db["Events"]
    events_id = events_dict.get(id)
    print(f"Event Key {events_id.get_uuid()} has been deleted successfully!")
    events_dict.pop(id)
    db["Events"] = events_dict
    db.close()
    return redirect(url_for("events.events"))


@endpoint.route("/status_event/<id>", methods=["POST"])
def status_event(id):
    db = shelve.open(get_db(), "w")
    events_dict: dict = db["Events"]
    events_id = events_dict.get(id)
    if events_id.get_status() == "Active":
        print(f"Event Key {events_id.get_uuid()} has been inactivated!")
        events_id.set_status("Inactive")
    else:
        print(f"Event Key {events_id.get_uuid()} has been activated!")
        events_id.set_status("Active")
    db["Events"] = events_dict
    db.close()
    return redirect(request.referrer)


@endpoint.route("/eventstxt/<id>", methods=["POST"])
def eventstxt(id):
    if request.method == "POST":
        db = shelve.open(get_db(), "r")
        events_dict: dict = db["Events"]
        db.close()
        events_id = events_dict.get(id)
        new_line = '\n'
        lines = [f"Event name: {events_id.name}{new_line}Date: {events_id.date}{new_line}Time: {events_id.start_time}-{events_id.end_time}{new_line}Participants: {events_id.user}"]
        return Response(
            lines,
            mimetype="text/plain",
            headers={"Content-Disposition": "attachment; filename=event.txt"},
        )
