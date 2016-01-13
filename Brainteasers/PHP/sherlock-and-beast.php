<?php

/**
A Decent Number has the following properties:

3, 5, or both as its digits. No other digit is allowed.
Number of times 3 appears is divisible by 5.
Number of times 5 appears is divisible by 3.
**/

$_fp = fopen("php://stdin", "r");
/* Enter your code here. Read input from STDIN. Print output to STDOUT */

$test_cases_count = fgets($_fp);
$digits = [];
for ($i = 0; $i < $test_cases_count; $i++){
	$digits[] = fgets($_fp);
}

foreach ($digits as $digit){
	if($digit < 3) {
		print "-1\n";
		continue;
	}
	list($div_by_3, $mod_by_3) = divmod($digit, 3);
	$count = $div_by_3;
	//print " div_by_3: " . $div_by_3 . " mod_by_3: " . $mod_by_3 . "\n";
	for($i = 0; $i <= $count; $i++){

		$new_div_by_3 = $div_by_3 - $i;
		$new_mod_by_3 = $mod_by_3 + (3 * $i);
		//print " div_by_3: " . $new_div_by_3 . " mod_by_3: " . $new_mod_by_3 . "\n";


		if($new_mod_by_3 == 0){
			$threes = 0;
			$fives = $new_div_by_3 * 3;
			print_decent_numbers($threes, $fives);
			break;
		}
		else{
			if($new_mod_by_3 >= 5) {
				list($div_by_5, $mod_by_5) = divmod($new_mod_by_3, 5);
				//print "mod_by_3: " . $new_mod_by_3 . " div_by_5: " . $div_by_5 . " mod_by_5: " . $mod_by_5 . "\n";
				if ($mod_by_5 == 0){
					$threes = $div_by_5 * 5;
					$fives = $new_div_by_3 * 3;
					print_decent_numbers($threes, $fives);
					break;
				}
			}
			if ($i == $count) {
				print "-1\n";
				break;
			}
		}
	}
}

function print_decent_numbers($threes, $fives) {
	if($threes == 0 && $fives == 0){
		print "-1\n";
		return;
	}
	for ($i = 0; $i < $fives; $i++){
		print '5';
	}
	for ($i = 0; $i < $threes; $i++){
		print '3';
	}
	print "\n";
}

function divmod($number, $divisor){
	$div = floor($number / $divisor);
	$mod = $number % $divisor;
	return array($div, $mod);
}


?>