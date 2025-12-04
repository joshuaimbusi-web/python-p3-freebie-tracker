#!/usr/bin/env python3

from helpers import (
    get_session,
    list_companies,
    list_devs,
    list_freebies,
    find_company_by_id,
    find_company_by_name,
    find_dev_by_id,
    find_dev_by_name,
    find_freebie_by_id,
    create_company,
    create_dev,
    give_freebie,
    transfer_freebie,
    delete_freebie,
    company_summary,
    dev_summary,
    freebie_summary,
)

MENU = """
Choose an option:
 1) List companies
 2) List devs
 3) List freebies
 4) Create company
 5) Create dev
 6) Give freebie (company -> dev)
 7) Transfer freebie (dev -> dev)
 8) Check if dev received a specific item
 9) Oldest company
10) Delete a freebie
0) Exit
"""


def input_int(prompt, allow_blank=False):
    s = input(prompt).strip()
    if s == "" and allow_blank:
        return None
    try:
        return int(s)
    except ValueError:
        print("Please enter a valid integer.")
        return input_int(prompt, allow_blank=allow_blank)


def main():
    session = get_session()
    try:
        while True:
            print(MENU)
            choice = input("Enter choice: ").strip()
            if choice == "1":
                comps = list_companies(session)
                if not comps:
                    print("No companies found.")
                for c in comps:
                    print(company_summary(c))

            elif choice == "2":
                devs = list_devs(session)
                if not devs:
                    print("No devs found.")
                for d in devs:
                    print(dev_summary(d))

            elif choice == "3":
                frees = list_freebies(session)
                if not frees:
                    print("No freebies found.")
                for f in frees:
                    print(freebie_summary(f))

            elif choice == "4":
                name = input("Company name: ").strip()
                if name == "":
                    print("Name required.")
                    continue
                fy = input("Founding year (blank if unknown): ").strip()
                fy_val = int(fy) if fy != "" else None
                c = create_company(session, name, fy_val)
                print("Created:", company_summary(c))

            elif choice == "5":
                name = input("Dev name: ").strip()
                if name == "":
                    print("Name required.")
                    continue
                d = create_dev(session, name)
                print("Created:", dev_summary(d))

            elif choice == "6":
                # Give freebie: choose company, dev, item_name, value
                comps = list_companies(session)
                for c in comps:
                    print(company_summary(c))
                comp_id = input_int("Company ID: ")
                company = find_company_by_id(session, comp_id)
                if not company:
                    print("Company not found.")
                    continue

                devs = list_devs(session)
                for d in devs:
                    print(dev_summary(d))
                dev_id = input_int("Dev ID: ")
                dev = find_dev_by_id(session, dev_id)
                if not dev:
                    print("Dev not found.")
                    continue

                item = input("Item name: ").strip()
                if item == "":
                    print("Item name required.")
                    continue
                value = input_int("Value (integer): ")
                fb = give_freebie(session, company, dev, item, value)
                print("Created freebie:", freebie_summary(fb))

            elif choice == "7":
                # Transfer freebie
                devs = list_devs(session)
                for d in devs:
                    print(dev_summary(d))
                from_id = input_int("Giver Dev ID: ")
                from_dev = find_dev_by_id(session, from_id)
                if not from_dev:
                    print("Dev not found.")
                    continue
                # show freebies owned by from_dev
                owned = from_dev.freebies
                if not owned:
                    print(f"{from_dev.name} has no freebies to give.")
                    continue
                for f in owned:
                    print(freebie_summary(f))
                freebie_id = input_int("Freebie ID to transfer: ")
                freebie = find_freebie_by_id(session, freebie_id)
                if not freebie or freebie not in owned:
                    print("That freebie is not owned by the giver.")
                    continue

                # choose recipient
                for d in devs:
                    print(dev_summary(d))
                to_id = input_int("Recipient Dev ID: ")
                to_dev = find_dev_by_id(session, to_id)
                if not to_dev:
                    print("Recipient not found.")
                    continue

                ok = transfer_freebie(session, from_dev, to_dev, freebie)
                if ok:
                    print("Transfer successful.")
                else:
                    print("Transfer failed.")

            elif choice == "8":
                devs = list_devs(session)
                for d in devs:
                    print(dev_summary(d))
                dev_id = input_int("Dev ID: ")
                dev = find_dev_by_id(session, dev_id)
                if not dev:
                    print("Dev not found.")
                    continue
                item = input("Item name to check: ").strip()
                if dev.received_one(item):
                    print(f"Yes — {dev.name} has received '{item}'.")
                else:
                    print(f"No — {dev.name} has not received '{item}'.")

            elif choice == "9":
                # Oldest company (requires DB query)
                # Use the session; call the classmethod we wrote on Company
                from models import Company  # local import to ensure class is available
                oldest = Company.oldest_company(session)
                if oldest:
                    print("Oldest company:", company_summary(oldest))
                else:
                    print("No companies in DB.")

            elif choice == "10":
                frees = list_freebies(session)
                for f in frees:
                    print(freebie_summary(f))
                fid = input_int("Freebie ID to delete: ")
                fb = find_freebie_by_id(session, fid)
                if not fb:
                    print("No such freebie.")
                    continue
                confirm = input(f"Delete {freebie_summary(fb)}? (y/N): ").strip().lower()
                if confirm == "y":
                    delete_freebie(session, fb)
                    print("Deleted.")
                else:
                    print("Canceled.")

            elif choice == "0":
                print("Goodbye!")
                break

            else:
                print("Unknown option — choose a number from the menu.")

    finally:
        session.close()


if __name__ == "__main__":
    main()
