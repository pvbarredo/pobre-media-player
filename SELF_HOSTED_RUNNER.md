# Self-Hosted GitHub Runner Setup

This guide helps you set up and use your Windows PC as a GitHub Actions runner for building the Pobre Media Player.

## Setting Up Your Self-Hosted Runner

1. **Go to your GitHub repository** → Settings → Actions → Runners

2. **Click "New self-hosted runner"** and select **Windows**

3. **Follow the setup commands** provided by GitHub. They'll look like this:

   ```powershell
   # Download the runner
   mkdir actions-runner; cd actions-runner
   Invoke-WebRequest -Uri https://github.com/actions/runner/releases/download/v2.xxx.x/actions-runner-win-x64-2.xxx.x.zip -OutFile actions-runner-win-x64-2.xxx.x.zip
   Add-Type -AssemblyName System.IO.Compression.FileSystem
   [System.IO.Compression.ZipFile]::ExtractToDirectory("$PWD/actions-runner-win-x64-2.xxx.x.zip", "$PWD")
   
   # Configure the runner
   ./config.cmd --url https://github.com/YOUR-USERNAME/pobre-media-player --token YOUR-TOKEN
   ```

4. **Add labels during configuration**:
   - When prompted for labels, add: `windows` (in addition to default labels)
   - This allows the workflow to specifically target your Windows runner

5. **Start the runner**:

   ```powershell
   # One-time run
   ./run.cmd
   
   # OR install as a Windows service (runs automatically)
   ./svc.install.cmd
   ./svc.start.cmd
   ```

## Workflows Created

### 1. Build on Self-Hosted Runner (`.github/workflows/build-self-hosted.yml`)
- **Triggers**: Push to main/master, pull requests, or manual dispatch
- **Runner**: Your self-hosted Windows PC
- **Use case**: Regular development builds

### 2. Build and Release (`.github/workflows/release.yml`)
- **Triggers**: Git tags (v*)
- **Runners**: GitHub-hosted (Windows + Linux)
- **Use case**: Official releases with both platforms

## Usage

### Option 1: Use Both Workflows
- Keep both workflows active
- Self-hosted workflow runs on regular commits
- Release workflow runs on tagged releases using GitHub runners

### Option 2: Manual Trigger
You can manually trigger the self-hosted build:
1. Go to **Actions** tab in GitHub
2. Select "Build on Self-Hosted Runner"
3. Click "Run workflow"
4. Select branch and click "Run workflow"

## Linux Runner Setup

If you also have a Linux self-hosted runner, follow similar steps:

1. **Download and configure the Linux runner** from GitHub Settings → Actions → Runners
2. **Add the `linux` label** during configuration
3. **Install system dependencies for PyQt6**:
   ```bash
   sudo apt-get update
   sudo apt-get install -y qt6-base-dev libgl1-mesa-dev \
     libxcb-xinerama0 libxcb-cursor0 libxkbcommon-x11-0 \
     libxcb-icccm4 libxcb-image0 libxcb-keysyms1 \
     libxcb-randr0 libxcb-render-util0 libxcb-shape0
   ```
4. **Start the runner as a service**:
   ```bash
   sudo ./svc.sh install
   sudo ./svc.sh start
   ```

## Troubleshooting

### Runner Not Picking Up Jobs
- Verify runner is online: Check Settings → Actions → Runners
- Ensure labels match: `runs-on: [self-hosted, windows]` or `[self-hosted, linux]`
- Check runner service is running: `./svc.status.cmd` (Windows) or `sudo ./svc.sh status` (Linux)

### Build Failures

#### Windows
- Ensure Python 3.11+ is installed on your PC
- Verify all dependencies can be installed
- Check runner has internet access for pip installs
- **PowerShell execution policy error**: Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force`

#### Linux
- **PyQt6 build errors**: Install Qt6 development libraries (see Linux Runner Setup above)
- Ensure Python 3.11+ is installed
- Runner needs sudo privileges for installing system packages
- Check that the runner user can execute sudo without password prompt (add to sudoers)

### Runner Performance
- The runner uses your PC's resources when building
- You can pause the service when not needed: `./svc.stop.cmd`
- Restart when needed: `./svc.start.cmd`

## Security Notes

- Self-hosted runners should only be used for repositories you trust
- Don't use self-hosted runners for public repositories with external contributors
- The runner has access to your PC's file system and resources

## Next Steps

1. Set up the runner following the steps above
2. Commit and push the new workflow file
3. Push a commit to main branch to trigger your first self-hosted build
4. Monitor the Actions tab to see your PC building the project!
