import common as common
import operations as ops
import meraki
import random

VERSION = '0.1'

d = meraki.DashboardAPI(
    caller=f"NMVPNAddBackupRestore/{VERSION} Kuchta",
    single_request_timeout=120,
)

selected_org_id = common.select_organization(d)

done = False

while not done:
    task_id = random.randint(1, 999999)

    print("Please select from one of the following options:")
    print("1. Summarize the current list of peers.")
    print("2. Back up the current list of peers to a file.")
    print("3. Restore a backup file to the current config, overwriting everything.")
    print("4. Add one or more peers to the current config.")
    print("5. Remove all peers.")
    this_choice: str = input("What would you like to do? Select 1-5: ")

    match this_choice:
        case "1":
            # Summarize the current config
            print("")
            summary = ops.summarize_current_peers(d, selected_org_id)
            print("")
        case "2":
            # Back up the current config
            print("")
            summary = ops.backup_nmvpn_peers(d, selected_org_id, task_id)
            print("")
        case "3":
            # Restore a config
            print("")
            selected_file = common.select_file("backups")
            if selected_file:
                ops.preview_changes(d, selected_org_id, selected_file)
                print(
                    "Are you sure you want to replace all NMVPN peers with those contained in the backup?"
                )
                if input("y/N: ").lower() == "y":
                    summaries = ops.restore_nmvpn_peers(
                        d, selected_org_id, selected_file, task_id
                    )
                    print("")
                    if summaries["after"]["count"] == summaries["restore"]["count"]:
                        print("SUCCESS: The peers were successfully restored.")
                    else:
                        print(
                            "There was an error. Please check the Python log and try again."
                        )
                    print("")
                else:
                    print("Canceling at user's request.")
            print("")
        case "4":
            # Add one or more peers
            print("")
            selected_file = common.select_file("additions")
            if selected_file:
                ops.preview_changes(
                    d, selected_org_id, selected_file, this_folder="additions"
                )
                print("Would you like to add the peers from the selected file?")
                if input("y/N: ").lower() == "y":
                    summaries = ops.add_nmvpn_peers(
                        d, selected_org_id, selected_file, task_id
                    )
                    print("")
                    if summaries["combined"]["count"] == summaries["after"]["count"]:
                        print("SUCCESS: The peers were successfully added.")
                    else:
                        print(
                            "There was an error. Please check the Python log and try again."
                        )
                    print("")
                else:
                    print("Canceling at user's request.")
            print("")
        case "5":
            print("")
            summary = ops.summarize_current_peers(d, selected_org_id)
            if summary["count"] > 0:
                print(f"This will delete all of {summary['count']} peers.")
                input_delete = input("Would you like to continue? (y/N): ")
                if input_delete == "y":
                    summary = ops.put_nmvpn_peers(d, selected_org_id, [])
                    print("")
                    if summary["count"] == 0:
                        print("SUCCESS: All peers were removed.")
                    else:
                        print(
                            "There was an error. Please check the Python log and try again."
                        )
                    print("")
                else:
                    print("Aborting.")
                    print("")
            else:
                print("There are no peers to delete.")
                print('')
        case _:
            done = True

