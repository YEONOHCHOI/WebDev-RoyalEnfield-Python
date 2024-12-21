from flask import Blueprint, render_template, url_for, request, session, flash, redirect
from .models import MotorBike, MotorBikeType, Order
from datetime import datetime
from .forms import CheckoutForm
from . import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    motorbiketypes = MotorBikeType.query.order_by(MotorBikeType.name).all()
    return render_template('index.html', motorbiketypes=motorbiketypes)

@main_bp.route('/viewbike/<motorbikes_id>',methods=['GET'])
def product_detail(motorbikes_id):
    # motorbike = MotorBike.query.filter_by(bike_id)
    motorbike = db.session.scalar(db.select(MotorBike).where(MotorBike.id==motorbikes_id))
    return render_template('product_detail.html', search=search, motorbike=motorbike)

@main_bp.route('/viewmodels/<int:motorbiketypesid>')
def viewmodels(motorbiketypesid):
    motorbikes = MotorBike.query.filter(MotorBike.motorbiketype_id==motorbiketypesid).all()
    return render_template('viewmodels.html', motorbikes=motorbikes)

@main_bp.route('/viewmodels/',methods=['GET'])
def search():
    search = request.args.get('search')
    search = '%{}%'.format(search)
    motorbikes = MotorBike.query.filter(MotorBike.name.like(search)).all()  
    return render_template('viewmodels.html', search=search, motorbikes=motorbikes)

# Referred to as "Basket" to the user
@main_bp.route('/order', methods=['POST','GET'])
def order():
    motorbikes_id = request.values.get('motorbikes_id')

    # retrieve order if there is one
    if 'order_id'in session.keys():
        order = Order.query.get(session['order_id'])
        # order will be None if order_id stale
    else:
        # there is no order
        order = None

    # create new order if needed
    if order is None:
        order = Order(status = False, firstname='', surname='', email='', phone='', totalcost=0, date=datetime.now())
        try:
            db.session.add(order)
            db.session.commit()
            session['order_id'] = order.id
        except:
            print('Failed at creating a new order')
            order = None
    
    # calcultate totalprice
    total_price = 0
    if order is not None:
        for motorbike in order.motorbike:
            total_price = total_price + motorbike.price
    
    # are we adding an item?
    if motorbikes_id is not None and order is not None:
        motorbike = MotorBike.query.get(motorbikes_id)
        if motorbike not in order.motorbike:
            try:
                order.motorbike.append(motorbike)
                db.session.commit()
            except:
                return 'There was an issue adding the item to your basket'
            return redirect(url_for('main.order'))
        else:
            flash('Motorbike already in basket')
            return redirect(url_for('main.order'))
    return render_template('order.html', order = order, total_price=total_price)

# Delete specific basket items
@main_bp.route('/deleteorderitem', methods=['POST'])
def deleteorderitem():
    id=request.form['id']
    if 'order_id' in session:
        order = Order.query.get_or_404(session['order_id'])
        motorbike_to_delete = MotorBike.query.get(id)
        try:
            order.motorbike.remove(motorbike_to_delete)
            db.session.commit()
            return redirect(url_for('main.order'))
        except:
            return 'Problem deleting item from order'
    return redirect(url_for('main.order'))

# Scrap basket
@main_bp.route('/deleteorder')
def deleteorder():
    if 'order_id' in session:
        del session['order_id']
        flash('All items deleted')
    return redirect(url_for('main.index'))

@main_bp.route('/checkout', methods=['POST','GET'])
def checkout():
    form = CheckoutForm() 
    if 'order_id' in session:
        order = Order.query.get_or_404(session['order_id'])
       
        if form.validate_on_submit():
            order.status = True
            order.firstname = form.firstname.data
            order.surname = form.surname.data
            order.email = form.email.data
            order.phone = form.phone.data
            totalcost = 0
            for tour in order.motorbike:
                totalcost = totalcost + tour.price
            order.totalcost = totalcost
            order.date = datetime.now()
            try:
                db.session.commit()
                del session['order_id']
                flash('Thank you! We will contact you soon...')
                return redirect(url_for('main.index'))
            except:
                return 'There was an issue completing your order'
    return render_template('checkout.html', form=form)