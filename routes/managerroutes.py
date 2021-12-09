from functools import cmp_to_key

from flask import render_template, request, session, redirect, url_for
from datetime import datetime, timedelta
from obj import journal, documentation, admin_processes


def setup_page_routing(app, database):
    """

    :param database:
    :param app:
    :return:

    Set Up routes to run for the manager

    Manager pages
    """
    @app.route('/manager_home')
    def manager_home_page():
        if "Manager" in session:
            username = session["Manager"]
            approved_entries = database.get_approved_journal_entries()
            pending_entries = database.get_pending_journal_entries()
            rejected_entries = database.get_rejected_journal_entries()
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
            return render_template('manager_home_page.html', username=username, approved_entries=approved_entries[:3],
                                   pending_entries=pending_entries[:3], rejected_entries=rejected_entries[:3], asset_sub_total=assets_subcategory_total,
                                   lib_sub_total = liability_subcategory_total,
                                   total_assets=total_Assets, asset_sub_totals=assets_subcategory_totals[1], total_rev = total_revenue,
                                   income_balance=net_total, total_equity=total_Equity)
        else:
            return redirect(url_for('login_page'))

    @app.route('/manager/chart_accounts')
    def manager_chart_accounts():
        if "Manager" in session:
            username = session["Manager"]
            accounts = database.get_active_accounts()
            subcategories = admin_processes.subcategory_accounts(accounts)
            return render_template('manager_char_accounts.html', username=username, accounts=accounts,
                                   sub_cats=subcategories)
        else:
            return redirect(url_for('login_page'))

    @app.route('/manager/<account_id>_ledger')
    def manager_account_ledger(account_id):
        if "Manager" in session:
            username = session["Manager"]
            account = database.get_account_info(account_id)
            ledger_entries = database.get_account_ledger_info(account.number)
            return render_template('manager_account_ledger.html', username=username, account=account,
                                   ledger_entries=ledger_entries)
        else:
            return redirect(url_for('login_page'))

    @app.route('/manager/eventlog')
    def manager_eventlog():
        if "Manager" in session:
            username = session["Manager"]
            account_events = [(event, 'Account') for event in database.get_all_account_events()]
            journal_events = [(event, 'Journal') for event in database.get_all_journal_events()]
            events = account_events + journal_events

            def event_compare(item1, item2):
                return (item1[0].date_made - item2[0].date_made).total_seconds()

            events = sorted(events, key=cmp_to_key(event_compare), reverse=True)
            # Set all times
            for event in events:
                event[0].date_made -= timedelta(hours=5)
            return render_template('manager_eventlog.html', username=username, events=events)
        else:
            return redirect(url_for('login_page'))

    @app.route('/manager/<account_number>_to_id')
    def manager_number_id(account_number):
        if "Manager" in session:
            account = database.get_account_info_by_number(account_number)
            return redirect(url_for('manager_account_ledger', account_id=account.id))
        else:
            return '', 204

    @app.route('/manager/journal')
    def manager_journal():
        if "Manager" in session:
            username = session["Manager"]
            accounts = database.get_active_accounts()
            entries = database.get_journal_entries()
            error = database.get_error_message(11)
            error1 = database.get_error_message(12)
            return render_template('manager_journal.html', username=username, accounts=accounts, entries=entries,
                                   error_message=error.message, error_message1=error1.message)
        else:
            return redirect(url_for('login_page'))

    @app.route('/manager/pr=<post_reference>_journal_entry')
    def manager_post_reference(post_reference):
        if "Manager" in session:
            username = session["Manager"]
            post_entry = database.get_journal_entry(post_reference)
            return render_template("manager_journal_entry.html", username=username, entry=post_entry)
        else:
            return '', 204

    @app.route('/manager/journal/submit_entry', methods=['GET', 'POST'])
    def manager_entry():
        if "Manager" in session:
            user = session["Manager"]
            if request.method == "POST":
                journal.journal_entry_form(user, database)
                return redirect(url_for('manager_journal'))
            else:
                return '', 204
        else:
            return redirect(url_for('login_page'))

    @app.route('/back_ground_accept_reject_entry', methods=['GET', 'POST'])
    def manager_accept_reject_entry():
        if "Manager" in session:
            if request.method == "POST":
                entry_id = request.form["entry_id"]
                entry = database.get_journal_entry(entry_id)
                if request.form['accept_reject'] == 'Accept':
                    journal.post_info(entry, database)
                else:
                    entry.comment_rejection=request.form["reason"]
                if request.form['accept_reject'] in ['Accept', 'Reject']:
                    entry.status = 'Accepted' if request.form['accept_reject'] == 'Accept' else 'Rejected'
                    database.commit_info()
                    journal_event = database.get_journal_event_table()
                    new_entry2 = journal_event(journal_type_before=entry.type, journal_type_after=entry.type,
                                               journal_debit_accounts_before=entry.debit_accounts, journal_debit_accounts_after=entry.debit_accounts,
                                               journal_debit_amounts_before=entry.debit_amounts, journal_debit_amounts_after=entry.debit_amounts,
                                               journal_credit_accounts_before=entry.credit_accounts, journal_credit_accounts_after=entry.credit_accounts,
                                               journal_credit_amounts_before=entry.credit_amounts, journal_credit_amounts_after=entry.credit_amounts,
                                               journal_status_before='Pending',
                                               journal_status_after='Accepted' if request.form['accept_reject'] == 'Accept' else 'Rejected',
                                               date_made=datetime.now(), event_type='Modified', username=session['username'],
                                               journal_id=entry.id)
                    database.commit_to_database(new_entry2)
                return redirect(url_for('manager_journal'))
            else:
                return render_template("manager_journal_entry.html")
        else:
            return redirect(url_for('login_page'))

    @app.route('/manager/reports/trial_balance')
    def manager_trial_balance():
        if "Manager" in session:
            username = session["Manager"]
            accounts = database.get_active_accounts()
            total_amounts = documentation.get_total_amounts(accounts)
            return render_template('manager_trial_balance.html', username=username, accounts=accounts,
                                   total_amounts=total_amounts)
        else:
            return redirect(url_for('login_page'))

    @app.route('/manager/reports/income_statement')
    def manager_income_statement():
        if"Manager" in session:
            username = session["Manager"]
            r_accounts = database.get_accounts_by_category("Revenue")
            exp_accounts = database.get_accounts_by_category("Expenses")
            total_revenue = documentation.get_total_amount(r_accounts)
            total_expense = documentation.get_total_amount(exp_accounts)
            net_total = total_revenue - total_expense
            return render_template('manager_income_statement.html', username=username, r_accounts=r_accounts,
                                   exp_accounts=exp_accounts, total_revenue=total_revenue, total_expenses=total_expense,
                                   total_netIncome=net_total)
        else:
            return redirect(url_for('login_page'))

    @app.route('/manger/reports/balance_sheet')
    def manager_balance_sheet():
        if "Manager" in session:
            username = session["Manager"]

            retained_account = database.get_account_info(149)
            r_accounts = database.get_accounts_by_category("Revenue")
            exp_accounts = database.get_accounts_by_category("Expenses")
            total_revenue = documentation.get_total_amount(r_accounts)
            total_expense = documentation.get_total_amount(exp_accounts)
            net_total = total_revenue - total_expense
            total_retained = net_total + retained_account.balance

            accounts = database.get_active_accounts()
            assets_subcategory_totals = documentation.get_subcategory_totals("Asset", database)
            total_Assets = documentation.get_category_totals(assets_subcategory_totals[1])
            liability_subcategory_totals = documentation.get_subcategory_totals("Liability", database)
            total_Liabilities = documentation.get_category_totals(liability_subcategory_totals[1])
            equity_subcategory_totals = documentation.get_subcategory_totals("Equity", database)
            total_Equity = documentation.get_category_totals(equity_subcategory_totals[1]) + total_retained
            total_LE = total_Equity + total_Liabilities
            return render_template('manager_balance_sheet.html', username=username, accounts=accounts,
                                   asset_sub_cat=assets_subcategory_totals[0],
                                   asset_sub_total=assets_subcategory_totals[1], total_assets=total_Assets,
                                   lia_sub_cat=liability_subcategory_totals[0],
                                   lia_sub_total=liability_subcategory_totals[1], total_liability=total_Liabilities,
                                   equi_sub_cat=equity_subcategory_totals[0], total_equity=total_Equity,
                                   equi_sub_total=equity_subcategory_totals[1], total_le=total_LE,
                                   total_retained=total_retained)
        else:
            return redirect(url_for('login_page'))

    @app.route('/manager/report/retained_earnings')
    def manager_retained_earnings():
        if "Manager" in session:
            username = session["Manager"]
            retained_account = database.get_account_info(149)
            r_accounts = database.get_accounts_by_category("Revenue")
            exp_accounts = database.get_accounts_by_category("Expenses")
            total_revenue = documentation.get_total_amount(r_accounts)
            total_expense = documentation.get_total_amount(exp_accounts)
            net_total = total_revenue - total_expense
            total_retained = net_total + retained_account.balance
            new_balance = total_retained - 0
            return render_template('manager_retained_earning.html', username=username, income_balance=net_total,
                                   retained_balance=retained_account.balance, dividends_amount=0,
                                   new_retained_balance=new_balance, total_retained=total_retained)
        else:
            return redirect(url_for('login_page'))

    @app.route('/manager_about')
    def manager_about():
        if "Manager" in session:
            username = session["Manager"]
            return render_template('manager_about.html', username=username)
        else:
            return redirect(url_for('login_page'))
