from functools import cmp_to_key
from flask import render_template, request, session, redirect, url_for, send_file
from obj import journal, documentation, admin_processes
from io import BytesIO


def setup_page_routing(app, database):
    """

    :param database:
    :param app:
    :return: None
    """

    # The accountant pages
    @app.route('/accountant_home')
    def accountant_home_page():
        if "Accountant" in session:
            username = session["Accountant"]
            approved_entries = database.get_approved_journal_entries()
            pending_entries = database.get_pending_journal_entries()
            rejected_entries = database.get_rejected_journal_entries()
            return render_template('accountant_home_page.html', username=username, approved_entries=approved_entries[:6],
                                   pending_entries=pending_entries[:6], rejected_entries=rejected_entries[:4])
        else:
            return redirect(url_for('login_page'))

    @app.route('/accountant/chart_accounts')
    def accountant_chart_accounts():
        if "Accountant" in session:
            username = session["Accountant"]
            accounts = database.get_active_accounts()
            subcategories = admin_processes.subcategory_accounts(accounts)
            return render_template('accountant_char_accounts.html', username=username, accounts=accounts,
                                   sub_cats=subcategories)
        else:
            return redirect(url_for('login_Page'))

    @app.route('/accountant/<account_id>_ledger')
    def accountant_account_ledger(account_id):
        if "Accountant" in session:
            username = session["Accountant"]
            account = database.get_account_info(account_id)
            ledger_entries = database.get_account_ledger_info(account.number)
            return render_template('accountant_account_ledger.html', username=username, account=account,
                                   ledger_entries=ledger_entries)
        else:
            return redirect(url_for('login_page'))

    @app.route('/accountant/journal')
    def accountant_journal():
        if "Accountant" in session:
            username = session["Accountant"]
            accounts = database.get_active_accounts()
            entries = database.get_journal_entries()
            error = database.get_error_message(11)
            error1 = database.get_error_message(12)
            return render_template('accountant_journal.html', username=username, accounts=accounts, entries=entries,
                                   error_message=error.message, error_message1=error1.message)
        else:
            return redirect(url_for('login_page'))

    @app.route('/accountant/pr=<post_reference>_journal_entry')
    def accountant_post_reference(post_reference):
        if "Accountant" in session:
            username = session["Accountant"]
            post_entry = database.get_journal_entry(post_reference)
            return render_template("accountant_journal_entry.html", username=username, entry=post_entry)

    @app.route('/accountant/<account_number>_to_id')
    def accountant_number_id(account_number):
        if "Accountant" in session:
            account = database.get_account_info_by_number(account_number)
            return redirect(url_for('accountant_account_ledger', account_id=account.id))
        else:
            return '', 204

    @app.route('/accountant/journal/submit_entry', methods=['GET', 'POST'])
    def accountant_entry():
        if "Accountant" in session:
            user = session["Accountant"]
            if request.method == "POST":
                journal.journal_entry_form(user, database)
                return redirect(url_for('accountant_journal'))
            else:
                return '', 204
        else:
            return redirect(url_for('login_page'))

    @app.route('/accountant/eventlog')
    def accountant_eventlog():
        if "Accountant" in session:
            username = session["Accountant"]
            account_events = [(event, 'Account') for event in database.get_all_account_events()]
            journal_events = [(event, 'Journal') for event in database.get_all_journal_events()]
            events = account_events + journal_events

            def event_compare(item1, item2):
                return (item1[0].date_made - item2[0].date_made).total_seconds()

            events = sorted(events, key=cmp_to_key(event_compare), reverse=True)
            return render_template('accountant_eventlog.html', username=username, events=events)
        else:
            return redirect(url_for('login_page'))

    @app.route('/accountant/reports/trial_balance')
    def accountant_trial_balance():
        if "Accountant" in session:
            username = session["Accountant"]
            accounts = database.get_active_accounts()
            total_amounts = documentation.get_total_amounts(accounts)
            return render_template('accountant_trial_balance.html', username=username, accounts=accounts,
                                   total_amounts=total_amounts)
        else:
            return redirect(url_for('login_page'))

    @app.route('/accountant/reports/income_statement')
    def accountant_income_statement():
        if "Accountant" in session:
            username = session["Accountant"]
            r_accounts = database.get_accounts_by_category("Revenue")
            exp_accounts = database.get_accounts_by_category("Expenses")
            total_revenue = documentation.get_total_amount(r_accounts)
            total_expense = documentation.get_total_amount(exp_accounts)
            net_total = total_revenue - total_expense
            return render_template('accountant_income_statement.html', username=username, r_accounts=r_accounts,
                                   exp_accounts=exp_accounts, total_revenue=total_revenue, total_expenses=total_expense,
                                   total_netIncome=net_total)
        else:
            return redirect(url_for('login_page'))

    @app.route('/accountant/reports/balance_sheet')
    def accountant_balance_sheet():
        if "Accountant" in session:
            username = session["Accountant"]
            return render_template('accountant_balance_sheet.html', username=username)
        else:
            return redirect(url_for('login_page'))

    @app.route('/accountant/report/retained_earnings')
    def accountant_retained_earnings():
        if "Accountant" in session:
            username = session["Accountant"]
            r_accounts = database.get_accounts_by_category("Revenue")
            exp_accounts = database.get_accounts_by_category("Expenses")
            total_revenue = documentation.get_total_amount(r_accounts)
            total_expense = documentation.get_total_amount(exp_accounts)
            net_total = total_revenue - total_expense
            new_balance = net_total - 0
            return render_template('accountant_retained_earning.html', username=username, income_balance=net_total,
                                   retained_balance=0, dividends_amount=0, new_retained_balance=new_balance)
        else:
            return redirect(url_for('login_page'))

    @app.route('/get_files_<post_reference>&_<file_name>', methods=['POST'])
    def get_file(post_reference, file_name):
        if request.method == "POST":
            entry = database.get_journal_entry(post_reference)
            data = None
            for x in range(0, len(entry.file_name)):
                if file_name == entry.file_name[x]:
                    data = entry.file_data[x]
            return send_file(BytesIO(data), attachment_filename=file_name, as_attachment=False)
