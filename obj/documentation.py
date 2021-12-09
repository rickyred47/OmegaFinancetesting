from obj import admin_processes

ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']


def get_total_amounts(accounts):
    total_debit = 0
    total_credit = 0
    for account in accounts:
        if account.normal_side == "Left":
            if account.balance < 0:
                total_credit += (account.balance * -1)
            else:
                total_debit += account.balance
        elif account.normal_side == "Right":
            if account.balance < 0:
                total_debit += (account.balance * -1)
            else:
                total_credit += account.balance
    return total_debit, total_credit


def get_total_amount(accounts):
    amount = 0
    for account in accounts:
        amount += account.balance
    return amount


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_category_totals(totals):
    total_amount = 0
    for total in totals:
        total_amount += total
    return total_amount


def get_subcategory_totals(category, database):
    accounts = database.get_accounts_by_category(category)
    subcategories = admin_processes.subcategory_accounts(accounts)
    totals = []
    for subcategory in subcategories:
        total = 0
        for account in accounts:
            if account.subcategory == subcategory:
                total += account.balance
        totals.append(total)
    return subcategories, totals


def get_subcategory_total_number(category, database):
    accounts = database.get_accounts_by_category(category)
    subcategories = admin_processes.subcategory_accounts(accounts)
    totals = []
    for subcategory in subcategories:
        total = 0
        for account in accounts:
            if account.subcategory == subcategory:
                total += account.balance
            totals.append(total)
    return totals
