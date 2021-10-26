from flask import render_template, request, session


def setup_page_routing(app, database):
    """

    :param app:
    :return:

    Set Up routes to run for the manager

    Manager pages
    """
    @app.route('/manager_home')
    def manager_home_page():
        return render_template('base_manager.html')
