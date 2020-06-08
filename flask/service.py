from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from flask import Flask, request, jsonify, redirect, Response, render_template
import json, os, sys 
sys.path.append('./data')
import prepare_data

# Connect to our local MongoDB
mongodb_hostname = os.environ.get("MONGO_HOSTNAME","localhost")
client = MongoClient('mongodb://'+'192.168.99.100'+':27017/')
# Choose InfoSys database
db = client['InfoSys']
students = db['Students']
users = db['Users']
movies = db['Movies']
# Initiate Flask App
app = Flask(__name__)
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.INFO)

#check data existence
def check_data():
    try:
        if users.count_documents({}) == 0:
            prepare_data.insert_all_users()
    except Exception as e:
        print(e)
        raise e
    try:
        if movies.count_documents({}) == 0:
            prepare_data.insert_all_movies()
    except Exception as e:
        print(e)
        raise e


# Access level ENUM          
ACCESS = {
    'guest': 0,
    'user': 1,
    'admin': 2
}

# Access Control
def is_admin(mail):
    try:
        usr = users.find_one({'email': mail})
        return usr['access'] == str(ACCESS['admin']) or usr['access'] == (ACCESS['admin'])
    except Exception:
        return Response({'is_admin Function error'},status=500,mimetype='application/json')
    
def is_loggedin(mail):
    try:
        usr = users.find_one({'email': mail})
        return usr['loggedin'] == "1"
    except Exception:
        return Response({'is_loggedin Function error'},status=500,mimetype='application/json')
    

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# User Endpoints

# Register User
@app.route('/register', methods=['GET','POST'])
def register_user():
    # Request JSON data
    data = None 
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        try:
            data = request.form.to_dict(flat=True)
        except Exception:
            return Response("Bad form content",status=500,mimetype='application/json')
        #try:
        #    data = json.loads(request.data)
        #except Exception:
        #    return Response("bad json content",status=500,mimetype='application/json')
        if data == None:
            return Response("bad request",status=500,mimetype='application/json')
        if not "name" in data or not "email" in data or not "password" in data:
            return Response("Information incomplete",status=500,mimetype="application/json")
        
        if users.count_documents({"email":data["email"]}) < 1 :
            try: 
                usr = {"name": data['name'], "email": data['email'], "password": data['password'], "comments": [], "access": ACCESS['user'], "loggedin": "0"}
                # Add user to the 'users' collection
                users.insert_one(usr)
                #return Response(data['name']+" was added to the MongoDB",status=200,mimetype='application/json') 
                return render_template('register_out.html', name=data['name'], email=data['email'], password=data['password'])
            except Exception :
                return Response({'Could not make any changes'},status=500,mimetype='application/json')
        else:
            return Response("A user with the given email already exists",status=200,mimetype='application/json')

# Logout user
@app.route('/logout', methods=['GET','POST'])
def logout_user():
    data = None 
    if request.method == 'GET':
        return render_template('logout.html')
    if request.method == 'POST':
        try:
            data = request.form.to_dict(flat=True)
        except Exception:
            return Response("Bad form content",status=500,mimetype='application/json')
        #try:
        #    data = json.loads(request.data)
        #except Exception:
        #    return Response("bad json content",status=500,mimetype='application/json')
        if data == None:
            return Response("bad request",status=500,mimetype='application/json')
        if not "email" in data or not "password" in data:
            return Response("Wrong key.",status=500,mimetype="application/json")
        if users.count_documents({"email":data["email"]}) < 1 :
            return Response("A user with the given email doesn't exist, please register first.",status=200,mimetype='application/json') 
        usr = users.find_one({"email": data['email']})
        if usr['password'] != data['password']:
            return Response("Wrong password, try again",status=200,mimetype='application/json')
        if usr['loggedin'] == "1":
            try:
                ud = { "$set": {"loggedin": "0" } }
                users.update_one(usr, ud)
                return Response("Logout successful! ",status=200,mimetype='application/json')
            except Exception:
                return Response({'Could not make any changes'},status=500,mimetype='application/json')
        else:
            return Response("User is currently logged out.",status=200,mimetype='application/json')

# Log in user
@app.route('/login', methods=['GET','POST'])
def login_user():
    data = None 
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        try:
            data = request.form.to_dict(flat=True)
        except Exception:
            return Response("Bad form content",status=500,mimetype='application/json')
        #try:
        #    data = json.loads(request.data)
        #except Exception:
        #    return Response("bad json content",status=500,mimetype='application/json')
        if data == None:
            return Response("bad request",status=500,mimetype='application/json')
        if not "email" in data or not "password" in data:
            return Response("Information incomplete",status=500,mimetype="application/json")
        if users.count_documents({"email":data["email"]}) < 1 :
            return Response("A user with the given email doesn't exist, please register first.",status=200,mimetype='application/json') 
        if users.find_one({"email": data['email']})['loggedin'] == "1" :
            return Response("User is already logged in from another computer, please log out first")
        try:
            usr = users.find_one({"email": data['email']})
            if usr['password'] == data['password']:
                ud = { "$set": {"loggedin": "1" } }
                users.update_one(usr, ud)
                return Response("Login successful! ",status=200,mimetype='application/json') 
        except Exception :
            return Response({'Could not make any changes'},status=500,mimetype='application/json')
        return Response("Incorrect password. Please try logging in again",status=200,mimetype='application/json')   

# Find movies
@app.route('/moviesby', methods=['GET', 'POST'])
def movies_by():
    if request.method == 'GET' :
        return render_template('moviesby.html')
    if request.method == 'POST' :
        try:
            title = request.form.get('title')
            year = request.form.get('year')
            actor = request.form.get('actor')
            if title != '' :
                return redirect("/moviesbytitle/"+title)
            if year != '' :
                return redirect("/moviesbyyear/"+str(year))
            if actor != '' :
                return redirect("/moviesbyactor/"+actor)
            return Response("No fields inserted, try again.",status=500,mimetype='application/json')
        except Exception:
            return Response("Bad form content",status=500,mimetype='application/json')

# By title
@app.route('/moviesbytitle/<string:title>', methods=['GET'])
def movies_by_title(title):
    if title == None:
        return Response("Bad request", status=500, mimetype='application/json')
    test = movies.find_one({"title":title})
    if test == None:
        return Response('No movie found with the title '+ title +' was found',status=200,mimetype='application/json')
    try:
        iterable = movies.find({"title":title})
        output = []
        for mov in iterable:
            mov['_id'] = None 
            output.append(mov)
        return jsonify(output)
    except Exception:
        return Response({'Could not make any changes'},status=500,mimetype='application/json')

# By year
@app.route('/moviesbyyear/<int:year>', methods=['GET'])
def movies_by_year(year):
    if year == None:
        return Response("Bad request", status=500, mimetype='application/json')
    test = movies.find_one({"year": year})
    if test == None:
        return Response('No movie published on '+ str(year) +' was found',status=200,mimetype='application/json')
    try:    
        iterable = movies.find({"year": year})
        output = []
        for mov in iterable:
            mov['_id'] = None 
            output.append(mov)
        return jsonify(output)
    except Exception:
        return Response({'Could not make any changes'},status=500,mimetype='application/json')
    
# By actors
@app.route('/moviesbyactor/<string:actor>', methods=['GET'])
def movies_by_actor(actor):
    if actor == None:
        return Response("Bad request", status=500, mimetype='application/json')
    test = movies.find_one({"actors": {"name": actor}})
    if test == None:
        return Response('No movie starring '+ actor +' was found',status=200,mimetype='application/json')
    try:
        iterable = movies.find({"actors": {"name": actor}})
        output = []
        for mov in iterable:
            mov['_id'] = None 
            output.append(mov)
        return jsonify(output)
    except Exception:
        return Response({'Could not make any changes'},status=500,mimetype='application/json')

#Movie
@app.route('/getinfo', methods=['GET'])
def movie():
    return render_template('info.html')

# Movie info 
@app.route('/movie', methods=['POST'])
def get_movie_info():
    try:
        title = request.form['title']
        mov = movies.find_one({"title": title})
        if mov == None:
            return Response('No movie found with the title '+ title +' was found',status=200,mimetype='application/json')
        movie = {"title": mov['title'], "year": mov['year'], "description": mov['description'], "actors": mov['actors']}
        return jsonify(movie)
    except Exception:
        return Response({'Could not make any changes'},status=500,mimetype='application/json')

# Movie comments
@app.route('/comments', methods=['POST'])
def get_movie_comments():
    try:
        title = request.form['title']
        mov = movies.find_one({"title": title})
        if mov == None:
            return Response('No movie found with the title '+ title +' was found',status=200,mimetype='application/json')
        comments = mov['comments']
        if comments :
            return jsonify(comments)
        else :
            return Response({'There are no comments on this movie yet, be the first one to comment!'},status=200,mimetype='application/json')
    except Exception:
        return Response({'Could not make any changes'},status=500,mimetype='application/json')

# Add Rating
@app.route('/addrating', methods=['GET','POST'])
def add_rating():
    data = None 
    if request.method == 'GET':
        return render_template('addrating.html')
    if request.method == 'POST':
        try:
            data = request.form.to_dict(flat=True)
        except Exception:
            return Response("Bad form content",status=500,mimetype='application/json')
        #try:
        #    data = json.loads(request.data)
        #except Exception:
        #    return Response("bad json content",status=500,mimetype='application/json')
        if data == None:
            return Response("bad request",status=500,mimetype='application/json')
        if not "email" in data or not "title" in data or not "year" in data or not "rating" in data:
            return Response("Information incomplete",status=500,mimetype="application/json")
        if not is_loggedin(data['email']):
            return Response("You must be logged in to perform this action",status=401,mimetype='application/json')  
        if users.count_documents({"email":data["email"]}) < 1 :
            return Response("A user with the given email doesn't exist, please register first.",status=200,mimetype='application/json') 
        movie = movies.find_one({"title": data['title'], "year": int(data['year'])})
        if movie == None:
            return Response('No movie found with the title '+ data['title'] +' published on '+data['year']+ ' was found',status=200,mimetype='application/json')
        try:
            ratings = movie['ratings']
            found = 0
            for r in ratings :
                if r['email']==data['email']:
                    found = 1
            if found == 1 :        
                return Response("User has already rated this movie",status=200,mimetype="application/json")
                        
            newrate = {"email": data['email'], "rate": float(data['rating'])}
            ratings.append(newrate)
            query = {"title": data['title'], "year":  int(data['year'])}
            movie = movies.find_one(query)
            ud = { "$set": {"ratings": ratings } }
            movies.update_one(query, ud)
            total = movie['totalratings']
            movierating = movie['rating']
            if movierating != -1:
                movieratingafter = movierating + ( float(data['rating']) - movierating) / (total + 1)
            else:
                movieratingafter = float(data['rating'])
            #adding a value in average of sum of n: 
            #s' = s + (value -s) /n+1
            #https://math.stackexchange.com/questions/22348/how-to-add-and-subtract-values-from-an-average
            movies.update_one(query, { "$set": {"rating": round(movieratingafter,1)} })
            total += 1
            movies.update_one(query, { "$set": {"totalratings": total} })
            return Response({'Rating successfully added'},status=200,mimetype='application/json')
        except Exception:
            return Response({'Could not make any changes'},status=500,mimetype='application/json')

# Remove Own Rating
@app.route('/removerating', methods=['GET','POST'])
def rem_rating():
    data = None 
    if request.method == 'GET':
        return render_template('removerating.html')
    if request.method == 'POST':
        try:
            data = request.form.to_dict(flat=True)
        except Exception:
            return Response("Bad form content",status=500,mimetype='application/json')
        #try:
        #    data = json.loads(request.data)
        #except Exception:
        #    return Response("bad json content",status=500,mimetype='application/json')
        if data == None:
            return Response("bad request",status=500,mimetype='application/json')
        if not "email" in data or not "title" in data or not "year" in data:
            return Response("Information incomplete",status=500,mimetype="application/json")
        if not is_loggedin(data['email']):
            return Response("You must be logged in to perform this action",status=401,mimetype='application/json')  
        if users.count_documents({"email":data["email"]}) < 1 :
            return Response("A user with the given email doesn't exist, please register first.",status=200,mimetype='application/json') 
        movie = movies.find_one({"title": data['title'], "year": int(data['year'])})
        if movie == None:
            return Response('No movie found with the title '+ data['title'] +' published on '+str(data['year'])+ ' was found',status=200,mimetype='application/json')
        try:
            ratings = movie['ratings']
            ratingsafter = []
            found = 0
            numbertorem = -1
            for r in ratings :
                if r['email']==data['email']:
                    found = 1
                    numbertorem = r['rate']
                else:
                    edited = {"email": r['email'], "rate": r['rate']}
                    ratingsafter.append(edited)
            if found == 0 :        
                return Response("User has not rated this movie",status=200,mimetype="application/json")
                        
            query = {"title": data['title'], "year": int(data['year'])}
            movie = movies.find_one(query)
            ud = { "$set": {"ratings": ratingsafter } }
            movies.update_one(query, ud)
            total = movie['totalratings']
            movierating = movie['rating']
            if total > 1:
                movieratingafter = movierating + ( movierating - numbertorem ) / (total - 1)
            else: 
                movieratingafter = -1
            #removing a value from sum of n:
            #s' = (ns-value)/n-1 = ns/(n-1) - value/(n-1) = s + (s - An)/(n-1)
            #https://math.stackexchange.com/questions/22348/how-to-add-and-subtract-values-from-an-average
            movies.update_one(query, { "$set": {"rating": round(movieratingafter,1)} })
            total -= 1
            movies.update_one(query, { "$set": {"totalratings": total} })
            return Response({'Rating successfully removed'},status=200,mimetype='application/json')
        except Exception :
            return Response({'Could not make any changes'},status=500,mimetype='application/json')

# Add Comment
@app.route('/addcomment', methods=['GET', 'POST'])
def add_comment():
    data = None 
    if request.method == 'GET':
        return render_template('addcomment.html')
    if request.method == 'POST':
        try:
            data = request.form.to_dict(flat=True)
        except Exception:
            return Response("Bad form content",status=500,mimetype='application/json')
        #try:
        #    data = json.loads(request.data)
        #except Exception:
        #    return Response("bad json content",status=500,mimetype='application/json')
        if data == None:
            return Response("bad request",status=500,mimetype='application/json')
        if not "email" in data or not "title" in data or not "year" in data or not "comment" in data:
            return Response("Information incomplete",status=500,mimetype="application/json")
        if not is_loggedin(data['email']):
            return Response("You must be logged in to perform this action",status=401,mimetype='application/json')  
        if users.count_documents({"email":data["email"]}) < 1 :
            return Response("A user with the given email doesn't exist, please register first.",status=200,mimetype='application/json') 
        movie = movies.find_one({"title": data['title'], "year": int(data['year'])})
        if movie == None:
            return Response('No movie found with the title '+ data['title'] +' was found',status=200,mimetype='application/json')
        try:
            comments = movie['comments']
            found = 0
            for c in comments :
                if c['email']==data['email']:
                    found = 1
            if found == 1 :        
                return Response("User has already commented on this movie",status=200,mimetype="application/json")
                        
            newcom = {"email": data['email'], "com": data['comment']}
            comments.append(newcom)
            query = {"title": data['title'], "year": int(data['year'])}
            ud = { "$set": {"comments": comments } }
            movies.update_one(query, ud)
            return Response({'Comment successfully added'},status=200,mimetype='application/json')
        except Exception:
            return Response({'Could not make any changes'},status=500,mimetype='application/json')
#User Info 
@app.route('/getuserinfo', methods=['GET'])
def userinfo():
    return render_template('userinfo.html')

# Show all user comments
@app.route('/usercomments', methods=['POST'])
def user_comments():
    email = request.form['email']
    print(email)
    if email == None:
        return Response("Bad request", status=500, mimetype='application/json')
    if not is_loggedin(email):
        return Response("You must be logged in to perform this action",status=401,mimetype='application/json')
    try:
        iterable = movies.find()
        output = []
        found = 0
        for mov in iterable:
            for d in mov['comments']:
                if d['email'] == email:
                    found = 1
                    comment = {""+mov['title']+"": d['com']}
                    output.append(comment)
        if found == 1:
            return jsonify(output)
        else:
             return Response({'User has not made any comments yet...'},status=200,mimetype='application/json')
    except Exception :
        return Response({'Could not make any changes'},status=500,mimetype='application/json')

# Show all user ratings
@app.route('/userratings', methods=['POST'])
def user_ratings():
    email = request.form['email']
    if email == None:
        return Response("Bad request", status=500, mimetype='application/json')
    if not is_loggedin(email):
        return Response("You must be logged in to perform this action",status=401,mimetype='application/json')
    try:
        iterable = movies.find()
        output = []
        found = 0
        for mov in iterable:
            for d in mov['ratings']:
                if d['email'] == email:
                    found = 1
                    rating = {""+mov['title']+"": d['rate']}
                    output.append(rating)
        if found == 1:
            return jsonify(output)
        else:
             return Response({'User has not made any ratings yet...'},status=200,mimetype='application/json')
    except Exception:
        return Response({'Could not make any changes'},status=500,mimetype='application/json')

# Delete own comment
@app.route('/deletecomment', methods=['GET','POST'])
def del_comment():
    data = None
    if request.method == 'GET':
        return render_template('remowncomment.html')
    if request.method == 'POST':
        try: 
            data = request.form.to_dict(flat=True)
        except Exception:
            return Response("Bad form content",status=500,mimetype='application/json')
        #try:
        #    data = json.loads(request.data)
        #except Exception:
        #    return Response("bad json content",status=500,mimetype='application/json')
    
        if data == None:
            return Response("bad request",status=500,mimetype='application/json')
        if not "email" in data or not "title" in data or not "year" in data:
            return Response("Information incomplete",status=500,mimetype="application/json")
        if not is_loggedin(data['email']):
            return Response("You must be logged in to perform this action",status=401,mimetype='application/json')  
        if users.count_documents({"email":data["email"]}) < 1 :
            return Response("A user with the given email doesn't exist, please register first.",status=200,mimetype='application/json') 
        
        movie = movies.find_one({"title": data['title'], "year": int(data['year'])})
        
        if movie == None:
            return Response('No movie found with the title '+ data['title'] +' was found',status=200,mimetype='application/json')
        try:
            comments = movie['comments']
            comafter = []
            found = 0
            for c in comments :
                if c['email']==data['email']:
                    found = 1
                else :
                    edited = {"email": c['email'], "com": c['com']}
                    comafter.append(edited)
            if found == 0 :        
                return Response("User has not commented on this movie",status=200,mimetype="application/json")
            else:
                query = {"title": data['title'], "year": int(data['year'])}
                ud = { "$set": {"comments": comafter } }
                movies.update_one(query, ud)
                return Response({'Comment successfully removed'},status=200,mimetype='application/json')
        except Exception:
            return Response({'Could not make any changes'},status=500,mimetype='application/json')


# Delete Account
@app.route('/deleteaccount', methods=['GET','POST'])
def delete_account():
    if request.method == 'GET':
        return render_template('deleteaccount.html')
    if request.method == 'POST':
        try:
            data = None 
            data = request.form.to_dict(flat=True)
        except Exception:
            return Response("Bad form content",status=500,mimetype='application/json')
        #try:
        #    data = json.loads(request.data)
        #except Exception:
        #    return Response("bad json content",status=500,mimetype='application/json')
        if data == None:
            return Response("bad request",status=500,mimetype='application/json')
        if not "email" in data or not "password" in data or not "name" in data:
            return Response("Information incomplete",status=500,mimetype="application/json")
        try: 
            if users.find_one({"email": data["email"]}) == None:
                return Response('No user with the email '+ data["email"] +' was found',status=200,mimetype='application/json')
            usr = users.find_one({"email": data["email"]})
            if not is_loggedin(data['email']):
                return Response("You must be logged in to perform this action",status=401,mimetype='application/json')  
            if usr['password'] == data['password'] and usr['name'] == data['name']:
                users.delete_one({"email": data["email"]})
            return Response('Account "'+ data['email'] +'\" has been deleted',status=500,mimetype='application/json')
        except Exception :
            return Response({'Could not make any changes'},status=500,mimetype='application/json')


# Admin Endpoints
# Insert Movie
@app.route('/addmovie', methods=['GET','POST'])
def add_movie():
    data = None 
    if request.method == 'GET':
        return render_template('addmovie.html')
    if request.method == 'POST':
        try:
            data = request.form.to_dict(flat=False)
        except Exception:
            return Response("Bad form content",status=500,mimetype='application/json')
    #try:
    #    data = json.loads(request.data)
    #except Exception:
    #    return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "email" in data or not "title" in data or not "actors" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")

    data['email'] = data['email'][0]
    data['title'] = data['title'][0]
    if data['year'][0] :
        data['year'] = int(data['year'][0])
    else :
        data['year'] = ''

    if users.count_documents({"email": data['email']}) == 0 :
        return Response("User does not exist",status=200,mimetype='application/json')  
    try:
        admin = users.find_one({"email":data['email']})
        if not is_loggedin(admin['email']):
                return Response("You must be logged in to perform this action",status=401,mimetype='application/json')  
        if not is_admin(admin['email']):
            return Response("The user that performs the action is not an admin", status=401,mimetype='application/json')

        
        atleastone = False
        actors = []
        for actorname in data['actors'] :
            if actorname :
                atleastone = True
                actor = {"name": actorname}
                actors.append(actor)
        data['actors'] = actors

        if not atleastone :
            return Response("Actor information incomplete",status=500,mimetype="application/json")

        movie = {"title": data['title'], "year": data.get('year', ''), "description": data.get('description', ''), "actors": data['actors'], "rating": data.get('rating', 0), "comments": data.get('comments', []), "totalratings": data.get('totalratings', 0), "ratings": data.get('ratings', [])}
        movies.insert_one(movie)
        return Response(data['title']+" was added to the MongoDB",status=200,mimetype='application/json')
    except Exception :
        return Response({'Could not make any changes'},status=500,mimetype='application/json') 

# Delete Movie
@app.route('/deletemovie', methods=['GET','POST'])
def delete_movie():
    data = None 
    if request.method == 'GET':
        return render_template('deletemovie.html')
    if request.method == 'POST':
        try:
            data = request.form.to_dict(flat=True)
        except Exception:
            return Response("Bad form content",status=500,mimetype='application/json')
        title=data['title']
        #if title == None:
        #    return Response("Bad request", status=500, mimetype='application/json')
        #try:
        #    data = json.loads(request.data)
        #except Exception:
        #    return Response("bad json content",status=500,mimetype='application/json')
        if data == None:
            return Response("bad request",status=500,mimetype='application/json')
        if not "email" in data :
            return Response("Information incomplete",status=500,mimetype="application/json")
        try:
            admin = users.find_one({"email": data["email"]})
            if not admin :
                return Response("A user with that email doesn't exist",status=401,mimetype='application/json')
            if not is_loggedin(admin['email']):
                return Response("You must be logged in to perform this action",status=401,mimetype='application/json')  
            if not is_admin(admin['email']):
                return Response("The user that performs the action is not an admin", status=401,mimetype='application/json')
            if movies.find_one({"title": title}) == None:
                return Response('No movie found with the title '+ title +' was found',status=200,mimetype='application/json')
            iterable = movies.find({"title": title})
            output = []
            for mov in iterable:
                output.append(mov)
            movs = sorted(output, key=lambda movies: movies['year'])
            movies.delete_one({"_id": movs[0]['_id']})
            return Response('Movie \"'+ title +'\" published on '+ str(movs[0]['year'])+ ' was successfully deleted',status=500,mimetype='application/json')
        except Exception as e:
            raise e
            return Response({'Could not make any changes'},status=500,mimetype='application/json')

# Update movie
@app.route('/update', methods=['GET','POST'])
def update_movie():
    data = None 
    if request.method == 'GET':
        return render_template('update.html')
    if request.method == 'POST':
        try:
            data = request.form.to_dict(flat=False)
        except Exception:
            return Response("Bad form content",status=500,mimetype='application/json')
    #data = None 
    #try:
    #    data = json.loads(request.data)
    #except Exception:
    #    return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')

    data['email'] = data['email'][0]
    data['year'] = int(data['year'][0])
    data['title'] = data['title'][0]
    data['description'] = data['description'][0]
    admin = users.find_one({"email":data['email']})

    if not "email" in data or not "year" in data or not "title" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")
    if not is_loggedin(admin['email']):
        return Response("You must be logged in to perform this action",status=401,mimetype='application/json')  
    if not is_admin(admin['email']):
        return Response("The user that performs the action is not an admin", status=401,mimetype='application/json')
    if movies.find_one({"title": data['title']}) == None:
        return Response('No movie found with the title '+ data['title'] +' was found',status=200,mimetype='application/json')
    try:
        atleastone = False
        actors = []
        for actorname in data['actors'] :
            if actorname :
                atleastone = True
                actor = {"name": actorname}
                actors.append(actor)
        data['actors'] = actors
        if not atleastone :
            return Response("Actor information incomplete",status=500,mimetype="application/json")

        mov = movies.find_one({"title": data['title']})
        newvalues = { "$set" : 
                        { "title": data.get('title', mov['title']),
                        "year": data.get('year', mov['year']),
                        "description:": data.get('description', mov['description']),
                        "actors": data.get('actors', mov['actors'])
                        }
                    }
        movies.update_one({"_id": mov['_id']}, newvalues)
        return Response('Μovie  '+data['title'] +' has been updated accordingly',status=200,mimetype='application/json')
    except Exception:
        return Response({'Could not make any changes'},status=200,mimetype='application/json')
    
# Delete any comment
@app.route('/deleteanycomment', methods=['GET','POST'])
def del_any_comment():
    data = None 
    if request.method == 'GET':
        return render_template('deleteanycomment.html')
    if request.method == 'POST':
        try:
            data = request.form.to_dict(flat=True)
            data['year'] = int(data['year'])
        except Exception:
            return Response("Bad form content",status=500,mimetype='application/json')
        #try:
        #    data = json.loads(request.data)
        #except Exception:
        #    return Response("bad json content",status=500,mimetype='application/json')
        if data == None:
            return Response("bad request",status=500,mimetype='application/json')
        if not "email" in data or not "title" in data or not "year" in data or not "useremail" in data :
            return Response("Information incomplete",status=500,mimetype="application/json")
        if users.count_documents({"email": data["email"]}) < 1 :
            return Response("A user with the given email doesn't exist, please register first.",status=200,mimetype='application/json') 
        if users.count_documents({"email": data["useremail"]}) < 1 :
            return Response("The target user doesn't exist, check key useremail.",status=200,mimetype='application/json') 
        if not is_admin(data['email']):
            return Response("This action requires admin priviledges",status=401,mimetype='application/json')  
        if not is_loggedin(data['email']):
            return Response("You must be logged in to perform this action",status=401,mimetype='application/json')  
        
        movie = movies.find_one({"title": data['title'], "year": data['year']})
        
        if movie == None:
            return Response('No movie found with the title '+ data['title'] +' was found',status=200,mimetype='application/json')
        try:
            comments = movie['comments']
            comafter = []
            found = 0
            for c in comments :
                if c['email']==data['useremail']:
                    found = 1
                else :
                    edited = {"email": c['email'], "com": c['com']}
                    comafter.append(edited)
            if found == 0 :        
                return Response("User has not commented on this movie",status=200,mimetype="application/json")
            else:
                query = {"title": data['title'], "year": data['year']}
                ud = { "$set": {"comments": comafter } }
                movies.update_one(query, ud)
                return Response({'Comment from user ' +data['useremail']+' on "'+data['title'] +'" successfully removed'},status=200,mimetype='application/json')
        except Exception:
            return Response({'Could not make any changes'},status=500,mimetype='application/json')

# Make Admin
@app.route('/makeadmin', methods=['GET','POST'])
def make_admin():
    data = None 
    if request.method == 'GET':
        return render_template('makeadmin.html')
    if request.method == 'POST':
        try:
            data = request.form.to_dict(flat=True)
        except Exception:
            return Response("Bad form content",status=500,mimetype='application/json')
        #try:
        #    data = json.loads(request.data)
        #except Exception:
        #    return Response("bad json content",status=500,mimetype='application/json')
        if data == None:
            return Response("bad request",status=500,mimetype='application/json')
        if not "email" in data or not "useremail" in data :
            return Response("Information incomplete",status=500,mimetype="application/json")
        if users.count_documents({"email":data["email"]}) == 1 and users.count_documents({"email":data["useremail"]}) == 1:  
            admin = users.find_one({"email":data["email"]})
            if not is_loggedin(admin['email']):
                return Response("You must be logged in to perform this action",status=401,mimetype='application/json')  
            if not is_admin(admin['email']):
                return Response("The user that performs the action is not an admin", status=401,mimetype='application/json')
        else:
            return Response("Corresponding users not found", status=200,mimetype='application/json')
        try:
            query = {"email":data['useremail']}
            user = users.find_one(query)
            if is_admin(user['email']):
                return Response("The target user is already an admin", status=200,mimetype='application/json')
            ud = { "$set": {"access": ACCESS['admin'] } }
            users.update_one(query, ud)
            return Response(admin['email']+" changed the access level of " + user['email']+ " to "+ str(ACCESS['admin']),status=200,mimetype='application/json') 
        except Exception:
            return Response({'Could not make any changes'},status=500,mimetype='application/json')

# Delete non-admin user
@app.route('/deleteuser', methods=['GET', 'POST'])
def delete_user():
    data = None 
    if request.method == 'GET':
        return render_template('deleteuser.html')
    if request.method == 'POST':
        try:
            data = request.form.to_dict(flat=True)
        except Exception:
            return Response("Bad form content",status=500,mimetype='application/json')
        
        #try:
        #    data = json.loads(request.data)
        #except Exception:
        #    return Response("bad json content",status=500,mimetype='application/json')
        if data == None:
            return Response("bad request",status=500,mimetype='application/json')
        if not "email" in data or not "useremail" in data :
            return Response("Information incomplete",status=500,mimetype="application/json")
        if users.count_documents({"email":data["email"]}) == 1 and users.count_documents({"email":data["useremail"]}) == 1:  
            admin = users.find_one({"email":data["email"]})
            if not is_loggedin(admin['email']):
                return Response("You must be logged in to perform this action",status=401,mimetype='application/json')  
            if not is_admin(admin['email']):
                return Response("The user that performs the action is not an admin", status=401,mimetype='application/json')
        else:
            return Response("Corresponding users not found", status=200,mimetype='application/json')
        try:
            query = {"email": data['useremail']}
            user = users.find_one(query)
            if is_admin(user['email']):
                return Response("The target user is an admin, cannot delete", status=200,mimetype='application/json')
            users.delete_one({"email": data['useremail']})
            return Response(admin['email']+" Deleted the user " + user['email'],status=200,mimetype='application/json') 
        except Exception:
            return Response({'Could not make any changes'},status=500,mimetype='application/json')

# Run Flask App
if __name__ == '__main__':
    check_data()
    app.run(debug=True, host='0.0.0.0', port=5000)