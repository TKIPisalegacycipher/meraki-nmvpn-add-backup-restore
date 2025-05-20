# Meraki NMVPN Add Backup Restore

_A straightforward way to add, backup, and restore non-Meraki VPN peers._

## Usage

Clone the repo, then run `python main.py` from your terminal. You will see the following options:

```aiignore
Please select from one of the following options:
1. Summarize the current list of peers.
2. Backup the current list of peers to a file.
3. Restore a backup file to the current config, overwriting everything.
4. Add one or more peers to the current config.
5. Remove all peers.
```
### 1. Summarize the current list of peers

This non-destructive operation will report how many peers are in your current cloud config. It does not make any
changes.

### 2. Backup the current list of peers to a file.

This non-destructive operation will create a local backup of your current cloud config, in the folder "backups". It does
not make any changes. Normally, you'll start here.

### 3. Restore a backup file to the current config, overwriting everything.

Use an existing local backup file to overwrite everything that's in the cloud. Before making any changes, it will create
additional backups, snapshotting the before and after configurations. If you have a large number of peers (1000+), you 
may encounter a timeout error. The script will automatically retry and inform you when the operation is complete.

### 4. Add one or more peers to the current config.

Before choosing this option, first copy the template file (templates/template_one_or_more_peers.json) to the `additions`
folder and update it with the peer(s) you'd like to add. You can add multiple peers to the list, separated by commas 
(e.g., `[{peer 1 info}, {peer 2 info}]`).

Then, choose this option, and select your additions file. Confirm the changes, and they will be added. If you have a
large number of peers (1000+), you may encounter a timeout error. The script will automatically retry and inform you 
when the operation is complete.

### 5. Remove all peers.

If you'd like to remove all peers from the cloud, this will do so. Ensure you have a backup _before_ doing this.