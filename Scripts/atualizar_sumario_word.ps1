# Abre o .docx no Word, converte as equacoes (estilo 'Equacao', escritas em UnicodeMath) em equacoes nativas,
# atualiza sumario/campos e salva (o Word precisa estar instalado)
param([string]$docx)
$w = New-Object -ComObject Word.Application
$w.Visible = $false; $w.DisplayAlerts = 0
$d = $w.Documents.Open($docx)
$n = 0
for ($i = 1; $i -le $d.Paragraphs.Count; $i++) {
    $p = $d.Paragraphs.Item($i)
    if ($p.Style.NameLocal -eq 'Equacao') {
        $r = $p.Range
        [void]$r.MoveEnd(1, -1)
        $m = $d.OMaths.Add($r)
        $n++
    }
}
if ($n -gt 0) { $d.OMaths.BuildUp() }
"equacoes: " + $n
$d.TablesOfContents | ForEach-Object { $_.Update() }
$d.Fields.Update() | Out-Null
"paginas: " + $d.ComputeStatistics(2)
$d.Save()
$d.Close($false)
$w.Quit()
