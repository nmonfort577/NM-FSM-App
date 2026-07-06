# Environment Guidelines for AWS Headless VM

These rules ensure the AI agent operates reliably in this controlled, headless VM environment.

## 1. Running Application Servers
- **Do NOT use `Start-Process`**: Launching interactive GUI/terminal windows (e.g. `Start-Process cmd` or `Start-Process powershell`) will fail or immediately terminate due to Windows Session Isolation (Session 0).
- **Use Background Tasks**: Always run servers (like Flask or Node.js) as background tasks under the agent's control (`run_command` in background). This keeps them alive and accessible on localhost.

## 2. Testing and Verification
- **Do NOT use `browser_subagent`**: Headless Chrome browser automation is resource-heavy and causes the host runner to crash and reset.
- **Use Programmatic Validation**: Test application endpoints using lightweight scripting (e.g., Python's `urllib` or `requests`) to verify route responses and database state.
- **Manual Verification**: Guide students to open their own browser to test the endpoints interactively.

## 3. UI Requirements
- **User ID Footnote**: Every page/screen template must include the user ID `nmonfort577` as a footnote at the top of the screen. In HTML templates, place a small, muted element right at the top of the main container:
  ```html
  <div class="text-end text-muted small mb-3">User ID: nmonfort577</div>
  ```
