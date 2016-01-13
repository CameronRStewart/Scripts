<?php
$_fp = fopen("php://stdin", "r");
/* Enter your code here. Read input from STDIN. Print output to STDOUT */

$steps = fgets($_fp);

for($i = 0; $i < $steps; $i++) {
    for($j = 1; $j < ($steps - $i); $j++) {
        print " ";
    }
    for($k = 0; $k <= $i; $k++ ){
        print "#";
    }
    print "\n";
}

?>