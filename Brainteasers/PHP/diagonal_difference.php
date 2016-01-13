<?php
$_fp = fopen("php://stdin", "r");
/* Enter your code here. Read input from STDIN. Print output to STDOUT */

$index = 0;
$count = fgets($_fp);
$sum1 = 0;
$sum2 = 0;
$matrix = [];

while($index < $count) {
    $line = fgets($_fp);
    $matrix[] = explode(" ", $line);
    $index++;
}

$index = 0;
foreach($matrix as $row){
    $addend1[] =  $row[$index];
    $sum1 += $row[$index];
    $reverse_diag_index = ($count - $index) - 1;
    $addend2[] = $row[$reverse_diag_index];
    $sum2 += $row[$reverse_diag_index];
    $index++;
}

print_r($addend1);
print_r($addend2);
print abs($sum1 - $sum2);
   


?>