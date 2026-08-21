# Agent Guidelines & Operating Procedures

This environment is used by students to create and manage full AWS-based application environments. All operations must follow the rules and constraints outlined below:

## Code & Workspace Organization
- **Code Directory Location**: All code should be placed in subdirectories within a new directory called `C:\code`.
- **User ID Header/Footnote**: Display the student User ID (`nmonfort577`) as a footnote/header note at the top of each web screen now and in the future.
- **DevOps Tooling Directory Layout**: All Ansible, Packer, and Terraform configuration files belong on the control-node.internal server under `~/NM-FSM-App/devops-course/`. Terraform files specifically go in their own subdirectory: `~/NM-FSM-App/devops-course/terraform/`. The corresponding Bastion mirror path is `C:\code\NM-FSM-App\devops-course\` (with `terraform\` subdirectory). Always sync new files back to Bastion before committing.

## Process & Execution Guidelines
- **Background Tasks**: Application servers will be run as background processes under the agent's control (which is stable in this VM session).
- **Programmatic Testing**: We will use lightweight scripts for automated verification instead of resource-heavy browser tools to prevent VM memory resets.
- **No Detached GUI Windows**: We will avoid `Start-Process` since Session 0 isolation prevents GUI/terminal windows from opening.
- **No Polling Loops**: NEVER poll `manage_task status` in a loop waiting for a task to finish. The system automatically notifies the agent when a background task completes. Launch the task, then STOP calling tools and let the system wake you up with the result. Repeated polling holds up the conversation and forces the user to manually cancel tasks.

## Remote Host & Configuration Management
- **Remote Configuration Files**: When writing configuration files to remote hosts, always write them to the local scratch directory first and then copy/pipe the file over SSH to prevent PowerShell quote/variable expansion issues.
- **Custom RPM Repositories via Ansible**: When installing custom RPM repositories via Ansible on Amazon Linux/EL9 hosts, download the RPM to `/tmp` first to avoid DNF home directory access restrictions.
- **MySQL Download Server User-Agent**: The MySQL download server blocks standard Python/Ansible User-Agents, so use `curl` with a browser-like `-A` string. Also note: `dev.mysql.com` returns HTTP 403 for repo RPMs — use `repo.mysql.com` instead (e.g., `https://repo.mysql.com/mysql84-community-release-el9-1.noarch.rpm`).
- **Amazon Linux 2023 PyMySQL Package**: Remember that Amazon Linux 2023 doesn't have `python3-pymysql` in its repositories, so you'll need to install it via `pip`.
- **MySQL 8.4 Plugin Change**: MySQL 8.4 removed `mysql_native_password` as a built-in plugin. Always specify `plugin: caching_sha2_password` explicitly in `community.mysql.mysql_user` tasks to avoid the `Plugin 'mysql_native_password' is not loaded` error.

## General Principles
- **Limit Assumptions**: Limit assumptions – if there is ambiguity, ask the user for clarification.

## Git & GitHub Workflows
- **Explicit Repository Targeting with GitHub CLI (`gh`)**: When creating Pull Requests using the GitHub CLI (`gh`), if the repository has multiple remotes (e.g., `origin` and `upstream`), always check the remotes using `git remote -v` and specify the correct target fork repository using the `--repo <owner>/<repo>` flag (e.g., `--repo <userid>/NM-FSM-App`) or configure it first using `gh repo set-default` to prevent invalid base/head SHA errors.
- **Base Branch Verification**: Before checking out a feature branch or staging commits, verify that the target base branch (should always be `dev`) exists locally and on the remote. If it does not exist, create and push it first.
- **Never submit to upstream**: Never push or create PRs back to `ts0491/NM-FSM-App`. All PRs target `nmonfort577/NM-FSM-App` only.
- **Never commit `venv/`**: The virtual environment directory must never be committed. It is listed in `.gitignore`.

## Bastion ↔ Control-Node Sync Discipline
The project uses two servers: **Bastion** (this Windows VM at `C:\code\NM-FSM-App`) and **control-node.internal** (`~/NM-FSM-App`).

**Rules (MUST be followed at all times):**
- **Bastion is the Git authority**: All `git commit`, `git push`, PR creation, and merges into `main` happen **only on Bastion**.
- **Control-node is a consumer**: The control-node clones/pulls from GitHub (`https://github.com/nmonfort577/NM-FSM-App.git`) and uses `git pull` to stay up to date. It never pushes or commits.
- **Sync any control-node changes back to Bastion first**: If a file is created or modified on the control-node (e.g., by Ansible, scripts, or configuration management tasks), copy it back to Bastion via `scp` or `ssh cat` **before** committing. Never let the control-node get ahead of Bastion.
- **After every PR merge into main**: Run `git pull origin main` on the control-node to keep it in sync with the latest merged state.
- **Module 6 and beyond (Jenkins pipeline)**: Once the Jenkins pipeline is in place, all changes flow through Bastion → GitHub → Jenkins → control-node. The control-node is updated exclusively via `git pull` triggered by the pipeline. No direct file edits on the control-node.
