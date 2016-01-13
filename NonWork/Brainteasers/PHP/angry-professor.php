<?php
$_fp = fopen("php://stdin", "r");
/* Enter your code here. Read input from STDIN. Print output to STDOUT */
$test_cases_number = fgets($_fp);

for($i = 0; $i < $test_cases_number; $i++){
	$total_and_expected_students = explode(" ", fgets($_fp));
    $students_count[] = $total_and_expected_students[0];
    $expected_students[] = $total_and_expected_students[1];
    $student_times[] = explode(" ", fgets($_fp));  
}



for($i = 0; $i < $test_cases_number; $i++){
	$on_time = 0;
	$late = 0;

	for ($j = 0; $j < sizeof($student_times[$i]); $j++){
		if ($student_times[$i][$j] <= 0){
			$on_time++;
		}
		else {
			$late++;
		}

		// if fewer than k ($expected_students[$i]) break and print.  If N - late < k
		if(($students_count[$i] - $late) < $expected_students[$i]) {
			print "YES\n";
			break;
		}
		// Or if k students are already on time.
		if ($on_time >= $expected_students[$i]) {
			print "NO\n";
			break;
		}
	}
}



?>