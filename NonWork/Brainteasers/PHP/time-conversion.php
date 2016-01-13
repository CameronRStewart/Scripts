<?php
$_fp = fopen("php://stdin", "r");
/* Enter your code here. Read input from STDIN. Print output to STDOUT */

// This will give us an array that looks like: [hh, mm, ssPM]
$time_array = explode(":", fgets($_fp));
$hours = $time_array[0];
$minutes = $time_array[1];
$seconds_plus = $time_array[2];
$am_or_pm = strpos($seconds_plus, 'AM') ? 'AM' : 'PM';

if($am_or_pm == 'AM') {
    $seconds = str_replace("AM", "", $seconds_plus);
    if($hours == '12') {
        $hours = '00';
    }
}
else { //PM
    $seconds = str_replace("PM", "", $seconds_plus);
    $hours = $hours == '12' ? '12' : (int)$hours + 12;
}

print $hours . ":" . $minutes . ":" . $seconds;


?>