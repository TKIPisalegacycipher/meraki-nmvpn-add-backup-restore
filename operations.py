import json
from datetime import datetime


def summarize_peer_list(list_of_peers):
    # Summarizes the peers
    summary = dict()

    summary["count"] = len(list_of_peers)
    summary["peers"] = list_of_peers

    return summary


def ingest_file(filename, folder='backups'):
    # Ingests a JSON file and returns the peers
    # Expects the peers to be unwrapped
    with open(f"{folder}/{filename}", "r", encoding="utf-8") as f:
        these_peers = json.load(f)
        f.flush()

    return these_peers


def print_summary(summary, name):
    # Prints a report based on the provided summary.
    print(f"The {name} contains {summary['count']} peers.")


def backup_nmvpn_peers(
    api_session, org_id, task_id, file_suffix="nmvpn_peers_backup.json"
):
    # Backs up the current NMVPN peers
    # Unwraps the 'peers' array for simpler manipulation
    summary = get_nmvpn_peers(api_session, org_id)

    current_datetime = datetime.now().strftime("%Y-%m-%d %H%M")

    this_backup_filename = (
        f"{current_datetime} (task {task_id}, org {org_id}) {file_suffix}".replace(
            ":", "."
        )
    )

    with open(f"backups/{this_backup_filename}", "w", encoding="utf-8") as f:
        json.dump(summary["peers"], f, indent=4)
        f.flush()

    print(f"The backup was created with filename: {this_backup_filename}.")

    return summary


def restore_nmvpn_peers(
    api_session,
    org_id,
    this_backup_filename,
    task_id,
    file_suffix="nmvpn_peers_backup.json",
):
    # Restores the full set of NMVPN peers
    # Expects an unwrapped 'peers' array
    with open(f"backups/{this_backup_filename}", "r", encoding="utf-8") as f:
        these_peers = json.load(f)
        f.flush()

    # create a before backup
    before_summary = backup_nmvpn_peers(
        api_session, org_id, task_id, file_suffix="backup-before-restore.json"
    )

    # restore the peers
    restore_summary = put_nmvpn_peers(api_session, org_id, these_peers)

    # create an "after" backup
    after_summary = backup_nmvpn_peers(
        api_session, org_id, task_id, file_suffix="backup-after-restore.json"
    )

    summaries = dict()
    summaries["before"] = before_summary
    summaries["after"] = after_summary
    summaries["restore"] = restore_summary

    return summaries


def put_nmvpn_peers(api_session, org_id, list_of_peers):
    # Puts the NMVPN peers and returns a summary object which also contains the peers
    summary = summarize_peer_list(list_of_peers)

    print(f"Replacing peers with {summary['count']} peers.")

    api_session.appliance.updateOrganizationApplianceVpnThirdPartyVPNPeers(
        org_id, peers=list_of_peers
    )

    return summary


def get_nmvpn_peers(api_session, org_id):
    # Gets the NMVPN peers and returns a summary object which also contains the peers
    print(f"Retrieving peers for {org_id}.")

    these_peers = api_session.appliance.getOrganizationApplianceVpnThirdPartyVPNPeers(
        org_id
    )["peers"]

    summary = summarize_peer_list(these_peers)

    print(f"Found {summary['count']} peers in current configuration.")

    return summary


def summarize_current_peers(api_session, org_id):
    # Gets the peers and returns the summary
    summary = get_nmvpn_peers(api_session, org_id)
    return summary


def preview_changes(api_session, org_id, this_filename, this_folder='backups'):
    before_summary = summarize_current_peers(api_session, org_id)

    # ingest the file and count the peers

    after_summary = dict()
    after_summary["count"] = len(ingest_file(this_filename, folder=this_folder))
    after_summary["peers"] = ingest_file(this_filename, folder=this_folder)

    print(f"The current cloud config has {before_summary['count']} peers.")
    print(f'The selected file has {after_summary["count"]} peers.')


def add_nmvpn_peers(
    api_session,
    org_id,
    this_filename,
    task_id
):
    # Adds one or more NMVPN peers to the existing config
    # Expects an unwrapped 'peers' array
    with open(f"additions/{this_filename}", "r", encoding="utf-8") as f:
        these_peers = json.load(f)
        f.flush()

    # create a before backup
    before_summary = backup_nmvpn_peers(
        api_session, org_id, task_id, file_suffix="backup-before-restore.json"
    )

    combined_summary = dict()
    combined_summary['peers'] = before_summary['peers'] + these_peers
    combined_summary['count'] = len(combined_summary['peers'])

    # restore the peers
    restore_summary = put_nmvpn_peers(api_session, org_id, combined_summary['peers'])

    # create an "after" backup
    after_summary = backup_nmvpn_peers(
        api_session, org_id, task_id, file_suffix="backup-after-restore.json"
    )

    summaries = dict()
    summaries["before"] = before_summary
    summaries["after"] = after_summary
    summaries["restore"] = restore_summary
    summaries["combined"] = restore_summary

    return summaries

