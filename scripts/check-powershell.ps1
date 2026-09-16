<#
.SYNOPSIS
    Static checks over every PowerShell script in this repository.

.DESCRIPTION
    Two things that only show up when a script actually runs, on a machine none of the
    tests can reach, and which the parser is perfectly happy with:

    * **A local variable that shadows a parameter by case alone.** PowerShell variable
      names are case-insensitive, so $architecture and $Architecture are one variable.
      Writing to the lower-case one assigns to the parameter - and if that parameter
      has a ValidateSet, the script dies on a value it never received from anybody.
      That is exactly how the installer broke.

    * **Non-ASCII characters.** Windows PowerShell reads a .ps1 with no byte-order mark
      as ANSI, so an em dash arrives on screen as mojibake.

    Anything the parser itself rejects is reported too.

.EXAMPLE
    pwsh -File scripts\check-powershell.ps1
#>
[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'

$scripts = Get-ChildItem -Path $PSScriptRoot -Filter '*.ps1' | Sort-Object Name
$problems = @()

foreach ($script in $scripts) {
    $errors = $null
    $tokens = $null
    $ast = [System.Management.Automation.Language.Parser]::ParseFile(
        $script.FullName, [ref]$tokens, [ref]$errors
    )

    if ($errors) {
        foreach ($parseError in $errors) {
            $problems += "$($script.Name):$($parseError.Extent.StartLineNumber) $($parseError.Message)"
        }
        continue
    }

    # Scope matters: a parameter of one function is a different variable from a
    # same-named local in another, and flagging those would be noise. What is worth
    # reporting is an assignment sitting in the very scope that declares the parameter.
    $scopeOf = {
        param($node)
        $walk = $node.Parent
        while ($null -ne $walk) {
            if ($walk -is [System.Management.Automation.Language.FunctionDefinitionAst]) { return $walk }
            $walk = $walk.Parent
        }
        return $null
    }

    $parameters = @()
    foreach ($parameter in $ast.FindAll(
            { $args[0] -is [System.Management.Automation.Language.ParameterAst] }, $true)) {
        $parameters += [pscustomobject]@{
            Name  = $parameter.Name.VariablePath.UserPath
            Scope = & $scopeOf $parameter
        }
    }

    $assignments = $ast.FindAll(
        { $args[0] -is [System.Management.Automation.Language.AssignmentStatementAst] }, $true
    )
    foreach ($assignment in $assignments) {
        $left = $assignment.Left
        if ($left -isnot [System.Management.Automation.Language.VariableExpressionAst]) { continue }
        $name = $left.VariablePath.UserPath
        $scope = & $scopeOf $assignment
        foreach ($parameter in $parameters) {
            if ($parameter.Scope -ne $scope) { continue }
            # Same name, different spelling: one variable, and almost certainly two
            # things that were meant to be separate.
            if ($name -eq $parameter.Name -and
                -not $name.Equals($parameter.Name, [System.StringComparison]::Ordinal)) {
                $problems += (
                    "$($script.Name):$($left.Extent.StartLineNumber) " +
                    "`$$name assigns to the parameter `$$($parameter.Name) - " +
                    'PowerShell variable names are case-insensitive'
                )
            }
        }
    }

    $content = [System.IO.File]::ReadAllText($script.FullName)
    foreach ($character in $content.ToCharArray()) {
        if ([int]$character -gt 126) {
            $problems += "$($script.Name) contains non-ASCII (U+{0:X4})" -f [int]$character
            break
        }
    }

    Write-Host "  checked $($script.Name)"
}

Write-Host ''
if ($problems.Count -gt 0) {
    foreach ($problem in $problems) { Write-Host "FAIL  $problem" }
    throw "$($problems.Count) problem(s) in the PowerShell scripts"
}
Write-Host "$($scripts.Count) scripts, nothing to report."
