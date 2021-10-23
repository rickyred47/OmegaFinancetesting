from flask import render_template


def setup_page_routing(app, base, db):
    """

    :param app:
    :param base: The automap of the data base
    :param db: the database engine
    :return: None
    """

    # The accounntant pages
    @app.routes('/accountant_home')
    def accountant_home_page():
        return render_template('base_accountant.html')
