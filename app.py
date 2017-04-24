from flask import Flask, render_template, request
from goeuro import get_matches

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')
    
@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        #result = request.form
        one = request.form['origin1']
        two = request.form['origin2']
        date = request.form['depart']
        print(date)
        result = get_matches(one,two,date)
        return render_template("result.html",result = result, one = one, two = two)
    
if __name__ == "__main__":
    app.run()
