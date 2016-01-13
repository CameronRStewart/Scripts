// File to host various functions used to brush up on some basic JS skills.
// These are VERY basic.  Im just playing around.

function reverseStringRecursive(str) {
    if (str.length === 0) {
        return "";
    } else if (str.length == 1) {
        return str[0];
    } else {
        return reverseString(str.substring(1)) + str[0];
    }
}

function reverseStringIterative(str) {
    var new_string = "";
    var num = str.length;
    for (var i=0; i<num; i++) {
        index = (+num - +i) - 1;
        new_string = new_string + str[index]; 
    }
    return new_string;
}




function go() {
    var rev_string = document.getElementById('myTextField').value;

    var new_string_iter = reverseStringIterative(rev_string);
    var new_string_rec = reverseStringRecursive(rev_string);


    var out = document.getElementById('myTextField');
    out.value = new_string;
}