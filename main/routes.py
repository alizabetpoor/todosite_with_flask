from main import app,bcrypt,db,mail
from flask_mail import Message
from main.models import User,Post
import os,secrets
from PIL import Image
from flask_login import login_user,login_required,logout_user,current_user
from flask import render_template,url_for,flash,redirect,request,abort
from main.forms import login_form,register_form,newpost_form,edit_post_form,edit_profile_form,sendmail_form
from main.forms import searchposts_form,searchusers_form
def send_email(user):
    token=user.get_verify_token()
    msg=Message("email confrim",sender="alizabetpoor80@gmail.com",recipients=[user.email])
    msg.body=f'''
        برای فعالسازی اکانت خود روی لینک زیر کلیک کنید.
        <a href='{url_for("verifyemail",token=token,_external=True)}'>click to activate</a>
    '''
    mail.send(msg)
@app.route("/verify/<token>",methods=["GET","POST"])
def verifyemail(token):
    user=User.check_verify(token)
    if user==None:
        flash("مشکلی پیش امده لطفا به پشتیبانی اطلاع دهید",category="danger")
        return redirect(url_for("index"))
    else:
        if user.verify==True:
            flash("ایمیل شما قبلا تایید شده است.",category="success")
            return redirect(url_for("index"))
        else:
            user.verify=True
            db.session.commit()
            flash("ایمیل شما با موفقیت تایید شد",category="success")
            return redirect(url_for("index"))
@app.route('/',methods=["POST","GET"])
def index():
    lform=login_form()
    rform=register_form()
    nform=newpost_form()
    if lform.lsubmit.data and lform.validate_on_submit():
        user=User.query.filter_by(email=lform.lemail.data).first()
        if user and bcrypt.check_password_hash(user.password,lform.lpassword.data):

            login_user(user)
            nextpage = request.args.get("next")
            flash("شما وارد شدید",category="success")
            if nextpage:
                return redirect(nextpage)
            else:
                return redirect(url_for("index"))
        else:
            flash("ایمیل و پسورد را دوباره چک کنید",category="danger")
            return redirect(url_for("index"))
    if rform.rsubmit.data and rform.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(rform.rpassword.data)
        user=User(firstname=rform.firstname.data,lastname=rform.lastname.data,email=rform.remail.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        # send_email(user)
        flash("ثبت نام شما با موفقیت انجام شد.",category="success")
        return redirect(url_for("index"))
    if current_user.is_authenticated==True:
        postslen=len(current_user.posts)
        page=request.args.get("page",1,int)
        posts=Post.query.filter_by(author=current_user).order_by(Post.id.desc()).paginate(page=page,per_page=5)
    else:
        postslen=0
        posts=None
    if nform.nsubmit.data and nform.validate_on_submit():
        post=Post(title=nform.title.data,date=nform.date.data,time=nform.time.data,user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash("پست شما افزوده شد",category="success")
        return redirect(url_for("index"))
    return render_template("index.html",lform=lform,rform=rform,nform=nform,title="صفحه اصلی",posts=posts,postslen=postslen)
# @app.route('/account')
# def account():
#     return render_template("account.html")
@app.route("/editpost/<int:postid>",methods=["GET","POST"])
@login_required
def editpost(postid):
    form=edit_post_form()
    getpost=Post.query.get_or_404(postid)
    if getpost.author!=current_user:
        abort(403)
    if form.validate_on_submit():
        getpost.title=form.title.data
        getpost.date=form.date.data
        getpost.time=form.time.data
        db.session.commit()
        flash("پست شما ویرایش شد.",category="success")
        return redirect(url_for("index"))
    elif request.method=="GET":
        form.title.data=getpost.title
        form.date.data=getpost.date
        form.time.data=getpost.time
    return render_template("editpost.html",form=form,post=getpost,title=f"ویرایش پست {getpost.id}")
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("index"))
@app.route('/deletepost/<int:postid>',methods=["GET"])
@login_required
def deletepost(postid):
    post=Post.query.get_or_404(postid)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("پست شما حذف شد.",category="success")
    return redirect(url_for("index"))
def save_pic(pic):
    randomname=secrets.token_hex(8)
    _,f_ext=os.path.splitext(pic.filename)
    picname=randomname+f_ext
    picpath=os.path.join(app.root_path,"static/images",picname)
    output_size=(125,125)
    i=Image.open(pic)
    i.thumbnail(output_size)
    i.save(picpath)
    oldpic=os.path.join(app.root_path,"static/images",current_user.profile_image)
    if os.path.exists(oldpic) and os.path.basename(oldpic) != "39348396.png":
        os.remove(oldpic)
    return picname
@app.route("/profile",methods=["GET","POST"])
@login_required
def editprofile():
    form=edit_profile_form()
    formemail=sendmail_form()
    if form.submit.data and form.validate_on_submit():
        if form.picture.data:
            picname=save_pic(form.picture.data)
            current_user.profile_image=picname
        current_user.firstname=form.firstname.data
        current_user.lastname=form.lastname.data
        db.session.commit()
        flash("اطلاعات شما ویرایش شد",category="success")
        return redirect(url_for("editprofile"))
    elif request.method=="GET":
        form.firstname.data=current_user.firstname
        form.lastname.data=current_user.lastname
        form.email.data=current_user.email
    print(formemail.validate_on_submit())
    if formemail.sendemail.data and formemail.validate_on_submit():
        send_email(current_user)
        flash("ایمیل تایید برای شما فرستاده شد.",category="success")
        return redirect(url_for("editprofile"))

    return render_template("account.html",form=form,title="پروفایل",sendmail=formemail)
@app.route("/adminpanel/users",methods=["POST","GET"])
def adminpanel_users():
    if current_user.isadmin==False:
        abort(403)
    form=searchusers_form()
    if form.validate_on_submit():
        return redirect(url_for("searchuser",user=form.search.data))
    usersearchcon=False
    page=request.args.get("page",1,int)
    users=User.query.paginate(page=page,per_page=10)
    return render_template("admin.html",users=users,title="پنل ادمین-یوزرها",con=usersearchcon,form=form)
@app.route("/adminpanel/users/<string:user>")
def searchuser(user):
    form=searchusers_form()
    usersearchcon=True
    users=User.query.filter_by(email=user).paginate()
    if len(users.items)==0:
        abort(404)
    return render_template("admin.html",con=usersearchcon,users=users,form=form,title=users.items[0].lastname)
@app.route("/adminpanel/posts",methods=["POST","GET"])
def adminpanel_posts():
    if current_user.isadmin==False:
        abort(403)
    showuserpostscon=False
    form = searchposts_form()
    if form.validate_on_submit():
        return redirect(url_for("showuserposts",userlastname=form.search.data))
    page=request.args.get("page",1,int)
    posts=Post.query.paginate(page=page,per_page=10)
    return render_template("admin.html",posts=posts,title="پنل ادمین-پست ها",form=form,con=showuserpostscon)
@app.route("/adminpanel/posts/<string:userlastname>",methods=["GET","POST"])
def showuserposts(userlastname):
    showuserpostscon=True
    form=searchposts_form()
    page=request.args.get("page",1,int)
    user = User.query.filter_by(lastname=userlastname).first_or_404()
    posts = Post.query.filter_by(user_id=user.id).paginate(page=page, per_page=5)
    return render_template("admin.html",posts=posts,form=form,con=showuserpostscon,user=user,title=f" پست های {user.lastname}")
@app.route("/adminpanel/deleteuser/<int:userid>")
@login_required
def deleteuser(userid):
    if current_user.isadmin==False:
        abort(403)
    user=User.query.get_or_404(userid)
    if user.isadmin==False:
        db.session.delete(user)
        db.session.commit()
        flash("یوزر با موفقیت حذف شد.", category="success")
        return redirect(url_for("adminpanel_users"))
    else:
        flash("شما نمیتوانید ادمین را حذف کنید.",category="danger")
        return redirect(url_for("adminpanel_users"))
@app.route("/adminpanel/deletepost/<int:postid>")
@login_required
def deletepostbyadmin(postid):
    if current_user.isadmin==False:
        abort(403)
    post=Post.query.get_or_404(postid)
    db.session.delete(post)
    db.session.commit()
    flash("پست با موفقیت حذف شد",category="success")
    return redirect(url_for("adminpanel_posts"))

