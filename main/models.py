from main import db,login_manager,app
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as serializer
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    firstname=db.Column(db.String(20),nullable=False)
    lastname=db.Column(db.String(20),nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)
    profile_image=db.Column(db.String(20),nullable=False,default="39348396.png")
    password=db.Column(db.String(60),nullable=False)
    verify=db.Column(db.Boolean,nullable=False,default=False)
    isadmin=db.Column(db.Boolean,nullable=False,default=False)
    posts=db.relationship("Post",backref="author",lazy=True)
    def get_verify_token(self,expiretime=3000):
        s=serializer(app.config['SECRET_KEY'],expiretime)
        print(self.id)
        return s.dumps({"user_id":self.id}).decode("utf-8")
    @staticmethod
    def check_verify(token):
        s = serializer(app.config['SECRET_KEY'])
        try:
            userid=s.loads(token)["user_id"]
        except Exception as e:
            print(e)
            return None
        return User.query.get(userid)
    def __repr__(self):
        return f"User('{self.email}','{self.firstname}','{self.lastname}')"
class Post(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(60),nullable=False)
    date=db.Column(db.Date,nullable=False,default=datetime.utcnow)
    time=db.Column(db.Time,nullable=False,default=datetime.now().time())
    user_id=db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    def __repr__(self):
        return f"Post('{self.title}','{self.date}','{self.time}')"