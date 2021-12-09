from flask import render_template, redirect, request, url_for, session, send_file
from functools import cmp_to_key
from obj import admin_processes, documentation
from datetime import datetime, timedelta
from io import BytesIO
import base64


def setup_page_routing(app, database):
    # set up routes to run

    # The admin pages

    @app.route('/admin_home')
    def admin_home_page():
        if "Administrator" in session:
            username = session["Administrator"]
            accounts = database.get_accounts_info()
            newusers = database.get_new_users()
            users = database.get_user_accounts()
            assets_subcategory_total = documentation.get_subcategory_total_number("Asset", database)
            assets_subcategory_totals = documentation.get_subcategory_totals("Asset", database)
            liability_subcategory_total = documentation.get_subcategory_total_number("Liability", database)
            total_Assets = documentation.get_category_totals(assets_subcategory_totals[1])
            r_accounts = database.get_accounts_by_category("Revenue")
            total_revenue = documentation.get_total_amount(r_accounts)
            exp_accounts = database.get_accounts_by_category("Expenses")
            total_expense = documentation.get_total_amount(exp_accounts)
            net_total = total_revenue - total_expense
            equity_subcategory_totals = documentation.get_subcategory_totals("Equity", database)
            total_Equity = documentation.get_category_totals(equity_subcategory_totals[1])
            return render_template('admin_home_page.html', accounts=accounts[-4:], newusers=newusers[-4:], users=users[-4:],
                                   username=username, asset_sub_total=assets_subcategory_total,
                                   lib_sub_total = liability_subcategory_total, total_assets=total_Assets,
                                   asset_sub_totals=assets_subcategory_totals[1], total_rev = total_revenue,
                                   income_balance=net_total, total_equity=total_Equity)
        else:
            return redirect(url_for('login_page'))

    @app.route('/admin_users_accounts')
    def admin_user_accounts():
        if "Administrator" in session:
            username = session["Administrator"]
            users = database.get_user_accounts()
            return render_template('adminuseraccounts.html', username=username, useraccounts=users)
        else:
            return redirect(url_for('login_page'))

    @app.route('/admin_chart_accounts', methods=['GET', 'POST'])
    def admin_chart_accounts():
        if "Administrator" in session:
            username = session["Administrator"]
            if request.method == "POST":
                idnum = request.form["account_id"]
                account = database.get_account_info(idnum)
                num = admin_processes.toggle_active(account, database)
                accounts = database.get_active_accounts()
                subcategories = admin_processes.subcategory_accounts(accounts)
                error = database.get_error_message(num)
                return render_template("chart_of_accounts.html", accounts=accounts, username=username,
                                       error_message=error.message, sub_cat=subcategories)
            else:
                accounts = database.get_active_accounts()
                subcategories = admin_processes.subcategory_accounts(accounts)
                return render_template("chart_of_accounts.html", accounts=accounts, username=username,
                                       sub_cat=subcategories)
        else:
            return redirect(url_for('login_page'))

    @app.route('/admin_create_user', methods=['GET', 'POST'])
    def admin_create_user():
        if "Administrator" in session:
            if request.method == "POST":
                if admin_processes.new_user_admin(database):
                    return redirect(url_for('admin_user_accounts'))
            else:
                username = session["username"]
                return render_template('admincreateuser.html', username=username)
        else:
            return redirect(url_for('login_page'))

    @app.route('/admin_create_account', methods=['GET', 'POST'])
    def admin_create_account():
        if "Administrator" in session:
            username = session["Administrator"]
            if request.method == "POST":
                if admin_processes.is_valid_name_number(database):
                    admin_processes.account_form(database)
                    return redirect(url_for('admin_chart_accounts'))
                else:
                    error = database.get_error_message(8)
                    return render_template('create_account.html', username=username, error_message=error.message)
            else:
                return render_template('create_account.html', username=username)
        else:
            return redirect(url_for('login_page'))

    @app.route('/admin_add_chart_accounts', methods=['GET', 'POST'])
    def admin_add_chart_accounts():
        if "Administrator" in session:
            username = session["Administrator"]
            accounts = database.get_inactive_accounts()
            active_accounts = database.get_active_accounts()
            max_order = admin_processes.max_order_num(active_accounts)
            error = database.get_error_message(12)
            max_order += 2
            if request.method == "POST":
                account_id = request.form["select_account"]
                account = database.get_account_info(account_id)
                if request.form["is_taken"] == "true":
                    print("test")
                    admin_processes.change_order(active_accounts, database)
                admin_processes.add_account_to_chart(account, database)
                return redirect(url_for('admin_chart_accounts'))
            else:
                return render_template('add_to_chart_of_accounts.html', username=username, accounts=accounts,
                                       active_accounts=active_accounts, max_order=max_order,
                                       error_message=error.message)
        else:
            return redirect(url_for('login_page'))

    @app.route('/admin_edit_account/<account_id>')
    def admin_edit_account(account_id):
        if "Administrator" in session:
            username = session["Administrator"]
            account = database.get_account_info(account_id)
            num_string = str(account.number)
            initial = int(num_string[0])
            number = num_string[1:]
            return render_template('edit_account.html', username=username, account=account, initial_number=initial,
                                   number=number)
        else:
            return redirect(url_for('login_page'))

    @app.route('/admin_edit_account/save_account', methods=['POST', 'GET'])
    def admin_save_account():
        if "Administrator" in session:
            if request.method == "POST":
                account_id = request.form["account_id"]
                account = database.get_account_info(account_id)
                admin_processes.edit_save_account(account, database)
                return redirect(url_for('admin_chart_accounts'))
            else:
                redirect(url_for('login_page'))
        else:
            return '', 204

    @app.route('/admin_ledger/<account_id>')
    def admin_account_ledger(account_id):
        if "Administrator" in session:
            username = session["Administrator"]
            account = database.get_account_info(account_id)
            ledger_entries = database.get_account_ledger_info(account.number)
            return render_template('admin_accounts_ledger.html', username=username, account=account,
                                   ledger_entries=ledger_entries)
        else:
            return redirect(url_for('login_page'))

    @app.route('/admin_about')
    def admin_about():
        if "Administrator" in session:
            username = session["Administrator"]
            return render_template('admin_about.html', username=username)
        else:
            return redirect(url_for('login_page'))

    @app.route('/admin/new_users')
    def admin_new_user_accounts():
        if "Administrator" in session:
            username = session["Administrator"]
            new_users = database.get_new_users()
            return render_template('admin_new_user_accounts.html', newusers=new_users, username=username)
        else:
            return redirect(url_for('login_page'))

    @app.route('/admin_password_report')
    def admin_password_report():
        if "Administrator" in session:
            username = session["Administrator"]
            users = database.get_expired_users()
            for user in users:
                user.the_password_hash = base64.b64encode(bytes(user.previous_passwords[0], 'utf-8'))
                user.the_password_hash = '#' + str(base64.b64encode(user.the_password_hash + base64.b64encode(user.the_password_hash)))[2:-1]
            return render_template('admin_password_report.html', username=username, users=users)
        else:
            return redirect(url_for('login_page'))

    @app.route('/admin_email', methods=['GET', 'POST'])
    def admin_email():
        if "Administrator" in session:
            if request.method == "POST":
                return admin_processes.email(database)
            else:
                username = session["Administrator"]
                users = database.get_user_accounts()
                return render_template('admin_email.html', username=username, users=users)
        else:
            return redirect(url_for('login_page'))

    @app.route('/eventlog')
    def eventlog():
        if "Administrator" in session:
            username = session["Administrator"]
            account_events = [(event, 'Account') for event in database.get_all_account_events()]
            journal_events = [(event, 'Journal') for event in database.get_all_journal_events()]
            user_events = [(event, 'User') for event in database.get_all_user_events()]
            events = account_events + journal_events + user_events
            def event_compare(item1, item2):
                return (item1[0].date_made - item2[0].date_made).total_seconds()
            events = sorted(events, key=cmp_to_key(event_compare), reverse=True)
            # Set all times
            for event in events:
                event[0].date_made -= timedelta(hours=5)
            return render_template('eventlog.html', username=username, events=events)
        else:
            return redirect(url_for('login_page'))

    @app.route('/background_accept_user', methods=['GET', 'POST'])
    def admin_accept_user():
        if request.method == "POST":
            username = request.form["username_input"]
            role = request.form["role"]
            admin_processes.transfer_User_info(username, role, database)
            user = database.get_user_account(username)
            admin_processes.send_acceptance_email(user)
            return redirect(url_for('admin_new_user_accounts'))
        else:
            return '', 204

    @app.route('/background_reject_user/<username>')
    def admin_reject_user(username):
        if "Adminstrator" in session:
            new_user = database.get_new_user(username)
            database.delete_row(new_user)

            # Create new user event
            UserEventsTable = database.get_user_event_table()
            new_user_event = UserEventsTable(username_before=new_user.username, username_after=None,
                                             role_before=None, role_after=None, f_name_before=new_user.firstname,
                                             f_name_after=None, l_name_before=new_user.lastname,
                                             l_name_after=None, address_before=new_user.street,
                                             address_after=None, city_before=None, city_after=None,
                                             apt_number_before=new_user.aptnum, apt_number_after=None,
                                             zip_before=new_user.zipcode, zip_after=None,
                                             state_province_before=new_user.state, state_province_after=None,
                                             country_before=new_user.country, country_after=None,
                                             activated_before=False, activated_after=False, is_suspended_before=False,
                                             is_suspended_after=False, date_made=datetime.now(),
                                             event_type='Modified', username=session['username'], user_id=new_user.id)
            database.commit_to_database(new_user_event)

            return redirect(url_for('admin_new_user_accounts'))
        else:
            return '', 204

    @app.route('/background_deactivate_user', methods=['GET', 'POST'])
    def admin_deactivate_user():
        if request.method == "POST":
            username = request.form["username_input"]
            user = database.get_user_account(username)
            selection = request.form["time"]
            if selection == "Indefinite":
                admin_processes.deactivated_user(user, database)
                return redirect(url_for('admin_user_accounts'))
            else:
                admin_processes.set_suspension(user, database)
                return redirect(url_for('admin_user_accounts'))
        else:
            return '', 204

    @app.route('/background_activate_user/<username>')
    def admin_activate_user(username):
        if "Administrator" in session:
            user = database.get_user_account(username)
            user.activated = True
            user.is_suspended = False
            database.commit_info()
            return redirect(url_for('admin_user_accounts'))
        else:
            return '', 204

    @app.route('/testing', methods=['GET', 'POST'])
    def admin_testing():
        if request.method == "POST":
            file = request.files['file']
            data = file.stream.read()
            return send_file(BytesIO(data), attachment_filename=file.filename, as_attachment=False)
        else:
            return render_template("testing_files.html")
