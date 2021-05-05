from flask import Flask, render_template, request, url_for
import psycopg2

app = Flask (__name__)

# Default (home) route
@app.route("/")
def home():
    return render_template("home.html")

# Over view (home) route
@app.route("/overview/")
def overview():
    return render_template("overview.html")

# Popularity route
@app.route("/popularity/")
def popularity():
    # Get user input
    counts = request.args.get("counts", "")
    limits = request.args.get("limits", "")
    # Validate input
    counts = counts if counts.isnumeric() else ""
    limits = limits if limits.isnumeric() else ""
    # Invalid input/default 
    if not counts or not limits: 
        return render_template("steampopularity_form.html")
    else: 
        # Connect to the database
        cur = get_db()
        sql = """
            SELECT * FROM popularity(%s, %s)"""
        counts = 93 if int(counts) > 93 else counts
        counts = counts if int(counts) > 0 else 1
        limits = 30 if int(limits) > 30 else limits
        limits = limits if int(limits) > 0 else 1
        cur.execute(sql, (counts, limits))
        queryvalue = cur.fetchall()
        return render_template("steampopularity_chart.html", counts = counts, limits = limits, queryvalue = queryvalue)

# Median Price route
@app.route("/medianprice/")
def median():
    # Get user input
    magnitude = request.args.get("magnitude", "")
    sliderval = request.args.get("sliderval", "")
    lowval = 0
    highval = 350
    # Grabs the slider values from slider text in highestPriceDeveloper.html
    if(sliderval != ""):
        sliderval = sliderval.replace(" - ", ' ').replace("$", ' ')
        lowval = sliderval.split(' ')[1]
        highval = sliderval.split(' ')[3]
    # Invalid input/default
    if lowval == 0 and highval == 350:
        return render_template("median_form.html",lowval=lowval, highval=highval)
    else:
        # Connect to the database
        cur = get_db()

        # Queries based on DESC/ASC values
        query1 = '''
           SELECT *
           FROM highestpricedeveloper
            WHERE medprice > (%s)
             AND medprice < (%s)
           ORDER BY medprice ''' + magnitude + ''', avgprice ''' + magnitude + '''
            LIMIT 10;'''
        # Selects query to run based off of browser arguments
        cur.execute(query1, (lowval, highval))
        hlTag = 'Highest' if (magnitude == 'DESC') else 'Lowest'
        datas = cur.fetchall()
        return render_template("median_chart.html", hlTag=hlTag, magnitude=magnitude, datas=datas, lowval=lowval, highval=highval)

# Best Value route
@app.route("/bestvalue/")
def bestvalue():
    # Get user input
    playtime = request.args.get("playtime")
    pparam = request.args.get("pparam")
    porder = request.args.get("porder")
    rparam = request.args.get("rparam")
    rating = request.args.get("rating")
    rorder = request.args.get("rorder")
    # Invalid input/default
    if not playtime or not pparam or not porder \
        or not rparam or not rating or not rorder:
        return render_template("bestvalue_form.html")
    else:
        sql = """
        SELECT name, average_playtime, net_ratings
        FROM bestvaluegames
            WHERE net_ratings """ + rparam + """ %s
                AND average_playtime """ + pparam + """ %s
        ORDER BY average_playtime """ + porder + """, net_ratings """ + rorder + """
        LIMIT 10;"""
        # Connect to the database
        cur = get_db()
        cur.execute(sql, (rating, playtime))
        return render_template("bestvalue_chart.html", cur=list(cur))

# Rated R route
@app.route("/ratedr/")
def ratedR():
    # Get user input
    positive_ratings = request.args.get("positive_ratings", "")
    # Invalid inputs/default
    if not positive_ratings:
        return render_template("ratedr_form.html")
    else:
        positive_ratings = positive_ratings if positive_ratings.isnumeric() and (int(positive_ratings) > 20000) else 20000
        positive_ratings = positive_ratings if int(positive_ratings) < 329061 else 329061
        # Connect to the database
        cur = get_db()
        sql = """
            SELECT name, positive_ratings, price
            FROM game
            WHERE positive_ratings >= (%s)
		    AND required_age >= 18
		    ORDER BY positive_ratings DESC;
            """
        cur.execute(sql,(positive_ratings,)) 
        datas = cur.fetchall()
        return render_template("ratedr_chart.html", positive_ratings = positive_ratings, datas = datas)

# Requirements route
@app.route("/requirements/")
def requirements():
    # Get user input
    english = request.args.get("english", "")
    genres = request.args.get("genres", "")
    plateforms = request.args.get("plateforms", "")

    # Invalid inputs/default
    if not genres:
        return render_template("requirement_form.html")
    else:
        # Connect to the database
        cur = get_db()
        sql = """
            SELECT *
            FROM require(%s, %s, %s)"""
        cur.execute(sql, (english, genres, plateforms))
        return render_template("requirement_chart.html", cur=list(cur))

# Connects to the specified database
# Returns a cursor of the specified database
def get_db():
    return psycopg2.connect("host=localhost dbname=steam user=steam password=js-EPJ3$Uh&q3$2=").cursor()

