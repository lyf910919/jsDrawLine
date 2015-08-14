<?php
	$myJson = json_decode(file_get_contents('php://input'), true);
	$userName = $myJson['userName'];
	$musicNumber = $myJson['musicNumber'];
	$strokes = $myJson['strokes'];
	$img = $myJson['img'];
	//echo $userName.'\n'.$musicNumber.'\n'.$strokes.'\n'.$img;
	
	//save stroke
	$fileName = $userName."_".$musicNumber.".txt";
	$logFile = fopen($fileName, "w") or die("unable to open file");
	fwrite($logFile, $strokes);
	fclose($logFile);

	//save image
	$uri = substr($img, strpos($img, ",") + 1);
	$uri = str_replace(' ', '+', $uri);
	$decodeData = base64_decode($uri);
	$fileName = $userName."_".$musicNumber.".jpg";
	$logFile = fopen($fileName, "wb") or die("unable to open file");
	fwrite($logFile, $decodeData);
	fclose($logFile);
	echo "图片已保存！进入下一首歌";
?>