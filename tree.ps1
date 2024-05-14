param (
    [string]$Path = ".",
    [int]$MaxDepth = 2
)

function Get-Tree {
    param (
        [string]$Path,
        [int]$CurrentDepth,
        [int]$MaxDepth
    )

    if ($CurrentDepth -gt $MaxDepth) {
        return
    }

    $items = Get-ChildItem -Path $Path

    foreach ($item in $items) {
        Write-Output (" " * ($CurrentDepth * 2) + "|-- " + $item.Name)

        if ($item.PSIsContainer) {
            Get-Tree -Path $item.FullName -CurrentDepth ($CurrentDepth + 1) -MaxDepth $MaxDepth
        }
    }
}

Write-Output $Path
Get-Tree -Path $Path -CurrentDepth 1 -MaxDepth $MaxDepth