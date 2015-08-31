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

	if ($musicNumber <= 4)
	{
		if ($musicNumber == 4)
		{
			$param = $userName." ".$userName."_1.txt ".$userName."_2.txt ". 
			$userName."_3.txt ".$userName."_4.txt";
			//call backend.py -learn stroke/...
			exec("python backend.py -learn ".$param, $output, $return);
		}
		$response_array['status'] = 'success';
		$response_array['message'] = '图片已保存！进入下一首歌';
		$response_array['return'] = $output;
	}
	else if ($musicNumber > 4)
	{
		//call backend.py -recommend stroke/...
		exec("python backend.py -recommend ".$userName." ".$userName."_".$musicNumber.".txt", $output, $return);
		$recommendInd = $output[1];
		$response_array['status'] = 'success';
		$response_array['recommend'] = $recommendInd;
		$response_array['return'] = $return;
	}
	
	header('Content-type: application/json');
	echo json_encode($response_array)
	// echo "图片已保存！进入下一首歌";
?>