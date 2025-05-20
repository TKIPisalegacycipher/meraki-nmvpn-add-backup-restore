# Meraki NMVPN Add Backup Restore

_A straightforward way to add, backup, and restore non-Meraki VPN peers._

## Usage

### Setup

First, if you don't already have one, [create your Meraki Dashboard API
key](https://documentation.meraki.com/General_Administration/Other_Topics/Cisco_Meraki_Dashboard_API). 

Then, add your API key to a user environment variable called `MERAKI_DASHBOARD_API_KEY` and reboot your computer. If
you are not sure how to do this, please see the guide at the bottom of this README. Once rebooted, continue with the 
**Operation** section.

### Operation

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

## Setting your API key as a user environment variable

These instructions are provided as a courtesy.

### Windows 11
1. **Open the Environment Variables Settings**:
   - Press `Win + S` to open the search bar.
   - Type **"Environment Variables"** and select **"Edit the system environment variables"**.
   - In the System Properties window, click **"Environment Variables"**.

2. **Add a User Environment Variable**:
   - In the **User variables** section, click **"New"**.
   - For **Variable Name**, enter: `MERAKI_DASHBOARD_API_KEY`.
   - For **Variable Value**, enter your API key (e.g., `123456abcdef`).
   - Click **OK** to save.

3. **Apply and Close**:
   - Click **OK** in the Environment Variables window.
   - Click **OK** in the System Properties window to close it.

4. **Verify**:
   - Open a new Command Prompt or PowerShell window.
   - Run: `echo %MERAKI_DASHBOARD_API_KEY%`.
   - If correctly set, it will display the API key. You may need to reboot your computer for it to take effect.

### macOS
1. **Open the Terminal**:
   - Press `Cmd + Space` to open Spotlight and type **"Terminal"**. Press Enter.

2. **Edit the Shell Configuration File**:
   - Determine your default shell by running: `echo $SHELL`.
     - If it is `zsh` (default in macOS Catalina and later), edit the `~/.zshrc` file.
     - If it is `bash`, edit the `~/.bash_profile` file.
   - Open the appropriate file in a text editor. For example:
     - `nano ~/.zshrc` (for zsh) or `nano ~/.bash_profile` (for bash).

3. **Add the Environment Variable**:
   - Add the following line to the file:
     ```bash
     export MERAKI_DASHBOARD_API_KEY="123456abcdef"
     ```

4. **Apply the Changes**:
   - Save and close the file (`Ctrl + O`, then `Enter`, then `Ctrl + X` for nano).
   - Run the command: `source ~/.zshrc` (or `source ~/.bash_profile` for bash) to apply the changes.

5. **Verify**:
   - Run: `echo $MERAKI_DASHBOARD_API_KEY`.
   - If correctly set, it will display the API key.

### Ubuntu
1. **Open the Terminal**:
   - Press `Ctrl + Alt + T` to open the terminal.

2. **Edit the Shell Configuration File**:
   - Determine your default shell by running: `echo $SHELL`.
     - If it is `bash` (default), edit the `~/.bashrc` file.
     - If it is `zsh`, edit the `~/.zshrc` file.
   - Open the appropriate file in a text editor. For example:
     - `nano ~/.bashrc` (for bash) or `nano ~/.zshrc` (for zsh).

3. **Add the Environment Variable**:
   - Add the following line to the file:
     ```bash
     export MERAKI_DASHBOARD_API_KEY="123456abcdef"
     ```

4. **Apply the Changes**:
   - Save and close the file (`Ctrl + O`, then `Enter`, then `Ctrl + X` for nano).
   - Run the command: `source ~/.bashrc` (or `source ~/.zshrc` for zsh) to apply the changes.

5. **Verify**:
   - Run: `echo $MERAKI_DASHBOARD_API_KEY`.
   - If correctly set, it will display the API key.