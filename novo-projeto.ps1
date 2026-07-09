param(
    [Parameter(Mandatory)]
    [string]$Nome
)

$base = $PSScriptRoot
$template = Join-Path $base "projetos\.template"
$destino = Join-Path $base "projetos\$Nome"

if (Test-Path $destino) {
    Write-Error "Projeto '$Nome' ja existe em projetos\$Nome"
    exit 1
}

# Copia o template
Copy-Item -Recurse $template $destino

# Ajusta o pyproject.toml com o nome do projeto
$pyproject = Join-Path $destino "pyproject.toml"
(Get-Content $pyproject) -replace "NOME_PROJETO", $Nome | Set-Content $pyproject -Encoding utf8

# Cria src/<nome>/__init__.py
$slug = $Nome -replace "-", "_"
$srcDir = Join-Path $destino "src\$slug"
New-Item -ItemType Directory -Force $srcDir | Out-Null
New-Item -ItemType File -Force (Join-Path $srcDir "__init__.py") | Out-Null

# Remove o .gitkeep
$gitkeep = Join-Path $destino "src\.gitkeep"
if (Test-Path $gitkeep) { Remove-Item $gitkeep }

# Cria .env a partir do .env.example do workspace
$envExample = Join-Path $base ".env.example"
$envDest = Join-Path $destino ".env"
Copy-Item $envExample $envDest

Write-Host ""
Write-Host "Projeto '$Nome' criado em projetos\$Nome" -ForegroundColor Green
Write-Host ""
Write-Host "Proximos passos:" -ForegroundColor Cyan
Write-Host "  1. Edite projetos\$Nome\pyproject.toml e descomente as deps necessarias"
Write-Host "  2. Rode: uv sync"
Write-Host "  3. Configure projetos\$Nome\.env com suas chaves de API"
Write-Host ""
