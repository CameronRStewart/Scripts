#!/usr/bin/perl
use strict;
use DBI;
use Getopt::Std;
use utf8;
use Encode;
use Scalar::Util qw(looks_like_number);

my $dbh;
my $oclc_q;
my $author_q;
my $title_q;
my $sth;
my $rv;
my $delim_baseDir;
my $infile;
my $line;
my $a;
my $b;
my $c;
my $q;
my $z;
my $auth;
my $var_let;
my $string;
my $start;
my $end;
my $val;
my $bib_num;
my @author_array;
my $oclc_num;
my $lc_num;
my $some_num_1;
my $some_num_2;
my @title;
my $title_pt_a;
my $title_pt_b;
my $title_pt_c;
my $title_pt_q;
my $callnum_pt_a;
my $callnum_pt_c;
my $callnum_pt_h;
my $callnum_pt_i;
my $callnum_pt_l;
my $callnum_pt_n;
my $callnum;
my @callnum_array;
my $isxn_pt_a;
my $isxn_pt_y;
my $isxn_pt_z;
my @isxn_array;
my $notes_a;
my $notes_b;
my $notes_c;
my $notes_d;
my $notes;
my @notes_array;
my $isxn_q;
my $notes_q;
my $callnum_q;
my @barcode_array;
my $barcode_q;
my @location_array;
my $location_q;
my @entries;
my $entry;
my $cleanval;



$delim_baseDir = "/var/www/html/webenv/files_conv/broken";
$infile = "cswrholdingsbroken150218.txt";

opendir(SGMLDIR, "$delim_baseDir") or die "Can’t open $delim_baseDir:  $!";

@entries = readdir(SGMLDIR);

closedir(SGMLDIR);

foreach $entry (@entries) {
  if ($entry ne '.' && $entry ne '..') {
    open (SGMLFILE, "$delim_baseDir\/$entry") or die "Can't open $delim_baseDir\/$entry.";
	print "Reading file $entry\n";
    process_file();
    close SGMLFILE;
  }
}

sub process_file {
    while ($line = <SGMLFILE>) {
        # CLEAR VARIABLES AT LEADER
        if ($line =~ /^=LDR/) {
          #  undef $a;
          undef $auth;
          undef @author_array;
          undef @title;
          undef @callnum_array;
          undef @isxn_array;
          undef @notes_array;
          undef @barcode_array;
          undef @location_array;
        }
        # ISXN
        if ($line =~ /^=020|^=022/) {
            $isxn_pt_a = get_delim_value("a", $line);
            $isxn_pt_y = get_delim_value("y", $line);
            $isxn_pt_z = get_delim_value("z", $line);
            
            if ($isxn_pt_a && $isxn_pt_a ne '') {
                push(@isxn_array, $isxn_pt_a);
            }
            if ($isxn_pt_y && $isxn_pt_y ne '') {
                push(@isxn_array, $isxn_pt_y);
            }
            if ($isxn_pt_z && $isxn_pt_z ne '') {
                push(@isxn_array, $isxn_pt_z);
            }
        }
        # AUTHOR
        if ($line =~ /^=100|^=110|^=130|^=111|^=700|^=710|^=711|^=730/) {
            $auth = "";
            $title_pt_a = get_delim_value("a", $line);
            $title_pt_b = get_delim_value("b", $line);
            $title_pt_c = get_delim_value("c", $line);
            $title_pt_q = get_delim_value("q", $line);
            
            if ($title_pt_a && $title_pt_a ne '') {
                $auth .= $title_pt_a;
            }
            if ($title_pt_b && $title_pt_b ne '') {
                $auth .= " " . $title_pt_b;
            }
            if ($title_pt_c && $title_pt_c ne '') {
                $auth .= " " . $title_pt_c;
            }
            if ($title_pt_q && $title_pt_q ne '') {
                $auth .= " (" . $title_pt_q . ")";
            }
            if ($auth && $auth ne '') {
                push(@author_array, $auth);
            }
        }
        # CALL NUMBER
        if ($line =~ /^=945|^=949/) {
            $callnum = "";
            $callnum_pt_a = get_delim_value("a", $line); # call number pt. 1
            $callnum_pt_c = get_delim_value("c", $line); # call number pt. 2
            $callnum_pt_h = get_delim_value("h", $line); # call number pt. 3
            $callnum_pt_i = get_delim_value("i", $line); # barcode
            $callnum_pt_l = get_delim_value("l", $line); # location
            $callnum_pt_n = get_delim_value("n", $line); #call number pt. 4
            
            if ($callnum_pt_a && $callnum_pt_a ne '') {
                $callnum .= $callnum_pt_a;
            }
            if ($callnum_pt_c && $callnum_pt_c ne '') {
                $callnum .= " " . $callnum_pt_c;
            }
            if ($callnum_pt_h && $callnum_pt_h ne '') {
                $callnum .= " " . $callnum_pt_h;
            }
            if ($callnum_pt_n && $callnum_pt_n ne '') {
                $callnum .= " (" . $callnum_pt_n . ")";
            }
            if ($callnum && $callnum ne '') {
                push(@callnum_array, $callnum);
            }
            if ($callnum_pt_i && $callnum_pt_i ne '') {
                push(@barcode_array, $callnum_pt_i);
            }
            if ($callnum_pt_l && $callnum_pt_l ne '') {
                push(@location_array, $callnum_pt_l);
            }
        }
        # OCLC number pt. 1
        if ($line =~ /^=001/) {
            $oclc_num = substr($line, 6);
            $oclc_num =~ s/[\r\n]*//g; # line returns
            $oclc_num =~ s/[\s\/\\]*$//; # spaces and slash at end
        }
        # BIB NUMBER = full_record_id
        if ($line =~ /^=907/) {
            $bib_num = get_delim_value("a", $line);
            if ($bib_num && $bib_num ne '') { # Only need to save it for other inserts
                $bib_num =~ s/^.b//;
            }
			print "Grabbing info for bib#: $bib_num\n";
        }
        # TITLE 
        if ($line =~ /^=240|^=245|^=246/) {
            $a = get_delim_value("a", $line);
            $b = get_delim_value("b", $line);
            if ($a && $a ne '') {
                push(@title, $a . " " . $b);
            }
        }
        # NOTES 
        if ($line =~ /^=500|^=501|^=502|^=590|^=591|^=830/) {
            $notes = "";
            $notes_a = get_delim_value("a", $line);
            $notes_b = get_delim_value("b", $line);
            $notes_c = get_delim_value("c", $line);
            $notes_d = get_delim_value("d", $line);
            if ($notes_a && $notes_a ne '') {
                $notes .= $notes_a;
            }
            if ($notes_b && $notes_b ne '') {
                $notes .= $notes_b;
            }
            if ($notes_c && $notes_c ne '') {
                $notes .= $notes_c;
            }
            if ($notes_d && $notes_d ne '') {
                $notes .= $notes_d;
            }
            if ($notes && $notes ne '') {
                push(@notes_array, $notes);
            }
        }
            
    
        if ($line =~ /^[\r\n]+$/) {
            to_db();
        }
    }
}


# Sub declarations

sub to_db {
    if ($bib_num && $bib_num ne '') {
        $dbh = DBI->connect("DBI:mysql:database=libros;host=localhost","libros_user","librospass", {mysql_enable_utf8 => 1});
        if (!$dbh) { print 'could not connect to database';
            exit;
        }
		print "Inserting fields into database\n";
        $dbh->do('SET NAMES utf8');
        if ($oclc_num && $oclc_num ne '' && looks_like_number($oclc_num)) {
            $oclc_q = "insert into oclc_number (oclc_number_oclc_number, oclc_number_full_record_id) values ('$oclc_num', '$bib_num')";
            $sth = $dbh->prepare($oclc_q) or die "Can't prepare $oclc_q: $dbh->errstr\n";
            $rv = $sth->execute or die "can't execute the query: $sth->errstr\n";
        }
        if (@author_array && @author_array ne '') {
            foreach (@author_array) {
                $cleanval = alpha_num_it($_);
                $author_q = "insert into author (author_author, author_author_clean, author_full_record_id) values ('$_', '$cleanval', '$bib_num')";
                $sth = $dbh->prepare($author_q) or die "Can't prepare $author_q: $dbh->errstr\n";
                $rv = $sth->execute or die "can't execute the query: $sth->errstr\n$author_q\n";
            }
        }
        if (@title && @title ne '') {
            foreach (@title) {
                $cleanval = alpha_num_it($_);
                $title_q = "insert into title (title_title, title_title_clean, title_full_record_id) values ('$_', '$cleanval', '$bib_num')";
                $sth = $dbh->prepare($title_q) or die "Can't prepare $title_q: $dbh->errstr\n";
                $rv = $sth->execute or die "can't execute the query: $sth->errstr\n$title_q\n";
            }
        }
        if (@isxn_array && @isxn_array ne '') {
            foreach (@isxn_array) {
                $cleanval = alpha_num_it($_);
                $isxn_q = "insert into isxn (isxn_isxn, isxn_isxn_clean, isxn_full_record_id) values ('$_', '$cleanval', '$bib_num')";
                $sth = $dbh->prepare($isxn_q) or die "Can't prepare $isxn_q: $dbh->errstr\n";
                $rv = $sth->execute or die "can't execute the query: $sth->errstr\n$isxn_q\n";
            }
        }
        if (@notes_array && @notes_array ne '') {
            foreach (@notes_array) {
                $cleanval = alpha_num_it($_);
                $notes_q = "insert into notes (notes_notes, notes_notes_clean, notes_full_record_id) values ('$_', '$cleanval', '$bib_num')";
                $sth = $dbh->prepare($notes_q) or die "Can't prepare $notes_q: $dbh->errstr\n";
                $rv = $sth->execute or die "can't execute the query: $sth->errstr\n$notes_q\n";
            }
        }
        if (@callnum_array && @callnum_array ne '') {
            foreach (@callnum_array) {
                $cleanval = alpha_num_it($_);
                $cleanval =~ s/[\s]//g;
                $callnum_q = "insert into call_number (call_number_call_number, call_number_call_number_clean, call_number_full_record_id) values ('$_', '$cleanval', '$bib_num')";
                $sth = $dbh->prepare($callnum_q) or die "Can't prepare $callnum_q: $dbh->errstr\n";
                $rv = $sth->execute or die "can't execute the query: $sth->errstr\n$callnum_q\n";
            }
        }
        if (@barcode_array && @barcode_array ne '') {
            foreach (@barcode_array) {
                $barcode_q = "insert into barcode (barcode_barcode, barcode_full_record_id) values ('$_', '$bib_num')";
                $sth = $dbh->prepare($barcode_q) or die "Can't prepare $barcode_q: $dbh->errstr\n";
                $rv = $sth->execute or die "can't execute the query: $sth->errstr\n$barcode_q\n";
            }
        }
        if (@location_array && @location_array ne '') {
            foreach (@location_array) {
                $location_q = "insert into location (location_location, location_full_record_id) values ('$_', '$bib_num')";
                $sth = $dbh->prepare($location_q) or die "Can't prepare $location_q: $dbh->errstr\n";
                $rv = $sth->execute or die "can't execute the query: $sth->errstr\n$location_q\n";
            }
        }
        $dbh->disconnect;
 
    }
}

sub get_delim_value { # Values passed are delimiter letter and $line
    $var_let = '$' . $_[0];
    $string = $_[1];
    $start = index($string, $var_let) + 2;
    if ($start != 1) {
        $end = index($string, '$', $start);
        if ($end != -1) {
            $val = substr($string, $start, $end - $start);
        } else {
            $val = substr($string, $start);
        }
        # Take out unnecessary characters, etc.
        $val =~ s/\n//g; # line returns
        $val =~ s/'//g; # single quotes
        $val =~ s/[\s\/\\]+$//; # spaces, slashes and backslashes at end
        $val =~ s/\s+:/:/g; # spaces in front of colons
        $val =~ s/{aelig}/ae/g; # 
        $val =~ s/{AElig}/AE/g; # 
        $val =~ s/{Dstrok}/D/g; # 
        $val =~ s/{lstrok}/l/g; # 
        $val =~ s/{Lstrok}/L/g; # 
        $val =~ s/{oelig}/oe/g; # 
        $val =~ s/{OElig}/OE/g; # 
        $val =~ s/{ostrok}/o/g; # 
        $val =~ s/{Ostrok}/O/g; # 
        $val =~ s/{uhorn}/u/g; # 
        $val =~ s/\s\s+/\s/g; # 
        
        $val =~ s/{[^}]*}//g; # 
        $val =~ s/{}//g; # 
        $val =~ s/{}//g; # 
        $val =~ s/{}//g; # 
        
        if ($val =~ /{/ && $val !~ /esc}/) {
            print "$val\n";
        }
    } else {
        $val = "";
    }
    
    return $val;
}

sub alpha_num_it {
    $val = $_[0];
    $val =~ s/[^a-zA-Z0-9\s]//g;
    return $val;
}






# Insert query:
# insert into article(collection_id,year,author,title,volume,abstract,subject,pdf_url,djvu_url,html_url,body,volume_number,issue_number,issue_period)
# values($CID,$qdat,$qaut,$qtit,$qvol,$qabs,$qsub,$qpdf,$qdjv,$qhtm,$qtxt,$qvoln,$qissn,$qissp)



