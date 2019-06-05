# For more details, see
# http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#declare-a-mapping
from anthill.framework.db import db
from anthill.framework.utils import timezone
from anthill.framework.utils.translation import translate as _
from anthill.platform.api.internal import InternalAPIMixin
from anthill.platform.auth import RemoteUser
from sqlalchemy_utils.types import JSONType


class Market(db.Model):
    __tablename__ = 'markets'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=True)
    title = db.Column(db.String(512), nullable=True)
    enabled = db.Column(db.Boolean, nullable=False, default=True)
    sellers = db.relationship('Seller', backref='market', lazy='dynamic')
    items = db.relationship('Item', backref='market', lazy='dynamic')


class Seller(InternalAPIMixin, db.Model):
    __tablename__ = 'sellers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False, unique=True)
    market_id = db.Column(db.Integer, db.ForeignKey('markets.id'))
    enabled = db.Column(db.Boolean, nullable=False, default=True)

    async def get_user(self) -> RemoteUser:
        data = await self.internal_request('login', 'get_user', user_id=self.user_id)
        return RemoteUser(**data)


class Item(InternalAPIMixin, db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    market_id = db.Column(db.Integer, db.ForeignKey('markets.id'))
    orders = db.relationship('Order', backref='item', lazy='dynamic')
    created = db.Column(db.DateTime, default=timezone.now)
    payload = db.Column(JSONType, nullable=False, default={})
    price = db.Column(JSONType, nullable=False, default={})
    enabled = db.Column(db.Boolean, nullable=False, default=True)

    async def get_user(self) -> RemoteUser:
        data = await self.internal_request('login', 'get_user', user_id=self.user_id)
        return RemoteUser(**data)


class Order(InternalAPIMixin, db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    created = db.Column(db.DateTime, default=timezone.now)

    async def get_user(self) -> RemoteUser:
        data = await self.internal_request('login', 'get_user', user_id=self.user_id)
        return RemoteUser(**data)

