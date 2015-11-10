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

for ($i = 0; $i < $test_cases_count; $i++){
	if ($digits[$i] < 3){
		print "-1\n";
	}
	else {
		// Maybe do for 5 and then 3 to see if there is a proper number of digits.

		// divisible by 5
		list($div_by_5, $mod_by_5) = divmod((int)$digits[$i], 5);
		// divisible by 3
		list($div_by_3, $mod_by_3) = divmod((int)$digits[$i], 3);
		print ("Divisible by 5 " . $div_by_5 . " mod " . $mod_by_5 . "\n");
		print ("Divisible by 3 " . $div_by_3 . " mod " . $mod_by_3 . "\n");
	}
}


function divmod($number, $divisor){
	$div = floor($number / $divisor);
	$mod = $number % $divisor;
	return array($div, $mod);
}


?>