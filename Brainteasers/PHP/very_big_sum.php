<?php
$_fp = fopen("php://stdin", "r");
/* Enter your code here. Read input from STDIN. Print output to STDOUT */
$count = fgets($_fp);
$nums = explode(" ", fgets($_fp));

$carry = 0;
$total = [];

$num_len = strlen($nums[0]);
for($i = $num_len - 1; $i >= 0; $i--) {
    $sum += $carry;
    foreach($nums as $num){
        $sum += $num[$i];
    }
    $carry = floor($sum / 10);
    array_unshift($total, $sum % 10); 
    $sum = 0;
}
if($carry > 0){
	array_unshift($total, $carry);
}

print implode("", $total);
    
?>