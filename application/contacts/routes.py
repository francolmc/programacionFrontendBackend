from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from application.extensions import db
from application.contacts.models import Contact

contacts_blueprint = Blueprint("contacts", __name__, url_prefix="/api")

@contacts_blueprint.route("/contacts", methods=["GET"])
@cross_origin()
def get_contacts():
    contacts = Contact.query.all()
    return jsonify([{ "id": contact.id, 'first_name': contact.first_name, 'last_name': contact.last_name, 'email': contact.email } for contact in contacts])

@contacts_blueprint.route("/contacts/<int:contact_id>", methods=["GET"])
@cross_origin()
def get_contact_by_id(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    return jsonify({
        "id": contact.id,
        "first_name": contact.first_name,
        "last_name": contact.last_name,
        "email": contact.email
    })

@contacts_blueprint.route("/contacts/search", methods=["GET"])
@cross_origin()
def search_contacts():
    search_text = request.args.get("q")
    if not search_text:
        return jsonify({"message": "Debes proporcionar un texto de búsqueda"}), 400

    contacts = Contact.query.filter(
        (Contact.first_name.ilike(f"%{search_text}%")) | (Contact.last_name.ilike(f"%{search_text}%") | (Contact.email.ilike(f"%{search_text}%")))
    ).all()

    if not contacts:
        return jsonify({"message": "No contacts matched the search were found"}), 404

    contact_data = [
        {
            "id": contact.id,
            "first_name": contact.first_name,
            "last_name": contact.last_name,
            "email": contact.email,
        }
        for contact in contacts
    ]
    return jsonify(contact_data)


@contacts_blueprint.route("/contacts", methods=["POST"])
@cross_origin()
def create_contact():
    data = request.get_json()
    new_contact = Contact(
    first_name=data["first_name"],
    last_name=data["last_name"],
    email=data["email"])
    db.session.add(new_contact)
    db.session.commit()
    return jsonify({
        "message": "Contact created successfully"
    }), 201

@contacts_blueprint.route("/contacts/<int:contact_id>", methods=["PUT"])
@cross_origin()
def update_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    data = request.get_json()
    contact.first_name = data.get("first_name", contact.first_name)
    contact.last_name = data.get("last_name", contact.last_name)
    contact.email = data.get("email", contact.email)
    db.session.commit()
    return jsonify({
        "message": "Contact updated successfully"
    })

@contacts_blueprint.route("/contacts/<int:contact_id>", methods=["DELETE"])
@cross_origin()
def delete_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    db.session.delete(contact)
    db.session.commit()
    return jsonify({
        "message": "Contact deleted successfully"
    })