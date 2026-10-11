$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$null=[Windows.Storage.StorageFile,Windows.Storage,ContentType=WindowsRuntime]
$null=[Windows.Graphics.Imaging.BitmapDecoder,Windows.Graphics.Imaging,ContentType=WindowsRuntime]
$null=[Windows.Media.Ocr.OcrEngine,Windows.Foundation,ContentType=WindowsRuntime]
$awaiter=([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object {$_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.IsGenericMethod})[0]
function Await-WinRT($operation,$type) {
 $task=$awaiter.MakeGenericMethod($type).Invoke($null,@($operation)); try {$task.Wait()} catch {throw $task.Exception.InnerException}; $task.Result
}
$engine=[Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
$base=Join-Path $PSScriptRoot '普林斯顿阅读'
foreach($volume in @('全书')) {
 $dest=Join-Path $base ($volume+'.jsonl')
 $writer=New-Object System.IO.StreamWriter($dest,$true,(New-Object System.Text.UTF8Encoding($false)))
 try {
  foreach($pic in (Get-ChildItem -LiteralPath (Join-Path $base $volume) -Filter '*.png' | Sort-Object Name | Where-Object { [int]$_.BaseName -ge 662 })) {
   $file=Await-WinRT ([Windows.Storage.StorageFile]::GetFileFromPathAsync($pic.FullName)) ([Windows.Storage.StorageFile])
   $stream=Await-WinRT ($file.OpenAsync([Windows.Storage.FileAccessMode]::Read)) ([Windows.Storage.Streams.IRandomAccessStream])
   $decoder=Await-WinRT ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)) ([Windows.Graphics.Imaging.BitmapDecoder])
   $bitmap=Await-WinRT ($decoder.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])
   $result=Await-WinRT ($engine.RecognizeAsync($bitmap)) ([Windows.Media.Ocr.OcrResult])
   $writer.WriteLine((@{page=[int]$pic.BaseName; text=$result.Text} | ConvertTo-Json -Compress));$writer.Flush()
   $bitmap.Dispose();$stream.Dispose()
   if(([int]$pic.BaseName)%50 -eq 0){Write-Output "$volume $($pic.BaseName)"}
  }
 } finally {$writer.Dispose()}
}
