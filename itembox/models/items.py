from itembox.config import db, ma

class Item(db.Model):
    __tablename__ = 'item'
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True)
    itemof = db.Column(db.String(32))

class ItemSchema(ma.ModelSchema):
    class Meta:
        model = Item
        sqla_session = db.session