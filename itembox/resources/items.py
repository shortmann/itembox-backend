"""
This is the items module and supports all the ReST actions for the
ITEMS collection
"""

# 3rd party modules
from flask import make_response, abort

from itembox.config import db
from itembox.models.items import Item, ItemSchema


def read_all():
    """
    This function responds to a request for /api/v1/item
    with the complete lists of ITEMS

    :return:        json string of list of items
    """
    # Create the list of items from our data
    items = Item.query.order_by(Item.uid).all()

    # Serialize the data for the response
    item_schema = ItemSchema(many=True)
    return item_schema.dump(items)


def read_one(uid):
    """
    This function responds to a request for /api/v1/items/{uid}
    with one matching item from ITEMS

    :param uid:     uid of item to find
    :return:        item matching uid
    """
    # Get the person requested
    item = Item.query.filter(Item.uid == uid).one_or_none()

    # Did we find a person?
    if item is not None:

        # Serialize the data for the response
        item_schema = ItemSchema()
        return item_schema.dump(item)


    # otherwise, nope, not found
    else:
        abort(
            404, "item with uid {uid} not found".format(uid=uid)
        )

    return item


def create(item):
    """
    This function creates a new item in the ITEMS structure
    based on the passed in item data

    :param item:    item to create in ITEMS structure
    :return:        201 on success, 406 on item exists
    """
    name = item.get("name")
    itemof = item.get("itemof")

    existing_item = (
        Item.query.filter(Item.name == name)
        .filter(Item.itemof == itemof)
        .one_or_none()
    )

    # Can we insert this item?
    if existing_item is None:

        # Create a person instance using the schema and the passed in item
        schema = ItemSchema()
        new_item = schema.load(item, session=db.session)

        # Add the person to the database
        db.session.add(new_item)
        db.session.commit()

        # Serialize and return the newly created item in the response
        data = schema.dump(new_item)

        return data, 201

    # Otherwise, they exist, that's an error
    else:
        abort(
            406,
            "Item with uid {uid} already exists".format(uid=uid),
        )


def update(uid, item):
    """
    This function updates an existing item in the ITEMS structure

    :param uid:   uid of item to update in the ITEMS structure
    :param item:  item to update
    :return:      updated item structure
    """
    # Get the item requested from the db into session
    update_item = Item.query.filter(
        Item.uid == uid
    ).one_or_none()

    # Try to find an existing item with the same name as the update
    name = item.get("name")
    itemof = item.get("itemof")

    existing_item = (
        Item.query.filter(Item.name == name)
        .filter(Item.itemof == itemof)
        .one_or_none()
    )

    # Are we trying to find a item that does not exist?
    if update_item is None:
        abort(
            404,
            "Item not found for Id: {uid}".format(uid=uid),
        )

    # Would our update create a duplicate of another item already existing?
    elif (
        existing_item is not None and existing_item.uid != uid
    ):
        abort(
            409,
            "Item {name} exists already".format(
                name=name
            ),
        )

    # Otherwise go ahead and update!
    else:

        # turn the passed in item into a db object
        schema = ItemSchema()
        update = schema.load(item, session=db.session)

        # Set the id to the item we want to update
        update.uid = update_item.uid

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated item in the response
        data = schema.dump(update_item)

        return data, 200


def delete(uid):
    """
    This function deletes a item from the ITEMS structure

    :param uid:   uid of item to delete
    :return:      200 on successful delete, 404 if not found
    """
    # Get the item requested
    item = Item.query.filter(Item.uid == uid).one_or_none()

    # Did we find a item?
    if item is not None:
        db.session.delete(item)
        db.session.commit()
        return make_response(
            "Item {uid} deleted".format(uid=uid), 200
        )

    # Otherwise, nope, item to delete not found
    else:
        abort(
            404, "Item with uid {uid} not found".format(uid=uid)
        )