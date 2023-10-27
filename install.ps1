# Define ANSI color codes for text formatting
$GREEN = [char]27 + '[32;1m'
$RED = [char]27 + '[31;1m'
$RESET = [char]27 + '[0m'

Function Test-Command {
    param (
        [string]$CommandName
    )

    $commandInfo = Get-Command -Name $CommandName -ErrorAction SilentlyContinue
    $fc = $host.UI.RawUI.ForegroundColor
    if ($commandInfo) {
        $host.UI.RawUI.ForegroundColor = "green"
        Write-Host "[+] $CommandName is available at $($commandInfo.Source)"
        $host.UI.RawUI.ForegroundColor = $fc
        return $true
    } else {
        $host.UI.RawUI.ForegroundColor = "red"
        Write-Host "[x] $CommandName is not available in the system, install $CommandName to continue."
        $host.UI.RawUI.ForegroundColor = $fc
        return $false
    }
}

# Check if required dependencies exist
Test-Command "git" | Out-Null
Test-Command "poetry" | Out-Null
Test-Command "docker" | Out-Null
$pip = Test-Command "pip" 
$pip3 = Test-Command "pip3"

$gitPath = Get-Command -Name "git" | Select-Object -ExpandProperty Source
$poetryPath = Get-Command -Name "poetry" | Select-Object -ExpandProperty Source
$dockerPath = Get-Command -Name "docker" | Select-Object -ExpandProperty Source

& $gitPath clone https://github.com/abhirambsn/kali-docker.git $env:HOME/kali-docker
cd $env:HOME/kali-docker/kalictl
& $poetryPath install  # Install script and dependencies
& $poetryPath build  # Build Dependencies
if ($pip) {
    & pip install .\dist\*.whl
} elseif ($pip3) {
    & pip3 install .\dist\*.whl
} else {
    Write-Host "[x] pip or pip3 is required to install the package"
    exit 1
}
$kalictlPath = Get-Command -Name "kalictl" | Select-Object -ExpandProperty Source

# # Create a docker network with name kali-net and subnet 10.0.0.0/16
& $dockerPath network create --subnet=10.0.0.0/16 kali-net

& $kalictlPath init  # Initialize config
& $kalictlPath build  # Build Images
& $kalictlPath start  # Start the compose stack

Write-Host "[+] Execute 'kalictl exec /bin/bash' to enter the container's shell"
Write-Host "For more usage information, use 'kalictl [<command>] --help'"

