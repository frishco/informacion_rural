from flask import Blueprint, render_template, request,  flash, g, session, redirect, url_for
from app.mercados.form import MercadoForm


mercados = Blueprint('mercados', __name__,
                        template_folder = 'templates', url_prefix = '/mercados' )

@mercados.route('/registro', methods=['GET', 'POST'])
def registro():

    # If sign in form is submitted
    form = MercadoForm()
    if form.validate_on_submit():
        flash("Success")
        return redirect(url_for("app.homepage"))

    return render_template("registro.html", form=form)
