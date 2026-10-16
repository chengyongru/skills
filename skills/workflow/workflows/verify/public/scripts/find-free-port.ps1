param(
  [int]$Count = 1
)

$ErrorActionPreference = "Stop"

if ($Count -lt 1) {
  throw "Count must be at least 1."
}

$ports = New-Object System.Collections.Generic.List[int]
$listeners = New-Object System.Collections.Generic.List[System.Net.Sockets.TcpListener]

try {
  for ($i = 0; $i -lt $Count; $i++) {
    $listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Loopback, 0)
    $listener.Start()
    $listeners.Add($listener)
    $ports.Add($listener.LocalEndpoint.Port)
  }
} finally {
  foreach ($listener in $listeners) {
    $listener.Stop()
  }
}

$ports | ForEach-Object { Write-Output $_ }
