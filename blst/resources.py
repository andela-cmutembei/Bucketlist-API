from flask_restful import Resource, fields, marshal
from flask_restful.reqparse import RequestParser
from blst.api import db
from blst.models import Bucketlist, Item
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound


item_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'date_created': fields.DateTime(dt_format='rfc822'),
    'date_modified': fields.DateTime(dt_format='rfc822'),
    'done': fields.Boolean,
}

bucketlist_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'date_created': fields.DateTime(dt_format='rfc822'),
    'date_modified': fields.DateTime(dt_format='rfc822'),
    'items': fields.List(fields.Nested(item_fields)),
    'created_by': fields.String
}


class AllBucketlists(Resource):
    """Resource for operations on all bucketlists"""

    def get(self):
        bucketlists = Bucketlist.query.all()
        return marshal(bucketlists, bucketlist_fields)

    def post(self):
        parser = RequestParser()
        parser.add_argument('name', type=str, required=True)
        args = parser.parse_args()
        try:
            new_bucketlist = Bucketlist(
                name=args.name, created_by=1
            )
            db.session.add(new_bucketlist)
            db.session.commit()
            return marshal(new_bucketlist, bucketlist_fields)

        except SQLAlchemyError:
            db.session.rollback()
        return {'message': 'Error creating bucketlist'}


class SingleBucketlists(Resource):
    """Resource for operations on a single bucketlists"""

    def get(self, id):
        try:
            bucketlist = Bucketlist.query.filter_by(id=id).one()
            return marshal(bucketlist, bucketlist_fields)
        except NoResultFound:
            return {'message': 'No bucketlist with id {0}'.format(id)}

    def put(self, id):
        parser = RequestParser()
        parser.add_argument('name', type=str, required=True)
        args = parser.parse_args()

        try:
            bucketlist = Bucketlist.query.filter_by(id=id).one()
            bucketlist.name = args.name
            db.session.commit()
            return marshal(bucketlist, bucketlist_fields)
        except NoResultFound:
            return {'message': 'No bucketlist with id {0}'.format(id)}

    def delete(self, id):
        try:
            bucketlist = Bucketlist.query.filter_by(id=id).one()
            db.session.delete(bucketlist)
            db.session.commit()
            return {'message': 'Deleted'}
        except NoResultFound:
            return {'message': 'Error deleting'}


class AllBucketlistItems(Resource):
    """Resource for operations on all items in bucketlists"""

    def post(self, id):
        parser = RequestParser()
        parser.add_argument('name', type=str, required=True)
        args = parser.parse_args()
        try:
            bucketlist = Bucketlist.query.filter_by(id=id).one()
            if bucketlist is not None:
                item = Item(name=args.name, bucketlist_id=id)
                db.session.add(item)
                db.session.commit()
                return marshal(item, item_fields)
        except NoResultFound:
            return {'message': 'No bucketlist with id {0}'.format(id)}


class SingleBucketlistItem(Resource):
    """Resource for operations on a single item in bucketlist"""

    def get(self, id, item_id):
        try:
            bucketlist = Bucketlist.query.filter_by(id=id).one()
            if bucketlist is not None:
                try:
                    item = Item.query.filter_by(id=item_id).one()
                    return marshal(item, item_fields)
                except NoResultFound:
                    return {'message': 'No item with id {0}'.format(item_id)}
        except NoResultFound:
            return {'message': 'No bucketlist with id {0}'.format(id)}

    def put(self, id, item_id):
        parser = RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('done')
        args = parser.parse_args()
        try:
            bucketlist = Bucketlist.query.filter_by(id=id).one()
            if bucketlist is not None:
                try:
                    item = Item.query.filter_by(id=item_id).one()
                    item.name = args.name or item.name
                    item.done = args.done or item.done
                    db.session.add(item)
                    db.session.commit()
                    return marshal(item, item_fields)
                except NoResultFound:
                    return {'message': 'No item with id {0}'.format(item_id)}
            return marshal(item, item_fields)
        except NoResultFound:
            return {'message': 'No bucketlist with id {0}'.format(id)}

    def delete(self, id, item_id):
        try:
            bucketlist = Bucketlist.query.filter_by(id=id).one()
            if bucketlist is not None:
                try:
                    item = Item.query.filter_by(id=item_id).one()
                    db.session.delete(item)
                    db.session.commit()
                    return {'message': 'Deleted'}
                except NoResultFound:
                    return {'message': 'No item with id {0}'.format(item_id)}
        except NoResultFound:
            return {'message': 'No bucketlist with id {0}'.format(id)}