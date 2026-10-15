# Abre o .docx no Word, atualiza sumario/campos e salva (o Word precisa estar instalado)
param([string]$docx)
$w = New-Object -ComObject Word.Application
$w.Visible = $false; $w.DisplayAlerts = 0
$d = $w.Documents.Open($docx)
$d.TablesOfContents | ForEach-Object { $_.Update() }
$d.Fields.Update() | Out-Null
"paginas: " + $d.ComputeStatistics(2)
$d.Save()
$d.Close($false)
$w.Quit()
