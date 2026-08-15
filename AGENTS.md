# Agent Guidelines & Operating Procedures

This environment is used by students to create and manage full AWS-based application environments. All operations must follow the rules and constraints outlined below:

## Code & Workspace Organization
- **Code Directory Location**: All code should be placed in subdirectories within a new directory called `C:\code`.
- **User ID Header/Footnote**: Display the student User ID (`nmonfort577`) as a footnote/header note at the top of each web screen now and in the future.

## Process & Execution Guidelines
- **Background Tasks**: Application servers will be run as background processes under the agent's control (which is stable in this VM session).
- **Programmatic Testing**: We will use lightweight scripts for automated verification instead of resource-heavy browser tools to prevent VM memory resets.
- **No Detached GUI Windows**: We will avoid `Start-Process` since Session 0 isolation prevents GUI/terminal windows from opening.

## Remote Host & Configuration Management
- **Remote Configuration Files**: When writing configuration files to remote hosts, always write them to the local scratch directory first and then copy/pipe the file over SSH to prevent PowerShell quote/variable expansion issues.
- **Custom RPM Repositories via Ansible**: When installing custom RPM repositories via Ansible on Amazon Linux/EL9 hosts, download the RPM to `/tmp` first to avoid DNF home directory access restrictions.
- **MySQL Download Server User-Agent**: Keep in mind that the MySQL download server blocks standard Python User-Agents, so use `curl` or set a custom `User-Agent` header when downloading repository RPMs.
- **Amazon Linux 2023 PyMySQL Package**: Remember that Amazon Linux 2023 doesn't have `python3-pymysql` in its repositories, so you'll need to install it via `pip`.

## General Principles
- **Limit Assumptions**: Limit assumptions – if there is ambiguity, ask the user for clarification.

## Git & GitHub Workflows
- **Explicit Repository Targeting with GitHub CLI (`gh`)**: When creating Pull Requests using the GitHub CLI (`gh`), if the repository has multiple remotes (e.g., `origin` and `upstream`), always check the remotes using `git remote -v` and specify the correct target fork repository using the `--repo <owner>/<repo>` flag (e.g., `--repo <userid>/NM-FSM-App`) or configure it first using `gh repo set-default` to prevent invalid base/head SHA errors.
- **Base Branch Verification**: Before checking out a feature branch or staging commits, verify that the target base branch (should always be `dev`) exists locally and on the remote. If it does not exist, create and push it first.
