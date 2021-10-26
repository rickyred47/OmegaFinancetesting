from flask import render_template


def setup_page_routing(app, database):
    """

    :param app:
    :return: None
    """

    # The accounntant pages
    @app.route('/accountant_home')
    def accountant_home_page():
        return render_template('base_accountant.html')
