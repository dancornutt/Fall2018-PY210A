#!/usr/bin/env python3

"""
mailroom assignment [-1]
"""
from operator import itemgetter
from collections import OrderedDict
from mailroom_oo.donor_models import Donor_Collection
from mailroom_oo.donor_models import Donor

WELCOME_PROMPT = (
    "\nWelcome to the main menu, please select from the following:\n"
    "1 - Send Thank You to a single donor.\n"
    "2 - Create a report from Donor history.\n"
    "3 - Send letters to all donors.\n"
    "4 - Modify Donor Database.\n"
    "5 - Quit\n"
    )

DATABASE_PROMPT = (
    "\nWelcome to the database menu, please select from the following:\n"
    "1 - See list of donors.\n"
    "2 - Add new donor or edit existing.\n"
    "3 - Quit this menu.\n"
)

## TODO: Return donor with dict.get -- returns donor or none if not found
def check_donor(name):
    """Returns True if user is in DB.
    :param1: name of donor
    """
    return name in DONORS.db.keys()


def gen_letter(name):
    return DONORS.db[name].write_letter()

def write_donor(name):
    """Writes thank you letter to file"""
    with open(name.replace(" ", "") + "_thank_you.txt", 'w') as f_out:
        f_out.write(gen_letter(name))


def thank_you(donor="", all_users=False):
    """Writes thank you letter to file, if all_users is True write letters for all users in database
    """
    if all_users:
        for d in DONORS.db.keys():
            write_donor(d)
    else:
        donor = input("Type Donor Name =>").title()
        if check_donor(donor):
            write_donor(donor)
        else:
            print("Sorry I could not find the donor, exiting...\n")

def donor_db():
    """Editing Donor Menu"""
    menu_selection(DATABASE_PROMPT, DATABASE_DISPATCH)


def edit_donor():
    answer = input("input donor name=> ").strip().title()
    if answer:
        add_donation(answer)
    else:
        print("The name must be letters only, returning...")

def add_donation(donor_name):
    """adds donation to donor records, adds donor if new donor

    :param1: donar name
    """
    donation = add_money()
    if donation:
        #TODO might break at setdefault, also make alter to check it you want to add donor
        if not donor_name in DONORS.db.keys():
            DONORS.db[donor_name] = Donor(donor_name, donation)
        else:
            DONORS.db[donor_name].add_donation(donation)
        print(
            "Thank you {} for your donation of ${:,.2f} dollars!".format(
                donor_name, donation)
        )


def add_money():
    """Takes input from user, validates donation

    :returns: donation amount or None if donation is invalid.
    """
    donation = input("Please enter the donor amount larger than 0.01 => $")
    try:
        if float(donation) < 0.01:
            raise ValueError
    except ValueError:
        print("Donation Error, numbers only. Value must be number greater than 0.01")
        return None
    else:
        return float(donation)


def thank_you_all():
    """Writes thank you email to all users"""
    thank_you(all_users=True)


def report():
    """Finds column widths, sorts donors based on amount donated.
    :returns: report string
    """
    rpt_sheet = []
    len_col = OrderedDict({
        "n_size": len("Donor Name"),
        "t_size" : len("Total Given"),
        "ng_size": len("Num Gifts"),
        "ag_size": len("Average Gift"),
        "nm": "Donor Name",
        "tot": "Total Given",
        "ng": "Num Gifts",
        "ag": "Average Gift"
        })

    for name, d in DONORS.db.items():
        #finds max column sizes
        if len(d.donor_name) > len_col["n_size"]:
            len_col["n_size"] = len(d.donor_name)
        if len(str(d.sum_donations)) > len_col["t_size"]:
            len_col["t_size"] = len(str(d.sum_donations))
        if len(str(d.num_donations)) > len_col["ng_size"]:
            len_col["ng_size"] = len(str(d.num_donations))
        if len(str(d.avg_donation)) > len_col["ag_size"]:
            len_col["ag_size"] = len(str(d.avg_donation))
        #creates report data
        rpt_sheet.append((
            d.donor_name, d.sum_donations, d.num_donations, d.avg_donation
            ))
    rpt_sheet.sort(key=return_total, reverse=True)

    #compiles data into wanted format
    #header
    sheet = (
        "{nm:{n_size}} | {tot:{t_size}} | {ng:{ng_size}} |{ag:<{ag_size}}\n".format(
            **len_col) + ("-" * sum(list(len_col.values())[:4]))
    )
    #data
    for d in rpt_sheet:
        sheet = sheet + (
            "\n{:{n_size}} |${:>{t_size},.2f} | {:>{ng_size}} |$ {:<{ag_size},.2f}"
            .format(*d, **len_col)
        )
    return sheet


def make_report():
    """Prints report"""
    info = report()
    print(info)

def return_total(elem):
    """sorting function for list"""
    return elem[1]


def donor_list():
    """prints donor in dict"""
    DONORS.list_donors()


def unknown():
    """Handles unknown user input"""
    print("That is not a valid response!")


def quit_menu():
    """Quits menu, returns 'exit menu'. """
    print("Quitting this menu now.")
    return "exit menu"


def menu_selection(prompt, dispatch_dict):
    """dispatch function for mailroom"""
    while True: #this loops forever, until quit is selected
        response = input(prompt).strip()
        response = response[:1].lower()
        if dispatch_dict.get(response, unknown)() == "exit menu":
            break

MAIN_DISPATCH = {
    "1": thank_you,
    "2": make_report,
    "3": thank_you_all,
    "4": donor_db,
    "5": quit_menu,
    }

DATABASE_DISPATCH = {
    "1": donor_list,
    "2": edit_donor,
    "3": quit_menu
}

if __name__ == "__main__":
    DONORS = Donor_Collection()
    menu_selection(WELCOME_PROMPT, MAIN_DISPATCH)
