from flask import Flask, url_for, render_template, redirect, flash, jsonify, request

from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm

app = Flask(__name__)

app.config['SECRET_KEY'] = "abcdef"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///adopt"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# # Disable intercepting redirects in Flask Debug Toolbar
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)
db.create_all()
app.app_context().push()
toolbar = DebugToolbarExtension(app)

@app.route("/")
def list_pets():
    """List all pets."""

    pets = Pet.query.all()
    print(pets)
 
    return render_template("pet_list.html", pets=pets)


@app.route("/add", methods=["GET", "POST"])
def add_pet():
    """Add a new pet to the database."""

    form = AddPetForm()

    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data
        available = form.available.data

        new_pet = Pet(
            name=name,
            species=species,
            photo_url=photo_url,
            age=age,
            notes=notes,
            available=available,
        )

        db.session.add(new_pet)
        db.session.commit()
        flash("Pet added successfully!", "success")
        return redirect(url_for('list_pets'))  # Redirect to the list_pets route
    else:
    # If the form is not submitted or has validation errors, render the form template
        return render_template("add_pet.html", form=form)

# @app.route("/add", methods=["GET", "POST"])
# def add_pet():
#     """Add a pet."""

#     form = AddPetForm()

#     if form.validate_on_submit():
#         data = {k: v for k, v in form.data.items() if k != "csrf_token"}
#         new_pet = Pet(**data)
#         # new_pet = Pet(name=form.name.data, age=form.age.data, ...)
#         db.session.add(new_pet)
#         db.session.commit()
#         flash(f"{new_pet.name} added.")
#         return redirect(url_for('list_pets'))

#     else:
#         # re-present form for editing
#         return render_template("add_pet.html", form=form)

@app.route("/<int:pet_id>", methods=["GET", "POST"])
def edit_pet(pet_id):
    # Fetch the pet with the given ID from the database
    pet = Pet.query.get_or_404(pet_id)
    
    # Create a form for editing the pet's information
    form = EditPetForm(obj=pet)  # Assuming you have an EditPetForm class
    
    if form.is_submitted() and form.validate():
        # Update the pet's information with the form data
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data
        
        db.session.commit()
        flash(f"{pet.name} updated.")
        return redirect(url_for('list_pets'))
    else:
        # If the form is not submitted or has validation errors, render the form template
        return render_template("pet_edit_form.html", pet=pet, form=form)
