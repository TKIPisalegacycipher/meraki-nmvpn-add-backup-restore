import os

import meraki

d = meraki.DashboardAPI(suppress_logging=True)


def select_organization(api_session):
    # Selects an organization from those the API key can access
    org_selected = False

    these_organizations = api_session.organizations.getOrganizations()

    while not org_selected:
        print("Which organization would you like to use?")

        valid_org_ids = [organization["id"] for organization in these_organizations]

        for organization in these_organizations:
            print(f"\tID {organization['id']}: {organization['name']}")

        chosen_org_id = input("Type or paste the organization ID: ")

        if chosen_org_id in valid_org_ids:
            org_selected = True
            print(f"Organization {chosen_org_id} selected.")
        else:
            print(f"Invalid organization ID: {chosen_org_id}")

    return chosen_org_id


def select_file(file_folder):
    # Selects a file from a list of files in a folder
    file_selected = False

    these_files = os.listdir(file_folder)

    if not these_files:
        print("No file to select; folder is empty.")
        return None

    while not file_selected:
        print("Which file would you like to use?")

        for idx, name in enumerate(these_files, start=1):
            print(f"{idx}. {name}")

        try:
            input_index: int = int(input(
                "Type the index number of the file you would like to use: "
            ))
        except ValueError:
            print("Invalid input. Please type the number corresponding to the file you'd like to use.")

        if 1 <= input_index <= len(these_files):
            file_selected = True
            print(f"File {input_index} selected.")
        else:
            print("There is no file with that index. Please try again.")

    return these_files[input_index-1]


