<?php
$_fp = fopen("php://stdin", "r");
/* Enter your code here. Read input from STDIN. Print output to STDOUT */

$count = fgets($_fp);
$nums = explode(" ", fgets($_fp));
$pos = 0;
$neg = 0;
$zero = 0;

foreach ($nums as $num) {
	if($num == 0){
		$zero++;
	}
	elseif($num < 0){
		$neg++;
	}
	else {
		$pos++;
	}
}

sprintf ("%.2f", $a);

$ratio_zero = sprintf("%.3f", ($zero / $count), 3);
$ratio_pos = sprintf("%.3f", ($pos / $count), 3);
$ratio_neg = sprintf("%.3f", ($neg / $count), 3);

print $ratio_pos . "\n";
print $ratio_neg . "\n";
print $ratio_zero . "\n";

?>