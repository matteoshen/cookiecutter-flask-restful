from {{cookiecutter.app_name}}.extensions import db, pwd_context


class User(db.Model):
    """Basic user model
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    username_cn = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"), nullable=False)
    active = db.Column(db.Boolean, default=True)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.password = pwd_context.hash(self.password)

    def __repr__(self):
        return "<User %s>" % self.username


class Role(db.Model):
    """Basic role model
    """

    id = db.Column(db.Integer, primary_key=True)
    rolename = db.Column(db.String(80), unique=True, nullable=False)
    rolename_cn = db.Column(db.String(80), unique=True, nullable=False)
    users = db.relationship("User", backref="role", lazy=True)

    def __repr__(self):
        return "<Role %s>" % self.rolename
