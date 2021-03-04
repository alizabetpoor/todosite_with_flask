from flask_wtf import FlaskForm
from flask_login import current_user
from flask_wtf.file import FileField,FileAllowed
from main.models import User
from main import bcrypt
from wtforms import StringField,PasswordField,SubmitField,DateField,TimeField,HiddenField
from wtforms.validators import Length,DataRequired,Email,EqualTo,ValidationError,optional
class login_form(FlaskForm):
    lemail=StringField("email",validators=[DataRequired("این فیلد باید پرشود"),Email("ایمیل خود را به درستی وارد کنید.")],render_kw={'placeholder':'email'})
    lpassword=PasswordField("password",validators=[DataRequired("این فیلد باید پرشود")],render_kw={"placeholder":"password"})
    lsubmit=SubmitField("login")
class register_form(FlaskForm):
    firstname=StringField("firstname",validators=[DataRequired("این فیلد باید پرشود"),Length(3,10,"نام شما باید بین 3 تا 10 کاراکتر باشد")],render_kw={"placeholder":"firstname"})
    lastname=StringField("lastname",validators=[DataRequired("این فیلد باید پرشود"),Length(3,15,"نام شما باید بین 3 تا 15 کاراکتر باشد")],render_kw={"placeholder":"lastname"})
    remail=StringField("email",validators=[DataRequired("این فیلد باید پرشود"),Length(5,30,"نام شما باید بین 5 تا 30 کاراکتر باشد"),Email("ایمیل خود را به درستی وارد کنید.")],render_kw={"placeholder":"email"})
    rpassword=PasswordField("password",validators=[DataRequired("این فیلد باید پرشود")],render_kw={"placeholder":"password"})
    confrim_password=PasswordField("confrim password",validators=[DataRequired("این فیلد باید پرشود"),EqualTo("rpassword","پسورد های وارد شده مطابقت ندارد")],render_kw={"placeholder":"confrim password"})
    rsubmit=SubmitField("ثبت نام")
    def validate_remail(self,remail):
        email=User.query.filter_by(email=remail.data).first()
        if email:
            raise ValidationError("این ایمیل در سایت موجود است.")
class newpost_form(FlaskForm):
    title=StringField("onvan",validators=[DataRequired("این فیلد باید پر شود"),Length(3,25,"تعداد کاراکتر باید بین 3 تا 25 باشد")],render_kw={"placeholder":"عنوان"})
    date=DateField("date",validators=[DataRequired()],render_kw={"type":"date"})
    time=TimeField("time",validators=[DataRequired()],render_kw={"type":"time","id":"timeinput"})
    nsubmit=SubmitField("افزودن")
class edit_post_form(FlaskForm):
    title = StringField("onvan", validators=[DataRequired("این فیلد باید پر شود"),
                                             Length(3, 25, "تعداد کاراکتر باید بین 3 تا 25 باشد")],
                        render_kw={"placeholder": "عنوان","id":"edit-post-text"})
    date = DateField("date", validators=[DataRequired()], render_kw={"type": "date"})
    time = TimeField("time", validators=[DataRequired()], render_kw={"type": "time", "id": "timeinput"})
    submit = SubmitField("ویرایش")
class edit_profile_form(FlaskForm):
    firstname = StringField("نام", validators=[DataRequired("این فیلد باید پرشود"),
                                                     Length(3, 10, "نام شما باید بین 3 تا 10 کاراکتر باشد")],
                            render_kw={"placeholder": "firstname","id":"first-name"})
    lastname = StringField("نام خانوادگی", validators=[DataRequired("این فیلد باید پرشود"),
                                                   Length(3, 15, "نام شما باید بین 3 تا 15 کاراکتر باشد")],
                           render_kw={"placeholder": "lastname","id":"last-name"})
    email = StringField("ایمیل",render_kw={"placeholder": "email","id":"email"})

    picture=FileField("آپلود عکس پروفایل",validators=[FileAllowed(["jpg","png"])],render_kw={"id":"profile-photo"})
    password = PasswordField("پسورد", validators=[DataRequired("این فیلد باید پرشود")])
    submit=SubmitField("ویرایش")

    def validate_password(self,password):
        if bcrypt.check_password_hash(current_user.password,password.data)==False:
            raise ValidationError("پسورد شما درست نمی باشد.")
class sendmail_form(FlaskForm):
    hidden=HiddenField("nothing")
    sendemail=SubmitField(" فرستادن ایمیل تایید")
class searchposts_form(FlaskForm):
    search=StringField("اسم نویسنده",validators=[DataRequired("این فیلد باید پر شود")],render_kw={"placeholder":"نام خانوادگی نویسنده"})
    submit=SubmitField("search")
class searchusers_form(FlaskForm):
    search=StringField("اسم نویسنده",validators=[DataRequired("این فیلد باید پر شود")],render_kw={"placeholder":"ایمیل فرد "})
    submit=SubmitField("search")