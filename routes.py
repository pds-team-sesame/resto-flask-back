from flask import Blueprint, render_template
from Controllers.reservation import add_reservation_function
from Models.roles import Role
import sys
main = Blueprint('main', __name__)

# -----------HomePage---------------------

@main.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@main.route('/add_reservation', methods=['GET','POST'])
def add_reservation():
    data= add_reservation_function()
    print (data,file=sys.stderr)
    return render_template('add.html', data=data)


