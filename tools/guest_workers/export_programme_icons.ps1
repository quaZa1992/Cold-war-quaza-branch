# IMPERIA CW — Cold War: Guest-worker agreements and diaspora policy.
# COLDWAR: export the ImageGen masters; this script does not draw the artwork.
# Requires FFmpeg. Keep native64x64 sprites and avoid lossy DXT block compression.
$ErrorActionPreference = 'Stop'
$iconExportRoot = (Resolve-Path (Join-Path $PSScriptRoot '../..')).Path
$iconExportTextureDirectory = Join-Path $iconExportRoot 'gfx/interface/ideas/nat_ideas'
$iconExportFfmpeg = (Get-Command ffmpeg -ErrorAction Stop).Source
$iconExportDefinitions = @(
    @{ Name = 'mdcw_gw_overseas_employment'; Master = 'COLDWAR_gw_overseas_employment_master.png' },
    @{ Name = 'mdcw_gw_recruitment'; Master = 'COLDWAR_gw_recruitment_master.png' }
)

foreach ($iconExportDefinition in $iconExportDefinitions) {
    $iconExportMaster = Join-Path $PSScriptRoot ('art/source/' + $iconExportDefinition.Master)
    if (-not (Test-Path -LiteralPath $iconExportMaster -PathType Leaf)) {
        throw ('Missing ImageGen master: ' + $iconExportMaster)
    }
    $iconExportPng = Join-Path $iconExportTextureDirectory ($iconExportDefinition.Name + '.png')
    $iconExportDds = Join-Path $iconExportTextureDirectory ($iconExportDefinition.Name + '.dds')
    # Premultiply during filtering so transparent borders cannot bleed black
    # into the metal rim, then restore the straight alpha expected by the DDS.
    & $iconExportFfmpeg -hide_banner -loglevel error -y -i $iconExportMaster `
        -vf 'format=gbrap,premultiply=inplace=1,scale=64:64:flags=lanczos,unpremultiply=inplace=1,format=rgba' `
        -frames:v 1 $iconExportPng
    if ($LASTEXITCODE -ne 0) { throw ('FFmpeg resize failed: ' + $iconExportDefinition.Name) }

    $iconExportRaw = [System.IO.Path]::GetTempFileName()
    try {
        & $iconExportFfmpeg -hide_banner -loglevel error -y -i $iconExportPng `
            -frames:v 1 -pix_fmt rgba -f rawvideo $iconExportRaw
        if ($LASTEXITCODE -ne 0) { throw ('FFmpeg RGBA export failed: ' + $iconExportDefinition.Name) }
        $iconExportPixels = [System.IO.File]::ReadAllBytes($iconExportRaw)
        if ($iconExportPixels.Length -ne 64 * 64 * 4) { throw 'Unexpected RGBA payload size' }
        # DDSD_CAPS|HEIGHT|WIDTH|PITCH|PIXELFORMAT; no mipmaps. Explicit masks
        # match FFmpeg's byte sequence R,G,B,A, preserving every alpha value.
        [uint32[]]$iconExportHeader = @(124, 4111, 64, 64, 256, 0, 0) + (@(0) * 11) +
            @(32, 65, 0, 32, 255, 65280, 16711680, 4278190080, 4096, 0, 0, 0, 0)
        if ($iconExportHeader.Length -ne 31) { throw 'Invalid DDS header length' }
        $iconExportStream = [System.IO.MemoryStream]::new()
        $iconExportWriter = [System.IO.BinaryWriter]::new($iconExportStream)
        try {
            $iconExportWriter.Write([System.Text.Encoding]::ASCII.GetBytes('DDS '))
            foreach ($iconExportField in $iconExportHeader) { $iconExportWriter.Write($iconExportField) }
            $iconExportWriter.Write($iconExportPixels)
            $iconExportWriter.Flush()
            if ($iconExportStream.Length -ne 16512) { throw 'Invalid DDS output size' }
            [System.IO.File]::WriteAllBytes($iconExportDds, $iconExportStream.ToArray())
        }
        finally {
            $iconExportWriter.Dispose()
            $iconExportStream.Dispose()
        }
    }
    finally {
        Remove-Item -LiteralPath $iconExportRaw -ErrorAction SilentlyContinue
    }
    Write-Output ($iconExportDefinition.Name + ': native64x64 PNG + uncompressed RGBA DDS exported')
}
